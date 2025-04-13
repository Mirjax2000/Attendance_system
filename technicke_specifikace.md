# Kdo je uživatel v této aplikaci?

V této aplikaci může být uživatelem:
napr:
* Majitel firmy
* Ředitel
* HR manažer

Tito uzivatela ziskavaji pristup k administratorskemu panelu, kde muzou ziskavat data o svych zamestancich:
napr:
* pocet zamestnancu
* kdo je v praci/ na sluzebni ceste/ na nemocenske
* statistiky
* Prehledy poctu hodin 
* rozesilani informacnich emailu

# Proč porovnávat vektory místo obrázků?

V tomto projektu se zaměřujeme na efektivní rozpoznávání obličejů. Níže jsou hlavní důvody pro používání vektorů:

## 1. Velikost dat
* Vektory zabírají kilobyty
* Obrázky mohou mít až megabyty
* Pro 1000 uživatelů:
    * Obrázky: až 2 GB
    * Vektory: několik MB

## 2. Rychlost porovnání
* Porovnávání čísel je rychlejší než obrázků
* Okamžité porovnání bez nutnosti extrakce
* Kratší doba identifikace

## 3. Efektivita při vyhledávání
* Není nutné opakovaně detekovat obličeje
* Možnost hromadného porovnání vektorů
* Výrazně vyšší efektivita systému

## 4. Zabezpečení
* Lepší ochrana soukromí
* Vektory nelze snadno převést zpět na obrázek
* Zvýšená bezpečnost dat

## Závěr
Porovnávání vektorů je optimální řešení pro:
* Rychlé rozpoznávání
* Efektivní využití paměti
* Bezpečné ukládání dat
* Budoucí škálovatelnost systému

# Funkce spojené s odesíláním e-mailů
Tato sekce dokumentace popisuje funkce týkající se práce s e-maily v projektu. Aplikace poskytuje komplexní řešení pro vytváření, validaci i cílené odesílání zpráv uživatelům, zaměstnancům a oddělením.
## Přehled funkcí
### Základní formulář pro odeslání e-mailů
Pomocí tohoto formuláře může uživatel zadat standardní parametry zprávy:
- **Předmět zprávy (Subject)** – povinná položka, definuje titulek zprávy.
- **Obsah zprávy (Message)** – povinná položka, může obsahovat standardní text i HTML formátování dle potřeby a nastavení aplikace.

### Možnosti výběru příjemců (Delivery Methods)
Formulář umožňuje výběr několika způsobů doručování podle typu a kategorii příjemců. Nabízeny jsou následující varianty:
- **Manuální zadání příjemců ("Ručně zadávané adresy")**
Umožňuje libovolně zadat seznam e-mailových adres přímo do textového pole. Aplikace provede jejich validaci, odstraní duplicity a upozorní uživatele na případné chyby ve vstupu. Jednotlivé mailové adresy je třeba oddělovat čárkou.
- **Zaměstnanci ("Employees")**
Umožní odeslat zprávu cíleně definovaným zaměstnancům, jejichž seznam se zobrazí pro jednoduchý výběr. Systém automaticky sjednotí jejich e-mailové adresy do seznamu mailových adres k odeslání.
- **Oddělení ("Departments")**
Odesílá zprávu všem zaměstnancům zvolených oddělení jedním kliknutím. Seznam adres je automaticky sestaven z aktuálních dat zaměstnanců přidružených k jednotlivým oddělením.
- **Kombinovaná metoda ("možné rozšíření")**
S touto volbou má uživatel možnost zkombinovat předchozí metody a vytvořit cílový seznam příjemců dle potřeby napříč skupinami. Zatím nebyla implementována.

### Další důležité vlastnosti a omezení
- **Automatické ověřování platnosti e-mailů:** Aplikace při každém odesílání kontroluje platnost e-mailových adres příjemců, včetně správného formátu e-mailů ve všech variantách jejich zadání.
- **Ošetření vstupních chyb:** Uživatele systém upozorní, pokud některý povinný údaj nevyplní, překročí maximální povolené délky textů nebo chybně zadá e-mailovou adresu.
- **Integrace e-mailových šablon:** Uživatelská zkušenost je usnadněna možností rychle vložit předdefinované e-mailové šablony. Pomocí AJAX rozhraní aplikace načítá šablony bez nutnosti opětovného načtení stránky a vkládá jejich obsah přímo do formuláře.
- **Optimalizace seznamu a odstranění duplicit:** Systém dokáže automaticky identifikovat a odstranit duplicitní adresy, pokud jsou zadány jak uživatelsky, tak i prostřednictvím zaměstnanců nebo oddělení. Zatím nebyla implementována.

## Praktická ukázka workflow:
Uživatelem typicky zvolený postup při práci s formulářem odesílání e-mailů:
1. Uživatel vybere požadovaný způsob zadání příjemců (způsob doručení).
2. Následně vyplní povinné údaje – předmět a tělo zprávy. Některé údaje mohou být předvyplněny šablonou.
3. Uživatel zadá nebo vybere cílové e-mailové adresy dle zvolené varianty.
4. Při potvrzení formuláře se provede automatická kontrola všech údajů.
5. V případě bezchybných dat je zpráva odeslána a uživatel je informován o úspěšném dokončení operace.

## Poznámky k vývoji a testování
Za účelem udržení kvality kódu a spolehlivosti realizovaných funkcí je implementován bohatý soubor automatizovaných testů, které:
- Ověřují správnost formulářů a jejich validačních pravidel.
- Zajišťují konzistentní chování AJAX volání při práci se šablonami.
- Kontrolují ošetření vstupů, duplikací a správnou manipulaci s e-mailovými adresami.

Z tohoto pohledu je tato část aplikace připravena jak pro běžné uživatelské použití, tak pro rozvoj budoucího funkcionalit s minimálním rizikem regresí díky existujícím testovacím scénářům.

# Testovací sada projektu
Testovací sada zajišťuje spolehlivost, stabilitu a správnou funkci celé aplikace. Testy v projektu pokrývají klíčové oblasti aplikace, jako jsou modely, view (pohledy) a formuláře, a zajišťují vysokou kvalitu kódu.
Níže naleznete popis testovaných oblastí a hlavních variant testů, kterými projekt disponuje.
## 1. Testy modelů (`tests_models`)
Tyto testy ověřují správnost implementace databázových modelů. Testování modelů zahrnuje především následující oblasti:
- **Základní operace s modelem zaměstnance a oddělení**
    - Ověření správného vytvoření zaměstnanců a oddělení.
    - Kontrola správného počtu zaměstnanců a jejich přiřazení ke správným oddělením.

- **Správa dat ve vektorových reprezentacích**
    - Kontrola správného generování a ukládání vektorů tváří.

- **Kontrola stavu databáze**
    - Testování kompletního procesu inicializace a případného vymazání databáze.
    - Ověřování existence základních záznamů, které musejí být vždy přítomny (např. výchozí oddělení a statusy zaměstnanců).

## 2. Testy pohledů (views) (`tests_views`)
Tato skupina testů ověřuje správnost a spolehlivost pohledů a jednotlivých akcí v aplikaci. K testovaným scénářům patří mimo jiné:
- **Uživatelské pohledy**
    - Validace detailního pohledu na uživatele, jeho aktualizace a smazání.
    - Kontrola správného zobrazení seznamů uživatelů.

- **Autentizace a registrace uživatele**
    - Kompletní testování procesu registrace nového uživatele.
    - Testy přihlášení uživatele nejen s platnými, ale i neplatnými údaji.

- **Odesílání a zpracování e-mailů**
    - Ověření zobrazení formulářů pro odeslání e-mailů s různými typy dat (platná a neplatná data).
    - Testování odeslání emailu jak zaměstnancům, jednotlivým emailům, tak i celému oddělení.
    - Testy načítání e-mailových šablon a kontroly jejich správného obsahu přes AJAX volání.
    - Kontrola limitů v délce obsahu e-mailu a správnost přesměrování při chybách.

## 3. Testy formulářů (`tests_forms`)
Tyto testy validují správnou funkcionalitu formulářů v aplikaci, a to jak ze strany UI, tak i na úrovni samotné validace na backendu.
- **Formulář registrace a aktualizace uživatele**
    - Kontrola formulářů registrace nového uživatele (validní data, duplicitní email, chybějící povinná pole, nesoulad hesel).
    - Formulář pro aktualizaci uživatele s různými typy dat a kontrolou validace.

- **Formulář zaměstnanců**
    - Testy pro celý životní cyklus zaměstnaneckého formuláře (validace polí jako email, telefon, PSČ, datum narození, PIN kód a kontrola duplicitních údajů).

- **Formulář pro odesílání emailů**
    - Kontrola validního i nevalidního vyplnění polí formuláře (výběr příjemců, formát e-mailů, kontrola povinných polí předmětu a zprávy, ověření prázdných polí).

## 4. Selenium testování (`tests_selenium`)
Pro maximální realističnost testování UI aplikace byl vytvořen testy s využitím frameworku Selenium. Je orientován na uživatelský pohled do aplikace a ověřuje:
- **Autentizační procesy**
    - Kompletní workflow uživatelského přihlášení a odhlášení s důrazem na uživatelskou interakci s aplikací a reálnou simulaci chování aplikace v prohlížeči.

Použití Selenium testů podporuje rychlé odhalení případných regresí na straně uživatelského rozhraní a uživatelské interakce.
## Přínos testů pro projekt
Testová sada byla navržena tak, aby zajišťovala:
- Maximální pokrytí projektu klíčových funkcionalit.
- Snadné sledování případných budoucích změn, které by mohly ovlivnit kritické části aplikace.
- Včasné odhalení chyb a snadnou možnost jejich opravy před nasazením do ostrého provozu.
- Rychlejší a bezpečnější nasazování nových funkcionalit bez rizika, že dojde k narušení existující funkcionality.

Pravidelná údržba a rozšiřování těchto testů je doporučeno v průběhu dalšího vývoje projektu, jelikož představují nejlepší postupy v oblasti moderního vývoje aplikací.
