from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from shop.filters import ProductFilter
from shop.models import Product
from shop.serializers import ProductSerializer


class ProductPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST' or request.method == 'DELETE' or request.method == 'PUT' or request.method == 'PATCH':
            if request.user.is_superuser:
                return True
            else:
                return False


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (ProductPermissions, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
