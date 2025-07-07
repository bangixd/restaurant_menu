from rest_framework import serializers
from .models import Blog, BlogCategory


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'title', 'slug']


class BlogSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogCategory.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'content', 'cover_image', 'category', 'category_id', 'is_published', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']
