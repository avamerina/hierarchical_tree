from datetime import datetime

from django.utils import timezone
from django.db import models


class Employee(models.Model):
    STANDARD = 'STD'
    MANAGER = 'MNG'
    SENIOR_MANAGER = 'SNR_MNG'
    EXECUTIVE = 'EXC'
    HEAD = 'HEAD'

    EMPLOYEE_TYPES = (
        (STANDARD, 'Base employee'),
        (MANAGER, 'Manager'),
        (SENIOR_MANAGER, 'Senior manager'),
        (EXECUTIVE, 'Executive'),
        (HEAD, 'Head')
    )

    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, null=True, choices=EMPLOYEE_TYPES)
    hire_date = models.DateField(default=datetime.today())
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor = models.ForeignKey('self', null=True, on_delete=models.SET_DEFAULT, default=0, related_name='subordinates')

    def __str__(self):
        return f'{self.position} {self.full_name}'

    def __repr__(self):
        return self.__str__()
    
