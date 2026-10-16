/* DD Volt — main.js
   Przełącznik ścieżki, menu mobile, reveal, liczniki, FAQ, formularz, motyw, cookies. */
(function () {
  'use strict';
  const html = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---------- ścieżka: firmy / fachowcy ---------- */
  const params = new URLSearchParams(location.search);
  const fromUrl = params.get('dla');
  const audience = (fromUrl === 'fachowcy' || fromUrl === 'firmy') ? fromUrl : (store.get('dd-audience') || 'firmy');
  html.setAttribute('data-audience', audience);

  function setAudience(value, { push = true } = {}) {
    html.setAttribute('data-audience', value);
    store.set('dd-audience', value);
    document.querySelectorAll('.audience').forEach(updateSwitch);
    if (push) {
      const url = new URL(location.href);
      url.searchParams.set('dla', value);
      history.replaceState(null, '', url);
    }
    // hero: ponowne odpalenie animacji słów
    document.querySelectorAll('.words').forEach(el => {
      el.classList.remove('is-visible');
      requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add('is-visible')));
    });
  }

  function updateSwitch(sw) {
    const current = html.getAttribute('data-audience');
    const btns = sw.querySelectorAll('button');
    let active = null;
    btns.forEach(b => {
      const on = b.dataset.value === current;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      if (on) active = b;
    });
    const thumb = sw.querySelector('.thumb');
    if (thumb && active) {
      thumb.style.width = active.offsetWidth + 'px';
      thumb.style.transform = 'translateX(' + (active.offsetLeft - 4) + 'px)';
    }
  }

  document.querySelectorAll('.audience').forEach(sw => {
    sw.querySelectorAll('button').forEach(b => b.addEventListener('click', () => setAudience(b.dataset.value)));
    updateSwitch(sw);
  });
  window.addEventListener('resize', () => document.querySelectorAll('.audience').forEach(updateSwitch));
  // po załadowaniu fontów przelicz szerokość kciuka
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => document.querySelectorAll('.audience').forEach(updateSwitch));

  // linki do podstron niosą ścieżkę dalej
  document.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href');
    if (!href || /^(https?:|mailto:|tel:|#)/.test(href)) return;
    a.addEventListener('click', () => {
      const url = new URL(a.href);
      url.searchParams.set('dla', html.getAttribute('data-audience'));
      a.href = url.toString();
    });
  });

  /* ---------- header: cień po przewinięciu + pasek postępu ---------- */
  const header = document.querySelector('.site-header');
  const progress = document.querySelector('.scroll-progress');
  function onScroll() {
    const y = window.scrollY || 0;
    if (header) header.classList.toggle('is-stuck', y > 8);
    if (progress) {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0) + ')';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- menu mobile ---------- */
  const menuBtn = document.querySelector('.menu-btn');
  const mobile = document.querySelector('.mobile-menu');
  if (menuBtn && mobile) {
    menuBtn.addEventListener('click', () => {
      const open = !mobile.classList.contains('is-open');
      mobile.classList.toggle('is-open', open);
      document.body.classList.toggle('menu-open', open);
      menuBtn.setAttribute('aria-expanded', String(open));
      menuBtn.querySelector('.ico-menu').style.display = open ? 'none' : '';
      menuBtn.querySelector('.ico-close').style.display = open ? '' : 'none';
    });
    mobile.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      mobile.classList.remove('is-open'); document.body.classList.remove('menu-open');
    }));
  }

  /* ---------- reveal przy przewijaniu ---------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      e.target.classList.add('is-visible');
      if (e.target.matches('.stat')) countUp(e.target);
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
  document.querySelectorAll('.reveal, .stagger, .steps, .words, .stat').forEach(el => io.observe(el));

  /* ---------- nagłówki słowo po słowie ---------- */
  document.querySelectorAll('.words').forEach(el => {
    el.querySelectorAll('.w').forEach((w, i) => { w.style.transitionDelay = (i * 60) + 'ms'; });
  });

  /* ---------- liczniki ---------- */
  function countUp(stat) {
    const el = stat.querySelector('[data-count]');
    if (!el) return;
    const target = parseFloat(el.dataset.count);
    if (reduce || isNaN(target)) { el.textContent = target; return; }
    const dur = 1400; const t0 = performance.now();
    function tick(now) {
      const p = Math.min(1, (now - t0) / dur);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased);
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  /* ---------- FAQ: płynne rozwijanie ---------- */
  document.querySelectorAll('.faq details').forEach(d => {
    const summary = d.querySelector('summary');
    const answer = d.querySelector('.answer');
    if (!summary || !answer || reduce) return;
    summary.addEventListener('click', (ev) => {
      ev.preventDefault();
      if (d.open) {
        const h = answer.offsetHeight;
        answer.style.height = h + 'px';
        requestAnimationFrame(() => { answer.style.transition = 'height 300ms cubic-bezier(.2,.8,.2,1)'; answer.style.height = '0px'; });
        answer.addEventListener('transitionend', () => { d.open = false; answer.style.cssText = ''; }, { once: true });
      } else {
        d.open = true;
        const h = answer.offsetHeight;
        answer.style.height = '0px'; answer.style.overflow = 'hidden';
        requestAnimationFrame(() => { answer.style.transition = 'height 300ms cubic-bezier(.2,.8,.2,1)'; answer.style.height = h + 'px'; });
        answer.addEventListener('transitionend', () => { answer.style.cssText = ''; }, { once: true });
      }
    });
  });

  /* ---------- formularz ---------- */
  const form = document.querySelector('form.form');
  if (form) {
    const status = form.querySelector('.form-status');
    form.addEventListener('submit', async (ev) => {
      ev.preventDefault();
      let ok = true;
      form.querySelectorAll('.field[data-required]').forEach(f => {
        const input = f.querySelector('input, textarea, select');
        const bad = !input.value.trim() || (input.type === 'email' && !/^\S+@\S+\.\S+$/.test(input.value));
        f.classList.toggle('is-invalid', bad);
        if (bad) ok = false;
      });
      if (!ok) { form.querySelector('.is-invalid input, .is-invalid textarea')?.focus(); return; }
      const btn = form.querySelector('button[type="submit"]');
      const label = btn.innerHTML;
      btn.disabled = true; btn.textContent = 'Wysyłanie…';
      status.className = 'form-status';
      try {
        const action = form.getAttribute('action');
        if (!action || action.includes('TWOJ_ID')) throw new Error('no-endpoint');
        const res = await fetch(action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
        if (!res.ok) throw new Error('bad');
        status.className = 'form-status ok';
        status.querySelector('span').textContent = 'Wysłano. Oddzwonimy w ciągu jednego dnia roboczego.';
        form.reset();
      } catch (e) {
        status.className = 'form-status err';
        status.querySelector('span').textContent = e.message === 'no-endpoint'
          ? 'Formularz nie jest jeszcze podpięty. Napisz na adres z sekcji obok.'
          : 'Nie udało się wysłać. Zadzwoń do nas.';
      } finally {
        btn.disabled = false; btn.innerHTML = label;
      }
    });
    form.querySelectorAll('.field input, .field textarea').forEach(i => i.addEventListener('input', () => i.closest('.field').classList.remove('is-invalid')));
    // ścieżka → domyślna wartość selecta
    const sel = form.querySelector('select[name="jako"]');
    if (sel) sel.value = html.getAttribute('data-audience') === 'fachowcy' ? 'fachowiec' : 'firma';
  }

  /* ---------- motyw jasny / ciemny ---------- */
  const savedTheme = store.get('dd-theme');
  if (savedTheme) html.setAttribute('data-theme', savedTheme);
  document.querySelectorAll('.theme-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next); store.set('dd-theme', next);
    });
  });

  /* ---------- cookies ---------- */
  const cookie = document.querySelector('.cookie');
  if (cookie && !store.get('dd-cookies')) {
    setTimeout(() => cookie.classList.add('is-open'), 900);
    cookie.querySelectorAll('button[data-consent]').forEach(b => b.addEventListener('click', () => {
      store.set('dd-cookies', b.dataset.consent); cookie.classList.remove('is-open');
    }));
  }

  /* ---------- aktywny link w nawigacji ---------- */
  const here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a, .mobile-menu a').forEach(a => {
    const target = (a.getAttribute('href') || '').split('?')[0];
    if (target === here) a.setAttribute('aria-current', 'page');
  });
})();
