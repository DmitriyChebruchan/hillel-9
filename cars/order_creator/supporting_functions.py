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
            car.save()
