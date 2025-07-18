from rest_framework import generics, permissions, serializers
from .models import Order
from .serializers import OrderSerializer, RestaurantOrderSerializer, InvoiceItemSerializer, OrderInvoiceSerializer
from django.utils.dateparse import parse_date
from .permissions import IsOrderOwner, IsRestaurantOwner
from .utils import is_restaurant_open


class OrderListCreateView(generics.ListCreateAPIView):
    """
    create and list api for orders by customer
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        restaurant = serializer.validated_data['restaurant']

        if not is_restaurant_open(restaurant):
            raise serializers.ValidationError({'detail': 'رستوران در حال حاضر بسته است.'})

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


class CompletedOrdersInvoiceView(generics.ListAPIView):
    """
    نمایش فاکتور سفارش‌های تکمیل شده برای کاربر
    """
    serializer_class = OrderInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user,
            status='delivered'
        ).order_by('-created_at')


class OrderInvoiceDetailView(generics.RetrieveAPIView):
    """
    نمایش جزییات فاکتور سفارش‌ تکمیل شده برای کاربر
    """
    serializer_class = OrderInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='completed')


class RestaurantOrdersInvoiceView(generics.ListAPIView):
    """
    نمایش فاکتور سفارش‌های تکمیل شده برای رستوران
    """
    serializer_class = OrderInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(
            restaurant__owner=user,
            status='delivered'
        ).select_related('restaurant', 'user').prefetch_related('order_items__menu_item')

        # فیلتر بر اساس رستوران خاص
        restaurant_id = self.request.query_params.get('restaurant_id')
        if restaurant_id:
            queryset = queryset.filter(restaurant__id=restaurant_id)

        # فیلتر بازه تاریخی
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(created_at__date__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(created_at__date__lte=parse_date(end_date))

        # جستجو در نام مشتری
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(user__full_name__icontains=search)

        return queryset.order_by('-created_at')
