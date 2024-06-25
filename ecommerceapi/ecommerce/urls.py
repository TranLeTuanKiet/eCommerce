from django.urls import path, include
from rest_framework import routers
from ecommerce import views

r = routers.DefaultRouter()
r.register('categories', views.CategoryViewSet, basename='categories')
r.register('products', views.ProductViewSet, basename='products')
r.register('stores', views.StoreViewSet, basename='stores')
r.register('users', views.UserViewSet, basename='users')
r.register('storecomments', views.StoreCommentViewSet, basename='storecomments')
r.register('storeratings', views.StoreRatingViewSet, basename='store_ratings')
r.register('productcomments', views.ProductCommentViewSet, basename='productcomments')
r.register('productratings', views.ProductRatingViewSet, basename='productratings')
r.register('carts', views.CartViewSet, basename='carts')
r.register('orders', views.OrderViewSet, basename='orders')
r.register('cartitems', views.CartItemViewSet, basename='cartitems')

urlpatterns = [
    path('', include(r.urls)),
]