# Proč porovnávat vektory místo obrázků

V tomto projektu se zaměřujeme na efektivní rozpoznávání obličejů. Při implementaci systému pro identifikaci uživatelů je důležité zvolit správný přístup k ukládání a porovnávání dat. Zde uvádíme důvody, proč je výhodné porovnávat obličejové vektory místo celých obrázků:

## 1. Velikost dat

Obličejové vektory obvykle zabírají pouze několik kilobajtů, zatímco obrázky mohou mít velikost až několik megabajtů. Například obrázek o velikosti 2 MB zabere pro 1000 uživatelů až 2 GB paměti, zatímco 1000 obličejových vektorů může zabrat jen několik megabajtů. Tímto způsobem je možné efektivněji využít dostupnou paměť.

## 2. Rychlost porovnání

Při porovnávání obličejových vektorů pracujeme s čísly, což je mnohem rychlejší než porovnávání celých obrázků. Uložení obličejového vektoru umožňuje okamžité porovnání s jinými vektory bez nutnosti opětovné extrakce z obrázků. To zvyšuje rychlost vyhledávání a zkracuje dobu potřebnou k identifikaci uživatele.

## 3. Efektivita při vyhledávání

Při porovnávání obrázků je nutné znovu a znovu provádět detekci obličeje a extrakci vektorů, což je časově náročný proces. Naopak, pokud máme všechny obličejové vektory uložené v paměti, můžeme je porovnávat hromadně a okamžitě, což výrazně zvyšuje efektivitu systému.

## 4. Zabezpečení

Uložení vektorů namísto obrázků přispívá k většímu zabezpečení. Vektory nelze snadno převést zpět na původní obrázek, což zvyšuje ochranu soukromí uživatelů.

## Závěr

Z těchto důvodů je porovnávání obličejových vektorů ideální volbou pro efektivní a rychlé rozpoznávání obličejů v našem projektu. Umožňuje nám optimalizovat výkon a efektivitu, což je klíčové pro budoucí rozvoj systému.
