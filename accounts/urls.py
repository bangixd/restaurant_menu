from django.urls import path
from .views import UserProfileView, LogoutView, SendOTPView, VerifyOTPView, PhoneNumberCreateView

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),

    path('profile/', UserProfileView.as_view(), name='profile'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('submit-phone/', PhoneNumberCreateView.as_view(), name='submit-phone'),

]
