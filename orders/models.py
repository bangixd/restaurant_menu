from django.db import models
from accounts.models import User
from restaurants.models import Restaurant, MenuItem


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'در حال بررسی'),
        ('confirmed', 'تأیید شده'),
        ('cancelled', 'لغو شده'),
        ('delivered', 'تحویل داده شده'),
    ], default='pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.phone}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
