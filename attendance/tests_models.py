"""model tests"""

import json
from datetime import date

import numpy as np
from django.test import TestCase

from app_main.models import (
    Department,
    Employee,
    EmployeeStatus,
    EmployeeStatusHistory,
    FaceVector,
)

from .populate_db import DatabaseControl

seed: int = 42
rng = np.random.default_rng(seed)
vektor = rng.random((128))
vektor_2 = rng.random((128))

face_vektor_list = vektor.tolist()
face_vektor_list_2 = vektor_2.tolist()

expected_vector_1: str = json.dumps({"vector": face_vektor_list})
expected_vector_2: str = json.dumps({"vector": face_vektor_list_2})


class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # one to many tabulky se musi zaplnit
        working_statuses = [
            EmployeeStatus(name="working"),
            EmployeeStatus(name="sick_leave"),
            EmployeeStatus(name="vacation"),
            EmployeeStatus(name="business_trip"),
            EmployeeStatus(name="free"),
        ]

        departments = [
            Department(name="uklid"),
            Department(name="management"),
            Department(name="udrzba"),
            Department(name="testing"),
            Department(name="front-end"),
            Department(name="back-end"),
            Department(name="nezarazeno"),
        ]

        EmployeeStatus.objects.bulk_create(working_statuses)
        Department.objects.bulk_create(departments)

        # Vytvořte zaměstnance pro testovací data
        employee1 = Employee.objects.create(
            name="Jan",
            surname="Novák",
            street_number="Hlavní 123",
            city="Praha",
            postal_code="10000",
            phone_number="+420123456789",
            email="jan.novak@example.com",
            date_of_birth=date(1985, 5, 10),
            is_valid=True,
            pin_code="1234",
        )
        FaceVector.objects.create(
            employee=employee1, face_vector={"vector": face_vektor_list}
        )

        employee2 = Employee.objects.create(
            name="Marie",
            surname="Kovářová",
            street_number="Vedlejší 45",
            city="Brno",
            postal_code="60200",
            phone_number="+420987654321",
            email="marie.kovarova@example.com",
            date_of_birth=date(1992, 8, 20),
            is_valid=False,
            pin_code="5678",
        )
        FaceVector.objects.create(
            employee=employee2, face_vector={"vector": face_vektor_list_2}
        )

    def test_employee_count(self):
        """Test na počet záznamů v tabulce Employee"""
        expected_count = 2
        self.assertEqual(Employee.objects.count(), expected_count)

    def test_employees_status_count(self):
        """Test na počet záznamů v tabulce EmployeeStatus"""
        expected_count = 5
        self.assertEqual(EmployeeStatus.objects.count(), expected_count)

    def test_employees_in_department(self):
        """kolik lidi je departments v nezarazeno"""
        expected_count = 2
        nezarazeno = Department.objects.get(name="nezarazeno")
        count = Employee.objects.filter(department=nezarazeno).count()
        self.assertEqual(count, expected_count)

    def test_employee_creation(
        self,
    ):
        """Z tabulky employee"""
        free_id = EmployeeStatus.objects.get(name="free")
        nezarazeno_id = Department.objects.get(name="nezarazeno")
        # instance jan-novak
        employee_jan = Employee.objects.get(slug="jan-novak")
        self.assertIsNotNone(employee_jan)
        self.assertTrue(employee_jan)
        self.assertIsInstance(employee_jan, Employee)
        self.assertEqual(employee_jan.name, "Jan")
        self.assertEqual(employee_jan.surname, "Novák")
        self.assertEqual(employee_jan.city, "Praha")
        self.assertEqual(employee_jan.postal_code, "10000")
        self.assertEqual(employee_jan.phone_number, "+420123456789")
        self.assertEqual(employee_jan.email, "jan.novak@example.com")
        self.assertEqual(employee_jan.date_of_birth, date(1985, 5, 10))
        self.assertEqual(employee_jan.age(), (39))
        self.assertEqual(employee_jan.check_pin_code("1234"), True)
        self.assertEqual(employee_jan.department, nezarazeno_id)
        self.assertEqual(employee_jan.employee_status, free_id)
        self.assertEqual(employee_jan.is_valid, True)
        # propojeni pres FK na tabulku FaceVector
        self.assertEqual(
            employee_jan.vector.decrypt_vector(),
            expected_vector_1,
        )

    def test_face_vector_creation(self):
        """z tabulky FaceVector"""
        face_vector_jan = FaceVector.objects.get(employee__slug="jan-novak")
        self.assertIsNotNone(face_vector_jan.face_vector_fernet)
        self.assertIsInstance(face_vector_jan.face_vector, list)
        self.assertIsInstance(face_vector_jan.face_vector_fernet, bytes)
        self.assertEqual(face_vector_jan.decrypt_vector(), expected_vector_1)
        self.assertNotEqual(
            face_vector_jan.decrypt_vector(),
            expected_vector_2,
        )
        self.assertFalse(face_vector_jan.face_vector)

    def test_departments_creation(self):
        """z tabulky department"""
        department_uklid = Department.objects.get(name="uklid")
        self.assertTrue(department_uklid)
        self.assertIsInstance(department_uklid, Department)

    def test_employee_status_creation(self):
        """z tabulky EmployeeStatus"""
        employee_status_work = EmployeeStatus.objects.get(name="working")
        employee_status_free = EmployeeStatus.objects.get(name="free")
        self.assertTrue(employee_status_work)
        self.assertTrue(employee_status_free)
        self.assertIsInstance(employee_status_work, EmployeeStatus)
        self.assertIsInstance(employee_status_free, EmployeeStatus)


class DatabaseControlTestI(TestCase):
    """testy na praci s prazdnou databazi"""

    def setUp(self):
        self.db_control = DatabaseControl()

    def test_checking_db_empty(self):
        """Ověřuje, že checking_db vrací False, pokud jsou tabulky prázdné."""
        self.assertFalse(self.db_control.checking_db())

    def test_default_department(self):
        """Testuje vytvoření výchozího oddělení."""
        self.db_control.default_department()
        self.assertTrue(Department.objects.filter(name="nezarazeno").exists())

    def test_default_employee_status(self):
        """Testuje vytvoření výchozích statusů zaměstnanců."""
        self.db_control.default_employee_status()
        statuses = [
            "working",
            "sick_leave",
            "vacation",
            "business_trip",
            "free",
        ]
        for status in statuses:
            self.assertTrue(
                EmployeeStatus.objects.filter(name=status).exists()
            )

    def test_run_all_default(self):
        """Ověří, že po spuštění run_all_default jsou tabulky správně naplněny."""
        self.db_control.run_all_default()
        self.assertTrue(Department.objects.exists())
        self.assertTrue(EmployeeStatus.objects.exists())

    def test_delete_db(self):
        """Ověří, že delete_db správně smaže všechny záznamy z databáze."""
        # nejdriv zaplnime
        self.db_control.run_all_default()
        self.assertTrue(EmployeeStatus.objects.exists())
        self.assertTrue(Department.objects.exists())
        # zde mazeme metodou delete_db()  vraci zda bylo vse smazano
        result = self.db_control.delete_db()
        self.assertTrue(result)
        self.assertFalse(Employee.objects.exists())
        self.assertFalse(EmployeeStatus.objects.exists())
        self.assertFalse(EmployeeStatusHistory.objects.exists())
        self.assertFalse(Department.objects.exists())
        self.assertFalse(FaceVector.objects.exists())


class DatabaseControlTestII(TestCase):
    """testy na praci s plnou databazi"""

    @classmethod
    def setUpTestData(cls):
        cls.db_control = DatabaseControl()
        cls.db_control.default_department()
        cls.db_control.default_employee_status()

        # Vytvořte zaměstnance pro testovací data
        employee1 = Employee.objects.create(
            name="Jan",
            surname="Novák",
            street_number="Hlavní 123",
            city="Praha",
            postal_code="10000",
            phone_number="+420123456789",
            email="jan.novak@example.com",
            date_of_birth=date(1985, 5, 10),
            is_valid=True,
            pin_code="1234",
        )
        FaceVector.objects.create(
            employee=employee1, face_vector={"vector": face_vektor_list}
        )

        employee2 = Employee.objects.create(
            name="Marie",
            surname="Kovářová",
            street_number="Vedlejší 45",
            city="Brno",
            postal_code="60200",
            phone_number="+420987654321",
            email="marie.kovarova@example.com",
            date_of_birth=date(1992, 8, 20),
            is_valid=False,
            pin_code="5678",
        )
        FaceVector.objects.create(
            employee=employee2, face_vector={"vector": face_vektor_list_2}
        )

    def test_delete_db(self):
        """delete db if full"""
        self.assertEqual(Employee.objects.count(), 2)
        self.db_control.delete_db()
        self.assertEqual(Employee.objects.count(), 0)
