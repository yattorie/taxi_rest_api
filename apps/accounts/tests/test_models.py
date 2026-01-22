import pytest
from django.contrib.auth import get_user_model
from apps.accounts.constants import UserRole

User = get_user_model()

@pytest.mark.django_db
def test_user_created_with_default_role(user):
    assert user.role == UserRole.USER

@pytest.mark.django_db
def test_user_username_field_is_email(user):
    assert User.USERNAME_FIELD == "email"





