import random
from django_seed import Seed
from app.models import Employee


def process():
    seeder = Seed.seeder()
    roles = tuple(role[1] for role in Employee.EMPLOYEE_TYPES[:-1])

    seeder.add_entity(Employee, 50000, {
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
    head.position = roles['Head']
    head.save()

    for emp in employees:
        if emp.position == roles['Base employee']:
            emp.supervisor = random.choice(employees.filter(position=roles['Manager']))
        elif emp.position == roles['Manager']:
            emp.supervisor = random.choice(employees.filter(position=roles['Senior manager']))
        elif emp.position == roles['Senior manager']:
            emp.supervisor = random.choice(employees.filter(position=roles['Executive']))
        elif emp.position == roles['Executive']:
            emp.supervisor = random.choice(employees.filter(position=roles['Head']))

        emp.save()


