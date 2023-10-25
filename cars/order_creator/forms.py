from django import forms

from .models import Order, OrderQuantity, Client, Dealership, CarType


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["client", "dealership", "is_paid"]


class OrderQuantityForm(forms.ModelForm):
    class Meta:
        model = OrderQuantity
        fields = ["car_type", "quantity", "order"]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "email", "phone"]


class DealershipForm(forms.ModelForm):
    class Meta:
        model = Dealership
        fields = ["name", "available_car_types", "clients"]


class CarTypeForm(forms.ModelForm):
    class Meta:
        model = CarType
        fields = ["name", "brand", "price"]
