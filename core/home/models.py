from django.db import models

# Create your models here.



class TaskManager(models.Model):
    task_name = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskHistory(models.Model):
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

