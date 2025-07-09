from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MenuItemDetailView, MenuCategoryDetailView, MenuItemListCreateView, MenuCategoryListCreateView,\
     RestaurantGalleryListCreateView, RestaurantGalleryDeleteView, RestaurantListView, RestaurantRetrieveUpdateView,\
     RestaurantDetailView, RestaurantOpeningHourListCreateView, RestaurantOpeningHourDetailView


urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurant-list'),
    path('<slug:slug>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('my-restaurant/', RestaurantRetrieveUpdateView.as_view(), name='my-restaurant'),

    path('menu-categories/', MenuCategoryListCreateView.as_view(), name='menu-category-list-create'),
    path('menu-categories/<int:id>/', MenuCategoryDetailView.as_view(), name='menu-category-detail'),

    path('menu-items/', MenuItemListCreateView.as_view(), name='menu-item-list-create'),
    path('menu-items/<int:id>/', MenuItemDetailView.as_view(), name='menu-item-detail'),

    path('opening-hour/', RestaurantOpeningHourListCreateView.as_view(), name='opening-hour-list-create'),
    path('opening-hour/<int:id>/', RestaurantOpeningHourDetailView.as_view(), name='opening-hour-detail'),

    path('my-restaurant/gallery/', RestaurantGalleryListCreateView.as_view(), name='restaurant-gallery'),
    path('my-restaurant/gallery/<int:pk>/delete/', RestaurantGalleryDeleteView.as_view(), name='delete-gallery-image'),
]
