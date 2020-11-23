from django.db import models


class Product(models.Model):

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.TextField(max_length=100, verbose_name='Наименование')
    description = models.TextField(max_length=1000, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, verbose_name='Цена', decimal_places=2, default=0)
    created_at = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлен',
        auto_now=True
    )

    def __str__(self):
        return self.name
