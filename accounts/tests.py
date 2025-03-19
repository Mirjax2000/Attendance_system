from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.forms import SignUpForm, UserUpdateForm

User = get_user_model()


class UserViewsTests(TestCase):
    """Testy pro zobrazení seznamu, detailu, aktualizace a mazání uživatele."""

    def setUp(self):
        """
        Vytvoření dvou testovacích uživatelů a přihlášení prvního z nich
        """
        self.user1 = User.objects.create_user(
            username="user1",
            password="pass12345",
            email="user1@seznam.cz",
            first_name="User",
            last_name="One",
        )

        self.user2 = User.objects.create_user(
            username="user2",
            password="pass12345",
            email="user2@seznam.cz",
            first_name="User",
            last_name="Two",
        )

        self.client.login(username="user1", password="pass12345")

    def test_user_list_view(self):
        """Přihlášený uživatel může zobrazit seznam uživatelů.
        Ověřuje se použitá šablona a kontext."""
        response = self.client.get(reverse("user_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/user_list_detail.html")
        self.assertIn("users", response.context)
        users_list = response.context["users"]
        self.assertIn(self.user1, users_list)
        self.assertIn(self.user2, users_list)

    def test_user_detail_view_valid(self):
        """Detail existujícího uživatele vrací HTTP 200.
        Kontext obsahuje správná data o uživateli"""
        url = reverse("user_detail", args=[self.user2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/user_detail.html")
        self.assertEqual(response.context.get("user"), self.user2)
        self.assertContains(response, self.user2.username)
        self.assertContains(response, self.user2.email)

    def test_user_detail_view_invalid_id(self):
        """Detail neexistujícího uživatele vrací chybu 404"""
        invalid_id = self.user2.pk + 100
        url = reverse("user_detail", args=[invalid_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_user_update_view_valid_post(self):
        """Platný POST aktualizuje uživatele.
        Po uložení dojde k přesměrování na seznam uživatelů"""
        url = reverse("update-user", args=[self.user2.pk])
        data = {
            "username": "user2_updated",
            "first_name": "User2",
            "last_name": "Two",
            "email": "user2_updated@seznam.cz",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_list"))
        updated_user = User.objects.get(pk=self.user2.pk)
        self.assertEqual(updated_user.username, "user2_updated")
        self.assertEqual(updated_user.email, "user2_updated@seznam.cz")

    def test_user_update_view_invalid_post(self):
        """Neplatný POST neuloží změny.
        Formulář se znovu zobrazí s chybovými hláškami."""
        url = reverse("update-user", args=[self.user2.pk])
        data = {
            "username": "",  # prázdné povinné pole username
            "first_name": "User",
            "last_name": "Two",
            "email": "user2@seznam.cz",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/user_update.html")
        form = response.context.get("form")
        self.assertTrue(form.errors)
        self.assertIn("username", form.errors)
        self.assertIn(
            "Toto pole je třeba vyplnit", str(form.errors["username"])
        )

    def test_user_delete_view_confirmation(self):
        """Stránka pro potvrzení smazání uživatele je přístupná.
        Obsahuje očekávaná data o uživateli."""
        url = reverse("delete-user", args=[self.user2.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/delete_user.html")
        self.assertEqual(response.context.get("user"), self.user2)
        self.assertContains(response, self.user2.username)

    def test_user_delete_view_deletion(self):
        """Potvrzení mazání odstraní uživatele z databáze.
        Uživatel je přesměrován na seznam uživatelů."""
        url = reverse("delete-user", args=[self.user2.pk])
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_list"))
        self.assertFalse(User.objects.filter(pk=self.user2.pk).exists())


class SignUpViewTest(TestCase):
    """Testy pro registrační stránku (SignUpView)."""

    def setUp(self):
        """Založení usera"""
        self.existing_user = User.objects.create_user(
            username="existing", password="passwd123", email="test@seznam.cz"
        )

    def test_signup_view_success(self):
        """Nový uživatel úspěšně zaregistruje.
        Po registraci je přesměrován na seznam uživatelů."""
        url = reverse("signup")
        data = {
            "username": "novyuzivatel",
            "first_name": "Novy",
            "last_name": "Uzivatel",
            "email": "novy@seznam.cz",
            "password1": "superheslo1",
            "password2": "superheslo1",
        }
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(
            response, reverse("login") + "?next=" + reverse("user_list")
        )
        self.assertTrue(User.objects.filter(username="novyuzivatel").exists())

    def test_signup_view_duplicate_email(self):
        """Registrace s již existujícím e‑mailem není umožněna.
        Formulář zobrazí chybu."""
        url = reverse("signup")
        data = {
            "username": "jinyuser",
            "first_name": "Jiny",
            "last_name": "Uzivatel",
            "email": "test@seznam.cz",
            "password1": "Testheslo123",
            "password2": "Testheslo123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")
        response = self.client.post(url, data)
        form = response.context.get("form")
        self.assertTrue(form.is_bound)
        self.assertIn(
            "Tento e-mail je již používán. Zvolte jiný.",
            form.errors.get("email"),
        )


class CustomLoginViewTest(TestCase):
    """Testy pro přihlašovací pohled (CustomLoginView)."""

    def setUp(self):
        """Vytvoření uživatele pro testy"""
        self.user = User.objects.create_user(
            username="testuser",
            password="heslotajne123",
            email="user@zlatohor.cz",
        )

    def test_custom_login_view_invalid_credentials(self):
        """Zadání nesprávných údajů neumožní přihlášení.
        Zobrazí se chybová hláška."""
        url = reverse("login")
        data = {"username": "testuser", "password": "spatneheslo"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")
        form = response.context.get("form")
        self.assertTrue(form.errors)
        self.assertIn("Nepodařilo se přihlásit", str(form.non_field_errors()))

    def test_custom_login_view_success(self):
        """Zadání správných údajů přihlásí uživatele.
        Došlo k přesměrování na dashboard"""
        url = reverse("login")
        data = {"username": "testuser", "password": "heslotajne123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("main_panel"))
        self.assertTrue(self.client.session.get("_auth_user_id"))


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
