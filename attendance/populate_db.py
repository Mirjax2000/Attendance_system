"""Napln FK tabulky one to many, Department, EmployeeStatus"""

from rich.console import Console

from app_main.models import Department, EmployeeStatus

from .settings import DEBUG

cons: Console = Console()


class DefaultFillTables:
    """defaultni zaplneni tabulek"""

    def checking_db(self) -> bool:
        """Vrátí True, pokud tabulky obsahují záznamy, jinak False."""
        return Department.objects.exists() or EmployeeStatus.objects.exists()

    def default_department(self):
        """Zaplnění tabulky Department, pokud je prázdná."""
        departments = [Department(name="nezarazeno")]
        if not Department.objects.exists():
            Department.objects.bulk_create(departments)
            if DEBUG:
                cons.log("Tabulka Department byla naplněna.")

    def default_employee_status(self):
        """Zaplnění tabulky EmployeeStatus, pokud je prázdná."""
        working_statuses = [
            EmployeeStatus(name="working"),
            EmployeeStatus(name="sick_leave"),
            EmployeeStatus(name="vacation"),
            EmployeeStatus(name="business_trip"),
            EmployeeStatus(name="free"),
        ]

        if not EmployeeStatus.objects.exists():
            EmployeeStatus.objects.bulk_create(working_statuses)
            if DEBUG:
                cons.log("Tabulka EmployeeStatus byla naplněna.")

    def run_all_default(self):
        """spusteni vsech funkci"""
        if self.checking_db():
            if DEBUG:
                cons.log("Tabulky už obsahují data. Není potřeba nic přidávat.")
            return
        self.default_department()
        self.default_employee_status()
        if DEBUG:
            cons.log("Tabulky byly naplněny.")


fill_tables: DefaultFillTables = DefaultFillTables()

if __name__ == "__main__":
    fill_tables.run_all_default()
