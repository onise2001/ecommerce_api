from rest_framework.permissions import BasePermission


class CanDeleteProduct(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            print(request.user.role)
            return request.user == obj.seller or request.user.role == 'Admin'
        
        return False

class CanUpdateProduct(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj.seller
        return False
    

class CanChangeProductStatus(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'Admin'
        return False
    


class CanAddToCart(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj.customuser
        
        return False
    


class CanDeleteFromCart(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj.user or request.user.role == "Admin"
        return False
    

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'Admin' or request.user.is_staff
        return False