from rest_framework import generics
from .models import CustomerLoyaltyPoint
from .serializers import LoyaltyCustomerSerializer, UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class RestaurantCustomerListView(generics.ListAPIView):
    serializer_class = LoyaltyCustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # فقط مشتری‌هایی که برای رستوران لاگین شده امتیاز دارند
        return CustomerLoyaltyPoint.objects.filter(
            restaurant__owner=self.request.user
        ).select_related('user')


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)
