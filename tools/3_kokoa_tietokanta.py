#!/usr/bin/env python3
"""Yhdistaa lahteet yhdeksi tiivistetyksi JS-tietokannaksi.

Lukee:   data/spocalc-*.json, data/spokecalculator-*.json
Kirjoittaa: data/builtin.js

Muoto:
  BUILTIN.r = [nimi, ERD, offset, ISO, vuosi, lahde]
  BUILTIN.h = [nimi, vasen laippa, vasen keskio, oikea laippa, oikea keskio,
               pinnareika, E/T, OLD, vuosi, lahde]
"""
import json, os, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
load = lambda n: json.load(open(os.path.join(DATA, n), encoding="utf-8"))

# BikeGremlin, itse mitatut nykymallit (bike.bikegremlin.com/9519/hub-data/)
BIKEGREMLIN_HUBS = [
    ("Shimano FH-M8000-3D XT", "R", 44, 35.3, 45, 22.1, 2.6),
    ("Shimano FH-M7110-B Microspline 12-v, 12 mm", "R", 60, 35.5, 61, 22, 2.6),
    ("Shimano FH-M475 6-pulttinen levyjarru", "R", 61, 34, 61, 21, 2.6),
    ("Shimano FH-M3050 Acera Centerlock 135", "R", 45, 33, 45, 20, 2.6),
    ("Shimano FH-M4050 Alivio Centerlock 135 (32r)", "R", 45, 33.5, 45, 21, 2.6),
    ("Shimano FH-M4050 Alivio Centerlock 135 (36r)", "R", 45, 33, 45, 19.5, 2.6),
    ("Shimano FH-RM30 Altus", "R", 45, 35, 45, 24, 2.6),
    ("Shimano FH-RS300 Sora", "R", 45, 35, 45, 19, 2.6),
    ("Shimano FH-M425", "R", 61, 31.5, 61, 17, 2.6),
    ("Shimano HB-RS300 Sora", "F", 38, 33, 38, 33, 2.6),
    ("Shimano HB-7710 Dura-Ace rata", "F", 38, 37, 38, 37, 2.5),
    ("Shimano HB-7600 Dura-Ace rata", "F", 67, 36, 67, 36, 2.5),
    ("Shimano DH-3D32-QR dynamonapa", "F", 74, 20, 74, 28, 2.6),
    ("Shimano DH-3D37-QR dynamonapa", "F", 74, 20, 74, 28, 2.6),
    ("Shimano DH-3N20 dynamonapa", "F", 74, 29, 74, 27, 2.6),
    ("Shimano DH-C3000-3N-NT dynamonapa", "F", 74, 30, 74, 27.5, 2.6),
    ("Shimano DH-T8000-3D XT dynamo, levyjarru", "F", 70, 18.5, 70, 26.5, 2.6),
    ("Shimano SG-3C41 Nexus 3-v vaihdenapa", "R", 59, 28, 59, 25, 2.6),
    ("Shimano SG-7C15 Nexus 7-v vaihdenapa", "R", 84, 31, 84, 21, 2.6),
    ("Shimano SG-8R31 Nexus 8-v vaihdenapa", "R", 92.5, 29.3, 92.5, 24.5, 2.6),
    ("Shimano WH-MT15-A Centerlock 135", "R", 45.5, 34, 45.5, 20, 2.6),
    ("Quando 6-pulttinen levyjarrunapa", "F", 68, 23, 68, 30, 2.8),
    ("Quando 6-pulttinen levyjarru, vapaarumpu", "R", 66, 33.5, 66, 21.5, 2.8),
    ("Velosteel jarrunapa 117 mm", "R", 52, 30, 52, 33, 2.9),
]
BIKEGREMLIN_RIMS = [
    ("DT Swiss PR 1600 Spline levyjarru", 576, "622"),
    ("Giant AM29", 598, "622"),
    ("H Plus Son TB14 700C", 612, "622"),
    ("Madux RS 3.0 700C", 602, "622"),
    ("Shimano MT15 584x19c", 563, "584"),
    ("Alexrims TD24 26\"", 546, "559"),
]

SRC_MAP = [("dtswiss", "DT Swiss"), ("mavic", "Mavic"), ("rigida", "Rigida"),
           ("araya", "Araya"), ("chrisking", "Chris King"), ("velocity", "Velocity"),
           ("amclassic", "American Classic"), ("sunrims", "Sun"), ("wtb", "WTB"),
           ("alexrims", "Alex"), ("campagnolo", "Campagnolo"), ("ritchey", "Ritchey"),
           ("zipp", "Zipp"), ("salsa", "Salsa"), ("surly", "Surly"),
           ("phil", "Phil Wood"), ("shimano", "Shimano"), ("bontrager", "Bontrager")]


def src_of(by):
    b = (by or "").lower()
    for key, name in SRC_MAP:
        if key in b:
            return name
    return "Spocalc"


def num(x):
    try:
        return round(float(str(x).replace(",", ".")), 2)
    except (TypeError, ValueError):
        return None


def split_pair(x):
    if not x or "/" not in x:
        return (None, None)
    a, b = x.split("/", 1)
    return (num(a), num(b))


def main():
    rims, hubs = [], []

    for r in load("spocalc-rims.json"):
        iso = r["iso"] if re.fullmatch(r"\d+", r["iso"] or "") else (r["iso"] or r["sz"])
        rims.append([r["n"], r["e"], r["o"], iso, r["y"] or 0, src_of(r["by"])])
    for h in load("spocalc-hubs.json"):
        fr = "R" if h["fr"].upper().startswith("R") else ("F" if h["fr"].upper().startswith("F") else "")
        hubs.append([h["n"], h["dl"], h["wl"], h["dr"], h["wr"], h["s"], fr,
                     h["old"] or 0, h["y"] or 0, src_of(h["by"])])

    for h in load("spokecalculator-hubs.json"):
        dl, dr = split_pair(h.get("Flange Ø (L/R)", ""))
        wl, wr = split_pair(h.get("Centre→flange (L/R)", ""))
        if None in (dl, dr, wl, wr):
            continue
        if not (10 < dl < 130 and 10 < dr < 130 and 3 < wl < 90 and 3 < wr < 90):
            continue
        name = h.get("_model", "").strip()
        if not name:
            continue
        if h.get("Interface") == "Straight-pull":
            name += " [suoraveto]"
        fr = "F" if h.get("Position") == "Front" else ("R" if h.get("Position") == "Rear" else "")
        hubs.append([name, dl, wl, dr, wr, num(h.get("Spoke hole")) or 2.6, fr,
                     num(h.get("OLN")) or 0, int(h.get("_date", "0")[:4] or 0),
                     "spokecalculator.app"])

    for r in load("spokecalculator-rims.json"):
        erd = num(r.get("ERD"))
        name = r.get("_model", "").strip()
        if erd is None or not name or not 200 < erd < 760:
            continue
        size = r.get("Size", "")
        m = re.search(r"ISO (\d+)", size)
        iso = m.group(1) if m else re.sub(r'[^0-9A-Za-z."/ ]', "", size)[:14]
        rims.append([name, erd, num(r.get("Offset")) or 0, iso,
                     int(r.get("_date", "0")[:4] or 0), "spokecalculator.app"])

    for name, fr, dl, wl, dr, wr, s in BIKEGREMLIN_HUBS:
        hubs.append([name, dl, wl, dr, wr, s, fr, 0, 2021, "BikeGremlin"])
    for name, erd, iso in BIKEGREMLIN_RIMS:
        rims.append([name, erd, 0, iso, 2022, "BikeGremlin"])

    norm = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
    key_r = lambda x: (norm(x[0]), round(x[1] * 2))
    key_h = lambda x: (norm(x[0]), round(x[1] * 2), round(x[2] * 2), round(x[3] * 2), round(x[4] * 2))

    def dedupe(rows, key):
        seen, out = set(), []
        for row in rows:
            k = key(row)
            if k not in seen:
                seen.add(k)
                out.append(row)
        return out

    rims = sorted(dedupe(rims, key_r), key=lambda x: x[0].lower())
    hubs = sorted(dedupe(hubs, key_h), key=lambda x: x[0].lower())

    js = ("var BUILTIN={r:" + json.dumps(rims, separators=(",", ":"), ensure_ascii=False) +
          ",h:" + json.dumps(hubs, separators=(",", ":"), ensure_ascii=False) + "};")
    open(os.path.join(DATA, "builtin.js"), "w", encoding="utf-8").write(js)
    print("Valmis:", len(rims), "vannetta,", len(hubs), "napaa,", len(js), "tavua")


if __name__ == "__main__":
    main()
