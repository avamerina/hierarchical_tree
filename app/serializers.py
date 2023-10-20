from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['supervisor']


class EmployeeSupervisorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'supervisor']

    def update(self, instance, validated_data):
        new_supervisor = validated_data.get('supervisor')
        if instance.position != 'Head' and new_supervisor.position != "Base employee": #temporary solution, adding supervisor to a head employee leads to a RecursionError
            instance.supervisor = new_supervisor
            instance.save()
        return instance


class EmployeeRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'position']
