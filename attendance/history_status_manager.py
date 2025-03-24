"""OOP history status manager"""

from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.manager import BaseManager
from rich.console import Console

from app_main.models import (
    Department,
    Employee,
    EmployeeStatus,
    EmployeeStatusHistory,
)

cons = Console()


class HistoryStatusManager:
    """History status manager"""

    def __init__(self, employee_slug: str) -> None:
        self.employee_slug: str = employee_slug
        self.utility = Utility()

    def __str__(self) -> str:
        return f"HistoryStatusManager for employee: {self.employee_slug}"

    def __repr__(self) -> str:
        return f"HistoryStatusManager(employee_slug='{self.employee_slug}')"

    def get_worked_hours_on_day(self, day) -> str:
        """jak dlouho pracoval v urcity den"""
        try:
            if isinstance(day, str):
                day = datetime.strptime(day, "%Y-%m-%d").date()

            employee: Employee = Employee.objects.get(slug=self.employee_slug)

            history: BaseManager[EmployeeStatusHistory] = (
                EmployeeStatusHistory.objects.filter(
                    employee=employee, timestamp__date=day
                )
            )
            time_spent_minutes: int = 0

            for record in history:
                if record.new_status.name == "working":
                    previous_record = history.filter(
                        timestamp__lt=record.timestamp
                    ).last()
                    if previous_record:
                        total_seconds = (
                            record.timestamp - previous_record.timestamp
                        ).seconds
                        time_spent_minutes += total_seconds // 60

            # Převedení na HH:MM formát
            hours = time_spent_minutes // 60
            minutes = time_spent_minutes % 60
            return f"{hours:02}:{minutes:02}"

        except ObjectDoesNotExist:
            return "00:00"

    def get_worked_hours_in_range(self, start_date, end_date) -> int:
        """jak dlouho pracoval v urcitem obdoby"""
        try:
            employee: Employee = Employee.objects.get(slug=self.employee_slug)

            history: BaseManager[EmployeeStatusHistory] = (
                EmployeeStatusHistory.objects.filter(
                    employee=employee,
                    timestamp__gte=start_date,
                    timestamp__lte=end_date,
                )
            )

            return self.utility.result_by_hours(history)

        except ObjectDoesNotExist:
            return 0

    def get_time_in_status_and_range(
        self, status_name, start_date, end_date
    ) -> int:
        """jak dlouho byl ve statusu"""
        try:
            employee: Employee = Employee.objects.get(slug=self.employee_slug)

            # Získání historie pro daný status a dané časové období
            history: BaseManager[EmployeeStatusHistory] = (
                EmployeeStatusHistory.objects.filter(
                    employee=employee,
                    new_status__name=status_name,
                    timestamp__gte=start_date,
                    timestamp__lte=end_date,
                )
            )

            return self.utility.result_by_hours(history)

        except ObjectDoesNotExist:
            return 0


class Utility:
    """pomocne metody"""

    @staticmethod
    def result_by_hours(history: BaseManager[EmployeeStatusHistory]) -> int:
        """vysledek preveden na hodiny"""
        time_spent = 0
        for record in history:
            if record.new_status.name == "working":
                previous_record = history.filter(
                    timestamp__lt=record.timestamp
                ).last()
                if previous_record:
                    time_spent += (
                        record.timestamp - previous_record.timestamp
                    ).seconds // 3600  # V hodinách

        return time_spent


if __name__ == "__main__":
    ...
