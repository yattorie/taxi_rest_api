from decimal import Decimal

from rest_framework import serializers

from . import constants
from .models import Order, Tariff


class OrderCreateSerializer(serializers.ModelSerializer):
    tariff = serializers.PrimaryKeyRelatedField(
        queryset=Tariff.objects.filter(is_active=True)
    )
    currency = serializers.ChoiceField(
        choices=constants.Currency,
        default=constants.Currency.BYN
    )
    class Meta:
        model = Order
        fields = (
            'from_address',
            'to_address',
            'tariff',
            'currency',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        tariff = validated_data['tariff']

        base_price = Decimal("3.00")
        price = base_price * tariff.multiplier

        validated_data['price'] = price

        return Order.objects.create(
            client=user,
            **validated_data
        )

    def validate_tariff(self, tariff):
        if not tariff.is_active:
            raise serializers.ValidationError("Тариф недоступен")
        return tariff
    
    def validate_from_address(self, value):
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError("Адрес отправления слишком короткий")
        return value.strip()

    def validate_to_address(self, value):
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError("Адрес назначения слишком короткий")
        return value.strip()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'from_address',
            'to_address',
            'price',
            'currency',
            'status',
            'created_at',
            'updated_at',
        )
        read_only_fields = fields


class AdminOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ('id', 'name', 'multiplier')
