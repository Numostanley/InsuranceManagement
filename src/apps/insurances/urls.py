
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("category", include("apps.insurances.views.category.urls"))
]
