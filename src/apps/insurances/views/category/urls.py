from django.urls import path
from apps.insurances.views.category import view

app_name="categories"
urlpatterns = [
    path("home", view.home, name="home"),
    path("create", view.create, name="create"),
    path("list", view.list, name="list"),
    path("update/<uuid:id>", view.update, name="update"),
    path("details/<uuid:id>", view.details, name="category-details"),
]
