"""Holt die Maschinen-Grafik (Marketing-Trichter) aus story6/maas_strukturbild.py in story7.11tydata.json.
Die Farben der Grafik setzt die Seite per CSS über die Stellschrauben (Attribut-Selektoren), die Grafik selbst bleibt unverändert."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "story6"))
import maas_strukturbild  # noqa: E402

p = os.path.join(HERE, "story7.11tydata.json")
d = json.load(open(p, encoding="utf-8"))
d["s7"]["maschine"] = maas_strukturbild.marketing_svg()
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(p, "a").write("\n")
print("Maschine übernommen")
