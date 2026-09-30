/* =========================================================
   Prozessbild: Kanäle im Kreis anordnen, Linien zur Nabe
   ziehen, Detailbereich umschalten.

   Die Positionen werden gerechnet statt im CSS festgenagelt –
   dann stimmen sie bei jeder Fensterbreite und bei einer
   zusätzlichen Kanal-Karte auch noch.
   ========================================================= */
(function () {
  "use strict";

  var stage = document.querySelector("[data-map]");
  if (!stage) return;

  var svg = stage.querySelector("[data-map-lines]");
  var hub = stage.querySelector('[data-node="hub"]');
  var kanaele = Array.prototype.slice.call(stage.querySelectorAll(".pz-node--kanal"));
  var panels = Array.prototype.slice.call(document.querySelectorAll("[data-panel]"));
  var mobil = window.matchMedia("(max-width: 767px)");

  /* --- Anordnung ----------------------------------------------------- */
  function anordnen() {
    if (mobil.matches) {
      // Gestapelt: Positionierung aus dem CSS, hier nichts zu tun.
      kanaele.forEach(function (el) { el.style.left = el.style.top = ""; });
      hub.style.left = hub.style.top = "";
      svg.innerHTML = "";
      return;
    }

    hub.style.left = "50%";
    hub.style.top = "50%";

    var n = kanaele.length;
    kanaele.forEach(function (el, i) {
      // Bei -90 Grad starten, damit der erste Kanal oben steht.
      var winkel = (-90 + i * (360 / n)) * Math.PI / 180;
      el.style.left = (50 + Math.cos(winkel) * 34) + "%";
      el.style.top = (50 + Math.sin(winkel) * 36) + "%";
    });

    linienZiehen();
  }

  /* --- Verbindungslinien ---------------------------------------------
     Zwei Bögen je Kanal statt einer Linie: nach außen unsere Aktion,
     nach innen das Signal zurück. Das ist die eigentliche Aussage des
     Bildes, deshalb bekommt jede Richtung eine eigene Spur und Spitze. */
  var RAUS = "#a167e4";
  var REIN = "#4ec9f1";

  function pfeilspitzen() {
    var defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
    [["pz-raus", RAUS], ["pz-rein", REIN]].forEach(function (paar) {
      var m = document.createElementNS("http://www.w3.org/2000/svg", "marker");
      m.setAttribute("id", paar[0]);
      m.setAttribute("viewBox", "0 0 10 10");
      m.setAttribute("refX", "9"); m.setAttribute("refY", "5");
      m.setAttribute("markerWidth", "5"); m.setAttribute("markerHeight", "5");
      m.setAttribute("orient", "auto-start-reverse");
      var pf = document.createElementNS("http://www.w3.org/2000/svg", "path");
      pf.setAttribute("d", "M 0 1 L 9 5 L 0 9 z");
      pf.setAttribute("fill", paar[1]);
      m.appendChild(pf); defs.appendChild(m);
    });
    svg.appendChild(defs);
  }

  /** Punkt auf dem Rand der Karte in Richtung Ziel – sonst enden die
      Bögen unter der Karte und die Spitze ist nicht zu sehen. */
  function randpunkt(box, zielX, zielY, rahmen) {
    var cx = box.cx, cy = box.cy;
    var dx = zielX - cx, dy = zielY - cy;
    if (!dx && !dy) return { x: cx, y: cy };
    var halbB = box.w / 2 + rahmen, halbH = box.h / 2 + rahmen;
    var t = Math.min(halbB / Math.abs(dx || 1e-6), halbH / Math.abs(dy || 1e-6));
    return { x: cx + dx * t, y: cy + dy * t };
  }

  function linienZiehen() {
    var stageBox = stage.getBoundingClientRect();
    svg.setAttribute("viewBox", "0 0 " + stageBox.width + " " + stageBox.height);
    svg.innerHTML = "";
    pfeilspitzen();

    function masse(el) {
      var r = el.getBoundingClientRect();
      return { cx: r.left + r.width / 2 - stageBox.left, cy: r.top + r.height / 2 - stageBox.top,
               w: r.width, h: r.height };
    }
    var h = masse(hub);

    kanaele.forEach(function (el) {
      var k = masse(el);
      var vonHub = randpunkt(h, k.cx, k.cy, 6);
      var amKanal = randpunkt(k, h.cx, h.cy, 6);

      // Senkrechte zur Verbindung, damit sich die Spuren nicht decken
      var dx = amKanal.x - vonHub.x, dy = amKanal.y - vonHub.y;
      var laenge = Math.hypot(dx, dy) || 1;
      var nx = -dy / laenge, ny = dx / laenge;
      var mx = (vonHub.x + amKanal.x) / 2, my = (vonHub.y + amKanal.y) / 2;
      // Bogen an die Strecke koppeln, sonst wird er auf kurzen Wegen zur Linse
      var bogen = Math.max(4, Math.min(9, laenge * 0.055));

      [[vonHub, amKanal, RAUS, "pz-raus", 1],
       [amKanal, vonHub, REIN, "pz-rein", -1]].forEach(function (cfg) {
        var a = cfg[0], b = cfg[1], farbe = cfg[2], marker = cfg[3], seite = cfg[4];
        var pfad = document.createElementNS("http://www.w3.org/2000/svg", "path");
        pfad.setAttribute("d", "M " + a.x + " " + a.y +
          " Q " + (mx + nx * bogen * seite) + " " + (my + ny * bogen * seite) +
          " " + b.x + " " + b.y);
        pfad.setAttribute("fill", "none");
        pfad.setAttribute("stroke", farbe);
        pfad.setAttribute("stroke-width", "1.5");
        pfad.setAttribute("marker-end", "url(#" + marker + ")");
        pfad.dataset.fuer = el.dataset.node;
        svg.appendChild(pfad);
      });
    });
  }

  /* --- Umschalten ----------------------------------------------------- */
  function zeigen(id) {
    panels.forEach(function (pn) { pn.hidden = pn.dataset.panel !== id; });
    [hub].concat(kanaele).forEach(function (el) {
      el.classList.toggle("is-aktiv", el.dataset.node === id);
    });
    svg.querySelectorAll("path[data-fuer]").forEach(function (l) {
      l.classList.toggle("is-aktiv", l.dataset.fuer === id);
    });
  }

  [hub].concat(kanaele).forEach(function (el) {
    el.addEventListener("click", function () { zeigen(el.dataset.node); });
  });

  anordnen();
  zeigen("hub");

  var timer;
  window.addEventListener("resize", function () {
    clearTimeout(timer);
    timer = setTimeout(anordnen, 120);
  }, { passive: true });

  // Erst wenn die Schriften stehen, haben die Karten ihre Endmaße.
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(anordnen);
})();
