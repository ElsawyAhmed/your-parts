from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,TokenRefreshView)

app_name = 'your_cart'

urlpatterns = [
    # Authentication Urls
    path('auth/register/', RegisterCustomerView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Edit and Add to cart
    # path('add/', add_to_cart),
    # path('edit/', edit_cart),

    # Product CRUD
    path('product/add/', ProductCreateAPIView.as_view()),
    path('product/list/', ProductListAPIView.as_view()),
    path('product/edit/<int:pk>', ProductEditAPIView.as_view()),
    path('product/details/<int:pk>', ProductRetrieveAPIView.as_view()),
    path('product/delete/<int:pk>', ProductDeleteAPIView.as_view()),

    # Order CRUD
    path('order/list', OrderListAPIView.as_view()),
    path('order/cancel/<int:pk>', OrderEditAPIView.as_view()),
    path('order/details/<int:pk>', OrderRetrieveAPIView.as_view()),

    # Cart Urls
    path('cart/', get_cart_view, name='get_cart'),
    path('cart/item/<int:item_id>/remove/', remove_from_cart_view, name='remove_from_cart'),
    path('cart/item/<int:item_id>/update/', update_cart_item_quantity_view, name='update_cart_item_quantity'),
    path('cart/add/', add_to_cart_view, name='add_to_cart'),
    path('cart/checkout/', checkout_view, name='checkout'),


]