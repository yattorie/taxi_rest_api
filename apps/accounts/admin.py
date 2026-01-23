from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
        'email_verified',
        'date_joined',
    )

    list_filter = (
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
        'email_verified',
        'date_joined',
    )

    search_fields = (
        'email',
        'first_name',
        'last_name',
        'phone_number',
    )

    readonly_fields = ['date_joined', 'last_login']

    ordering = ['-date_joined']

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'email',
                'password',
            )
        }),
        ('Личные данные', {
            'fields': (
                'first_name',
                'last_name',
                'phone_number',
                'age',
            )
        }),
        ('Права и роли', {
            'fields': (
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
        ('Подтверждение', {
            'fields': (
                'email_verified',
            )
        }),
        ('Временные метки', {
            'fields': (
                'last_login',
                'date_joined',
            ),
            'classes': ('collapse',),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'phone_number',
                'age',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'email_verified',
            ),
        }),
    )
