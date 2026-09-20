# Lähteet

Tietokannassa on 2035 vannetta ja 2105 napaa. Jokainen rivi kantaa lähteensä
ja vuotensa, ja ne näkyvät sovelluksessa hakutuloksen alla.

## spokecalculator.app — 1053 vannetta, 1251 napaa

https://spokecalculator.app/hubs/ ja https://spokecalculator.app/rims/

Käsin tarkistettu tietokanta, joka on sulauttanut itseensä myös Freespoken
(kstoerz.com/freespoke) arkiston. Painottuu nykykalustoon: DT Swiss 350 ja 240
kaikilla akselistandardeilla, Hope Pro 4 ja Pro 5, Shimanon nykysarjat, Chris
King, Onyx, Industry Nine, Novatec, Bitex, SON-dynamot. Merkitsee myös
liitäntätyypin, joten suoravetonavat on erotettu ja merkitty sovelluksessa
`[suoraveto]`.

## Spocalc — 726 vannetta, 583 napaa

https://www.sheldonbrown.com/rinard/spocalc.htm

Damon Rinardin ylläpitämä kiekonrakentajien taulukko vuodesta 1997, jaossa
Sheldon Brownin sivustolla. Kattaa 1990- ja 2000-luvun kaluston, jota yhä
korjataan: Rigida, Araya, Mavic, Wolber, Ambrosio, Fiamme, Sachs, Suntour,
Ringlé, Matrix. Monessa rivissä on alkuperäinen lähdeviite valmistajan
sivulle, ja ne on säilytetty lähdenimenä (Mavic, Rigida, Araya, DT Swiss…).

## BikeGremlin — 6 vannetta, 24 napaa

https://bike.bikegremlin.com/9519/hub-data/
https://bike.bikegremlin.com/9503/erd-data/

Itse mitattuja arvoja, erityisesti Shimanon vaihde- ja dynamonapoja, joita
muista lähteistä ei löydy.

## Mitä luvuista pitää tietää

**Sama malli voi esiintyä kahdesti eri lukemilla.** Esimerkiksi DT Swiss
EX 511 29" on yhdessä lähteessä 601 mm ja toisessa 607 mm. Näitä ei ole
yhdistetty eikä valittu puolesta: katso lähde ja vuosi ja valitse se, joka
vastaa omaa yksilöäsi.

**Vanteen ERD vaihtelee.** Valmistuserien välillä tyypillisesti 1–2 mm, ja
vuosimallin vaihtuessa enemmän. Tietokannan luku on lähtökohta, ei tilausperuste.
Sovellus varoittaa tästä aina kun vanne ladataan tietokannasta.

**Navan mitat ovat vakaampia** kuin vanteen, mutta samakin mallinimi voi
tarkoittaa eri vuosina eri laippamittoja. Akselistandardi (OLD) on
tunnistamisen paras apu.

**Suoravetonavat.** Sovelluksen laskukaava olettaa J-mutkapinnat. Suoraveto-
navoissa pinnan pituus mitataan eri referenssistä, joten käytä niille navan
valmistajan omaa laskuria.

**Mittaa itse, kun voit.** Ohjeet ERD:n, laipan halkaisijan ja keskiöetäisyyden
mittaamiseen ovat sovelluksen välilehdellä 1. Omat mittaukset tallentuvat
sovelluksen omaan kirjastoon ja nousevat hakutuloksissa ensimmäisiksi.

## Pinnatiedot

Sovelluksen 23 pinnamallin mitat ovat valmistajien ilmoittamia nimellismittoja
(DT Swiss, Sapim, Pillar) sekä yleisiä mittaluokkia 13G–14/17G. Ne on kirjoitettu
suoraan sovellukseen, eivät tässä kansiossa olevaan tietokantaan.
