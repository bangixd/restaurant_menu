from rest_framework import viewsets, permissions, generics
from rest_framework.exceptions import PermissionDenied
from .permissions import IsRestaurantOwner, IsCategoryOwner, IsMenuItemOwner
from .models import Restaurant, MenuCategory, MenuItem
from .serializers import RestaurantSerializer, MenuCategorySerializer, MenuItemSerializer


class RestaurantListCreateView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsRestaurantOwner()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RestaurantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'id'  # می‌تونیم slug هم بذاریم

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsRestaurantOwner()]

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.owner:
            raise PermissionDenied("شما اجازه ویرایش این رستوران را ندارید.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.owner:
            raise PermissionDenied("شما اجازه حذف این رستوران را ندارید.")
        instance.delete()


class MenuCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuCategorySerializer

    def get_queryset(self):
        # فقط دسته‌بندی‌های رستورانی که توی query param داده شده
        restaurant_id = self.request.query_params.get('restaurant')
        if restaurant_id:
            return MenuCategory.objects.filter(restaurant__id=restaurant_id)
        return MenuCategory.objects.none()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsCategoryOwner()]

    def perform_create(self, serializer):
        restaurant = serializer.validated_data.get('restaurant')
        if restaurant.owner != self.request.user:
            raise PermissionDenied("شما اجازه افزودن دسته‌بندی به این رستوران را ندارید.")
        serializer.save()


class MenuCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsCategoryOwner()]

    def perform_update(self, serializer):
        if serializer.instance.restaurant.owner != self.request.user:
            raise PermissionDenied("شما اجازه ویرایش این دسته‌بندی را ندارید.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.restaurant.owner != self.request.user:
            raise PermissionDenied("شما اجازه حذف این دسته‌بندی را ندارید.")
        instance.delete()


class MenuItemListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category')
        if category_id:
            return MenuItem.objects.filter(category__id=category_id)
        return MenuItem.objects.none()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsMenuItemOwner()]

    def perform_create(self, serializer):
        category = serializer.validated_data.get('category')
        if category.restaurant.owner != self.request.user:
            raise PermissionDenied("شما اجازه افزودن آیتم به این دسته‌بندی را ندارید.")
        serializer.save()


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsMenuItemOwner()]

    def perform_update(self, serializer):
        if serializer.instance.category.restaurant.owner != self.request.user:
            raise PermissionDenied("شما اجازه ویرایش این آیتم را ندارید.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.category.restaurant.owner != self.request.user:
            raise PermissionDenied("شما اجازه حذف این آیتم را ندارید.")
        instance.delete()
