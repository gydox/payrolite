from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from django.urls import reverse_lazy


app_name = "payroll"

urlpatterns = [
    path('', views.payroll, name='payroll'),
    path('view/<int:payroll_id>', views.payroll_view, name='payroll_view'),
    path('payslip/<int:payroll_item_id>', views.payslip, name='payslip'),
    path('history', views.history, name='history'),
]