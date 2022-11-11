from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Category, Policy, PolicyRecord


def categories(request):
    all_categories = Category.get_all_categories()
    context = {
        'categories': all_categories,
        'title': 'Categories'
    }
    return render(request, 'insurances/categories.html', context)


def policies(request):
    all_policies = Policy.get_all_policies()
    context = {
        'policies': all_policies,
        'title': 'Policies'
    }
    return render(request, 'insurances/policies.html', context)


@login_required
def user_policy_records(request):
    policy_records = PolicyRecord.get_all_policy_records(request.user)

    context = {
        'policy_records': policy_records,
        'title': f'{request.user.username} Policy Records'
    }
    return render(request, 'insurances/user_policy_records.html', context)


@login_required
def user_policy_record_detail(request, id):
    policy_record = PolicyRecord.get_user_policy_record(request.user, id)

    context = {
        'policy_record': policy_record,
        'title': f'Policy Record {policy_record.id}'
    }
    return render(request, '', context)
