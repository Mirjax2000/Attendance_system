"""Forms tests"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import SignUpForm, UserUpdateForm
from app_dashboard.forms import EmailForm, EmployeeForm
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
            form.errors["email"], ["Tento e-mail je již používán. Zvolte jiný."]
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
            form.errors["email"], ["Tento e-mail je již používán. Zvolte jiný."]
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
            form.errors["email"], ["Tento e-mail je již používán. Zvolte jiný."]
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


class EmailFormTests(TestCase):
    def test_valid_single_email(self):
        """
        Testuje validní jeden e-mail se správným formátem, tématem a zprávou.
        """
        data = {
            "recipient_email": "user@seznam.cz",
            "subject": "Pozdrav",
            "message": "Toto je platná zpráva, která obsahuje "
            "více jak 10 znaků.",
        }
        form = EmailForm(data=data)
        self.assertTrue(form.is_valid())
        # Očekáváme seznam s jedním e-mailem
        self.assertEqual(
            form.cleaned_data["recipient_email"], ["user@seznam.cz"]
        )

    def test_valid_multiple_emails(self):
        """Testuje validní více e-mailových adres oddělených čárkou."""
        data = {
            "recipient_email": "user1@seznam.cz, user2@seznam.cz, "
            "user3@seznam.cz",
            "subject": "Informace",
            "message": "Kompletní zpráva bez chyb, splňující délku a "
            "ostatní podmínky.",
        }
        form = EmailForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["recipient_email"],
            ["user1@seznam.cz", "user2@seznam.cz", "user3@seznam.cz"],
        )

    def test_invalid_email_format(self):
        """Testuje neplatný formát e-mailové adresy."""
        data = {
            "recipient_email": "invalid-email",
            "subject": "Test",
            "message": "Toto je dostatečně dlouhá zpráva.",
        }
        form = EmailForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("má neplatný formát", str(form.errors["recipient_email"]))

    def test_banned_domain(self):
        """Testuje e-mailovou adresu s nepovolenou doménou."""
        data = {
            "recipient_email": "user@spam.com",
            "subject": "Upozornění",
            "message": "Plně validní zpráva, která splňuje všechny "
            "ostatní podmínky.",
        }
        form = EmailForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("není povolena", str(form.errors["recipient_email"]))

    def test_empty_recipient_email(self):
        """Testuje prázdné pole pro příjemce."""
        data = {
            "recipient_email": "",
            "subject": "Něco",
            "message": "Tato zpráva je dostatečně dlouhá.",
        }
        form = EmailForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Toto pole je vyžadováno.", str(form.errors["recipient_email"])
        )

    def test_subject_in_message(self):
        """Testuje případ, kdy se předmět nachází v textu zprávy."""
        data = {
            "recipient_email": "user@seznam.cz",
            "subject": "Test",
            "message": "Toto je test zprávy, která obsahuje i slovo test.",
        }
        form = EmailForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Předmět by neměl být obsažen ve zprávě.",
            str(form.errors["subject"]),
        )

    def test_message_too_short(self):
        """Testuje případ, kdy je zpráva příliš krátká."""
        data = {
            "recipient_email": "user@seznam.cz",
            "subject": "Zpráva",
            "message": "krátká",
        }
        form = EmailForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("Zpráva je příliš krátká", str(form.errors["message"]))

    def test_valid_when_subject_not_in_message(self):
        """Test, kdy je předmět odlišný od obsahu zprávy."""
        data = {
            "recipient_email": "user@seznam.cz",
            "subject": "Pozdrav",
            "message": "Toto je zpráva, která nezmiňuje daný předmět a "
            "je dostatečně dlouhá.",
        }
        form = EmailForm(data=data)
        self.assertTrue(form.is_valid())

    def test_both_subject_and_message_errors(self):
        """
        Testuje případ, kdy zároveň selže kontrola předmětu
        (je součástí zprávy) a zpráva je příliš krátká.
        """
        data = {
            "recipient_email": "user@seznam.cz",
            "subject": "Chyba",
            "message": "chyba",  # příliš krátká a obsahuje předmět
        }
        form = EmailForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Předmět by neměl být obsažen ve zprávě.",
            str(form.errors["subject"]),
        )
        self.assertIn("Zpráva je příliš krátká", str(form.errors["message"]))

    def test_recipient_email_with_extra_whitespace(self):
        """
        Testuje situaci, kdy jsou e-mailové adresy zadány s
        přebytečnými mezerami.
        """
        data = {
            "recipient_email": "  user@seznam.cz  ,   user2@seznam.cz   ",
            "subject": "Info",
            "message": "Zpráva je dostatečně dlouhá a bez chyb.",
        }
        form = EmailForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["recipient_email"],
            ["user@seznam.cz", "user2@seznam.cz"],
        )
