from django.urls import path
from apps.insurances.views.policy import view
app_name = "polices"
urlpatterns = [
    path("create", view.create, name="create"),
    path("list", view.list, name="list"),
    path("update/<uuid:id>", view.update, name="update"),
    path("details/<uuid:id>", view.details, name="policy-details"),
    path("apply", view.apply, name="apply"),
    path("home", view.home, name="home")
]
