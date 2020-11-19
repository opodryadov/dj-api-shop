from rest_framework import serializers
from django.contrib.auth.models import User
from shop.models import Product, Review, Order
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя"""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer для товаров"""

    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer для отзывов"""

    creator = UserSerializer(
        read_only=True,
    )

    product = ProductSerializer(
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        user_name = self.context["request"].user
        product_id = self.context["request"].data["product"]
        method = self.context["request"].stream.method
        reviews = Review.objects.filter(product=product_id).filter(creator=user_name).count()
        if reviews and method == "POST":
            raise ValidationError({"Error": "Нельзя оставлять более одного отзыва на один товар!"})
        return data


class OrderSerializer(serializers.ModelSerializer):
    """Serializer для заказов"""

    class Meta:
        model = Order
        fields = ('id', 'creator', 'product', 'quantity')

# class PositionsSerializer(serializers.ModelSerializer):
#     """Serializer для позиций"""
#     orders = OrderSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Positions
#         fields = '__all__'
