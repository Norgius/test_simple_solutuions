from django.contrib import admin

from payment.models import Item, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderItem(admin.ModelAdmin):
    readonly_fields = ['creation_time']
