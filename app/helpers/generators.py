def generate_subs_list(employee):
    subordinates = employee.subordinates.all()
    if subordinates:
        return {'employee': employee, 'subordinates': [generate_subs_list(sub) for sub in subordinates]}
    return {'employee': employee}

