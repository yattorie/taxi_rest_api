from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Ожидает подтверждения"
    CONFIRMED = "confirmed", "Подтвержден"
    COMPLETED = "completed", "Завершен"
    CANCELLED = "cancelled", "Отменен"


class Currency(models.TextChoices):
    BYN = "BYN", "Белорусский рубль"
