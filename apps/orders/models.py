from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

from apps.orders import constants


class Tariff(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название тарифа"
    )

    multiplier = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="Коэффициент",
        help_text="1.0, 1.5, 2.0 и т.д."
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return self.name


class Order(models.Model):
    # Поля модели
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Клиент",
        help_text="Пользователь, создавший заказ")

    from_address = models.CharField(
        max_length=255,
        verbose_name="Откуда ехать",
        help_text="Введите адрес отправления")

    to_address = models.CharField(
        max_length=255,
        verbose_name="Куда ехать",
        help_text="Введите адрес назначения"
    )

    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Тариф"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость",
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00'),
        help_text="Укажите стоимость поездки"
    )

    currency = models.CharField(
        max_length=3,
        choices=constants.Currency,
        default=constants.Currency.BYN,
        verbose_name="Валюта"
    )

    status = models.CharField(
        max_length=20,
        choices=constants.OrderStatus,
        default=constants.OrderStatus.PENDING,
        verbose_name="Статус")

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания")

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']

    def __str__(self):
        return f"Заказ {self.id} от {self.client.email}"
