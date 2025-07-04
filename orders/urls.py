from django.urls import path
from .views import OrderListCreateView, OrderDetailView, OwnerOrderListView, OwnerOrderDetailView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('owner/orders/', OwnerOrderListView.as_view(), name='owner-order-list'),
    path('owner/orders/<int:pk>/', OwnerOrderDetailView.as_view(), name='owner-order-detail'),
]
