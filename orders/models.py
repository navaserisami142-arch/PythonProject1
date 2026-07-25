from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Order(models.Model):

    STATUS_CHOICES = [

        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),

    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    address = models.TextField()

    city = models.CharField(max_length=100)

    postal_code = models.CharField(max_length=20)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    paid = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    coupon_code = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    discount = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Order #{self.id}"

    def get_total_price(self):

        total = sum(item.get_total_price() for item in self.items.all())

        if self.discount:

            total -= (
                total * Decimal(self.discount) / Decimal("100")
            )

        return total


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=0
    )

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):

        return f"{self.product.name}"

    def get_total_price(self):

        return self.price * self.quantity