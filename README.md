# Hierarchical_tree
  

## How to run

```
* git clone git@github.com:avamerina/hierarchical_tree.git
  
* python manage.py migrate
* python manage.py seedtrees
* python manage.py runserver
  
* to see a tree go to
  localhost:8000/
  
* to see a list of employees full info go to
  localhost:8000/list

note:
  before running seedtrees you may change number of objects to generate (setted up on 50 000) in app/helpers/seed_data.py
  to see a list of employees remove LoginRequiredMixin and set permission_classes=[permissions.AllowAny,] in app/views.py
  
```


## APIs

* registration
```
POST /users/ 
body: {"username": "your_username", "password": "your_password"}
```

* login
```
POST /token/login/
body: {"username": "your_username", "password": "your_password"} 
```

* logout
```
POST /token/logout/
parameters: {"Authorization" : Token your_token}
```

* list ordering
```
GET /employees/?oredering=full_name
parameters: {"Authorization" : Token your_token}
```

* search
```
GET /employees?search=manager
parameters: {"Authorization" : Token your_token}
```
* crud
```
GET/PUT/PATCH/POST/DELETE /employees/
parameters: {"Authorization" : Token your_token}
body:
  {
    "full_name": "full_name",
    "position": "Base employee",
    "hire_date": "2020-05-21",
    "salary": "120341.00",
    "supervisor": null
}
```


  

  

