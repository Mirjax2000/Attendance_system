"""Django tests"""

from datetime import date

from django.test import TestCase

from app_main.models import Employee, FaceVector


class EmployeeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
            employee=employee1, face_vector={"vector": [0.1, 0.2, 0.3]}
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
            employee=employee2, face_vector={"vector": [0.4, 0.5, 0.6]}
        )

    def test_employee_creation(self):
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
        self.assertEqual(employee_jan.is_valid, True)

    def test_face_vector_creation(self):
        face_vector_jan = FaceVector.objects.get(
            employee__email="jan.novak@example.com"
        )
        self.assertIsNotNone(face_vector_jan.face_vector_fernet)
        self.assertIsInstance(face_vector_jan.face_vector, list)
        self.assertIsInstance(face_vector_jan.face_vector_fernet, bytes)
        self.assertEqual(
            face_vector_jan.decrypt_vector(), '{"vector": [0.1, 0.2, 0.3]}'
        )
        self.assertFalse(face_vector_jan.face_vector)
