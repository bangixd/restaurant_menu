from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomerLoyaltyPoint
from orders.models import Order


@receiver(post_save, sender=Order)
def update_loyalty_points(sender, instance, created, **kwargs):
    if instance.is_paid:
        if not hasattr(instance, '_loyalty_added'):
            points = int(instance.total_price / 100)  # هر ۱۰۰ تومان = ۱ امتیاز
            print(points)
            if points > 0:
                print('yes')
                obj, created = CustomerLoyaltyPoint.objects.get_or_create(
                    user=instance.user,
                    restaurant=instance.restaurant,
                    defaults={'points': 0}
                )
                obj.points += points
                obj.save()
            instance._loyalty_added = True
