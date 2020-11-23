from django_filters import rest_framework as filters
from shop.models import Product


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    description = filters.CharFilter(field_name='description', lookup_expr='contains')

    class Meta:
        model = Product
        fields = ('name', 'description', 'min_price', 'max_price',)
