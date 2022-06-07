from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Avg, Max, Min, Sum
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.views.generic import View
from django.http import JsonResponse
from django.forms.models import model_to_dict
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from .filters import *


def home(request):
    return render(request,"main/sidenavbar.html")

def analise(request):
    return render(request, "main/analise.html")

def register_page(request):
    if request.user.is_authenticated:
        return redirect('budget_view')
    else:
        form = create_user_form()
        if request.method == 'POST':
            form = create_user_form(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account created for ' + user)
                return redirect('login')
        context = {'form': form}
        return render(request,'main/register.html',context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('budget_view')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request,user)
                return redirect('budget_view')
            else:
                messages.info(request,'Username or Password incorrect')
        context = {}
        return render(request,'main/login.html',context)

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def analise(request):
    category = Expenses_category.objects.all()
    context = {'category': category}
    return render(request, "main/analise.html")

@login_required(login_url='login')
def analise_earnings(request):
    category = Earnings_category.objects.all()
    context = {'category': category}
    return render(request, "main/analise_earnings.html")

@login_required(login_url='login')
def budget_view(request):
    current_user = request.user.id
    last_month = datetime.now() - timedelta(days=30)
    now = datetime.now()
    expenses = Expenses.objects.filter(date__range=[last_month,now]).filter(user_custom_id=current_user)
    earnings = Earnings.objects.filter(date__range=[last_month,now]).filter(user_custom_id=current_user)
    total_amount_expenses = 0
    total_amount_earnings = 0


    for expense in expenses:
        total_amount_expenses += expense.amount_expenses

    for earning in earnings:
        total_amount_earnings += earning.amount_earnings

    bilance = total_amount_earnings - total_amount_expenses

    context = {'expenses': expenses,'earnings': earnings,
               'total_amount_expenses': total_amount_expenses,
               'total_amount_earnings': total_amount_earnings,
               'bilance': bilance, 'last_month': last_month,'now': now,'filter':filter}
    return render(request,"main/budget.html",context)

@login_required(login_url='login')
def create_expense(request):
    expenses = Expenses.objects.all()
    form = crud_form_expenses()
    filter = order_filter(request.GET, queryset=expenses)
    expenses = filter.qs
    if request.method == 'POST':
        form = crud_form_expenses(request.POST)
        form.instance.user_custom = User.objects.get(pk=request.user.id)
        if form.is_valid():
            form.save()
            return redirect('budget_view')
    context = {'form': form,'filter':filter,'expenses': expenses}
    return render(request,'main/expense.html',context)

@login_required(login_url='login')
def create_earning(request):
    form = crud_form_earnings()
    earnings = Earnings.objects.all()
    filter = order_filter_earnings(request.GET, queryset=earnings)
    earnings = filter.qs
    if request.method == 'POST':
        form = crud_form_earnings(request.POST)
        form.instance.user_custom = User.objects.get(pk=request.user.id)
        if form.is_valid():
            form.save()
            return redirect('budget_view')
    context = {'form': form,'filter':filter,'earnings':earnings}
    return render(request,'main/earning.html',context)


@login_required(login_url='login')
def create_expense_category(request):
    form = crud_form_expense_category()
    if request.method == 'POST':
        form = crud_form_expense_category(request.POST)
        form.instance.user_custom = User.objects.get(pk=request.user.id)
        if form.is_valid():
            form.save()
            return redirect('budget_view')
    context = {'form': form}
    return render(request, 'main/expense_category.html', context)


@login_required(login_url='login')
def create_earning_category(request):
    form = crud_form_earning_category()
    if request.method == 'POST':
        form = crud_form_earning_category(request.POST)
        form.instance.user_custom = User.objects.get(pk=request.user.id)
        if form.is_valid():
            form.save()
            return redirect('budget_view')
    context = {'form': form}
    return render(request, 'main/earning_category.html', context)

@login_required(login_url='login')
def update_expense(request, pk):
    expense = Expenses.objects.get(id=pk)
    form = crud_form_expenses(instance=expense)

    if request.method == 'POST':
        form = crud_form_expenses(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('budget_view')
    context = {'form': form}
    return render(request, 'main/earning.html', context)

@login_required(login_url='login')
def update_earning(request, pk):
    earning = Earnings.objects.get(id=pk)
    form = crud_form_earnings(instance=earning)

    if request.method == 'POST':
        form = crud_form_earnings(request.POST, instance=earning)
        if form.is_valid():
            form.save()
            return redirect('budget_view')
    context = {'form': form}
    return render(request, 'main/earning.html', context)



@login_required(login_url='login')
def delete_expense(request,pk):
    expense = Expenses.objects.get(id=pk)
    if request.method == "POST":
        expense.delete()
        return redirect('budget_view')
    context = {'item': expense}
    return render(request,'main/delete.html',context)

@login_required(login_url='login')
def delete_earning(request,pk):
    earning = Earnings.objects.get(id=pk)
    if request.method == "POST":
        earning.delete()
        return redirect('budget_view')
    context = {'item': earning}
    return render(request,'main/delete_earning.html',context)


def get_data(request):
    current_user = request.user.id
    category_data = []
    expenses_data = []
    category = Expenses_category.objects.all()
    for i in category:
        sum = 0
        expenses = Expenses.objects.filter(user_custom_id=current_user).filter(category=i)
        for expense in expenses:
            sum += expense.amount_expenses
        category_data.append({i.name: sum})
    return JsonResponse(category_data, safe=False)

def get_data_earnings(request):
    current_user = request.user.id
    category_data = []
    earnings_data = []
    category = Earnings_category.objects.all()
    for i in category:
        sum = 0
        earnings = Earnings.objects.filter(user_custom_id=current_user).filter(category=i)
        for earning in earnings:
            sum += earning.amount_earnings
        category_data.append({i.name: sum})
    return JsonResponse(category_data, safe=False)

def pdf(request):
    current_user = request.user.id
    category = Expenses_category.objects.all()
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "sum")
    
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

