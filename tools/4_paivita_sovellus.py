#!/usr/bin/env python3
"""Korvaa kiekkoverstas.html:n sisalla olevan BUILTIN-tietokannan
data/builtin.js:n sisallolla. Aja 3_kokoa_tietokanta.py ensin."""
import os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(HERE, "kiekkoverstas.html")
DB = os.path.join(HERE, "data", "builtin.js")

src = open(APP, encoding="utf-8").read()
data = open(DB, encoding="utf-8").read().strip()

start = src.find("var BUILTIN={r:")
if start < 0:
    sys.exit("BUILTIN-lohkoa ei loytynyt tiedostosta " + APP)
end = src.index("\n", src.index("};\n", start))

open(APP, "w", encoding="utf-8").write(src[:start] + data + src[end:])
print("Paivitetty", APP, "->", len(data), "tavua tietokantaa")
