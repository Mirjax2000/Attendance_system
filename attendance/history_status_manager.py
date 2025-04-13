from datetime import date, datetime
from typing import Union

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.manager import BaseManager
from rich.console import Console

from app_main.models import (
    Employee,
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

    def get_worked_hours_on_day(self, day: Union[str, date]) -> str:
        """Jak dlouho pracoval v určený den"""
        try:
            if isinstance(day, str):
                day = datetime.strptime(day, "%Y-%m-%d").date()

            employee = Employee.objects.get(slug=self.employee_slug)

            history = EmployeeStatusHistory.objects.filter(
                employee=employee, timestamp__date=day
            ).order_by("timestamp")

            return self.utility.result_by_hours(
                history=history, status="working"
            )

        except Employee.DoesNotExist:
            return "00:00"

    def get_worked_hours_in_range(
        self, start_date: Union[str, date], end_date: Union[str, date]
    ) -> str:
        """jak dlouho pracoval v urcitem obdoby"""
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            employee: Employee = Employee.objects.get(slug=self.employee_slug)

            history: BaseManager[EmployeeStatusHistory] = (
                EmployeeStatusHistory.objects.filter(
                    employee=employee,
                    timestamp__date__gte=start_date,
                    timestamp__date__lte=end_date,
                ).order_by("timestamp")
            )

            return self.utility.result_by_hours(history, "working")

        except ObjectDoesNotExist:
            return "00:00"

    def get_time_in_status_and_range(
        self,
        status_name: str,
        start_date: Union[str, date],
        end_date: Union[str, date],
    ) -> str:
        """jak dlouho byl ve statusu"""
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            employee: Employee = Employee.objects.get(slug=self.employee_slug)

            history: BaseManager[EmployeeStatusHistory] = (
                EmployeeStatusHistory.objects.filter(
                    employee=employee,
                    new_status__name=status_name,
                    timestamp__date__gte=start_date,
                    timestamp__date__lte=end_date,
                ).order_by("timestamp")
            )

            return self.utility.result_by_hours(history, status_name)

        except ObjectDoesNotExist:
            return "00:00"


class Utility:
    """pomocne metody"""

    @staticmethod
    def result_by_hours(
        history: BaseManager[EmployeeStatusHistory], status: str
    ) -> str:
        """vysledek preveden na hodiny"""
        time_spent_minutes: int = 0
        start_time = None

        for record in history:
            if record.new_status.name == status:
                start_time = record.timestamp  # Uložíme začátek práce

            elif (
                record.previous_status
                and record.previous_status.name == status
            ):
                if start_time:
                    total_seconds: int = (
                        record.timestamp - start_time
                    ).seconds
                    time_spent_minutes += total_seconds // 60
                    start_time = None  # Resetujeme začátek

        # Převedení na HH:MM formát
        hours = time_spent_minutes // 60
        minutes = time_spent_minutes % 60
        return f"{hours:02}:{minutes:02}"


if __name__ == "__main__":
    ...
