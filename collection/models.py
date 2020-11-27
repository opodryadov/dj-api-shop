from django.db import models
from product.models import Product


class ProductInCollection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    collection = models.ForeignKey('Collection', related_name='collections', on_delete=models.CASCADE, default=None)


class Collection(models.Model):

    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

    title = models.TextField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(max_length=1000, verbose_name='Текст')
    products = models.ManyToManyField(Product, through=ProductInCollection, related_name="collections")
    created_at = models.DateTimeField(
        verbose_name='Создана',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлена',
        auto_now=True
    )

    def __str__(self):
        return self.title
