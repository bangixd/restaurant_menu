from django.db import models
from accounts.models import User
from restaurants.models import Restaurant


class LoyaltyProgram(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='loyalty_program')
    point_per_currency = models.PositiveIntegerField(default=10)  # چند امتیاز به ازای هر 1000 تومان؟
    reward_threshold = models.PositiveIntegerField(default=100)  # حداقل امتیاز لازم برای دریافت هدیه
    reward_description = models.TextField()  # توضیح هدیه


class CustomerLoyaltyPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loyalty_points')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='customer_loyalties')
    points = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
