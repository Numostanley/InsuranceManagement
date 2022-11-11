from django.urls import path
from apps.insurances.views.category import view

urlpatterns = [
    path("create", view.create, name="category-create"),
    path("list", view.list, name="category-list"),
    path("update/<uuid:id>", view.update, name="category-update"),
    path("details/<uuid:id>", view.details, name="category-details"),
]
