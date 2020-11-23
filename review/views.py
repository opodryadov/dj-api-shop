from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from review.filters import ReviewFilter
from review.models import Review
from review.serializers import ReviewSerializer


class RewiewPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            if request.user.is_authenticated:
                return True
            else:
                return False
        if request.method == 'DELETE' or request.method == 'PUT' or request.method == 'PATCH':
            if request.user.is_authenticated:
                pass
                # print(Review.objects.all())
                # Вот тут мы описываем условие отбора отзыва (как проверить пользователя, что отзыв принадлежит ему??)
                # if request.user == view.queryset._result_cache.creator:
                #     return True
                # else:
                #     return False
            else:
                return False


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (RewiewPermissions, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
