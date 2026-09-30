/* Internes Prozessbild: Überblick und je Kanal ein Prozessdiagramm.
   Positionen stehen in Prozent, die Linien werden daraus in Pixeln gerechnet. */
(function () {
  "use strict";

  var brett = document.querySelector("[data-board]");
  if (!brett) return;

  var buehne = brett.querySelector("[data-stage]");
  var titel = brett.querySelector("[data-titel]");
  var zurueck = brett.querySelector("[data-zurueck]");
  var tabs = Array.prototype.slice.call(brett.querySelectorAll("[data-tab]"));
  var ansichten = Array.prototype.slice.call(buehne.querySelectorAll("[data-view]"));
  var panels = Array.prototype.slice.call(document.querySelectorAll("[data-panel]"));
  var ruhig = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Positionen -------------------------------------------------- */

  var UEBERBLICK = {
    mailing:   { x: 14, y: 12 },
    linkedin:  { x: 38, y: 12 },
    meta:      { x: 64, y: 12 },
    website:   { x: 88, y: 50 },
    datenbank: { x: 50, y: 88 }
  };

  var RING      = { x: 38, y: 52, rx: 28, ry: 42 };   /* mit Website-Zweig rechts */
  var RING_WEIT = { x: 50, y: 52, rx: 33, ry: 42 };   /* ohne Zweig: mittig */
  var ring = RING;
  var ZWEIG = { website: { x: 85, y: 15 }, lead: { x: 88, y: 52 } };

  function ringPunkt(i, n) {
    var w = (-90 + i * (360 / n)) * Math.PI / 180;
    return { x: ring.x + Math.cos(w) * ring.rx, y: ring.y + Math.sin(w) * ring.ry };
  }

  /* ---------- Linienarten ------------------------------------------------- */

  var ARTEN = {
    aktion:  { breite: 1.6, deckung: 0.5,  strich: "",     spitze: "pz-spitze" },
    signal:  { breite: 1.6, deckung: 0.5,  strich: "7 5",  spitze: "pz-spitze" },
    traffic: { breite: 1.4, deckung: 0.3,  strich: "2 5",  spitze: "pz-spitze-schwach" },
    lead:    { breite: 2.4, deckung: 0.95, strich: "",     spitze: "pz-spitze-stark" },
    ring:    { breite: 1.6, deckung: 0.42, strich: "",     spitze: "pz-spitze" }
  };

  var ABSTAND = 11;   /* halber Abstand zweier Gegenrichtungen, in px */
  var BOGEN = 1.9;    /* wie weit die beiden Linien auseinandergehen */

  /* ---------- Geometrie --------------------------------------------------- */

  function kasten(el, bezug) {
    var r = el.getBoundingClientRect();
    return {
      x: r.left - bezug.left + r.width / 2,
      y: r.top - bezug.top + r.height / 2,
      w: r.width,
      h: r.height
    };
  }

  /* Punkt auf dem Rand des Kastens in Richtung dx/dy, plus Luft für die Spitze */
  function rand(k, dx, dy, luft) {
    var len = Math.sqrt(dx * dx + dy * dy) || 1;
    dx /= len; dy /= len;
    var hw = k.w / 2 + luft, hh = k.h / 2 + luft;
    var tx = Math.abs(dx) > 1e-6 ? hw / Math.abs(dx) : Infinity;
    var ty = Math.abs(dy) > 1e-6 ? hh / Math.abs(dy) : Infinity;
    var t = Math.min(tx, ty);
    return { x: k.x + dx * t, y: k.y + dy * t };
  }

  function pfadD(a, b, seite, bogen) {
    var dx = b.x - a.x, dy = b.y - a.y;
    var len = Math.sqrt(dx * dx + dy * dy) || 1;
    var nx = -dy / len, ny = dx / len;          /* Normale */
    var p0 = { x: a.x + nx * seite, y: a.y + ny * seite };
    var p1 = { x: b.x + nx * seite, y: b.y + ny * seite };
    var c = {
      x: (p0.x + p1.x) / 2 + nx * bogen,
      y: (p0.y + p1.y) / 2 + ny * bogen
    };
    return "M" + p0.x.toFixed(1) + " " + p0.y.toFixed(1) +
           "Q" + c.x.toFixed(1) + " " + c.y.toFixed(1) +
           " " + p1.x.toFixed(1) + " " + p1.y.toFixed(1);
  }

  /* Ein Anker ohne Ausdehnung: die Linie endet genau hier */
  function punkt(x, y) { return { x: x, y: y, w: 0, h: 0 }; }

  var NS = "http://www.w3.org/2000/svg";

  function defs(nr) {
    var d = document.createElementNS(NS, "defs");
    [["pz-spitze", 0.85, 11], ["pz-spitze-schwach", 0.6, 10], ["pz-spitze-stark", 1, 14]]
      .forEach(function (m) {
        var mk = document.createElementNS(NS, "marker");
        mk.setAttribute("id", m[0] + "-" + nr);
        mk.setAttribute("viewBox", "0 0 10 10");
        mk.setAttribute("refX", "9");
        mk.setAttribute("refY", "5");
        mk.setAttribute("markerWidth", String(m[2]));
        mk.setAttribute("markerHeight", String(m[2]));
        mk.setAttribute("orient", "auto-start-reverse");
        mk.setAttribute("markerUnits", "userSpaceOnUse");
        var pf = document.createElementNS(NS, "path");
        pf.setAttribute("d", "M0 0L10 5L0 10z");
        pf.setAttribute("fill", "#ffffff");
        pf.setAttribute("fill-opacity", String(m[1]));
        mk.appendChild(pf);
        d.appendChild(mk);
      });
    return d;
  }

  /* zeichnet eine Linie von Element a nach Element b */
  function linie(svg, art, ka, kb, seite, bogenRichtung, marke) {
    var A = ARTEN[art];
    var dx = kb.x - ka.x, dy = kb.y - ka.y;
    var len = Math.sqrt(dx * dx + dy * dy) || 1;
    var p0 = rand(ka, dx, dy, 4);
    var p1 = rand(kb, -dx, -dy, 9);
    var b = typeof bogenRichtung === "number"
      ? bogenRichtung
      : bogenAus(seite, len);

    var pf = document.createElementNS(NS, "path");
    pf.setAttribute("d", pfadD(p0, p1, seite, b));
    pf.setAttribute("fill", "none");
    pf.setAttribute("stroke", "#ffffff");
    pf.setAttribute("stroke-width", String(A.breite));
    pf.setAttribute("stroke-opacity", String(A.deckung));
    pf.setAttribute("stroke-linecap", "round");
    if (A.strich) pf.setAttribute("stroke-dasharray", A.strich);
    pf.setAttribute("marker-end", "url(#" + A.spitze + "-" + svg.getAttribute("data-nr") + ")");
    pf.setAttribute("class", "pz-linie pz-linie--" + art);
    if (marke) pf.setAttribute("data-von", marke);
    svg.appendChild(pf);
    return pf;
  }

  function bogenAus(seite, len) {
    if (!seite) return Math.max(6, Math.min(26, len * 0.06));
    return seite * BOGEN;
  }

  /* ---------- Ansichten aufbauen ----------------------------------------- */

  /* Jede Ansicht braucht eigene Marker-IDs: url(#id) greift sonst auf die
     Marker im ausgeblendeten Überblick-SVG zu, und die zeichnet der Browser nicht. */
  function leeren(svg, nr) {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    svg.setAttribute("data-nr", nr);
    svg.appendChild(defs(nr));
  }

  function bauUeberblick(view) {
    var svg = view.querySelector("[data-lines]");
    var bezug = view.getBoundingClientRect();
    svg.setAttribute("viewBox", "0 0 " + bezug.width + " " + bezug.height);
    leeren(svg, "ueberblick");

    var nodes = {};
    Array.prototype.forEach.call(view.querySelectorAll("[data-node]"), function (n) {
      var id = n.getAttribute("data-node");
      var pos = UEBERBLICK[id];
      if (!pos) return;
      n.style.left = pos.x + "%";
      n.style.top = pos.y + "%";
      nodes[id] = n;
    });

    var bezug2 = view.getBoundingClientRect();
    var k = {};
    Object.keys(nodes).forEach(function (id) { k[id] = kasten(nodes[id], bezug2); });
    if (!k.datenbank) return;

    /* Die Datenbank ist eine breite Leiste: jeder Kanal dockt senkrecht darunter an. */
    var leiste = k.datenbank;
    var oben = leiste.y - leiste.h / 2;

    ["mailing", "linkedin", "meta"].forEach(function (id, i) {
      if (!k[id]) return;
      var an = punkt(k[id].x, oben);
      /* Auf so langer Strecke wirken gerade Parallelen ruhiger als Bögen. */
      linie(svg, "aktion", an, k[id], ABSTAND, 0, id);       /* Aktion nach außen */
      linie(svg, "signal", k[id], an, ABSTAND, 0, id);       /* Signal zurück */
      /* Traffic auf die Website, versetzt damit die Spitzen nicht aufeinanderliegen */
      if (k.website) linie(svg, "traffic", k[id], k.website, (i - 1) * 15, -14, id);
    });

    /* Lead von der Website in die Datenbank - das Hauptziel */
    if (k.website) linie(svg, "lead", k.website, punkt(k.website.x - 40, oben), 0, 18, "website");
  }

  function bauKanal(view) {
    var svg = view.querySelector("[data-lines]");
    var bezug = view.getBoundingClientRect();
    svg.setAttribute("viewBox", "0 0 " + bezug.width + " " + bezug.height);
    leeren(svg, view.getAttribute("data-view"));

    var db = view.querySelector('[data-node="datenbank"]');
    var schritte = Array.prototype.slice.call(view.querySelectorAll("[data-schritt]"));
    var web = view.querySelector('[data-zweig="website"]');
    var lead = view.querySelector('[data-zweig="lead"]');

    ring = web ? RING : RING_WEIT;
    db.style.left = ring.x + "%";
    db.style.top = ring.y + "%";
    schritte.forEach(function (s, i) {
      var pos = ringPunkt(i, schritte.length);
      s.style.left = pos.x + "%";
      s.style.top = pos.y + "%";
    });
    if (web)  { web.style.left  = ZWEIG.website.x + "%"; web.style.top  = ZWEIG.website.y + "%"; }
    if (lead) { lead.style.left = ZWEIG.lead.x + "%";    lead.style.top = ZWEIG.lead.y + "%"; }

    var b2 = view.getBoundingClientRect();
    var kdb = kasten(db, b2);
    var ks = schritte.map(function (s) { return kasten(s, b2); });

    /* Der Kreislauf: 1 → 2 → … → n → 1, nach außen gebogen */
    ks.forEach(function (a, i) {
      var j = (i + 1) % ks.length;
      var b = ks[j];
      var mx = (a.x + b.x) / 2 - kdb.x, my = (a.y + b.y) / 2 - kdb.y;
      var dx = b.x - a.x, dy = b.y - a.y;
      var len = Math.sqrt(dx * dx + dy * dy) || 1;
      /* Normale so wählen, dass sie von der Mitte wegzeigt */
      var nx = -dy / len, ny = dx / len;
      var weg = (nx * mx + ny * my) >= 0 ? 1 : -1;
      linie(svg, "ring", a, b, 0, weg * Math.max(14, len * 0.11), "ring");
    });

    /* Speichen zur Datenbank, Richtung nach Typ */
    schritte.forEach(function (s, i) {
      var typ = s.getAttribute("data-typ");
      if (typ === "signal") linie(svg, s.hasAttribute("data-lead") ? "lead" : "signal", ks[i], kdb, 0, 0, "s" + (i + 1));
      else if (typ === "datenbank") linie(svg, "aktion", kdb, ks[i], 0, 0, "s" + (i + 1));
    });

    /* Website-Zweig: Posting → Website → Lead → Datenbank */
    if (web && lead) {
      var kweb = kasten(web, b2), klead = kasten(lead, b2);
      var quelle = -1;
      schritte.forEach(function (s, i) {
        if (s.hasAttribute("data-zur-website")) quelle = i;
      });
      if (quelle < 0) {
        schritte.forEach(function (s, i) {
          if (quelle < 0 && s.getAttribute("data-typ") === "aktion") quelle = i;
        });
      }
      if (quelle >= 0) linie(svg, "traffic", ks[quelle], kweb, 0, null, "web");
      linie(svg, "traffic", kweb, klead, 0, 6, "web");
      linie(svg, "lead", klead, kdb, 0, -22, "web");
    }
  }

  function bauen(view) {
    if (view.getAttribute("data-view") === "ueberblick") bauUeberblick(view);
    else bauKanal(view);
  }

  /* ---------- Umschalten ------------------------------------------------- */

  var aktuell = "ueberblick";

  function zeigen(id, mitAnimation) {
    var ziel = ansichten.filter(function (v) { return v.getAttribute("data-view") === id; })[0];
    if (!ziel) return;
    var alt = ansichten.filter(function (v) { return v.classList.contains("is-aktiv"); })[0];
    aktuell = id;

    ansichten.forEach(function (v) {
      var an = v === ziel;
      v.hidden = !an;
      v.classList.toggle("is-aktiv", an);
    });

    panels.forEach(function (pa) {
      pa.hidden = pa.getAttribute("data-panel") !== id;
    });

    var kanal = tabs.filter(function (t) { return t.getAttribute("data-tab") === id; })[0];
    tabs.forEach(function (t) {
      var an = t === kanal;
      t.classList.toggle("is-aktiv", an);
      t.setAttribute("aria-pressed", an ? "true" : "false");
    });

    brett.classList.toggle("is-fokus", id !== "ueberblick");
    zurueck.hidden = id === "ueberblick";
    titel.textContent = kanal ? kanal.textContent.trim() : "Überblick";

    bauen(ziel);

    if (mitAnimation && !ruhig && alt !== ziel) {
      ziel.classList.remove("is-eingang");
      void ziel.offsetWidth;
      ziel.classList.add("is-eingang");
    }
  }

  /* ---------- Ereignisse ------------------------------------------------- */

  buehne.addEventListener("click", function (e) {
    var node = e.target.closest ? e.target.closest("button[data-node]") : null;
    if (!node) return;
    var id = node.getAttribute("data-node");
    zeigen(id, true);
    if (history.replaceState) history.replaceState(null, "", "#" + id);
  });

  tabs.forEach(function (t) {
    t.addEventListener("click", function () {
      var id = t.getAttribute("data-tab");
      var ziel = id === aktuell ? "ueberblick" : id;   /* vor zeigen() lesen, das ändert aktuell */
      zeigen(ziel, true);
      if (history.replaceState) history.replaceState(null, "", ziel === "ueberblick" ? "#" : "#" + ziel);
    });
  });

  zurueck.addEventListener("click", function () {
    zeigen("ueberblick", true);
    if (history.replaceState) history.replaceState(null, "", "#");
  });

  /* Linien einer Verbindung hervorheben, wenn man über den Knoten fährt */
  buehne.addEventListener("mouseover", function (e) {
    var node = e.target.closest ? e.target.closest("[data-node]") : null;
    if (!node) return;
    var id = node.getAttribute("data-node");
    var view = ansichten.filter(function (v) { return v.classList.contains("is-aktiv"); })[0];
    if (!view) return;
    Array.prototype.forEach.call(view.querySelectorAll(".pz-linie"), function (l) {
      l.classList.toggle("is-hell", l.getAttribute("data-von") === id);
    });
  });
  buehne.addEventListener("mouseout", function () {
    Array.prototype.forEach.call(buehne.querySelectorAll(".pz-linie.is-hell"), function (l) {
      l.classList.remove("is-hell");
    });
  });

  /* ---------- Start ------------------------------------------------------ */

  var warte;
  window.addEventListener("resize", function () {
    clearTimeout(warte);
    warte = setTimeout(function () {
      var view = ansichten.filter(function (v) { return v.classList.contains("is-aktiv"); })[0];
      if (view) bauen(view);
    }, 120);
  });

  function start() {
    var hash = (location.hash || "").replace("#", "");
    var erlaubt = tabs.map(function (t) { return t.getAttribute("data-tab"); });
    zeigen(erlaubt.indexOf(hash) > -1 ? hash : "ueberblick", false);
  }

  window.addEventListener("hashchange", start);

  if (document.fonts && document.fonts.ready) document.fonts.ready.then(start);
  else start();
  window.addEventListener("load", function () {
    var view = ansichten.filter(function (v) { return v.classList.contains("is-aktiv"); })[0];
    if (view) bauen(view);
  });
})();
