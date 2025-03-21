# Create your views here.
from rest_framework import mixins

from app_main.models import Employee

from .serializers import EmployeeSerializer


class Employees(mixins.ListModelMixin):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, *args, **kwargs):
        return self.list(request, *args, **kwargs)
