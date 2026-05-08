from django.urls import path
from . import views

urlpatterns = [
    path('incoming/', views.incoming_webhook, name='whatsapp_incoming'),
]
