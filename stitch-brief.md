# Design-brief Google Stitchille

Liitä alla oleva brief kokonaisuudessaan ensimmäiseen viestiin, mutta pyydä
siltä vain **kireysmittausnäyttö**. Kun suunta on kohdallaan, jatka briefin
lopun järjestyksessä yksi näyttö kerrallaan — muuten työkalu tasapäistää
kaikki näytöt samaan muottiin.

Brief on englanniksi, koska nämä työkalut tuottavat sillä parempaa jälkeä.
Käyttöliittymän tekstit pysyvät suomena: sanasto on briefin sisällä.

---

PROJECT BRIEF — "Kiekkoverstas" (Finnish for "wheel workshop")

WHAT IT IS
A single-page web app for building and truing bicycle wheels by hand. Not a
consumer app, not a marketing site: a working instrument that sits open on a
bench for hours. It calculates spoke lengths, guides the lacing sequence,
diagnoses runout, analyses spoke tension, and keeps each wheel as a saved
project.

WHO USES IT AND HOW
Bicycle mechanics and serious home wrenchers. The user is standing at a truing
stand with a wheel spinning in front of them. One hand holds a spoke wrench or
a tension meter; the other taps the screen. Fingers are often greasy. The room
may be a dim garage or a bright shop.

Two device contexts, both first-class:
- Laptop or tablet on the bench, next to the stand. Primary.
- Phone propped against the stand. Frequent. Must be genuinely usable at 390px
  wide — not merely "responsive", but designed for that width.

Sessions are interrupted constantly. A wheel build can span three evenings.
The design must make "where was I?" answerable in one glance.

THE SEVEN SCREENS

1. MITAT JA PINNANPITUUS — Measurements & spoke length
   Input: rim ERD, rim offset, spoke count, cross count per side, hub flange
   diameters (left/right), centre-to-flange (left/right), flange hole diameter.
   A search field that queries a 4140-component database and fills the fields.
   A spoke-model picker (23 models: DT Swiss, Sapim, Pillar, generic gauges).
   Output: two spoke lengths to 0.1 mm, tension ratio between sides, warnings.
   A top-down lacing diagram drawn from the entered values.

2. PINNOITUS — Lacing
   A 13-step checklist that adapts to the spoke and cross count. Progress bar.
   Steps get struck through when done. Below: common mistakes as short essays.

3. RIHTAUS — Truing
   Runout measurement: two rows of 8-36 signed millimetre values (lateral and
   radial) taken around the rim. A circular runout profile: lateral as radial
   bars on an outer ring, rim roundness as a closed curve on an inner ring.
   A correction plan: an ordered list naming specific spokes and turn amounts.
   Plus a quick advisor with a direction selector and a magnitude slider.

4. KIREYSMITTAUS — Tension measurement
   A grid of 8-20 small number fields per wheel side, filled while holding a
   tension meter. Cells colour themselves by deviation as you type.
   THE CENTREPIECE: two circular wheel diagrams side by side, drive side and
   non-drive side. Each spoke is a bar at its true angular position. The
   dashed circle is the side's mean. Bars point outward when tight, inward
   when loose. A green band marks +/-10%. Valve position at 12 o'clock.
   Below: statistics, a verdict chip, and a prioritised correction list.
   Also a calibration card where the user types 2-4 points from their own
   meter's conversion chart.

5. VIIMEISTELY — Finishing
   A second checklist, a tolerance table, closing advice.

6. TIETOKANTA — Component database
   Search across 2035 rims and 2105 hubs. Filter chips by wheel size and by
   front/rear. Result rows carry name, dimensions, data source and year.
   The user's own measurements appear first and are visually distinct.
   Plus a reference table of 23 spoke models and a backup text area.

7. PROJEKTIT — Projects
   A list of saved wheels. Each shows a name, a one-line summary of its state
   ("32 spokes / 3-cross / ERD 602 - lacing 8/13 / 24 tension readings"), and
   when it was last touched. Free-text notes per project. Autosave, with a
   save indicator in the header.

A persistent header carries the app name, the active project name as an
editable field, the save status, and navigation between the seven screens.

THE DESIGN PROBLEMS WORTH SOLVING
These are where the work matters. Treat them as the brief, not as details.

a) The circular diagrams are the soul of this app. Four of them: the lacing
   pattern, two tension wheels, one runout profile. They should read as
   precision instruments, not as infographics. How do they stay legible at
   390px? How do the two tension wheels read as a pair without becoming
   symmetrical wallpaper? What happens to the space in the middle?

b) Entering twenty numbers in a row, one-handed, while a wheel spins. The grid
   must be fast to move through, obvious about where you are, and it must tell
   you something the moment a value lands. How small can a field be before it
   stops being tappable with a dirty thumb?

c) Severity has three levels everywhere — fine, watch, fix — and it appears in
   cells, chips, bars, rings and list rows. Find an encoding that survives at
   both 12px and 400px, works for colour-blind users, and never looks like a
   traffic light bolted onto a grey box.

d) An interrupted build. The user returns after four days. What do they see
   first, and what tells them where they stopped?

e) Advice lists. Sentences like "Spoke right 8 is 18% looser than the drive
   side average — turn the nipple clockwise 1/2 turn and check lateral true."
   These are instructions to act on while looking away from the screen. How do
   they get typeset so the actionable part survives a glance?

CONSTRAINTS THAT ARE NOT NEGOTIABLE
- All interface copy in Finnish. Glossary below.
- Full light and dark themes, both designed, neither an inversion of the other.
  The garage is dark; the shop is bright.
- Every measurement uses tabular figures. Columns of numbers must align.
- Measurement grid targets at least 44px tall.
- Dense by intent. This is a tool for someone who wants all of it visible.
  Do not hide function behind progressive disclosure to look calmer.
- No imagery of bicycles, no stock photography, no illustration of a cyclist.
  The only pictures are the diagrams, and they are made of data.

FINNISH GLOSSARY — use these exact terms
  kiekko = wheel          vanne = rim              napa = hub
  pinna = spoke           nippa = nipple           laippa = flange
  rihtaus = truing        sivuheitto = lateral runout
  korkeusheitto = radial runout                    keskitys = dish
  kireys = tension        vetopuoli = drive side
  vapaapuoli = non-drive side                      pinnoitus = lacing
  ristiluku = cross count ERD = efektiivinen kehähalkaisija
  venttiiliaukko = valve hole                      kgf = kilogram-force

WHAT I DO NOT WANT — these are the current defaults of AI-generated interfaces
and I will reject anything that lands in them:
- Warm cream backgrounds with a serif display face and a terracotta accent.
- Near-black canvas with a single acid-green or vermilion highlight.
- Purple-to-blue gradients, anywhere, for anything.
- Inter or Space Grotesk chosen because they are safe.
- Emoji as section markers or status icons.
- Every block a rounded card with the same border, radius and shadow, so that
  nothing has more weight than anything else.
- A coloured accent bar down the left edge of every card.
- Big centred hero areas. The first screen should open into work.
- Generic dashboard KPI tiles with a big number and a tiny green arrow.
- Numbered eyebrow labels (01 / 02 / 03) on content that is not a sequence.

WHERE YOU HAVE ROOM
Choose the visual direction yourself and commit to it. Three provocations you
may take, combine or throw out:
  — PRECISION INSTRUMENT: the vocabulary of a dial gauge and a vernier scale.
    Engraved rules, hairlines, a single machined accent, typography that
    behaves like an instrument face.
  — WORKSHOP PRINT: the parts catalogue and the exploded diagram. Flat ink,
    strong numerals, technical drawing conventions used as real structure.
  — NORDIC UTILITY: light, quiet, generous white space, one confident colour,
    everything earning its place. Restraint as the statement.
Or propose a fourth that fits a Finnish bicycle workshop better than any of
these. Pick typefaces deliberately and say why. Decide where the one bold
move goes and keep everything else quiet around it.

DELIVERABLES
1. The tension measurement screen (4), desktop and mobile, light and dark.
   This is the screen to design first and hardest — the two circular wheel
   diagrams are the identity of the whole product.
2. The measurement & spoke length screen (1), desktop and mobile.
3. The truing screen (3) with the runout profile.
4. The projects screen (7) and the header, showing the interrupted-build case.
5. The component database screen (6) with search and filter chips.
6. A token and component sheet: colours for both themes, type scale, spacing,
   the severity encoding, form controls, chips, list rows, and the shared
   anatomy of the circular diagrams.

SUGGESTED ORDER
Give me the tension screen first and let me react before you continue. Then
screen 1, then 3, then the header and projects, then the database, then the
token sheet once the language has settled.
