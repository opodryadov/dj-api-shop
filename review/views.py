from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
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
                review = Review.objects.get(id=request.parser_context['kwargs']['pk'])
                if review.creator.username == request.user.username:
                    return True
        return []


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermissions, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
