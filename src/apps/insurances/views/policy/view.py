from django.contrib.auth.decorators import login_required

from apps.insurances.models import Policy, PolicyRecord, Category
from django.shortcuts import render, redirect
from uuid import UUID
from apps.decorators import authorize
from apps.users.models import User
from apps.users.views import ADMIN, COMPANY_USER, CUSTOMER


@login_required
@authorize([COMPANY_USER, ADMIN])
def home(request):
    user: User = request.user
    if request.user.is_superuser:
        group_name = "Admin"
    else:
        group_name = user.get_group_name()
    total_application = 0
    total_disapproved = 0
    total_pending = 0
    total_approved = 0
    base_template = 'admin-app/base.html'
    if group_name == ADMIN:
        total_application = PolicyRecord.objects.all().count()
        total_approved = PolicyRecord.objects.filter(status="Approved").count()
        total_disapproved = PolicyRecord.objects.filter(status="DisApproved").count()
        total_pending = PolicyRecord.objects.filter(status="Pending").count()

    elif group_name == COMPANY_USER:
        company_id = request.user.company.id
        total_application = PolicyRecord.objects.filter(policy__company_id=company_id).count()
        total_approved = PolicyRecord.objects.filter(status="Approved").count()
        total_disapproved = PolicyRecord.objects.filter(status="DisApproved", policy__company_id=company_id).count()
        total_pending = PolicyRecord.objects.filter(status="Pending", policy__company_id=company_id).count()
        base_template = 'companies/comp-base.html'
    return render(request, "insurances/policy/home.html",
                  {"total_application": total_application, "total_disapproved": total_disapproved,
                   "total_pending": total_pending, "total_approved": total_approved, "group": group_name,
                   "base_template": base_template})


@login_required
def apply(request):
    policies = Policy.objects.all()
    return render(request, "insurances/policy/apply.html", {"polices": policies})


@login_required
@authorize([COMPANY_USER])
def create(request):
    if request.method == "GET":
        categories = Category.objects.only("id", "name").all()
        return render(request, "insurances/policy/create.html", {"categories": categories})
    category_id = request.POST.get("category_id", None)
    name = request.POST.get("name", None)
    sum_assurance = request.POST.get("sum_assurance", None)
    premium = request.POST.get("premium", None)
    tenure = request.POST.get("tenure", None)
    company_id = request.user.company.id
    if None in [category_id, name, sum_assurance, premium, tenure]:
        return render(request, "insurances/policy/create.html", {"message": "Please ensure you fill all data"})
    if Policy.objects.filter(name__iexact=name).exists():
        return render(request, "insurances/policy/create.html", {"message": "Policy name already exits"})
    policy = Policy()
    policy.company_id = company_id
    policy.category_id = category_id
    policy.name = name
    policy.sum_assurance = sum_assurance
    policy.premium = premium
    policy.tenure = tenure
    policy.save()
    return redirect("insurances:polices:list")


@login_required
@authorize([COMPANY_USER, CUSTOMER])
def update(request, id: UUID):
    try:
        policy = Policy.objects.get(id=id)
        if request.method == 'GET':
            return render(request, "insurances/policy/update.html", {"policy": policy})
        category_id = request.POST.get("category_id", policy.category_id)
        name = request.POST.get("name", policy.name)
        sum_assurance = request.POST.get("sum_assurance", policy.sum_assurance)
        premium = request.POST.get("premium", policy.premium)
        tenure = request.POST.get("tenure", policy.tenure)
        policy.category_id = category_id
        policy.name = name
        policy.sum_assurance = sum_assurance
        policy.premium = premium
        policy.tenure = tenure
        policy.save()
        return redirect("insurances:polices:list")
    except (Policy.DoesNotExist, Policy.MultipleObjectsReturned) as e:
        return render(request, "insurances/policy/", {"message": "No Policy found"})


@login_required
@authorize([ADMIN, COMPANY_USER, CUSTOMER])
def list(request):
    user: User = request.user
    base_template = 'admin-app/base.html'
    records = Policy.objects.only("name", "sum_assurance", "tenure", "company", "category",
                                  "premium", "creation_date", "id")
    if request.user.is_superuser:
        return render(request, "insurances/policy/list.html",
                      {"base_template": base_template, "policies": records, "group": "Admin"})
    group_name = user.get_group_name()
    if group_name == COMPANY_USER:
        company_id = request.user.company.id
        records = records.filter(company_id=company_id)
        base_template = 'companies/comp-base.html'
    return render(request, "insurances/policy/list.html",
                  {"base_template": base_template, "policies": records, "group": group_name})


@login_required
@authorize([ADMIN, COMPANY_USER, CUSTOMER])
def details(request, policy_id: UUID):
    try:
        policy = Policy.objects.get(id=policy_id)
        return render(request, "", {})
    except (Policy.DoesNotExist, Policy.MultipleObjectsReturned) as e:
        return render(request, "", {})
