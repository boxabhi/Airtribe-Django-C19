from django.contrib import admin

# Register your models here.
from .models import ImportJOB, Person

class ImportJOBAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'status', 'error_message', 'uid', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('file', 'error_message', 'uid')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'address', 'city', 'state', 'pincode', 'company', 'job_title', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'company', 'job_title')


admin.site.register(ImportJOB, ImportJOBAdmin)
admin.site.register(Person, PersonAdmin)
