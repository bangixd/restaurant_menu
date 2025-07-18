from django.contrib import admin
from .models import Restaurant, MenuCategory, MenuItem, RestaurantGallery, RestaurantVideo, RestaurantOpeningHour, TableCall


class RestaurantGalleryInline(admin.TabularInline):
    model = RestaurantGallery
    extra = 1


class RestaurantVideoInline(admin.TabularInline):
    model = RestaurantVideo
    extra = 1


class OpeningHourInline(admin.TabularInline):
    model = RestaurantOpeningHour
    extra = 1


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['owner', 'name', 'slug', 'phone_number1', 'phone_number2', 'rating', 'address', 'slogan']
    list_filter = ['rating']
    search_fields = ['name', 'slug', 'phone_number1']

    readonly_fields = ['preview_logo', 'preview_banner']
    inlines = [RestaurantGalleryInline, RestaurantVideoInline, OpeningHourInline]

    fieldsets = (
        (None, {
            'fields': ('owner', 'name', 'slug', 'slogan', 'short_description', 'phone_number1', 'phone_number2',
                       'address', 'location', 'rating')
        }),
        ('ارتباطات', {
            'fields': ('instagram', 'telegram')
        }),
        ('تصاویر', {
            'fields': ('logo', 'preview_logo', 'banner', 'preview_banner')
        }),
    )

    def preview_logo(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" style="max-height:100px;" />'
        return "-"
    preview_logo.allow_tags = True
    preview_logo.short_description = 'پیش‌نمایش لوگو'

    def preview_banner(self, obj):
        if obj.banner:
            return f'<img src="{obj.banner.url}" style="max-height:100px;" />'
        return "-"
    preview_banner.allow_tags = True
    preview_banner.short_description = 'پیش‌نمایش بنر'


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


@admin.register(TableCall)
class TableCallAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant', 'user', 'table_number', 'is_resolved', 'created_at']
    list_filter = ['restaurant', 'is_resolved']
    search_fields = ['table_number', 'restaurant__name', 'user__phone']