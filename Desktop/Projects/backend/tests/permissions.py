from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.user and request.user.is_authenticated and request.user == obj.username and request.user.is_admin:
            return True
        return False
