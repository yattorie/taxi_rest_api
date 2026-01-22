from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from apps.accounts.models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'phone_number',
        )

    def create(self, validated_data):
        user = super().create(validated_data)
        user.is_active = False
        user.email_verified = False
        user.save(update_fields=['is_active', 'email_verified'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'role',
            'email_verified',
        )
        read_only_fields = ('role', 'email_verified')


class EmailConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # code = serializers.CharField()
    code = serializers.CharField(max_length=6)
