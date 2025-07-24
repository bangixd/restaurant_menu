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
    is_paid = models.BooleanField(default=False)

    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # جمع کل بدون مالیات
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # مالیات
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # مبلغ نهایی قابل پرداخت

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

    def calculate_totals(self):
        self.subtotal = sum(item.total_price for item in self.items.all())
        self.tax = self.subtotal * 0.09
        self.total_price = self.subtotal + self.tax
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0, blank=True)

    def save(self, *args, **kwargs):
        self.total_price = self.menu_item.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    authority = models.CharField(max_length=100, null=True, blank=True)
    ref_id = models.CharField(max_length=100, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
