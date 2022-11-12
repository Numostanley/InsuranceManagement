from functools import wraps

from django.shortcuts import render

from apps.companies.models import Company


def validate_company_user(f):
    @wraps(f)
    def func(request, company_id: str, *args, **kwargs):
        company = Company.get_company_by_id(company_id)
        if request.user.id == company.user.id:
            return f(*args, **kwargs)
        return render(request, '403.html')
    return func
