from django.utils import timezone
from apps.claims.models import Claim, ClaimFile
from apps.orders.models import Order
from apps.verification.decision_engine import run_verification
from apps.verification.utils import download_twilio_media
from .models import ConversationSession, WhatsAppMessage

GREETING = (
    "👋 Hi! Welcome to Snitch support.\n\n"
    "To raise a replacement request, reply *REPLACE*.\n"
    "For order status, reply *STATUS <order_id>*."
)

WELCOME_REPLACE = (
    "Got it! Let's start your replacement request.\n\n"
    "Please send your *Order ID* (e.g. SN260509ABCD)."
)

ASK_DAMAGE_PHOTO = (
    "✅ Order found and verified!\n\n"
    "Now please send a *clear photo of the damaged item*."
)

ASK_INVOICE = (
    "📸 Photo received!\n\n"
    "Now please send a photo of the *invoice/packing slip* that came with the order."
)

PROCESSING = "⏳ Processing your claim... please wait a moment."

APPROVED_MSG = (
    "✅ *Claim Approved!*\n\n"
    "Your replacement has been initiated. You'll receive a confirmation shortly.\n"
    "Claim ID: {claim_id}"
)

REJECTED_MSG = (
    "❌ *Claim Rejected*\n\n"
    "Reason: {reason}\n\n"
    "If you think this is a mistake, contact support@snitch.in"
)

MANUAL_MSG = (
    "🔍 Your claim is under *manual review*.\n\n"
    "Our team will contact you within 24 hours.\n"
    "Claim ID: {claim_id}"
)


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
        return GREETING

    if body_upper.startswith('STATUS '):
        return _handle_status(body_upper[7:].strip())

    if state == ConversationSession.STATE_INITIAL:
        if body_upper == 'REPLACE':
            session.current_state = ConversationSession.STATE_AWAITING_ORDER_ID
            session.save()
            return WELCOME_REPLACE
        return GREETING

    if state == ConversationSession.STATE_AWAITING_ORDER_ID:
        return _handle_order_id(session, body_raw)

    if state == ConversationSession.STATE_AWAITING_DAMAGE_PHOTO:
        return _handle_damage_photo(session, media_url)

    if state == ConversationSession.STATE_AWAITING_INVOICE:
        return _handle_invoice(session, media_url)

    if state in (ConversationSession.STATE_DONE, ConversationSession.STATE_ABANDONED):
        session.current_state = ConversationSession.STATE_INITIAL
        session.save()
        return GREETING

    return GREETING


def _handle_status(order_id: str) -> str:
    try:
        order = Order.objects.get(id=order_id.upper())
        return (
            f"📦 Order *{order.id}*\n"
            f"Status: *{order.get_status_display()}*\n"
            f"Items: {order.items.count()}\n"
            f"Total: ₹{order.total_amount}"
        )
    except Order.DoesNotExist:
        return f"❌ Order *{order_id}* not found. Please check the ID and try again."


def _handle_order_id(session: ConversationSession, order_id: str) -> str:
    try:
        order = Order.objects.get(id=order_id.upper())
    except Order.DoesNotExist:
        return f"❌ Order *{order_id}* not found. Please check and try again."

    phone_clean = session.customer_phone.replace('whatsapp:', '').strip()
    if order.whatsapp_number != phone_clean:
        return "❌ This order is not associated with your WhatsApp number."

    if not order.is_in_replacement_window():
        return (
            f"⏰ Sorry, the {order.replacement_window_days}-day replacement window for order "
            f"*{order.id}* has closed."
        )

    existing = Claim.objects.filter(order=order, status__in=[
        Claim.STATUS_PENDING, Claim.STATUS_IN_PROGRESS, Claim.STATUS_APPROVED
    ]).first()
    if existing:
        return f"⚠️ A claim already exists for this order (ID: {existing.id})."

    claim = Claim.objects.create(
        order=order,
        customer_phone=phone_clean,
        reason_text='Raised via WhatsApp bot',
    )
    session.active_claim = claim
    session.context_data = {'order_id': order.id}
    session.current_state = ConversationSession.STATE_AWAITING_DAMAGE_PHOTO
    session.save()
    return ASK_DAMAGE_PHOTO


def _handle_damage_photo(session: ConversationSession, media_url: str) -> str:
    if not media_url:
        return "📸 Please send a *photo* of the damaged item (not text)."

    claim = session.active_claim
    if not claim:
        session.current_state = ConversationSession.STATE_INITIAL
        session.save()
        return "Something went wrong. Please start again by typing REPLACE."

    file_path = download_twilio_media(media_url, 'damage_photos')
    if file_path:
        cf = ClaimFile(claim=claim, file_type=ClaimFile.DAMAGE_PHOTO)
        cf.file.name = file_path
        cf.file_size = 0
        cf.save()

    session.current_state = ConversationSession.STATE_AWAITING_INVOICE
    session.save()
    return ASK_INVOICE


def _handle_invoice(session: ConversationSession, media_url: str) -> str:
    if not media_url:
        return "📄 Please send a *photo of your invoice/packing slip*."

    claim = session.active_claim
    if not claim:
        session.current_state = ConversationSession.STATE_INITIAL
        session.save()
        return "Something went wrong. Please start again by typing REPLACE."

    file_path = download_twilio_media(media_url, 'invoices')
    if file_path:
        cf = ClaimFile(claim=claim, file_type=ClaimFile.INVOICE)
        cf.file.name = file_path
        cf.file_size = 0
        cf.save()

    claim.status = Claim.STATUS_IN_PROGRESS
    claim.save()
    session.current_state = ConversationSession.STATE_DONE
    session.save()

    result = run_verification(claim)

    if result.recommendation == 'APPROVED':
        return APPROVED_MSG.format(claim_id=claim.id)
    elif result.recommendation == 'REJECTED':
        return REJECTED_MSG.format(reason='Verification failed. Product damage not confirmed.')
    else:
        return MANUAL_MSG.format(claim_id=claim.id)
