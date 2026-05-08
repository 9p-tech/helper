from django.urls import path
from . import views

urlpatterns = [
    path('claims/', views.claim_list, name='claim_list'),
    path('claims/<str:claim_id>/', views.claim_detail, name='claim_detail'),
    path('claims/<str:claim_id>/approve/', views.approve_claim, name='claim_approve'),
    path('claims/<str:claim_id>/reject/', views.reject_claim, name='claim_reject'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
]
