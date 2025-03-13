 ## how to install
 prerequisities
 C++ build tools / desktop development

 pres winget terminalovym prikazem
 ```shell
winget install Microsoft.VisualStudio.2022.BuildTools --force --override "--passive --wait --add Microsoft.VisualStudio.Workload.VCTools;includeRecommended"

 ```
nebo rucne / desktop development
https://visualstudio.microsoft.com/cs/visual-cpp-build-tools/

stahni Visual Studio 2022
    https://visualstudio.microsoft.com/cs/thank-you-downloading-visual-studio/?sku=Community&channel=Release&version=VS2022&source=VSLandingPage&cid=2030&passive=false

nainstaluj cmake: C++ nastroj
https://github.com/Kitware/CMake/releases/download/v4.0.0-rc4/cmake-4.0.0-rc4-windows-x86_64.msi
v instalatoru zaskrtni add CMake to PATH

 

naclonuj github: https://github.com/Mirjax2000/Attendance_system.git

sled prikazu do terminalu
```shell
pip install uv
```
vytvoreni VR enviroment
```shell
uv venv

```
activace VR enviroment
```shell
.venv\Scripts\activate
```


## SECRET KEY
1. priprav .env soubor prejmenovanim souboru .env.example a vytvor promennou SECRET_KEY
2. bez uvozovek prekopiruj hodnotu z Django attendance settings.py
a prepis settings tykajici se SECRET key na nasledujici
3. ```python
    load_dotenv(override=True)
    SECRET_KEY = os.getenv("SECRET_KEY", default="")
    ```
4. pokud je potreba vygenerovat SECRET_KEY pro jineho developera / terminal
    ```shell
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```
5. FERNET klic pouzij z .env.example 
 
 
 ## start projektu
 ```shell
 django-admin startproject <jmeno projektu> . 
 python manage.py startapp <jmeno applikace>
 ```

## migrace DB
```shell
python manage.py makemigrations
python manage.py migrate
```
a regni appku do settings
## vytvor superusera
jen na zacatku
```shell
python manage.py createsuperuser
```

### souborovy strom
- BASE_DIR
    - files -> fixtures.json, assets atd.
    - projekt
    - tvoje_appka
        - templates -> app templates
        - static -> app static
    - templates - global template
       - base.html
       - 404.html
    - static -> globalni static
        - main.css

## ukladani obsahu DB
```shell
python manage.py dumpdatautf8 myapp --indent 2 > fixtures.json

python manage.py loaddatautf8 .\files\fixtures.json
 ```

## Render to string
hlavne na HttpResponseNotFound
tento kod do views
```python
from django.template.loader import render_to_string

def custom_404(request, exception):
    html = render_to_string("404.html", {"message": str(exception)})
    return HttpResponseNotFound(html)
```
tento kod do url.py
```python
from moje_aplikace.views import custom_404
  # Importuj funkce z views

handler400 = "moje_aplikace.views.custom_400"
handler403 = "moje_aplikace.views.custom_403"
handler404 = "moje_aplikace.views.custom_404"
handler500 = "moje_aplikace.views.custom_500"
```


## dulezite pro vytvareni modelu
```python
created = models.DateTimeField(auto_now_add=True)
updated = models.DateTimeField(auto_now=True)
```

## admin panel, pridavani DB class do admin
soubor admin.py
```python
from . import models

admin.site.register(models.Movie)
```