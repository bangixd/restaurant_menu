from rest_framework import generics, permissions, serializers
from .models import Order
from .serializers import OrderSerializer, RestaurantOrderSerializer
from .permissions import IsOrderOwner, IsRestaurantOwner


class OrderListCreateView(generics.ListCreateAPIView):
    """
    create and list api for orders by customer
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    edit and delete orders in pending status by customer
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrderOwner]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.status != 'pending':
            raise serializers.ValidationError("فقط سفارش‌های در حال بررسی قابل ویرایش هستند.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.status != 'pending':
            raise serializers.ValidationError("فقط سفارش‌های در حال بررسی قابل حذف هستند.")
        instance.delete()


class OwnerOrderListView(generics.ListAPIView):
    """
    list of orders for restaurant owner
    """
    serializer_class = RestaurantOrderSerializer
    permission_classes = [IsRestaurantOwner]

    def get_queryset(self):
        return Order.objects.filter(restaurant__owner=self.request.user)


class OwnerOrderDetailView(generics.RetrieveUpdateAPIView):
    """
    update status of orders by restaurant owner
    """
    serializer_class = RestaurantOrderSerializer
    permission_classes = [IsRestaurantOwner]

    def get_queryset(self):
        return Order.objects.filter(restaurant__owner=self.request.user)