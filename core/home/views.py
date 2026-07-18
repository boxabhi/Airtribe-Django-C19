import random
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from .serializers import CreateEmployeeSerializer, DepartmentSerializer,EmployeeSerializer, LoginSerializer, ResgiterSerializer, SkillsSerializer
from home.models import Department, Employee, Person, Skills, TaskManager
from faker import Faker
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


# 1000

# Select * from TaskManager;



def employee_list(request):
    departments = Department.objects.all().prefetch_related('employees', 'employees__skills')
    # for department in departments:
    #     employees = department.employees.all()
    #     print(f"Department: {department.name}")
    #raise Exception("This is a test exception for debugging purposes.")
    return render(request, 'employee_list.html', {'departments': departments})

import time
def index(request):
    # time.sleep(10)
    tasks = TaskManager.objects.all()
    print(tasks.query)
    for task in tasks:
        print(f'Id : {task.id} | Task Name: {task.task_name}, Completed: {task.is_completed}')
    return render(request, 'index.html', context={'tasks': tasks})

def contact(request):
    return render(request, 'contact.html')



def todo(request):
    context = {
        'tasks': TaskManager.objects.all() 
    }
    return render(request, 'todo_app.html', context=context)


def create_todo(request):
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task= TaskManager(task_name=task_name) 
        task.save()
    return redirect('todo')

def delete_task(request, task_id):
    task = TaskManager.objects.get(id=task_id)
    task.delete()
    return redirect('todo')



def update_task(request, task_id):
    task = TaskManager.objects.get(id=task_id)
    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task.task_name = task_name
        task.save()
    return redirect('todo')

def about(request):
    return render(request, 'about.html')

def insert_task(request):
    task_name = "Write a blog post about Django"
    is_completed = False
    task = TaskManager(task_name=task_name, is_completed=is_completed)
    task.save()
    return HttpResponse(f'Task "{task_name}" has been added successfully!')

# Select * from TaskManager where id = 2;
# Update TaskManager set task_name = "Learn Django ORM" where id = 2;


def execute_query(request):
    # Execute a raw SQL query to retrieve all tasks
    tasks = TaskManager.objects.raw('SELECT * FROM home_taskmanager')
    
    # Print the retrieved tasks
    for task in tasks:
        print(f'Id: {task.id}, Task Name: {task.task_name}, Completed: {task.is_completed}')
    
    return HttpResponse('Query executed successfully!')

def seed_fake_data(request):
    fake = Faker()
    skills = ['Python', 'Django', 'JavaScript', 'React', 'SQL', 'HTML', 'CSS']
    for skill in skills:
        Skills.objects.get_or_create(name=skill)

    skills_objects = list(Skills.objects.all())
    for employee in Employee.objects.all():
        employee.skills.set(random.sample(skills_objects, k=random.randint(1, 5)))
        employee.save()

    return HttpResponse('Fake data seeded successfully!')




def registration(request):
   
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user_exists = User.objects.filter(Q(username=username) | Q(email=email)).exists()

        if user_exists:
            messages.warning(request, "User with this username or email already exists.")
            return redirect('registration')
    
        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password) 
        user.save()

        print(f"Received registration data: username={username}, email={email}, first_name={first_name}, last_name={last_name}")
        messages.success(request, f'User "{username}" has been registered successfully!')
        return redirect('registration')
    return render(request, 'registration.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).exists()
        if not user:
            messages.warning(request, "We are not able to find your account.")
            return redirect('login')

        credentials = authenticate(username=username, password=password)
        if credentials is None:
            messages.warning(request, "Your password is incorrect. Please try again.")
            return redirect('login')
        login(request, credentials)
        return redirect('dashboard')


       
    return render(request, 'login.html')


@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST','PUT', 'DELETE'])
def example_api(request):
    if request.method == 'GET':
        payload = {
            "method" : "GET",
            "message" : "This is a GET API response",
            "status" : 200,
            "bool" : True,
            "fruits" : ["apple", "banana", "cherry"],
        }
        return Response(payload)

    if request.method == 'POST':
        data = request.data
        payload = {
            "method" : "POST",
            "message" : "This is a POST API response",
            "status" : 200,
            "bool" : True,
            "payload" : data
        }
        return Response(payload)

    if request.method == 'PUT':
        data = request.data
        payload = {
            "method" : "PUT",
            "message" : "This is a PUT API response",
            "status" : 200,
            "bool" : True,
            "payload" : data
        }
        return Response(payload)

    return Response({"message": "This is a default API response"})



from rest_framework import status

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def department_api(request):
    if request.method == 'GET':
        department = Department.objects.all()
        serializer = DepartmentSerializer(department, many=True)
        return Response({'departments': serializer.data}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        data = request.data
        serializer = DepartmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Department created successfully", "payload": serializer.data})
        return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)


    if request.method == 'PUT':
        data = request.data
        if data.get('id') is None:
            return Response({"message": "Department ID is required for update"}, status=400)

        department_obj = Department.objects.filter(id=data.get('id')).first()
        if not department_obj:
            return Response({"message": "Department not found"}, status=404)

        serializer = DepartmentSerializer(department_obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Department updated successfully", "payload": serializer.data},status=200)

        return Response({"message": "Department not updated", "payload": serializer.errors}, status=501)

    if request.method == 'PATCH':
        data = request.data
        if data.get('id') is None:
            return Response({"message": "Department ID is required for update"}, status=400)

        department_obj = Department.objects.filter(id=data.get('id')).first()
        if not department_obj:
            return Response({"message": "Department not found"}, status=404)

        serializer = DepartmentSerializer(department_obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Department updated successfully", "payload": serializer.data})

        return Response({"message": "Department not updated", "payload": serializer.errors}, status=501)

    if request.method == 'DELETE':
        data = request.data
        if data.get('id') is None:
            return Response({"message": "Department ID is required for deletion"}, status=400)

        department_obj = Department.objects.filter(id=data.get('id')).first()
        if not department_obj:
            return Response({"message": "Department not found"}, status=404)

        department_obj.delete()
        return Response({"message": "Department deleted successfully"})

    return Response({"message": "Invalid Method"})


@api_view(['POST'])
def skills_post_api(request):
    if request.method == 'POST':
        data = request.data
        serializer = SkillsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Skill created successfully", "payload": serializer.data})
        return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)


@api_view(['DELETE'])
def skills_delete_api(request):
    if request.method == 'DELETE':
        data = request.data
        if data.get('id') is None:
            return Response({"message": "Skill ID is required for deletion"}, status=400)
        skill_obj = Skills.objects.filter(id=data.get('id')).first()
        if not skill_obj:
            return Response({"message": "Skill not found"}, status=404)
        skill_obj.delete()
        return Response({"message": "Skill deleted successfully"})

    return Response({"message": "Invalid Method"})

   



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_api(request):
    print("**********")
    print(request.user, request.user.id, request.user.username)
    print("**********")
    employees = Employee.objects.filter(user = request.user).order_by('-id')
    serializer = EmployeeSerializer(employees, many=True)
    return Response({'employees': serializer.data})

@api_view(['POST'])
def create_employee_api(request):
    data = request.data
    serializer = CreateEmployeeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        
        return Response({"message": "Employee created successfully", "payload": serializer.data})
    return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)


@api_view(['POST'])
def register_api(request):
    data = request.data
    serializer = ResgiterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully", "payload": serializer.data})
    return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)


@api_view(['POST'])
def login_api(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            #token, _ = Token.objects.get_or_create(user=user)
            jwt_token = RefreshToken.for_user(user)
            return Response({"message": "Login successful", "token" : {
                'refresh': str(jwt_token),
                'access': str(jwt_token.access_token),
            }})
        else:
            return Response({"message": "Wrong password"}, status=401)
    return Response({"message": "Invalid data", "errors": serializer.errors}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    request.user.auth_token.delete()
    return Response({"message": "Logout successful"})
