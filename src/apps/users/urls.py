from django.urls import path
from apps.users.views import register, signin, signout, list, update, customer_dashboard, admin_dashboard, \
    company_dashboard, pre_login, assessor_dashboard

app_name = 'users'

urlpatterns = [
    path("signup", register, name="sign-up"),
    path("signin", signin, name="sign-in"),
    path("signout", signout, name="sign-out"),
    path('list', list, name="user-list"),
    path('update/<uuid:pk>', update, name='user-update'),
    path("customer-dashboard", customer_dashboard, name="customer-dashboard"),
    path("admin-dashboard", admin_dashboard, name="admin-dashboard"),
    path("company-dashboard", company_dashboard, name="company-dashboard"),
    path("pre-login", pre_login, name="pre-login"),
    path("assessor-dashboard", assessor_dashboard, name="assessor-dashboard"),
]
