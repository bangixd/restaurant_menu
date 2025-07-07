from rest_framework import generics
from .models import Blog, BlogCategory
from .serializers import BlogSerializer, BlogCategorySerializer


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = BlogSerializer


class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.filter(is_published=True)
    serializer_class = BlogSerializer


class BlogCategoryListView(generics.ListAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
