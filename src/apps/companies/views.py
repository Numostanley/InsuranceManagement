from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Company
from .forms import CreateCompanyForm, UpdateCompanyForm


@login_required
@transaction.atomic
def create_company(request):
    if request.method == "POST":
        form = CreateCompanyForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            if Company.get_company_by_name(form.name) or \
                    Company.get_company_by_email(form.email) or \
                    Company.get_company_by_contact(form.contact) or \
                    Company.get_company_by_website(form.website):
                messages.error(request, f'{form.errors}')
                return render(request, 'companies/create_company.html')
            form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, f'{form.name} is successfully created!')
            return redirect('companies:companies')
        return render(request, 'companies/create_company.html')
    else:
        form = CreateCompanyForm()
    context = {
        'form': form,
        'title': 'Create Company'
    }
    return render(request, 'companies/create_company.html', context)


def all_companies(request):
    companies = Company.get_all_active_companies()
    context = {
        'companies': companies,
        'title': 'All Companies'
    }
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
        'date_created': company.date_created,
        'title': f'{company.name} Detail'
    }

    return render(request, 'companies/company_detail.html', context)


@login_required
def update_company(request, id):
    company = Company.get_company_by_id(id)

    if not company:
        return render(request, '404.html')

    if company.user != request.user:
        return render(request, '403.html')

    if request.method == "POST":
        with transaction.atomic():
            form = UpdateCompanyForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, f'{company.name} is successfully updated!')
            return redirect('companies:detail', id)
    else:
        form = UpdateCompanyForm(data=company)
    context = {
        'form': form,
        'title': f'Update {company.name}'
    }
    return render(request, 'companies/update_company.html', context)


@login_required
def delete_company(request, id):
    company = Company.get_company_by_id(id)

    if not company:
        return render(request, '404.html')

    if request.method == 'POST':
        Company.delete_company_by_id(id)
        messages.success(request, f'{company.name} is successfully deleted!')
        return redirect('companies:companies')
    context = {
        'title': f'Delete {company.name}'
    }
    return render(request, 'companies/delete_company.html', context)
