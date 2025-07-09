from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from rest_framework import permissions
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title='Pojio',
        default_version='v0.0.1-beta',
        description='this is a project for project management ',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='abolfazls4yy4h@gmail.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('orders/', include('orders.urls')),
    path('blogs/', include('blog.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),

    # swagger routes
    path('api-auth/', include('rest_framework.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
