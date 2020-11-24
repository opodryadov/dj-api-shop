from rest_framework import serializers
from review.models import Review
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from shop.models import Product


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username',)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name',)


class ReviewSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

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
        method = self.context["request"].stream.method
        reviews = Review.objects.filter(product=product_id).filter(creator=user_name).count()
        if reviews and method == 'POST':
            raise ValidationError({"Error": "Нельзя оставлять более одного отзыва на один товар!"})
        return data
