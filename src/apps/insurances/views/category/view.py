from apps.insurances.models import Category
from django.shortcuts import render, redirect
from uuid import UUID
from apps.decorators import authorize
from apps.users.views import ADMIN, COMPANY_USER


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
    return render(request, "insurances/category/create.html", {"message" : "Created"})


@authorize([ADMIN])
def update(request, id: UUID):
    try:
        category = Category.objects.get(id=id)
        if request.method == "GET":
            return render(request, "insurances/category/update.html", {"category": category})
        name = request.POST.get("name", category.name)
        category.objects.update(name=name)
        return redirect(list)
    except (Category.DoesNotExist, Category.MultipleObjectsReturned) as e:
        return render(request, "insurances/category/view.html", {"message": "category not found"})


@authorize([ADMIN, COMPANY_USER])
def list(request):
    categories = Category.objects.all()
    return render(request, "insurances/category/view.html", {"categories": categories})


@authorize([ADMIN, COMPANY_USER])
def details(request, id: UUID):
    try:
        category = Category.objects.get(id=id)
        render(request, "", {})
    except (Category.DoesNotExist, Category.MultipleObjectsReturned) as e:
        return render(request, "", {})
