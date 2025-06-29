from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['phone', 'full_name', 'is_staff', 'is_active']
    search_fields = ['phone', 'full_name']

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('اطلاعات شخصی'), {'fields': ('full_name',)}),
        (_('دسترسی‌ها'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('تاریخ‌ها'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

    readonly_fields = ['last_login']
