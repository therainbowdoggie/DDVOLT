/* DD Volt — main.js
   Ekran startowy, ścieżka (firmy / fachowcy), menu, animacje wejścia, fale w hero,
   liczniki, efekty przewijania, FAQ, telefon, formularz, motyw. Bez zależności. */
(function () {
  'use strict';
  window.DDV_READY = true;

  var d = document, html = d.documentElement;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, r) { return (r || d).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };
  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };

  function storage(kind) {
    return {
      get: function (k) { try { return window[kind].getItem(k); } catch (e) { return null; } },
      set: function (k, v) { try { window[kind].setItem(k, v); } catch (e) {} },
      del: function (k) { try { window[kind].removeItem(k); } catch (e) {} }
    };
  }
  var local = storage('localStorage'), session = storage('sessionStorage');

  /* ---------------------------------------------------------- powiadomienie */
  var toastEl = $('[data-toast]'), toastTimer;
  function toast(text) {
    if (!toastEl) return;
    toastEl.textContent = text;
    toastEl.classList.add('is-on');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('is-on'); }, 2600);
  }

  /* ---------------------------------------------------------- ścieżka: firmy / fachowcy */
  var lock = html.getAttribute('data-audience-lock');
  function audience() { return html.getAttribute('data-audience') === 'fachowcy' ? 'fachowcy' : 'firmy'; }
  function syncSwitches() {
    var a = audience();
    $$('[data-audience-switch] button').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-value') === a));
    });
  }
  function setAudience(value) {
    if (value === audience()) return;
    html.setAttribute('data-audience', value);
    if (!lock) local.set('dd-audience', value);
    syncSwitches();
    // nagłówki dla nowej ścieżki wjeżdżają od nowa
    $$('.split[data-for="' + value + '"]').forEach(function (el) {
      el.classList.remove('in');
      void el.offsetWidth;
      el.classList.add('in');
    });
    d.dispatchEvent(new CustomEvent('ddv:audience', { detail: value }));
    requestScroll();
  }
  $$('[data-audience-switch] button').forEach(function (b) {
    b.addEventListener('click', function () { setAudience(b.getAttribute('data-value')); });
  });
  syncSwitches();
  (function () { // wejście z linku ?dla=fachowcy / ?for=jobs zapamiętujemy jak kliknięcie
    try {
      var q = new URLSearchParams(location.search), p = q.get('dla') || q.get('for');
      p = p === 'jobs' ? 'fachowcy' : p === 'companies' ? 'firmy' : p;
      if (!lock && (p === 'fachowcy' || p === 'firmy')) local.set('dd-audience', p);
    } catch (e) {}
  })();

  /* ---------------------------------------------------------- menu mobilne */
  var menu = $('#menu'), menuBtn = $('.menu-btn');
  var outside = $$('main, .site-footer, .dock');
  function setMenu(open) {
    if (!menu || !menuBtn) return;
    menu.classList.toggle('is-open', open);
    menu.inert = !open;
    html.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', menuBtn.getAttribute(open ? 'data-close' : 'data-open'));
    outside.forEach(function (el) { el.inert = open; });
    if (!open) refreshDock();
  }
  if (menu && menuBtn) {
    menuBtn.addEventListener('click', function () { setMenu(!menu.classList.contains('is-open')); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('is-open')) { setMenu(false); menuBtn.focus(); }
    });
    matchMedia('(min-width: 1024px)').addEventListener('change', function (e) { if (e.matches) setMenu(false); });
  }

  /* ---------------------------------------------------------- motyw */
  var themeBtns = $$('[data-theme-toggle]');
  function syncTheme() {
    var dark = html.getAttribute('data-theme') === 'dark';
    themeBtns.forEach(function (b) { b.setAttribute('aria-checked', String(dark)); });
  }
  themeBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      local.set('dd-theme', next);
      syncTheme();
    });
  });
  syncTheme();

  /* ---------------------------------------------------------- telefon
     Na telefonie link otwiera wybieranie numeru. Na komputerze pierwsze kliknięcie
     pokazuje numer i kopiuje go do schowka, kolejne działa jak zwykły link tel: */
  $$('[data-phone]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (!finePointer || a.getAttribute('data-shown')) return;
      e.preventDefault();
      var number = a.getAttribute('data-phone');
      var label = $('[data-phone-label]', a);
      if (label) label.textContent = number;
      a.setAttribute('data-shown', '1');
      var said = (toastEl && toastEl.getAttribute('data-copied')) || '';
      var done = function () { toast(said ? said + ': ' + number : number); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(number).then(done, function () { toast(number); });
      else toast(number);
    });
  });

  /* ---------------------------------------------------------- poświata pod kursorem na kartach */
  if (finePointer) {
    $$('[data-spot]').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }

  /* ---------------------------------------------------------- FAQ: płynne rozwijanie */
  $$('.qa').forEach(function (qa) {
    var summary = $('summary', qa), body = $('.qa-body', qa), anim = null;
    if (!summary || !body || reduce || !body.animate) return;
    summary.addEventListener('click', function (e) {
      e.preventDefault();
      if (anim) anim.cancel();
      var closing = qa.open && !qa.classList.contains('is-closing');
      if (closing) {
        qa.classList.add('is-closing');
        anim = body.animate({ height: [body.offsetHeight + 'px', '0px'], opacity: [1, 0] }, { duration: 380, easing: 'cubic-bezier(.4,0,.2,1)' });
        anim.onfinish = function () { qa.open = false; qa.classList.remove('is-closing'); anim = null; };
        anim.oncancel = function () { qa.classList.remove('is-closing'); };
      } else {
        qa.classList.remove('is-closing');
        qa.open = true;
        anim = body.animate({ height: ['0px', body.offsetHeight + 'px'], opacity: [0, 1] }, { duration: 520, easing: 'cubic-bezier(.16,1,.3,1)' });
        anim.onfinish = function () { anim = null; };
      }
    });
  });

  /* ---------------------------------------------------------- liczniki (cyfry przewijają się jak w liczniku) */
  function buildOdometer(el) {
    var text = el.getAttribute('data-count');
    if (reduce || !/^\d+$/.test(text)) return null;
    var html_ = '<span class="sr-only">' + text + '</span><span class="odo" aria-hidden="true">';
    for (var i = 0; i < text.length; i++) {
      html_ += '<span class="odo-col"><span class="odo-strip" style="--j:' + i + '">';
      for (var n = 0; n < 10; n++) html_ += '<span data-d="' + n + '"></span>'; // cyfry z CSS: nie trafiają do tekstu strony
      html_ += '</span></span>';
    }
    el.innerHTML = html_ + '</span>';
    return function () {
      $$('.odo-strip', el).forEach(function (strip, idx) { strip.style.transform = 'translateY(-' + text.charAt(idx) + 'em)'; });
    };
  }
  var statGroups = $$('[data-stats]').map(function (group) {
    return { el: group, run: $$('[data-count]', group).map(buildOdometer).filter(Boolean) };
  });

  /* ---------------------------------------------------------- fale w hero: trzy fazy prądu przemiennego */
  var hero = $('[data-hero]');
  var wave = (function () {
    var canvas = $('[data-wave]');
    if (!canvas || !canvas.getContext) return null;
    var ctx = canvas.getContext('2d');
    var W = 0, H = 0, raf = 0, visible = false, started = false, power = reduce ? 1 : 0, startAt = 0, mx = -1, mxTarget = -1, fade = 1, shown = -1;
    var PH = [0, 2 * Math.PI / 3, 4 * Math.PI / 3];
    var LINES = [
      { i: 2, rgb: '110,110,115', w: 1.6, a: 1 },
      { i: 1, rgb: '245,245,247', w: 1.6, a: .9 },
      { i: 0, rgb: '242,85,0', w: 2.4, a: 1, glow: true }
    ];
    function size() {
      var r = canvas.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
      W = r.width; H = r.height;
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      if (!raf) draw(performance.now());
    }
    function trace(line, t, amp, k) {
      ctx.beginPath();
      for (var x = -6; x <= W + 6; x += 5) {
        var boost = mx >= 0 ? 1 + .26 * Math.exp(-Math.pow((x - mx) / 180, 2)) : 1;
        var y = H * .45 + Math.sin(k * x - t * 1.25 + PH[line.i]) * amp * boost;
        if (x === -6) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
    }
    function draw(now) {
      var t = reduce ? 1.4 : now / 1000;
      if (started && power < 1) { var p = clamp((now - startAt) / 2200); power = 1 - Math.pow(1 - p, 3); }
      if (mxTarget < 0) mx = -1; else mx = mx < 0 ? mxTarget : mx + (mxTarget - mx) * .12;
      var amp = Math.min(H * .34, 112) * power * fade;
      var k = 2 * Math.PI / Math.max(360, Math.min(820, W * .55));
      ctx.clearRect(0, 0, W, H);
      ctx.lineJoin = ctx.lineCap = 'round';
      LINES.forEach(function (l) {
        trace(l, t, amp, k);
        if (l.glow) {
          ctx.strokeStyle = 'rgba(' + l.rgb + ',' + (.1 * power) + ')'; ctx.lineWidth = 14; ctx.stroke();
          ctx.strokeStyle = 'rgba(' + l.rgb + ',' + (.22 * power) + ')'; ctx.lineWidth = 6; ctx.stroke();
        }
        ctx.strokeStyle = 'rgba(' + l.rgb + ',' + l.a + ')'; ctx.lineWidth = l.w; ctx.stroke();
      });
      if (hero && power !== shown) { shown = power; hero.style.setProperty('--power', power.toFixed(3)); }
    }
    function loop(now) { draw(now); raf = visible && !reduce ? requestAnimationFrame(loop) : 0; }
    function play() { if (!raf && visible && !reduce && !d.hidden) raf = requestAnimationFrame(loop); }
    new IntersectionObserver(function (es) { visible = es[0].isIntersecting; play(); }).observe(canvas);
    d.addEventListener('visibilitychange', play);
    window.addEventListener('resize', size);
    if (hero && finePointer) {
      hero.addEventListener('pointermove', function (e) { mxTarget = e.clientX - canvas.getBoundingClientRect().left; });
      hero.addEventListener('pointerleave', function () { mxTarget = -1; });
    }
    if (hero && !reduce) hero.style.setProperty('--power', '0');
    size();
    return {
      start: function () { started = true; startAt = performance.now(); play(); if (reduce) draw(0); },
      fade: function (v) { fade = v; }
    };
  })();

  /* ---------------------------------------------------------- efekty powiązane z przewijaniem */
  var header = $('[data-header]');
  var stepSets = $$('[data-steps]').map(function (el) { return { el: el, steps: $$('.step', el) }; });
  var litSets = $$('[data-lit]').map(function (el) { return { el: el, words: $$('.lw', el), n: -1 }; });
  var dock = $('[data-dock]'), dockBlock = 0, ticking = false;
  var vertical = matchMedia('(max-width: 799px)');

  function refreshDock() {
    if (!dock) return;
    var on = window.scrollY > window.innerHeight * .6 && !dockBlock && !html.classList.contains('menu-open');
    dock.classList.toggle('is-on', on);
    dock.inert = !on;
    html.classList.toggle('dock-on', on);
  }
  if (dock) {
    dock.inert = true;
    var seen = new Set();
    var dockIO = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) seen.add(e.target); else seen.delete(e.target); });
      dockBlock = seen.size; refreshDock();
    }, { rootMargin: '0px 0px -10% 0px' });
    $$('.cta, .site-footer').forEach(function (el) { dockIO.observe(el); });
  }

  function onScroll() {
    ticking = false;
    var y = window.scrollY || 0, vh = window.innerHeight;
    var max = html.scrollHeight - vh;
    if (header) {
      header.classList.toggle('is-scrolled', y > 8);
      header.style.setProperty('--scroll', max > 0 ? clamp(y / max).toFixed(4) : '0');
    }
    if (hero) {
      var hp = clamp(y / (hero.offsetHeight || 1));
      hero.style.setProperty('--hero-p', hp.toFixed(3));
      if (wave) wave.fade(1 - hp * .65);
    }
    stepSets.forEach(function (s) {
      var r = s.el.getBoundingClientRect();
      if (r.top > vh + 200) return;
      var p = reduce ? 1 : Math.max(s.p || 0, clamp((vh * .92 - r.top) / (r.height + vh * .14)));
      s.p = p;
      s.el.style.setProperty('--p', p.toFixed(4));
      var isV = vertical.matches, end = isV ? r.top + p * r.height : r.left + p * r.width;
      s.steps.forEach(function (st) {
        var n = $('.step-node', st).getBoundingClientRect();
        var c = isV ? n.top + n.height / 2 : n.left + n.width / 2;
        st.classList.toggle('is-on', p > 0 && end >= c - 4);
      });
    });
    litSets.forEach(function (s) {
      var r = s.el.getBoundingClientRect();
      if (r.top > vh + 200) return;
      var p = reduce ? 1 : clamp((vh * .94 - r.top) / (r.height + vh * .2));
      var n = Math.max(s.n, Math.round(p * (s.words.length + 1)));
      if (n === s.n) return;
      s.n = n;
      s.words.forEach(function (w, i) { w.classList.toggle('is-lit', i < n); });
    });
    refreshDock();
  }
  function requestScroll() { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }
  window.addEventListener('scroll', requestScroll, { passive: true });
  window.addEventListener('resize', requestScroll);

  /* ---------------------------------------------------------- wejścia elementów */
  function startReveals() {
    if (!('IntersectionObserver' in window)) { html.classList.add('no-anim'); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        el.classList.add('in');
        io.unobserve(el);
        // po wejściu zdejmujemy opóźnienia, żeby hover na kartach reagował od razu
        setTimeout(function () { el.classList.add('done'); }, 1700);
      });
    }, { rootMargin: '0px 0px -7% 0px', threshold: .08 });
    $$('.split, .rise, .reveal, .stagger').forEach(function (el) { io.observe(el); });

    var statIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        statIO.unobserve(e.target);
        statGroups.forEach(function (g) {
          if (g.el === e.target) setTimeout(function () { g.run.forEach(function (fn) { fn(); }); }, 350);
        });
      });
    }, { threshold: .35 });
    statGroups.forEach(function (g) { statIO.observe(g.el); });

    var artIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { e.target.classList.toggle('is-live', e.isIntersecting); });
    }, { threshold: .25 });
    $$('[data-art]').forEach(function (el) { artIO.observe(el); });
  }

  /* ---------------------------------------------------------- start: z ekranem powitalnym albo bez */
  function start() {
    html.classList.add('is-ready');
    startReveals();
    if (wave) wave.start();
    onScroll();
  }
  var boot = $('.boot');
  if (html.classList.contains('is-booting') && boot) {
    session.set('dd-boot', '1');
    setTimeout(function () {
      boot.classList.add('is-leaving');
      start();
      setTimeout(function () { html.classList.remove('is-booting'); }, 620);
    }, Math.max(250, 1450 - performance.now()));
  } else {
    html.classList.remove('is-booting');
    requestAnimationFrame(start);
  }

  /* ---------------------------------------------------------- formularz kontaktowy */
  var form = $('[data-form]');
  if (form) (function () {
    var msg = JSON.parse($('[data-form-msg]', form).textContent);
    var fieldsBox = $('.form-fields', form), doneBox = $('[data-done]', form), status = $('[data-status]', form);
    var submit = $('button[type="submit"]', form), draftNote = $('[data-draft]', form);
    var checked = $$('[data-field]', form);
    var KEY = 'dd-form', saveTimer;

    var rules = {
      name: function (el) { return el.value.trim().length >= 2; },
      phone: function (el) { return el.value.replace(/\D/g, '').length >= 7; },
      email: function (el) { var v = el.value.trim(); return !v || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); },
      consent: function (el) { return el.checked; }
    };
    function validate(field, show) {
      var el = $('input', field), ok = rules[field.getAttribute('data-field')](el);
      if (show || field.classList.contains('is-invalid')) {
        field.classList.toggle('is-invalid', !ok);
        if (ok) el.removeAttribute('aria-invalid'); else el.setAttribute('aria-invalid', 'true');
        $('.error', field).hidden = ok;
      }
      return ok;
    }
    checked.forEach(function (field) {
      var el = $('input', field);
      el.addEventListener('blur', function () { if (el.type === 'checkbox' || el.value.trim()) validate(field, true); });
      el.addEventListener(el.type === 'checkbox' ? 'change' : 'input', function () { validate(field, false); });
    });
    var phone = form.elements.telefon;
    phone.addEventListener('input', function () {
      var clean = phone.value.replace(/[^\d+\s()-]/g, '');
      if (clean !== phone.value) phone.value = clean;
    });
    phone.addEventListener('blur', function () { phone.value = phone.value.trim(); });

    /* telefon: e-mail, firma, lokalizacja i termin chowają się pod jednym przyciskiem */
    var more = $('[data-more]', form), moreBtn = $('[data-more-btn]', form), moreIn = $('.form-more-in', form);
    var small = matchMedia('(max-width: 599px)'), openTimer;
    function moreFilled() { return $$('input', more).some(function (i) { return !i.disabled && i.value.trim(); }); }
    function setMore(open) {
      clearTimeout(openTimer);
      more.classList.toggle('is-collapsed', !open);
      more.classList.remove('is-open');
      moreIn.inert = !open;
      moreBtn.hidden = open || !small.matches;
      moreBtn.setAttribute('aria-expanded', String(open));
      if (open) openTimer = setTimeout(function () { more.classList.add('is-open'); }, 600); // po animacji: nie przycinaj obrysu fokusu
    }
    moreBtn.addEventListener('click', function () {
      setMore(true);
      var first = $('input:not([disabled])', more);
      if (first) first.focus({ preventScroll: true });
    });
    more.addEventListener('change', function () { if (more.classList.contains('is-collapsed') && moreFilled()) setMore(true); }); // np. autouzupełnianie
    small.addEventListener('change', function () { setMore(!small.matches || moreFilled() || !more.classList.contains('is-collapsed')); });

    function syncGroups() {
      var a = audience();
      $$('[data-group]', form).forEach(function (g) {
        var off = g.getAttribute('data-group') !== a;
        $$('input, textarea', g).forEach(function (i) { i.disabled = off; });
      });
      form.elements.rodzaj.value = a === 'fachowcy' ? msg.topic_fach : msg.topic_firmy;
      var note = form.elements.wiadomosc;   // podpowiedź w polu zależy od ścieżki
      note.placeholder = note.getAttribute('data-ph-' + a) || '';
    }
    d.addEventListener('ddv:audience', function () { syncGroups(); queueSave(); });

    /* kopia robocza: nic nie ginie po odświeżeniu albo przypadkowym zamknięciu karty */
    function eachInput(fn) {
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || el.name.charAt(0) === '_' || el.type === 'hidden' || el.type === 'submit' || el.name === 'zgoda') return;
        fn(el);
      });
    }
    function collect() {
      var o = {}, any = false;
      eachInput(function (el) {
        if (el.type === 'checkbox') { o[el.name] = o[el.name] || []; if (el.checked) { o[el.name].push(el.value); any = true; } }
        else if (el.type === 'radio') { if (el.checked) { o[el.name] = el.value; any = true; } }
        else { o[el.name] = el.value; if (el.value.trim()) any = true; }
      });
      return any ? o : null;
    }
    function queueSave() {
      clearTimeout(saveTimer);
      saveTimer = setTimeout(function () { var o = collect(); if (o) local.set(KEY, JSON.stringify(o)); else local.del(KEY); }, 400);
    }
    function restore() {
      var o; try { o = JSON.parse(local.get(KEY) || 'null'); } catch (e) { o = null; }
      if (!o) return false;
      eachInput(function (el) {
        var v = o[el.name];
        if (v == null) return;
        if (el.type === 'checkbox') el.checked = v.indexOf(el.value) > -1;
        else if (el.type === 'radio') el.checked = v === el.value;
        else el.value = v;
      });
      return true;
    }
    form.addEventListener('input', queueSave);
    form.addEventListener('change', queueSave);
    if (restore() && draftNote) draftNote.hidden = false;
    setMore(!small.matches || moreFilled());
    $$('[data-draft-clear]', form).forEach(function (b) {
      b.addEventListener('click', function () { clearTimeout(saveTimer); local.del(KEY); form.reset(); syncGroups(); draftNote.hidden = true; clearErrors(); setMore(!small.matches); });
    });

    // stanowisko z linku „Aplikuj” przy ofercie pracy
    try {
      var q = new URLSearchParams(location.search), role = q.get('stanowisko') || q.get('role');
      if (role) $$('input[data-role]', form).forEach(function (r) { if (r.getAttribute('data-role') === role) r.checked = true; });
    } catch (e) {}
    syncGroups();

    function clearErrors() {
      checked.forEach(function (f) { f.classList.remove('is-invalid'); $('input', f).removeAttribute('aria-invalid'); $('.error', f).hidden = true; });
      say('', false);
    }
    function say(text, isError) { status.textContent = text; status.classList.toggle('is-error', !!isError); }
    function busy(on) { submit.disabled = on; submit.classList.toggle('is-busy', on); if (on) say(msg.sending, false); }
    function subject() { return (audience() === 'fachowcy' ? msg.mail_subject_fach : msg.mail_subject_firmy) + ': ' + form.elements.imie.value.trim(); }
    function labelOf(el) {
      var box = el.closest('.field'), lab = box && $('label:not(.pick):not(.check), legend', box);
      if (!lab) return el.name;
      var c = lab.cloneNode(true);
      $$('.opt, [data-for="' + (audience() === 'fachowcy' ? 'firmy' : 'fachowcy') + '"]', c).forEach(function (n) { n.remove(); });
      return c.textContent.replace(/\s+/g, ' ').trim();
    }
    function viaMail() {
      var lines = [form.elements.rodzaj.value, ''], groups = {};
      eachInput(function (el) {
        if (el.disabled) return;
        if ((el.type === 'checkbox' || el.type === 'radio')) { if (el.checked) (groups[el.name] = groups[el.name] || { label: labelOf(el), v: [] }).v.push(el.value); return; }
        if (el.value.trim()) lines.push(labelOf(el) + ': ' + el.value.trim());
      });
      Object.keys(groups).forEach(function (k) { lines.push(groups[k].label + ': ' + groups[k].v.join(', ')); });
      var link = d.createElement('a');
      link.href = 'mailto:' + msg.email + '?subject=' + encodeURIComponent(subject()) + '&body=' + encodeURIComponent(lines.join('\n'));
      link.hidden = true;
      form.appendChild(link); link.click(); link.remove();
      say(msg.mailto, false);
    }
    function success() {
      clearTimeout(saveTimer); local.del(KEY);
      fieldsBox.hidden = true; doneBox.hidden = false; if (draftNote) draftNote.hidden = true;
      doneBox.focus({ preventScroll: true });
      var top = form.getBoundingClientRect().top;
      if (top < 70) window.scrollTo({ top: window.scrollY + top - 90, behavior: reduce ? 'auto' : 'smooth' });
    }
    $$('[data-again]', form).forEach(function (b) {
      b.addEventListener('click', function () { form.reset(); syncGroups(); clearErrors(); setMore(!small.matches); doneBox.hidden = true; fieldsBox.hidden = false; form.elements.imie.focus(); });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = checked.filter(function (f) { return !validate(f, true); });
      if (bad.length) { if (more.contains(bad[0])) setMore(true); $('input', bad[0]).focus(); say('', false); return; }
      if (form.elements._gotcha.value) return;
      var action = form.getAttribute('action') || '';
      if (!action || action.indexOf('TWOJ_ID') > -1) { viaMail(); return; }
      busy(true);
      var data = new FormData(form);
      var scope = data.getAll('zakres');
      if (scope.length > 1) { data.delete('zakres'); data.append('zakres', scope.join(', ')); } // jedna pozycja w mailu zamiast kilku
      data.append('_subject', subject());
      fetch(action, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (r) { if (!r.ok) throw new Error('send'); busy(false); say('', false); success(); })
        .catch(function () { busy(false); say(msg.fail, true); });
    });
  })();
})();
