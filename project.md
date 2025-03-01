proces validace zamestnace pred kamerou

zamestnanec Franta si stoupne pred kameru
    - spusti se funkce na vektor obliceje
    - ziska se vektor obliceje
    - jakmile je ziskan vektor obliceje 
        udelat databazovy dotaz aby databaze vratila ID uzivatele podle vektoru
        Employee.objects.filter(vektor=inputvektor)

        nyni mame instanci objectu Franta

        zpristupni se NUMPAD pro zadani pinu.
        je to formular ktery vraci "POST" method

        overeni:  pokud pin je ok tak presmeruj na jiny template
                  pokud ne nejaka error message

    otazka je kde a jak provest overeni PINu jestli sedi s franta.pin v DB.

    ten POST method mam poslat na jiny endpoint? a tam spustit funkci
    jestli pinInput so rovna franta.pin tak jdi zpatky na hlavni stranku, ale nyni jiz s contextem PIN valid? 

        
        