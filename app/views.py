from django.shortcuts import render

from app.models import Employee
from app.helpers.generators import generate_subs_list


def index(request):
    employees = Employee.objects.select_related('supervisor').all()
    hierarchy = [generate_subs_list(employee) for employee in employees]
    context = {'hierarchy': hierarchy}
    return render(request, 'index.html', context)





