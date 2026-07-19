import os

from celery import Celery
from home.pdf_generators import generate_pdf_with_pyhtml2pdf

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

@app.task(bind=True, ignore_result=True)
def send_email_task(self, email, username):
    import time
    time.sleep(10)
    print(f"Sending email to {email} for user {username}")
    return True


@app.task(bind=True, ignore_result=True)
def data_to_pdf_convertor(self, data):
    generate_pdf_with_pyhtml2pdf(data)


@app.task(bind=True, ignore_result=True)
def company_to_pdf_convertor(self):
    from home.models import Company, Person
    people = Person.objects.all()
    data = []
    for person in people:
        data.append({
            "id" : person.id,
            "name": person.name,
            "age": person.age,
            "email": person.email,
            "address": person.address,
        })
    generate_pdf_with_pyhtml2pdf(data)
