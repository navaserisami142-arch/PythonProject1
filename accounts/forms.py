from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegisterForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "w-full px-5 py-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder:text-gray-400 focus:ring-2 focus:ring-indigo-500 outline-none transition",
                "placeholder": "Username",
            }
        )
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "w-full px-5 py-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder:text-gray-400 focus:ring-2 focus:ring-indigo-500 outline-none transition",
                "placeholder": "Email",
            }
        ),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-5 py-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder:text-gray-400 focus:ring-2 focus:ring-indigo-500 outline-none transition",
                "placeholder": "Password",
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full px-5 py-4 rounded-xl border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder:text-gray-400 focus:ring-2 focus:ring-indigo-500 outline-none transition",
                "placeholder": "Confirm Password",
            }
        )
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border rounded-xl"
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border rounded-xl"
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full p-3 border rounded-xl"
                }
            ),
        }


class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [
            "avatar",
            "phone",
            "address",
            "birth_date",
        ]

        widgets = {

            "avatar": forms.FileInput(
                attrs={
                    "class": "w-full p-3 border rounded-xl"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "w-full p-3 border rounded-xl",
                    "placeholder": "Phone Number"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "w-full p-3 border rounded-xl",
                    "rows": 4,
                    "placeholder": "Your Address"
                }
            ),

            "birth_date": forms.DateInput(
                attrs={
                    "class": "w-full p-3 border rounded-xl",
                    "type": "date"
                }
            ),

        }