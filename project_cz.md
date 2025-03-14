



# Docházkový systém

Tento projekt je založen na dvou aplikacích:

## 1. Zaměstnanecká aplikace /  dochazkovy system

**Funkčnost:**
- Příchod
- Odchod
- Další akce (napr, sluzebni cesta, dovolena, atd)

**Funkce:**
- Využívá hardwarový ovladač kamery k zachycení tváře zaměstnance.
- detekce tvare pomoci face detectoru YUNET
- Vypočítá vektor obličeje ze zachyceného obrazu.
- Budeme pouzivat neuronovou sit DLIB a modul face_recognition.
- Porovnává vypočítaný vektor s vektory uloženými v databázi pro ověření.
- Ověření zaměstnance pomocí vektoru obličeje a PIN kódu.
- Výběr režimu po úspěšném ověření.
- Sleduje pracovní stav zaměstnance (přítomen nebo nepřítomen).
- Po potvrzení zaměstnancem nastaví stav na 'v práci' a začne sledovat čas v databázi.
- Databázové modely lze rozšířit o různé další funkce a metody.

## 2. Dashboard / Přehled

**Uživatelé:**
- Majitel společnosti
- Ředitel
- HR manažer

**Přístup:**
- Administrativní panel

**Přístup k datům:**
- CRUD zamestance
- Počet zaměstnanců
- Stav zaměstnanců v reálném čase (v práci, na služební cestě, na nemocenské)
- Statistiky
- Hodinové výkazy
- Rozesílání informačních emailů
- CRUD departement

**Permisions:**
- omezeni pro create/delete  zamestnance
- Prehledy - default
- rozesilani emailu - HR


