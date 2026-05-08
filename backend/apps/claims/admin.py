from django.contrib import admin
from .models import Claim, ClaimFile, VerificationResult


class ClaimFileInline(admin.TabularInline):
    model = ClaimFile
    extra = 0


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'customer_phone', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['id', 'order__id', 'customer_phone']
    inlines = [ClaimFileInline]


@admin.register(VerificationResult)
class VerificationResultAdmin(admin.ModelAdmin):
    list_display = ['claim', 'recommendation', 'confidence_score', 'phone_matched',
                    'damage_detected', 'is_authentic', 'created_at']
    list_filter = ['recommendation', 'damage_detected', 'is_authentic']
