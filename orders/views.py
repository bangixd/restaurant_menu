from rest_framework import generics, permissions, serializers
from .models import Order
from .serializers import OrderSerializer

class IsOrderOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
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
