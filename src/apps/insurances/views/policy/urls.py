from django.urls import path
from apps.insurances.views.policy import view

urlpatterns = [
    path("create", view.create, name="policy-create"),
    path("list", view.list, name="policy-list"),
    path("update/<uuid:id>", view.update, name="policy-update"),
    path("details/<uuid:id>", view.details, name="policy-details"),
]
