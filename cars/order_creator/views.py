from django import forms
from django.shortcuts import render

from .forms import OrderForm, OrderQuantityForm
from .models import Client, Car, Order


class AddToOrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)


def client_list(request):
    clients = Client.objects.all()
    return render(request, "list.html", {"elements": clients, "list_name": "Clients"})


def car_list(request):
    cars = Car.objects.all()
    return render(request, "list.html", {"elements": cars, "list_name": "Cars"})


def order_list(request):
    orders = Order.objects.all()
    return render(request, "list.html", {"elements": orders, "list_name": "Orders"})


def success(request):
    return render(request, "result_of_order.html")


def create_order(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        order_quantity_form = OrderQuantityForm(request.POST)
        print(order_form.is_valid())
        if order_form.is_valid() and order_quantity_form.is_valid():
            order = order_form.save()
            order_quantity = order_quantity_form.save(commit=False)
            order_quantity.order = order
            order_quantity.save()
            return render(request, "result_of_order.html", {
                'result': "Order is successful!"})
    else:
        order_form = OrderForm()
        order_quantity_form = OrderQuantityForm()
    return render(request, "create_order.html",
                  {"order_form": order_form,
                   "order_quantity_form": order_quantity_form})
