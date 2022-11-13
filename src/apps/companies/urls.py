from django.urls import path

from . import views


app_name = "companies"

urlpatterns = [
    path('create', views.create_company, name='create'),
    path('all_companies', views.all_companies, name='all-companies'),
    path('<str:id>', views.company_detail, name='detail'),
    path('<str:id>/update', views.update_company, name='update'),
    path('<str:id>/delete', views.delete_company, name='delete')
]
