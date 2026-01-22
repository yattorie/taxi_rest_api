import pytest
from django.core.cache import cache
from rest_framework.test import APIClient
from apps.accounts.models import User


@pytest.mark.django_db
def test_verify_email_success():
    user = User.objects.create_user(
        username="verifyuser",
        email="verify@test.com",
        password="password123",
        phone_number="+375293333333",
        is_active=False,
    )

    cache.set(f"email_verify:{user.email}", "123456")

    client = APIClient()
    response = client.post(
        "/api/accounts/verify-email/",
        {
            "email": user.email,
            "code": "123456",
        },
        format="json",
    )

    user.refresh_from_db()

    assert response.status_code == 200
    assert user.email_verified is True


@pytest.mark.django_db
def test_verify_email_invalid_code(user):
    cache.set(f"email_verify:{user.email}", "123456")

    client = APIClient()
    response = client.post(
        "/api/accounts/verify-email/",
        {
            "email": user.email,
            "code": "000000",
        },
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_verify_email_user_not_found():
    cache.set("email_verify:notfound@test.com", "123456")

    client = APIClient()
    response = client.post(
        "/api/accounts/verify-email/",
        {
            "email": "notfound@test.com",
            "code": "123456",
        },
        format="json",
    )

    assert response.status_code == 404
