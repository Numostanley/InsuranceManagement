from django.urls import path
from apps.users.views import index, register, signin, signout, list, update

app_name = 'users'

urlpatterns = [
    path("", index, name="index"),
    path("signup", register, name="sign-up"),
    path("signin", signin, name="sign-in"),
    path("signout", signout, name="sign-out"),
    path('list', list, name="user-list"),
    path('update/<uuid:pk>', update, name='user-update')
]
