from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from shop.filters import ProductFilter, ReviewFilter
from shop.models import Product, Review, Order
from shop.serializers import ProductSerializer, ReviewSerializer, OrderSerializer


class ProductViewSet(ModelViewSet):
    """ViewSet для товаров"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return []


class ProductReviewViewSet(ModelViewSet):
    """ViewSet для отзывов"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return []

    def get_serializer_context(self):
        response = {'request': self.request}
        return response


class OrderViewSet(ModelViewSet):
    """ViewSet для заказов"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer