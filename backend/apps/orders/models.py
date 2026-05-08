import random
import string
from datetime import datetime
from django.db import models
from apps.accounts.models import User
from apps.catalog.models import Product, ProductVariant


def generate_order_id():
    date_part = datetime.now().strftime("%y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"SN{date_part}{random_part}"


class Coupon(models.Model):
    FLAT = 'FLAT'
    PERCENT = 'PERCENT'
    DISCOUNT_TYPES = [(FLAT, 'Flat'), (PERCENT, 'Percent')]

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_uses = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        if not self.is_active:
            return False, 'Coupon is inactive'
        if now < self.valid_from:
            return False, 'Coupon not yet valid'
        if now > self.valid_until:
            return False, 'Coupon expired'
        if self.max_uses and self.used_count >= self.max_uses:
            return False, 'Coupon usage limit reached'
        return True, 'OK'

    def calculate_discount(self, subtotal):
        if self.discount_type == self.FLAT:
            return min(self.discount_value, subtotal)
        return round(subtotal * self.discount_value / 100, 2)


class Order(models.Model):
    STATUS_PLACED = 'PLACED'
    STATUS_CONFIRMED = 'CONFIRMED'
    STATUS_SHIPPED = 'SHIPPED'
    STATUS_DELIVERED = 'DELIVERED'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_CHOICES = [
        (STATUS_PLACED, 'Placed'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    id = models.CharField(max_length=20, primary_key=True, default=generate_order_id)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PLACED)

    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    whatsapp_number = models.CharField(max_length=15, db_index=True)

    shipping_name = models.CharField(max_length=150)
    shipping_phone = models.CharField(max_length=15)
    shipping_line1 = models.CharField(max_length=255)
    shipping_line2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_pincode = models.CharField(max_length=10)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    coupon_code = models.CharField(max_length=50, blank=True)
    replacement_window_days = models.PositiveIntegerField(default=7)

    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def is_in_replacement_window(self):
        if not self.delivered_at or self.status != self.STATUS_DELIVERED:
            return False
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() <= self.delivered_at + timedelta(days=self.replacement_window_days)

    def __str__(self):
        return self.id


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)

    product_name = models.CharField(max_length=255)
    product_image = models.URLField(blank=True)
    size = models.CharField(max_length=5)
    color = models.CharField(max_length=50)

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
