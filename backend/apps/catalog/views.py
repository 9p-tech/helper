from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer, ReviewSerializer
)


class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True)


class ProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'is_featured']
    search_fields = ['name', 'description', 'material']
    ordering_fields = ['base_price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs


class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    queryset = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'variants', 'reviews')


class ReviewListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product = generics.get_object_or_404(Product, slug=self.kwargs['slug'])
        return Review.objects.filter(product=product)

    def perform_create(self, serializer):
        from apps.orders.models import OrderItem
        product = generics.get_object_or_404(Product, slug=self.kwargs['slug'])
        is_verified = OrderItem.objects.filter(
            order__user=self.request.user,
            product=product,
            order__status='DELIVERED'
        ).exists()
        serializer.save(user=self.request.user, product=product, is_verified_buyer=is_verified)
