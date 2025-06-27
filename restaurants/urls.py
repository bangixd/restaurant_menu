from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RestaurantViewSet, MenuCategoryViewSet, MenuItemViewSet

router = DefaultRouter()
router.register('restaurants', RestaurantViewSet, basename='restaurant')
router.register('categories', MenuCategoryViewSet, basename='category')
router.register('items', MenuItemViewSet, basename='item')

urlpatterns = [
    path('', include(router.urls)),
]
