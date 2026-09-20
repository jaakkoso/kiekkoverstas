#!/usr/bin/env python3
"""Lataa Damon Rinardin Spocalc-taulukon ja poimii vanne- ja napatiedot.

Kirjoittaa: data/spocalc-rims.json, data/spocalc-hubs.json
Lahde: https://www.sheldonbrown.com/rinard/spocalc.htm
"""
import datetime, io, json, os, re, urllib.request, zipfile
from xml.etree import ElementTree as ET

URL = "https://www.sheldonbrown.com/rinard/spocalc-2022a.xlsm"
M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")


def sheet_rows(z, shared, path):
    sh = ET.fromstring(z.read(path))
    out = []
    for row in sh.iter(M + "row"):
        cells = {}
        for c in row.iter(M + "c"):
            col = re.match(r"[A-Z]+", c.get("r")).group(0)
            t, v, inl = c.get("t"), c.find(M + "v"), c.find(M + "is")
            if t == "s" and v is not None:
                val = shared[int(v.text)]
            elif inl is not None:
                val = "".join(x.text or "" for x in inl.iter(M + "t"))
            elif v is not None:
                val = v.text
            else:
                val = None
            if val is not None:
                cells[col] = val
        out.append((int(row.get("r")), cells))
    return out


def num(x):
    try:
        return round(float(x), 2)
    except (TypeError, ValueError):
        return None


def year(serial):
    try:
        d = datetime.date(1899, 12, 30) + datetime.timedelta(days=int(float(serial)))
        return d.year
    except (TypeError, ValueError):
        return None


def main():
    print("Ladataan", URL)
    raw = urllib.request.urlopen(URL, timeout=60).read()
    z = zipfile.ZipFile(io.BytesIO(raw))
    ss = ET.fromstring(z.read("xl/sharedStrings.xml"))
    shared = ["".join(t.text or "" for t in si.iter(M + "t")) for si in ss]

    # sheet3 = rims, sheet4 = hubs (tarkista workbook.xml jos jarjestys muuttuu)
    rims, seen = [], set()
    for r, c in sheet_rows(z, shared, "xl/worksheets/sheet3.xml"):
        if r < 9 or "E" not in c:
            continue
        erd, name = num(c.get("A")), (c.get("E") or "").strip()
        if erd is None or not name or not 200 < erd < 720:
            continue
        key = (name.lower(), erd)
        if key in seen:
            continue
        seen.add(key)
        iso = (c.get("D") or "").strip()
        rims.append({"n": name, "e": erd, "o": num(c.get("B")) or 0,
                     "sz": (c.get("C") or "").strip(), "iso": iso,
                     "y": year(c.get("F")), "by": (c.get("G") or "").strip()})

    hubs, seen = [], set()
    for r, c in sheet_rows(z, shared, "xl/worksheets/sheet4.xml"):
        if r < 10 or "I" not in c:
            continue
        dl, wl, dr, wr = (num(c.get(k)) for k in "BCDE")
        name = (c.get("I") or "").strip()
        if None in (dl, wl, dr, wr) or not name:
            continue
        if not (10 < dl < 120 and 10 < dr < 120 and 3 < wl < 90 and 3 < wr < 90):
            continue
        key = (name.lower(), dl, wl, dr, wr, c.get("H"))
        if key in seen:
            continue
        seen.add(key)
        hubs.append({"n": name, "dl": dl, "wl": wl, "dr": dr, "wr": wr,
                     "s": num(c.get("A")) or 2.6, "fr": (c.get("F") or "").strip(),
                     "old": num(c.get("H")), "cogs": (c.get("G") or "").strip(),
                     "y": year(c.get("J")), "by": (c.get("K") or "").strip()})

    json.dump(rims, open(os.path.join(DATA, "spocalc-rims.json"), "w"), ensure_ascii=False)
    json.dump(hubs, open(os.path.join(DATA, "spocalc-hubs.json"), "w"), ensure_ascii=False)
    print("Tallennettu", len(rims), "vannetta ja", len(hubs), "napaa")


if __name__ == "__main__":
    main()
