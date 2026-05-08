from django.contrib import admin
from .models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'size', 'color', 'quantity', 'price', 'total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'whatsapp_number', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'customer_name', 'whatsapp_number', 'customer_email']
    readonly_fields = ['id', 'created_at']
    inlines = [OrderItemInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ['user', 'customer_email']
        return self.readonly_fields


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'used_count', 'valid_until', 'is_active']
    list_filter = ['discount_type', 'is_active']
    search_fields = ['code']
