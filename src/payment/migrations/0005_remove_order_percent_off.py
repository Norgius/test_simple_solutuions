# Generated by Django 4.2.8 on 2023-12-27 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_order_discount_order_percent_off'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='percent_off',
        ),
    ]