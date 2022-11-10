from django.shortcuts import render, redirect

from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from apps.insurance.models import Policy, Category, Question, PolicyRecord
from apps.insurance.forms import QuestionForm
from apps.customer.models import Customer
from apps.customer.forms import CustomerForm, CustomerUserForm


def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'customer/customerclick.html')


def customer_signup_view(request):
    userForm = CustomerUserForm()
    customerForm = CustomerForm()

    context = {
        'userForm': userForm,
        'customerForm' : customerForm
    }

    if request.method == 'POST':
        userForm = CustomerUserForm(request.POST)
        customerForm = CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('customerlogin')
    return render(request,
                  'customer/customersignup.html',
                  context=context)


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    customer = Customer.objects.get(user_id=request.user.id)

    context = {
        'customer': Customer.objects.get(user_id=request.user.id),
        'available_policy': Policy.objects.all().count(),
        'applied_policy': PolicyRecord.objects.filter(customer=customer).count(),
        'total_category': Category.objects.all().count(),
        'total_question': Question.objects.filter(customer=customer).count(),
    }
    return render(request,
                  'customer/customer_dashboard.html',
                  context=context)


def apply_policy_view(request):
    customer = Customer.objects.get(user_id=request.user.id)
    policies = Policy.objects.all()
    return render(request,
                  'customer/apply_policy.html',
                  {'policies': policies, 'customer': customer})


def apply_view(request,pk):
    customer = Customer.objects.get(user_id=request.user.id)
    policy = Policy.objects.get(id=pk)
    policyrecord = PolicyRecord()
    policyrecord.Policy = policy
    policyrecord.customer = customer
    policyrecord.save()
    return redirect('history')


def history_view(request):
    customer = Customer.objects.get(user_id=request.user.id)
    policies = PolicyRecord.objects.filter(customer=customer)
    return render(request,
                  'customer/history.html',
                  {'policies': policies, 'customer': customer})


def ask_question_view(request):
    customer = Customer.objects.get(user_id=request.user.id)
    questionForm = QuestionForm()

    if request.method == 'POST':
        questionForm = QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            question.customer = customer
            question.save()
            return redirect('question-history')
    return render(request,
                  'customer/ask_question.html',
                  {'questionForm': questionForm, 'customer': customer})


def question_history_view(request):
    customer = Customer.objects.get(user_id=request.user.id)
    questions = Question.objects.all().filter(customer=customer)
    return render(request,
                  'customer/question_history.html',
                  {'questions': questions, 'customer': customer})
