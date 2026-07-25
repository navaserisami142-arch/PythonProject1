from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/<slug:slug>/review/', views.add_review, name='add_review'),
    path("wishlist/<int:product_id>/",views.toggle_wishlist,name="toggle_wishlist"),
    path("wishlist/",views.wishlist,name="wishlist",),
    path("search/",views.search_products,name="search_products",),
    path("about/", views.about, name="about"),
]