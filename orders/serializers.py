from rest_framework import serializers
from orders.models import Order, Position
from django.contrib.auth.models import User

from shop.models import Product


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',)


class PositionSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product.id")
    name = serializers.CharField(source='product.name', read_only=True)
    quantity = serializers.IntegerField(min_value=1, max_value=10)


class OrderSerializer(serializers.ModelSerializer):
    position_orders = PositionSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'creator', 'position_orders', 'status',)
        read_only_fields = ('creator',)

    def get_user(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        order_product = validated_data.pop("position_orders")
        order = super().create(validated_data)

        for product_position_data in order_product:
            Position.objects.create(
                product=product_position_data["product"]["id"],
                quantity=product_position_data["quantity"],
                order=order,
            )

        return order
