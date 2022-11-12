from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse

from apps import decorators
from apps.reviews.forms import Review, ReviewForm
from .models import Company
from .forms import CreateCompanyForm, UpdateCompanyForm
from ..users.views import COMPANY_USER


@transaction.atomic
def create_company(request):
    if request.method == "POST":
        form = CreateCompanyForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            if Company.get_company_by_name(form.data["name"]) or \
                    Company.get_company_by_email(form.data["email"]) or \
                    Company.get_company_by_contact(form.data["contact"]) or \
                    Company.get_company_by_website(form.data["website"]):
                messages.error(request, f'{form.errors}')
                return render(request, 'companies/create_company.html')
            form.save()
            company = Company.get_company_by_name(form.data["name"])
            messages.success(request, f'{form.data["name"]} is successfully created!')
            return redirect(reverse('users:sign-up') + f'?group=Company User&company_id={company.id}')
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


def company_detail(request, id: str):
    company = Company.get_company_by_id(id)

    if not company:
        return render(request, '404.html')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.info(request, f'Login to send a review!')
            return redirect('user:login')
        if request.user.id == company.user.id:
            messages.error(request, f'You cannot review your own company!')
            return redirect('companies:detail', id)

        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            cd = review_form.cleaned_data
            rating = cd['rating']
            comment = cd['comment'] if cd['comment'] else ""

            Review.create_review(company, request.user, rating, comment)
            messages.success(request, f'Your review has been sent!')
            return redirect('companies:detail')
    else:
        review_form = ReviewForm()
    context = {
        'name': company.name,
        'website': company.website,
        'email': company.email,
        'contact': company.contact,
        'photo': company.photo,
        'location': company.location,
        'date_created': company.date_created,
        'title': f'{company.name} Detail',
        'review_form': review_form
    }

    return render(request, 'companies/company_detail.html', context)


@login_required
@decorators.validate_company_user
def update_company(request, id: str):
    company = Company.get_company_by_id(id)

    if not company:
        return render(request, '404.html')

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
@decorators.validate_company_user
def delete_company(request, id: str):
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
