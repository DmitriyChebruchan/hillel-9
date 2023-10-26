from django import forms

from .models import Order, LogedInUser


class ClientForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client']


class UserLogInForm(forms.ModelForm):
    class Meta:
        model = LogedInUser
        fields = ["user"]
