import random
from django.conf.locale import ta
from django.http import HttpResponse
from django.shortcuts import render,redirect
from home.models import Department, Employee, Person, Skills, TaskManager
from faker import Faker
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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

def index(request):
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