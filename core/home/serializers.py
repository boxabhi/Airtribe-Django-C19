from django.db.migrations import serializer
from rest_framework import serializers
from home.models import Department, Employee, Skills,EmployeeLog
import json
from django.contrib.auth.models import User


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','name','tag']


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ['id', 'name', 'created_at']


class EmployeeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLog
        fields = ['employee_email', 'action']


class EmployeeSerializer(serializers.ModelSerializer):
    #salary_before_tax  = serializers.SerializerMethodField()
    department = DepartmentSerializer(write_only=True)
    # log = serializers.SerializerMethodField()
    file = serializers.FileField(write_only=True, required=False)
    url = serializers.JSONField(write_only=True, required=False)
    class Meta:
        model = Employee
        exclude = ['skills','created_at','updated_at']


    


    def calculate_salary_before_tax(self, salary):
        tax_rate = 0.10
        salary_before_tax = float(salary) * (1 - tax_rate)
        return salary_before_tax

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['salary_before_tax'] = self.calculate_salary_before_tax(instance.salary)
        data['domain'] = instance.email.split('@')[-1] if instance.email else None
        return data
    #     print(data)
    #     data['salary_before_tax'] = float(instance.salary) * 0.10 
    #     data['logs']= EmployeeLogSerializer(EmployeeLog.objects.filter(employee_email=instance.email), many=True).data
    #     return data

        # return super().to_representation(instance)

    # def get_salary_before_tax(self, employee):
    #     return float(employee.salary) * 0.10  # Assuming 20% tax

    # def get_log(self, employee):
    #     logs = EmployeeLog.objects.filter(employee_email=employee.email)
    #     return EmployeeLogSerializer(logs, many=True).data


class CreateEmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'age', 'salary', 'city', 'joining_date', 'is_active', 'department', 'skills']

    def to_internal_value(self, data):
        data['name'] = data.get('name', '').lower() 
        data['email'] = data.get('email', '').lower() 
        data['city'] = data.get('city', '').upper()
        return super().to_internal_value(data)



class ResgiterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value


    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)

    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("User not found")
        return value