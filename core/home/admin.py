from django.contrib import admin

# Register your models here.

from home.models import Person, Company, Department, Skills, Employee


admin.site.register(Person)
admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Skills)
admin.site.register(Employee)
