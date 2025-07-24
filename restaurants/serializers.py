from rest_framework import serializers
from .models import MenuCategory, MenuItem, Restaurant, RestaurantGallery, RestaurantOpeningHour, RestaurantVideo,\
    RestaurantComment, TableCall


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = MenuCategory
        fields = '__all__'


class RestaurantVideoSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantVideo
        fields = ['id', 'title', 'video', 'uploaded_at']

    def get_video(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.video.url) if obj.video else None


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
    videos = RestaurantVideoSerializer(many=True, read_only=True)
    opening_hours = RestaurantOpeningHourSerializer(many=True, read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'eng_name',
            'slug',
            'slogan',
            'logo',
            'short_description',
            'about',
            'address',
            'location',
            'phone_number1',
            'phone_number2',
            'instagram',
            'telegram',
            'banner',
            'rating',
            'gallery',
            'videos',
            'opening_hours',
            'created_at',
        ]
        read_only_fields = ['id', 'slug', 'rating', 'created_at']


class RestaurantCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RestaurantComment
        fields = ['id', 'restaurant', 'user', 'text', 'rating', 'created_at']
        read_only_fields = ['user', 'created_at']


class TableCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableCall
        fields = ['id', 'restaurant', 'user', 'table_number', 'message', 'created_at', 'is_resolved']
        read_only_fields = ['id', 'user', 'created_at', 'is_resolved', 'restaurant']