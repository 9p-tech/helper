from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.catalog.models import ProductVariant
from .models import Cart, CartItem
from .serializers import CartSerializer


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    cart = get_or_create_cart(request.user)
    return Response(CartSerializer(cart).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cart_add(request):
    variant_id = request.data.get('variant_id')
    quantity = int(request.data.get('quantity', 1))

    try:
        variant = ProductVariant.objects.get(pk=variant_id, is_available=True)
    except ProductVariant.DoesNotExist:
        return Response({'error': 'Variant not found or unavailable'}, status=status.HTTP_404_NOT_FOUND)

    if quantity < 1:
        return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)

    if variant.stock < quantity:
        return Response({'error': f'Only {variant.stock} in stock'}, status=status.HTTP_400_BAD_REQUEST)

    cart = get_or_create_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, variant=variant, defaults={'quantity': quantity})
    if not created:
        item.quantity += quantity
        if item.quantity > variant.stock:
            item.quantity = variant.stock
        item.save()

    return Response(CartSerializer(cart).data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def cart_item_update(request, pk):
    cart = get_or_create_cart(request.user)
    try:
        item = cart.items.get(pk=pk)
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    quantity = int(request.data.get('quantity', 1))
    if quantity < 1:
        item.delete()
    else:
        item.quantity = min(quantity, item.variant.stock)
        item.save()

    return Response(CartSerializer(cart).data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cart_item_delete(request, pk):
    cart = get_or_create_cart(request.user)
    try:
        cart.items.get(pk=pk).delete()
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(CartSerializer(cart).data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cart_clear(request):
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    return Response(CartSerializer(cart).data)
