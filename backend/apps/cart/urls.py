from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/', views.cart_add, name='cart_add'),
    path('cart/items/<int:pk>/', views.cart_item_update, name='cart_item_update'),
    path('cart/items/<int:pk>/delete/', views.cart_item_delete, name='cart_item_delete'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
]
