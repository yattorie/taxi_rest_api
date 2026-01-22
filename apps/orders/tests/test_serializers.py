import pytest
from decimal import Decimal
from rest_framework.test import APIRequestFactory

from apps.orders.serializers import OrderCreateSerializer
from apps.orders.models import Tariff, Order


@pytest.mark.django_db
def test_order_serializer_creates_order(user):
    factory = APIRequestFactory()
    request = factory.post("/api/orders/")
    request.user = user

    tariff = Tariff.objects.create(
        name="Эконом",
        multiplier=Decimal("2.0")
    )

    serializer = OrderCreateSerializer(
        data={
            "from_address": "Минск, Ленина 1",
            "to_address": "Гродно, Советская 5",
            "tariff": tariff.id,
        },
        context={"request": request},
    )

    assert serializer.is_valid(), serializer.errors

    order = serializer.save()

    assert Order.objects.count() == 1
    assert order.client == user
    assert order.tariff == tariff


@pytest.mark.django_db
def test_order_price_calculated_correctly(user):
    factory = APIRequestFactory()
    request = factory.post("/api/orders/")
    request.user = user

    tariff = Tariff.objects.create(
        name="Бизнес",
        multiplier=Decimal("3.0")
    )

    serializer = OrderCreateSerializer(
        data={
            "from_address": "Минск, Ленина 1",
            "to_address": "Гродно, Советская 5",
            "tariff": tariff.id,
        },
        context={"request": request},
    )

    serializer.is_valid(raise_exception=True)
    order = serializer.save()

    assert order.price == Decimal("9.00")


@pytest.mark.django_db
def test_order_serializer_invalid_tariff(user):
    factory = APIRequestFactory()
    request = factory.post("/api/orders/")
    request.user = user

    serializer = OrderCreateSerializer(
        data={
            "from_address": "Минск, Ленина 1",
            "to_address": "Гродно, Советская 5",
            "tariff": 9999,
        },
        context={"request": request},
    )

    assert not serializer.is_valid()
    assert "tariff" in serializer.errors
