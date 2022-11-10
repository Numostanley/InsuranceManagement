from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User

from apps.customer.models import Customer
from apps.customer.forms import CustomerUserForm, CustomerForm
from core.settings import base
from . import forms, models


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request, 'insurance/index.html')


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    if is_customer(request.user):      
        return redirect('customer/customer-dashboard')
    else:
        return redirect('admin-dashboard')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    context = {
        'total_user': Customer.objects.all().count(),
        'total_policy': models.Policy.objects.all().count(),
        'total_category': models.Category.objects.all().count(),
        'total_question': models.Question.objects.all().count(),
        'total_policy_holder': models.PolicyRecord.objects.all().count(),
        'approved_policy_holder': models.PolicyRecord.objects.all().filter(status='approved').count(),
        'disapproved_policy_holder': models.PolicyRecord.objects.all().filter(status='disapproved').count(),
        'waiting_policy_holder': models.PolicyRecord.objects.all().filter(status='pending').count(),
    }
    return render(request,
                  'admin/admin_dashboard.html',
                  context=context)


@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers = Customer.objects.all()
    return render(request,
                  'admin/admin_view_customer.html',
                  {'customers': customers})


@login_required(login_url='adminlogin')
def update_customer_view(request, pk):
    customer = Customer.objects.get(id=pk)
    user = User.objects.get(id=customer.user_id)
    userForm = CustomerUserForm(instance=user)
    customerForm = CustomerForm(request.FILES, instance=customer)
    context = {
        'userForm': userForm,
        'customerForm': customerForm
    }
    if request.method == 'POST':
        userForm = CustomerUserForm(request.POST, instance=user)
        customerForm = CustomerForm(request.POST,request.FILES, instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,
                  'insurance/update_customer.html',
                  context=context)


@login_required(login_url='adminlogin')
def delete_customer_view(request, pk):
    customer = Customer.objects.get(id=pk)
    user = User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/admin-view-customer')


def admin_category_view(request):
    return render(request, 'admin/admin_category.html')


def admin_add_category_view(request):
    categoryForm = forms.CategoryForm()
    if request.method == 'POST':
        categoryForm = forms.CategoryForm(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('admin-view-category')
    return render(request,
                  'admin/admin_add_category.html',
                  {'categoryForm': categoryForm})


def admin_view_category_view(request):
    categories = models.Category.objects.all()
    return render(request,
                  'admin/admin_view_category.html',
                  {'categories': categories})


def admin_delete_category_view(request):
    categories = models.Category.objects.all()
    return render(request,
                  'admin/admin_delete_category.html',
                  {'categories': categories})


def delete_category_view(request, pk):
    category = models.Category.objects.get(id=pk)
    category.delete()
    return redirect('admin-delete-category')


def admin_update_category_view(request):
    categories = models.Category.objects.all()
    return render(request,
                  'admin/admin_update_category.html',
                  {'categories': categories})


@login_required(login_url='adminlogin')
def update_category_view(request, pk):
    category = models.Category.objects.get(id=pk)
    categoryForm= forms.CategoryForm(instance=category)
    
    if request.method == 'POST':
        categoryForm = forms.CategoryForm(request.POST, instance=category)
        
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('admin-update-category')
    return render(request,
                  'insurance/update_category.html',
                  {'categoryForm': categoryForm})


def admin_policy_view(request):
    return render(request, 'admin/admin_policy.html')


def admin_add_policy_view(request):
    policyForm = forms.PolicyForm()
    
    if request.method == 'POST':
        policyForm = forms.PolicyForm(request.POST)
        if policyForm.is_valid():
            category_id = request.POST.get('category')
            category = models.Category.objects.get(id=category_id)
            policy = policyForm.save(commit=False)
            policy.category = category
            policy.save()
            return redirect('admin-view-policy')
    return render(request,
                  'admin/admin_add_policy.html',
                  {'policyForm': policyForm})


def admin_view_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,
                  'admin/admin_view_policy.html',
                  {'policies': policies})


def admin_update_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,
                  'admin/admin_update_policy.html',
                  {'policies': policies})


@login_required(login_url='adminlogin')
def update_policy_view(request, pk):
    policy = models.Policy.objects.get(id=pk)
    policyForm = forms.PolicyForm(instance=policy)

    if request.method == 'POST':
        policyForm = forms.PolicyForm(request.POST, instance=policy)

        if policyForm.is_valid():
            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            policy = policyForm.save(commit=False)
            policy.category = category
            policy.save()
            return redirect('admin-update-policy')
    return render(request,
                  'insurance/update_policy.html',
                  {'policyForm': policyForm})
  
  
def admin_delete_policy_view(request):
    policies = models.Policy.objects.all()
    return render(request,
                  'admin/admin_delete_policy.html',
                  {'policies': policies})


def delete_policy_view(request, pk):
    policy = models.Policy.objects.get(id=pk)
    policy.delete()
    return redirect('admin-delete-policy')


def admin_view_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all()
    return render(request,
                  'admin/admin_view_policy_holder.html',
                  {'policyrecords': policyrecords})


def admin_view_approved_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='approved')
    return render(request,
                  'admin/admin_view_approved_policy_holder.html',
                  {'policyrecords': policyrecords})


def admin_view_disapproved_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='disapproved')
    return render(request,
                  'admin/admin_view_disapproved_policy_holder.html',
                  {'policyrecords': policyrecords})


def admin_view_waiting_policy_holder_view(request):
    policyrecords = models.PolicyRecord.objects.all().filter(status='pending')
    return render(request,
                  'admin/admin_view_waiting_policy_holder.html',
                  {'policyrecords': policyrecords})


def approve_request_view(request, pk):
    policy_records = models.PolicyRecord.objects.get(id=pk)
    policy_records.status = 'approved'
    policy_records.save()
    return redirect('admin-view-policy-holder')


def disapprove_request_view(request, pk):
    policy_records = models.PolicyRecord.objects.get(id=pk)
    policy_records.status = 'disapproved'
    policy_records.save()
    return redirect('admin-view-policy-holder')


def admin_question_view(request):
    questions = models.Question.objects.all()
    return render(request,
                  'admin/admin_question.html',
                  {'questions': questions})


def update_question_view(request, pk):
    question = models.Question.objects.get(id=pk)
    questionForm = forms.QuestionForm(instance=question)

    if request.method == 'POST':
        questionForm = forms.QuestionForm(request.POST, instance=question)
        
        if questionForm.is_valid():
            admin_comment = request.POST.get('admin_comment')
            question = questionForm.save(commit=False)
            question.admin_comment = admin_comment
            question.save()
            return redirect('admin-question')
    return render(request,
                  'insurance/update_question.html',
                  {'questionForm': questionForm})


def aboutus_view(request):
    return render(request,'insurance/aboutus.html')


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(f'{name} || {email}',
                      message,
                      base.EMAIL_HOST_USER,
                      base.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            return render(request, 'insurance/contactussuccess.html')
    return render(request,
                  'insurance/contactus.html',
                  {'form': sub})
