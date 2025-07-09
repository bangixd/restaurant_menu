from django.urls import path
from .views import OrderListCreateView, OrderDetailView, OwnerOrderListView, OwnerOrderDetailView

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('owner/', OwnerOrderListView.as_view(), name='owner-order-list'),
    path('owner/<int:pk>/', OwnerOrderDetailView.as_view(), name='owner-order-detail'),
]
