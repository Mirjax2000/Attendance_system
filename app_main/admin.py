from django.contrib import admin

from app_main.models import (
    Department,
    Employee,
    EmployeeStatus,
    EmployeeStatusHistory,
    FaceVector,
)

admin.site.register(Employee)
admin.site.register(FaceVector)
admin.site.register(Department)
admin.site.register(EmployeeStatus)
admin.site.register(EmployeeStatusHistory)
