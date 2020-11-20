from rest_framework import serializers
from django.contrib.auth.models import User
from shop.models import Product, Review, Order
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class ReviewSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def get_items(self, obj):
        return obj.product.id

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        user_name = self.context["request"].user
        product_id = self.context["request"].data["product"]
        # method = self.context["request"].stream.method
        reviews = Review.objects.filter(product=product_id).filter(creator=user_name).count()
        if reviews:
            raise ValidationError({"Error": "Нельзя оставлять более одного отзыва на один товар!"})
        return data


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
