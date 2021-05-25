from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,ExpensCreateForm,DateSearchForm,ReviewExpenseForm
from django.contrib.auth import authenticate,login,logout
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

# Create your views here.
#registration
#login
#logout
def signin(request):
    if request.method=="POST":
        uname=request.POST.get("uname")
        pwd=request.POST.get("password")
        #authenticate user with this username nd password
        #user model authenticate
        user=authenticate(username=uname,password=pwd)
        if user is not None:
            login(request,user)
            return render(request,"budget/home.html")
        else:
            return render(request,"budget/login.html")

    return render(request,"budget/login.html")

def registration(request):
    form=UserRegistrationForm()
    context={}
    context["form"]=form
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("user created")
            return redirect("signin")
        else:
            context["form"]=form
            return render(request, "budget/registration.html", context)

    return render(request,"budget/registration.html",context)


def signout(request):
        logout(request)
        return redirect("signin")

@login_required
def expens_create(request):
    form=ExpensCreateForm(initial={'user':request.user})
    context={}
    context["form"]=form
    if request.method=="POST":
        form=ExpensCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("addexpens")
        else:
            context['form']=form
            return render(request,"budget/addexpense.html",context)
    return render(request,"budget/addexpense.html",context)

@login_required
def view_expense(request):
    form=DateSearchForm()
    context={}
    expense=Expense.objects.filter(user=request.user)
    context["form"]=form
    context["expense"]=expense
    if request.method=="POST":
        form=DateSearchForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data.get("date")
            expense=Expense.objects.filter(date=date,user=request.user)
            context["expense"] = expense
            return render(request, "budget/viewexpense.html", context)

    return render(request,"budget/viewexpense.html",context)

@login_required
def edit_expense(request,id):
    expens=Expense.objects.get(id=id)
    form=ExpensCreateForm(instance=expens)
    context={}
    context['form']=form
    if request.method=="POST":
        form=ExpensCreateForm(request.POST,instance=expens)
        if form.is_valid():
            form.save()
            return redirect("viewexpens")
        else:
            form=ExpensCreateForm(request.POST,instance=expens)
            context['form']=form
            return render(request,'budget/editexpens.html',context)
    return render(request,'budget/editexpens.html',context)

@login_required
def delete_expense(request,id):
    expens=Expense.objects.get(id=id)
    expens.delete()
    return redirect("viewexpens")
@login_required
def review_expense(request):
    form=ReviewExpenseForm()
    context={}
    context["form"]=form
    if request.method=="POST":
        form=ReviewExpenseForm(request.POST)
        if form.is_valid():
            frm_date=form.cleaned_data.get("from_date")
            to_date=form.cleaned_data.get("to_date")
            total=Expense.objects.filter(date__gte=frm_date,date__lte=to_date,user=request.user).aggregate(Sum("amount"))
            total=total["amount__sum"]
            context["total"]=total
            return render(request, "budget/review_expens.html", context)

    return render(request,"budget/review_expens.html",context)

