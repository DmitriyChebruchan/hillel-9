from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class LoggedInUser(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)


class CarType(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.brand} {self.name}"


class Car(models.Model):
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    year = models.IntegerField()
    blocked_by_order = models.ForeignKey(
        "Order",
        on_delete=models.SET_NULL,
        null=True,
        related_name="reserved_cars",
    )
    owner = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, related_name="cars"
    )
    order = models.ForeignKey("Order", null=True, on_delete=models.SET_NULL)

    def block(self, order):
        self.blocked_by_order = order
        self.order = order
        self.save()

    def unblock(self):
        self.blocked_by_order = None
        self.order = None
        self.owner = None
        self.licence.delete()
        self.save()

    def sell(self, order):
        self.blocked_by_order = order
        self.order = order
        self.owner = self.blocked_by_order.client
        self.save()

    def __str__(self):
        try:
            licence_str = f"Номер: {self.licence}"
        except AttributeError:
            licence_str = ""

        owner = f"Власник: {self.owner}" if self.owner else ""
        order = f"{self.blocked_by_order}" if self.blocked_by_order else ""

        arguments = [
            str(arg)
            for arg in [self.car_type, self.color, order, owner, licence_str]
            if arg
        ]
        return " - ".join(arguments)


class Licence(models.Model):
    car = models.OneToOneField(
        Car, on_delete=models.SET_NULL, null=True, related_name="licence"
    )
    number = models.CharField(max_length=50)

    def __str__(self):
        return self.number


class Dealership(models.Model):
    name = models.CharField(max_length=50)
    available_car_types = models.ManyToManyField(
        CarType, related_name="dealerships"
    )
    clients = models.ManyToManyField(Client, related_name="dealerships")

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="orders"
    )
    dealership = models.ForeignKey(
        Dealership, on_delete=models.CASCADE, related_name="orders"
    )
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Замовлення: {self.id}"
