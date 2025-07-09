from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from .permissions import IsRestaurantOwner, IsCategoryOwner, IsMenuItemOwner
from .models import Restaurant, MenuCategory, MenuItem, RestaurantGallery, RestaurantOpeningHour, RestaurantComment, TableCall
from .serializers import RestaurantSerializer, MenuCategorySerializer, MenuItemSerializer, RestaurantGallerySerializer,\
    RestaurantOpeningHourSerializer, RestaurantCommentSerializer, TableCallSerializer
from rest_framework.throttling import UserRateThrottle


class RestaurantListView(generics.ListAPIView):
    """
    api for listing all restaurants
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]


class RestaurantDetailView(generics.RetrieveAPIView):
    """
    api for detail of a restaurant
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]


class RestaurantRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    api for updating restaurant fields by owner
    """
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated, IsRestaurantOwner]

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)

    def get_object(self):
        return self.get_queryset().first()


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


class RestaurantGalleryListCreateView(generics.ListCreateAPIView):
    """
    api for create and list gallery of restaurant
    """
    serializer_class = RestaurantGallerySerializer
    permission_classes = [permissions.IsAuthenticated, IsRestaurantOwner]

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(owner=self.request.user).first()
        return restaurant.gallery.all() if restaurant else RestaurantGallery.objects.none()

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.filter(owner=self.request.user).first()
        serializer.save(restaurant=restaurant)


class RestaurantGalleryDeleteView(generics.DestroyAPIView):
    """
    api for delete pic from gallery of restaurant
    """
    queryset = RestaurantGallery.objects.all()
    serializer_class = RestaurantGallerySerializer
    permission_classes = [permissions.IsAuthenticated, IsRestaurantOwner]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


class RestaurantOpeningHourListCreateView(generics.ListCreateAPIView):
    """
    create or list opening hour
    """
    serializer_class = RestaurantOpeningHourSerializer
    permission_classes = [IsRestaurantOwner]

    def get_queryset(self):
        return RestaurantOpeningHour.objects.filter(restaurant__owner=self.request.user)

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.get(owner=self.request.user)
        serializer.save(restaurant=restaurant)


class RestaurantOpeningHourDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete and update opening hour
    """
    serializer_class = RestaurantOpeningHourSerializer
    permission_classes = [IsRestaurantOwner]

    def get_queryset(self):
        return RestaurantOpeningHour.objects.filter(restaurant__owner=self.request.user)


class RestaurantCommentListCreateView(generics.ListCreateAPIView):
    queryset = RestaurantComment.objects.all()
    serializer_class = RestaurantCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RestaurantCommentByRestaurantView(generics.ListAPIView):
    serializer_class = RestaurantCommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        restaurant_id = self.kwargs['restaurant_id']
        return RestaurantComment.objects.filter(restaurant_id=restaurant_id)


class WaiterCallThrottle(UserRateThrottle):
    rate = '2/min'


class TableCallCreateView(generics.CreateAPIView):
    serializer_class = TableCallSerializer
    throttle_classes = [WaiterCallThrottle]

    def perform_create(self, serializer):
        slug = self.kwargs.get('restaurant_slug')
        try:
            restaurant = Restaurant.objects.get(slug=slug)
        except Restaurant.DoesNotExist:
            raise NotFound("رستوران مورد نظر یافت نشد.")

        serializer.save(restaurant=restaurant, user=self.request.user)


class TableCallListView(generics.ListAPIView):
    serializer_class = TableCallSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TableCall.objects.filter(
            restaurant__owner=self.request.user
        )


class ResolveCallView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            call = TableCall.objects.get(pk=pk, restaurant__owner=request.user)
        except TableCall.DoesNotExist:
            return Response({"detail": "درخواست یافت نشد."}, status=404)

        call.is_resolved = True
        call.save()
        return Response({"detail": "درخواست حل شد."})