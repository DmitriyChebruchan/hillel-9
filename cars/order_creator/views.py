from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from .forms import UserLogInForm, OrderForm
from .models import Client, Car, Order, Licence
from .supporting_functions import (
    update_cars_status,
    assigning_licence,
    available_cars_generator,
)


def client_list(request):
    clients = Client.objects.all()
    return render(
        request, "list.html", {"elements": clients, "list_name": "Clients"}
    )


def car_list(request):
    cars = Car.objects.all()
    return render(request, "list.html", {"elements": cars, "list_name": "Cars"})


def order_list(request):
    orders = Order.objects.all()
    return render(
        request, "list.html", {"elements": orders, "list_name": "Orders"}
    )


def success(request):
    return render(request, "cancelled_success.html")


def log_in(request):
    if request.method == "POST":
        user_form = UserLogInForm(request.POST)
        if user_form.is_valid():
            client = user_form.cleaned_data["client"]
            return redirect("personal_cabinet/" + str(client.id))
    user_form = UserLogInForm()
    return render(request, "log_in.html", {"form": user_form})


def personal_cabinet(request, pk):
    client = Client.objects.get(pk=pk)
    # Retrieve the user based on the user_id
    return render(request, "personal_cabinet.html", {"client": client})


def make_order(request, pk):
    client = Client.objects.get(pk=pk)
    cars = Car.objects.filter(owner=None, blocked_by_order=None)
    dealership = client.dealerships.first()
    car_types = list({car.car_type for car in cars})
    available_car_quantities = available_cars_generator(car_types, cars)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client, order.dealership = client, dealership

            total_quantity = sum(
                int(request.POST.get(str(car_type), 0))
                for car_type, _ in available_car_quantities
            )

            if total_quantity == 0:
                form = OrderForm()
                return render(
                    request,
                    "make_order.html",
                    {
                        "form": form,
                        "client": client,
                        "car_types": car_types,
                        "available_car_quantities": available_car_quantities,
                        "error_msg": True,
                    },
                )

            order.save()
            update_cars_status(request, order, car_types, cars)
            return redirect("/order_details/" + str(order.id))

    order_info = {
        "form": OrderForm(),
        "client": client,
        "car_types": car_types,
        "available_car_quantities": available_car_quantities,
    }
    return render(request, "make_order.html", order_info)


def order_details(request, pk):
    order = Order.objects.get(pk=pk)
    cars = Car.objects.filter(order=order)
    print("order is", order)
    return render(request, "order_details.html", {"order": order, "cars": cars})


def payment(request, pk):
    order = Order.objects.get(pk=pk)
    cars = Car.objects.filter(order=order)
    client = order.client
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order.is_paid = True
            order.save()
            cars = order.reserved_cars.all()
            for car in cars:
                car.sell(order)
                licence = assigning_licence(car)
                print(licence)
                licence.save()
            return redirect(f"/personal_cabinet/{client.id}")
    else:
        form = OrderForm(instance=order)
    return render(
        request,
        "mark_order_as_paid.html",
        {"form": form, "order": order, "client": client, "cars": cars},
    )


def list_of_clients_orders(request, pk):
    client = Client.objects.get(pk=pk)
    orders = Order.objects.filter(client=client)
    return render(
        request, "your_orders.html", {"orders": orders, "client": client}
    )


def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    cars = Car.objects.filter(order=order)
    if request.method == "POST":
        for car in cars:
            car.unblock()
            licence = Licence.objects.filter(car=car)
            licence.delete()
        cancelled_order = order
        client_id = order.client.id
        order.delete()
        return render(
            request,
            "cancelled_success.html",
            {
                "canceled_order": cancelled_order,
                "title": "Order is cancelled.",
                "client_id": client_id,
            },
        )
    return render(
        request,
        "cancel_order.html",
        {"order": order, "cars": cars},
    )
