from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Discount(models.Model):
    class DiscountDuration(models.TextChoices):
        FOREVER = 'forever', 'Навсегда'
        ONCE = 'once', 'Одноразовый'
        REPEATING = 'repeating', 'Повторяющийся'

    code = models.CharField('Название', max_length=100)
    duration = models.CharField(
        'Продолжительность',
        choices=DiscountDuration.choices,
        db_index=True,
    )
    creation_time = models.DateTimeField(
        'Время создания',
        auto_now_add=True,
        db_index=True,
    )
    valid_to = models.DateTimeField(
        'Действителен до',
        db_index=True,
        blank=True,
        null=True,
    )
    percent_off = models.FloatField(
        'Процент скидки',
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )

    def __str__(self) -> str:
        return f'{self.code} - {self.percent_off}%'

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидка'
