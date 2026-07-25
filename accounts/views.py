from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from orders.models import Order
from .models import Profile
from .forms import (
    RegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # ساخت پروفایل در صورت نبود
            Profile.objects.get_or_create(user=user)

            login(request, user)

            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user,
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect("profile")

    else:

        user_form = UserUpdateForm(
            instance=request.user,
        )

        profile_form = ProfileUpdateForm(
            instance=profile,
        )

    return render(
        request,
        "accounts/profile.html",
        {
            "form": user_form,
            "profile_form": profile_form,
            "profile": profile,
        },
    )


@login_required
def my_orders(request):

    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related("items")
        .order_by("-created")
    )

    return render(
        request,
        "accounts/my_orders.html",
        {
            "orders": orders,
        },
    )

from django.contrib.auth.decorators import login_required
from orders.models import Order
from products.models import Wishlist


@login_required
def dashboard(request):

    orders = Order.objects.filter(user=request.user)

    wishlist_count = Wishlist.objects.filter(
        user=request.user
    ).count()

    context = {

        "orders_count": orders.count(),

        "wishlist_count": wishlist_count,

        "recent_orders": orders.order_by("-created")[:5],

    }

    return render(
        request,
        "accounts/dashboard.html",
        context,
    )

@login_required
def dashboard(request):
    return render(
        request,
        "accounts/dashboard.html",
    )