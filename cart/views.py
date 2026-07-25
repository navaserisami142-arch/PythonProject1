from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string

from products.models import Product, Coupon
from .cart import Cart
from .forms import CouponForm


def cart_detail(request):
    cart = Cart(request)
    form = CouponForm()
    return render(request, "cart/detail.html", {
        "cart": cart,
        "form": form,
    })


def cart_add(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get("quantity", 1))

    cart.add(product=product, quantity=quantity)

    # Ajax Request
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "cart_count": len(cart),
            "product": product.name,
        })

    messages.success(
        request,
        f'"{product.name}" added to cart successfully!'
    )

    return redirect("cart_detail")


def cart_remove(request, product_id):
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        html = render_to_string(
            "cart/drawer.html",
            {"cart": cart},
            request=request
        )

        return JsonResponse({

            "success": True,

            "html": html,

            "count": len(cart),

            "total": str(cart.get_total_price_after_discount())

        })

    messages.success(request, f'"{product.name}" removed from cart!')

    return redirect("cart_detail")


def apply_coupon(request):
    if request.method == "POST":
        form = CouponForm(request.POST)

        if form.is_valid():

            code = form.cleaned_data["code"]

            try:

                coupon = Coupon.objects.get(
                    code__iexact=code,
                    active=True,
                    valid_from__lte=timezone.now(),
                    valid_to__gte=timezone.now(),
                )

                request.session["coupon_id"] = coupon.id

                messages.success(
                    request,
                    f'Coupon "{code}" applied! {coupon.discount}% discount.'
                )

            except Coupon.DoesNotExist:

                request.session["coupon_id"] = None

                messages.error(
                    request,
                    "Invalid or expired coupon code."
                )

    return redirect("cart_detail")


def cart_drawer(request):
    cart = Cart(request)

    html = render_to_string(
        "cart/drawer.html",
        {"cart": cart},
        request=request
    )

    return JsonResponse({
        "html": html,
        "count": len(cart),
        "total": cart.get_total_price_after_discount()
    })