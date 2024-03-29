from django.shortcuts import render, redirect, get_object_or_404
from authentication.decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, ExpressionWrapper, fields, Avg
from employee.models import FullTimeEmployee, PartTimeEmployee
from datetime import datetime, timedelta
from .models import Company
from .forms import CompanyForm
from django.contrib import messages


@login_required
def dashboard(request):
    total_salary = FullTimeEmployee.objects.filter(active=True).aggregate(total_salary=Sum('monthly_salary'))['total_salary'] or 0
    total_active_full_time_employees = FullTimeEmployee.objects.filter(active=True).count()
    total_active_part_time_employees = PartTimeEmployee.objects.filter(active=True).count()
    active_full_time_employees = FullTimeEmployee.objects.filter(active=True)
    active_part_time_employees = PartTimeEmployee.objects.filter(active=True)
    average_full_time_salary = active_full_time_employees.aggregate(avg_salary=Avg('monthly_salary'))['avg_salary']
    average_full_time_salary_formatted = round(average_full_time_salary, 2) if average_full_time_salary is not None else None


    for employee in active_full_time_employees:
        start_date = employee.start_date
        current_date = datetime.now().date()
        days_of_service = (current_date - start_date).days
        days_of_service = max(days_of_service, 0)
        employee.days_of_service = days_of_service
        employee.probation_completion = days_of_service/60 * 100

    return render(request=request,
                  template_name="main/dashboard.html",
                  context={
                    'total_salary': total_salary,
                    'total_active_full_time_employees': total_active_full_time_employees,
                    'total_active_part_time_employees':total_active_part_time_employees,
                    'active_full_time_employees': active_full_time_employees,
                    'active_part_time_employees': active_part_time_employees,
                    'average_full_time_salary_formatted': average_full_time_salary_formatted,
                  })

@login_required
def settings(request):
    try:
        company = Company.objects.get()
        # If company exists, populate the form with its instance for editing
        form = CompanyForm(request.POST or None, instance=company)
    except Company.DoesNotExist:
        # If no company exists, create a new form for adding company information
        form = CompanyForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Company informatioon successfully updated")
            return redirect('main:settings')  # Redirect to the same view after saving the form
        else:
            messages.error(request, form.errors)


    return render(request=request,
                  template_name="main/settings.html",
                  context={
                    'form':form,
                  })