from django.conf import settings
from django.db import models


class MarkChoices(models.IntegerChoices):
    """Оценки товара"""

    EXCELLENT = 5, 'Отлично'
    GOOD = 4, 'Хорошо'
    NORMAL = 3, 'Нормально'
    BAD = 2, 'Плохо'
    DISGUSTING = 1, 'Отвратительно'


class StatusChoices(models.TextChoices):
    """Статусы заказа"""

    NEW = "NEW", "Новый"
    IN_PROGRESS = "IN PROGRESS", "В процессе"
    DONE = "DONE", "Завершен"


class Product(models.Model):
    """Товар"""

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.TextField()
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзыв к товару"""

    class Meta:
        verbose_name = 'Отзыв к товару'
        verbose_name_plural = 'Отзывы к товару'

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    text = models.TextField(default='')
    mark = models.IntegerField(
        choices=MarkChoices.choices
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.text


class Order(models.Model):
    """Заказ"""

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status = models.TextField(
        choices=StatusChoices.choices,
        default=StatusChoices.NEW
    )
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)
    # product = models.ManyToManyField(
    #     Product,
    #     through='Positions',
    #     through_fields=('order', 'product', 'quantity'),
    # )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_cost(self):
        return self.price * self.quantity


# class Positions(models.Model):
#     """Позиции"""
#
#     order = models.ForeignKey(Order, related_name='positions', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)
#
#     def get_cost(self):
#         return self.price * self.quantity