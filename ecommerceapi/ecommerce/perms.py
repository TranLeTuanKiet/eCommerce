from rest_framework import permissions

class CommentOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, comment):
        return super().has_permission(request, view) and request.user == comment.buyer

class RatingOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, rating):
        return super().has_permission(request, view) and request.user == rating.buyer

class IsSellerUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'SELLER'

class IsBuyerUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'BUYER'

class StoreOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, store):
        return super().has_permission(request, view) and request.user == store.owner

class ProductOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, product):
        return super().has_permission(request, view) and request.user == product.store.owner

class CartOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, cart):
        return super().has_permission(request, view) and request.user == cart.buyer

class CartItemOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, cartitem):
        return super().has_permission(request, view) and request.user == cartitem.cart.buyer