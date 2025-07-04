from django.urls import path
from .views import SendOTPView, VerifyOTPView, LogoutView

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),

    path('api/logout/', LogoutView.as_view(), name='logout'),
]
