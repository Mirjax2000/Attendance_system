from django.core.exceptions import ObjectDoesNotExist
from django.db.models import BaseManager

"""OOP history status manager"""

from app_main.models import (
    Department,
    Employee,
    EmployeeStatus,
    EmployeeStatusHistory,
)


class HistoryStatusManager:
    """History status manager"""

    def __init__(self, employee_slug: str) -> None:
        self.employee_slug: str = employee_slug
        self.utility = Utility()

    def __str__(self) -> str:
        return f"HistoryStatusManager for employee: {self.employee_slug}"

    def __repr__(self) -> str:
        return f"HistoryStatusManager(employee_slug='{self.employee_slug}')"

    def get_worked_hours_on_day(self, day) -> int:
        """jak dlouho pracoval v urcity den"""
        try:
            employee: Employee = Employee.objects.get(slug=self.employee_slug)

            history: BaseManager[EmployeeStatusHistory] = (
                EmployeeStatusHistory.objects.filter(
                    employee=employee, timestamp__date=day
                )
            )
            return self.utility.result_by_hours(history)

        except ObjectDoesNotExist:
            return 0

    def get_worked_hours_in_week(self, start_date, end_date) -> int:
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

    def get_time_in_status(self, status_name, start_date, end_date) -> int:
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
