"""API django TEST framework"""

from rest_framework.serializers import ModelSerializer

from app_main.models import Department, Employee, EmployeeStatus


class EmployeeSerializer(ModelSerializer):
    """API serializer"""

    class Meta:
        """Meta class"""

        model = Employee
        fields = ["name", "surname", "slug", "department", "employee_status"]
        labels = {
            "name": "jmeno",
            "surname": "prijmeni",
            "slug": "slug",
            "department": "department",
            "employee_status": "stav",
        }


class DepartmentSerializer(ModelSerializer):
    """API serializer"""

    class Meta:
        """Meta class"""

        model = Department
        fields = "__all__"


class EmployeeStatusSerializer(ModelSerializer):
    """API serializer"""

    class Meta:
        """Meta class"""

        model = EmployeeStatus
        fields = "__all__"
