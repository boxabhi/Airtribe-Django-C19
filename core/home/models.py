from django.db import models
from django.db.models import Q
from django.db.models.aggregates import Count
from django.contrib.auth.models import User
from utility.models import BaseModel

# Create your models here.





class TaskManager(BaseModel):
    task_name = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)


class TaskHistory(BaseModel):
    action = models.CharField(max_length=255)

# gmail.com rediff.com yahoo.com

class Person(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    age = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"
        db_table = "person"
        ordering = ['name']


    def __str__(self):
        return f"Person - {self.name} | Age : {self.age}"




class Company(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Company - {self.name}"

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


class Department(BaseModel):
    name = models.CharField(max_length=255) # IT , HR , Finance, Marketing
    tag = models.CharField(max_length=10) # IT , HR , Finance, Marketing

    def __str__(self):
        return f"Department - {self.name}"

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Department"
        db_table = "Department"


class Skills(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"Skill - {self.name}"
class Employee(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=10)
    email = models.EmailField(null = True, blank = True)
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='employees')
    skills = models.ManyToManyField(Skills, related_name='employees')

    def __str__(self):
        return f"Employee - {self.name}"


class EmployeeLog(BaseModel):
    employee_email = models.EmailField()
    action = models.CharField(max_length=255)

    def __str__(self):
        return f"EmployeeLog - {self.employee_email} | Action: {self.action}"


