from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from twilio.twiml.messaging_response import MessagingResponse
from .state_machine import handle_message


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def incoming_webhook(request):
    from_number = request.data.get('From', '')
    body = request.data.get('Body', '')
    media_url = request.data.get('MediaUrl0', '')
    num_media = int(request.data.get('NumMedia', 0))

    if not from_number:
        return Response({'error': 'Missing From'}, status=400)

    reply_text = handle_message(from_number, body, media_url if num_media > 0 else '')

    twiml = MessagingResponse()
    twiml.message(reply_text)
    return Response(str(twiml), content_type='text/xml')
