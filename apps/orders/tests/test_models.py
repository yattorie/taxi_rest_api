import pytest
from decimal import Decimal

from apps.orders.models import Tariff, Order
from apps.orders.constants import OrderStatus


@pytest.mark.django_db
def test_tariff_create():
    tariff = Tariff.objects.create(
        name="Эконом",
        multiplier=Decimal("1.0")
    )

    assert tariff.id is not None
    assert tariff.name == "Эконом"
    assert tariff.multiplier == Decimal("1.0")


@pytest.mark.django_db
def test_order_default_status(user):
    tariff = Tariff.objects.create(
        name="Комфорт",
        multiplier=Decimal("1.5")
    )

    order = Order.objects.create(
        client=user,
        from_address="Минск, Ленина 1",
        to_address="Гродно, Советская 5",
        tariff=tariff,
        price=Decimal("100.00")
    )

    assert order.status == OrderStatus.PENDING