from django import forms

from .models import Order, LogedInUser, Car


class UserLogInForm(forms.ModelForm):
    class Meta:
        model = LogedInUser
        fields = ["user"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['is_paid']


class CarAssignmentForm(forms.Form):
    available_cars = Car.objects.filter(owner__isnull=True,
                                        blocked_by_order__isnull=True)
    cars = forms.ModelMultipleChoiceField(queryset=available_cars, required=False)
