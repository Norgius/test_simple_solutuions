# Generated by Django 4.2.8 on 2023-12-27 08:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0001_initial'),
        ('payment', '0003_alter_item_description_alter_item_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='discount.discount', verbose_name='Скидка'),
        ),
        migrations.AddField(
            model_name='order',
            name='percent_off',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='Процент скидки'),
        ),
    ]
