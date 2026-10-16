/* DD Volt — map.js
   Interaktywna mapa realizacji (Leaflet + ciemne kafle CARTO).
   Dane projektów: edytuj tablicę PROJECTS. Współrzędne = miasto; gdy miasto
   nieznane, pinezka stoi w środku kraju i ma dopisek w polu "note". */
(function () {
  'use strict';
  const root = document.getElementById('map');
  if (!root || typeof L === 'undefined') return;

  const PROJECTS = [
    { id: 'ford-kolonia', title: 'Ford — linia i lakiernia', place: 'Kolonia', country: 'Niemcy', cc: 'DE', lat: 50.9375, lon: 6.9603,
      sector: 'Automotive', duration: '24 mies.', via: 'SICA', text: 'Instalacje elektryczne linii produkcyjnej i lakierni. Dwa lata na jednym zakładzie, jako podwykonawca SICA.' },
    { id: 'tesla', title: 'Tesla — zakład produkcyjny', place: 'Grünheide', country: 'Niemcy', cc: 'DE', lat: 52.3926, lon: 13.8084,
      sector: 'Automotive', duration: '12 mies.', via: 'własna działalność', text: 'Rok na budowie linii: elektryka i mechanika. Pierwszy duży projekt na własnej działalności.', note: 'lokalizacja do potwierdzenia' },
    { id: 'bmw-monachium', title: 'BMW — linia produkcyjna', place: 'Monachium', country: 'Niemcy', cc: 'DE', lat: 48.1351, lon: 11.5820,
      sector: 'Automotive', duration: 'do potwierdzenia', via: 'Proster', text: 'Instalacje elektryczne i mechaniczne linii dla BMW, jako podwykonawca.' },
    { id: 'audi-gyor', title: 'Audi — zakład produkcyjny', place: 'Győr', country: 'Węgry', cc: 'HU', lat: 47.6875, lon: 17.6504,
      sector: 'Automotive', duration: '2 mies.', text: 'Dwa miesiące na linii Audi: okablowanie i podłączenia.' },
    { id: 'bergamo', title: 'Lakiernia', place: 'Bergamo', country: 'Włochy', cc: 'IT', lat: 45.6983, lon: 9.6773,
      sector: 'Automotive', duration: '3 mies.', text: 'Instalacje elektryczne i mechaniczne lakierni. Trzy miesiące z ekipą na miejscu.' },
    { id: 'frankfurt-woda', title: 'Producent wód mineralnych', place: 'Frankfurt', country: 'Niemcy', cc: 'DE', lat: 50.1109, lon: 8.6821,
      sector: 'Przemysł', duration: '2 mies.', text: 'Elektryka linii rozlewniczej w zakładzie spożywczym.' },
    { id: 'microsoft', title: 'Serwerownia — Microsoft', place: 'Niemcy', country: 'Niemcy', cc: 'DE', lat: 51.1657, lon: 10.4515,
      sector: 'Obiekty', duration: '2 mies.', text: 'Instalacja elektryczna serwerowni. Prowadzenie ekipy na miejscu jako lider.', note: 'miasto do potwierdzenia' },
    { id: 'szkoly-de', title: 'Szkoły — instalacje elektryczne', place: 'Niemcy', country: 'Niemcy', cc: 'DE', lat: 49.6, lon: 9.1,
      sector: 'Obiekty', duration: 'kilka obiektów', text: 'Pełne instalacje szkolne: oświetlenie, siła, rozdzielnie.', note: 'miasta do potwierdzenia' },
    { id: 'warszawa', title: 'Podłączenie silników', place: 'Warszawa', country: 'Polska', cc: 'PL', lat: 52.2297, lon: 21.0122,
      sector: 'Przemysł', duration: 'do potwierdzenia', text: 'Podłączenia silników i urządzeń na hali produkcyjnej.' },
    { id: 'czestochowa', title: 'Podłączenie silników', place: 'Częstochowa', country: 'Polska', cc: 'PL', lat: 50.8118, lon: 19.1203,
      sector: 'Przemysł', duration: 'do potwierdzenia', text: 'Podłączenia silników i urządzeń linii.' },
    { id: 'zawiercie', title: 'Piece przemysłowe', place: 'Zawiercie', country: 'Polska', cc: 'PL', lat: 50.4879, lon: 19.4166,
      sector: 'Przemysł', duration: 'do potwierdzenia', text: 'Elektryka pieców przemysłowych.' }
  ];

  const map = L.map(root, { zoomControl: true, scrollWheelZoom: false, attributionControl: true, zoomSnap: .25 });
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd', maxZoom: 12, minZoom: 3
  }).addTo(map);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}{r}.png', { subdomains: 'abcd', maxZoom: 12, opacity: .7, pane: 'shadowPane' }).addTo(map);

  const list = document.querySelector('.map-list');
  const active = document.querySelector('.map-active');
  const count = document.querySelector('.map-count');
  const filters = document.querySelector('.map-filters');
  const markers = {};
  let current = null;
  let filter = 'all';

  const icon = () => L.divIcon({ className: '', html: '<div class="dd-pin"></div>', iconSize: [14, 14], iconAnchor: [7, 7] });

  PROJECTS.forEach(p => {
    const m = L.marker([p.lat, p.lon], { icon: icon(), keyboard: false, title: p.title }).addTo(map);
    m.bindTooltip(p.place + ' · ' + p.sector, { className: 'dd-tip', direction: 'top', offset: [0, -12] });
    m.on('click', () => select(p.id, true));
    m.on('mouseover', () => m.getElement()?.querySelector('.dd-pin')?.classList.add('is-active'));
    m.on('mouseout', () => { if (current !== p.id) m.getElement()?.querySelector('.dd-pin')?.classList.remove('is-active'); });
    markers[p.id] = m;

    if (list) {
      const b = document.createElement('button');
      b.type = 'button'; b.dataset.id = p.id; b.dataset.sector = p.sector; b.dataset.cc = p.cc;
      b.innerHTML = '<span class="sq"></span><span>' + p.title + '</span><span class="city">' + p.place + '</span>';
      b.addEventListener('click', () => select(p.id, true));
      b.addEventListener('mouseenter', () => markers[p.id].getElement()?.querySelector('.dd-pin')?.classList.add('is-active'));
      b.addEventListener('mouseleave', () => { if (current !== p.id) markers[p.id].getElement()?.querySelector('.dd-pin')?.classList.remove('is-active'); });
      list.appendChild(b);
    }
  });

  function select(id, fly) {
    const p = PROJECTS.find(x => x.id === id);
    if (!p) return;
    current = id;
    Object.entries(markers).forEach(([k, m]) => m.getElement()?.querySelector('.dd-pin')?.classList.toggle('is-active', k === id));
    list?.querySelectorAll('button').forEach(b => b.setAttribute('aria-current', b.dataset.id === id ? 'true' : 'false'));
    if (active) {
      active.innerHTML =
        '<span class="tag">' + p.place + ' · ' + p.country + (p.note ? ' · ' + p.note : '') + '</span>' +
        '<h3>' + p.title + '</h3>' +
        '<p>' + p.text + '</p>' +
        '<span class="tag">' + p.sector + ' · ' + p.duration + (p.via ? ' · przez ' + p.via : '') + '</span>';
    }
    if (fly) map.flyTo([p.lat, p.lon], Math.max(map.getZoom(), 6), { duration: .8 });
  }

  function applyFilter(value) {
    filter = value;
    filters?.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', b.dataset.filter === value ? 'true' : 'false'));
    const visible = PROJECTS.filter(p => value === 'all' || p.sector === value || p.cc === value);
    PROJECTS.forEach(p => {
      const on = visible.includes(p);
      if (on) markers[p.id].addTo(map); else map.removeLayer(markers[p.id]);
      list?.querySelector('button[data-id="' + p.id + '"]')?.classList.toggle('is-hidden', !on);
    });
    if (count) count.textContent = visible.length + (visible.length === 1 ? ' lokalizacja' : visible.length < 5 ? ' lokalizacje' : ' lokalizacji');
    if (visible.length) {
      const b = L.latLngBounds(visible.map(p => [p.lat, p.lon]));
      map.flyToBounds(b, { padding: [40, 40], duration: .8, maxZoom: 7 });
      if (!visible.find(p => p.id === current)) select(visible[0].id, false);
    }
  }

  filters?.querySelectorAll('button').forEach(b => b.addEventListener('click', () => applyFilter(b.dataset.filter)));

  // start
  map.fitBounds(L.latLngBounds(PROJECTS.map(p => [p.lat, p.lon])), { padding: [40, 40], maxZoom: 6 });
  select(PROJECTS[0].id, false);
  if (count) count.textContent = PROJECTS.length + ' lokalizacji';

  // Leaflet potrzebuje przeliczenia rozmiaru, gdy kontener pojawia się po załadowaniu
  setTimeout(() => map.invalidateSize(), 300);
  window.addEventListener('resize', () => map.invalidateSize());
})();
