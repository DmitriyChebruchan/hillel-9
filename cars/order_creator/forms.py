from django import forms

from .models import Order, LogedInUser


class UserLogInForm(forms.ModelForm):
    class Meta:
        model = LogedInUser
        fields = ["user"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ("client", "dealership", "car")


class MarkOrderAsPaidForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["is_paid"]
