from rest_framework import permissions


class IsOwnerOrNoAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'company'):
            if obj.company == request.user.employee.company:
                return True
        if hasattr(obj, 'client'):
            if obj.client.company == request.user.employee.company:
                return True
            if obj.client.clientaccount.user == request.user:
                return True
        if hasattr(obj, 'vendor'):
            if obj.vendor.company == request.user.employee.company:
                return True
        return False
