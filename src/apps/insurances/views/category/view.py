from uuid import UUID

from django.shortcuts import render, redirect

from apps.insurances.models import Category
from apps.decorators import authorize
from apps.users.views import ADMIN, COMPANY_USER


@authorize([ADMIN])
def home(request):
    return render(request, "insurances/category/home.html", {})


@authorize([ADMIN])
def create_category(request):
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


@authorize([ADMIN])
def update_category(request, id: UUID):
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


@authorize([ADMIN, COMPANY_USER])
def category_list(request):
    categories = Category.objects.all()
    return render(request, "insurances/category/view.html", {"categories": categories})


@authorize([ADMIN, COMPANY_USER])
def category_detail(request, id: UUID):
    try:
        category = Category.objects.get(id=id)
        render(request, "", {})
    except (Category.DoesNotExist, Category.MultipleObjectsReturned) as e:
        return render(request, "", {})
