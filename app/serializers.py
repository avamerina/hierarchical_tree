from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeSupervisorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['supervisor']

    def update(self, instance, validated_data):
        instance.supervisor = validated_data.get('supervisor')
        instance.save()
        return instance
