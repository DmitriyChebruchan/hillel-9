from django import forms

from .models import Order, LoggedInUser


class UserLogInForm(forms.ModelForm):
    class Meta:
        model = LoggedInUser
        fields = ["client"]
        labels = {"client": "Клієнт"}


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["is_paid"]
        labels = {"is_paid": "Сплачено"}


class MarkOrderAsPaidForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["is_paid"]
        labels = {"is_paid": "Сплатити"}
