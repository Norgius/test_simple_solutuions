from django.db import models
from django.db.models import Sum, F

from discount.models import Discount


class Item(models.Model):
    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание', blank=True)
    price = models.PositiveIntegerField(
        'Цена',
        help_text='Цена: 100 = 1$',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_displayed_price(self):
        if self.price:
            return f'{(self.price / 100):.2f}'
        return 0


class OrderQuerySet(models.QuerySet):
    def receive_assembled_order(self):
        return self.prefetch_related('items').filter(status=Order.OrderStatus.IN_ASSEMBLY).first()

    def calculate_total_cost(self):
        return self.select_related('discount').prefetch_related('items').annotate(total_cost=Sum(F('items__price')))


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        IN_ASSEMBLY = 'IN_ASSEMBLY', 'Сборка заказа'
        PAID = 'PAID', 'Заказ оплачен'

    status = models.CharField(
        'Стутус заказа',
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.IN_ASSEMBLY,
        db_index=True,
    )
    creation_time = models.DateTimeField(
        'Время создания',
        auto_now_add=True,
        db_index=True,
    )
    paid_at = models.DateTimeField(
        'Оплачен в',
        db_index=True,
        blank=True,
        null=True,
    )
    items = models.ManyToManyField(
        Item,
        verbose_name='Товары',
        related_name='orders',
    )
    discount = models.ForeignKey(
        Discount,
        verbose_name='Скидка',
        related_name='orders',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    objects = OrderQuerySet.as_manager()

    def __str__(self) -> str:
        if self.status == self.OrderStatus.PAID:
            return f'{self.get_status_display()} - {self.paid_at}'
        return f'{self.get_status_display()} - {self.creation_time}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_displayed_price(self):
        if self.total_cost:
            if self.discount:
                discount = self.total_cost * (self.discount.percent_off / 100)
                return f'{((self.total_cost - discount) / 100):.2f}'
            return f'{(self.total_cost / 100):.2f}'
        return 0
