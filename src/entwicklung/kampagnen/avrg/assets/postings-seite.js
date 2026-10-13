/* Postings AVRG: Raster mit Themenfilter und Großansicht.
   Die Bilder werden aus den Daten in postings.js gebaut (Darstellung aus dem Medienkonzept),
   deshalb wechseln sie mit der Farbwahl. */
(function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var P = window.AVRG_POSTINGS || [], TH = window.AVRG_THEMEN || {};
  var FOTO = '/entwicklung/kampagnen/avrg/assets/fotos/';
  function nr(i) { return (i + 1 < 10 ? '0' : '') + (i + 1); }
  function flaeche(p, art) {
    return '<div class="cr cr--' + art + '">' + (p.d ? '<span class="cr__deko">' + p.d + '</span>' : '') +
      '<div class="cr__in"><p class="cr__label">' + p.l + '</p><p class="cr__h cr__mitte">' + p.h + '</p>' + (p.fuss ? '<p class="cr__fuss">' + p.fuss + '</p>' : '') + '</div></div>';
  }
  function creative(p) {
    switch (p.t) {
      case 'weiss': case 'rot': case 'schwarz': return flaeche(p, p.t);
      case 'blase':
        return '<div class="cr"><img class="cr__foto" src="' + FOTO + p.foto + '.jpg" alt="" loading="lazy"><p class="cr__blase">' + p.blase + '</p><span class="cr__tag">' + p.tag + '</span></div>';
      case 'band':
        return '<div class="cr cr--band"><img class="cr__foto" src="' + FOTO + p.foto + '.jpg" alt="" loading="lazy"><div class="cr__in"><p class="cr__h">' + p.h + '</p></div></div>';
      case 'fa':
        return '<div class="cr cr--fa"><div class="cr__frage"><p class="cr__fa-label">Frage</p><p class="cr__h">' + p.q + '</p></div><div class="cr__antwort"><p class="cr__fa-label">Antwort</p><p>' + p.a + '</p></div></div>';
      case 'durch':
        return '<div class="cr cr--durch"><div class="cr__in"><p class="cr__label" style="color:var(--r-text)">Was du bei uns nicht bekommst</p><div class="cr__mitte"><ul class="cr__weg">' + p.items.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul><p class="cr__h">' + p.h + '</p></div></div></div>';
      case 'check':
        return '<div class="cr cr--check"><div class="cr__in"><p class="cr__label" style="color:var(--auf-r-leise)">Neue Altersvorsorge 2027</p><div class="cr__mitte"><p class="cr__h">' + p.h + '</p><ul class="cr__haken">' + p.items.map(function (x) { return '<li><i></i>' + x + '</li>'; }).join('') + '</ul></div></div></div>';
      case 'split':
        return '<div class="cr cr--split"><div class="cr__teil cr__teil--o"><small>Ergebnis A</small><b>Mitnehmen.</b></div><div class="cr__teil cr__teil--u"><small>Ergebnis B</small><b>Abhaken<span>.</span></b></div><span class="cr__oder">oder</span></div>';
      case 'zahl':
        return '<div class="cr cr--zahl"><div class="cr__in"><p class="cr__label" style="color:var(--r-text)">Countdown</p><div class="cr__mitte"><p class="cr__zahl">' + p.z + '</p><p class="cr__h">' + p.h + '</p></div><p class="cr__fuss">' + p.fuss + '</p></div></div>';
      case 'zitat':
        return '<div class="cr cr--zitat"><div class="cr__in"><p class="cr__anf">“</p><p class="cr__h cr__mitte">' + p.h + '</p></div></div>';
      case 'suche':
        return '<div class="cr cr--suche"><div class="cr__in"><div class="cr__such"><div class="cr__feld"><span class="cr__lupe"></span><span>' + p.q + '<span class="cr__cursor"></span></span></div><ul class="cr__vorsch">' + p.vorschlaege.map(function (x) { return '<li><span>altersvorsorge <b>' + x.replace('… ', '') + '</b></span></li>'; }).join('') + '</ul></div><p class="cr__h">' + p.h + '</p></div></div>';
      case 'chat':
        return '<div class="cr cr--chat"><div class="cr__in"><p class="cr__label" style="color:var(--r-text)">Neue Altersvorsorge 2027</p><div class="cr__chat"><p class="cr__msg cr__msg--ich"><small>Du</small>' + p.ich + '</p><p class="cr__msg cr__msg--wir"><small>Wir</small>' + p.wir + '</p><span class="cr__tippt"><i></i><i></i><i></i></span></div></div></div>';
      case 'notiz':
        return '<div class="cr cr--notiz"><div class="cr__zettel"><b>' + p.titel + '</b><ul>' + p.items.map(function (x) { return '<li class="' + (x[1] ? 'ok' : 'offen') + '"><i></i><span>' + x[0] + '</span></li>'; }).join('') + '</ul></div><div class="cr__in"><p class="cr__h">' + p.h + '</p></div></div>';
      case 'ticket':
        return '<div class="cr cr--ticket"><div class="cr__in"><p class="cr__h">' + p.h + '</p></div><div class="cr__tk"><div class="cr__tk-haupt"><small>Neue Altersvorsorge 2027</small><b>15 Minuten Klarheit</b><ul><li>Betrifft mich das?</li><li>Wenn ja: wie?</li><li>Habe ich einen Vorteil?</li></ul></div><div class="cr__tk-ab"><span>Kostenlos</span></div></div></div>';
    }
    return '';
  }

  var raster = $('#ps-raster'), filter = $('#ps-filter'), modal = $('#ps-modal');
  if (!raster) return;

  raster.innerHTML = P.map(function (p, i) {
    return '<li class="ps-kachel" data-th="' + p.th + '"><button type="button" data-i="' + i + '" aria-label="Posting ' + nr(i) + ' öffnen">' +
      creative(p) + '</button><span class="ps-kachel__info"><b>' + nr(i) + '</b> · Woche ' + p.w + ' · ' + TH[p.th] + '</span></li>';
  }).join('');

  var zaehl = {};
  P.forEach(function (p) { zaehl[p.th] = (zaehl[p.th] || 0) + 1; });
  filter.innerHTML = '<button type="button" aria-pressed="true" data-th="">Alle <span>' + P.length + '</span></button>' +
    Object.keys(TH).filter(function (k) { return zaehl[k]; }).map(function (k) {
      return '<button type="button" aria-pressed="false" data-th="' + k + '">' + TH[k] + ' <span>' + zaehl[k] + '</span></button>';
    }).join('');
  $$('button', filter).forEach(function (b) {
    b.addEventListener('click', function () {
      var th = b.dataset.th;
      $$('button', filter).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      $$('.ps-kachel', raster).forEach(function (k) { k.hidden = !!th && k.dataset.th !== th; });
    });
  });

  var jetzt = 0, kanal = 'ig';
  function zeigeText() {
    var p = P[jetzt], t = kanal === 'li' ? p.li : p.ig;
    $('#ps-m-text').innerHTML = t.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/(#[\wäöüÄÖÜß]+)/g, '<span class="ps-tags">$1</span>');
    $$('[data-kanal]', modal).forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.kanal === kanal ? 'true' : 'false'); });
    var k = $('#ps-kopieren'); k.textContent = 'Text kopieren';
  }
  function sichtbar() { return $$('.ps-kachel', raster).filter(function (k) { return !k.hidden; }).map(function (k) { return +$('button', k).dataset.i; }); }
  function oeffne(i) {
    jetzt = i; var p = P[i];
    $('#ps-m-bild').innerHTML = creative(p);
    $('#ps-m-titel').textContent = 'Posting ' + nr(i) + ' · Woche ' + p.w + ' · ' + TH[p.th];
    $('#ps-m-meta').innerHTML = '<dt>Bildidee</dt><dd>' + p.bild + '</dd><dt>Ziel</dt><dd>' + p.ziel + '</dd><dt>Format</dt><dd>Einzelbild 4:5, 1080 × 1350 px</dd>';
    zeigeText();
    if (!modal.open) modal.showModal();
  }
  raster.addEventListener('click', function (e) { var b = e.target.closest('button[data-i]'); if (b) oeffne(+b.dataset.i); });
  function blaettere(d) { var l = sichtbar(), pos = l.indexOf(jetzt); oeffne(l[(pos + d + l.length) % l.length]); }
  $('#ps-zurueck').addEventListener('click', function () { blaettere(-1); });
  $('#ps-vor').addEventListener('click', function () { blaettere(1); });
  $('#ps-zu').addEventListener('click', function () { modal.close(); });
  $$('[data-kanal]', modal).forEach(function (b) { b.addEventListener('click', function () { kanal = b.dataset.kanal; zeigeText(); }); });
  $('#ps-kopieren').addEventListener('click', function () {
    var t = kanal === 'li' ? P[jetzt].li : P[jetzt].ig, k = this;
    (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { k.textContent = 'Kopiert ✓'; }, function () { k.textContent = 'Bitte markieren und kopieren'; });
  });
  modal.addEventListener('click', function (e) { if (e.target === modal) modal.close(); });
  modal.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') blaettere(1); if (e.key === 'ArrowLeft') blaettere(-1); });
})();
