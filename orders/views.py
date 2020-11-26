from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from orders.filters import OrderFilter
from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.prefetch_related('positions').all()
        if self.request.user.is_authenticated:
            return Order.objects.prefetch_related('positions').filter(creator=self.request.user.id)
        else:
            raise ValidationError({"Error": "Вы не авторизированы!"})

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []
