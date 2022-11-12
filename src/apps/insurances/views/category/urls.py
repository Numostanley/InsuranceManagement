from django.urls import path
from apps.insurances.views.category import view


app_name="categories"

urlpatterns = [
    path("home", view.home, name="home"),
    path("create", view.create_category, name="create"),
    path("list", view.category_list, name="list"),
    path("update/<uuid:id>", view.update_category, name="update"),
    path("details/<uuid:id>", view.category_detail, name="category-details"),
]
