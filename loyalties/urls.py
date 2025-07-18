from django.urls import path
from .views import RestaurantCustomerListView, UserProfileView

urlpatterns = [
    path('loyalty/customers/', RestaurantCustomerListView.as_view(), name='loyalty-customer-list'),
    path('loyalty/profile/', UserProfileView.as_view(), name='user-profile'),
]
