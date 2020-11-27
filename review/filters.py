from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from review.models import Review
from product.models import Product


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