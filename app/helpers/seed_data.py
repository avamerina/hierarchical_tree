import random
from django_seed import Seed
from app.models import Employee


def process():
    seeder = Seed.seeder()
    roles = tuple(role[1] for role in Employee.EMPLOYEE_TYPES[:-1])

    seeder.add_entity(Employee, 15, {
        'full_name': lambda x: seeder.faker.name(),
        'position': lambda x: random.choice(roles),
        'hire_date': lambda x: seeder.faker.date_time_this_decade(),
        'salary': lambda x: random.randint(30000, 150000),
        'supervisor': None
    })

    seeder.execute()


def create_hierarchy():
    employees = Employee.objects.all()
    roles = dict(Employee.EMPLOYEE_TYPES)

    head = Employee.objects.first()
    head.position = roles['HEAD']
    head.save()

    for emp in employees:
        if emp.position == roles['STD']:
            emp.supervisor = random.choice(employees.filter(position=roles['MNG']))
        elif emp.position == roles['MNG']:
            emp.supervisor = random.choice(employees.filter(position=roles['SNR_MNG']))
        elif emp.position == roles['SNR_MNG']:
            emp.supervisor = random.choice(employees.filter(position=roles['EXC']))
        elif emp.position == roles['EXC']:
            emp.supervisor = random.choice(employees.filter(position=roles['HEAD']))

        emp.save()


