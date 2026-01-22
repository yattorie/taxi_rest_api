from django.urls import path
from apps.accounts.views import VerifyEmailView

urlpatterns = [
    path('verify-email/', VerifyEmailView.as_view()),
]
