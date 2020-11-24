from django.db import models
from django.conf import settings
from shop.models import Product
from django.core.validators import MinValueValidator


class Order(models.Model):

    STATUS_NEW = 'NEW'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_COMPLETED = 'COMPLETED'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'В обработке'),
        (STATUS_COMPLETED, 'Выполнен')
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
    )
    position = models.ManyToManyField('Position', related_name='orders', verbose_name='Позиции')
    status = models.CharField(max_length=20, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)
    total_amount = models.DecimalField(max_digits=10, verbose_name='Общая стоимость', decimal_places=2, default=0)
    created_at = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлен',
        auto_now=True
    )

    def __str__(self):
        return "Заказ №%s от %s на сумму %s" % (self.id, self.customer, self.total_amount)


class Position(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='positions', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(1)], default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return f"{self.product.name} - колличество: {self.quantity}"