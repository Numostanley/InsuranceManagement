from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

from apps.companies.models import Company
from .forms import ReviewForm
from .models import Review


@login_required
@transaction.atomic
def create_review(request, company_id: str):
    company = Company.get_company_by_id(company_id)

    if not company:
        return render(request, '404.html')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.info(request, 'Login to send a review!')
            return redirect('users:sign-in')

        if request.user.id == company.user.id:
            messages.error(request, f'You cannot review your company!')
            return redirect('companies:detail', company.id)

        if Review.has_user_reviewed(company, request.user):
            messages.error(request, f'You already reviewed this company!')
            return redirect('companies:detail', company.id)

        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            cleaned_data = review_form.cleaned_data
            rating = cleaned_data['rating']
            comment = cleaned_data['comment'] if cleaned_data else ''
            review = Review.create_review(company, request.user, rating, comment)
            messages.success(request, f'Successfully reviewed!')
            review.save()
            return redirect('companies:detail', company.id)
    else:
        review_form = ReviewForm()
    context = {
        'review_form': review_form
    }
    return render(request, 'includes/review.html', context)
