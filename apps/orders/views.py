from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Order, Tariff
from .serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    AdminOrderSerializer, TariffSerializer,
)
from .permissions import IsAdmin
from apps.accounts.constants import UserRole
from apps.orders.constants import OrderStatus


@extend_schema_view(
    list=extend_schema(
        tags=['Orders'],
        summary='Список заказов',
        description='Админ видит все заказы, пользователь — только свои'
    ),
    retrieve=extend_schema(
        tags=['Orders'],
        summary='Получить заказ'
    ),
    create=extend_schema(
        tags=['Orders'],
        summary='Создать заказ',
        request=OrderCreateSerializer,
        responses={201: OrderSerializer}
    ),
    update=extend_schema(
        tags=['Orders'],
        summary='Обновить заказ (ADMIN)'
    ),
    partial_update=extend_schema(
        tags=['Orders'],
        summary='Частично обновить заказ (ADMIN)'
    ),
    destroy=extend_schema(
        tags=['Orders'],
        summary='Удалить заказ (ADMIN)'
    ),
)
class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == UserRole.ADMIN:
            return Order.objects.all()
        return Order.objects.filter(client=user)

    def get_serializer_class(self):
        if self.request.user.role == UserRole.ADMIN:
            return AdminOrderSerializer
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    # def perform_create(self, serializer):
    #     serializer.save(client=self.request.user)

    def update(self, request, *args, **kwargs):
        if request.user.role != UserRole.ADMIN:
            return Response(
                {'detail': 'Редактирование заказа запрещено'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if request.user.role != UserRole.ADMIN:
            return Response(
                {'detail': 'Редактирование заказа запрещено'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=['Orders'],
        summary='Подтвердить заказ',
        description='Подтверждение заказа (только ADMIN)',
        responses={200: AdminOrderSerializer}
    )
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdmin]
    )
    def confirm(self, request, pk=None):
        order = self.get_object()

        if order.status != OrderStatus.PENDING:
            return Response(
                {'detail': 'Заказ нельзя подтвердить из текущего статуса'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = OrderStatus.CONFIRMED
        order.save(update_fields=['status'])

        return Response({'status': order.status})

    @extend_schema(
        tags=['Orders'],
        summary='Завершить заказ',
        description='Завершить подтверждённый заказ'
    )
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdmin]
    )
    def complete(self, request, pk=None):
        order = self.get_object()

        if order.status != OrderStatus.CONFIRMED:
            return Response(
                {'detail': 'Завершить можно только подтверждённый заказ'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = OrderStatus.COMPLETED
        order.save(update_fields=['status'])

        return Response({'status': order.status})

    @extend_schema(
        tags=['Orders'],
        summary='Отменить заказ',
        description='Отмена заказа'
    )
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdmin]
    )
    def cancel(self, request, pk=None):
        order = self.get_object()

        if order.status == OrderStatus.COMPLETED:
            return Response(
                {'detail': 'Завершённый заказ нельзя отменить'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = OrderStatus.CANCELLED
        order.save(update_fields=['status'])

        return Response({'status': order.status})


class TariffViewSet(ReadOnlyModelViewSet):
    queryset = Tariff.objects.filter(is_active=True)
    serializer_class = TariffSerializer
