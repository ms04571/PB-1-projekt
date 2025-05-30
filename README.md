# PB-1-projekt




V tabeli "naslovi" bodo vsebovane tako serije kot epizode. Povezovala jih bo povezovalna tabela "epizode". V tabeli naslovi se nahaja id naslova (oblike tt123456), tip (serija/epizoda), naslov, končno in začetno leto ter čas trajanja. Vsak naslov bo imel tudi oceno v tabeli Ocene. Vsak naslov bo lahko imel do 3 žanre v tabeli "zanr".


naslov: id, tip, naslov, začetno leto, končno leto, čas 
epizode: id epizode, id serije, sezona, epizoda
ocena: id naslova, povprečje, število glasov
zanr: id, žanr


![ERdiagram](https://github.com/user-attachments/assets/97fb5ab2-836e-4925-86ff-a977c659687d)




Če se hoče ustvariti bazo je potrebno v ta imenik vstaviti še 3 dodatne datoteke.
To je potrebno zato, ker so datoteke prevelike, da bi jih shranil na github.
Na strani https://datasets.imdbws.com/ je potrebno prenesti naslednje datoteke:
- title.basics.tsv.gz
- title.episode.tsv.gz
- title.ratings.tsv.gz

Po tem jih je treba ekstrahirati in vstaviti datoteke title.basics.tsv, title.episode.tsv, title.ratings.tsv
v imenik v katerem se nahaja program ustvari.py. Šele potem lahko uspešno zaženeš program ustvari.py.








Funkcionalnosti:
Baza je bila namenjena za brskanje TV serij.
V tekstovnem vmesniku je možno:
- Iskanje po nasloivu
- Iskanje po enem žanru.
- Prikaz 10 najboljših serij po oceni
- Ogled vseh podatkov o iskani seriji
- Ogled vseh epizod serije ali pa najboljših 10 po oceni
- Ogled vseh podatkov o epizodi seriji

V spletnem vmesniku je možno bolj natančno iskanje. In sicer za vsak podatek serije se lahko na strani prilagodijo filtri, ki se potem uporabijo za iskanje serij oz. serije. Podobno kot pri tekstovnem vmesniku je za vsako serijo in epizodo možno ogledat vse njihove podatke.
