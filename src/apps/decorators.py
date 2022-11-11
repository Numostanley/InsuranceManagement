from functools import wraps

from apps.companies.models import Company


def validate_company_user(f):
    @wraps(f)
    def func(request, *args, **kwargs):
        if request.user == '':
            return f(*args, **kwargs)
    return func
