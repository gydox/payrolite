# Generated by Django 4.2.3 on 2024-03-12 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DeductionAllocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='DeductionAllocationArchive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='EarningAllocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='EarningAllocationArchive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='IncomeItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('epf', models.BooleanField(default=False)),
                ('socso', models.BooleanField(default=False)),
                ('eis', models.BooleanField(default=False)),
                ('irbm', models.BooleanField(default=False)),
                ('hrdcorp', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(choices=[(2023, '2023'), (2024, '2024'), (2025, '2025'), (2026, '2026')])),
                ('month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('creation_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Deductions',
            fields=[
                ('incomeitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payroll.incomeitem')),
                ('name', models.CharField(max_length=100)),
            ],
            bases=('payroll.incomeitem',),
        ),
        migrations.CreateModel(
            name='Earnings',
            fields=[
                ('incomeitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payroll.incomeitem')),
                ('name', models.CharField(max_length=100)),
            ],
            bases=('payroll.incomeitem',),
        ),
        migrations.CreateModel(
            name='PayrollItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('payroll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salary_information', to='payroll.payroll')),
            ],
        ),
        migrations.AddConstraint(
            model_name='payroll',
            constraint=models.UniqueConstraint(fields=('year', 'month'), name='unique_payslip_per_month_year'),
        ),
        migrations.AddField(
            model_name='earningallocationarchive',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='earningallocationarchive',
            name='payroll_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='earning_allocations_archive', to='payroll.payrollitem'),
        ),
        migrations.AddField(
            model_name='earningallocation',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='deductionallocationarchive',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='deductionallocationarchive',
            name='payroll_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deduction_allocations_archive', to='payroll.payrollitem'),
        ),
        migrations.AddField(
            model_name='deductionallocation',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='earningallocation',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.earnings'),
        ),
        migrations.AddField(
            model_name='deductionallocation',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payroll.deductions'),
        ),
    ]