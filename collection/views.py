from django.http import Http404
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from collection.models import Collection
from collection.serializers import CollectionSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            return Response({'Error': 'Подборка не найдена'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Success': 'Подборка удалена'}, status=status.HTTP_204_NO_CONTENT)
