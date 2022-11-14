from django.contrib.auth.decorators import login_required

from apps.insurances.models import Category
from django.shortcuts import render, redirect
from uuid import UUID
from apps.decorators import authorize
from apps.users.models import User
from apps.users.views import ADMIN, COMPANY_USER


@login_required
@authorize([ADMIN])
def home(request):
    return render(request, "insurances/category/home.html", {})


@login_required
@authorize([ADMIN])
def create(request):
    if request.method == "GET":
        return render(request, "insurances/category/create.html", {})
    name = request.POST.get("name", None)
    if not name:
        return render(request, "insurances/category/create.html", {"message": "Please enter a name for the category"})
    if Category.objects.filter(name__iexact=name).exists():
        return render(request, "insurances/category/create.html",
                      {"message": f"Category with name {name} already exits"})
    Category.objects.create(name=name)
    return redirect("insurances:categories:list")


@login_required
@authorize([ADMIN])
def update(request, id: UUID):
    try:
        category = Category.objects.get(id=id)
        if request.method == "GET":
            return render(request, "insurances/category/update.html", {"category": category})
        name = request.POST.get("name", category.name)
        category.name = name
        category.save()
        return redirect("insurances:categories:list")
    except (Category.DoesNotExist, Category.MultipleObjectsReturned) as e:
        return render(request, "insurances/category/view.html", {"message": "category not found"})


@login_required
@authorize([ADMIN, COMPANY_USER])
def list(request):
    base_template = "admin-app/base.html"
    group = "Admin"
    categories = Category.objects.all()
    if request.user.is_superuser:
        return render(request, "insurances/category/view.html",
                      {"categories": categories, "base_template": base_template, "group": group})
    user: User = request.user
    group = user.get_group_name()
    if group == COMPANY_USER:
        base_template = "companies/comp-base.html"
        group = "Company User"
    return render(request, "insurances/category/view.html",
                  {"categories": categories, "base_template": base_template, "group": group})


@login_required
@authorize([ADMIN, COMPANY_USER])
def details(request, id: UUID):
    try:
        category = Category.objects.get(id=id)
        render(request, "", {})
    except (Category.DoesNotExist, Category.MultipleObjectsReturned) as e:
        return render(request, "", {})
