/* AVRG · Black Week 3.0 (Noah, 22.11.2026) – Verhalten der Seite /zielgruppen/avrg-3 */

/* Text-Umschalter (nur Entwicklung): Alternativen je Gruppe, Wahl steht in der Adresse (?hero=2&pos=3&paket=1) */
(function () {
  var box = document.querySelector('[data-n3-texte]'); if (!box) return;
  var q = new URLSearchParams(location.search);
  if (q.get('texte') === '0') { box.hidden = true; }
  function zeige(gruppe, v, merken) {
    document.querySelectorAll('[data-alt="' + gruppe + '"]').forEach(function (el) { el.hidden = el.getAttribute('data-v') !== v; });
    box.querySelectorAll('[data-gruppe="' + gruppe + '"] button').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-v') === v ? 'true' : 'false'); });
    if (merken) { var u = new URL(location.href); u.searchParams.set(gruppe, v); history.replaceState(null, '', u); }
  }
  box.querySelectorAll('[data-gruppe]').forEach(function (z) {
    var g = z.getAttribute('data-gruppe');
    z.querySelectorAll('button').forEach(function (b) { b.addEventListener('click', function () { zeige(g, b.getAttribute('data-v'), true); }); });
    var start = q.get(g); if (start && /^[123]$/.test(start)) zeige(g, start, false);
  });
  var auf = box.querySelector('[data-n3-texte-auf]');
  auf.addEventListener('click', function () { var zu = box.classList.toggle('ist-zu'); auf.setAttribute('aria-expanded', zu ? 'false' : 'true'); });
  if (window.matchMedia('(max-width: 640px)').matches) { box.classList.add('ist-zu'); auf.setAttribute('aria-expanded', 'false'); }
})();

/* Sichtbarkeit: Abschnitte bekommen .ist-sichtbar, sobald sie ins Bild kommen (Animationen starten erst dann) */
(function () {
  var ziele = document.querySelectorAll('[data-n3-pl], [data-n3-schritte]');
  if (!('IntersectionObserver' in window)) { ziele.forEach(function (z) { z.classList.add('ist-sichtbar'); }); return; }
  var io = new IntersectionObserver(function (e) { e.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('ist-sichtbar'); io.unobserve(x.target); } }); }, { threshold: .25 });
  ziele.forEach(function (z) { io.observe(z); });
})();

/* Konfigurator: echte Landingpage live im MacBook. Farbe per Hex-Code, Farbfeld oder Schnellauswahl. */
(function () {
  var k = document.querySelector('[data-n3-konfig]'); if (!k) return;
  var feld = k.querySelector('[data-n3-feld]'), punkt = k.querySelector('[data-n3-punkt]'), hexFeld = k.querySelector('[data-n3-hex]');
  var LP = '/entwicklung/kampagnen/avrg/landingpage-', stil = '3';
  var farbe;                                         /* { h, s, l, hex? } – hex bleibt exakt, wenn er eingegeben oder gewählt wurde */
  var L_OBEN = 82, L_UNTEN = 14, S_FELD = 78;       /* Farbfeld: x = Farbton, y = Helligkeit */

  function begrenzen(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function hslZuRgb(h, s, l) { s /= 100; l /= 100; var f = function (n) { var k2 = (n + h / 30) % 12, a = s * Math.min(l, 1 - l); return l - a * Math.max(-1, Math.min(k2 - 3, 9 - k2, 1)); }; return [f(0), f(8), f(4)]; }
  function rgbZuHex(rgb) { return rgb.map(function (v) { var x = Math.round(v * 255).toString(16); return x.length < 2 ? '0' + x : x; }).join('').toUpperCase(); }
  function hexZuHsl(hex) {
    var r = parseInt(hex.slice(0, 2), 16) / 255, g = parseInt(hex.slice(2, 4), 16) / 255, b = parseInt(hex.slice(4, 6), 16) / 255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 2, h = 0, s = 0, d = max - min;
    if (d) { s = d / (1 - Math.abs(2 * l - 1)); h = max === r ? ((g - b) / d) % 6 : max === g ? (b - r) / d + 2 : (r - g) / d + 4; h = (h * 60 + 360) % 360; }
    return { h: Math.round(h), s: Math.round(s * 100), l: Math.round(l * 100), hex: hex.toUpperCase() };
  }
  function lum(rgb) { var c = rgb.map(function (v) { return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }); return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]; }
  function hsl(h, s, l) { return 'hsl(' + h + ' ' + s + '% ' + begrenzen(l, 0, 100) + '%)'; }

  farbe = hexZuHsl('11708A');
  function vars() {
    var h = farbe.h, s = farbe.s, l = farbe.l, rgb = hslZuRgb(h, s, l), hellGrund = lum(rgb) > .42;
    var rgbT = rgb.map(function (v) { return Math.round(v * 255); }).join(',');
    return { '--rot': hsl(h, s, l), '--rot-dunkel': hsl(h, s, l - 8), '--rot-text': hellGrund ? hsl(h, s, Math.min(l, 34)) : hsl(h, s, l),
      '--rot-hell': hsl(h, s, Math.max(l, 62)), '--rot-betont': hellGrund ? hsl(h, s, 20) : hsl(h, s, 86), '--rot-glut': 'rgba(' + rgbT + ',.38)',
      '--rot-schatten': 'rgba(' + rgbT + ',.45)', '--auf-rot': hellGrund ? '#111' : '#fff', '--auf-rot-leise': hellGrund ? 'rgba(17,17,17,.78)' : 'rgba(255,255,255,.86)',
      '--auf-rot-rand': hellGrund ? 'rgba(17,17,17,.4)' : 'rgba(255,255,255,.55)', '--auf-rot-linie': hellGrund ? 'rgba(17,17,17,.2)' : 'rgba(255,255,255,.3)',
      farbe: farbe.hex ? '#' + farbe.hex : hsl(h, s, l), auf: hellGrund ? '#111' : '#fff', hex: farbe.hex || rgbZuHex(rgb) };
  }

  function faerben(fr) {
    try { var d = fr.contentDocument; if (!d || !d.documentElement) return; var v = vars(); Object.keys(v).forEach(function (n) { if (n.indexOf('--') === 0) d.documentElement.style.setProperty(n, v[n]); }); } catch (e) {}
  }
  function vorbereiten(fr) {
    try {
      var d = fr.contentDocument;
      d.querySelectorAll('img[src*="logo-platzhalter"]').forEach(function (i) { i.src = '/entwicklung/kampagnen/avrg/assets/black-week/dein-logo.svg'; });
      var w = d.createTreeWalker(d.body, NodeFilter.SHOW_TEXT), n; while ((n = w.nextNode())) n.nodeValue = n.nodeValue.replace(/15(\s| )Minuten/g, '30$1Minuten');
      var st = d.createElement('style'); st.textContent = 'html,body{overflow:hidden!important}*{scroll-behavior:auto!important}'; d.head.appendChild(st);
      var kappen = function () {
        var nr = (fr.getAttribute('src').match(/landingpage-(\d)/) || [])[1];
        if (nr !== '1') d.querySelectorAll('section').forEach(function (sec) { var t = sec.getBoundingClientRect().top; if (t > 120 && t < 900) sec.style.visibility = 'hidden'; });
        d.querySelectorAll('body *').forEach(function (el) { var r = el.getBoundingClientRect(); if (r.top > 830 && r.top < 900 && r.height > 40) el.style.visibility = 'hidden'; });
      };
      kappen(); setTimeout(kappen, 800);
    } catch (e) {}
    faerben(fr); fr.parentNode.classList.add('ist-bereit');
  }
  var rahmen = [];
  document.querySelectorAll('#n3 [data-b2-live]').forEach(function (box) {
    var fr = document.createElement('iframe');
    fr.setAttribute('title', 'Vorschau der Landingpage'); fr.setAttribute('aria-hidden', 'true'); fr.setAttribute('tabindex', '-1');
    fr.addEventListener('load', function () { vorbereiten(fr); });
    box.appendChild(fr); rahmen.push(fr);
    var passen = function () { fr.style.transform = 'scale(' + (box.clientWidth / 1440) + ')'; };
    if (window.ResizeObserver) new ResizeObserver(passen).observe(box); passen();
  });
  function laden() { rahmen.forEach(function (fr) { fr.parentNode.classList.remove('ist-bereit'); fr.src = LP + stil + '/?farbe=sofort&vorschau'; }); }

  function zeige(quelle) {
    var v = vars();
    document.getElementById('n3').style.setProperty('--n3-farbe', v.farbe);
    document.getElementById('n3').style.setProperty('--n3-auf-farbe', v.auf);
    document.querySelectorAll('#n3 [data-n3-farbpunkt]').forEach(function (i) { i.style.background = v.farbe; });
    /* Punkt im Feld */
    var x = farbe.h / 359, y = begrenzen((L_OBEN - farbe.l) / (L_OBEN - L_UNTEN), 0, 1);
    punkt.style.left = (x * 100) + '%'; punkt.style.top = (y * 100) + '%'; punkt.style.background = v.farbe;
    feld.setAttribute('aria-valuetext', '#' + v.hex);
    if (quelle !== 'hex') { hexFeld.value = v.hex; hexFeld.classList.remove('ist-falsch'); }
    k.querySelectorAll('[data-n3-muster]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-n3-muster').slice(1).toUpperCase() === v.hex ? 'true' : 'false'); });
    k.querySelectorAll('[data-b2-stil]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-b2-stil') === stil ? 'true' : 'false'); });
    document.querySelectorAll('#n3 [data-b2-schritt-stil]').forEach(function (sp) { sp.classList.toggle('an', sp.getAttribute('data-b2-schritt-stil') === stil); });
    rahmen.forEach(faerben);
  }

  /* Farbfeld: ziehen mit Maus oder Finger, Pfeiltasten */
  function ausFeld(e) {
    var r = feld.getBoundingClientRect();
    var x = begrenzen((e.clientX - r.left) / r.width, 0, 1), y = begrenzen((e.clientY - r.top) / r.height, 0, 1);
    farbe = { h: Math.round(x * 359), s: S_FELD, l: Math.round(L_OBEN - y * (L_OBEN - L_UNTEN)) };
    zeige('feld');
  }
  feld.addEventListener('pointerdown', function (e) { feld.setPointerCapture(e.pointerId); feld.classList.add('ist-aktiv'); ausFeld(e); });
  feld.addEventListener('pointermove', function (e) { if (feld.hasPointerCapture(e.pointerId)) ausFeld(e); });
  feld.addEventListener('pointerup', function () { feld.classList.remove('ist-aktiv'); });
  feld.addEventListener('keydown', function (e) {
    var d = e.shiftKey ? 10 : 2, f = { h: farbe.h, s: farbe.s, l: farbe.l };
    if (e.key === 'ArrowLeft') f.h = (f.h - d + 360) % 360; else if (e.key === 'ArrowRight') f.h = (f.h + d) % 360;
    else if (e.key === 'ArrowUp') f.l = begrenzen(f.l + d, L_UNTEN, L_OBEN); else if (e.key === 'ArrowDown') f.l = begrenzen(f.l - d, L_UNTEN, L_OBEN); else return;
    e.preventDefault(); farbe = f; zeige('feld');
  });

  /* Hex-Code: übernimmt, sobald sechs gültige Zeichen dastehen */
  hexFeld.addEventListener('input', function () {
    var w = hexFeld.value.replace(/[^0-9a-f]/gi, '').slice(0, 6);
    if (hexFeld.value !== w) hexFeld.value = w;
    if (w.length === 3) w = w.split('').map(function (c) { return c + c; }).join('');
    var ok = w.length === 6; hexFeld.classList.toggle('ist-falsch', !ok && hexFeld.value.length > 0);
    if (ok) { farbe = hexZuHsl(w); zeige('hex'); }
  });
  hexFeld.addEventListener('blur', function () { hexFeld.value = vars().hex; hexFeld.classList.remove('ist-falsch'); });

  k.querySelectorAll('[data-n3-muster]').forEach(function (b) { b.addEventListener('click', function () { farbe = hexZuHsl(b.getAttribute('data-n3-muster').slice(1)); zeige('muster'); }); });
  k.querySelectorAll('[data-b2-stil]').forEach(function (b) { b.addEventListener('click', function () { stil = b.getAttribute('data-b2-stil'); laden(); zeige(); }); });
  laden(); zeige();
})();

/* Black-Week-Countdown bis 04.12.2026, 23:59:59 (deutsche Zeit); danach Normalpreis 89 € ohne Aktion */
(function () {
  var ende = new Date('2026-12-04T23:59:59+01:00').getTime();
  function zwei(n) { return (n < 10 ? '0' : '') + n; }
  function tick() {
    var rest = ende - Date.now();
    if (rest <= 0) {
      document.querySelectorAll('#n3 [data-av9-uhr], #n3 [data-n3-aktion]').forEach(function (u) { u.hidden = true; });
      document.querySelectorAll('#n3 [data-av9-preis2]').forEach(function (p) { p.innerHTML = '<small>AVRG-Vertriebsstrecke</small><b>89 €</b><span>im Monat</span>'; });
      document.querySelectorAll('#n3 [data-n3-betrag]').forEach(function (p) { p.innerHTML = '<b>89 €</b><span>pro Monat</span>'; });
      document.querySelectorAll('#n3 .n3-preis__marke').forEach(function (m) { m.textContent = 'AVRG-Vertriebsstrecke'; });
      return;
    }
    var t = Math.floor(rest / 864e5), s = Math.floor(rest % 864e5 / 36e5), mi = Math.floor(rest % 36e5 / 6e4), se = Math.floor(rest % 6e4 / 1e3);
    document.querySelectorAll('#n3 [data-av9-uhr]').forEach(function (u) {
      u.querySelector('[data-t]').textContent = t; u.querySelector('[data-s]').textContent = zwei(s); u.querySelector('[data-m]').textContent = zwei(mi); u.querySelector('[data-sek]').textContent = zwei(se);
    });
    setTimeout(tick, 1000 - Date.now() % 1000);
  }
  tick();
})();
