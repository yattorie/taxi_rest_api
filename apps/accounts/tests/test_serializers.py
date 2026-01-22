import pytest
from apps.accounts.serializers import UserCreateSerializer
from apps.accounts.models import User


@pytest.mark.django_db
def test_user_create_serializer_creates_inactive_user():
    data = {
        "email": "user@test.com",
        "username": "user",
        "password": "StrongPass123!",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "+375292222222",
    }

    serializer = UserCreateSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    user = serializer.save()

    assert isinstance(user, User)
    assert user.email == "user@test.com"
    assert user.is_active is False
    assert user.email_verified is False
