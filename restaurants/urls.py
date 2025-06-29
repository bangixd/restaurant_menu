from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MenuItemDetailView, MenuCategoryDetailView, MenuItemListCreateView, MenuCategoryListCreateView,\
    RestaurantListCreateView, RestaurantRetrieveUpdateDestroyView

urlpatterns = [
    path('restaurants/', RestaurantListCreateView.as_view(), name='restaurant-list-create'),
    path('restaurants/<int:id>/', RestaurantRetrieveUpdateDestroyView.as_view(), name='restaurant-detail'),

    path('menu-categories/', MenuCategoryListCreateView.as_view(), name='menu-category-list-create'),
    path('menu-categories/<int:id>/', MenuCategoryDetailView.as_view(), name='menu-category-detail'),

    path('menu-items/', MenuItemListCreateView.as_view(), name='menu-item-list-create'),
    path('menu-items/<int:id>/', MenuItemDetailView.as_view(), name='menu-item-detail'),
]
