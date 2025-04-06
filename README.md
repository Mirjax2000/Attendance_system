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
