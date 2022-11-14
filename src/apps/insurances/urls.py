from apps.insurances import views
from django.urls import path, include

app_name = 'insurances'
urlpatterns = [
    path("category/", include("apps.insurances.views.category.urls")),
    path("policy/", include("apps.insurances.views.policy.urls")),
    path("policy-record/", include("apps.insurances.views.policy_record.urls"))
    # path('categories', views.categories, name='categories'),
    # path('policies', views.policies, name='policies'),
    # path('user-policy-records', views.user_policy_records, name='user-policy-record')
]
