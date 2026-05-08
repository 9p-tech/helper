from django.db.models import F as models_F
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.accounts.models import Address
from apps.cart.models import Cart
from .models import Order, OrderItem, Coupon
from .serializers import OrderSerializer, OrderCreateSerializer, CouponApplySerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    serializer = OrderCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    try:
        address = Address.objects.get(pk=data['address_id'], user=request.user)
    except Address.DoesNotExist:
        return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        cart = request.user.cart
    except Cart.DoesNotExist:
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

    cart_items = cart.items.select_related('variant__product').all()
    if not cart_items.exists():
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

    for item in cart_items:
        if item.variant.stock < item.quantity:
            return Response(
                {'error': f'Insufficient stock for {item.variant.product.name} ({item.variant.size}/{item.variant.color})'},
                status=status.HTTP_400_BAD_REQUEST
            )

    subtotal = sum(item.subtotal for item in cart_items)
    discount_amount = 0
    coupon_code = data.get('coupon_code', '')

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            valid, msg = coupon.is_valid()
            if not valid:
                return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
            if subtotal < coupon.min_order_value:
                return Response(
                    {'error': f'Minimum order value is ₹{coupon.min_order_value}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            discount_amount = coupon.calculate_discount(subtotal)
        except Coupon.DoesNotExist:
            return Response({'error': 'Invalid coupon'}, status=status.HTTP_400_BAD_REQUEST)

    shipping_charge = 0 if subtotal >= 499 else 49
    total_amount = subtotal - discount_amount + shipping_charge

    profile = getattr(request.user, 'profile', None)
    order = Order.objects.create(
        user=request.user,
        customer_name=profile.full_name if profile else request.user.username,
        customer_email=request.user.email,
        whatsapp_number=data['whatsapp_number'],
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

    order_items = []
    for item in cart_items:
        product = item.variant.product
        primary_img = product.images.filter(is_primary=True).first() or product.images.first()
        img_url = primary_img.image.url if primary_img else ''
        order_items.append(OrderItem(
            order=order,
            product=product,
            variant=item.variant,
            product_name=product.name,
            product_image=img_url,
            size=item.variant.size,
            color=item.variant.color,
            quantity=item.quantity,
            price=product.selling_price,
        ))
    OrderItem.objects.bulk_create(order_items)

    for item in cart_items:
        item.variant.stock -= item.quantity
        item.variant.save()

    if coupon_code:
        Coupon.objects.filter(code=coupon_code).update(used_count=models_F('used_count') + 1)

    cart.items.all().delete()

    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, order_id):
    try:
        order = Order.objects.prefetch_related('items').get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(OrderSerializer(order).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    if order.status not in [Order.STATUS_PLACED, Order.STATUS_CONFIRMED]:
        return Response({'error': 'Order cannot be cancelled at this stage'}, status=status.HTTP_400_BAD_REQUEST)

    order.status = Order.STATUS_CANCELLED
    order.cancelled_at = timezone.now()
    order.save()

    for item in order.items.select_related('variant').all():
        if item.variant:
            item.variant.stock += item.quantity
            item.variant.save()

    return Response(OrderSerializer(order).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_coupon(request):
    serializer = CouponApplySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    try:
        coupon = Coupon.objects.get(code=data['code'])
    except Coupon.DoesNotExist:
        return Response({'error': 'Invalid coupon code'}, status=status.HTTP_404_NOT_FOUND)

    valid, msg = coupon.is_valid()
    if not valid:
        return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)

    if data['cart_total'] < coupon.min_order_value:
        return Response({'error': f'Minimum order ₹{coupon.min_order_value} required'}, status=status.HTTP_400_BAD_REQUEST)

    discount = coupon.calculate_discount(data['cart_total'])
    return Response({
        'code': coupon.code,
        'discount_type': coupon.discount_type,
        'discount_value': str(coupon.discount_value),
        'discount_amount': str(discount),
    })
