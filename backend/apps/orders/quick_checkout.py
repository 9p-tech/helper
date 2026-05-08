"""
Quick checkout — creates user (or logs in), address, and order in one request.
No pre-auth required. Used by the frontend checkout page.
"""
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import Address, Profile
from apps.catalog.models import ProductVariant
from .models import Order, OrderItem, Coupon, generate_order_id

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def quick_checkout(request):
    """
    Body:
    {
      "email": "user@example.com",
      "full_name": "Raj Kumar",
      "whatsapp_number": "+919876543210",
      "address": {
        "line1": "123 MG Road",
        "line2": "",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400001",
        "phone": "+919876543210"
      },
      "items": [
        {"variant_id": 1, "quantity": 2}
      ],
      "coupon_code": ""
    }
    """
    data = request.data

    email = data.get('email', '').strip().lower()
    full_name = data.get('full_name', '').strip()
    whatsapp = data.get('whatsapp_number', '').strip()
    addr_data = data.get('address', {})
    items_data = data.get('items', [])
    coupon_code = data.get('coupon_code', '').strip()

    # Validate required fields
    errors = {}
    if not email:
        errors['email'] = 'Required'
    if not whatsapp or not whatsapp.startswith('+91') or len(whatsapp) != 13:
        errors['whatsapp_number'] = 'Must be +91XXXXXXXXXX (13 chars)'
    if not items_data:
        errors['items'] = 'Cart is empty'
    if not addr_data.get('line1'):
        errors['address'] = 'Address line 1 required'
    if errors:
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            # Get or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0] + '_' + email.split('@')[1].split('.')[0],
                    'is_active': True,
                }
            )
            if created:
                user.set_unusable_password()
                user.save()

            # Upsert profile
            Profile.objects.update_or_create(
                user=user,
                defaults={'full_name': full_name, 'whatsapp_number': whatsapp},
            )

            # Create address
            address = Address.objects.create(
                user=user,
                label='Order Address',
                full_name=full_name,
                phone=addr_data.get('phone', whatsapp),
                line1=addr_data.get('line1', ''),
                line2=addr_data.get('line2', ''),
                city=addr_data.get('city', ''),
                state=addr_data.get('state', ''),
                pincode=addr_data.get('pincode', ''),
            )

            # Resolve variants and validate stock
            resolved = []
            for item in items_data:
                vid = item.get('variant_id')
                qty = int(item.get('quantity', 1))
                try:
                    variant = ProductVariant.objects.select_related('product').get(pk=vid, is_available=True)
                except ProductVariant.DoesNotExist:
                    return Response(
                        {'error': f'Variant {vid} not found or unavailable'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if variant.stock < qty:
                    return Response(
                        {'error': f'Only {variant.stock} left for {variant.product.name} ({variant.size}/{variant.color})'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                resolved.append((variant, qty))

            # Calculate totals
            subtotal = sum(v.product.selling_price * q for v, q in resolved)
            discount_amount = 0

            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code)
                    valid, msg = coupon.is_valid()
                    if not valid:
                        return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
                    if subtotal < coupon.min_order_value:
                        return Response(
                            {'error': f'Minimum order ₹{coupon.min_order_value} required'},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    discount_amount = coupon.calculate_discount(subtotal)
                    Coupon.objects.filter(code=coupon_code).update(used_count=coupon.used_count + 1)
                except Coupon.DoesNotExist:
                    return Response({'error': 'Invalid coupon'}, status=status.HTTP_400_BAD_REQUEST)

            shipping_charge = 0 if subtotal >= 499 else 49
            total_amount = subtotal - discount_amount + shipping_charge

            # Create order
            order = Order.objects.create(
                user=user,
                customer_name=full_name,
                customer_email=email,
                whatsapp_number=whatsapp,
                shipping_name=address.full_name,
                shipping_phone=address.phone,
                shipping_line1=address.line1,
                shipping_line2=address.line2,
                shipping_city=address.city,
                shipping_state=address.state,
                shipping_pincode=address.pincode,
                subtotal=subtotal,
                discount_amount=discount_amount,
                shipping_charge=shipping_charge,
                total_amount=total_amount,
                coupon_code=coupon_code,
            )

            # Create order items & decrement stock
            for variant, qty in resolved:
                product = variant.product
                primary_img = product.images.filter(is_primary=True).first() or product.images.first()
                img_url = primary_img.image.url if primary_img else ''
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    variant=variant,
                    product_name=product.name,
                    product_image=img_url,
                    size=variant.size,
                    color=variant.color,
                    quantity=qty,
                    price=product.selling_price,
                )
                variant.stock -= qty
                variant.save()

            # Issue JWT for this user so frontend can use it
            refresh = RefreshToken.for_user(user)

            return Response({
                'order_id': order.id,
                'total_amount': str(order.total_amount),
                'status': order.status,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
