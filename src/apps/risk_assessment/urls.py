from django.urls import path
from apps.risk_assessment import views


app_name="risk-assessment"

urlpatterns = [
    path("home", views.home, name="home"),
    path("create", views.submit, name="create"),
    path("list", views.list, name="list"),
    path("view/<uuid:id>", views.view, name="view"),
    path("policy-assessment-list", views.assessment, name="view-list"),
]
