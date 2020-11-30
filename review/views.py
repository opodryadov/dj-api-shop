from django.http import Http404
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet
from review.filters import ReviewFilter
from review.models import Review
from review.serializers import ReviewSerializer


class ReviewPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user.is_authenticated:
            if request.method == 'POST':
                return True
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                try:
                    review = Review.objects.get(id=request.parser_context['kwargs']['pk'])
                except:
                    raise NotFound({'Error': 'Отзыв не найден'})
                if review.creator.username == request.user.username:
                    return True
        return []


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermissions, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'Success': 'Отзыв удален'}, status=status.HTTP_204_NO_CONTENT)
