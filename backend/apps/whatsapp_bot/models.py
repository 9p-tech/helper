from django.db import models
from apps.claims.models import Claim


class ConversationSession(models.Model):
    STATE_INITIAL = 'INITIAL'
    STATE_AWAITING_ORDER_ID = 'AWAITING_ORDER_ID'
    STATE_AWAITING_DAMAGE_PHOTO = 'AWAITING_DAMAGE_PHOTO'
    STATE_AWAITING_INVOICE = 'AWAITING_INVOICE'
    STATE_DECISION_MADE = 'DECISION_MADE'   # spec name
    STATE_DONE = 'DECISION_MADE'            # alias kept so old code still works
    STATE_ABANDONED = 'ABANDONED'
    STATE_CHOICES = [
        (STATE_INITIAL, 'Initial'),
        (STATE_AWAITING_ORDER_ID, 'Awaiting Order ID'),
        (STATE_AWAITING_DAMAGE_PHOTO, 'Awaiting Damage Photo'),
        (STATE_AWAITING_INVOICE, 'Awaiting Invoice'),
        (STATE_DECISION_MADE, 'Decision Made'),
        (STATE_ABANDONED, 'Abandoned'),
    ]

    customer_phone = models.CharField(max_length=20, unique=True, db_index=True)
    current_state = models.CharField(
        max_length=30, choices=STATE_CHOICES, default=STATE_INITIAL
    )
    active_claim = models.ForeignKey(
        Claim, on_delete=models.SET_NULL, null=True, blank=True
    )
    context_data = models.JSONField(default=dict)
    last_active = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_phone} [{self.current_state}]"


class WhatsAppMessage(models.Model):
    INBOUND = 'INBOUND'
    OUTBOUND = 'OUTBOUND'
    DIRECTION_CHOICES = [(INBOUND, 'Inbound'), (OUTBOUND, 'Outbound')]

    session = models.ForeignKey(
        ConversationSession, on_delete=models.CASCADE, related_name='messages'
    )
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    message_body = models.TextField(blank=True)
    media_url = models.URLField(blank=True, max_length=500)
    twilio_message_sid = models.CharField(max_length=50, blank=True)  # kept as-is, no migration
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.direction} [{self.session.customer_phone}] {self.timestamp:%H:%M}"
