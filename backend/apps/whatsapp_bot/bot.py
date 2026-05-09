"""
Twilio send helper + thin orchestrator.
The heavy state logic lives in state_machine.py.
"""
from django.conf import settings


def send_whatsapp_message(to: str, body: str) -> str:
    """
    Send an outbound WhatsApp message via Twilio.
    Returns the Twilio message SID, or empty string on failure.

    `to` must be in Twilio's format: 'whatsapp:+919999999999'
    If it doesn't have the prefix we add it automatically.
    """
    if not to.startswith('whatsapp:'):
        to = f'whatsapp:{to}'

    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_=settings.TWILIO_WHATSAPP_FROM,
            to=to,
            body=body,
        )
        return message.sid
    except Exception as exc:
        # Log but don't crash — the TwiML response already delivers the reply
        import logging
        logging.getLogger(__name__).warning('Twilio send failed: %s', exc)
        return ''


def process_incoming(from_number: str, body: str, media_url: str = '') -> str:
    """
    Entry point called by the webhook view.
    Returns the reply text to be wrapped in TwiML.
    """
    from .state_machine import handle_message
    return handle_message(from_number, body, media_url)
