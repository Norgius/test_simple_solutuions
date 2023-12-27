from django.contrib import admin

from discount.models import Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass
