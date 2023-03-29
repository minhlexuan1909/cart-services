from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def create(self, validated_data):
        cart = validated_data["cart"]
        cart.total_value += validated_data["quantity"] * validated_data["price"]
        cart.save()

        return super().create(validated_data)


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = (
            "id",
            "account_id",
            "total_value",
            "cart_items",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "account_id", "total_value", "created_at", "updated_at")
