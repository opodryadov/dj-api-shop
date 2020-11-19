from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from shop.models import Product, Review


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    description = filters.CharFilter(field_name='description', lookup_expr='contains')

    class Meta:
        model = Product
        fields = ('name', 'description', 'min_price', 'max_price',)


class ReviewFilter(filters.FilterSet):
    creator = filters.ModelChoiceFilter(
        field_name="creator",
        to_field_name="id",
        queryset=User.objects.all(),
    )
    product = filters.ModelChoiceFilter(
        field_name="product",
        to_field_name="id",
        queryset=Product.objects.all(),
    )
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Review
        fields = ('creator', 'product', 'created_at',)
