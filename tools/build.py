#!/usr/bin/env python3
"""Generator statycznych stron DD Volt (PL + EN).

Uruchom z katalogu repozytorium:
    python3 tools/build.py
Treść i ustawienia są w tools/content.py. Ten plik zawiera tylko szablony."""
import html, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import content as C
import geo

ROOT = pathlib.Path(__file__).resolve().parent.parent
LANGS = ('pl', 'en')


# ---------------------------------------------------------------- pomocnicze
def esc(s):
    return html.escape(str(s), quote=False)


def attr(s):
    return html.escape(str(s), quote=True)


def typo(s, lang):
    """Tekst do HTML. Po polsku: twarda spacja po jednoliterowych słowach (a, i, o, u, w, z)."""
    s = esc(s).replace(' – ', '&nbsp;– ').replace(' — ', '&nbsp;— ')  # myślnik nie zaczyna wiersza
    s = s.replace('Mercedes-Benz', '<span class="nb">Mercedes-Benz</span>')  # nazwa nie łamie się na łączniku
    if lang == 'pl':
        s = re.sub(r'(?<![\w&;])([aiouwzAIOUWZ])\s+', r'\1&nbsp;', s)
    return s


WORDS = re.compile(r' (?![^<]*>)')  # spacje między słowami, ale nie wewnątrz znaczników


def split(s, lang):
    """Nagłówek pocięty na słowa (animacja wejścia). Bez JS wygląda jak zwykły tekst."""
    words = WORDS.split(typo(s, lang))
    return ' '.join(f'<span class="w" style="--i:{i}"><span>{w}</span></span>' for i, w in enumerate(words))


def lit(s, lang):
    return ' '.join(f'<span class="lw">{w}</span>' for w in WORDS.split(typo(s, lang)))


def loc(v, lang):
    return v[lang] if isinstance(v, dict) else v


def page_file(lang, key):
    return C.PAGES[key][lang]


def href(lang, key):
    """Link do strony w tym samym języku (pliki jednego języka leżą w jednym katalogu)."""
    return pathlib.PurePosixPath(page_file(lang, key)).name


def alt_href(lang, key):
    """Link do tej samej strony w drugim języku."""
    name = pathlib.PurePosixPath(page_file('en' if lang == 'pl' else 'pl', key)).name
    return ('en/' + name) if lang == 'pl' else ('../' + name)


def asset(lang, path):
    return ('../' if lang == 'en' else '') + path


def abs_url(lang, key):
    f = page_file(lang, key)
    if f.endswith('index.html'):
        f = f[:-len('index.html')]
    return C.SITE_URL + '/' + f


def contact_href(lang, audience=None, role=None):
    q = []
    if audience == 'fachowcy':
        q.append('dla=fachowcy' if lang == 'pl' else 'for=jobs')
    if role:
        q.append(('stanowisko=' if lang == 'pl' else 'role=') + role)
    return href(lang, 'contact') + ('?' + '&'.join(q) if q else '')


def join_names(names, lang):
    if len(names) < 2:
        return ''.join(names)
    return ', '.join(names[:-1]) + ' ' + C.UI[lang]['and'] + ' ' + names[-1]


def country_names(lang):
    return [c[1] if lang == 'pl' else c[2] for c in C.COUNTRIES]


def country_name(cc, lang):
    for c in C.COUNTRIES:
        if c[0] == cc:
            return c[1] if lang == 'pl' else c[2]
    return cc


# ---------------------------------------------------------------- ikony (siatka 24, obrys, zaokrąglone końce)
def ico(name, cls=''):
    paths = {
        'chev': '<path d="M9 5.5l6.5 6.5L9 18.5"/>',
        'phone': ('<path class="hs" d="M6.7 3.5h2.9l1.5 4-2 1.5a12 12 0 0 0 5.9 5.9l1.5-2 4 1.5v2.9a2 2 0 0 1-2.2 2A17.4 17.4 0 0 1 4.7 5.7a2 2 0 0 1 2-2.2z"/>'
                  '<path class="zap" d="M15.2 2.6l1.5 2-1.7.5 1.4 2"/><path class="zap" d="M19.2 6.6l2 1.3-1.5.9 1.8 1.4"/>'),
        'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.5 1.5M17.2 17.2l1.5 1.5M5.3 18.7l1.5-1.5M17.2 6.8l1.5-1.5"/>',
        'moon': '<path d="M20 14.2A8 8 0 0 1 9.8 4 8 8 0 1 0 20 14.2z"/>',
        'plus': '<path d="M12 5.5v13M5.5 12h13"/>',
        'minus': '<path d="M5.5 12h13"/>',
        'mail': '<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="M3.5 7.5l8.5 6 8.5-6"/>',
        'pin': '<path d="M12 21s-6.5-5.5-6.5-10.6a6.5 6.5 0 0 1 13 0C18.5 15.5 12 21 12 21z"/><circle cx="12" cy="10.4" r="2.3"/>',
        'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
        'alert': '<circle cx="12" cy="12" r="9"/><path d="M12 7.5v5.5M12 16.4v.1"/>',
        'theme': '<circle cx="12" cy="12" r="8.5"/><path d="M12 3.5a8.5 8.5 0 0 1 0 17z" fill="currentColor" stroke="none"/>',
        'doc': '<path d="M7.5 3.5H14l4 4v12a1 1 0 0 1-1 1H7.5a1 1 0 0 1-1-1v-15a1 1 0 0 1 1-1z"/><path d="M14 3.5v4h4M9.5 12.5h5M9.5 16h5"/>',
        'team': '<circle cx="9" cy="8.5" r="3"/><path d="M3.5 19.5c.5-3.1 2.7-4.8 5.5-4.8s5 1.7 5.5 4.8"/><circle cx="17" cy="9.5" r="2.4"/><path d="M16.6 14.3c2.100.3 3.5 1.8 3.9 4.7"/>',
        'link': '<path d="M10.5 13.5a4 4 0 0 0 5.7 0l2.8-2.8a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M13.5 10.5a4 4 0 0 0-5.7 0L5 13.3A4 4 0 0 0 10.7 19l1-1"/>',
        'globe': '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.9 3.1 2.9 13.9 0 17M12 3.5c-2.9 3.1-2.9 13.9 0 17"/>',
    }
    c = ('i ' + ('i-call ' if name == 'phone' else '') + cls).strip()
    return f'<svg class="{c}" viewBox="0 0 24 24" aria-hidden="true">{paths[name]}</svg>'


BOLT = 'M36 3 9 52h19l-6 41 33-55H35z'

# ---------------------------------------------------------------- ilustracje usług
ART = {
    'wire': '''<svg class="art art-wire" viewBox="0 0 320 180" aria-hidden="true">
<rect class="art-block" x="250" y="24" width="48" height="132" rx="12"/>
<g class="art-wires">
<path d="M0 30H70C100 30 100 72 130 72H180C208 72 208 42 236 42H256"/>
<path d="M0 70H70C100 70 100 84 130 84H180C208 84 208 74 236 74H256"/>
<path d="M0 110H70C100 110 100 96 130 96H180C208 96 208 106 236 106H256"/>
<path d="M0 150H70C100 150 100 108 130 108H180C208 108 208 138 236 138H256"/>
</g>
<g class="art-pulse">
<path pathLength="100" style="--i:0" d="M0 30H70C100 30 100 72 130 72H180C208 72 208 42 236 42H256"/>
<path pathLength="100" style="--i:1" d="M0 70H70C100 70 100 84 130 84H180C208 84 208 74 236 74H256"/>
<path pathLength="100" style="--i:2" d="M0 110H70C100 110 100 96 130 96H180C208 96 208 106 236 106H256"/>
<path pathLength="100" style="--i:3" d="M0 150H70C100 150 100 108 130 108H180C208 108 208 138 236 138H256"/>
</g>
<g class="art-leds"><circle cx="274" cy="42" r="6" style="--i:0"/><circle cx="274" cy="74" r="6" style="--i:1"/><circle cx="274" cy="106" r="6" style="--i:2"/><circle cx="274" cy="138" r="6" style="--i:3"/></g>
</svg>''',
    'robot': '''<svg class="art art-robot" viewBox="0 0 320 180" aria-hidden="true">
<path class="art-floor" d="M36 158H284"/>
<rect class="art-solid" x="84" y="142" width="72" height="16" rx="6"/>
<rect class="art-solid" x="105" y="114" width="30" height="30" rx="8"/>
<g class="art-arm1">
<path class="art-limb" d="M120 112 168 54" stroke-width="18"/>
<g class="art-arm2">
<path class="art-limb" d="M168 54 232 76" stroke-width="13"/>
<path class="art-limb" d="M232 76 240 98" stroke-width="7"/>
<circle class="art-joint" cx="232" cy="76" r="5"/>
<circle class="art-spark" cx="241" cy="103" r="4.5"/>
</g>
<circle class="art-joint" cx="168" cy="54" r="7"/>
</g>
<circle class="art-joint" cx="120" cy="112" r="8"/>
<rect class="art-part" x="216" y="124" width="52" height="34" rx="7"/>
</svg>''',
    'building': '''<svg class="art art-building" viewBox="0 0 320 180" aria-hidden="true">
<path class="art-floor" d="M36 158H284"/>
<rect class="art-frame" x="72" y="22" width="176" height="136" rx="12"/>
<g class="art-windows">''' + ''.join(
        f'<rect x="{88 + c * 30}" y="{38 + r * 38}" width="22" height="26" rx="5" style="--i:{r * 5 + c}"/>'
        for r in range(3) for c in range(5)) + '''</g>
</svg>''',
}


# ---------------------------------------------------------------- komponenty
def seg(lang, extra=''):
    u = C.UI[lang]
    return f'''<div class="seg{extra}" role="group" aria-label="{attr(u['aud_aria'])}" data-audience-switch>
  <span class="seg-thumb" aria-hidden="true"></span>
  <button type="button" data-value="firmy" aria-pressed="true">{esc(u['aud_firmy'])}</button>
  <button type="button" data-value="fachowcy" aria-pressed="false">{esc(u['aud_fachowcy'])}</button>
</div>'''


def theme_switch(lang):
    u = C.UI[lang]
    return (f'<button class="theme-switch" type="button" role="switch" aria-checked="false" aria-label="{attr(u["theme"])}" data-theme-toggle>'
            f'{ico("sun")}{ico("moon")}<span class="theme-thumb" aria-hidden="true"></span></button>')


def call_btn(lang, cls='btn btn--ghost', extra=''):
    u = C.UI[lang]
    return (f'<a class="{cls}" href="{C.PHONE_HREF}" data-phone="{attr(C.PHONE)}"{extra}>{ico("phone")}'
            f'<span data-phone-label>{esc(u["call"])}</span></a>')


def cta_pair(lang, size='', here=False):
    """Główne CTA zależne od ścieżki: wycena (firmy) albo aplikacja (fachowcy).
    here=True: jesteśmy na stronie kontaktu, więc przycisk przewija do formularza."""
    u = C.UI[lang]
    s = (' ' + size) if size else ''
    a = b = '#' + FORM_ID[lang]
    if not here:
        a, b = contact_href(lang), contact_href(lang, 'fachowcy')
    return (f'<a class="btn btn--primary{s}" data-for="firmy" href="{a}">{esc(u["quote"])}</a>'
            f'<a class="btn btn--primary{s}" data-for="fachowcy" href="{b}">{esc(u["apply"])}</a>')


FORM_ID = {'pl': 'formularz', 'en': 'form'}


def more(label, url):
    return f'<a class="more" href="{url}">{esc(label)}{ico("chev")}</a>'


def stat(value, unit, label, lang):
    u = f'<span class="stat-unit">{esc(unit)}</span>' if unit else ''
    return (f'<div class="stat"><p class="stat-num"><span data-count="{value}">{value}</span>{u}</p>'
            f'<p class="stat-label">{typo(label, lang)}</p></div>')


def main_stats(lang):
    u = C.UI[lang]
    return ''.join([
        stat(C.PROJECTS_COUNT, '+', u['stat_projects'], lang),
        stat(len(C.COUNTRIES), '', u['stat_countries'].format(list=', '.join(country_names(lang))), lang),
        stat(C.MAIN_PROJECT_MONTHS, u['months'], u['stat_main'], lang),
        stat(C.ROBOTS, '', u['stat_robots'].format(w=C.ROBOTS_WEEKS), lang),
    ])


def ticks(items, lang):
    return '<ul class="ticks">' + ''.join(f'<li>{ico("check")}<span>{typo(i, lang)}</span></li>' for i in items) + '</ul>'


def service_cards(lang):
    u = C.UI[lang]
    out = []
    for s in C.SERVICES:
        out.append(f'''<a class="svc card" href="{href(lang, 'services')}#{s['id'][lang]}" data-art>
  <div class="svc-art">{ART[s['art']]}</div>
  <div class="svc-body">
    <h3 class="h-card">{typo(loc(s['title'], lang), lang)}</h3>
    <p>{typo(loc(s['text'], lang), lang)}</p>
    <p class="label">{esc(u['scope'])}</p>
    {ticks(s['items'][lang], lang)}
    <span class="more">{esc(u['details'])}{ico('chev')}</span>
  </div>
</a>''')
    return '<div class="grid grid-3 stagger">' + ''.join(out) + '</div>'


def steps_block(items, lang):
    li = ''.join(f'''<li class="step">
    <span class="step-node" aria-hidden="true">{i + 1}</span>
    <h3 class="h-step">{typo(loc(t, lang), lang)}</h3>
    <p>{typo(loc(x, lang), lang)}</p>
  </li>''' for i, (t, x) in enumerate(items))
    return f'<div class="steps-wrap" data-steps><span class="steps-fill" aria-hidden="true"></span><ol class="steps">{li}</ol></div>'


def feats(items, lang):
    li = ''.join(f'<li class="feat card" data-spot><span class="feat-ico">{ico(i)}</span>'
                 f'<h3 class="h-feat">{typo(loc(t, lang), lang)}</h3><p>{typo(loc(x, lang), lang)}</p></li>'
                 for i, t, x in items)
    return f'<ul class="feats stagger">{li}</ul>'


def job_cards(lang, limit=None, cols=3):
    u = C.UI[lang]
    out = []
    for j in C.JOBS[:limit]:
        out.append(f'''<article class="job card">
  <p class="job-status"><span class="dot" aria-hidden="true"></span>{esc(u['open_recruitment'])}</p>
  <h3 class="h-card">{typo(j['title'][lang], lang)}</h3>
  <ul class="job-meta"><li>{ico('pin')}{esc(C.JOB_PLACE[lang])}</li><li>{esc(j['sector'][lang])}</li><li>{esc(C.JOB_TYPE[lang])}</li></ul>
  <p class="label">{esc(u['requirements'])}</p>
  {ticks(j['req'][lang], lang)}
  <div class="job-actions">
    <a class="btn btn--primary" href="{contact_href(lang, 'fachowcy', j['slug'])}">{esc(u['apply'])}</a>
    {call_btn(lang)}
  </div>
</article>''')
    return f'<div class="grid grid-{cols} stagger">' + ''.join(out) + '</div>'


def faq_block(items, lang, audience=None):
    d = ''.join(f'''<details class="qa">
    <summary><span>{typo(q[lang], lang)}</span><span class="qa-ico" aria-hidden="true"></span></summary>
    <div class="qa-body"><p>{typo(a[lang], lang)}</p></div>
  </details>''' for q, a in items)
    a = f' data-for="{audience}"' if audience else ''
    return f'<div class="faq"{a}>{d}</div>'


def place_label(p, lang):
    cities = [loc(pt['city'], lang) for pt in p['points'] if not pt.get('approx')]
    country = country_name(p['cc'], lang)
    if not cities:
        return country
    return join_names(cities, lang) + ', ' + country


def map_block(lang):
    u = C.UI[lang]
    items, data = [], {'countries': [], 'projects': []}
    for cc, pl, en, lat, lon in C.COUNTRIES:
        x, y = geo.project(lon, lat)
        data['countries'].append({'cc': cc, 'label': pl if lang == 'pl' else en, 'x': round(x, 1), 'y': round(y, 1)})
    for p in C.PROJECTS:
        pts = []
        for pt in p['points']:
            x, y = geo.project(pt['lon'], pt['lat'])
            pts.append({'x': round(x, 1), 'y': round(y, 1),
                        'label': country_name(p['cc'], lang) if pt.get('approx') else loc(pt['city'], lang),
                        'approx': bool(pt.get('approx'))})
        data['projects'].append({'id': p['id'], 'sector': p['sector'], 'points': pts})
        badge = f'<span class="tag tag--volt">{esc(loc(p["badge"], lang))}</span>' if p.get('badge') else ''
        img = (f'<img class="map-item-img" src="{asset(lang, p["img"])}" alt="" loading="lazy" decoding="async">' if p.get('img') else '')
        facts = ''.join(f'<li>{typo(f, lang)}</li>' for f in [u['sectors'][p['sector']]] + p['facts'][lang])
        items.append(f'''<li class="map-item" data-id="{p['id']}" data-sector="{p['sector']}">
        <button class="map-item-btn" type="button" aria-expanded="false">
          <span class="map-item-name">{typo(loc(p['client'], lang), lang)}{badge}</span>
          <span class="map-item-place">{typo(place_label(p, lang), lang)}</span>
        </button>
        <div class="map-item-body"><div>
          {img}
          <p class="map-item-scope">{typo(loc(p['scope'], lang), lang)}</p>
          <p>{typo(loc(p['text'], lang), lang)}</p>
          <ul class="facts">{facts}</ul>
        </div></div>
      </li>''')
    chips = f'<button type="button" class="chip" data-filter="all" aria-pressed="true">{esc(u["all"])}</button>' + ''.join(
        f'<button type="button" class="chip" data-filter="{k}" aria-pressed="false">{esc(v)}</button>' for k, v in u['sectors'].items())
    meta = {'forms': u['loc_forms'], 'lang': lang}
    data['meta'] = meta
    return f'''<div class="mapbox reveal" data-map>
    <div class="map-stage">
      <svg class="map-svg" role="img" aria-label="{attr(u['map_aria'])}" data-map-svg preserveAspectRatio="xMidYMid slice"></svg>
      <button class="map-reset" type="button" hidden>{esc(u['map_reset'])}</button>
      <div class="map-zoom">
        <button type="button" data-zoom="in" aria-label="{attr(u['map_zoom_in'])}">{ico('plus')}</button>
        <button type="button" data-zoom="out" aria-label="{attr(u['map_zoom_out'])}">{ico('minus')}</button>
      </div>
    </div>
    <div class="map-side">
      <div class="map-head">
        <div class="chips" role="group" aria-label="{attr(u['map_filter_aria'])}">{chips}</div>
        <span class="map-count" aria-live="polite"></span>
      </div>
      <ol class="map-list" aria-label="{attr(u['map_list_aria'])}">
      {''.join(items)}
      </ol>
    </div>
    <script type="application/json" data-map-data>{json.dumps(data, ensure_ascii=False, separators=(',', ':'))}</script>
  </div>'''


def project_cards(lang):
    u = C.UI[lang]
    out = []
    for p in C.PROJECTS:
        badge = f'<span class="tag tag--volt">{esc(loc(p["badge"], lang))}</span>' if p.get('badge') else ''
        img = (f'<img class="proj-img" src="{asset(lang, p["img"])}" alt="{attr(loc(p["client"], lang))}, {attr(place_label(p, lang))}" loading="lazy" decoding="async">'
               if p.get('img') else '')
        facts = ''.join(f'<li>{typo(f, lang)}</li>' for f in p['facts'][lang])
        out.append(f'''<article class="proj card{' proj--photo' if img else ''}" id="{p['id']}">
  {img}
  <div class="proj-body">
    <p class="proj-top"><span class="tag">{esc(u['sectors'][p['sector']])}</span>{badge}</p>
    <h3 class="h-card">{typo(loc(p['client'], lang), lang)}</h3>
    <p class="proj-scope">{typo(loc(p['scope'], lang), lang)}</p>
    <p class="proj-place">{ico('pin')}{typo(place_label(p, lang), lang)}</p>
    <p class="proj-text">{typo(loc(p['text'], lang), lang)}</p>
    <ul class="facts">{facts}</ul>
  </div>
</article>''')
    return '<div class="grid grid-3 stagger">' + ''.join(out) + '</div>'


def cta_band(lang):
    u = C.UI[lang]
    return f'''<section class="cta tone-night">
  <div class="cta-glow" aria-hidden="true"></div>
  <div class="container reveal">
    <h2 class="h-display" data-for="firmy">{typo(u['cta_firmy_h'], lang)}</h2>
    <h2 class="h-display" data-for="fachowcy">{typo(u['cta_fach_h'], lang)}</h2>
    <p class="lead" data-for="firmy">{typo(u['cta_firmy_p'], lang)}</p>
    <p class="lead" data-for="fachowcy">{typo(u['cta_fach_p'], lang)}</p>
    <div class="actions">
      {cta_pair(lang, 'btn--lg')}
      {call_btn(lang, 'btn btn--ghost btn--lg')}
    </div>
  </div>
</section>
'''


def intro(h, p=None, link=None, lang='pl', tag='h2'):
    out = f'<header class="intro reveal"><{tag} class="h-display">{typo(h, lang)}</{tag}>'
    if p:
        out += f'<p class="lead">{typo(p, lang)}</p>'
    if link:
        out += more(*link)
    return out + '</header>'


def page_head(h1, lead, lang, extra='', h1_alt=None):
    """Nagłówek podstrony. h1_alt = wariant dla ścieżki „fachowcy”."""
    if h1_alt:
        hs = (f'<h1 class="h-page"><span class="split" data-for="firmy">{split(h1, lang)}</span>'
              f'<span class="split" data-for="fachowcy">{split(h1_alt, lang)}</span></h1>')
    else:
        hs = f'<h1 class="h-page split">{split(h1, lang)}</h1>'
    lead_html = f'<p class="lead rise" style="--d:2">{typo(lead, lang)}</p>' if lead else ''
    return f'''<section class="page-head tone-night">
  <div class="container">
    {hs}
    {lead_html}
    {extra}
  </div>
</section>
'''


# ---------------------------------------------------------------- szkielet strony
BOOT_JS = ("(function(){var d=document.documentElement;d.classList.remove('no-js');d.classList.add('js');try{"
           "var t=localStorage.getItem('dd-theme');if(t==='dark'||t==='light')d.setAttribute('data-theme',t);"
           "var q=new URLSearchParams(location.search),p=q.get('dla')||q.get('for');"
           "p=p==='jobs'?'fachowcy':p==='companies'?'firmy':p;"
           "var a=d.getAttribute('data-audience-lock')||(p==='fachowcy'||p==='firmy'?p:localStorage.getItem('dd-audience'));"
           "if(a==='fachowcy'||a==='firmy')d.setAttribute('data-audience',a);"
           # animacja startowa: pierwsze wejście w sesji na dowolnej stronie; na stronie głównej zawsze
           # (wejście, kliknięcie w logo/Strona główna, odświeżenie), poza cofaniem/przód w historii
           "var again=false;if(d.hasAttribute('data-home')){var n=performance.getEntriesByType&&performance.getEntriesByType('navigation')[0],"
           "ty=n?n.type:'',r=document.referrer,inside=!!location.host&&r.indexOf(location.protocol+'//'+location.host+'/')===0;"
           "again=ty!=='back_forward';}"
           "if((again||!sessionStorage.getItem('dd-boot'))&&!matchMedia('(prefers-reduced-motion: reduce)').matches)d.classList.add('is-booting');"
           "}catch(e){}setTimeout(function(){if(!window.DDV_READY)d.classList.add('no-anim')},4500);})();")


def head(lang, key, title, desc, lock=None, extra_head='', noindex=False):
    other = 'en' if lang == 'pl' else 'pl'
    alternates = ''
    if key in C.PAGES:
        alternates = (f'<link rel="canonical" href="{abs_url(lang, key)}">\n'
                      f'<link rel="alternate" hreflang="{lang}" href="{abs_url(lang, key)}">\n'
                      f'<link rel="alternate" hreflang="{other}" href="{abs_url(other, key)}">\n'
                      f'<link rel="alternate" hreflang="x-default" href="{abs_url("pl", key)}">\n'
                      f'<meta property="og:url" content="{abs_url(lang, key)}">\n')
    lock_attr = f' data-audience-lock="{lock}"' if lock else ''
    if key == 'home':
        lock_attr += ' data-home'
    robots = '<meta name="robots" content="noindex">\n' if noindex else ''
    return f'''<!DOCTYPE html>
<html lang="{lang}" class="no-js" data-theme="light" data-audience="{lock or 'firmy'}"{lock_attr}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{attr(desc)}">
{robots}{alternates}<meta property="og:title" content="{attr(title)}">
<meta property="og:description" content="{attr(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DD Volt">
<meta property="og:locale" content="{'pl_PL' if lang == 'pl' else 'en_GB'}">
<meta property="og:image" content="{C.SITE_URL}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#000000">
<meta name="format-detection" content="telephone=no">
<link rel="icon" href="{asset(lang, 'assets/favicon.svg')}" type="image/svg+xml">
<link rel="icon" href="{asset(lang, 'assets/favicon-48.png')}" type="image/png" sizes="48x48">
<link rel="apple-touch-icon" href="{asset(lang, 'assets/apple-touch-icon.png')}">
<link rel="preload" href="{asset(lang, 'assets/fonts/sofia-sans-latin.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{asset(lang, 'assets/fonts/sofia-sans-latin-ext.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{asset(lang, 'css/style.css')}">
<script>{BOOT_JS}</script>
{extra_head}</head>
<body>
'''


def header(lang, key):
    u = C.UI[lang]

    def link(k, big=False):
        cur = ' aria-current="page"' if k == key else ''
        if big:
            return f'<a href="{href(lang, k)}"{cur} style="--i:{C.NAV.index(k)}"><span>{esc(u["nav"][k])}</span>{ico("chev")}</a>'
        return f'<a href="{href(lang, k)}"{cur}>{esc(u["nav"][k])}</a>'

    nav = ''.join(link(k) for k in C.NAV)
    mob = ''.join(link(k, True) for k in C.NAV)
    other = 'en' if lang == 'pl' else 'pl'
    lang_link = lambda cls, label: (f'<a class="{cls}" href="{alt_href(lang, key) if key in C.PAGES else alt_href(lang, "home")}" '
                                    f'hreflang="{other}" lang="{other}">{label}</a>')
    return f'''<a class="skip" href="#main">{esc(u['skip'])}</a>
<div class="boot" aria-hidden="true">
  <div class="boot-flash"></div>
  <svg class="boot-bolt" viewBox="0 0 64 96"><path class="boot-bolt-fill" d="{BOLT}"/><path class="boot-bolt-line" pathLength="1" d="{BOLT}"/></svg>
  <span class="boot-name">DD Volt</span>
</div>
<header class="site-header" data-header>
  <div class="bar">
    <a class="brand" href="{href(lang, 'home')}" aria-label="{attr(u['home_aria'])}"><span class="brand-mark" aria-hidden="true"></span>DD Volt</a>
    <nav class="nav" aria-label="{attr(u['nav_aria'])}">{nav}</nav>
    <div class="bar-actions">
      <a class="bar-phone" href="{C.PHONE_HREF}" data-phone="{attr(C.PHONE)}">{ico('phone')}<span>{esc(C.PHONE)}</span></a>
      {theme_switch(lang)}
      {lang_link('bar-lang', esc(u['lang_code']) + '<span class="sr-only">: ' + esc(u['lang_aria']) + '</span>')}
      {cta_pair(lang, 'btn--sm', key == 'contact')}
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu" aria-label="{attr(u['menu_open'])}" data-open="{attr(u['menu_open'])}" data-close="{attr(u['menu_close'])}"><span></span><span></span></button>
    </div>
  </div>
  <div class="progress" aria-hidden="true"><svg class="progress-bolt" viewBox="0 0 64 96"><path d="{BOLT}"/></svg></div>
</header>
<div class="menu" id="menu" inert>
  <nav class="menu-nav" aria-label="{attr(u['menu_aria'])}">{mob}</nav>
  <div class="menu-foot">
    <div class="menu-row">
      {seg(lang)}
      <span class="menu-tools">{lang_link('menu-lang', ico('globe') + esc(u['lang_switch']))}{theme_switch(lang)}</span>
    </div>
    <div class="menu-cta">
      {cta_pair(lang, 'btn--lg', key == 'contact')}
      {call_btn(lang, 'btn btn--ghost btn--lg')}
    </div>
  </div>
</div>
'''


def footer(lang, key, scripts=(), dock=True):
    u = C.UI[lang]
    nav = ''.join(f'<li><a href="{href(lang, k)}">{esc(u["nav"][k])}</a></li>' for k in C.NAV)
    other = 'en' if lang == 'pl' else 'pl'
    alt = alt_href(lang, key) if key in C.PAGES else alt_href(lang, 'home')
    js = ''.join(f'<script src="{asset(lang, s)}" defer></script>\n' for s in ('js/main.js',) + tuple(scripts))
    dock_html = f'''<div class="dock" role="region" aria-label="{attr(u['dock_aria'])}" data-dock>
  {call_btn(lang, 'dock-call')}
  {cta_pair(lang)}
</div>
''' if dock else ''
    return f'''<footer class="site-footer tone-night">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="{href(lang, 'home')}" aria-label="{attr(u['home_aria'])}"><span class="brand-mark" aria-hidden="true"></span>DD Volt</a>
        <p>{typo(u['footer_tag'], lang)}</p>
      </div>
      <nav class="footer-col" aria-label="{attr(u['f_site'])}"><h2>{esc(u['f_site'])}</h2><ul>{nav}</ul></nav>
      <div class="footer-col"><h2>{esc(u['f_for'])}</h2><ul>
        <li><a href="{href(lang, 'services')}">{typo(u['f_firmy'], lang)}</a></li>
        <li><a href="{href(lang, 'careers')}">{typo(u['f_fachowcy'], lang)}</a></li>
        <li><a href="{href(lang, 'projects')}">{typo(u['f_map'], lang)}</a></li>
      </ul></div>
      <div class="footer-col"><h2>{esc(u['f_contact'])}</h2><ul>
        <li><a href="{C.PHONE_HREF}" data-phone="{attr(C.PHONE)}"><span>{esc(C.PHONE)}</span></a></li>
        <li><a href="mailto:{C.EMAIL}">{esc(C.EMAIL)}</a></li>
        <li><a href="{href(lang, 'contact')}">{typo(u['f_form'], lang)}</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <span>© {C.YEAR} DD Volt designed by <a class=\"credit\" href=\"https://swagency.com.pl\" target=\"_blank\" rel=\"noopener\">SWAGency</a></span>
      <ul>
        <li><a href="{href(lang, 'privacy')}">{esc(u['privacy'])}</a></li>
        <li><a href="{href(lang, 'cookies')}">{esc(u['cookies'])}</a></li>
        <li><a href="{alt}" hreflang="{other}" lang="{other}">{esc(u['lang_switch'])}</a></li>
      </ul>
    </div>
  </div>
</footer>
{dock_html}<div class="toast" role="status" aria-live="polite" data-toast data-copied="{attr(u['copied'])}"></div>
{js}</body>
</html>
'''


def write(path, text):
    f = ROOT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding='utf-8')
    print('  ', path)


def page(lang, key, body, lock=None, scripts=(), extra_head='', dock=True, main_cls=''):
    t = C.T[lang][key]
    cls = f' class="{main_cls}"' if main_cls else ''
    doc = (head(lang, key, t['title'], t.get('desc', t['title']), lock, extra_head)
           + header(lang, key) + f'<main id="main"{cls}>\n' + body + '</main>\n' + footer(lang, key, scripts, dock))
    write(page_file(lang, key), doc)


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '</script>\n'


# ---------------------------------------------------------------- strony
def build_home(lang):
    t, u = C.T[lang]['home'], C.UI[lang]
    clients = ''.join(f'<span class="marquee-item"><b>{esc(n)}</b> {esc(pl if lang == "pl" else en)}</span>' for n, pl, en in C.CLIENTS)
    body = f'''<section class="hero tone-night" data-hero>
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="container hero-top">
    <div class="rise" style="--d:0">{seg(lang)}</div>
    <h1 class="h-hero"><span class="split" data-for="firmy">{split(t['h1_firmy'], lang)}</span><span class="split" data-for="fachowcy">{split(t['h1_fach'], lang)}</span></h1>
    <p class="lead rise" style="--d:3" data-for="firmy">{typo(t['lead_firmy'], lang)}</p>
    <p class="lead rise" style="--d:3" data-for="fachowcy">{typo(t['lead_fach'], lang)}</p>
    <div class="actions rise" style="--d:4">
      <a class="btn btn--primary btn--lg" data-for="firmy" href="{contact_href(lang)}">{esc(u['quote'])}</a>
      <a class="btn btn--ghost btn--lg" data-for="firmy" href="{href(lang, 'projects')}">{esc(t['see_projects'])}</a>
      <a class="btn btn--primary btn--lg" data-for="fachowcy" href="{href(lang, 'careers')}">{esc(t['see_jobs'])}</a>
      {call_btn(lang, 'btn btn--ghost btn--lg', ' data-for="fachowcy"')}
    </div>
  </div>
  <div class="wave rise" style="--d:5" aria-hidden="true">
    <canvas data-wave></canvas>
    <p class="wave-key"><span>L1</span><span>L2</span><span>L3</span></p>
  </div>
  <div class="container">
    <div class="stats stats--4 rise" style="--d:6" data-stats>{main_stats(lang)}</div>
  </div>
</section>

<div class="marquee tone-night" role="group" aria-label="{attr(u['clients_aria'])}">
  <div class="marquee-track"><div class="marquee-set">{clients}</div><div class="marquee-set" aria-hidden="true">{clients}</div></div>
</div>

<section class="section tone-light" id="{'oferta' if lang == 'pl' else 'services'}" data-order="offer">
  <div class="container">
    {intro(t['offer_h'], t['offer_p'], (t['offer_more'], href(lang, 'services')), lang)}
    {service_cards(lang)}
  </div>
</section>

<section class="section tone-night" id="{'mapa' if lang == 'pl' else 'map'}">
  <div class="container">
    {intro(t['map_h'], t['map_p'].format(countries=join_names(country_names(lang), lang)), (t['map_more'], href(lang, 'projects')), lang)}
    {map_block(lang)}
  </div>
</section>

<section class="section tone-soft" id="{'jak-pracujemy' if lang == 'pl' else 'process'}">
  <div class="container">
    {intro(t['steps_h'], lang=lang)}
    {steps_block(C.STEPS, lang)}
  </div>
</section>

<section class="section tone-night" id="{'dlaczego-my' if lang == 'pl' else 'why-us'}">
  <div class="container">
    <div class="why">
      <h2 class="h-display reveal">{typo(t['why_h'], lang)}</h2>
      <p class="lit" data-lit>{lit(t['why_p'], lang)}</p>
      <a class="btn btn--light btn--lg reveal" href="{href(lang, 'projects')}">{esc(t['why_btn'])}</a>
    </div>
    {feats(C.WHY, lang)}
  </div>
</section>

<section class="section tone-light" id="{'kariera' if lang == 'pl' else 'careers'}" data-order="jobs">
  <div class="container">
    {intro(t['jobs_h'], t['jobs_p'], (t['jobs_more'], href(lang, 'careers')), lang)}
    {job_cards(lang, C.JOBS_ON_HOME)}
  </div>
</section>

<section class="section tone-soft" id="faq">
  <div class="container">
    {intro(t['faq_h'], lang=lang)}
    {faq_block(C.FAQ_FIRMY, lang, 'firmy')}
    {faq_block(C.FAQ_FACHOWCY, lang, 'fachowcy')}
    <p class="center">{more(t['faq_more'], href(lang, 'faq'))}</p>
  </div>
</section>

{cta_band(lang)}'''
    org = {
        '@context': 'https://schema.org', '@type': 'Organization', 'name': 'DD Volt', 'url': C.SITE_URL + '/',
        'logo': C.SITE_URL + '/assets/apple-touch-icon.png', 'image': C.SITE_URL + '/assets/og.png',
        'description': t['desc'], 'telephone': C.PHONE.replace(' ', ''), 'email': C.EMAIL,
        'areaServed': {'@type': 'Place', 'name': 'Europe'},
        'contactPoint': {'@type': 'ContactPoint', 'telephone': C.PHONE.replace(' ', ''), 'email': C.EMAIL,
                         'contactType': 'sales', 'availableLanguage': ['pl', 'en']},
    }
    page(lang, 'home', body, scripts=('js/map-data.js', 'js/map.js'), extra_head=ld(org), main_cls='home')


def build_services(lang):
    t, u = C.T[lang]['services'], C.UI[lang]
    rows = ''.join(f'''<article class="feature reveal" id="{s['id'][lang]}" data-art>
      <div class="feature-art card">{ART[s['art']]}</div>
      <div class="feature-body">
        <h2 class="h-section">{typo(loc(s['title'], lang), lang)}</h2>
        <p class="lead">{typo(loc(s['text'], lang), lang)}</p>
        <p class="label">{esc(u['scope'])}</p>
        {ticks(s['items'][lang], lang)}
      </div>
    </article>''' for s in C.SERVICES)
    sectors = ''.join(f'<li class="card"><h3 class="h-card">{typo(a, lang)}</h3><p>{typo(b, lang)}</p></li>' for a, b in t['sectors'])
    body = page_head(t['h1'], t['lead'], lang) + f'''<section class="section tone-light">
  <div class="container features">
    {rows}
  </div>
</section>
<section class="section tone-soft">
  <div class="container">
    {intro(t['sectors_h'], lang=lang)}
    <ul class="grid grid-3 stagger plain">{sectors}</ul>
  </div>
</section>
<section class="section tone-light">
  <div class="container">
    {intro(t['steps_h'], lang=lang)}
    {steps_block(C.STEPS, lang)}
  </div>
</section>
<section class="section tone-soft">
  <div class="container">
    {intro(t['reach_h'], t['reach_p'], lang=lang)}
    <div class="stats stats--3 reveal" data-stats>
      {stat(len(C.COUNTRIES), '', t['stat_countries'], lang)}
      {stat(C.PROJECTS_COUNT, '+', t['stat_projects'], lang)}
      {stat(1, u['stat_reply_unit'], u['stat_reply'], lang)}
    </div>
  </div>
</section>
{cta_band(lang)}'''
    page(lang, 'services', body, lock='firmy')


def build_projects(lang):
    t = C.T[lang]['projects']
    body = page_head(t['h1'], t['lead'], lang) + f'''<section class="section section--flush tone-night" id="{'mapa' if lang == 'pl' else 'map'}">
  <div class="container">
    <h2 class="sr-only">{esc(t['map_h'])}</h2>
    {map_block(lang)}
  </div>
</section>
<section class="section tone-light">
  <div class="container">
    {intro(t['list_h'], lang=lang)}
    {project_cards(lang)}
  </div>
</section>
{cta_band(lang)}'''
    page(lang, 'projects', body, scripts=('js/map-data.js', 'js/map.js'))


def build_about(lang):
    t = C.T[lang]['about']
    story = ''.join(f'<p>{typo(p, lang)}</p>' for p in t['story'])
    body = page_head(t['h1'], t['lead'], lang) + f'''<section class="section tone-light">
  <div class="container story">
    <div class="story-text reveal">
      <h2 class="h-display">{typo(t['story_h'], lang)}</h2>
      {story}
      <a class="btn btn--light" href="{href(lang, 'projects')}">{esc(t['btn'])}</a>
    </div>
    <div class="story-stats card reveal" style="--d:1" data-stats>{main_stats(lang)}</div>
  </div>
</section>
<section class="section tone-night">
  <div class="container">
    {intro(t['rules_h'], lang=lang)}
    {feats(t['rules'], lang)}
  </div>
</section>
{cta_band(lang)}'''
    page(lang, 'about', body)


def build_careers(lang):
    t, u = C.T[lang]['careers'], C.UI[lang]
    chips = (f'<ul class="tags rise" style="--d:3"><li class="tag tag--live"><span class="dot" aria-hidden="true"></span>{esc(u["open_recruitment"])}</li>'
             + ''.join(f'<li class="tag">{esc(c)}</li>' for c in t['chips']) + '</ul>')
    steps = [({lang: a}, {lang: b}) for a, b in t['process']]
    body = page_head(t['h1'], t['lead'], lang, chips) + f'''<section class="section tone-light" id="{'oferty' if lang == 'pl' else 'positions'}">
  <div class="container">
    {intro(t['jobs_h'], lang=lang)}
    {job_cards(lang, cols=2)}
  </div>
</section>
<section class="section tone-soft">
  <div class="container">
    {intro(t['process_h'], lang=lang)}
    {steps_block(steps, lang)}
  </div>
</section>
<section class="section tone-light">
  <div class="container">
    {intro(t['faq_h'], lang=lang)}
    {faq_block(C.FAQ_FACHOWCY, lang)}
  </div>
</section>
{cta_band(lang)}'''
    page(lang, 'careers', body, lock='fachowcy')


def build_faq(lang):
    t = C.T[lang]['faq']
    schema = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q[lang], 'acceptedAnswer': {'@type': 'Answer', 'text': a[lang]}}
        for q, a in C.FAQ_FIRMY + C.FAQ_FACHOWCY]}
    body = page_head(t['h1'], t['lead'], lang, f'<div class="rise" style="--d:3">{seg(lang)}</div>') + f'''<section class="section tone-light">
  <div class="container">
    {faq_block(C.FAQ_FIRMY, lang, 'firmy')}
    {faq_block(C.FAQ_FACHOWCY, lang, 'fachowcy')}
  </div>
</section>
{cta_band(lang)}'''
    page(lang, 'faq', body, extra_head=ld(schema))


def build_contact(lang):
    t, u = C.T[lang]['contact'], C.UI[lang]
    f = t['form']
    opt = f'<span class="opt">{esc(f["optional"])}</span>'
    scope = ''.join(f'<label class="pick"><input type="checkbox" name="zakres" value="{attr(o)}"><span>{esc(o)}</span></label>' for o in f['scope_opts'])
    roles = ''.join(f'<label class="pick"><input type="radio" name="stanowisko" value="{attr(lab)}" data-role="{slug}"><span>{esc(lab)}</span></label>'
                    for slug, lab in f['role_opts'])
    msgs = {k: f[k] for k in ('err_name', 'err_phone', 'err_email', 'err_consent', 'sending', 'mailto', 'draft', 'draft_clear',
                              'mail_subject_firmy', 'mail_subject_fach', 'topic_firmy', 'topic_fach')}
    msgs['fail'] = f['fail'].format(phone=C.PHONE, email=C.EMAIL)
    msgs['email'] = C.EMAIL
    body = page_head(t['h1_firmy'], t['lead'], lang, h1_alt=t['h1_fach']) + f'''<section class="section tone-light">
  <div class="container contact">
    <aside class="contact-side reveal">
      <h2 class="label">{esc(t['direct'])}</h2>
      <a class="contact-big" href="{C.PHONE_HREF}" data-phone="{attr(C.PHONE)}"><span class="sr-only">{esc(t['phone_label'])}: </span><span>{esc(C.PHONE)}</span></a>
      <a class="contact-mail" href="mailto:{C.EMAIL}"><span class="sr-only">{esc(t['email_label'])}: </span>{esc(C.EMAIL)}</a>
      <p class="contact-note">{typo(t['note'], lang)}</p>
      <a class="more" data-for="fachowcy" href="mailto:{C.EMAIL}?subject={attr(t['cv_subject']).replace(' ', '%20')}">{esc(t['cv_mail'])}{ico('chev')}</a>
    </aside>
    <form class="form card reveal" id="{FORM_ID[lang]}" style="--d:1" action="{attr(C.FORM_ACTION)}" method="POST" novalidate data-form data-lang="{lang}">
      <div class="form-fields">
        <fieldset class="form-topic">
          <legend>{esc(f['legend'])}</legend>
          <div class="seg seg--light seg--wide" role="group" aria-label="{attr(f['legend'])}" data-audience-switch>
            <span class="seg-thumb" aria-hidden="true"></span>
            <button type="button" data-value="firmy" aria-pressed="true">{esc(f['topic_firmy'])}</button>
            <button type="button" data-value="fachowcy" aria-pressed="false">{esc(f['topic_fach'])}</button>
          </div>
        </fieldset>
        <p class="form-draft" hidden data-draft>{esc(f['draft'])} <button type="button" data-draft-clear>{esc(f['draft_clear'])}</button></p>
        <div class="row">
          <div class="field" data-field="name">
            <label for="f-name">{esc(f['name'])}</label>
            <input id="f-name" name="imie" type="text" autocomplete="name" autocapitalize="words" enterkeyhint="next" required aria-describedby="e-name">
            <p class="error" id="e-name" hidden>{ico('alert')}<span>{esc(f['err_name'])}</span></p>
          </div>
          <div class="field" data-field="phone">
            <label for="f-phone">{esc(f['phone'])}</label>
            <input id="f-phone" name="telefon" type="tel" inputmode="tel" autocomplete="tel" enterkeyhint="next" placeholder="+48 600 000 000" required aria-describedby="e-phone">
            <p class="error" id="e-phone" hidden>{ico('alert')}<span>{esc(f['err_phone'])}</span></p>
          </div>
        </div>
        <button class="form-more-btn" type="button" aria-expanded="false" aria-controls="form-more" hidden data-more-btn>{ico('plus')}<span data-for="firmy">{esc(f['more_firmy'])}</span><span data-for="fachowcy">{esc(f['more_fach'])}</span></button>
        <div class="form-more" id="form-more" data-more><div class="form-more-in">
        <div class="row">
          <div class="field" data-field="email">
            <label for="f-email">{esc(f['email'])} {opt}</label>
            <input id="f-email" name="email" type="email" inputmode="email" autocomplete="email" spellcheck="false" enterkeyhint="next" aria-describedby="e-email">
            <p class="error" id="e-email" hidden>{ico('alert')}<span>{esc(f['err_email'])}</span></p>
          </div>
          <div class="field" data-for="firmy" data-group="firmy">
            <label for="f-company">{esc(f['company'])} {opt}</label>
            <input id="f-company" name="firma" type="text" autocomplete="organization" enterkeyhint="next">
          </div>
          <div class="field" data-for="fachowcy" data-group="fachowcy">
            <label for="f-avail">{esc(f['avail'])} {opt}</label>
            <input id="f-avail" name="dostepnosc" type="text" enterkeyhint="next" placeholder="{attr(f['avail_ph'])}">
          </div>
        </div>
        <div class="row" data-for="firmy" data-group="firmy">
          <div class="field">
            <label for="f-loc">{esc(f['location'])} {opt}</label>
            <input id="f-loc" name="lokalizacja" type="text" enterkeyhint="next" placeholder="{attr(f['location_ph'])}">
          </div>
          <div class="field">
            <label for="f-date">{esc(f['date'])} {opt}</label>
            <input id="f-date" name="termin" type="text" enterkeyhint="next" placeholder="{attr(f['date_ph'])}">
          </div>
        </div>
        </div></div>
        <fieldset class="field picks" data-for="firmy" data-group="firmy">
          <legend>{esc(f['scope'])} {opt}</legend>
          <div class="pick-row">{scope}</div>
        </fieldset>
        <fieldset class="field picks" data-for="fachowcy" data-group="fachowcy">
          <legend>{esc(f['role'])} {opt}</legend>
          <div class="pick-row">{roles}</div>
        </fieldset>
        <div class="field">
          <label for="f-msg"><span data-for="firmy">{esc(f['msg_firmy'])}</span><span data-for="fachowcy">{esc(f['msg_fach'])}</span> {opt}</label>
          <textarea id="f-msg" name="wiadomosc" rows="3" placeholder="{attr(f['msg_firmy_hint'])}" data-ph-firmy="{attr(f['msg_firmy_hint'])}" data-ph-fachowcy="{attr(f['msg_fach_hint'])}"></textarea>
        </div>
        <div class="field field--check" data-field="consent">
          <label class="check"><input type="checkbox" name="zgoda" value="tak" required aria-describedby="e-consent"><span class="check-box" aria-hidden="true">{ico('check')}</span>
            <span>{typo(f['consent'], lang)} <a href="{href(lang, 'privacy')}">{esc(f['consent_link'])}</a></span></label>
          <p class="error" id="e-consent" hidden>{ico('alert')}<span>{esc(f['err_consent'])}</span></p>
        </div>
        <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
        <input type="hidden" name="rodzaj" value="">
        <input type="hidden" name="jezyk" value="{lang}">
        <div class="form-submit">
          <button class="btn btn--primary btn--lg" type="submit"><span class="btn-label"><span data-for="firmy">{esc(f['submit_firmy'])}</span><span data-for="fachowcy">{esc(f['submit_fach'])}</span></span><span class="spinner" aria-hidden="true"></span></button>
          <p class="form-status" role="status" aria-live="polite" data-status></p>
        </div>
      </div>
      <div class="form-done" hidden data-done tabindex="-1">
        <svg class="done-mark" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="28"/><path d="M20 33l8.5 8.5L45 24"/></svg>
        <h2 class="h-card">{esc(f['ok_h'])}</h2>
        <p>{esc(f['ok_p'])}</p>
        <button class="btn btn--ghost" type="button" data-again>{esc(f['ok_again'])}</button>
      </div>
      <script type="application/json" data-form-msg>{json.dumps(msgs, ensure_ascii=False, separators=(',', ':'))}</script>
    </form>
  </div>
</section>
'''
    page(lang, 'contact', body, dock=False)


def build_legal(lang, key):
    t = C.T[lang][key]
    body = page_head(t['h1'], None, lang) + f'''<section class="section tone-light">
  <div class="container"><div class="prose">{t['body'].format(email=C.EMAIL)}</div></div>
</section>
'''
    page(lang, key, body)


def build_404():
    """Jedna strona błędu dla całej domeny. Adresy od korzenia (/), bo 404 może wypaść w dowolnym katalogu."""
    pl, en = C.T['pl']['e404'], C.T['en']['e404']
    doc = f'''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(pl['title'])}</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#000000">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<style>
@font-face{{font-family:"Sofia Sans";src:url(/assets/fonts/sofia-sans-latin.woff2) format("woff2");font-weight:1 1000;font-display:swap}}
*{{box-sizing:border-box}}html,body{{height:100%}}
body{{margin:0;display:grid;place-items:center;background:#000;color:#f5f5f7;font:17px/1.5 "Sofia Sans",system-ui,-apple-system,"Segoe UI",sans-serif;text-align:center;padding:24px;-webkit-font-smoothing:antialiased}}
svg{{width:44px;height:66px;fill:#f25500;margin-bottom:28px}}
h1{{font-size:clamp(2rem,6vw,3.5rem);line-height:1.05;letter-spacing:-.02em;margin:0 0 .4em}}
p{{color:#a1a1a6;margin:0 0 .3em}}p[lang=en]{{color:#86868b}}
nav{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:32px}}
a{{display:inline-flex;align-items:center;height:48px;padding:0 24px;border-radius:999px;font-weight:600;text-decoration:none;background:#f25500;color:#000}}
a+a{{background:none;color:#f5f5f7;box-shadow:inset 0 0 0 1px #48484a}}
a:focus-visible{{outline:2px solid #fff;outline-offset:3px}}
</style>
</head>
<body>
<main>
<svg viewBox="0 0 64 96" aria-hidden="true"><path d="{BOLT}"/></svg>
<h1>{esc(pl['h1'])}</h1>
<p>{esc(pl['p'])}</p>
<p lang="en">{esc(en['h1'])}. {esc(en['p'])}</p>
<nav><a href="/">{esc(pl['btn'])}</a><a href="/en/" lang="en">{esc(en['btn'])}</a></nav>
</main>
</body>
</html>
'''
    write('404.html', doc)


def build_seo():
    urls = []
    for key in C.PAGES:
        for lang in LANGS:
            alts = ''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{abs_url(l, key)}"/>' for l in LANGS)
            alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{abs_url("pl", key)}"/>'
            urls.append(f'  <url><loc>{abs_url(lang, key)}</loc>{alts}</url>')
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + '\n'.join(urls) + '\n</urlset>\n')
    write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {C.SITE_URL}/sitemap.xml\n')
    write('.nojekyll', '')


def main():
    print('DD Volt: generuję strony')
    for lang in LANGS:
        build_home(lang)
        build_services(lang)
        build_projects(lang)
        build_about(lang)
        build_careers(lang)
        build_faq(lang)
        build_contact(lang)
        build_legal(lang, 'privacy')
        build_legal(lang, 'cookies')
    build_404()
    build_seo()
    print('Gotowe.')


if __name__ == '__main__':
    main()
