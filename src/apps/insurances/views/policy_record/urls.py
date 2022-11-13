from django.urls import path
from apps.insurances.views.policy_record import view


app_name = "records"

urlpatterns = [
    path("create/<uuid:policy_id>", view.create, name="create"),
    path("list/<str:status>", view.list, name="list"),
    path("update/<uuid:id>/<str:status>", view.update, name="update"),
    path("details/<uuid:id>", view.details, name="details"),
]
