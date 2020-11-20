from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from shop.filters import ProductFilter, ReviewFilter
from shop.models import Product, Review, Order
from shop.serializers import ProductSerializer, ReviewSerializer, OrderSerializer


class ProductPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST' or request.method == 'DELETE' or request.method == 'PUT' or request.method == 'PATCH':
            if request.user.is_superuser:
                return True
            else:
                return False


class RewiewPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            if request.user.is_authenticated:
                return True
            else:
                return False
        if request.method == 'DELETE' or request.method == 'PUT' or request.method == 'PATCH':
            if request.user.is_authenticated:
                pass
                # Вот тут мы описываем условие отбора отзыва (как проверить пользователя, что отзыв принадлежит ему??)
                # if request.user == view.queryset._result_cache.creator:
                #     return True
                # else:
                #     return False
            else:
                return False


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (ProductPermissions, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (RewiewPermissions, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
