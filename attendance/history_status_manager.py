"""OOP history status manager"""

from app_main.models import (
    Department,
    Employee,
    EmployeeStatus,
    EmployeeStatusHistory,
)


class HistoryStatusManager:
    """History status manager"""

    def __init__(self, employee_slug: str):
        self.employee_slug = employee_slug

    def __str__(self) -> str:
        return f"HistoryStatusManager for employee: {self.employee_slug}"

    def __repr__(self) -> str:
        return f"HistoryStatusManager(employee_slug='{self.employee_slug}')"

    def get_worked_hours_on_day(self, day) -> int:
        """jak dlouho pracoval v urcity den"""
        try:
            employee = Employee.objects.get(slug=self.employee_slug)

            history = EmployeeStatusHistory.objects.filter(
                employee=employee, timestamp__date=day
            )

            worked_time: int = 0

            for record in history:
                # Pokud byl zaměstnanec ve stavu "working"
                if record.new_status.name == "working":
                    # Získáme předchozí status (může být nemocenská, volno apod.)
                    previous_record = history.filter(
                        timestamp__lt=record.timestamp
                    ).last()
                    if previous_record:
                        # Vypočítat čas mezi předchozím záznamem a tímto
                        worked_time += (
                            record.timestamp - previous_record.timestamp
                        ).seconds // 3600  # V hodinách

            return worked_time

        except Employee.DoesNotExist:
            return 0

    def get_worked_hours_in_week(self, start_date, end_date) -> int:
        """jak dlouho pracoval v urcitem obdoby"""
        try:
            employee = Employee.objects.get(slug=self.employee_slug)

            history = EmployeeStatusHistory.objects.filter(
                employee=employee,
                timestamp__gte=start_date,
                timestamp__lte=end_date,
            )

            worked_time = 0

            for record in history:
                if record.new_status.name == "working":
                    previous_record = history.filter(
                        timestamp__lt=record.timestamp
                    ).last()
                    if previous_record:
                        worked_time += (
                            record.timestamp - previous_record.timestamp
                        ).seconds // 3600  # V hodinách

            return worked_time

        except Employee.DoesNotExist:
            return 0

    def get_time_in_status(self, status_name, start_date, end_date) -> int:
        """jak dlouho byl ve statusu"""
        try:
            employee = Employee.objects.get(slug=self.employee_slug)

            # Získání historie pro daný status a dané časové období
            history = EmployeeStatusHistory.objects.filter(
                employee=employee,
                new_status__name=status_name,
                timestamp__gte=start_date,
                timestamp__lte=end_date,
            )

            time_spent = 0


    class Utility:

        @staticmethod
        def result_by_hours(history)->int:
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

        except Employee.DoesNotExist:
            return 0


if __name__ == "__main__":
    pass
