from django.contrib import admin

from app_main.models import (
    Department,
    Employee,
    EmployeeStatus,
    EmployeeStatusHistory,
    FaceVector,
)


class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ["name", "surname", "slug"]
    list_display = ["slug", "employee_status", "department"]


class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class EmployeeStatusAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class EmployeeStatusHistoryAdmin(admin.ModelAdmin):
    search_fields = ["timestamp"]
    list_display = ["previous_status", "new_status", "timestamp"]


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(FaceVector)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(EmployeeStatus, EmployeeStatusAdmin)
admin.site.register(EmployeeStatusHistory, EmployeeStatusHistoryAdmin)
