from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "profile/",
        views.profile,
        name="profile",
    ),

    path(
        "orders/",
        views.my_orders,
        name="my_orders",
    ),

    path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/change_password.html",
            success_url="/accounts/profile/",
        ),
        name="change_password",
    ),
path(
    "dashboard/",
    views.dashboard,
    name="dashboard",
),

]