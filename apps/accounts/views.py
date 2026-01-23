from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.models import User
from apps.accounts.serializers import EmailConfirmationSerializer


class VerifyEmailView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=['Auth'],
        summary='Подтверждение email',
        description='Подтверждение email по коду, отправленному на почту',
        request=EmailConfirmationSerializer,
        responses={
            200: {'type': 'object', 'properties': {'detail': {'type': 'string'}}},
            400: {'type': 'object', 'properties': {'detail': {'type': 'string'}}},
            404: {'type': 'object', 'properties': {'detail': {'type': 'string'}}},
        }
    )
    def post(self, request):
        serializer = EmailConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        key = f'email_verify:{email}'
        saved_code = cache.get(key)

        if not saved_code or saved_code != code:
            return Response(
                {'detail': 'Неверный или просроченный код'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {'detail': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        user.email_verified = True
        user.is_active = True
        user.save(update_fields=['email_verified', 'is_active'])

        cache.delete(key)

        return Response({'detail': 'Email подтвержден'}, status=status.HTTP_200_OK)
