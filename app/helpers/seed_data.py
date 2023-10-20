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

    supervisor = None
    employees_to_update = []

    for emp in employees:
        if emp.position == roles['Base employee']:
            supervisor = random.choice(employees.filter(position=roles['Manager']))
        elif emp.position == roles['Manager']:
            supervisor = random.choice(employees.filter(position=roles['Senior manager']))
        elif emp.position == roles['Senior manager']:
            supervisor = random.choice(employees.filter(position=roles['Executive']))
        elif emp.position == roles['Executive']:
            supervisor = random.choice(employees.filter(position=roles['Head']))

        emp.supervisor = supervisor
        employees_to_update.append(emp)

    Employee.objects.bulk_update(employees_to_update, ['supervisor'])
