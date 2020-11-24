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
        # TODO: реализовать метод DELETE и PUT
        if request.method == 'DELETE' or request.method == 'PUT' or request.method == 'PATCH':
            if request.user.is_authenticated:
                review = Review.objects.get(id=request.parser_context['kwargs']['pk'])
                new_review = Review.objects.get(product=request.data['product'], creator=request.user)
                if review.id == new_review.id and review.creator.username == new_review.creator.username:
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
