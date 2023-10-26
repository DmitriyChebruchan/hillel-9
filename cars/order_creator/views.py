from django.shortcuts import render, redirect

from .forms import UserLogInForm
from .models import Client, Car, Order


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


def log_in(request):
    if request.method == "POST":
        user_form = UserLogInForm(request.POST)
        if user_form.is_valid():
            client = user_form.cleaned_data['user']
            return redirect("personal_cabinet/" + str(client.id))
    user_form = UserLogInForm()
    return render(request, 'log_in.html', {'form': user_form})


def personal_cabinet(request, pk):
    client = Client.objects.get(pk=pk)
    # Retrieve the user based on the user_id
    return render(request, 'personal_cabinet.html', {'client': client})


def make_order(request, pk):
    return
