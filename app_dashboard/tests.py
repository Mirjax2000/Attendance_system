"""Django tests"""

import json
from datetime import date

import numpy as np
from django.test import TestCase

from app_dashboard.forms import EmployeeForm
from app_main.models import Department, Employee, EmployeeStatus, FaceVector

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

    def test_employee_creation(self):
        """Z tabulky employee"""
        employee_jan = Employee.objects.get(slug="jan-novak")
        self.assertEqual(employee_jan.name, "Jan")
        self.assertEqual(employee_jan.surname, "Novák")
        self.assertEqual(employee_jan.city, "Praha")
        self.assertEqual(employee_jan.postal_code, "10000")
        self.assertEqual(employee_jan.phone_number, "+420123456789")
        self.assertEqual(employee_jan.email, "jan.novak@example.com")
        self.assertEqual(employee_jan.date_of_birth, date(1985, 5, 10))
        self.assertEqual(employee_jan.age(), (39))
        self.assertTrue(employee_jan.check_pin_code("1234"))
        self.assertTrue(employee_jan.department, "nezarazeno")
        self.assertEqual(employee_jan.employee_status, "free")
        self.assertNotEqual(employee_jan.employee_status, "vacation")
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


class EmployeeFormTests(TestCase):
    def setUp(self):
        """Vytvoření potřebných objektů."""
        self.department = Department.objects.create(name="IT Department")
        self.employee_status = EmployeeStatus.objects.create(name="Active")

        self.existing_employee = Employee.objects.create(
            name="Josef",
            surname="Drtikol",
            street_number="Vrsovicka 12",
            city="Praha",
            postal_code="11000",
            phone_number="123456789",
            email="testuser@seznam.cz",
            date_of_birth="1989-02-13",
            pin_code="1234",
            department=self.department,
            employee_status=self.employee_status,
        )

    def get_valid_form_data(self):
        """Pomocná metoda vracející validní data formuláře."""
        return {
            "name": "Karel",
            "surname": "Tanker",
            "street_number": "Zelnak 456",
            "city": "Brno",
            "postal_code": "60200",
            "phone_number": "987654321",
            "email": "karel.tanker@tankovna.cz",
            "date_of_birth": "1975-05-15",
            "pin_code": "4321",
            "department": self.department.pk,
            "employee_status": self.employee_status.pk,
        }

    def test_valid_form(self):
        """Formulář s platnými daty by měl projít validací."""
        form_data = self.get_valid_form_data()
        form = EmployeeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_required_field_name(self):
        """Testuje, že pole 'name' je povinné."""
        form_data = self.get_valid_form_data()
        form_data["name"] = ""
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("Jméno je povinné!", form.errors["name"])

    def test_required_field_surname(self):
        """Testuje, že pole 'surname' je povinné."""
        form_data = self.get_valid_form_data()
        form_data["surname"] = ""
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("surname", form.errors)
        self.assertIn("Příjmení je povinné!", form.errors["surname"])

    def test_duplicate_email(self):
        """
        Testuje, že při zadání e-mailu, který již existuje
        (upraví i velikost písma),dojde k chybě.
        """
        form_data = self.get_valid_form_data()
        form_data["email"] = "TESTUSER@seznam.cz"
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(
            form.errors["email"], ["Tento e-mail je již používán. Zvolte jiný."]
        )

    def test_invalid_postal_code(self):
        """
        Testuje, že je vyvolána chyba validace pro PSČ,
        pokud PSČ neobsahuje přesně 5 číslic.
        """
        form_data = self.get_valid_form_data()
        form_data["postal_code"] = "1234"
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("postal_code", form.errors)
        self.assertIn(
            "PSČ musí obsahovat 5 číslic.", form.errors["postal_code"]
        )

    def test_invalid_pin_code(self):
        """
        Testuje, že je vyvolána chyba validace,
        pokud PIN kód neobsahuje přesně 4 číslice.
        """
        form_data = self.get_valid_form_data()
        form_data["pin_code"] = "123"
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("pin_code", form.errors)
        self.assertIn(
            "PIN kód musí obsahovat přesně 4 číslice.", form.errors["pin_code"]
        )
