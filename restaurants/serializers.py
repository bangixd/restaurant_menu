from rest_framework import serializers
from .models import MenuCategory, MenuItem, Restaurant, RestaurantGallery, RestaurantOpeningHour


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = MenuCategory
        fields = '__all__'


class RestaurantGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantGallery
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class RestaurantOpeningHourSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_display', read_only=True)

    class Meta:
        model = RestaurantOpeningHour
        fields = ['id', 'day', 'day_display', 'open_time', 'close_time']


class RestaurantSerializer(serializers.ModelSerializer):
    gallery = RestaurantGallerySerializer(many=True, read_only=True)
    opening_hours = RestaurantOpeningHourSerializer(many=True, read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'slug',
            'short_description',
            'about',
            'address',
            'location',
            'phone_number',
            'instagram',
            'telegram',
            'banner',
            'rating',
            'gallery',
            'opening_hours',
            'created_at',
        ]
        read_only_fields = ['id', 'slug', 'rating', 'created_at']

