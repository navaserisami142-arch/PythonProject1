from django.urls import path
from . import views

urlpatterns = [
    path(
        "create/",
        views.order_create,
        name="order_create"
    ),
    path(
        "success/<int:order_id>/",
        views.order_success,
        name="order_success"
    ),
path(
    "my-orders/",
    views.my_orders,
    name="my_orders",
),
path(
    "<int:order_id>/",
    views.order_detail,
    name="order_detail",
),
path(
    "<int:order_id>/invoice/",
    views.order_invoice,
    name="order_invoice",
),
]