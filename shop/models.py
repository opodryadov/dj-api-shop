from django.conf import settings
from django.db import models


class Product(models.Model):

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.TextField()
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, j) for i, j in enumerate(range(1, 6), start=1)])
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return "Отзыв от %s на %s " % (self.creator, self.product)
