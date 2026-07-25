from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm
from django.http import HttpResponse
from .pdf import render_invoice
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def order_create(request):

    cart = Cart(request)

    if len(cart) == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("cart_detail")

    if request.method == "POST":

        form = OrderCreateForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user

            if cart.coupon:
                order.coupon_code = cart.coupon.code
                order.discount = cart.coupon.discount

            order.save()

            # ساخت آیتم‌های سفارش
            for item in cart:

                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            # ==========================
            # ارسال ایمیل تأیید سفارش
            # ==========================

            subject = f"Order Confirmation #{order.id}"


            html_message = render_to_string(
                "emails/order_confirmation.html",
                {
                    "order": order,
                },
            )

            email = EmailMultiAlternatives(
                subject=subject,
                body="Thank you for your purchase.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[order.email],
            )

            email.attach_alternative(
                html_message,
                "text/html",
            )

            email.send()

            # ==========================

            cart.clear()

            return redirect("order_success", order.id)

    else:

        form = OrderCreateForm()

    return render(
        request,
        "orders/order_create.html",
        {
            "cart": cart,
            "form": form,
        },
    )


def order_success(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    return render(
        request,
        "orders/order_success.html",
        {
            "order": order,
        },
    )

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created")

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders,
        },
    )

@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
        },
    )

@login_required
def order_invoice(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "orders/order_invoice.html",
        {
            "order": order,
        }
    )

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import Order
from .pdf import render_invoice


@login_required
def order_invoice(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    pdf = render_invoice(order)

    response = HttpResponse(
        pdf,
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="Invoice-{order.id}.pdf"'
    )

    return response