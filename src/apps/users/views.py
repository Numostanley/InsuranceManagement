import uuid
from typing import Tuple
import re

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

from apps.risk_assessment.models import RiskAssessment
from apps.users.models import User
from apps.insurances.models import Policy, PolicyRecord, Category
from django.contrib.auth.models import Group
from apps.users.dto import RegisterUser, UpdateUser
from apps.companies.models import Company

# Group Names
ADMIN = "Admin"
COMPANY_USER = "Company User"
CUSTOMER = "Customer"
RISK_ASSESSOR = "Risk Assessor"


def pre_login(request):
    return render(request, "user/pre-login.html", {})


def assessor_dashboard(request):
    context = {
        'total_assessment': RiskAssessment.objects.filter(assessor=request.user).count(),
        'total_polices': Policy.objects.all().count(),
    }
    return render(request, "risk-assessment/dashboard.html", context)


@login_required
def customer_dashboard(request):
    context = {
        "total_policy": Policy.objects.all().count(),
        "total_applied": PolicyRecord.objects.filter(user=request.user).count(),
        "total_category": Category.objects.all().count()
    }
    return render(request, "customer/dashboard.html", context)


@login_required
def company_dashboard(request):
    context = {
        "total_policies": Policy.objects.all().count(),
        "total_categories": Category.objects.all().count(),
        "total_applied": PolicyRecord.objects.all().count(),
        "total_approved": PolicyRecord.objects.filter(status="Approved").count(),
        "total_rejected": PolicyRecord.objects.filter(status="Rejected").count(),
        "total_pending": PolicyRecord.objects.filter(status="Pending").count()
    }
    return render(request, "companies/dashboard.html", context)


@login_required
def admin_dashboard(request):
    context = {
        "total_users": User.objects.all().count(),
        "total_policies": Policy.objects.all().count(),
        "total_categories": Category.objects.all().count(),
        "total_applied": PolicyRecord.objects.all().count(),
        "total_approved": PolicyRecord.objects.filter(status="Approved").count(),
        "total_rejected": PolicyRecord.objects.filter(status="Rejected").count(),
        "total_pending": PolicyRecord.objects.filter(status="Pending").count(),
        "total_companies": Company.objects.all().count(),
    }
    return render(request, "admin-app/dashboard.html", context)


def register(request):
    if request.method == "POST":
        is_valid, message = _validate(request)
        if not is_valid:
            return _render_registration_view(request, message)
        user = _save(message, request.FILES.get("image", None))
        company_id = request.POST.get("company_id", None)
        if company_id:
            company = Company.get_company_by_id(company_id)
            company.user = user
            company.save()
        return redirect("users:sign-in")
    return _render_registration_view(request)


@login_required
def list(request):
    users = User.objects.exclude(is_superuser=True).defer("password").all()
    return render(request, "user/user-list.html", context={'users': users})


def signin(request):
    if request.method == "GET":
        return render(request, "user/signin.html", {})
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    user: User = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        if user.is_superuser:
            return redirect("users:admin-dashboard")
        elif user.group.name == ADMIN:
            return redirect("users:admin-dashboard")
        elif user.group.name == COMPANY_USER:
            return redirect("users:company-dashboard")
        elif user.group.name == CUSTOMER:
            return redirect("users:customer-dashboard")
        elif user.group.name == RISK_ASSESSOR:
            return redirect("users:assessor-dashboard")
    return render(request, "user/signin.html", {"message": "Username or Password Incorrect"})


def signout(request):
    logout(request)
    return render(request, "main/index.html", {})


@login_required
def update(request, pk: uuid.UUID):
    try:
        user = User.objects.get(id=pk)
        if request.method == "GET":
            return render(request, "user/user-update.html", context={"user": user})
        model = _get_attribute_from_request_update(request, user)
        user.first_name = model.first_name
        user.last_name = model.last_name
        user.location = model.location
        user.phone_number = model.phone_number
        user.save()
        return list(request)
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        return render(request, "user/user-list.html", {})


@login_required
def details(request, pk: uuid.UUID):
    try:
        user = User.objects.exclude("password").get(id=pk)
        return render(request, "", {})
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        return render(request, "", {})


@login_required
def delete(request, pk: uuid.UUID):
    try:
        User.objects.get(id=pk).delete()
        return render(request, "", {})
    except (User.DoesNotExist, User.MultipleObjectsReturned):
        return render(request, "", {})


def _add_user_to_group(user: User, group: str):
    group, _ = Group.objects.get_or_create(name=group)
    user.group = group
    user.save()


def _render_registration_view(request, message=None):
    if request.method == "GET":
        group: str = request.GET.get("group", "")
        company_id = request.GET.get("company_id", "")
    else:
        group: str = request.POST.get("group", "")
        company_id = request.POST.get("company_id", "")
    if group.lower() == COMPANY_USER.lower():
        return render(request, "companies/company-user.html",
                      {"group": COMPANY_USER, "company_id": company_id, "message": message})
    if group.lower() == RISK_ASSESSOR.lower():
        return render(request, "user/siginup.html", {"group": RISK_ASSESSOR, "message": message})
    return render(request, "user/siginup.html", {"group": CUSTOMER, "message": message})


def _save(data: RegisterUser, file) -> User:
    user = User()
    user.id = uuid.uuid4()
    user.first_name = data.first_name
    user.last_name = data.last_name
    user.email = data.email
    user.username = data.username
    user.location = data.location
    user.password = make_password(password=data.password)
    user.phone_number = data.phone_number
    user.image = file
    user.save()

    # assign user to group
    _add_user_to_group(user, data.group)
    return user


def _validate(request) -> Tuple[bool, str] or Tuple[bool, RegisterUser]:
    is_valid, data = _get_attribute_from_request_reg(request)
    if not is_valid:
        return False, data
    is_valid, message = _validate_password(data.password, data.confirm_password)
    if not is_valid:
        return False, message
    is_email_exits = _check_if_exit(is_email=True, email=data.email)
    is_username_exits = _check_if_exit(is_username=True, username=data.username)
    if is_username_exits or is_email_exits:
        return False, "Username or email already exit"
    return True, data


def _get_attribute_from_request_reg(request) -> Tuple[
                                                    bool, RegisterUser] or \
                                                Tuple[
                                                    bool, str]:
    model = RegisterUser()
    # get required fields and validate
    model.email = request.POST.get("email", None)
    model.username = request.POST.get("username", None)
    model.password = request.POST.get("password", None)
    model.confirm_password = request.POST.get("confirm_password", None)
    to_check = [model.email, model.username, model.password, model.confirm_password]
    if None in to_check or '' in to_check:
        return False, "Please ensure you fill data for 'username, email, password and confirm password'"
    model.first_name = request.POST.get("first_name", "")
    model.last_name = request.POST.get("last_name", "")
    model.location = request.POST.get("location", "")
    model.phone_number = request.POST.get("phone_number", "")
    model.group = request.POST.get("group", CUSTOMER)
    return True, model


def _get_attribute_from_request_update(request, user) -> UpdateUser:
    model = UpdateUser()
    model.first_name = request.POST.get("first_name", user.first_name)
    model.last_name = request.POST.get("last_name", user.last_name)
    model.location = request.POST.get("location", user.location)
    model.phone_number = request.POST.get("phone_number", user.phone_number)
    return model


def _validate_password(password: str, confirm_password) -> Tuple[bool, str]:
    if password != confirm_password:
        return False, "Password dose not match"
    if len(re.findall(r"[0-9]", password)) == 0:
        return False, "Password should have at least one number."

    if len(re.findall(r"[a-z]", password)) == 0:
        return False, "Passwords should have at least one lowercase letter."

    if len(re.findall(r"[A-Z]", password)) == 0:
        return False, "Passwords should have at least one uppercase letter."

    if len(re.findall(r"\W", password)) == 0:
        return False, "Passwords should have at least one special character."
    return True, ""


def _check_if_exit(is_email=False, is_username=False, email=None, username=None):
    if is_email:
        return User.objects.filter(email__iexact=email).exists()
    elif is_username:
        return User.objects.filter(username__iexact=username).exists()
