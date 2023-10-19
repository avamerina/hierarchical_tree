from django.urls import path
from rest_framework import routers

from .views import index, EmployeeListView, EmployeeViewSet

urlpatterns = [
    path('', index, name='index'),
    path('list/', EmployeeListView.as_view(), name='list')
]

router = routers.SimpleRouter()
router.register('employees', EmployeeViewSet, basename='employees')

urlpatterns += router.urls
