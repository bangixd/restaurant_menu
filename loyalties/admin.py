from django.contrib import admin
from .models import CustomerLoyaltyPoint


@admin.register(CustomerLoyaltyPoint)
class CustomerLoyaltyPointAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'points')
    search_fields = ('user__phone', 'restaurant__name')
    list_filter = ('restaurant',)
