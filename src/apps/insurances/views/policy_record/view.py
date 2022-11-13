from django.contrib.auth.decorators import login_required

from apps.insurances.models import PolicyRecord
from django.shortcuts import render, redirect
from uuid import UUID
from apps.decorators import authorize
from apps.users.models import User
from apps.users.views import ADMIN, COMPANY_USER, CUSTOMER


@login_required
@authorize([CUSTOMER])
def create(request, policy_id: UUID):
    user_id = request.user.id
    policy_record = PolicyRecord()
    policy_record.policy_id = policy_id
    policy_record.user_id = user_id
    policy_record.save()
    return redirect("insurances:polices:apply")


@login_required
@authorize([COMPANY_USER])
def update(request, id: UUID, status: str):
    try:
        policy_record = PolicyRecord.objects.get(id=id)
        policy_record.status = status
        policy_record.save()
        return redirect("insurances:records:list", status="All")
    except (PolicyRecord.DoesNotExist, PolicyRecord.MultipleObjectsReturned) as e:
        return redirect("insurances:records:list")


@login_required
@authorize([ADMIN, COMPANY_USER, CUSTOMER])
def list(request, status: str):
    user: User = request.user
    group_name = user.get_group_name()
    base_template = "admin-app/base.html"
    records = PolicyRecord.objects.only("policy", "status",
                                        "user", "creation_date", "id")
    if not status.lower() == "All".lower():
        records.filter(status=status)
    if group_name == COMPANY_USER:
        company_id = request.user.company.id
        records.filter(policy__company_id=company_id)
        base_template = "companies/comp-base.html"
    if group_name == CUSTOMER:
        records.filter(user__id=request.user.id)
        base_template = "customer/base.html"
    page = "insurances/policy_record/view-all.html" if status.lower() == "All".lower() \
        else "insurances/policy_record/list-status.html"
    return render(request, page,
                  {"group": group_name, "base_template": base_template, "records": records})


@login_required
@authorize([COMPANY_USER, ADMIN, CUSTOMER])
def details(request, record_id: UUID):
    try:
        policy_record = PolicyRecord.objects.select_related("user", "policy").get(id=record_id)
        return render(request, "", {})
    except (PolicyRecord.DoesNotExist, PolicyRecord.MultipleObjectsReturned) as e:
        return render(request, "", {})
