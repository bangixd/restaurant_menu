from rest_framework import generics, permissions, serializers, status
import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, Payment
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


class StartPaymentView(APIView):
    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user, is_paid=False)
        except Order.DoesNotExist:
            return Response({'detail': 'سفارش یافت نشد یا قبلا پرداخت شده'}, status=404)

        merchant_id = order.restaurant.zarinpal_merchant_id
        if not merchant_id:
            return Response({'detail': 'درگاه پرداخت برای این رستوران تنظیم نشده'}, status=400)

        amount = order.total_amount  # مبلغ به تومان
        callback_url = f'https://bestmenumarket.com/api/payment/verify/'  # آدرس بازگشت بعد از پرداخت

        data = {
            "merchant_id": merchant_id,
            "amount": amount * 10,  # تبدیل به ریال
            "callback_url": callback_url,
            "description": f"پرداخت سفارش #{order.id}",
        }

        response = requests.post('https://api.zarinpal.com/pg/v4/payment/request.json', json=data)
        res_data = response.json()

        if res_data['data'].get('code') == 100:
            authority = res_data['data']['authority']
            Payment.objects.create(order=order, authority=authority)
            payment_url = f'https://www.zarinpal.com/pg/StartPay/{authority}'
            return Response({'payment_url': payment_url})
        else:
            return Response({'detail': 'خطا در ارتباط با درگاه پرداخت'}, status=500)

class VerifyPaymentView(APIView):
    def get(self, request):
        authority = request.query_params.get('Authority')
        status_payment = request.query_params.get('Status')

        if status_payment != 'OK':
            return Response({'detail': 'پرداخت توسط کاربر لغو شد'}, status=400)

        try:
            payment = Payment.objects.get(authority=authority)
        except Payment.DoesNotExist:
            return Response({'detail': 'پرداخت یافت نشد'}, status=404)

        merchant_id = payment.order.restaurant.zarinpal_merchant_id
        data = {
            "merchant_id": merchant_id,
            "amount": payment.order.total_amount * 10,
            "authority": authority,
        }

        response = requests.post('https://api.zarinpal.com/pg/v4/payment/verify.json', json=data)
        res_data = response.json()

        if res_data['data'].get('code') == 100:
            payment.is_paid = True
            payment.ref_id = res_data['data']['ref_id']
            payment.save()

            payment.order.is_paid = True
            payment.order.save()

            return Response({'detail': 'پرداخت با موفقیت انجام شد', 'ref_id': payment.ref_id})
        else:
            return Response({'detail': 'پرداخت تایید نشد'}, status=400)