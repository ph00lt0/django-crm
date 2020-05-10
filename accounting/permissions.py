from rest_framework import permissions


class IsOwnerOrNoAccess(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'company'):
            if obj.company == request.user.employee.company:
                return True
        if hasattr(obj, 'client'):
            if obj.client.company == request.user.employee.company:
                return True
        return False
