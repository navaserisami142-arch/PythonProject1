from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order

        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "postal_code",
        ]

        input_class = (
            "w-full rounded-xl border p-3 "
            "bg-white dark:bg-gray-800 "
            "text-gray-900 dark:text-white "
            "placeholder:text-gray-400 dark:placeholder:text-gray-500 "
            "border-gray-300 dark:border-gray-700 "
            "focus:outline-none focus:ring-2 focus:ring-indigo-500 "
            "transition-all duration-300"
        )

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": input_class
            }),

            "last_name": forms.TextInput(attrs={
                "class": input_class
            }),

            "email": forms.EmailInput(attrs={
                "class": input_class
            }),

            "phone": forms.TextInput(attrs={
                "class": input_class
            }),

            "address": forms.Textarea(attrs={
                "class": input_class,
                "rows": 3,
            }),

            "city": forms.TextInput(attrs={
                "class": input_class
            }),

            "postal_code": forms.TextInput(attrs={
                "class": input_class
            }),
        }