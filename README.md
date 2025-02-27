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
