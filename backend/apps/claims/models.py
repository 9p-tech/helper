import random
import string
from django.db import models
from apps.accounts.models import User
from apps.orders.models import Order


def generate_claim_id():
    number = ''.join(random.choices(string.digits, k=5))
    return f"RS-{number}"


class Claim(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_MANUAL_REVIEW = 'MANUAL_REVIEW'
    STATUS_RESOLVED = 'RESOLVED'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_MANUAL_REVIEW, 'Manual Review'),
        (STATUS_RESOLVED, 'Resolved'),
    ]

    id = models.CharField(max_length=15, primary_key=True, default=generate_claim_id)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='claims')
    customer_phone = models.CharField(max_length=15, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    reason_text = models.TextField()
    final_decision_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    manual_action_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.id


class ClaimFile(models.Model):
    DAMAGE_PHOTO = 'DAMAGE_PHOTO'
    INVOICE = 'INVOICE'
    FILE_TYPE_CHOICES = [(DAMAGE_PHOTO, 'Damage Photo'), (INVOICE, 'Invoice')]

    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='files')
    file_type = models.CharField(max_length=15, choices=FILE_TYPE_CHOICES)
    file = models.FileField(upload_to='claims/')
    image_hash = models.CharField(max_length=64, blank=True)
    file_size = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.claim.id} - {self.file_type}"


class VerificationResult(models.Model):
    SEVERITY_LOW = 'LOW'
    SEVERITY_MEDIUM = 'MEDIUM'
    SEVERITY_HIGH = 'HIGH'
    SEVERITY_CHOICES = [(SEVERITY_LOW, 'Low'), (SEVERITY_MEDIUM, 'Medium'), (SEVERITY_HIGH, 'High')]

    REC_APPROVED = 'APPROVED'
    REC_REJECTED = 'REJECTED'
    REC_MANUAL = 'MANUAL_REVIEW'
    REC_CHOICES = [(REC_APPROVED, 'Approved'), (REC_REJECTED, 'Rejected'), (REC_MANUAL, 'Manual Review')]

    claim = models.OneToOneField(Claim, on_delete=models.CASCADE, related_name='verification')

    phone_matched = models.BooleanField(default=False)
    order_in_window = models.BooleanField(default=False)

    damage_detected = models.BooleanField(default=False)
    damage_type = models.CharField(max_length=20, blank=True)
    damage_severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, blank=True)
    damage_confidence = models.FloatField(default=0.0)

    is_authentic = models.BooleanField(default=False)
    authenticity_confidence = models.FloatField(default=0.0)
    authenticity_flags = models.JSONField(default=list)

    invoice_ocr_raw_text = models.TextField(blank=True)
    invoice_order_id_found = models.CharField(max_length=20, blank=True)
    invoice_date_found = models.CharField(max_length=30, blank=True)
    invoice_matched = models.BooleanField(default=False)

    duplicate_image_found = models.BooleanField(default=False)
    duplicate_claim_id = models.CharField(max_length=15, blank=True)

    recommendation = models.CharField(max_length=15, choices=REC_CHOICES, blank=True)
    confidence_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification for {self.claim.id} → {self.recommendation}"
