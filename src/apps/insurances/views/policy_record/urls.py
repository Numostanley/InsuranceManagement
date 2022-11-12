from django.urls import path
from apps.insurances.views.policy_record import view


app_name = "records"

urlpatterns = [
    path("create", view.create_policy_record, name="create"),
    path("list/<str:status>", view.policy_record_list, name="list"),
    path("update/<uuid:id>", view.update_policy_record, name="update"),
    path("details/<uuid:id>", view.policy_record_detail, name="details"),
]
