<<<<<<< HEAD

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("category", include("apps.insurances.views.category.urls"))
]
=======
from django.urls import path

from . import views


app_name = 'insurances'

urlpatterns = [
    path('categories', views.categories, name='categories'),
    path('policies', views.policies, name='policies'),
    path('user-policy-records', views.user_policy_records, name='user-policy-record')
]
>>>>>>> rawkib_testing
