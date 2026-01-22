from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'role',
        'phone_number',
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
        'username',
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
                'username',
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
                'groups',
                'user_permissions',
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
