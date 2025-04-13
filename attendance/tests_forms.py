"""Forms tests"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import SignUpForm, UserUpdateForm
from app_dashboard.forms import EmployeeForm, SendMailForm
from app_main.models import Department, Employee, EmployeeStatus

User = get_user_model()


class SignUpFormTests(TestCase):
    """Testy pro registrační formulář SignUpForm."""

    def setUp(self):
        """Vytvoříme uživatele pro testy"""
        self.existing_user = User.objects.create_user(
            username="lojzauser",
            password="heslo12345",
            email="lojza@seznam.cz",
            first_name="Lojza",
            last_name="User",
        )

    def test_signup_form_valid_data(self):
        """Ověření, že formulář je validní při zadání platných dat."""
        form_data = {
            "username": "jirikuser",
            "first_name": "Jirik",
            "last_name": "User",
            "email": "jirikuser@email.cz",
            "password1": "masakr123",
            "password2": "masakr123",
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_signup_form_duplicate_email(self):
        """Formulář není validní, pokud je zadán e‑mail, který je již v DB."""
        form_data = {
            "username": "ferencuser",
            "first_name": "Ferenc",
            "last_name": "User",
            "email": "lojza@seznam.cz",
            "password1": "megasuper123",
            "password2": "megasuper123",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(
            form.errors["email"],
            ["Tento e-mail je již používán. Zvolte jiný."],
        )

    def test_signup_form_missing_required_field(self):
        """
        Formulář je validní, pokud chybí nepovinné pole (first_name)
        """
        form_data = {
            "username": "josefvyskocil",
            "first_name": "",
            "last_name": "Vyskocil",
            "email": "zaskoc@me.com",
            "password1": "Zass12345!",
            "password2": "Zass12345!",
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_missing_required_field_2(self):
        """
        Formulář je validní, pokud chybí nepovinné pole (last_name)
        """
        form_data = {
            "username": "josefvyskocil",
            "first_name": "Josef",
            "last_name": "",
            "email": "zaskoc@me.com",
            "password1": "Zass12345!",
            "password2": "Zass12345!",
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_missing_required_field_3(self):
        """
        Formulář není validní, pokud chybí povinné pole (user_name)
        """
        form_data = {
            "username": "",
            "first_name": "Josef",
            "last_name": "Vyskocil",
            "email": "zaskoc@me.com",
            "password1": "Zass12345!",
            "password2": "Zass12345!",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertTrue(form.errors["username"])

    def test_signup_form_password_mismatch(self):
        """Formulář není validní, pokud se zadaná hesla neshodují"""
        form_data = {
            "username": "neumipsat",
            "first_name": "Neumi",
            "last_name": "Psat",
            "email": "chyba@velka.eu",
            "password1": "heslo123",
            "password2": "heslo321",
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)
        self.assertTrue(form.errors["password2"])


class UserUpdateFormTests(TestCase):
    """Testy pro formulář pro aktualizaci uživatele UserUpdateForm."""

    def setUp(self):
        """Vytvoříme uživatele pro testy"""
        self.user = User.objects.create_user(
            username="lojzahovorka",
            password="verymuchstrong",
            email="lojzahovorka@metoo.cz",
            first_name="Lojza",
            last_name="Hovorka",
        )

    def test_update_form_valid_data(self):
        """
        Ověření, že formulář je validní při zadání platných dat
        a lze uložit změny
        """
        form_data = {
            "username": "lojzahovorka",
            "first_name": "Jirik",
            "last_name": "Vasicek",
            "email": "zmena@menot.cz",
            "pin_code": "2121",
        }
        form = UserUpdateForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        updated_user = form.save()
        self.assertEqual(updated_user.first_name, "Jirik")
        self.assertEqual(updated_user.last_name, "Vasicek")
        self.assertEqual(updated_user.email, "zmena@menot.cz")

    def test_update_form_missing_required_field(self):
        """Formulář není validní, pokud chybí povinné pole (username)"""
        form_data = {
            "username": "",
            "first_name": "Jan",
            "last_name": "Zrokycan",
            "email": "janvon@rokycan.eu",
        }
        form = UserUpdateForm(instance=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_update_form_missing_required_field2(self):
        """Formulář je validní, pokud chybí nepovinné pole (first_name)"""
        form_data = {
            "username": "lojzahovorka",
            "first_name": "",
            "last_name": "Zrokycan",
            "email": "janvon@rokycan.eu",
        }
        form = UserUpdateForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_form_missing_required_field3(self):
        """Formulář je validní, pokud chybí nepovinné pole (last_name)"""
        form_data = {
            "username": "lojzahovorka",
            "first_name": "Jan",
            "last_name": "",
            "email": "janvon@rokycan.eu",
        }
        form = UserUpdateForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_form_optional_email(self):
        """
        Ověření, že e‑mail je volitelné pole – prázdný e‑mail nevyvolá chybu
        """
        form_data = {
            "username": "lojzahovorka",
            "first_name": "Jan",
            "last_name": "Zizka",
            "email": "",
        }
        form = UserUpdateForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid(), form.errors)


class EmployeeFormTests(TestCase):
    """Testy pro formulář uživatele."""

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

    def test_required_field_pin_code(self):
        """Testuje, že pole 'pin_code' je povinné."""
        form_data = self.get_valid_form_data()
        form_data["pin_code"] = ""
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("pin_code", form.errors)
        self.assertIn(
            "PIN musí obsahovat přesně 4 číslice.", form.errors["pin_code"]
        )

    def test_duplicate_email(self):
        """
        Testuje, že při zadání e-mailu, který již existuje
        (upraví i velikost písma), dojde k chybě.
        """
        form_data = self.get_valid_form_data()
        form_data["email"] = "TESTUSER@seznam.cz"
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(
            form.errors["email"],
            ["Tento e-mail je již používán. Zvolte jiný."],
        )

    def test_invalid_email_format(self):
        """
        Testuje validaci e-mailu, pokud je zadán ve špatném formátu.
        """
        form_data = self.get_valid_form_data()
        form_data["email"] = "invalid-email"
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertTrue(
            any("platnou" in msg.lower() for msg in form.errors["email"])
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
            "PSČ musí obsahovat přesně 5 číslic bez mezer.",
            form.errors["postal_code"],
        )

    def test_invalid_phone_number(self):
        """
        Testuje, že je vyvolána chyba validace,
        pokud telefonní číslo obsahuje nepovolené znaky.
        """
        form_data = self.get_valid_form_data()
        form_data["phone_number"] = "12345ABCD"
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)
        self.assertTrue(
            any(
                "telefonní číslo musí" in msg.lower()
                and "formátu" in msg.lower()
                for msg in form.errors["phone_number"]
            )
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
            "PIN musí obsahovat přesně 4 číslice.", form.errors["pin_code"]
        )

    def test_invalid_date_of_birth(self):
        """
        Testuje, že je vyvolána chyba validace, pokud
        je datum narození zadané v budoucnosti.
        """
        form_data = self.get_valid_form_data()
        form_data["date_of_birth"] = "3000-01-01"
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("date_of_birth", form.errors)
        self.assertTrue(
            any(
                "budoucnosti" in msg.lower()
                for msg in form.errors["date_of_birth"]
            )
        )

    def test_name_trimming(self):
        """
        Testuje, že mezery na začátku a na konci pole 'name' jsou odstraněny.
        """
        form_data = self.get_valid_form_data()
        form_data["name"] = "  Karel  "
        form = EmployeeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        employee = form.save(commit=False)
        self.assertEqual(employee.name, "Karel")

    def test_surname_trimming(self):
        """
        Testuje, že mezery na začátku a na konci pole 'surname' jsou odstraněny.
        """
        form_data = self.get_valid_form_data()
        form_data["surname"] = "  Tanker  "
        form = EmployeeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        employee = form.save(commit=False)
        self.assertEqual(employee.surname, "Tanker")

    def test_update_employee_valid(self):
        """
        Testuje, že aktualizace existujícího zaměstnance
        s validními daty projde validací.
        """
        form_data = self.get_valid_form_data()
        form = EmployeeForm(data=form_data, instance=self.existing_employee)
        self.assertTrue(form.is_valid(), form.errors)
        updated_employee = form.save()
        self.assertEqual(updated_employee.name, form_data["name"])
        self.assertEqual(updated_employee.surname, form_data["surname"])
        self.assertEqual(updated_employee.email, form_data["email"].lower())

    def test_update_employee_same_email(self):
        """
        Testuje, že aktualizace zaměstnance, kdy zůstane e-mail stejný
        (i když je upraveno na jiné písmena),
        projde validací.
        """
        form_data = self.get_valid_form_data()
        form_data["email"] = self.existing_employee.email.upper()
        form = EmployeeForm(data=form_data, instance=self.existing_employee)
        self.assertTrue(form.is_valid(), form.errors)

    def test_update_employee_duplicate_email(self):
        """
        Testuje, že při aktualizaci zaměstnance novým e-mailem,
        který je duplicitní (patří jinému zaměstnanci),
        dojde k chybě.
        """
        another_employee = Employee.objects.create(
            name="User",
            surname="Novy",
            street_number="Zelňák 1",
            city="Brno",
            postal_code="60200",
            phone_number="111222333",
            email="novy@user.cz",
            date_of_birth="1990-01-01",
            pin_code="0000",
            department=self.department,
            employee_status=self.employee_status,
        )
        form_data = self.get_valid_form_data()
        form_data["email"] = self.existing_employee.email.upper()
        form = EmployeeForm(data=form_data, instance=another_employee)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(
            form.errors["email"],
            ["Tento e-mail je již používán. Zvolte jiný."],
        )

    def test_update_pin_code(self):
        """
        testuje pin_code update
        """
        another_employee = Employee.objects.create(
            name="User",
            surname="Novy",
            street_number="Zelňák 1",
            city="Brno",
            postal_code="60200",
            phone_number="111222333",
            email="novy@user.cz",
            date_of_birth="1990-01-01",
            pin_code="0000",
            department=self.department,
            employee_status=self.employee_status,
        )
        form_data = self.get_valid_form_data()
        form_data["pin_code"] = "1111"
        form = EmployeeForm(data=form_data, instance=another_employee)
        self.assertTrue(form.is_valid())
        updated_employee = form.save()
        self.assertEqual(updated_employee.pin_code, "")
        self.assertEqual(updated_employee.check_pin_code("1111"), True)


class SendMailFormTests(TestCase):
    """Testy pro formulář odesílání mailů."""

    def setUp(self):
        """Vytvoření potřebných dat"""
        self.department = Department.objects.create(name="Oddělení testování")
        self.employee = Employee.objects.create(
            name="Jan",
            surname="Novák",
            email="jan.novak@priklad.cz",
            date_of_birth="1985-04-01",
        )

    def get_valid_form_data(self):
        """validní data"""
        return {
            "subject": "Předmět testovacího e-mailu",
            "message": "Testovací text zprávy.",
            "delivery_method": "manual",  # změněno na validní hodnotu "manual"
            "emails": "test@priklad.cz",
            "employee_ids": [self.employee.id],
            "department": self.department.id,
        }

    def test_valid_full_form(self):
        """test validních dat"""
        form = SendMailForm(data=self.get_valid_form_data())
        self.assertTrue(form.is_valid())

    def test_form_empty_recipients(self):
        """test prázdný adresát"""
        data = self.get_valid_form_data()
        data["emails"] = ""
        data["employee_ids"] = []
        data["department"] = ""
        form = SendMailForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("emails", form.errors)
        self.assertIn(
            "Zadejte prosím e-mailové adresy.", form.errors["emails"]
        )

    def test_invalid_email_format(self):
        """test neplatný formát zprávy"""
        data = self.get_valid_form_data()
        data["emails"] = "neplatny-email"
        form = SendMailForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("emails", form.errors)

    def test_only_employees_selected(self):
        """test výběru mailů zaměstnanců"""
        data = self.get_valid_form_data()
        data["delivery_method"] = "employee"
        data["emails"] = ""
        data["department"] = ""
        form = SendMailForm(data=data)
        self.assertTrue(form.is_valid())

    def test_only_department_selected(self):
        """test výběru mailů oddělení"""
        data = self.get_valid_form_data()
        data["delivery_method"] = "department"
        data["emails"] = ""
        data["employee_ids"] = []
        form = SendMailForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_delivery_method(self):
        """test výběr neplatné metody"""
        data = self.get_valid_form_data()
        data["delivery_method"] = "neplatna_metoda"  # záměrně neplatná metoda
        form = SendMailForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("delivery_method", form.errors)

    def test_empty_subject_message(self):
        """test prázdný předmět"""
        data = self.get_valid_form_data()
        data["subject"] = ""
        data["message"] = ""
        form = SendMailForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("subject", form.errors)
        self.assertIn("message", form.errors)
