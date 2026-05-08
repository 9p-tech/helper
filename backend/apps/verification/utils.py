import os
import uuid
import requests
from django.conf import settings


def download_twilio_media(media_url: str, subfolder: str) -> str:
    """Download Twilio media to local media folder. Returns relative path or empty string."""
    if not media_url:
        return ''

    try:
        resp = requests.get(
            media_url,
            auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
            timeout=30,
        )
        resp.raise_for_status()
    except Exception:
        return ''

    ext = _guess_extension(resp.headers.get('Content-Type', ''))
    filename = f"{uuid.uuid4()}{ext}"
    save_dir = os.path.join(settings.MEDIA_ROOT, subfolder)
    os.makedirs(save_dir, exist_ok=True)
    full_path = os.path.join(save_dir, filename)

    with open(full_path, 'wb') as f:
        f.write(resp.content)

    return os.path.join(subfolder, filename)


def _guess_extension(content_type: str) -> str:
    mapping = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/webp': '.webp',
        'application/pdf': '.pdf',
    }
    return mapping.get(content_type.split(';')[0].strip(), '.bin')
