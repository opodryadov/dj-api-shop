from django.db import models
from django.conf import settings
from product.models import Product


class ProductInOrder(models.Model):
    product = models.ForeignKey(Product, related_name='position_products', on_delete=models.CASCADE, default=None)
    order = models.ForeignKey('Order', related_name='positions', on_delete=models.CASCADE, default=None)
    quantity = models.PositiveIntegerField(default=1)


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
    products = models.ManyToManyField(Product, through=ProductInOrder, related_name="order")
    order_price = models.DecimalField(max_digits=10, verbose_name='Стоимость заказа', decimal_places=2,)
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
        return "Заказ №%s от %s на сумму %s" % (self.id, self.creator, self.order_price)
