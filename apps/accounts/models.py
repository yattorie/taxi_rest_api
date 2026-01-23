from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator

from apps.accounts import constants
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )

    email = models.EmailField(
        unique=True,
        verbose_name='Почта'
    )

    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Имя'
    )

    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Фамилия'
    )

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        verbose_name="Номер телефона"
    )

    role = models.CharField(
        max_length=10,
        choices=constants.UserRole,
        default=constants.UserRole.USER,
        verbose_name="Роль"
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Возраст"
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name="Активность"
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name="Доступ в админку"
    )

    email_verified = models.BooleanField(
        default=False,
        verbose_name="Email подтвержден",
        help_text="Указывает, подтвердил ли пользователь email кодом"
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
