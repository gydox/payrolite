from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from employee.models import Employee, FullTimeEmployee, PartTimeEmployee
from .models import Payroll, PayrollItem, IncomeItem, Earnings, Deductions, EarningAllocation, DeductionAllocation, EarningAllocationArchive, DeductionAllocationArchive
from main.models import Company
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import PayrollForm
from django.urls import reverse


@login_required
def payroll(request):
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            payroll_instance = form.save()
            messages.success(request, "Payroll Created")
            return redirect(reverse('payroll:payroll_view', kwargs={'payroll_id': payroll_instance.id}))
        else:
            messages.error(request, form.errors)
    else:
        form = PayrollForm()

    payrolls = Payroll.objects.all().order_by('-year', '-month')
    return render(request=request,
                  template_name="payroll/payroll.html",
                  context={
                    'payrolls': payrolls,
                    'form': form,
                  })

@login_required
def payroll_view(request, payroll_id):
    payroll = get_object_or_404(Payroll, pk=payroll_id)
    payroll_items = payroll.payroll_information.all()

    if request.method == 'POST':
        payroll.processed = True
        payroll.save()
        messages.success(request, 'Payroll processed successfully.')

    return render(request=request,
                  template_name="payroll/payroll_view.html",
                  context={
                    'payroll': payroll,
                    'payroll_items': payroll_items,
                  })

@login_required
def history(request):
    payrolls = Payroll.objects.all()

    return render(request=request,
                  template_name="payroll/history.html",
                  context={
                    'payrolls': payrolls,
                  })

@login_required
def payslip(request, payroll_item_id):
    payroll_item = get_object_or_404(PayrollItem, pk=payroll_item_id)
    company = Company.objects.first()

    return render(request=request,
                  template_name="payroll/payslip.html",
                  context={
                    'payroll_item': payroll_item,
                    'company': company,
                  })

@receiver(post_save, sender=Payroll)
def create_payroll_items(sender, instance, created, **kwargs):
    """
    Signal receiver function to create PayrollItem instances for active employees
    when a Payroll is created.
    """
    print("fucntion triggered")

    if created:
        print("created")
        active_employees = Employee.objects.filter(active=True)
        print(active_employees)
        for employee in active_employees:
            try:
                employee_obj = FullTimeEmployee.objects.get(employee_id=employee.employee_id)
                employee_type = 'full_time'
            except FullTimeEmployee.DoesNotExist:
                try:
                    employee_obj = PartTimeEmployee.objects.get(employee_id=employee.employee_id)
                    employee_type = 'part_time'
                except PartTimeEmployee.DoesNotExist:
                    raise Exception("Employee not found")
            amount = 0.0
            if employee_type == 'full_time':
                amount = employee_obj.monthly_salary
            elif employee_type == 'part_time':
                amount = employee_obj.hourly_rate
            else:
                pass
            
            if isinstance(employee, FullTimeEmployee):
                print("is full time")
                amount = employee.monthly_salary
            PayrollItem.objects.create(payroll=instance, employee=employee, amount=amount)
    else:
        print("not created")