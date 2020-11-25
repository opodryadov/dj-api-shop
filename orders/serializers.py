from rest_framework import serializers
from orders.models import Order, ProductInOrder
from django.contrib.auth.models import User
from shop.models import Product


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',)


class ProductInOrderSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product.id")
    name = serializers.CharField(source='product.name', read_only=True)
    quantity = serializers.IntegerField(min_value=1, max_value=10)


class OrderSerializer(serializers.ModelSerializer):
    positions = ProductInOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'creator', 'positions', 'order_price', 'status', 'created_at', 'updated_at',)
        read_only_fields = ('creator', 'order_price', )

    def create(self, validated_data, total_price=0):
        validated_data["creator"] = self.context["request"].user
        order_product = validated_data.pop("positions")
        for product_position_data in order_product:
            total_price += product_position_data["product"]["id"].price * product_position_data["quantity"]
            validated_data["order_price"] = total_price
        order = super().create(validated_data)
        for product_position_data in order_product:
            ProductInOrder.objects.create(
                product=product_position_data["product"]["id"],
                quantity=product_position_data["quantity"],
                order=order,
            )
        return order
