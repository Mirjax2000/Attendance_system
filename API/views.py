# Create your views here.
from rest_framework import generics, mixins

from app_main.models import Department, Employee, EmployeeStatus

from .serializers import (
    DepartmentSerializer,
    EmployeeSerializer,
    EmployeeStatusSerializer,
)


class EmployeesApi(mixins.ListModelMixin, generics.GenericAPIView):
    """employees API"""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, *args, **kwargs):
        """GET method"""
        return self.list(request, *args, **kwargs)


class DepartmentApi(mixins.ListModelMixin, generics.GenericAPIView):
    """Department API"""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get(self, request, *args, **kwargs):
        """GET method"""
        return self.list(request, *args, **kwargs)


class EmployeeStatusApi(mixins.ListModelMixin, generics.GenericAPIView):
    """EmployeeStatus API"""

    queryset = Department.objects.all()
    serializer_class = EmployeeStatusSerializer

    def get(self, request, *args, **kwargs):
        """GET method"""
        return self.list(request, *args, **kwargs)


class EmployeeDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """Employee detail"""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = "slug"

    def get(self, request, *args, **kwargs):
        """get method"""
        return self.retrieve(request, *args, **kwargs)
