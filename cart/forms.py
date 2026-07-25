from django import forms


class CouponForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter coupon code...',
            'class': 'w-full border border-gray-300 rounded-xl px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )