import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth import get_user_model

User = get_user_model()


def get_available_driver():
    """Zkusí postupně inicializovat webdriver pro Chrome, Edge a Firefox.
    Použije první dostupný webdriver. Pokud žádný není nalezen, vyhodí výjimku
    """
    try:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        print("[LOG] Chrome webdriver byl úspěšně inicializován.")
        return driver
    except Exception as e:
        print("Chrome webdriver není k dispozici:", e)

    try:
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        driver = webdriver.Edge(options=edge_options)
        print("[LOG] Edge webdriver byl úspěšně inicializován.")
        return driver
    except Exception as e:
        print("Edge webdriver není k dispozici:", e)

    try:
        driver = webdriver.Firefox()
        print("[LOG] Firefox webdriver byl úspěšně inicializován.")
        return driver
    except Exception as e:
        print("Firefox webdriver není k dispozici:", e)

    raise Exception("Žádný dostupný webdriver nebyl nalezen.")


class LoginLogoutSeleniumTest(StaticLiveServerTestCase):
    """
    Selenium test, který ověřuje přihlášení 
    a následné odhlášení v aplikaci.
    """

    @classmethod
    def setUpClass(cls):
        """Inicializace webdriveru"""
        super().setUpClass()
        cls.driver = get_available_driver()
        cls.driver.implicitly_wait(10)
        print("[LOG] Webdriver byl nastaven s implicitním čekáním 10 sekund.")

    @classmethod
    def tearDownClass(cls):
        """Ukončení webdriveru."""
        time.sleep(1)
        try:
            if cls.driver:
                cls.driver.quit()
                print("[LOG] Webdriver byl úspěšně ukončen.")
        except Exception as e:
            print("Chyba při ukončování webdriveru:", e)
        super().tearDownClass()

    def setUp(self):
        """Vytvoří testovacího uživatele pro přihlášení."""
        self.test_username = "seleniumuser"
        self.test_password = "hesloheslo123"
        User.objects.create_user(
            username=self.test_username,
            password=self.test_password,
            email="testbot@selenim.cz"
        )
        print("[LOG] Testovací uživatel byl vytvořen.")
        time.sleep(1)

    def test_login_logout_flow(self):
        """Otevře přihlašovací stránku, přihlásí se, ověří stav přihlášení,
        provede odhlášení a ověří přítomnost přihl. formuláře"""

        login_url = f"{self.live_server_url}/accounts/login/"
        self.driver.get(login_url)
        print("[LOG] Otevřena přihlašovací stránka:", login_url)
        time.sleep(1)

        username_input = self.driver.find_element(By.ID, "id_username")
        password_input = self.driver.find_element(By.ID, "id_password")
        print("[LOG] Nalezena pole pro username a heslo.")

        username_input.send_keys(self.test_username)
        password_input.send_keys(self.test_password)
        print("[LOG] Vyplněné přihlašovací údaje.")
        time.sleep(1)
        password_input.send_keys(Keys.RETURN)
        print("[LOG] Odeslán formulář pro přihlášení.")
        time.sleep(1)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//a[contains(@href, '/accounts/logout/')]"))
        )
        print("[LOG] Přihlášení bylo úspěšné, nalezen odkaz pro odhlášení.")
        logout_link = self.driver.find_element(By.XPATH,
                                               "//a[contains(@href,"
                                               " '/accounts/logout/')]")
        self.assertIsNotNone(logout_link)

        logout_link.click()
        print("[LOG] Kliknuto na odkaz pro odhlášení.")
        time.sleep(1)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_username"))
        )
        print("[LOG] Odhlášení bylo úspěšné.")
        
        login_form_username = self.driver.find_element(
            By.ID, "id_username"
        )
        self.assertIsNotNone(login_form_username)
        print("[LOG] Přihlašovací formulář byl nalezen.")
        