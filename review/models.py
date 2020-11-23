from django.db import models
from django.conf import settings
from shop.models import Product


class Review(models.Model):
    CHOICES_LIST = ((1, '1',), (2, '2',), (3, '3',), (4, '4',), (5, '5',))

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
        choices=CHOICES_LIST
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

