# Kiekkoverstas

Yhden tiedoston websovellus polkupyörän kiekon kasaukseen ja rihtaukseen.
Suomenkielinen, toimii selaimessa ilman palvelinta ja ilman verkkoyhteyttä.

**Julkaistu osoitteessa:** https://claude.ai/artifact/8kw9SKdeSHxVBzj6pLWfkF

## Avaaminen

Avaa `kiekkoverstas.html` selaimeen — kaksoisklikkaus riittää. Kaikki toiminta
on tiedoston sisällä: ei asennusta, ei riippuvuuksia, ei verkkopyyntöjä
lukuun ottamatta Google Fontsin kahta kirjasinta.

## Mitä sovellus tekee

| Välilehti | Sisältö |
|---|---|
| 1 · Mitat ja pinnanpituus | Pinnanpituuslaskuri, kireyssuhde, pinnoituskaavio, pinnan valinta, komponenttihaku |
| 2 · Pinnoitus | 13-vaiheinen rastitettava ohje, joka mukautuu pinnalukuun ja ristilukuun |
| 3 · Rihtaus | Heittomittaus, heittoprofiili kiekkona, paikkakohtainen korjaussuunnitelma |
| 4 · Kireysmittaus | Pinnankireyden syöttö, kaksi kiekkonäkymää, poikkeama-analyysi, korjausohjeet |
| 5 · Viimeistely | Tarkistuslista ja valmiin kiekon mittarajat |
| 6 · Tietokanta | 4140 komponenttia haettavana, omat mittaukset, pinnataulukko |
| Projektit | Useita kiekkoja rinnakkain, automaattitallennus, muistiinpanot, varmuuskopio |

### Laskenta

Pinnanpituus lasketaan vakiokaavalla

    L = sqrt(R² + r² + f² − 2·R·r·cos α) − s/2

jossa `R` = ERD/2, `r` = laipan halkaisija/2, `f` = keskiöstä laippaan,
`α` = 720 × ristiluku / pinnaluku ja `s` = laipan pinnareiän halkaisija.
Epäsymmetrinen vanne siirtää tehollisia laippaetäisyyksiä (`f ± offset`).

Puolten kireyssuhde tulee sivuttaisvoimien tasapainosta:
`T_vasen / T_oikea ≈ (f_oikea / L_oikea) / (f_vasen / L_vasen)`.

### Tallennus ja synkronointi

Kaikki tila elää selaimen `localStorage`-muistissa avaimilla, jotka alkavat
`kv.`. Projektinvaihto kopioi avaimet projektin omaan lokeroon ja takaisin.
Laitekohtaisia (projektien ulkopuolisia) avaimia ovat `kv.own`, `kv.tab`,
`kv.projects`, `kv.active`, `kv.tmview`, `kv.theme`, `kv.vspeak` sekä kaikki
`kv.sync.*`-avaimet.

Ilman synkronointia tiedot ovat vain siinä selaimessa, jolla niitä käytettiin.

**Synkronointi GitHubiin** (Projektit → Synkronointi GitHubiin) tallentaa
projektit ja omat komponenttimittaukset salaiseen gistiin käyttäjän
GitHub-tilille. Jokaiseen selaimeen liitetään kerran GitHub-avain, jolla on
pelkkä `gist`-oikeus. Avain pysyy selaimen muistissa (`kv.sync.token`) eikä
koskaan päädy projekteihin, varmuuskopioon tai gistiin.

- Synkronointi käynnistyy muutama sekunti muutoksen jälkeen, sovellukseen
  palatessa ja sovellusta suljettaessa.
- Yhdistäminen tehdään projekteittain muokkausajan mukaan. Jos samaa
  projektia on muokattu kahdella laitteella edellisen synkronoinnin jälkeen,
  uudempi jää voimaan ja toinen tallennetaan kopiona laitteen nimellä —
  mitään ei hävitetä.
- Poistetut projektit merkitään hautakivellä, jotta ne eivät palaa toiselta
  laitteelta.
- Salainen gist ei näy hauissa eikä profiilissa, mutta sen osoitteen
  tietävä voi lukea sen.
- claude.ai-artifactissa synkronointi on estetty; se toimii GitHub Pages
  -osoitteessa.

## Kansion rakenne

    kiekkoverstas.html      Sovellus. Tämä on ainoa tiedosto jota tarvitset.
    stitch-brief.md         Design-brief Google Stitchille tai muulle työkalulle.
    data/
      builtin.js            Komponenttitietokanta tiivistettynä (upotettu sovellukseen).
      spocalc-rims.json     Välivaiheen data, Spocalc.
      spocalc-hubs.json
      spokecalculator-rims.json   Välivaiheen data, spokecalculator.app.
      spokecalculator-hubs.json
      LAHTEET.md            Mistä luvut ovat peräisin ja mitä niistä pitää tietää.
    tools/
      1_hae_spocalc.py            Lataa ja purkaa Spocalc-taulukon.
      2_hae_spokecalculator.py    Hakee spokecalculator.app -tietokannan.
      3_kokoa_tietokanta.py       Yhdistää lähteet -> data/builtin.js
      4_paivita_sovellus.py       Vaihtaa builtin.js:n sovelluksen sisään.

## Tietokannan päivittäminen

    python3 tools/1_hae_spocalc.py
    python3 tools/2_hae_spokecalculator.py
    python3 tools/3_kokoa_tietokanta.py
    python3 tools/4_paivita_sovellus.py

Vain Python 3:n vakiokirjasto, ei asennettavia paketteja. Vaiheet 1 ja 2
tarvitsevat verkkoyhteyden; 3 ja 4 toimivat talletetulla datalla.
Skriptit poistavat kaksoiskappaleet nimen ja mittojen perusteella, mutta
säilyttävät saman mallin eri lähteistä jos lukemat poikkeavat.

## Tekninen rakenne

Yksi HTML-tiedosto: `<title>`, `<style>`, seitsemän `<section>`-välilehteä ja
yksi `<script>`, jonka sisällä koko logiikka on yhdessä IIFE:ssä. Ei
rakennusvaihetta, ei kehyksiä. Kaaviot piirretään SVG:nä suoraan merkkijonoina.

Teemat tulevat CSS-muuttujista: vaalea `:root`-lohkossa, tumma
`prefers-color-scheme`-kyselyssä ja `[data-theme="dark"]`-valitsimessa.
Jokainen väri määritellään vaaleassa lohkossa ensin.

## Muokkaaminen

Sovellus on tarkoituksella yksi tiedosto, jotta sen voi kopioida muistitikulle
tai lähettää sähköpostilla. Jos muokkaat sitä, pidä `BUILTIN`-rivi omana
rivinään — `tools/4_paivita_sovellus.py` etsii sen `var BUILTIN={r:` -alusta
ja korvaa rivin loppuun asti.
