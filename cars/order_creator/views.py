from django.shortcuts import get_object_or_404, render, redirect

from .forms import UserLogInForm, OrderForm, MarkOrderAsPaidForm
from .models import Client, Car, Order


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
            client = user_form.cleaned_data["user"]
            return redirect("personal_cabinet/" + str(client.id))
    user_form = UserLogInForm()
    return render(request, "log_in.html", {"form": user_form})


def personal_cabinet(request, pk):
    client = Client.objects.get(pk=pk)
    # Retrieve the user based on the user_id
    return render(request, "personal_cabinet.html", {"client": client})


def make_order(request, pk):
    client = Client.objects.get(pk=pk)
    dealership = client.dealerships.first()
    cars = Car.objects.filter(owner=None, blocked_by_order=None)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = client
            order.dealership = dealership
            order.save()  # Save the order first

            car_ids = request.POST.getlist("car")
            for car_id in car_ids:
                car = Car.objects.get(pk=car_id)
                car.block(order)
                if order.is_paid:
                    car.sell()
                car.save()  # Save the car after the order

            return redirect("/order_details/" + str(order.id))
    else:
        form = OrderForm()
    return render(
        request,
        "make_order.html",
        {"form": form, "client": client, "cars": cars},
    )


def order_details(request, pk):
    order = Order.objects.get(pk=pk)
    cars = Car.objects.filter(order=order)
    return render(request, "order_details.html", {"order": order, "cars": cars})


def payment(request, pk):
    order = Order.objects.get(pk=pk)
    client = order.client
    if request.method == "POST":
        form = MarkOrderAsPaidForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            cars = order.reserved_cars.all()
            for car in cars:
                car.sell()
            return redirect("/personal_cabinet/" + str(client.id))
    else:
        form = MarkOrderAsPaidForm(instance=order)
    return render(
        request,
        "mark_order_as_paid.html",
        {"form": form, "order": order, "client": client},
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
