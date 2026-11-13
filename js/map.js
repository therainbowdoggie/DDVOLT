/* DD Volt — map.js
   Mapa realizacji rysowana w SVG (bez kafli i kluczy API). Kontury krajów: js/map-data.js.
   Projekty i pinezki przychodzą ze strony w <script data-map-data> (generuje je tools/build.py
   z tools/content.py, więc danych nie edytuje się tutaj).
   Linie między punktami to najkrótsza sieć łącząca widoczne realizacje, rysowana od głównego projektu.
   Mapę można przesuwać palcem lub myszą, przybliżać dwoma palcami, przyciskami +/−, dwuklikiem
   albo Ctrl + kółko (zwykłe kółko przewija stronę). */
(function () {
  'use strict';
  var box = document.querySelector('[data-map]'), G = window.DDV_MAP;
  if (!box || !G) return;

  var NS = 'http://www.w3.org/2000/svg';
  var data = JSON.parse(box.querySelector('[data-map-data]').textContent);
  var svg = box.querySelector('[data-map-svg]'), stage = box.querySelector('.map-stage'), list = box.querySelector('.map-list');
  var items = [].slice.call(list.querySelectorAll('.map-item'));
  var chips = [].slice.call(box.querySelectorAll('[data-filter]'));
  var countEl = box.querySelector('.map-count'), resetBtn = box.querySelector('.map-reset');
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mobile = matchMedia('(max-width: 899px)');

  function el(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }

  /* ---------- warstwy ---------- */
  var gLand = el('g', { 'class': 'map-land' }, svg);
  var gLabels = el('g', { 'class': 'map-cl' }, svg);
  var gEdges = el('g', {}, svg);
  var gPins = el('g', {}, svg);

  var active = {};
  data.countries.forEach(function (c) { active[c.cc] = true; });
  Object.keys(G.c).sort(function (a, b) { return (active[a] ? 1 : 0) - (active[b] ? 1 : 0); }).forEach(function (cc) {
    el('path', { d: G.c[cc], 'class': active[cc] ? 'is-on' : '' }, gLand);
  });
  var labels = data.countries.map(function (c) {
    var g = el('g', {}, gLabels);
    el('text', {}, g).textContent = c.label;
    return { g: g, x: c.x, y: c.y };
  });

  /* ---------- pinezki ---------- */
  var points = [], byId = {};
  data.projects.forEach(function (p, pi) {
    byId[p.id] = { id: p.id, sector: p.sector, points: [], item: items.filter(function (i) { return i.getAttribute('data-id') === p.id; })[0] };
    p.points.forEach(function (pt) {
      var g = el('g', { 'class': 'pin' + (pt.approx ? ' is-approx' : '') }, gPins);
      var inner = el('g', { 'class': 'pin-in', style: '--n:' + points.length }, g);
      el('circle', { 'class': 'pin-halo', r: 10 }, inner);
      el('circle', { 'class': 'pin-dot', r: pt.approx ? 5.5 : 6.5 }, inner);
      var text = el('text', { 'class': 'pin-label', x: 14, y: 4.5 }, inner);
      text.textContent = pt.label;
      el('circle', { 'class': 'pin-hit', r: 22 }, g);
      var point = { id: p.id, x: pt.x, y: pt.y, g: g, text: text, order: pi };
      g.addEventListener('click', function () { select(p.id, { zoom: true, scroll: true }); });
      g.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') hover(p.id, true); });   // podpis pod kursorem tylko dla myszy
      g.addEventListener('pointerleave', function () { hover(p.id, false); });
      points.push(point);
      byId[p.id].points.push(point);
    });
  });

  /* ---------- kadr ---------- */
  var view = { x: 0, y: 0, w: G.w, h: G.h }, target = view, frame = 0, glide = 0;
  var MIN_W = 120;   // największe przybliżenie: szerokość kadru w jednostkach mapy
  var zoomIn = box.querySelector('[data-zoom="in"]'), zoomOut = box.querySelector('[data-zoom="out"]');
  function stopMotion() { cancelAnimationFrame(frame); cancelAnimationFrame(glide); glide = 0; }
  function maxW() { return Math.min(G.w, G.h * aspect()); }
  function bound(v) {   // kadr nie wychodzi poza mapę ani poza dozwolone przybliżenie
    var w = Math.max(MIN_W, Math.min(maxW(), v.w)), h = w / aspect();
    return { x: Math.min(Math.max(v.x, 0), G.w - w), y: Math.min(Math.max(v.y, 0), G.h - h), w: w, h: h };
  }
  function aspect() { return (stage.clientWidth || 1) / (stage.clientHeight || 1); }
  function fit(pts, pad, minW) {
    var x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity, a = aspect();
    pts.forEach(function (p) { x0 = Math.min(x0, p.x); x1 = Math.max(x1, p.x); y0 = Math.min(y0, p.y); y1 = Math.max(y1, p.y); });
    var w = Math.max((x1 - x0) * (1 + 2 * pad), minW), h = Math.max((y1 - y0) * (1 + 2 * pad), minW / a);
    if (w / h < a) w = h * a; else h = w / a;
    if (w > G.w) { w = G.w; h = w / a; }
    if (h > G.h) { h = G.h; w = h * a; }
    var cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    return { x: Math.min(Math.max(cx - w / 2, 0), G.w - w), y: Math.min(Math.max(cy - h / 2, 0), G.h - h), w: w, h: h };
  }
  function apply(v) {
    view = v;
    svg.setAttribute('viewBox', v.x.toFixed(2) + ' ' + v.y.toFixed(2) + ' ' + v.w.toFixed(2) + ' ' + v.h.toFixed(2));
    var k = v.w / (stage.clientWidth || 1), ks = k.toFixed(4);
    svg.style.setProperty('--k', ks);
    points.forEach(function (p) { p.g.setAttribute('transform', 'translate(' + p.x + ' ' + p.y + ') scale(' + ks + ')'); });
    labels.forEach(function (l) { l.g.setAttribute('transform', 'translate(' + l.x + ' ' + l.y + ') scale(' + ks + ')'); });
    if (zoomIn) { zoomIn.disabled = v.w <= MIN_W + .5; zoomOut.disabled = v.w >= maxW() - .5; }
  }
  function go(v, instant, ms) {
    target = v;
    stopMotion();
    points.forEach(function (p) { // etykieta po tej stronie pinezki, po której jest miejsce
      var left = (p.x - v.x) > v.w * .7;
      p.text.setAttribute('x', left ? -14 : 14);
      p.text.setAttribute('text-anchor', left ? 'end' : 'start');
    });
    if (instant || reduce) { apply(v); return; }
    var from = view, t0 = performance.now();
    (function step(now) {
      var t = Math.min(1, (now - t0) / (ms || 1100)), e = t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      apply({ x: from.x + (v.x - from.x) * e, y: from.y + (v.y - from.y) * e, w: from.w + (v.w - from.w) * e, h: from.h + (v.h - from.h) * e });
      if (t < 1) frame = requestAnimationFrame(step);
    })(t0);
  }

  /* ---------- stan ---------- */
  var filter = 'all', current = null, zoomed = false, manual = false;
  function shown(p) { return filter === 'all' || p.sector === filter; }
  function shownPoints() { return points.filter(function (p) { return shown(byId[p.id]); }); }
  function overview(instant) {
    zoomed = false; manual = false; resetBtn.hidden = true;
    var pts = shownPoints();
    if (pts.length) go(fit(pts, .34, 380), instant);
  }
  function focus(id, instant) {
    zoomed = true; manual = false; resetBtn.hidden = false;
    go(fit(byId[id].points, .9, 250), instant);
  }

  /* ---------- sieć połączeń (minimalne drzewo rozpinające) ---------- */
  function network() {
    while (gEdges.firstChild) gEdges.removeChild(gEdges.firstChild);
    var pts = shownPoints();
    if (pts.length < 2) return;
    var inTree = [pts[0]], rest = pts.slice(1), depth = new Map([[pts[0], 0]]), made = [];
    while (rest.length) {
      var best = null;
      inTree.forEach(function (a) {
        rest.forEach(function (b, bi) {
          var dd = (a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y);
          if (!best || dd < best.d) best = { a: a, b: b, bi: bi, d: dd };
        });
      });
      depth.set(best.b, depth.get(best.a) + 1);
      inTree.push(best.b); rest.splice(best.bi, 1);
      var a = best.a, b = best.b, dx = b.x - a.x, dy = b.y - a.y, bend = (made.length % 2 ? -1 : 1) * .13;
      var path = 'M' + a.x + ' ' + a.y + 'Q' + ((a.x + b.x) / 2 - dy * bend).toFixed(1) + ' ' + ((a.y + b.y) / 2 + dx * bend).toFixed(1) + ' ' + b.x + ' ' + b.y;
      var edge = el('path', { d: path, 'class': 'map-edge', pathLength: 1, style: '--depth:' + depth.get(a) + ';stroke-dashoffset:1' }, gEdges);
      el('path', { d: path, 'class': 'map-flow' }, gEdges);
      made.push(edge);
    }
    void gEdges.getBoundingClientRect(); // start przejścia: linia rysuje się od punktu wyjścia
    made.forEach(function (e) { e.style.strokeDashoffset = ''; });
  }

  /* ---------- wybór ---------- */
  function hover(id, on) {
    byId[id].points.forEach(function (p) { p.g.classList.toggle('is-hover', on); });
  }
  var quiet = 0; // podczas programowego przewijania karuzeli nie reagujemy na jej scroll
  function select(id, opt) {
    opt = opt || {};
    var same = current === id;
    current = id;
    points.forEach(function (p) { p.g.classList.toggle('is-active', p.id === id); if (p.id === id) gPins.appendChild(p.g); });
    items.forEach(function (it) {
      var on = it.getAttribute('data-id') === id;
      it.classList.toggle('is-active', on);
      it.querySelector('.map-item-btn').setAttribute('aria-expanded', String(on || mobile.matches));
    });
    if (opt.zoom) focus(id);
    if (opt.scroll) {
      var it = byId[id].item;
      if (mobile.matches) {
        quiet = Date.now() + 700;
        list.scrollTo({ left: it.offsetLeft - (list.clientWidth - it.offsetWidth) / 2, behavior: reduce ? 'auto' : 'smooth' });
      } else if (!same) {
        setTimeout(function () {
          var top = it.offsetTop;
          if (top < list.scrollTop || top + it.offsetHeight > list.scrollTop + list.clientHeight) list.scrollTo({ top: Math.max(0, top - 8), behavior: reduce ? 'auto' : 'smooth' });
        }, 300);
      }
    }
  }

  items.forEach(function (it) {
    var id = it.getAttribute('data-id');
    it.querySelector('.map-item-btn').addEventListener('click', function () {
      if (!mobile.matches && current === id && zoomed) { overview(); return; }
      select(id, { zoom: true, scroll: mobile.matches });
    });
    it.addEventListener('pointerenter', function () { hover(id, true); });
    it.addEventListener('pointerleave', function () { hover(id, false); });
  });
  resetBtn.addEventListener('click', function () { overview(); });

  // karuzela na telefonie: przesunięcie karty wybiera projekt i przybliża mapę
  var settle;
  list.addEventListener('scroll', function () {
    if (!mobile.matches || Date.now() < quiet) return;
    clearTimeout(settle);
    settle = setTimeout(function () {
      var mid = list.scrollLeft + list.clientWidth / 2, best = null, bd = Infinity;
      items.forEach(function (it) {
        if (it.classList.contains('is-off')) return;
        var dd = Math.abs(it.offsetLeft + it.offsetWidth / 2 - mid);
        if (dd < bd) { bd = dd; best = it; }
      });
      if (best && best.getAttribute('data-id') !== current) select(best.getAttribute('data-id'), { zoom: true });
    }, 110);
  }, { passive: true });

  /* ---------- filtr ---------- */
  function plural(n) {
    var f = data.meta.forms;
    if (data.meta.lang !== 'pl') return n === 1 ? f[0] : f[1];
    if (n === 1) return f[0];
    var d10 = n % 10, d100 = n % 100;
    return d10 >= 2 && d10 <= 4 && (d100 < 12 || d100 > 14) ? f[1] : f[2];
  }
  function setFilter(value, instant) {
    filter = value;
    chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.getAttribute('data-filter') === value)); });
    var first = null;
    data.projects.forEach(function (p) {
      var on = shown(p), o = byId[p.id];
      o.item.classList.toggle('is-off', !on);
      o.points.forEach(function (pt) { pt.g.classList.toggle('is-off', !on); });
      if (on && !first) first = p.id;
    });
    var n = shownPoints().length;
    countEl.textContent = n + ' ' + plural(n);
    network();
    if (first && (!current || !shown(byId[current]))) select(first);
    if (mobile.matches) { quiet = Date.now() + 400; list.scrollTo({ left: 0 }); if (first) select(first); }
    overview(instant);
  }
  chips.forEach(function (c) { c.addEventListener('click', function () { setFilter(c.getAttribute('data-filter')); }); });

  /* ---------- przesuwanie i przybliżanie ---------- */
  function byHand() { zoomed = true; manual = true; resetBtn.hidden = false; }
  function zoomBy(factor, px, py, smooth) {   // px, py: punkt sceny (w pikselach), który zostaje pod palcem
    var base = smooth ? target : view, r = stage.getBoundingClientRect();
    var w = Math.max(MIN_W, Math.min(maxW(), base.w / factor)), h = w / aspect();
    var v = bound({ x: base.x + (px / r.width) * (base.w - w), y: base.y + (py / r.height) * (base.h - h), w: w, h: h });
    byHand();
    if (smooth) go(v, false, 420); else { stopMotion(); target = v; apply(v); }
  }
  var ptrs = new Map(), origin = null, dragging = false, swallow = 0, vx = 0, vy = 0, lastT = 0;
  function capture(id) { try { svg.setPointerCapture(id); } catch (err) {} }
  function startDrag() {
    if (dragging) return;
    dragging = true; stopMotion(); target = view; byHand();
    svg.classList.add('is-dragging');
    points.forEach(function (pt) { pt.g.classList.remove('is-hover'); });
  }
  svg.addEventListener('pointerdown', function (e) {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (ptrs.size === 1) { origin = { x: e.clientX, y: e.clientY }; dragging = false; vx = vy = 0; if (glide) stopMotion(); }
    else if (ptrs.size === 2) { startDrag(); ptrs.forEach(function (_, id) { capture(id); }); }
  });
  svg.addEventListener('pointermove', function (e) {
    var p = ptrs.get(e.pointerId);
    if (!p) return;
    var r = stage.getBoundingClientRect(), k;
    if (ptrs.size === 1) {
      if (!dragging) {   // drobne drgnięcie palca to nadal stuknięcie w pinezkę
        if (Math.hypot(e.clientX - origin.x, e.clientY - origin.y) < 7) return;
        startDrag(); capture(e.pointerId);
        p.x = e.clientX; p.y = e.clientY; lastT = e.timeStamp;
        return;
      }
      var dx = e.clientX - p.x, dy = e.clientY - p.y;
      p.x = e.clientX; p.y = e.clientY;
      k = view.w / (r.width || 1);
      var want = { x: view.x - dx * k, y: view.y - dy * k, w: view.w, h: view.h }, v = bound(want);
      apply(v); target = v;
      // na górnej i dolnej krawędzi mapy ruch palca przewija stronę, więc mapa nie blokuje przewijania
      if (e.pointerType === 'touch') { var rest = (want.y - v.y) / k; if (Math.abs(rest) > .5) window.scrollBy(0, rest); }
      var dt = Math.max(1, e.timeStamp - lastT); lastT = e.timeStamp;
      vx = .75 * (dx / dt) + .25 * vx; vy = .75 * (dy / dt) + .25 * vy;
    } else if (ptrs.size === 2) {
      var o = null;
      ptrs.forEach(function (q, id) { if (id !== e.pointerId) o = q; });
      var d0 = Math.hypot(p.x - o.x, p.y - o.y), m0x = (p.x + o.x) / 2, m0y = (p.y + o.y) / 2;
      p.x = e.clientX; p.y = e.clientY;
      var d1 = Math.hypot(p.x - o.x, p.y - o.y), m1x = (p.x + o.x) / 2, m1y = (p.y + o.y) / 2;
      var w = Math.max(MIN_W, Math.min(maxW(), view.w * d0 / Math.max(d1, 1))), h = w / aspect();
      var ax = view.x + (m0x - r.left) / r.width * view.w, ay = view.y + (m0y - r.top) / r.height * view.h;  // punkt mapy między palcami
      var nv = bound({ x: ax - (m1x - r.left) / r.width * w, y: ay - (m1y - r.top) / r.height * h, w: w, h: h });
      apply(nv); target = nv;
    }
  });
  function coast() {   // krótki wybieg po puszczeniu palca
    var last = performance.now();
    glide = requestAnimationFrame(function step(now) {
      var dt = Math.min(40, now - last), k = view.w / (stage.clientWidth || 1); last = now;
      var v = bound({ x: view.x - vx * dt * k, y: view.y - vy * dt * k, w: view.w, h: view.h });
      apply(v); target = v;
      var f = Math.pow(.92, dt / 16); vx *= f; vy *= f;
      glide = Math.hypot(vx, vy) > .03 ? requestAnimationFrame(step) : 0;
    });
  }
  function release(e) {
    if (!ptrs.has(e.pointerId)) return;
    ptrs.delete(e.pointerId);
    if (ptrs.size) { vx = vy = 0; return; }   // z dwóch palców został jeden: przesuwamy dalej bez skoku
    svg.classList.remove('is-dragging');
    if (dragging) {
      swallow = Date.now() + 400;   // koniec przeciągania nie jest kliknięciem w pinezkę
      if (!reduce && e.type === 'pointerup' && e.timeStamp - lastT < 90 && Math.hypot(vx, vy) > .2) coast();
    }
    dragging = false;
  }
  svg.addEventListener('pointerup', release);
  svg.addEventListener('pointercancel', release);
  svg.addEventListener('click', function (e) { if (Date.now() < swallow) { e.stopPropagation(); e.preventDefault(); } }, true);
  svg.addEventListener('dblclick', function (e) {
    var r = stage.getBoundingClientRect();
    zoomBy(1.9, e.clientX - r.left, e.clientY - r.top, true);
  });
  svg.addEventListener('wheel', function (e) {
    if (!e.ctrlKey && !e.metaKey) return;   // zwykłe kółko zostaje dla przewijania strony
    e.preventDefault();
    var r = stage.getBoundingClientRect();
    zoomBy(Math.exp(-Math.max(-30, Math.min(30, e.deltaY)) * .012), e.clientX - r.left, e.clientY - r.top, false);   // jeden ząbek kółka to najwyżej ok. 1,4×
  }, { passive: false });
  if (zoomIn) {
    zoomIn.addEventListener('click', function () { zoomBy(1.7, stage.clientWidth / 2, stage.clientHeight / 2, true); });
    zoomOut.addEventListener('click', function () { zoomBy(1 / 1.7, stage.clientWidth / 2, stage.clientHeight / 2, true); });
  }

  /* ---------- start ---------- */
  setFilter('all', true);
  function refit() {
    if (manual) { var v = bound(view); target = v; apply(v); }   // kadr ustawiony ręcznie zostaje
    else if (zoomed && current) focus(current, true);
    else overview(true);
  }
  if ('ResizeObserver' in window) new ResizeObserver(refit).observe(stage); else window.addEventListener('resize', refit);
  mobile.addEventListener('change', function () { if (current) select(current); refit(); });

  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { box.classList.add('is-live'); io.disconnect(); }
    }, { threshold: .25 });
    io.observe(stage);
  } else {
    box.classList.add('is-live');
  }
})();
