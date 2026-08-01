import os

from celery import Celery
from home.pdf_generators import generate_pdf_with_pyhtml2pdf
import pandas as pd
import time

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



@app.task(bind=True, ignore_result=True)
def import_person_task(self, job_id):
    from jobs.models import ImportJOB, Person
    import_job = ImportJOB.objects.get(uid=job_id)
    file_path = import_job.file.path
    df = pd.read_excel(file_path)
    total_records = len(df)
    import_job.total_records = total_records
    import_job.save()
    for index, row in df.iterrows():
        time.sleep(3)  
        person = Person(
            job = import_job,
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            phone_number=row['phone_number'],
            date_of_birth=row['date_of_birth'],
            address=row['address'],
            city=row['city'],
            state=row['state'],
            pincode=row['pincode'],
            company=row['company'],
            job_title=row['job_title']
        )
        person.save()
        import_job.inserted_records = Person.objects.filter(job=import_job).count()
        import_job.save()
        



