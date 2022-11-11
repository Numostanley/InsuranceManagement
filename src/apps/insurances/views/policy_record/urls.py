from django.urls import path
from apps.insurances.views.policy_record import view

urlpatterns = [
    path("create", view.create, name="record-create"),
    path("list/<str:status>", view.list, name="record-list"),
    path("update/<uuid:id>", view.update, name="record-update"),
    path("details/<uuid:id>", view.details, name="record-details"),
]
