from django.db import models
from django.conf import settings
from shop.models import Product


class Position(models.Model):
    product = models.ForeignKey(Product, related_name='position_products', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', related_name='position_orders', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


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

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Покупатель',
        on_delete=models.CASCADE,
    )
    positions = models.ManyToManyField(Product, through=Position, related_name="orders")
    status = models.CharField(max_length=20, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлен',
        auto_now=True
    )

    def __str__(self):
        return "Заказ №%s от %s" % (self.id, self.creator)
