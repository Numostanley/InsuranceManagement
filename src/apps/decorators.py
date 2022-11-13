from functools import wraps

from django.contrib.auth.models import Group
from django.shortcuts import render

from apps.companies.models import Company
from apps.users.models import User


def validate_company_user(f):
    @wraps(f)
    def func(request, company_id: str, *args, **kwargs):
        company = Company.get_company_by_id(company_id)
        if request.user.id == company.user.id:
            return f(request, *args, **kwargs)
        return render(request, '403.html')
    return func


def authorize(group_names: list):
    def wrapper_func(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return func(request, *args, **kwargs)
            groups_name = [group.name for group in Group.objects.filter(name__in=group_names).only("name")]
            user: User = request.user
            user_group = user.get_group_name()
            if user_group in groups_name:
                return func(request, *args, **kwargs)
            return render(request, "403.html", {})

        return wrapper

    return wrapper_func
