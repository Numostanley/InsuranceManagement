from django.urls import path, include


urlpatterns = [
    path("category/", include("apps.insurances.views.category.urls", namespace='categories')),
    path("policy/", include("apps.insurances.views.policy.urls", namespace='policy')),
    path("palicy-record/", include("apps.insurances.views.policy_record.urls", namespace='policy-record'))
]
