from django.contrib import admin
from django.utils.html import format_html

from .models import Order, Tariff
from .constants import OrderStatus


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client',
        'from_address',
        'to_address',
        'tariff',
        'price',
        'currency',
        'status',
        'created_at',
        'updated_at'
    )

    list_filter = [
        'status',
        'tariff',
        'currency',
        'created_at',
        'updated_at'
    ]

    search_fields = [
        'client__email',
        'client__first_name',
        'client__last_name',
        'from_address',
        'to_address',
        'id'
    ]

    readonly_fields = (
        'tariff',
        'price',
        'currency',
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Клиент и статус', {
            'fields': ('client', 'status'),
        }),
        ('Тариф и стоимость', {
            'fields': ('tariff', 'price', 'currency'),
        }),
        ('Маршрут', {
            'fields': ('from_address', 'to_address'),
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    ordering = ['-created_at']


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'multiplier',
        'is_active',
    )

    list_filter = ('is_active',)
    search_fields = ('name',)
