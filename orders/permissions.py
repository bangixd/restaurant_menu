from rest_framework import permissions


class IsRestaurantOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.restaurant.owner == request.user

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsOrderOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
