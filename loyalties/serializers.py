from rest_framework import serializers
from .models import CustomerLoyaltyPoint
from accounts.models import User


class LoyaltyCustomerSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='user.phone')
    full_name = serializers.CharField(source='user.full_name')

    class Meta:
        model = CustomerLoyaltyPoint
        fields = ['user', 'phone', 'full_name', 'points', 'updated_at']


class UserProfileSerializer(serializers.ModelSerializer):
    loyalty_points = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'phone', 'full_name', 'birth_date', 'gender', 'role', 'loyalty_points']

    def get_loyalty_points(self, user):
        request = self.context.get('request')
        if not request:
            return 0
        # فقط مجموع امتیاز تمام رستوران‌ها برای سادگی
        return CustomerLoyaltyPoint.objects.filter(user=user).aggregate(
            total=sum('points')
        )['total'] or 0
