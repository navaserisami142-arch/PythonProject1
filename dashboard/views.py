from decimal import Decimal
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone

from orders.models import Order
from products.models import Product, Review


@staff_member_required
def dashboard_home(request):

    orders = Order.objects.all()

    total_sales = Decimal("0")

    for order in orders:
        total_sales += order.get_total_price()

    recent_orders = (
        Order.objects
        .select_related("user")
        .prefetch_related("items")
        .order_by("-created")[:8]
    )

    recent_users = (
        User.objects
        .order_by("-date_joined")[:8]
    )

    recent_products = (
        Product.objects
        .order_by("-created")[:8]
    )

    low_stock_products = (
        Product.objects
        .filter(stock__lte=5)
        .order_by("stock")
    )

    paid_orders = orders.filter(paid=True).count()

    pending_orders = orders.filter(status="pending").count()

    today = timezone.now()

    this_month = today.replace(day=1)

    month_orders = (
        Order.objects
        .filter(created__gte=this_month)
        .count()
    )

    context = {

        "users_count": User.objects.count(),

        "products_count": Product.objects.count(),

        "orders_count": Order.objects.count(),

        "reviews_count": Review.objects.count(),

        "paid_orders": paid_orders,

        "pending_orders": pending_orders,

        "month_orders": month_orders,

        "total_sales": total_sales,

        "recent_orders": recent_orders,

        "recent_users": recent_users,

        "recent_products": recent_products,

        "low_stock_products": low_stock_products,

    }

    return render(
        request,
        "dashboard/dashboard_home.html",
        context,
    )