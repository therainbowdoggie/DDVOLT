/* DD Volt — map.js
   Mapa realizacji rysowana w SVG (bez kafli i kluczy API). Kontury krajów: js/map-data.js.
   Projekty i pinezki przychodzą ze strony w <script data-map-data> (generuje je tools/build.py
   z tools/content.py, więc danych nie edytuje się tutaj).
   Linie między punktami to najkrótsza sieć łącząca widoczne realizacje, rysowana od głównego projektu. */
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
      g.addEventListener('pointerenter', function () { hover(p.id, true); });
      g.addEventListener('pointerleave', function () { hover(p.id, false); });
      points.push(point);
      byId[p.id].points.push(point);
    });
  });

  /* ---------- kadr ---------- */
  var view = { x: 0, y: 0, w: G.w, h: G.h }, target = view, frame = 0;
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
  }
  function go(v, instant) {
    target = v;
    cancelAnimationFrame(frame);
    points.forEach(function (p) { // etykieta po tej stronie pinezki, po której jest miejsce
      var left = (p.x - v.x) > v.w * .7;
      p.text.setAttribute('x', left ? -14 : 14);
      p.text.setAttribute('text-anchor', left ? 'end' : 'start');
    });
    if (instant || reduce) { apply(v); return; }
    var from = view, t0 = performance.now();
    (function step(now) {
      var t = Math.min(1, (now - t0) / 1100), e = t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      apply({ x: from.x + (v.x - from.x) * e, y: from.y + (v.y - from.y) * e, w: from.w + (v.w - from.w) * e, h: from.h + (v.h - from.h) * e });
      if (t < 1) frame = requestAnimationFrame(step);
    })(t0);
  }

  /* ---------- stan ---------- */
  var filter = 'all', current = null, zoomed = false;
  function shown(p) { return filter === 'all' || p.sector === filter; }
  function shownPoints() { return points.filter(function (p) { return shown(byId[p.id]); }); }
  function overview(instant) {
    zoomed = false; resetBtn.hidden = true;
    var pts = shownPoints();
    if (pts.length) go(fit(pts, .34, 380), instant);
  }
  function focus(id, instant) {
    zoomed = true; resetBtn.hidden = false;
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

  /* ---------- start ---------- */
  setFilter('all', true);
  function refit() { if (zoomed && current) focus(current, true); else overview(true); }
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
