from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from order.filters import OrderFilter
from order.models import Order
from order.serializers import OrderSerializer


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

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            return Response({'Error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Success': 'Заказ удален'}, status=status.HTTP_204_NO_CONTENT)
