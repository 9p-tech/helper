from django.contrib import admin
from .models import ConversationSession, WhatsAppMessage


class WhatsAppMessageInline(admin.TabularInline):
    model = WhatsAppMessage
    extra = 0
    readonly_fields = ['direction', 'message_body', 'media_url', 'twilio_message_sid', 'timestamp']
    can_delete = False
    ordering = ['timestamp']


@admin.register(ConversationSession)
class ConversationSessionAdmin(admin.ModelAdmin):
    list_display = ['customer_phone', 'current_state', 'active_claim', 'last_active', 'created_at']
    list_filter = ['current_state']
    search_fields = ['customer_phone']
    readonly_fields = ['last_active', 'created_at']
    inlines = [WhatsAppMessageInline]


@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'direction', 'short_body', 'has_media', 'twilio_message_sid', 'timestamp']
    list_filter = ['direction']
    search_fields = ['session__customer_phone', 'message_body', 'twilio_message_sid']
    readonly_fields = ['session', 'direction', 'message_body', 'media_url', 'twilio_message_sid', 'timestamp']
    ordering = ['-timestamp']

    @admin.display(description='Message')
    def short_body(self, obj):
        return obj.message_body[:60] + '…' if len(obj.message_body) > 60 else obj.message_body

    @admin.display(boolean=True, description='Media?')
    def has_media(self, obj):
        return bool(obj.media_url)
