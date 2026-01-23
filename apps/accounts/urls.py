from django.urls import path
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.accounts.views import VerifyEmailView


user_register = UserViewSet.as_view({
    "post": "create",
})

user_me = UserViewSet.as_view({
    "get": "me",
})

urlpatterns = [
    path("register/", user_register, name="auth-register"),
    path("login/", TokenObtainPairView.as_view(), name="auth-login"),
    path("verify-email/", VerifyEmailView.as_view(), name="auth-verify-email"),

    path("token/refresh/", TokenRefreshView.as_view(), name="auth-token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="auth-token-verify"),

    path("users/me/", user_me, name="user-me"),
]
