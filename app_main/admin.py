from django.contrib import admin

from app_main.models import Department, Employee, FaceVector

admin.site.register(Employee)
admin.site.register(FaceVector)
admin.site.register(Department)
