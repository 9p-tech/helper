from django.urls import path
from . import views
from .quick_checkout import quick_checkout

urlpatterns = [
    path('orders/create/', views.create_order, name='order_create'),
    path('orders/quick-checkout/', quick_checkout, name='quick_checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<str:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<str:order_id>/cancel/', views.cancel_order, name='order_cancel'),
    path('coupons/apply/', views.apply_coupon, name='coupon_apply'),
]
