from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .bot import process_incoming, send_whatsapp_message


@csrf_exempt
@require_POST
def incoming_webhook(request):
    from_number = request.POST.get('From', '')
    body = request.POST.get('Body', '')
    num_media = int(request.POST.get('NumMedia', 0))
    media_url = request.POST.get('MediaUrl0', '') if num_media > 0 else ''

    if not from_number:
        return HttpResponse('Missing From', status=400)

    reply_text = process_incoming(from_number, body, media_url)

    send_whatsapp_message(to=from_number, body=reply_text)

    twiml = '<?xml version="1.0" encoding="UTF-8"?><Response></Response>'
    return HttpResponse(twiml, content_type='text/xml')
