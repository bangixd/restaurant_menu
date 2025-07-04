from rest_framework import serializers
from .models import Order, OrderItem
from restaurants.models import MenuItem  # اگر MenuItem در app دیگری هست


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.id')  # فقط برای نمایش، از request گرفته میشه

    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'status', 'created_at', 'items']
        read_only_fields = ['user', 'status', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order

    def update(self, instance, validated_data):
        if instance.status != 'pending':
            raise serializers.ValidationError("سفارش فقط در حالت pending قابل ویرایش است.")

        items_data = validated_data.pop('items', None)
        instance.restaurant = validated_data.get('restaurant', instance.restaurant)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item in items_data:
                OrderItem.objects.create(order=instance, **item)

        return instance


class RestaurantOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'status', 'created_at', 'items']
        read_only_fields = ['id', 'user', 'restaurant', 'created_at', 'items']