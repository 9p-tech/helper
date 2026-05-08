from django.contrib import admin
from .models import ConversationSession, WhatsAppMessage


class WhatsAppMessageInline(admin.TabularInline):
    model = WhatsAppMessage
    extra = 0
    readonly_fields = ['direction', 'message_body', 'media_url', 'timestamp']


@admin.register(ConversationSession)
class ConversationSessionAdmin(admin.ModelAdmin):
    list_display = ['customer_phone', 'current_state', 'active_claim', 'last_active']
    list_filter = ['current_state']
    search_fields = ['customer_phone']
    inlines = [WhatsAppMessageInline]
