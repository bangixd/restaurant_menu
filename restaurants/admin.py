from django.contrib import admin
from .models import Restaurant, MenuCategory, MenuItem


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'slug')
    search_fields = ('name', 'owner__phone')
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('owner',)


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'restaurant')
    search_fields = ('title', 'restaurant__name')
    list_filter = ('restaurant',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    search_fields = ('name', 'category__title')
    list_filter = ('category__restaurant', 'is_available')
