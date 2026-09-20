#!/usr/bin/env python3
"""Hakee spokecalculator.app -tietokannan sivutetut taulukot.

Kirjoittaa: data/spokecalculator-rims.json, data/spokecalculator-hubs.json
Lahde: https://spokecalculator.app/hubs/ ja /rims/
"""
import html, json, os, re, time, urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
UA = {"User-Agent": "Mozilla/5.0 (kiekkoverstas data sync)"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "ignore")


def parse(page):
    body = page[page.find('<tbody id="db-rows">'):]
    body = body[:body.find("</tbody>")]
    rows = []
    for _rid, tr in re.findall(r'<tr[^>]*data-record-id="(\d+)"(.*?)</tr>', body, re.S):
        model = re.search(r"data-listing-model[^>]*>(.*?)</a>", tr, re.S)
        vals = re.findall(r'data-label="([^"]+)"><span data-listing-value>(.*?)</span>', tr, re.S)
        rec = {html.unescape(k): html.unescape(re.sub(r"<[^>]+>", "", v)).strip() for k, v in vals}
        rec["_model"] = html.unescape(re.sub(r"<[^>]+>", "", model.group(1))).strip() if model else ""
        date = re.search(r"Record version/date:\s*([0-9-]+)", tr)
        rec["_date"] = date.group(1) if date else ""
        rows.append(rec)
    return rows


def crawl(kind):
    first = get("https://spokecalculator.app/%s/" % kind)
    pages = sorted({int(n) for n in re.findall(r"/%s/page/(\d+)/" % kind, first)})
    rows = parse(first)
    for p in pages:
        time.sleep(0.4)
        rows += parse(get("https://spokecalculator.app/%s/page/%d/" % (kind, p)))
        print("  sivu", p, "->", len(rows), "rivia")
    return rows


def main():
    for kind, out in (("hubs", "spokecalculator-hubs.json"), ("rims", "spokecalculator-rims.json")):
        print("Haetaan", kind)
        rows = crawl(kind)
        json.dump(rows, open(os.path.join(DATA, out), "w"), ensure_ascii=False)
        print("Tallennettu", len(rows), "->", out)


if __name__ == "__main__":
    main()
