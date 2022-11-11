from django.shortcuts import render, redirect
from django.db import transaction

from .models import Company
from .forms import CreateCompanyForm, UpdateCompanyForm


@transaction.atomic
def create_company(request):
    if request.method == "POST":
        form = CreateCompanyForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect()
        return render(request, 'companies/create_company.html')
    else:
        form = CreateCompanyForm()
    context = {
        'form': form
    }
    return render(request, 'companies/create_company.html', context)


def all_companies(request):
    context = Company.get_all_active_companies()
    return render(request, 'companies/all_companies.html', context)


def company_detail(request, id):
    company = Company.get_company_by_id(id)

    if not company:
        return render(request, '404.html')

    context = {
        'name': company.name,
        'website': company.website,
        'email': company.email,
        'contact': company.contact,
        'photo': company.photo,
        'location': company.location,
        'date_created': company.date_created
    }

    return render(request, 'companies/company_detail.html', context)


def update_company(request, id):
    company = Company.get_company_by_id(id)

    if not company:
        return render(request, '404.html')

    if request.method == "POST":
        form = UpdateCompanyForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = UpdateCompanyForm(data=company)
    context = {
        'form': form
    }
    return render(request, 'companies/update_company.html', context)


def delete_company(request, id):
    company = Company.get_company_by_id(id)

    if not company:
        return render(request, '404.html')

    return render(request, 'companies/delete_company.html')
