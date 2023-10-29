import random

from django.db import IntegrityError

from .models import Licence


def licence_number_generator():
    existing_licence_ids = set(Licence.objects.values_list("car_id", flat=True))
    while True:
        new_licence = str(random.randrange(10 ** 5))
        if new_licence not in existing_licence_ids:
            return new_licence
        else:
            new_licence = str(random.randrange(10 ** 5))
        return new_licence


def assigning_licence(car):
    try:
        licence = Licence(car=car, number=licence_number_generator())
        licence.save()
        return licence
    except IntegrityError:
        # Handle the case where the car_id already exists in the Licence table
        # You can either generate a new licence or handle the situation based on your application's logic
        return None


def update_cars_status(request, order, car_types, cars):
    for car_type in car_types:
        quantity = request.POST.get(str(car_type))
        quantity = 0 if quantity is None else int(quantity)

        available_cars_of_the_type = [
            car for car in cars if car.car_type == car_type
        ]
        selected_cars = available_cars_of_the_type[:quantity]

        for car in selected_cars:
            car.block(order)
            if order.is_paid:
                car.sell(order)
                licence = assigning_licence(car)
                licence.save()
            car.save()
