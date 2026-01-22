import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APIClient

from apps.orders.models import Tariff, Order


@pytest.mark.django_db
def test_create_order_unauthorized():
    client = APIClient()

    url = reverse("orders-list")
    response = client.post(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_create_order_authenticated(user):
    client = APIClient()
    client.force_authenticate(user=user)

    tariff = Tariff.objects.create(
        name="Эконом",
        multiplier=Decimal("1.0")
    )

    url = reverse("orders-list")
    response = client.post(
        url,
        {
            "from_address": "Минск, Ленина 1",
            "to_address": "Гродно, Советская 5",
            "tariff": tariff.id,
        },
        format="json",
    )

    assert response.status_code == 201
    assert Order.objects.count() == 1


@pytest.mark.django_db
def test_cannot_create_order_without_tariff(user):
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("orders-list")
    response = client.post(
        url,
        {
            "from_address": "Минск, Ленина 1",
            "to_address": "Гродно, Советская 5",
        },
        format="json",
    )

    assert response.status_code == 400
