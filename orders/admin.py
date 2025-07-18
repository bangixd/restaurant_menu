from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['menu_item', 'quantity', 'total_price']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'restaurant', 'total_price', 'is_paid', 'created_at']
    list_filter = ['status', 'restaurant', 'created_at']
    search_fields = ['user__phone_number', 'restaurant__name']
    inlines = [OrderItemInline]
    readonly_fields = ['subtotal', 'tax', 'total_price']

    def has_add_permission(self, request):
        # جلوگیری از ساخت سفارش از طریق ادمین
        return False
