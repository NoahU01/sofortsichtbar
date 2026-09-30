/**
 * Rechnet den Strategie-Graphen einmal beim Build durch.
 *
 * Damit bleiben die Templates dumm und alle Darstellungen teilen sich
 * dieselbe Wahrheit: Rang, Blockaden, Fortschritt und fertige Koordinaten
 * für die beiden gezeichneten Varianten (Graph und Liniennetz).
 */
import fs from "node:fs";

const roh = JSON.parse(fs.readFileSync("src/_data/strategie.json", "utf8"));

const nachId = new Map(roh.schritte.map((s) => [s.id, s]));
const istFertig = (id) => nachId.get(id).status === "erreicht";

/* --- Rang: längster Pfad von einem Startknoten ------------------------ */
const rang = new Map();
function rangVon(id, pfad = new Set()) {
  if (rang.has(id)) return rang.get(id);
  if (pfad.has(id)) throw new Error(`Zyklus im Strategie-Graphen bei "${id}"`);
  pfad.add(id);
  const vorher = nachId.get(id).braucht.map((b) => rangVon(b, pfad));
  pfad.delete(id);
  const wert = vorher.length ? Math.max(...vorher) + 1 : 0;
  rang.set(id, wert);
  return wert;
}
roh.schritte.forEach((s) => rangVon(s.id));

/* --- Anreichern -------------------------------------------------------- */
const schritte = roh.schritte.map((s) => {
  const offeneAbhaengigkeit = s.braucht.filter((b) => !istFertig(b));
  return {
    ...s,
    rang: rang.get(s.id),
    blockiertVon: offeneAbhaengigkeit,
    machbar: s.status !== "erreicht" && offeneAbhaengigkeit.length === 0,
    nachfolger: roh.schritte.filter((a) => a.braucht.includes(s.id)).map((a) => a.id),
    // Abhängigkeiten, die den Strang wechseln – nur die sind erklärungsbedürftig
    querBraucht: s.braucht.filter((b) => nachId.get(b).strang !== s.strang),
  };
});

const schrittNachId = new Map(schritte.map((s) => [s.id, s]));
const anteil = (liste) =>
  liste.length ? Math.round((liste.filter((s) => s.status === "erreicht").length / liste.length) * 100) : 0;

const straenge = roh.straenge.map((strang, i) => {
  const eigene = schritte.filter((s) => s.strang === strang.id);
  return { ...strang, spur: i, schritte: eigene, anzahl: eigene.length, fortschritt: anteil(eigene) };
});

const meilensteine = roh.meilensteine.map((m) => {
  const eigene = schritte.filter((s) => s.meilenstein === m.id);
  return {
    ...m,
    schritte: eigene,
    anzahl: eigene.length,
    fortschritt: anteil(eigene),
    erreicht: eigene.every((s) => s.status === "erreicht"),
  };
});

const aktuellerMeilenstein = meilensteine.find((m) => !m.erreicht) || meilensteine[meilensteine.length - 1];

/* Jeder Schritt trägt alles, was eine Darstellung über ihn braucht –
   die Templates sollen keine Nachschlage-Logik enthalten. */
const kurzform = (id) => {
  const s = schrittNachId.get(id);
  const strang = straenge.find((t) => t.id === s.strang);
  return { id: s.id, titel: s.titel, status: s.status, strangKurz: strang.kurz, farbe: strang.farbe };
};

const aufwandNamen = { S: "Klein (Stunden bis ein Tag)", M: "Mittel (mehrere Tage)", L: "Groß (Wochen)" };

schritte.forEach((s) => {
  const strang = straenge.find((t) => t.id === s.strang);
  const stein = meilensteine.find((m) => m.id === s.meilenstein);
  s.aufwandLabel = aufwandNamen[s.aufwand] || s.aufwand;
  s.strangLabel = strang.label;
  s.strangKurz = strang.kurz;
  s.farbe = strang.farbe;
  s.spur = strang.spur;
  s.meilensteinNr = stein.nr;
  s.meilensteinTitel = stein.titel;
  s.brauchtListe = s.braucht.map(kurzform);
  s.blockiertListe = s.blockiertVon.map(kurzform);
  s.nachfolgerListe = s.nachfolger.map(kurzform);
});

/* --- Kritischer Pfad: der längste Weg bis zum Ziel --------------------- */
const gewicht = { S: 1, M: 2, L: 3 };
const laengster = new Map();
function laengsterPfad(id) {
  if (laengster.has(id)) return laengster.get(id);
  const s = schrittNachId.get(id);
  let best = { kosten: 0, vorher: null };
  s.braucht.forEach((b) => {
    const v = laengsterPfad(b);
    if (v.kosten > best.kosten) best = { kosten: v.kosten, vorher: b };
  });
  const eintrag = { kosten: best.kosten + (gewicht[s.aufwand] || 1), vorher: best.vorher };
  laengster.set(id, eintrag);
  return eintrag;
}
schritte.forEach((s) => laengsterPfad(s.id));

let ende = schritte[0].id;
schritte.forEach((s) => {
  if (laengster.get(s.id).kosten > laengster.get(ende).kosten) ende = s.id;
});
const kritischerPfad = [];
for (let cur = ende; cur; cur = laengster.get(cur).vorher) kritischerPfad.unshift(cur);
const kritischSet = new Set(kritischerPfad);
schritte.forEach((s) => { s.kritisch = kritischSet.has(s.id); });

/* --- Layout 1: Graph nach Abhängigkeitsrang ---------------------------- */
const K = { breite: 196, hoehe: 92, spaltenLuft: 76, zeilenLuft: 18, spurLuft: 52 };

const maxRang = Math.max(...schritte.map((s) => s.rang));
const zelle = (r, spur) =>
  schritte.filter((s) => s.rang === r && straenge[spur].id === s.strang);

const spurStapel = straenge.map((_, spur) =>
  Math.max(1, ...Array.from({ length: maxRang + 1 }, (_, r) => zelle(r, spur).length))
);
const spurHoehe = spurStapel.map((n) => n * K.hoehe + (n - 1) * K.zeilenLuft);
const spurY = spurHoehe.map((_, i) => spurHoehe.slice(0, i).reduce((a, b) => a + b, 0) + i * K.spurLuft);

const graphKnoten = [];
for (let r = 0; r <= maxRang; r++) {
  straenge.forEach((strang, spur) => {
    zelle(r, spur).forEach((s, i) => {
      graphKnoten.push({
        id: s.id,
        x: r * (K.breite + K.spaltenLuft),
        y: spurY[spur] + i * (K.hoehe + K.zeilenLuft),
        breite: K.breite,
        hoehe: K.hoehe,
      });
    });
  });
}
const graphPos = new Map(graphKnoten.map((k) => [k.id, k]));
schritte.forEach((s) => {
  const p = graphPos.get(s.id);
  s.gx = p.x;
  s.gy = p.y;
});

const bogen = (a, b) => {
  const x1 = a.x + a.breite;
  const y1 = a.y + a.hoehe / 2;
  const x2 = b.x;
  const y2 = b.y + b.hoehe / 2;
  const dx = Math.max(36, (x2 - x1) / 2);
  return `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;
};

const graphKanten = schritte.flatMap((s) =>
  s.braucht.map((b) => ({
    von: b,
    nach: s.id,
    quer: nachId.get(b).strang !== s.strang,
    kritisch: kritischSet.has(b) && kritischSet.has(s.id),
    pfad: bogen(graphPos.get(b), graphPos.get(s.id)),
  }))
);

const graphSpalten = Array.from({ length: maxRang + 1 }, (_, r) => ({
  nr: r + 1,
  x: r * (K.breite + K.spaltenLuft),
  breite: K.breite,
  anzahl: schritte.filter((s) => s.rang === r).length,
}));

const graph = {
  knoten: graphKnoten,
  kanten: graphKanten,
  knotenBreite: K.breite,
  knotenHoehe: K.hoehe,
  querAnzahl: graphKanten.filter((k) => k.quer).length,
  spalten: graphSpalten,
  breite: (maxRang + 1) * (K.breite + K.spaltenLuft) - K.spaltenLuft,
  hoehe: spurY[spurY.length - 1] + spurHoehe[spurHoehe.length - 1],
  spuren: straenge.map((s, i) => ({
    id: s.id,
    label: s.label,
    farbe: s.farbe,
    y: spurY[i],
    hoehe: spurHoehe[i],
  })),
};

/* --- Layout 2: Liniennetz nach Meilensteinen --------------------------- */
// oben lässt Platz für die Stationsköpfe, damit sie nicht in den Linien liegen
const M = { halt: 176, station: 128, spurLuft: 122, oben: 168, links: 92, rechts: 92 };

const metroHalte = [];
const metroStationen = [];
let x = M.links;

meilensteine.forEach((m) => {
  const proStrang = straenge.map((strang) =>
    m.schritte.filter((s) => s.strang === strang.id).sort((a, b) => a.rang - b.rang)
  );
  const breiteste = Math.max(1, ...proStrang.map((l) => l.length));

  proStrang.forEach((liste, spur) => {
    // Halte mittig im Abschnitt verteilen, damit kurze Stränge nicht kleben
    const versatz = (breiteste - liste.length) / 2;
    liste.forEach((s, i) => {
      metroHalte.push({
        id: s.id,
        x: x + (versatz + i + 0.5) * M.halt,
        y: M.oben + spur * M.spurLuft,
      });
    });
  });

  x += breiteste * M.halt;
  metroStationen.push({
    id: m.id,
    nr: m.nr,
    titel: m.titel,
    ergebnis: m.ergebnis,
    erreicht: m.erreicht,
    fortschritt: m.fortschritt,
    x: x + M.station / 2,
  });
  x += M.station;
});

const metroPos = new Map(metroHalte.map((h) => [h.id, h]));
schritte.forEach((s) => {
  const p = metroPos.get(s.id);
  s.mx = p.x;
  s.my = p.y;
});
const metroBreite = x + M.rechts;
const metroHoehe = M.oben + (straenge.length - 1) * M.spurLuft + 96;

const metroLinien = straenge.map((strang, spur) => {
  const y = M.oben + spur * M.spurLuft;
  const punkte = strang.schritte
    .map((s) => metroPos.get(s.id))
    .filter(Boolean)
    .sort((a, b) => a.x - b.x);
  return {
    id: strang.id,
    label: strang.label,
    kurz: strang.kurz,
    farbe: strang.farbe,
    y,
    fortschritt: strang.fortschritt,
    pfad: `M ${M.links / 2} ${y} L ${metroBreite - M.rechts / 2} ${y}`,
    halte: punkte,
  };
});

// Nur Abhängigkeiten zwischen verschiedenen Strängen zeichnen – der Rest
// steckt schon in der Linie selbst und würde das Bild zumüllen.
const metroQuer = schritte.flatMap((s) =>
  s.querBraucht.map((b) => {
    const a = metroPos.get(b);
    const z = metroPos.get(s.id);
    if (!a || !z) return null;
    const mitte = (a.y + z.y) / 2;
    const vonS = schrittNachId.get(b);
    return {
      von: b,
      nach: s.id,
      text: `${s.strangKurz} „${s.titel}" wartet auf ${vonS.strangKurz} „${vonS.titel}"`,
      pfad: `M ${a.x} ${a.y} C ${a.x} ${mitte}, ${z.x} ${mitte}, ${z.x} ${z.y}`,
    };
  }).filter(Boolean)
);

const metro = {
  breite: metroBreite,
  hoehe: metroHoehe,
  linien: metroLinien,
  stationen: metroStationen,
  halte: metroHalte,
  quer: metroQuer,
};

/* --- Layout 3: Graph V2 – Abschnitte je Ergebnisstufe ------------------
   Nicht nach reiner Abhängigkeitstiefe, sondern in Blöcken je Stufe. So
   lassen sich Stationen wie im Liniennetz dazwischensetzen. Zulässig, weil
   kein Schritt von einer späteren Stufe abhängt – alle Pfeile zeigen rechts. */
// Ohne Fußzeile reichen Überschrift + zweizeiliger Satz
const G2 = { breite: 238, hoehe: 110, spaltenLuft: 58, zeilenLuft: 16, spurLuft: 56, station: 132 };

const lokalRang = new Map();
function lokal(id) {
  if (lokalRang.has(id)) return lokalRang.get(id);
  const s = schrittNachId.get(id);
  const innen = s.braucht.filter((b) => schrittNachId.get(b).meilenstein === s.meilenstein);
  const wert = innen.length ? Math.max(...innen.map(lokal)) + 1 : 0;
  lokalRang.set(id, wert);
  return wert;
}
schritte.forEach((s) => lokal(s.id));

const abschnitte = meilensteine.map((m) => ({
  stein: m,
  spalten: Math.max(...m.schritte.map((s) => lokalRang.get(s.id))) + 1,
}));

const zelle2 = (m, lr, strangId) =>
  m.schritte.filter((s) => lokalRang.get(s.id) === lr && s.strang === strangId);

const g2Stapel = straenge.map((st) => {
  let max = 1;
  abschnitte.forEach((a) => {
    for (let lr = 0; lr < a.spalten; lr++) max = Math.max(max, zelle2(a.stein, lr, st.id).length);
  });
  return max;
});
const g2SpurHoehe = g2Stapel.map((n) => n * G2.hoehe + (n - 1) * G2.zeilenLuft);
const g2SpurY = g2SpurHoehe.map((_, i) =>
  g2SpurHoehe.slice(0, i).reduce((a, b) => a + b, 0) + i * G2.spurLuft
);

const g2Stationen = [];
let gx = 0;
abschnitte.forEach((a, index) => {
  for (let lr = 0; lr < a.spalten; lr++) {
    straenge.forEach((st, spur) => {
      zelle2(a.stein, lr, st.id).forEach((s, i) => {
        s.g2x = gx + lr * (G2.breite + G2.spaltenLuft);
        s.g2y = g2SpurY[spur] + i * (G2.hoehe + G2.zeilenLuft);
      });
    });
  }
  gx += a.spalten * G2.breite + (a.spalten - 1) * G2.spaltenLuft + G2.spaltenLuft;
  g2Stationen.push({
    id: a.stein.id,
    nr: a.stein.nr,
    titel: a.stein.titel,
    ergebnis: a.stein.ergebnis,
    erreicht: a.stein.erreicht,
    fortschritt: a.stein.fortschritt,
    anzahl: a.stein.anzahl,
    x: gx + G2.station / 2,
    letzte: index === abschnitte.length - 1,
  });
  gx += G2.station + G2.spaltenLuft;
});

const g2Breite = gx - G2.spaltenLuft;
const g2Hoehe = g2SpurY[g2SpurY.length - 1] + g2SpurHoehe[g2SpurHoehe.length - 1];

const bogen2 = (a, b) => {
  const x1 = a.g2x + G2.breite;
  const y1 = a.g2y + G2.hoehe / 2;
  const x2 = b.g2x;
  const y2 = b.g2y + G2.hoehe / 2;
  const dx = Math.max(30, (x2 - x1) / 2);
  return `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;
};

const g2Kanten = schritte.flatMap((s) =>
  s.braucht.map((b) => ({
    von: b,
    nach: s.id,
    quer: nachId.get(b).strang !== s.strang,
    pfad: bogen2(schrittNachId.get(b), s),
  }))
);

const graph2 = {
  breite: g2Breite,
  hoehe: g2Hoehe,
  knotenBreite: G2.breite,
  knotenHoehe: G2.hoehe,
  kanten: g2Kanten,
  stationen: g2Stationen,
  spuren: straenge.map((s, i) => ({
    id: s.id,
    label: s.label,
    kurz: s.kurz,
    frage: s.frage,
    farbe: s.farbe,
    fortschritt: s.fortschritt,
    y: g2SpurY[i],
    hoehe: g2SpurHoehe[i],
  })),
};

export default {
  ...roh,
  graph2,
  schritte,
  straenge,
  meilensteine,
  aktuellerMeilenstein,
  fortschritt: anteil(schritte),
  anzahl: schritte.length,
  kritischerPfad: kritischerPfad.map((id) => schrittNachId.get(id)),
  machbar: schritte.filter((s) => s.machbar),
  blockiert: schritte.filter((s) => !s.machbar && s.status !== "erreicht"),
  erledigt: schritte.filter((s) => s.status === "erreicht"),
  graph,
  metro,
};
