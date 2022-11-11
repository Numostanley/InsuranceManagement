from apps.insurances.models import Category
from django.shortcuts import render, redirect
from uuid import UUID


def create(request):
    if request.method == "GET":
        return render(request, "", {})
    name = request.POST.get("name", None)
    if not name:
        return render(request, "", {})
    Category.objects.create(name=name)
    return render(request, "", {})


def update(request, id: UUID):
    try:
        category = Category.objects.get(id=id)
        if request.method == "GET":
            return render(request, "", {})
        name = request.POST.get("name", None)
        if not name:
            return render(request, "", {})
        category.objects.update(name=name)
        return redirect(list)
    except (Category.DoesNotExist, Category.MultipleObjectsReturned) as e:
        return render(request, "", {})


def list(request):
    categories = Category.objects.all()
    return render(request, "", {})


def details(request, id: UUID):
    try:
        category = Category.objects.get(id=id)
        render(request, "", {})
    except (Category.DoesNotExist, Category.MultipleObjectsReturned) as e:
        return render(request, "", {})
