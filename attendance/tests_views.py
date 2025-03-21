from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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
