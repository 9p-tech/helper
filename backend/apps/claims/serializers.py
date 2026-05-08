from rest_framework import serializers
from .models import Claim, ClaimFile, VerificationResult


class ClaimFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimFile
        fields = ['id', 'file_type', 'file', 'file_size', 'uploaded_at']


class VerificationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationResult
        exclude = ['claim']


class ClaimSerializer(serializers.ModelSerializer):
    files = ClaimFileSerializer(many=True, read_only=True)
    verification = VerificationResultSerializer(read_only=True)
    order_id = serializers.CharField(source='order.id', read_only=True)

    class Meta:
        model = Claim
        fields = ['id', 'order_id', 'customer_phone', 'status', 'reason_text',
                  'final_decision_reason', 'created_at', 'resolved_at',
                  'files', 'verification']


class ClaimDecisionSerializer(serializers.Serializer):
    reason = serializers.CharField()
