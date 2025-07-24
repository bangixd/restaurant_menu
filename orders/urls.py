from django.urls import path
from .views import OrderListCreateView, OrderDetailView, OwnerOrderListView, OwnerOrderDetailView,\
    CompletedOrdersInvoiceView, OrderInvoiceDetailView, RestaurantOrdersInvoiceView, StartPaymentView, VerifyPaymentView

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('owner/', OwnerOrderListView.as_view(), name='owner-order-list'),
    path('owner/<int:pk>/', OwnerOrderDetailView.as_view(), name='owner-order-detail'),

    path('invoices/', CompletedOrdersInvoiceView.as_view(), name='order-invoices'),
    path('invoices/<int:pk>/', OrderInvoiceDetailView.as_view(), name='order-invoice-detail'),

    path('restaurant/invoices/', RestaurantOrdersInvoiceView.as_view(), name='restaurant-orders-invoices'),

    path('payment/start/<int:order_id>/', StartPaymentView.as_view(), name='start-payment'),
    path('payment/verify/', VerifyPaymentView.as_view(), name='verify-payment'),

]
