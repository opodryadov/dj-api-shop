from django_filters import rest_framework as filters
from order.models import Order
from product.models import Product


class OrderFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='order_price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='order_price', lookup_expr='lte')
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()
    positions = filters.ModelChoiceFilter(
        field_name="products",
        to_field_name="id",
        queryset=Product.objects.all(),
    )

    class Meta:
        model = Order
        fields = ('status', 'min_price', 'max_price', 'created_at', 'updated_at', 'positions',)
