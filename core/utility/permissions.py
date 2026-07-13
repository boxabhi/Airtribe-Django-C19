from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission


class IsManager(BasePermission):
    """
    Custom permission to only allow managers to access certain views.
    """
    message = 'Only Manager Can access this'
    def has_permission(self, request, view):
        try:
            if not hasattr(request.user, 'userrole') and not request.user.userrole.role_name == 'MANAGER':
                return False    
            if not request.user.has_perm('hotel.get_amenity'):
                return False
            return True
        except Exception as e:
            return False


class RoleAccess(BasePermission):
    """
    Custom permission to allow access based on user roles.
    """
    message = 'You do not have permission to access this resource.'
    ROLES = ['MANAGER', 'ADMIN', 'HELPER']

    def has_permission(self, request, view):
        print("*****************")
        print(request.user.userrole.role_name)
        print(request.user.id)
        print(request.user.username)
        print("*****************")
        return hasattr(request.user, 'userrole') and request.user.userrole.role_name in self.ROLES

       