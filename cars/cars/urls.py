from django.contrib import admin
from django.urls import path, include

from .views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("order_creator.urls")),
    path("", index),
]
