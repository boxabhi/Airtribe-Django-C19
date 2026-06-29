from rest_framework import serializers
from home.models import Department, Employee, Skills



class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','name','tag','created_at']


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ['id', 'name', 'created_at']


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['skills','id','created_at','updated_at']
        # fields = '__all__'
        # fields = ['name', 'email', 'age', 'phone_number', 'address', 'department', 'salary', 'city', 'is_active', 'created_at']

