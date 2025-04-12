## Jak Instalovat

### Předpoklady

- C++ Build Tools / Desktop Development

> ⚠️ **Varování**: Jedná se o dlouhý instalační proces!

1. nainstalovat [Visual C++ Build Tools](https://visualstudio.microsoft.com/cs/visual-cpp-build-tools/)
    nebo terminalovym prikazem
    ```shell
    winget install Microsoft.VisualStudio.2022.BuildTools --force --override "--passive --wait --add Microsoft.VisualStudio.Workload.VCTools;includeRecommended"
    ```
    restart PC

2. [CMake Tool](https://github.com/Kitware/CMake/releases/download/v4.0.0-rc4/cmake-4.0.0-rc4-windows-x86_64.msi)
    - Během instalace zaškrtněte "Add CMake to PATH"

### Nastavení Projektu

1. Klonování repozitáře:
```shell
git clone https://github.com/Mirjax2000/Attendance_system.git
```
prepnout vetev na develop

2. Nastavení virtuálního prostředí:
```shell
pip install uv
uv venv
.venv\Scripts\activate
```
- nastavit python interpreter
- spustit visual studio instaler pred windows start
- kliknout na spustit
- otevre se prompt podobny cmd terminalu
- prikazem CD se dostat do rootu projectu
- spustit sadu prikazu
```shell
pip install uv
uv add dlib
```
pokud zde vsechno projde muze se uz ve svem editoru instalovat seznam modulu prikazem
```shell
uv sync
```
## Verifikace
Kontrola ze dlib je spravne nainstalovan:
```shell
python -c "import dlib; print(dlib.__version__)"
```

If no errors occur, the installation was successful.


## TAJNÝ KLÍČ
1. Vytvořte soubor `.env` přejmenováním `.env.example` a přidejte proměnnou SECRET_KEY
2. Zkopírujte hodnotu z Django attendance `settings.py` (bez uvozovek)
3. Aktualizujte nastavení pomocí:
```python
load_dotenv(override=True)
SECRET_KEY = os.getenv("SECRET_KEY", default="")
```

4. V případě potřeby vygenerujte nový SECRET_KEY:
```shell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
5. Použijte FERNET klíč z `.env.example`
6. Pouzijte email klice z `.env.example`

## Příkazy Projektu

Databázové migrace:
```shell
python manage.py makemigrations
python manage.py migrate
```

Vytvoření superuživatele (pouze při počátečním nastavení):
```shell
python manage.py createsuperuser
```

## Operace s Databází
pokud mate fixtures muzete pouzit tyto prikazy
```shell
python manage.py dumpdatautf8 myapp --indent 2 > fixtures.json
python manage.py loaddatautf8 .\files\fixtures.json
```

po spusteni aplikace je treba nastavit databazi.
jdete do aplikace a zmacknete zaplnit databzi v sekci DB status

