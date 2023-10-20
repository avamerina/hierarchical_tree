import copy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.db.models import Count, Min

from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import Employee
from app.helpers.generators import generate_subs_list
from app.serializers import EmployeeSerializer, EmployeeSupervisorUpdateSerializer, EmployeeRoleUpdateSerializer


def index(request):
    employees = Employee.objects.select_related('supervisor').all()
    hierarchy = [generate_subs_list(employee) for employee in employees]
    context = {'hierarchy': hierarchy}
    return render(request, 'index.html', context)


class EmployeeListView(LoginRequiredMixin, View):
    template_name = 'list.html'
    login_url = 'http://127.0.0.1:8000/token/login/'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'
    search_fields = ['full_name', 'position', 'salary', 'hire_date', ]
    permission_classes = [permissions.IsAuthenticated, ]

    @staticmethod
    def _appoint_new_supervisor(previous_employee_state):
        """
            Appoints new supervisor for employee's subordinates
            when employee changes position in company
        """
        role = previous_employee_state.position
        rest_supervisors = Employee.objects.filter(position=role)
        rest_supervisors_with_subs_quantity = rest_supervisors.annotate(
            subs_quantity=Count('subordinates')
        )
        min_subordinates_quantity = rest_supervisors_with_subs_quantity.aggregate(
            min_quantity=Min('subs_quantity')
        )
        employee_with_min_subordinates = rest_supervisors_with_subs_quantity.filter(
            subs_quantity=min_subordinates_quantity['min_quantity']
        ).first()

        return employee_with_min_subordinates

    @staticmethod
    def _transfer_subs_under_new_supervisor(new_supervisor, subordinates):
        for sub in subordinates:
            serializer = EmployeeSupervisorUpdateSerializer(sub, data={"supervisor": new_supervisor.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()

    @action(methods=['POST'], detail=True)
    def update_position(self, request, *args, **kwargs):
        """
            Updates employee position, moves all it's subordinates under a new supervisor of the same role
        """
        emp = self.get_object()
        previous_employee_state = copy.deepcopy(emp)
        subordinates_to_transfer = copy.deepcopy(list(emp.subordinates.all()))
        prev_sup = copy.copy(emp.supervisor)

        serializer = EmployeeSupervisorUpdateSerializer(emp, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        new_sup = emp.supervisor

        emp_new_role_after_supervisor = {
            "Head": "Executive",
            "Executive": "Senior manager",
            "Senior manager": "Manager",
            "Manager": "Base employee",
            "Base employee": "Base employee"
        }

        if prev_sup and new_sup.position != prev_sup.position:
            serializer = EmployeeRoleUpdateSerializer(
                emp,
                data={'position': emp_new_role_after_supervisor.get(new_sup.position)}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

            new_supervisor = self._appoint_new_supervisor(previous_employee_state)
            self._transfer_subs_under_new_supervisor(new_supervisor, subordinates_to_transfer)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        previous_employee_state = copy.deepcopy(self.get_object())
        subordinates_to_transfer = copy.deepcopy(list(previous_employee_state.subordinates.all()))

        response = super().destroy(request, args, **kwargs)

        if response.status_code == status.HTTP_204_NO_CONTENT and len(subordinates_to_transfer) > 0:
            new_supervisor = self._appoint_new_supervisor(previous_employee_state)
            self._transfer_subs_under_new_supervisor(new_supervisor, subordinates_to_transfer)

        return response



