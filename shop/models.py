from django.conf import settings
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


class Review(models.Model):

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    product = models.ForeignKey(Product, verbose_name='Товар', related_name='reviews', on_delete=models.CASCADE)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )
    text = models.TextField(max_length=1000, verbose_name='Текст отзыва')
    rating = models.PositiveIntegerField(
        verbose_name='Оценка',
        choices=[(i, j) for i, j in enumerate(range(1, 6), start=1)]
    )
    created_at = models.DateTimeField(
        verbose_name='Создан',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлен',
        auto_now=True
    )

    def __str__(self):
        return "Отзыв от %s на %s " % (self.creator, self.product)


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
    status = models.CharField(max_length=20, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW)
    product = models.ForeignKey(Product, verbose_name='Товар', related_name='orders', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)
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
