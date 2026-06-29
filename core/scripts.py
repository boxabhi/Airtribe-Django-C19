import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()
try:
    import django
    django.setup()
except ImportError:
    print("[warn] Django not found or not configured. DB-backed training is disabled.")


from home.models import *

from django.db.models import Avg, Count, Max, Min, Sum,Q

one  = Department.objects.annotate(
    employee_count=Count('employees'))

two = Department.objects.annotate(
    total_salary=Sum('employees__salary'))

three = Department.objects.annotate(
    employee_count=Count('employees'),
    highest_salary=Max('employees__salary'),
    lowest_salary=Min('employees__salary'),
    average_salary=Avg('employees__salary'))

four = Department.objects.annotate(
    employee_count=Count('employees'),
    active_employee_count = Count('employees', filter=Q(employees__is_active=True)))


five = Department.objects.filter(employees__salary__gt=50000).annotate(highest_salary=Max('employees__salary'))

six = Department.objects.annotate(
    chennai_count = Count('employees', filter=Q(employees__city='Chennai')),
    bangalore_count = Count('employees', filter=Q(employees__city='Bangalore'))
)


seven = Department.objects.annotate(
    emp_30 = Count('employees', filter=Q(employees__age__gt=30)),
    emp_25 = Count('employees', filter=Q(employees__age__lt=25),),
    emp_active_30 = Count('employees', filter=Q(employees__age__gt=30, employees__is_active=True))
)

departments = Department.objects.annotate(
    employee_count=Avg('employees__salary'))