"""
URL configuration for cars project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import (
    car_list,
    order_list,
    client_list,
    success,
    log_in,
    personal_cabinet,
    make_order,
    order_details,
    payment,
    list_of_clients_orders,
    cancel_order,
)

urlpatterns = [
    path("order_list", order_list, name="order_list"),
    path("car_list", car_list, name="car_list"),
    path("client_list", client_list, name="car_list"),
    path("success", success, name="success"),
    path("log_in", log_in, name="log_in"),
    path("personal_cabinet/<int:pk>", personal_cabinet,
         name="personal_cabinet"),
    path("make_order/<int:pk>", make_order, name="make_order"),
    path("order_details/<int:pk>", order_details, name="order_details"),
    path("payment/<int:pk>", payment, name="payment"),
    path("cancel_order/<int:pk>", cancel_order, name="cancel_order"),
    path("your_orders/<int:pk>", list_of_clients_orders, name="your_orders"),
]
