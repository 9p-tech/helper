from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Profile, Address


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    full_name = serializers.CharField(write_only=True, required=False)
    whatsapp_number = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'full_name', 'whatsapp_number']

    def create(self, validated_data):
        full_name = validated_data.pop('full_name', '')
        whatsapp_number = validated_data.pop('whatsapp_number', '')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, full_name=full_name, whatsapp_number=whatsapp_number)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('Account is disabled')
        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'whatsapp_number', 'alternate_phone',
                  'date_of_birth', 'gender', 'profile_image']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_staff', 'date_joined', 'profile']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'label', 'full_name', 'phone', 'line1', 'line2',
                  'city', 'state', 'pincode', 'is_default', 'created_at']
        read_only_fields = ['id', 'created_at']
