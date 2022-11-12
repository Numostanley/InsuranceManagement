from django.urls import path
from apps.insurances.views.policy_record import view


app_name = "records"

urlpatterns = [
    path("create", view.create, name="create"),
    path("list/<str:status>", view.list, name="list"),
    path("update/<uuid:id>", view.update, name="update"),
    path("details/<uuid:id>", view.details, name="details"),
]
