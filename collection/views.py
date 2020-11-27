from rest_framework.viewsets import ModelViewSet
from collection.models import Collection
from collection.serializers import CollectionSerializer
from rest_framework.permissions import IsAdminUser


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []
