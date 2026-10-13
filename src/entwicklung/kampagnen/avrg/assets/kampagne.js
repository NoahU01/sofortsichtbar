/* Kampagnen-Landingpage AVRG: Variante und Farbe in der Vorschau wählen.
   Die Landingpage läuft echt im Rahmen: am Desktop 1280 px breit und auf die
   verfügbare Breite verkleinert, am Handy in Originalgröße. */
(function () {
  var wahl = document.querySelector('[data-wahl]');
  if (!wahl) return;
  var schirm = wahl.querySelector('[data-schirm]');
  var rahmen = wahl.querySelector('[data-rahmen]');
  var offen = wahl.querySelector('[data-offen]');
  var adresse = wahl.querySelector('[data-adresse]');
  var stand = { variante: '1', farbe: 'rot' };
  var BREITE = 1280;

  function url() { return '/entwicklung/kampagnen/avrg/landingpage-' + stand.variante + '/?farbe=' + stand.farbe; }

  function skaliere() {
    // Schmale Bildschirme: die Handy-Ansicht in Originalgröße statt einer winzigen Desktop-Ansicht
    var breite = schirm.clientWidth < 700 ? schirm.clientWidth : BREITE;
    rahmen.style.width = breite + 'px';
    var f = schirm.clientWidth / breite;
    rahmen.style.transform = 'scale(' + f + ')';
    rahmen.style.height = (schirm.clientHeight / f) + 'px';
  }

  function zeige() {
    rahmen.src = url();
    offen.href = url();
    adresse.textContent = 'deine-agentur.de/neue-altersvorsorge' + (stand.variante === '1' ? '' : '-' + stand.variante);
    wahl.querySelectorAll('[data-variante]').forEach(function (b) {
      b.setAttribute('aria-selected', b.dataset.variante === stand.variante ? 'true' : 'false');
    });
    wahl.querySelectorAll('[data-text]').forEach(function (p) { p.hidden = p.dataset.text !== stand.variante; });
    wahl.querySelectorAll('[data-farbe]').forEach(function (b) {
      b.setAttribute('aria-pressed', b.dataset.farbe === stand.farbe ? 'true' : 'false');
    });
  }

  wahl.querySelectorAll('[data-variante]').forEach(function (b) {
    b.addEventListener('click', function () { stand.variante = b.dataset.variante; zeige(); });
  });
  wahl.querySelectorAll('[data-farbe]').forEach(function (b) {
    b.addEventListener('click', function () {
      stand.farbe = b.dataset.farbe;
      // Gleiche Seite: nur die Farbe im Rahmen umschalten, ohne neu zu laden und ohne Scrollposition zu verlieren
      try {
        rahmen.contentDocument.documentElement.setAttribute('data-farbe', stand.farbe);
        offen.href = url();
        wahl.querySelectorAll('[data-farbe]').forEach(function (x) {
          x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
        });
      } catch (e) { zeige(); }
    });
  });

  skaliere();
  window.addEventListener('resize', skaliere);
})();
