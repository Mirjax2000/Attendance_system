"""Napln FK tabulky one to many, Department, EmployeeStatus"""

from rich.console import Console

from app_main.models import Department, EmployeeStatus

cons: Console = Console()


class DefaultFillTables:
    """defaultni zaplneni tabulek"""

    def __init__(self):
        self.working_statuses = [
            EmployeeStatus(name="working"),
            EmployeeStatus(name="sick_leave"),
            EmployeeStatus(name="vacation"),
            EmployeeStatus(name="business_trip"),
            EmployeeStatus(name="free"),
        ]

        self.departments = [Department(name="nezarazeno")]

    def default_department(self):
        """Zaplnění tabulky Department, pokud je prázdná."""
        if not Department.objects.exists():
            Department.objects.bulk_create(self.departments)
            cons.log("Tabulka Department byla naplněna.")

    def default_employee_status(self):
        """Zaplnění tabulky EmployeeStatus, pokud je prázdná."""

        if not EmployeeStatus.objects.exists():
            EmployeeStatus.objects.bulk_create(self.working_statuses)
            cons.log("Tabulka EmployeeStatus byla naplněna.")
