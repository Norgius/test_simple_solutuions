from django.contrib import admin

from payment.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass
