from django.shortcuts import redirect, render

# Create your views here.
from django.http import request
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from core.celery import import_person_task
from jobs.models import ImportJOB
from .serializers import ImportJOBSerializer





def index_import_job(request):
    if request.method == 'POST':
        file = request.FILES['file']
        import_job = ImportJOB.objects.create(file=file)
        import_person_task.delay(import_job.uid)
        return redirect('real_time_job_data', job_id=import_job.uid)
    return render(request, 'job_index.html', {})


def real_time_job_data(request, job_id):
    context = {"job_id" : job_id}
    return render(request, 'real_time_job_data.html', context=context)
   


class CreateImportJOB(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ImportJOBSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            import_person_task.delay(serializer.data['uid']) 

            return Response({"message": "Import job created", "job_id": serializer.data}, status=201)

        return Response(serializer.errors, status=400)
    