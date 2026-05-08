import os
from django.conf import settings
from apps.claims.models import Claim, ClaimFile, VerificationResult
from .ml_interface import detect_damage, check_authentic
from .ocr import extract_invoice_data
from .fraud_check import check_duplicate_image


def run_verification(claim: Claim) -> VerificationResult:
    order = claim.order

    phone_clean = claim.customer_phone.replace('whatsapp:', '').strip()
    phone_matched = order.whatsapp_number == phone_clean
    order_in_window = order.is_in_replacement_window()

    damage_result = {'damage_detected': False, 'damage_type': 'none', 'severity': 'low', 'confidence': 0.0}
    authentic_result = {'is_authentic': False, 'confidence': 0.0, 'flags': []}
    duplicate_result = {'duplicate_found': False, 'duplicate_claim_id': ''}

    damage_photo = claim.files.filter(file_type=ClaimFile.DAMAGE_PHOTO).first()
    if damage_photo and damage_photo.file:
        img_path = os.path.join(settings.MEDIA_ROOT, str(damage_photo.file))
        if os.path.exists(img_path):
            damage_result = detect_damage(img_path)
            authentic_result = check_authentic(img_path)
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
        authenticity_confidence=authentic_result['confidence'],
        invoice_matched=invoice_matched,
        duplicate_found=duplicate_result['duplicate_found'],
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

    if recommendation == 'APPROVED':
        claim.status = Claim.STATUS_APPROVED
    elif recommendation == 'REJECTED':
        claim.status = Claim.STATUS_REJECTED
    else:
        claim.status = Claim.STATUS_MANUAL_REVIEW
    claim.save()

    return result


def _decide(
    phone_matched: bool,
    order_in_window: bool,
    damage_detected: bool,
    damage_confidence: float,
    is_authentic: bool,
    authenticity_confidence: float,
    invoice_matched: bool,
    duplicate_found: bool,
) -> tuple:
    if duplicate_found:
        return VerificationResult.REC_REJECTED, 0.95

    if not phone_matched:
        return VerificationResult.REC_REJECTED, 0.99

    if not order_in_window:
        return VerificationResult.REC_REJECTED, 0.99

    if not damage_detected or damage_confidence < 0.5:
        return VerificationResult.REC_REJECTED, 0.80

    score = 0.0
    score += damage_confidence * 0.4
    score += authenticity_confidence * 0.3
    score += (0.3 if invoice_matched else 0.0)

    if score >= 0.75 and is_authentic:
        return VerificationResult.REC_APPROVED, score
    elif score >= 0.5:
        return VerificationResult.REC_MANUAL, score
    else:
        return VerificationResult.REC_REJECTED, 1.0 - score
