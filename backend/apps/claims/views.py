from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from apps.orders.models import Order
from .models import Claim
from .serializers import ClaimSerializer, ClaimDecisionSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])
def claim_list(request):
    status_filter = request.query_params.get('status')
    qs = Claim.objects.select_related('order', 'verification').prefetch_related('files')
    if status_filter:
        qs = qs.filter(status=status_filter.upper())
    serializer = ClaimSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def claim_detail(request, claim_id):
    try:
        claim = Claim.objects.select_related('order', 'verification').prefetch_related('files').get(id=claim_id)
    except Claim.DoesNotExist:
        return Response({'error': 'Claim not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(ClaimSerializer(claim).data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def approve_claim(request, claim_id):
    try:
        claim = Claim.objects.get(id=claim_id)
    except Claim.DoesNotExist:
        return Response({'error': 'Claim not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClaimDecisionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    claim.status = Claim.STATUS_APPROVED
    claim.final_decision_reason = serializer.validated_data['reason']
    claim.resolved_at = timezone.now()
    claim.manual_action_by = request.user
    claim.save()
    return Response(ClaimSerializer(claim).data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def reject_claim(request, claim_id):
    try:
        claim = Claim.objects.get(id=claim_id)
    except Claim.DoesNotExist:
        return Response({'error': 'Claim not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClaimDecisionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    claim.status = Claim.STATUS_REJECTED
    claim.final_decision_reason = serializer.validated_data['reason']
    claim.resolved_at = timezone.now()
    claim.manual_action_by = request.user
    claim.save()
    return Response(ClaimSerializer(claim).data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    from apps.orders.models import Order
    stats = {
        'total_orders': Order.objects.count(),
        'orders_by_status': {s: Order.objects.filter(status=s).count() for s, _ in [('PLACED',''), ('CONFIRMED',''), ('SHIPPED',''), ('DELIVERED',''), ('CANCELLED','')]},
        'total_claims': Claim.objects.count(),
        'claims_by_status': {s: Claim.objects.filter(status=s).count() for s, _ in Claim.STATUS_CHOICES},
        'pending_manual_review': Claim.objects.filter(status=Claim.STATUS_MANUAL_REVIEW).count(),
    }
    return Response(stats)
