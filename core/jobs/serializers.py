from rest_framework import serializers
from jobs.models import ImportJOB

class ImportJOBSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportJOB
        fields = '__all__'

       