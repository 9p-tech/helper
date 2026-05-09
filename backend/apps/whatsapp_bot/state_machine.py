import logging
from datetime import timedelta

from django.utils import timezone

from apps.claims.models import Claim, ClaimFile
from apps.orders.models import Order
from apps.verification.decision_engine import run_verification
from apps.verification.utils import download_twilio_media
from .models import ConversationSession, WhatsAppMessage
from . import messages as msg

_logger = logging.getLogger(__name__)


def handle_message(phone: str, body: str, media_url: str = '') -> str:
    session, _ = ConversationSession.objects.get_or_create(customer_phone=phone)

    WhatsAppMessage.objects.create(
        session=session,
        direction=WhatsAppMessage.INBOUND,
        message_body=body,
        media_url=media_url,
    )

    body_clean = body.strip().upper()
    response = _route(session, body_clean, body.strip(), media_url)

    WhatsAppMessage.objects.create(
        session=session,
        direction=WhatsAppMessage.OUTBOUND,
        message_body=response,
    )

    return response


def _route(session: ConversationSession, body_upper: str, body_raw: str, media_url: str) -> str:
    state = session.current_state

    if body_upper in ('HI', 'HELLO', 'START', 'HEY'):
        session.current_state = ConversationSession.STATE_INITIAL
        session.save()
        return msg.GREETING

    if body_upper.startswith('STATUS '):
        return _handle_status(body_upper[7:].strip())

    if state == ConversationSession.STATE_INITIAL:
        if body_upper == 'REPLACE':
            session.current_state = ConversationSession.STATE_AWAITING_ORDER_ID
            session.save()
            return msg.ASK_ORDER_ID
        return msg.GREETING

    if state == ConversationSession.STATE_AWAITING_ORDER_ID:
        return _handle_order_id(session, body_raw)

    if state == ConversationSession.STATE_AWAITING_DAMAGE_PHOTO:
        return _handle_damage_photo(session, media_url)

    if state == ConversationSession.STATE_AWAITING_INVOICE:
        return _handle_invoice(session, media_url)

    if state in (ConversationSession.STATE_DECISION_MADE, ConversationSession.STATE_ABANDONED):
        session.current_state = ConversationSession.STATE_INITIAL
        session.save()
        return msg.GREETING

    return msg.GREETING


def _handle_status(order_id: str) -> str:
    try:
        order = Order.objects.get(id=order_id.upper())
        return msg.STATUS_FOUND.format(
            order_id=order.id,
            status=order.get_status_display(),
            item_count=order.items.count(),
            total=order.total_amount,
        )
    except Order.DoesNotExist:
        return msg.STATUS_NOT_FOUND.format(order_id=order_id)


def _handle_order_id(session: ConversationSession, order_id: str) -> str:
    try:
        order = Order.objects.get(id=order_id.upper())
    except Order.DoesNotExist:
        return msg.ORDER_NOT_FOUND.format(order_id=order_id)

    phone_clean = session.customer_phone.replace('whatsapp:', '').strip()
    if order.whatsapp_number != phone_clean:
        return msg.PHONE_MISMATCH

    reference_date = order.delivered_at or order.created_at
    days_elapsed = (timezone.now() - reference_date).days
    in_window = timezone.now() <= reference_date + timedelta(days=order.replacement_window_days)
    _logger.info(
        '[WhatsApp] order=%s ref=%s elapsed=%sd in_window=%s',
        order.id, reference_date.date(), days_elapsed, in_window,
    )
    if not in_window:
        return msg.WINDOW_CLOSED.format(
            days=order.replacement_window_days,
            order_id=order.id,
        )

    existing = Claim.objects.filter(order=order, status__in=[
        Claim.STATUS_PENDING, Claim.STATUS_IN_PROGRESS, Claim.STATUS_APPROVED
    ]).first()
    if existing:
        return msg.CLAIM_EXISTS.format(
            order_id=order.id,
            claim_id=existing.id,
            status=existing.get_status_display(),
        )

    claim = Claim.objects.create(
        order=order,
        customer_phone=phone_clean,
        reason_text='Raised via WhatsApp bot',
    )
    session.active_claim = claim
    session.context_data = {'order_id': order.id}
    session.current_state = ConversationSession.STATE_AWAITING_DAMAGE_PHOTO
    session.save()
    return msg.ORDER_VERIFIED.format(order_id=order.id)


def _handle_damage_photo(session: ConversationSession, media_url: str) -> str:
    if not media_url:
        return msg.NEED_DAMAGE_PHOTO

    claim = session.active_claim
    if not claim:
        session.current_state = ConversationSession.STATE_INITIAL
        session.save()
        return msg.ERROR_NO_ACTIVE_CLAIM

    file_path = download_twilio_media(media_url, 'damage_photos')
    if file_path:
        cf = ClaimFile(claim=claim, file_type=ClaimFile.DAMAGE_PHOTO)
        cf.file.name = file_path
        cf.file_size = 0
        cf.save()

    session.current_state = ConversationSession.STATE_AWAITING_INVOICE
    session.save()
    return msg.DAMAGE_PHOTO_RECEIVED


def _handle_invoice(session: ConversationSession, media_url: str) -> str:
    if not media_url:
        return msg.NEED_INVOICE

    claim = session.active_claim
    if not claim:
        session.current_state = ConversationSession.STATE_INITIAL
        session.save()
        return msg.ERROR_NO_ACTIVE_CLAIM

    file_path = download_twilio_media(media_url, 'invoices')
    if file_path:
        cf = ClaimFile(claim=claim, file_type=ClaimFile.INVOICE)
        cf.file.name = file_path
        cf.file_size = 0
        cf.save()

    claim.status = Claim.STATUS_IN_PROGRESS
    claim.save()
    session.current_state = ConversationSession.STATE_DECISION_MADE
    session.save()

    result = run_verification(claim)

    if result.recommendation == 'APPROVED':
        claim.status = Claim.STATUS_APPROVED
        claim.save()
        return msg.APPROVED.format(claim_id=claim.id)
    elif result.recommendation == 'REJECTED':
        claim.status = Claim.STATUS_REJECTED
        claim.save()
        reason = getattr(result, '_rejection_reason', 'Verification could not be completed.')
        return msg.REJECTED.format(
            reason=reason,
            claim_id=claim.id,
        )
    else:
        return msg.MANUAL_REVIEW.format(claim_id=claim.id)
