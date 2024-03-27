from rest_framework.permissions import BasePermission
from tracker.models import Company

class ManageCompany(BasePermission):
    def has_permission(self, request, view):
        # Allow GET request (list view) to anyone
        if request.method == 'GET' or request.method == 'POST':
            return True
        # Check if the user is staff or owner for other methods
        return request.user.is_staff or request.user == view.get_object().owner

    def has_object_permission(self, request, view, obj):
        # Allow GET request (retrieve view) to anyone
        if request.method == 'GET':
            return True
        # Check if the user is staff or owner for other methods
        return request.user.is_staff or request.user == obj.owner