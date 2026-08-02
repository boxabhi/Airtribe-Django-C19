from django.db import models
import uuid
# Create your models here.
from utility.models import BaseModel
from django.db.models.signals import post_save,pre_save, pre_delete, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync,sync_to_async


class ImportJOB(BaseModel):
    file = models.FileField(upload_to='import_jobs/')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    error_message = models.TextField(blank=True, null=True)
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    total_records = models.IntegerField(default=0)
    inserted_records = models.IntegerField(default=0)

    def __str__(self):
        return f"Import Job {self.id} - {self.status}"



class Person(BaseModel):
    job = models.ForeignKey(ImportJOB, on_delete=models.CASCADE, related_name='persons')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"






@receiver(post_save, sender=Person)
def send_websocket_event(sender, instance, created, **kwargs):
    if created:

        payload = {
            "event": "new_person",
            "person": {
                "id": instance.id,
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "email": instance.email,
                "phone_number": instance.phone_number,
                "date_of_birth": str(instance.date_of_birth),
                "address": instance.address,
                "city": instance.city,
                "state": instance.state,
                "pincode": instance.pincode,
                "company": instance.company,
                "job_title": instance.job_title
            },
            "job_status": {
                "total_records": instance.job.total_records,
                "inserted_records": Person.objects.filter(job=instance.job).count(),
                "status": instance.job.status,
                "inserted_percentage": (instance.job.inserted_records / instance.job.total_records * 100) if instance.job.total_records > 0 else 0
            }
        }

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"job_{instance.job.uid}",
            {
                "type": "send_person_event",
                "message": json.dumps(payload)
            }
        )
        print("CHANNLE INFORMATION SENT")
