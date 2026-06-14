from django.conf.locale import ta
from django.http import HttpResponse
from django.shortcuts import render
from home.models import TaskManager

# Create your views here.


# 1000

# Select * from TaskManager;

def index(request):
    tasks = TaskManager.objects.all()
    print(tasks.query)
    for task in tasks:
        print(f'Id : {task.id} | Task Name: {task.task_name}, Completed: {task.is_completed}')
    return render(request, 'index.html', context={'tasks': tasks})

def contact(request):
    return render(request, 'contact.html')

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

def update_task(request):
    task_id = 1
    task = TaskManager.objects.get(id=task_id)
    task.delete()
    # task.is_completed = True
    # task.task_name = "Write 5 Blog post on Django"
    # task.save()
    return HttpResponse(f'Task with id {task_id} has been updated successfully!')