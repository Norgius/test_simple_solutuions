from django.db import models


class Item(models.Model):
    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена')

    def __str__(self):
        return self.name

    def get_displayed_price(self):
        return f'{(self.price / 100):.2f}'
