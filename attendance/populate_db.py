"""OOP trida pro kontrolu databaze"""

from typing import Type

from django.core.management import call_command
from django.db import models
from rich.console import Console

from app_main.models import (
    Department,
    Employee,
    EmployeeStatus,
    EmployeeStatusHistory,
    FaceVector,
)

from .settings import DEBUG

cons: Console = Console()


class DatabaseControl:
    """defaultni zaplneni tabulek"""

    def checking_db(self) -> bool:
        """Vrátí True, pokud tabulky obsahují záznamy, jinak False."""
        return Department.objects.exists() or EmployeeStatus.objects.exists()

    def default_department(self) -> None:
        """Zaplnění tabulky Department, pokud je prázdná."""
        departments = [Department(name="nezarazeno")]
        if not Department.objects.exists():
            Department.objects.bulk_create(departments)
            if DEBUG:
                cons.log("Tabulka Department byla naplněna.", style="green")

    def default_employee_status(self) -> None:
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
                cons.log("Tabulka EmployeeStatus byla naplněna.", style="green")

    def run_all_default(self) -> None:
        """spusteni vsech funkci"""
        if self.checking_db():
            if DEBUG:
                cons.log(
                    "Tabulky už obsahují data. Není potřeba nic přidávat.",
                    style="green",
                )
            return
        self.default_department()
        self.default_employee_status()
        if DEBUG:
            cons.log("Tabulky byly naplněny.", style="green")

    def delete_db(self) -> bool:
        """Smaže DB jako truncate a zkontroluje prázdnost tabulek"""
        call_command("flush", "--noinput")

        db_status: list[bool] = []
        db_tables: list[Type[models.Model]] = [
            Employee,
            EmployeeStatus,
            EmployeeStatusHistory,
            Department,
            FaceVector,
        ]

        for db_table in db_tables:
            if not db_table.objects.exists():
                if DEBUG:
                    cons.log(
                        f"Tabulka: {db_table.__name__} je prázdná.",
                        style="green",
                    )
                db_status.append(True)
            else:
                if DEBUG:
                    cons.log(
                        f"Tabulka: {db_table.__name__} není prázdná.",
                        style="red",
                    )
                db_status.append(False)

        if all(db_status):
            if DEBUG:
                cons.log("Všechny tabulky jsou prázdné.", style="green")
            return True

        if DEBUG:
            cons.log("Některé tabulky nejsou prázdné.", style="red")
        return False


# aktivace instance
db_control: DatabaseControl = DatabaseControl()
# nyni je instance vytovrena a je pripraven k importu

if __name__ == "__main__":
    db_control.run_all_default()
