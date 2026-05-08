from rest_framework import serializers
from .models import Order, OrderItem, Coupon


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'product_image', 'size', 'color',
                  'quantity', 'price', 'total']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'customer_name', 'customer_email', 'whatsapp_number',
            'shipping_name', 'shipping_phone', 'shipping_line1', 'shipping_line2',
            'shipping_city', 'shipping_state', 'shipping_pincode',
            'subtotal', 'discount_amount', 'shipping_charge', 'total_amount',
            'coupon_code', 'replacement_window_days', 'items',
            'created_at', 'delivered_at', 'cancelled_at',
        ]


class OrderCreateSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    whatsapp_number = serializers.CharField(max_length=15)
    coupon_code = serializers.CharField(required=False, allow_blank=True)

    def validate_whatsapp_number(self, value):
        value = value.strip()
        if not value.startswith('+91') or len(value) != 13:
            raise serializers.ValidationError('Must be in +91XXXXXXXXXX format (13 chars)')
        return value


class CouponApplySerializer(serializers.Serializer):
    code = serializers.CharField()
    cart_total = serializers.DecimalField(max_digits=10, decimal_places=2)
