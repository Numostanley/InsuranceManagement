from django.urls import path
from apps.users.views import register, signin, signout, list, update, customer_dashboard, admin_dashboard

app_name = 'users'

urlpatterns = [
    path("signup", register, name="sign-up"),
    path("signin", signin, name="sign-in"),
    path("signout", signout, name="sign-out"),
    path('list', list, name="user-list"),
    path('update/<uuid:pk>', update, name='user-update'),
    path("customer-dashboard", customer_dashboard, name="customer-dashboard"),
    path("admin-app-dashboard", admin_dashboard, name="admin-dashboard"),
]
