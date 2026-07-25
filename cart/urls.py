from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('coupon/', views.apply_coupon, name='apply_coupon'),
    path("drawer/", views.cart_drawer, name="cart_drawer"),
    path("drawer/", views.cart_drawer, name="cart_drawer"),
]