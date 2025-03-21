from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.forms import SignUpForm, UserUpdateForm

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
