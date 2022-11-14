from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.decorators import authorize
from apps.insurances.models import Policy
from apps.risk_assessment.models import RiskAssessment
from apps.users.models import User
from apps.users.views import RISK_ASSESSOR, CUSTOMER


def home(request):
    return render(request, "risk-assessment/home.html", {})


@login_required
@authorize([RISK_ASSESSOR])
def submit(request):
    if request.method == 'POST':
        policy_id = request.POST.get("policy_id", None)
        assessment = request.POST.get("assessment", None)
        level = request.POST.get("assessment", None)
        type = request.POST.get('type', None)
        to_check = [assessment, level, type, policy_id]
        if None in to_check or '' in to_check:
            return redirect("risk-assessment:list")
        risk_assessment = RiskAssessment()
        risk_assessment.assessment = assessment
        risk_assessment.risk_level = level
        risk_assessment.type = type
        risk_assessment.assessor = request.user
        risk_assessment.policy_id = policy_id
        risk_assessment.save()
        message = "assessment submitted"

        return render(request, "risk-assessment/assess.html", {"message": message})
    policy_id = request.GET.get("policy_id", None)
    return render(request, "risk-assessment/assess.html", {"policy_id": policy_id})


def assessment(request):
    return render(request, "risk-assessment/policies-for-assessment.html", {"polices": Policy.objects.all()})


@authorize([CUSTOMER])
def list_for_customer(request, policy_id: UUID):
    assessments = RiskAssessment.objects.filter(policy__id=policy_id)
    return render(request, "risk-assessment/list-customer.html", {"assessments": assessments})


@login_required
@authorize([RISK_ASSESSOR])
def list(request):
    assessments = RiskAssessment.objects.select_related("assessor").all()
    return render(request, "risk-assessment/list.html", {"assessments": assessments})


@login_required
def view(request, id: UUID):
    try:
        base_template = "customer/base.html"
        user: User = request.user
        if user.group == RISK_ASSESSOR:
            base_template = "risk_assessment/base.html"
        assessment = RiskAssessment.objects.select_related("policy", "assessor", "policy__company").get(id=id)
        return render(request, "risk-assessment/view.html", {"assessment": assessment, "base_template": base_template})
    except (RiskAssessment.DoesNotExist, RiskAssessment.MultipleObjectsReturned):
        return render(request, "risk-assessment/view.html", {"message": "assessment not found"})
