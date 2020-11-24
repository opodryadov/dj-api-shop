from rest_framework import serializers
from orders.models import Order
from django.contrib.auth.models import User
from shop.serializers import ProductSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    product = ProductSerializer(many=True, read_only=True)
    # total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('product', 'customer', 'position',)

    def create(self, validated_data):
        validated_data["customer"] = self.context["request"].user
        return super().create(validated_data)
