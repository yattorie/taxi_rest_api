from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from apps.accounts import constants


class User(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Имя')

    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Фамилия')

    email = models.EmailField(
        unique=True,
        verbose_name='Email')

    role = models.CharField(
        max_length=10,
        choices=constants.UserRole,
        default=constants.UserRole.USER,
        verbose_name="Роль")

    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Возраст")

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        verbose_name="Номер телефона"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активность"
    )

    email_verified = models.BooleanField(
        default=False,
        verbose_name="Email подтвержден",
        help_text="Указывает, подтвердил ли пользователь email кодом")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name} ({self.email})'
        return self.email
