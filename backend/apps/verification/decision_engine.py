import os
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from apps.claims.models import Claim, ClaimFile, VerificationResult
from .ml_interface import detect_damage, check_authentic, match_product
from .ocr import extract_invoice_data
from .fraud_check import check_duplicate_image


def run_verification(claim: Claim) -> VerificationResult:
    order = claim.order

    phone_clean = claim.customer_phone.replace('whatsapp:', '').strip()
    phone_matched = order.whatsapp_number == phone_clean

    reference_date = order.delivered_at or order.created_at
    order_in_window = timezone.now() <= reference_date + timedelta(days=order.replacement_window_days)

    damage_result = {'damage_detected': False, 'damage_type': 'none', 'severity': 'low', 'confidence': 0.0}
    authentic_result = {'is_authentic': False, 'confidence': 0.0, 'flags': []}
    match_result = {'is_same_product': True, 'similarity_score': 1.0, 'matched_attributes': [], 'mismatched_attributes': [], 'reason': ''}
    duplicate_result = {'duplicate_found': False, 'duplicate_claim_id': ''}

    damage_photo = claim.files.filter(file_type=ClaimFile.DAMAGE_PHOTO).first()
    if damage_photo and damage_photo.file:
        img_path = os.path.join(settings.MEDIA_ROOT, str(damage_photo.file))
        if os.path.exists(img_path):
            damage_result = detect_damage(img_path)
            authentic_result = check_authentic(img_path)
            match_result = match_product(img_path, order)
            duplicate_result = check_duplicate_image(img_path, claim.id)

    ocr_result = {'raw_text': '', 'order_id_found': '', 'date_found': ''}
    invoice_matched = False
    invoice_file = claim.files.filter(file_type=ClaimFile.INVOICE).first()
    if invoice_file and invoice_file.file:
        inv_path = os.path.join(settings.MEDIA_ROOT, str(invoice_file.file))
        if os.path.exists(inv_path):
            ocr_result = extract_invoice_data(inv_path)
            invoice_matched = (ocr_result['order_id_found'] == order.id)

    recommendation, confidence_score = _decide(
        phone_matched=phone_matched,
        order_in_window=order_in_window,
        damage_detected=damage_result['damage_detected'],
        damage_confidence=damage_result['confidence'],
        is_authentic=authentic_result['is_authentic'],
        is_same_product=match_result['is_same_product'],
        similarity_score=match_result['similarity_score'],
        duplicate_found=duplicate_result['duplicate_found'],
    )

    print(f"\n========== DECISION ENGINE ==========")
    print(f"[DEBUG] damage result: {damage_result}")
    print(f"[DEBUG] authenticity result: {authentic_result}")
    print(f"[DEBUG] product match result: {match_result}")
    print(f"[DEBUG] phone_matched: {phone_matched}, order_in_window: {order_in_window}")
    print(f"[DEBUG] Final recommendation: {recommendation}")

    rejection_reason = _get_rejection_reason(
        recommendation=recommendation,
        duplicate_found=duplicate_result['duplicate_found'],
        duplicate_claim_id=duplicate_result['duplicate_claim_id'],
        phone_matched=phone_matched,
        order_in_window=order_in_window,
        damage_detected=damage_result['damage_detected'],
        is_same_product=match_result['is_same_product'],
        similarity_score=match_result['similarity_score'],
        is_authentic=authentic_result['is_authentic'],
        damage_confidence=damage_result['confidence'],
    )

    result = VerificationResult.objects.create(
        claim=claim,
        phone_matched=phone_matched,
        order_in_window=order_in_window,
        damage_detected=damage_result['damage_detected'],
        damage_type=damage_result['damage_type'],
        damage_severity=damage_result['severity'].upper(),
        damage_confidence=damage_result['confidence'],
        is_authentic=authentic_result['is_authentic'],
        authenticity_confidence=authentic_result['confidence'],
        authenticity_flags=authentic_result['flags'],
        invoice_ocr_raw_text=ocr_result['raw_text'],
        invoice_order_id_found=ocr_result['order_id_found'],
        invoice_date_found=ocr_result['date_found'],
        invoice_matched=invoice_matched,
        duplicate_image_found=duplicate_result['duplicate_found'],
        duplicate_claim_id=duplicate_result['duplicate_claim_id'],
        recommendation=recommendation,
        confidence_score=confidence_score,
    )

    result._rejection_reason = rejection_reason

    if recommendation == 'APPROVED':
        claim.status = Claim.STATUS_APPROVED
    elif recommendation == 'REJECTED':
        claim.status = Claim.STATUS_REJECTED
    else:
        claim.status = Claim.STATUS_MANUAL_REVIEW
    claim.save()

    return result


def _get_rejection_reason(
    recommendation: str,
    duplicate_found: bool,
    duplicate_claim_id: str,
    phone_matched: bool,
    order_in_window: bool,
    damage_detected: bool,
    is_same_product: bool,
    similarity_score: float,
    is_authentic: bool,
    damage_confidence: float,
) -> str:
    if recommendation == VerificationResult.REC_APPROVED:
        return ''
    if duplicate_found:
        ref = f' (Claim ID: {duplicate_claim_id})' if duplicate_claim_id else ''
        return f'This photo was already used in a previous claim{ref}. Please submit a new photo.'
    if not phone_matched:
        return 'This order is not registered to your WhatsApp number.'
    if not order_in_window:
        return 'The 7-day replacement window for this order has closed.'
    if not is_same_product:
        return 'The item in the photo does not appear to match the ordered product.'
    if similarity_score < 0.6:
        return 'Low product match confidence — sent for manual review.'
    if not is_authentic:
        return 'The photo appears to be edited or AI-generated. Please send an original photo.'
    if not damage_detected:
        return 'No visible damage was detected in the submitted photo.'
    if damage_confidence < 0.5:
        return 'Damage confidence too low — sent for manual review.'
    return 'Verification could not be completed. Please contact support.'


def _decide(
    phone_matched: bool,
    order_in_window: bool,
    damage_detected: bool,
    damage_confidence: float,
    is_authentic: bool,
    is_same_product: bool,
    similarity_score: float,
    duplicate_found: bool,
) -> tuple:
    # Hard failures — immediate reject
    if duplicate_found:
        return VerificationResult.REC_REJECTED, 0.95

    if not phone_matched:
        return VerificationResult.REC_REJECTED, 0.99

    if not order_in_window:
        return VerificationResult.REC_REJECTED, 0.99

    # Rule 1: product doesn't match → manual review (not hard reject — damage alters appearance)
    if not is_same_product:
        return VerificationResult.REC_MANUAL, 0.70

    # Rule 2: low similarity → manual
    if similarity_score < 0.6:
        return VerificationResult.REC_MANUAL, similarity_score

    # Rule 3: authenticity suspect → manual
    if not is_authentic:
        return VerificationResult.REC_MANUAL, 0.60

    # Rule 4: no damage detected → reject
    if not damage_detected:
        return VerificationResult.REC_REJECTED, 0.80

    # Rule 5: low damage confidence → manual
    if damage_confidence < 0.5:
        return VerificationResult.REC_MANUAL, damage_confidence

    # Rule 6: all checks passed → approve
    return VerificationResult.REC_APPROVED, damage_confidence
