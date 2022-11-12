from django.urls import path
from apps.insurances.views.policy import view


app_name = "polices"

urlpatterns = [
    path("create", view.create_policy, name="create"),
    path("list", view.policy_list, name="list"),
    path("update/<uuid:id>", view.update_policy, name="update"),
    path("details/<uuid:id>", view.policy_detail, name="policy-details"),
    path("apply", view.apply, name="apply"),
    path("home", view.home, name="home")
]
