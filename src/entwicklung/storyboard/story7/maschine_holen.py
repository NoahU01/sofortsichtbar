"""Holt die Maschinen-Grafik (Marketing-Trichter) aus story6/maas_strukturbild.py in story7.11tydata.json.
Die Farben der Grafik setzt die Seite per CSS über die Stellschrauben (Attribut-Selektoren), die Grafik selbst bleibt unverändert."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "story6"))
import maas_strukturbild  # noqa: E402

p = os.path.join(HERE, "story7.11tydata.json")
d = json.load(open(p, encoding="utf-8"))
svg = maas_strukturbild.marketing_svg()
# Alles, was auf dem Akzent steht (Kern des Trichters, Punkte, Rückweg-Band), bekommt die Klasse s7-kern –
# so kann die Seite die Schrift dort per Stellschraube umfärben (z. B. weiß auf vollflächiger Farbe).
import re
svg = svg.replace('<g transform="translate(48 172)', '<g class="s7-kern" transform="translate(48 172)', 1)
svg = re.sub(r'<text ([^>]*)>(Baustein 1|Kernpaket|sofort sichtbar|Sichtbarkeit pflegt[^<]*)</text>', r'<text class="s7-kern" \1>\2</text>', svg)
svg = re.sub(r'<circle ([^>]*r="4.2" fill="#1a1817"[^>]*)/>', r'<circle class="s7-kern" \1/>', svg)
assert svg.count('class="s7-kern"') >= 7, svg.count('class="s7-kern"')
d["s7"]["maschine"] = svg
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(p, "a").write("\n")
print("Maschine übernommen")
