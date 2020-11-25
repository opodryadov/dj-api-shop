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
        if request.method == 'POST':
            if request.user.is_authenticated:
                return True
            else:
                return False
        if request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
            if request.user.is_authenticated:
                review = Review.objects.get(id=request.parser_context['kwargs']['pk'])
                if review.creator.username == request.user.username:
                    return True
                else:
                    return False
            else:
                return False


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermissions, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
