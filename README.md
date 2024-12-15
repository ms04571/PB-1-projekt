# PB-1-projekt


Dve glavni tabeli serija in epizoda kjer bodo vse serije in njihove epizode.
Te bodo vse imele svoje Id-je in bile med seboj povezane.
Serije bodo povezanje z tebelo ocen (mogoče bodo tudi posamezne epizode
imele svoje ocene).
Serije bodo povezane z tabelo oseb kjer bodo igralci in direktorji
(mogoče tudi pisatelji). lahko da bodo tudi posamezne epizode bile povezane
z tabelo oseb.

serija: id, začetno leto, končno leto, jezik, naslov
epizoda: id, id serije, sezona, epizoda, naslov, čas
ocena: id serije ali epizode, povprečje, število glasov
osebe: id, id serije ali epizode, kategorija zaposlitve, karakterji


![ERdiagram](https://github.com/user-attachments/assets/9214e5b5-f5d6-4175-be74-01bbe75d4d99)
