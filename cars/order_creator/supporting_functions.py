def save_order(order_form, client):
    order = order_form.save(commit=False)
    order.client = client
    order.save()
    return order


def update_cars(order, cars):
    for car in cars:
        if order.is_paid:
            car.sell(order)
        else:
            car.block(order)
