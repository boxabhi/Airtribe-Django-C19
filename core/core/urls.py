"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from home.views import (
    create_todo, dashboard, delete_task, department_api, employee_list, index, contact, about,
    insert_task, login_view, logout_view, seed_fake_data, todo, update_task,registration)
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('', index, name='index'),
    path('', include('django_prometheus.urls')),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('insert_task/', insert_task, name='insert_task'),
    path('create_todo/', create_todo, name='create_todo'),
    path('todo/', todo, name='todo'),
    path('delete-task/<task_id>/', delete_task, name='delete_task'),
    path('update_task/<task_id>/', update_task, name='update_task'),
    path('seed_fake_data/', seed_fake_data, name='seed_fake_data'),
    path('employee_list/', employee_list, name='employee_list'),
    path('registration/', registration, name='registration'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),

    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),

] + debug_toolbar_urls()


