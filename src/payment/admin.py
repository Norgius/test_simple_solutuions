from collections.abc import Callable, Sequence
from typing import Any

from django.contrib import admin
from django.http.request import HttpRequest
from django.db.models.query import QuerySet

from payment.models import Item, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'price']
    readonly_fields = ['get_price']
    list_display = ('__str__', 'get_price')

    def get_fields(self, request: HttpRequest, obj: Any | None = ...) -> Sequence[Callable[..., Any] | str]:
        if obj:
            return self.fields + ['get_price']
        return super().get_fields(request, obj)

    def get_price(self, obj: Order) -> str:
        return f'{obj.get_displayed_price()} $'
    get_price.short_description = 'Цена'


class ItemInline(admin.TabularInline):
    model = Item.orders.through
    raw_id_fields = ('item',)
    verbose_name = 'Товар для заказа'
    verbose_name_plural = 'Товары для заказа'


@admin.register(Order)
class OrderItem(admin.ModelAdmin):
    fields = ['status', 'creation_time', 'paid_at', 'discount']
    readonly_fields = ['creation_time', 'get_total_cost']
    list_display = ('__str__', 'get_total_cost')
    inlines = [ItemInline]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        return queryset.calculate_total_cost().prefetch_related('items')

    def get_fields(self, request: HttpRequest, obj: Any | None = ...) -> Sequence[Callable[..., Any] | str]:
        if not obj:
            return super().get_fields(request, obj)
        return self.fields + ['get_total_cost']

    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> list[str] | tuple[Any, ...]:
        if obj and obj.status == Order.OrderStatus.PAID:
            return self.readonly_fields + ['paid_at', 'discount']
        return self.readonly_fields

    def get_total_cost(self, obj: Order) -> str:
        return f'{obj.get_displayed_price()} $'
    get_total_cost.short_description = 'Стоимость заказа'
