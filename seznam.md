 ## start projektu
 ```shell
 django-admin startproject <jmeno projektu> . 
 python manage.py startapp <jmeno applikace>
 ```
## SECRET KEY
1. priprav .env soubor a vytvor promennou SECRET_KEY
2. bez uvozovek prekopiruj hodnotu ze settings
3. ```python
    load_dotenv(override=True)
    SECRET_KEY = os.getenv("SECRET_KEY", default="")
    ```
4. pokud je potreba vygenerovat SECRET_KEY pro jineho developera / terminal
    ```shell
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
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