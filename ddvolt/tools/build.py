#!/usr/bin/env python3
"""Generator statycznych stron DD Volt.
Uruchom: python3 tools/build.py  (z katalogu repo). Wynik: pliki *.html w katalogu głównym."""
import os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- ikony
ICO = {
  'aur': '<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
  'ar':  '<svg class="arrow-r" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
  'phone': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="miter"/></svg>',
  'mail': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18v14H3zM3 6l9 7 9-7" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
  'pin': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="10" r="2.5" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
  'check': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12l5 5L20 6" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
  'alert': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 2 21h20L12 3zM12 10v5M12 17.5v.5" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
  'plus': '<svg class="plus" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
  'minus': '<svg class="minus" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
  'menu': '<svg class="ico-menu" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
  'close': '<svg class="ico-close" viewBox="0 0 24 24" aria-hidden="true" style="display:none"><path d="M5 5l14 14M19 5 5 19" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
  'sun': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1" stroke="currentColor" stroke-width="2"/></svg>',
}

NAV = [('Oferta','oferta.html'),('Realizacje','realizacje.html'),('O nas','o-nas.html'),('Kariera','kariera.html'),('FAQ','faq.html'),('Kontakt','kontakt.html')]

# ---------------------------------------------------------------- dane kontaktowe (podmień)
PHONE = '+48 000 000 000'
PHONE_HREF = 'tel:+48000000000'
EMAIL = 'kontakt@ddvolt.pl'
FORM_ACTION = 'https://formspree.io/f/TWOJ_ID'  # załóż darmowe konto na formspree.io i wklej ID

def words(text):
  return ' '.join(f'<span class="w">{w}</span>' for w in text.split(' '))

def head(title, desc, canonical):
  return f'''<!doctype html>
<html lang="pl" data-theme="light" data-audience="firmy">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0b0b0b">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/bricolage-grotesque-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/fonts.css">
<link rel="stylesheet" href="css/style.css">
<script>try{{var t=localStorage.getItem('dd-theme');if(t)document.documentElement.setAttribute('data-theme',t);var a=new URLSearchParams(location.search).get('dla')||localStorage.getItem('dd-audience');if(a==='fachowcy'||a==='firmy')document.documentElement.setAttribute('data-audience',a);}}catch(e){{}}</script>
</head>
<body>
<div class="scroll-progress" aria-hidden="true"></div>
'''

def header():
  nav = ''.join(f'<a href="{h}">{l}</a>' for l, h in NAV)
  mob = ''.join(f'<a href="{h}">{l}{ICO["aur"]}</a>' for l, h in NAV)
  return f'''<header class="site-header">
  <div class="container">
    <a class="brand" href="index.html" aria-label="DD Volt — strona główna"><i></i>DD Volt</a>
    <nav class="nav" aria-label="Główna">{nav}</nav>
    <div class="header-actions">
      <div class="audience" role="group" aria-label="Ścieżka">
        <span class="thumb" aria-hidden="true"></span>
        <button type="button" data-value="firmy" aria-pressed="true">Dla firm</button>
        <button type="button" data-value="fachowcy" aria-pressed="false">Dla fachowców</button>
      </div>
      <a class="btn btn--sm" data-for="firmy" href="kontakt.html">Wyceń projekt {ICO["aur"]}</a>
      <a class="btn btn--sm" data-for="fachowcy" href="kontakt.html">Aplikuj {ICO["aur"]}</a>
      <button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false">{ICO["menu"]}{ICO["close"]}</button>
    </div>
  </div>
</header>
<div class="mobile-menu">
  {mob}
  <div class="audience" role="group" aria-label="Ścieżka" style="justify-self:start;margin-top:16px">
    <span class="thumb" aria-hidden="true"></span>
    <button type="button" data-value="firmy" aria-pressed="true">Dla firm</button>
    <button type="button" data-value="fachowcy" aria-pressed="false">Dla fachowców</button>
  </div>
  <div class="mobile-cta">
    <a class="btn btn--lg" data-for="firmy" href="kontakt.html">Wyceń projekt {ICO["aur"]}</a>
    <a class="btn btn--lg" data-for="fachowcy" href="kontakt.html">Aplikuj {ICO["aur"]}</a>
    <a class="btn btn--lg btn--outline" href="{PHONE_HREF}">{ICO["phone"]} Zadzwoń</a>
  </div>
</div>
'''

def footer(map_script=False):
  nav = ''.join(f'<li><a href="{h}">{l}</a></li>' for l, h in NAV)
  scripts = '<script src="js/main.js"></script>'
  if map_script:
    scripts = ('<link rel="stylesheet" href="vendor/leaflet.css">'
               '<script src="vendor/leaflet.js"></script>'
               '<script src="js/main.js"></script><script src="js/map.js"></script>')
  return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html"><i></i>DD Volt</a>
        <p class="muted" style="margin-top:16px;max-width:34ch">Elektryka i mechanika linii produkcyjnych. Automotive, przemysł, obiekty. Cała Europa.</p>
      </div>
      <div class="col"><h4>Serwis</h4><ul>{nav}</ul></div>
      <div class="col"><h4>Dla kogo</h4><ul>
        <li><a href="oferta.html?dla=firmy">Dla firm — wycena</a></li>
        <li><a href="kariera.html?dla=fachowcy">Dla fachowców — praca</a></li>
        <li><a href="realizacje.html">Mapa realizacji</a></li>
      </ul></div>
      <div class="col"><h4>Kontakt</h4><ul>
        <li><a href="{PHONE_HREF}">{PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="kontakt.html">Formularz</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 DD Volt</span>
      <span style="display:flex;gap:24px;flex-wrap:wrap">
        <a href="polityka-prywatnosci.html">Polityka prywatności</a>
        <a href="polityka-cookies.html">Polityka cookies</a>
        <button class="theme-toggle" type="button">{ICO["sun"]} motyw</button>
      </span>
    </div>
  </div>
</footer>
<div class="cookie" role="dialog" aria-label="Cookies">
  <p>Bez analityki i reklam. Tylko ustawienia strony i kafle mapy z CARTO. Szczegóły w <a href="polityka-cookies.html">polityce cookies</a>.</p>
  <button class="btn btn--sm" type="button" data-consent="all">OK</button>
</div>
{scripts}
</body>
</html>
'''

def page(name, title, desc, body, map_script=False):
  html = head(title, desc, name) + header() + body + footer(map_script)
  (ROOT / name).write_text(html, encoding='utf-8')
  print('→', name)

# ---------------------------------------------------------------- bloki wielokrotne
def cta_band():
  return f'''<section class="section section--night cta-band on-night">
  <div class="glow" aria-hidden="true"></div>
  <div class="container reveal">
    <span class="eyebrow">Kontakt</span>
    <h2 class="display" style="margin-top:16px" data-for="firmy">Masz linię do podłączenia? <span class="hl">Policzmy to.</span></h2>
    <h2 class="display" style="margin-top:16px" data-for="fachowcy">Umiesz czytać schemat? <span class="hl">Jedź z nami.</span></h2>
    <p class="lead" style="margin-top:16px">Odpisujemy w ciągu jednego dnia roboczego. Bez formularzy na pięć stron.</p>
    <div class="actions">
      <a class="btn btn--lg" data-for="firmy" href="kontakt.html">Wyceń projekt {ICO["aur"]}</a>
      <a class="btn btn--lg" data-for="fachowcy" href="kontakt.html">Aplikuj {ICO["aur"]}</a>
      <a class="btn btn--lg btn--outline" href="{PHONE_HREF}">{ICO["phone"]} Zadzwoń</a>
    </div>
  </div>
</section>
'''

SERVICES = [
  ('01','Elektryka od A do Z','Trasy, okablowanie, szafy i podłączenia. Zgodnie ze schematem, e-planem i layoutem od generalnego wykonawcy.',
   ['Czytanie schematów i e-planu','Trasy kablowe i okablowanie','Szafy sterownicze','Podłączenie maszyn i silników']),
  ('02','Mechanika i roboty','Stawiamy roboty i urządzenia linii, potem je podłączamy. Jedna ekipa od montażu do gotowego stanowiska.',
   ['Montaż robotów','Ustawienie urządzeń linii','Podłączenie do instalacji','Uruchomienie z GW']),
  ('03','Obiekty i budynki','Serwerownie, szkoły, oświetlenie i siła. Tam, gdzie liczy się porządek w trasach i czysta dokumentacja.',
   ['Serwerownie','Oświetlenie i siła','Rozdzielnie','Mieszkaniówka na zapytanie']),
]

def service_cards(link=True):
  out = []
  for idx, t, txt, items in SERVICES:
    li = ''.join(f'<li>{i}</li>' for i in items)
    tag = 'a' if link else 'div'
    href = ' href="oferta.html"' if link else ''
    out.append(f'''<{tag} class="card service"{href}>
      <div class="top"><span class="idx">{idx}</span><span class="ring">{ICO["ar"]}</span></div>
      <h3 class="heading">{t}</h3>
      <p>{txt}</p>
      <ul>{li}</ul>
    </{tag}>''')
  return ''.join(out)

PROJECTS = [
  ('Automotive','Ford — linia i lakiernia','Kolonia, Niemcy','Instalacje elektryczne linii produkcyjnej i lakierni. Dwa lata na jednym zakładzie.',[('Kraj','Niemcy'),('Czas','24 mies.'),('Przez','SICA')],'Lider zespołu'),
  ('Automotive','Tesla — zakład produkcyjny','Niemcy','Rok na budowie linii: elektryka i mechanika. Pierwszy duży projekt na własnej działalności.',[('Kraj','Niemcy'),('Czas','12 mies.'),('Zakres','Elektryka + mechanika')],''),
  ('Automotive','Lakiernia','Bergamo, Włochy','Instalacje elektryczne i mechaniczne lakierni, trzy miesiące z ekipą na miejscu.',[('Kraj','Włochy'),('Czas','3 mies.'),('Zakres','Elektryka + mechanika')],''),
  ('Automotive','BMW — linia produkcyjna','Monachium, Niemcy','Elektryka i mechanika linii dla BMW, jako podwykonawca.',[('Kraj','Niemcy'),('Przez','Proster'),('Zakres','Linia')],''),
  ('Automotive','Audi — zakład produkcyjny','Győr, Węgry','Dwa miesiące na linii Audi: okablowanie i podłączenia.',[('Kraj','Węgry'),('Czas','2 mies.'),('Zakres','Elektryka')],''),
  ('Obiekty','Serwerownia — Microsoft','Niemcy','Instalacja elektryczna serwerowni. Prowadzenie ekipy jako lider.',[('Branża','IT / obiekty'),('Czas','2 mies.'),('Rola','Lider')],'Lider zespołu'),
  ('Przemysł','Producent wód mineralnych','Frankfurt, Niemcy','Elektryka linii rozlewniczej w zakładzie spożywczym.',[('Kraj','Niemcy'),('Czas','2 mies.'),('Branża','Spożywcza')],''),
  ('Obiekty','Szkoły — instalacje','Niemcy','Pełne instalacje szkolne: oświetlenie, siła, rozdzielnie. Kilka obiektów.',[('Kraj','Niemcy'),('Obiekty','kilka'),('Zakres','Instalacje')],''),
  ('Przemysł','Piece przemysłowe','Zawiercie, Polska','Elektryka pieców przemysłowych.',[('Kraj','Polska'),('Zakres','Elektryka'),('Branża','Przemysł')],''),
  ('Przemysł','Podłączenie silników','Warszawa · Częstochowa','Podłączenia silników i urządzeń na halach produkcyjnych.',[('Kraj','Polska'),('Obiekty','2'),('Zakres','Silniki')],''),
]

def project_cards(limit=None):
  out = []
  for sector, title, place, txt, facts, badge in PROJECTS[:limit]:
    f = ''.join(f'<div><span class="label">{k}</span><b>{v}</b></div>' for k, v in facts)
    b = f'<span class="badge tag-chip tag-chip--solid">{badge}</span>' if badge else ''
    out.append(f'''<article class="card project">
      <div class="photo">{b}<span class="label">Zdjęcie z realizacji</span></div>
      <div class="body">
        <span class="tag-chip" style="justify-self:start">{sector}</span>
        <h3 class="heading">{title}</h3>
        <span class="place">{ICO["pin"]}{place}</span>
        <p>{txt}</p>
        <div class="facts">{f}</div>
      </div>
    </article>''')
  return ''.join(out)

def map_block(eyebrow='02 / Realizacje', title='Gdzie już <span class="hl">pracowaliśmy</span>.', lead='Każdy projekt na mapie to miejsce, w którym ekipa była na hali. Kliknij pinezkę albo pozycję z listy.'):
  return f'''<section class="section section--night on-night" id="mapa">
  <div class="container">
    <div class="section-header section-header--row reveal">
      <div>
        <span class="eyebrow">{eyebrow}</span>
        <h2 class="display" style="margin-top:16px">{title}</h2>
        <p class="lead" style="margin-top:16px">{lead}</p>
      </div>
      <a class="btn btn--outline" href="realizacje.html">Wszystkie realizacje {ICO["ar"]}</a>
    </div>
    <div class="map-panel reveal" data-delay="1">
      <div class="map-canvas"><div id="map" role="application" aria-label="Mapa realizacji"></div></div>
      <aside class="map-side">
        <div class="head"><span class="eyebrow">Lokalizacje</span><span class="tag map-count">—</span></div>
        <div class="map-filters" role="group" aria-label="Filtr">
          <button type="button" data-filter="all" aria-pressed="true">Wszystkie</button>
          <button type="button" data-filter="Automotive" aria-pressed="false">Automotive</button>
          <button type="button" data-filter="Przemysł" aria-pressed="false">Przemysł</button>
          <button type="button" data-filter="Obiekty" aria-pressed="false">Obiekty</button>
          <button type="button" data-filter="DE" aria-pressed="false">DE</button>
          <button type="button" data-filter="PL" aria-pressed="false">PL</button>
          <button type="button" data-filter="IT" aria-pressed="false">IT</button>
          <button type="button" data-filter="HU" aria-pressed="false">HU</button>
        </div>
        <div class="map-active" aria-live="polite"></div>
        <div class="map-list" role="list"></div>
      </aside>
    </div>
  </div>
</section>
'''

FAQ_FIRMY = [
  ('Na jakim obszarze pracujecie?','W całej Europie. Mamy za sobą projekty w Niemczech, we Włoszech, na Węgrzech i w Polsce. Rozmawiamy też o projektach poza Europą.'),
  ('Z jakiej dokumentacji pracujecie?','Ze schematów elektrycznych, e-planu i layoutu od generalnego wykonawcy. Czytamy je sami, nie potrzebujemy tłumaczenia na miejscu.'),
  ('Robicie tylko elektrykę?','Nie. Elektrykę i mechanikę: stawiamy roboty i urządzenia linii, a potem je podłączamy. Jedna ekipa, jeden lider.'),
  ('Jak szybko możecie wejść na projekt?','Zależy od terminu i wielkości ekipy. Zwykle podajemy datę w ciągu kilku dni od zapytania.'),
  ('Ilu ludzi możecie wystawić?','Prowadziliśmy ekipy do 20 osób. Przy większych zakresach łączymy kilka brygad z osobnymi liderami.'),
  ('Czy możecie pokazać referencje?','Tak, po rozmowie. Nazwy klientów końcowych podajemy tekstem; zdjęcia z zakładów udostępniamy po zgodzie GW.'),
]
FAQ_FACHOWCY = [
  ('Jaka forma współpracy?','Umowa albo B2B, do wyboru. Przy B2B pomagamy ogarnąć start.'),
  ('Jak wyglądają wyjazdy?','Projekty trwają od kilku tygodni do kilkunastu miesięcy. Zakwaterowanie i dojazd ustalamy przed wyjazdem, nie po.'),
  ('Czego wymagacie?','Czytania schematów elektrycznych albo doświadczenia w montażu mechanicznym. Reszty nauczysz się na hali, z liderem obok.'),
  ('Czy potrzebuję znać język?','Podstawy angielskiego albo niemieckiego pomagają, ale lider na miejscu ogarnia komunikację z GW.'),
  ('Jak aplikować?','Wyślij formularz z kontaktu albo zadzwoń. Odpisujemy w ciągu jednego dnia roboczego.'),
]

def faq_block(items, audience=None):
  d = ''.join(f'''<details>
      <summary>{q}<span class="ico">{ICO["plus"]}{ICO["minus"]}</span></summary>
      <div class="answer"><div>{a}</div></div>
    </details>''' for q, a in items)
  attr = f' data-for="{audience}"' if audience else ''
  return f'<div class="faq"{attr}>{d}</div>'

STEPS = [
  ('01','Dokumentacja','Dostajemy schematy, e-plan i layout od generalnego wykonawcy. Planujemy robotę i ludzi.'),
  ('02','Ekipa na miejscu','Przyjeżdżamy z liderem, który ustawia robotę tak, żeby szła do przodu od pierwszego dnia.'),
  ('03','Montaż i podłączenie','Trasy, okablowanie, roboty i urządzenia. Od A do Z, zgodnie ze schematem.'),
  ('04','Przekazanie','Oddajemy zakres gotowy do dalszych prac generalnego wykonawcy. Bez spalonych mostów.'),
]
def steps_block():
  return '<div class="steps">' + ''.join(f'<div class="step"><span class="idx">{i}</span><h3 class="heading">{t}</h3><p>{x}</p></div>' for i,t,x in STEPS) + '</div>'

SCHEMATIC = '''<svg class="schematic" viewBox="0 0 400 500" aria-hidden="true">
  <g>
    <polyline class="draw" points="40,60 40,140 120,140 120,200"/>
    <polyline class="draw" points="120,200 120,260 200,260 200,330 280,330"/>
    <polyline class="draw" points="280,330 280,420 360,420"/>
    <polyline class="draw" points="200,60 200,120 320,120 320,200"/>
    <rect class="draw" x="280" y="200" width="80" height="50"/>
    <rect class="draw" x="60" y="300" width="100" height="60"/>
    <polyline class="draw" points="160,330 200,330"/>
  </g>
  <polyline class="flow" points="40,60 40,140 120,140 120,200 120,260 200,260 200,330 280,330 280,420 360,420"/>
  <rect class="node" x="36" y="56" width="8" height="8"/>
  <rect class="node" x="196" y="56" width="8" height="8"/>
  <rect class="node" x="356" y="416" width="8" height="8"/>
  <rect class="pulse" x="114" y="194" width="12" height="12"/>
  <rect class="pulse" x="314" y="194" width="12" height="12"/>
  <rect class="pulse" x="274" y="324" width="12" height="12"/>
  <text x="60" y="52">L1 · 400V</text>
  <text x="220" y="52">PLC</text>
  <text x="290" y="226" style="text-anchor:start">ROBOT 03</text>
  <text x="70" y="335">SZAFA 1</text>
  <text x="300" y="455">M1 · 15 kW</text>
</svg>'''

# ---------------------------------------------------------------- strona główna
HOME = f'''<section class="hero on-night">
  <div class="container">
    <div class="hero-grid">
      <div>
        <span class="eyebrow" data-for="firmy">Elektryka · Mechanika · Automotive</span>
        <span class="eyebrow" data-for="fachowcy">Kariera · Wyjazdy · Europa</span>
        <h1 class="display-xl words" data-for="firmy">{words('Linie produkcyjne podłączone')} <span class="hl">{words('od A do Z.')}</span></h1>
        <h1 class="display-xl words" data-for="fachowcy">{words('Jeździsz na montaże? Jedź z ekipą,')} <span class="hl">{words('która dowozi.')}</span></h1>
        <p class="lead" data-for="firmy">Elektryka i mechanika dla automotive i przemysłu: od czytania schematów po podłączenie robota. Pracujemy w całej Europie.</p>
        <p class="lead" data-for="fachowcy">Projekty u Forda, Tesli, BMW i Audi. Lider na miejscu, jasne warunki, robota, która idzie do przodu.</p>
        <div class="actions">
          <a class="btn btn--lg" data-for="firmy" href="kontakt.html">Wyceń projekt {ICO["aur"]}</a>
          <a class="btn btn--lg btn--outline" data-for="firmy" href="realizacje.html">Zobacz realizacje</a>
          <a class="btn btn--lg" data-for="fachowcy" href="kariera.html">Zobacz oferty pracy {ICO["aur"]}</a>
          <a class="btn btn--lg btn--outline" data-for="fachowcy" href="{PHONE_HREF}">{ICO["phone"]} Zadzwoń</a>
        </div>
      </div>
      <div class="hero-art reveal" data-delay="2">
        {SCHEMATIC}
        <span class="label label-r">E-plan · fragment</span>
        <span class="label">Tu wejdzie zdjęcie z hali</span>
      </div>
    </div>
    <div class="stats stats--4">
      <div class="stat"><div class="num"><span data-count="12">0</span><span class="unit">+</span></div><span class="label">Realizacji w automotive i przemyśle</span></div>
      <div class="stat"><div class="num"><span data-count="4">0</span></div><span class="label">Kraje: DE · IT · HU · PL</span></div>
      <div class="stat"><div class="num"><span data-count="24">0</span><span class="unit">mies.</span></div><span class="label">Najdłuższy projekt — Ford, Kolonia</span></div>
      <div class="stat"><div class="num"><span data-count="20">0</span><span class="unit">osób</span></div><span class="label">Największa ekipa pod jednym liderem</span></div>
    </div>
  </div>
</section>

<div class="ticker" aria-label="Klienci końcowi">
  <div class="track">
    {''.join('<span class="item"><b>%s</b> %s</span>' % x for x in [('Ford','Kolonia'),('Tesla','Niemcy'),('BMW','Monachium'),('Audi','Győr'),('Microsoft','serwerownia'),('Lakiernia','Bergamo'),('Wody mineralne','Frankfurt'),('Piece','Zawiercie')]*2)}
  </div>
</div>

<section class="section" id="oferta">
  <div class="container">
    <div class="section-header section-header--row reveal">
      <div>
        <span class="eyebrow">01 / Oferta</span>
        <h2 class="display" style="margin-top:16px">Elektryka i mechanika linii <span class="hl">od A do Z</span>.</h2>
        <p class="lead" style="margin-top:16px">Pracujemy według schematów, e-planu i layoutu od generalnego wykonawcy. Od tras kablowych po podłączenie robota.</p>
      </div>
      <a class="btn btn--outline" href="oferta.html">Cała oferta {ICO["ar"]}</a>
    </div>
    <div class="grid grid-3 stagger">{service_cards()}</div>
  </div>
</section>

{map_block()}

<section class="section section--alt" id="jak-pracujemy">
  <div class="container">
    <div class="section-header reveal">
      <span class="eyebrow">03 / Jak pracujemy</span>
      <h2 class="display">Cztery kroki, <span class="hl">jeden lider</span>.</h2>
    </div>
    {steps_block()}
  </div>
</section>

<section class="section section--night on-night" id="dlaczego-my">
  <div class="container">
    <div class="why">
      <div class="reveal">
        <span class="eyebrow">04 / Dlaczego my</span>
        <h2 class="display" style="margin-top:16px">Bez spalonych mostów. Z robotą, która <span class="hl">idzie do przodu</span>.</h2>
        <p class="lead" style="margin-top:24px">Każdy generalny wykonawca pyta o to samo: gdzie robiliście i czy wrócicie na kolejny projekt. Odpowiedź na pierwsze jest na mapie. Na drugie: tak, wracamy.</p>
        <a class="btn btn--outline" style="margin-top:32px" href="o-nas.html">Poznaj ekipę {ICO["ar"]}</a>
      </div>
      <ul class="why-list stagger">
        <li><span class="idx">01</span><div><h3>Czytamy schematy sami</h3><p>E-plan, layout, dokumentacja GW. Nie czekamy, aż ktoś pokaże palcem.</p></div></li>
        <li><span class="idx">02</span><div><h3>Lider zawsze na hali</h3><p>Ustawia ludzi, pilnuje tempa i rozmawia z generalnym wykonawcą. Robota nie stoi.</p></div></li>
        <li><span class="idx">03</span><div><h3>Elektryka i mechanika razem</h3><p>Stawiamy robota i go podłączamy. Jedna ekipa zamiast dwóch firm, które się nie dogadują.</p></div></li>
        <li><span class="idx">04</span><div><h3>Te same twarze na kolejnym projekcie</h3><p>Ekipa, która wraca z Forda na Teslę, a z Tesli do Bergamo. Zgrana, nie przypadkowa.</p></div></li>
      </ul>
    </div>
  </div>
</section>

<section class="section" id="kariera">
  <div class="container">
    <div class="section-header section-header--row reveal">
      <div>
        <span class="eyebrow">05 / Kariera</span>
        <h2 class="display" style="margin-top:16px">Szukamy ludzi, którzy <span class="hl">umieją czytać schemat</span>.</h2>
        <p class="lead" style="margin-top:16px">Umowa albo B2B. Projekty w całej Europie, lider na miejscu, warunki ustalone przed wyjazdem.</p>
      </div>
      <a class="btn btn--outline" href="kariera.html">Wszystkie oferty {ICO["ar"]}</a>
    </div>
    <div class="grid grid-2 stagger">{job_cards() if False else ''}</div>
  </div>
</section>

<section class="section section--alt" id="faq">
  <div class="container">
    <div class="section-header reveal">
      <span class="eyebrow">06 / FAQ</span>
      <h2 class="display">Pytania, które <span class="hl">zawsze padają</span>.</h2>
    </div>
    <div class="reveal">
      {faq_block(FAQ_FIRMY[:4],'firmy')}
      {faq_block(FAQ_FACHOWCY[:4],'fachowcy')}
    </div>
    <a class="link" style="margin-top:32px" href="faq.html">Wszystkie pytania {ICO["ar"]}</a>
  </div>
</section>

{cta_band()}
'''

JOBS = [
  ('Elektryk przemysłowy','Umowa / B2B','Europa — wyjazdy','Automotive',['Czytasz schematy elektryczne i e-plan','Masz doświadczenie w trasach i okablowaniu','Jesteś gotów na wyjazdy na projekty w Europie']),
  ('Monter mechanik — roboty i linie','Umowa / B2B','Europa — wyjazdy','Przemysł',['Stawiasz roboty i urządzenia według layoutu','Pracujesz w zespole z liderem na miejscu','Jesteś gotów na wyjazdy na projekty w Europie']),
  ('Lider zespołu — elektryka','Umowa / B2B','Europa — wyjazdy','Automotive',['Prowadziłeś ekipę minimum 5 osób na hali','Rozmawiasz z GW po angielsku albo niemiecku','Ustawiasz robotę tak, żeby szła do przodu']),
]
def job_cards(limit=None):
  out = []
  for t, typ, loc, sec, items in JOBS[:limit]:
    li = ''.join(f'<li>{ICO["check"]}<span>{i}</span></li>' for i in items)
    out.append(f'''<article class="card job">
      <div class="top"><span class="tag-chip tag-chip--soft">Rekrutacja otwarta</span><span class="label muted">{typ}</span></div>
      <h3 class="heading">{t}</h3>
      <span class="meta">{ICO["pin"]}{loc} · {sec}</span>
      <ul>{li}</ul>
      <div class="actions"><a class="btn" href="kontakt.html?dla=fachowcy">Aplikuj {ICO["aur"]}</a><a class="btn btn--outline" href="{PHONE_HREF}">{ICO["phone"]} Zadzwoń</a></div>
    </article>''')
  return ''.join(out)
HOME = HOME.replace('<div class="grid grid-2 stagger"></div>', f'<div class="grid grid-2 stagger">{job_cards(2)}</div>')

page('index.html','DD Volt — elektryka i mechanika linii produkcyjnych','Budujemy i podłączamy linie produkcyjne dla automotive i przemysłu w całej Europie. Elektryka od A do Z i mechanika: roboty, urządzenia, szafy.', HOME, map_script=True)

# ---------------------------------------------------------------- oferta
OFERTA = f'''<section class="page-head on-night">
  <div class="container">
    <span class="eyebrow">Oferta</span>
    <h1 class="display-xl words">{words('Od schematu do')} <span class="hl">{words('podłączonego robota.')}</span></h1>
    <p class="lead">Trzy zakresy, jedna ekipa. Wchodzimy na halę z dokumentacją od GW i oddajemy zakres gotowy do dalszych prac.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid-3 stagger">{service_cards(link=False)}</div>
  </div>
</section>
<section class="section section--alt">
  <div class="container">
    <div class="section-header reveal"><span class="eyebrow">Branże</span><h2 class="display">Gdzie to <span class="hl">działa</span>.</h2></div>
    <div class="grid grid-3 stagger">
      <div class="card"><span class="label muted">01</span><h3 class="heading" style="margin-top:12px">Automotive</h3><p class="muted" style="margin-top:8px">Linie montażowe, lakiernie, stanowiska robotów. Ford, Tesla, BMW, Audi.</p></div>
      <div class="card"><span class="label muted">02</span><h3 class="heading" style="margin-top:12px">Przemysł i spożywka</h3><p class="muted" style="margin-top:8px">Rozlewnie, piece przemysłowe, podłączenia silników i urządzeń na halach.</p></div>
      <div class="card"><span class="label muted">03</span><h3 class="heading" style="margin-top:12px">Obiekty</h3><p class="muted" style="margin-top:8px">Serwerownie, szkoły, oświetlenie i siła. Mieszkaniówka, gdy ma to sens.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-header reveal"><span class="eyebrow">Jak pracujemy</span><h2 class="display">Cztery kroki, <span class="hl">jeden lider</span>.</h2></div>
    {steps_block()}
  </div>
</section>
<section class="section section--alt">
  <div class="container">
    <div class="section-header reveal"><span class="eyebrow">Zasięg</span><h2 class="display">Cała Europa. <span class="hl">Rozmawiamy też o USA.</span></h2>
    <p class="lead">Ekipa jeździ tam, gdzie jest projekt: Niemcy, Włochy, Węgry, Polska. Dalsze kierunki ustalamy indywidualnie.</p></div>
    <div class="stats reveal">
      <div class="stat"><div class="num"><span data-count="4">0</span></div><span class="label">Kraje z realizacjami</span></div>
      <div class="stat"><div class="num"><span data-count="12">0</span><span class="unit">+</span></div><span class="label">Projekty na hali</span></div>
      <div class="stat"><div class="num"><span data-count="1">0</span><span class="unit">dzień</span></div><span class="label">Czas odpowiedzi na zapytanie</span></div>
    </div>
  </div>
</section>
{cta_band()}
'''
page('oferta.html','Oferta — DD Volt','Elektryka od A do Z, mechanika i roboty, obiekty. Zakres usług DD Volt dla automotive, przemysłu i budynków.', OFERTA)

# ---------------------------------------------------------------- realizacje
REALIZACJE = f'''<section class="page-head on-night">
  <div class="container">
    <span class="eyebrow">Realizacje</span>
    <h1 class="display-xl words">{words('Gdzie już')} <span class="hl">{words('pracowaliśmy.')}</span></h1>
    <p class="lead">Nazwy klientów końcowych podajemy uczciwie, z rolą. Zdjęcia z zakładów pokazujemy po zgodzie generalnego wykonawcy.</p>
    <div class="tags"><span class="tag-chip">Niemcy</span><span class="tag-chip">Włochy</span><span class="tag-chip">Węgry</span><span class="tag-chip">Polska</span></div>
  </div>
</section>
{map_block('Mapa','Każdy pin to <span class="hl">hala</span>, nie biuro.','Filtruj po branży albo kraju. Lista obok działa z klawiatury.')}
<section class="section">
  <div class="container">
    <div class="section-header reveal"><span class="eyebrow">Case study</span><h2 class="display">Projekty <span class="hl">po kolei</span>.</h2></div>
    <div class="grid grid-3 stagger">{project_cards()}</div>
  </div>
</section>
{cta_band()}
'''
page('realizacje.html','Realizacje — DD Volt','Mapa i lista realizacji DD Volt: Ford w Kolonii, Tesla, BMW w Monachium, Audi w Győr, lakiernia w Bergamo, serwerownia Microsoft i projekty w Polsce.', REALIZACJE, map_script=True)

# ---------------------------------------------------------------- o nas
ONAS = f'''<section class="page-head on-night">
  <div class="container">
    <span class="eyebrow">O nas</span>
    <h1 class="display-xl words">{words('Ekipa, która wraca')} <span class="hl">{words('na kolejny projekt.')}</span></h1>
    <p class="lead">DD Volt to elektrycy i mechanicy z doświadczeniem na liniach Forda, Tesli, BMW i Audi. Firma wyrosła z jednej zasady: robota ma iść do przodu, a mosty zostają całe.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="why" style="align-items:center">
      <div class="reveal">
        <span class="eyebrow">Historia</span>
        <h2 class="display" style="margin-top:16px">Od Kolonii <span class="hl">do własnej firmy</span>.</h2>
        <p class="lead" style="margin-top:24px">Zaczęło się od dwóch lat na linii i lakierni Forda w Kolonii, jako podwykonawca SICA. Potem Audi na Węgrzech, serwerownia Microsoftu, szkoły w Niemczech. Rok na Tesli to już własna działalność. Dalej Bergamo, Frankfurt, Monachium i projekty w Polsce.</p>
        <p class="lead" style="margin-top:16px">Dziś prowadzimy ekipy do 20 osób i bierzemy zakresy elektryczne i mechaniczne razem.</p>
      </div>
      <div class="card" style="padding:0;overflow:hidden;background:var(--night);aspect-ratio:4/5;position:relative;background-image:repeating-linear-gradient(135deg,transparent 0 14px,#1c1c1c 14px 15px)">
        <span class="label" style="position:absolute;left:16px;bottom:16px;color:var(--on-night-muted)">Zdjęcie ekipy przy pracy</span>
      </div>
    </div>
  </div>
</section>
<section class="section section--night on-night">
  <div class="container">
    <div class="section-header reveal"><span class="eyebrow">Zasady</span><h2 class="display">Jak robimy <span class="hl">robotę</span>.</h2></div>
    <ul class="why-list stagger" style="max-width:860px">
      <li><span class="idx">01</span><div><h3>Konkret zamiast obietnic</h3><p>Mówimy, co zrobimy, w jakim czasie i iloma ludźmi. Potem to robimy.</p></div></li>
      <li><span class="idx">02</span><div><h3>Dokumentacja na stole, nie w głowie</h3><p>Pracujemy według e-planu i layoutu. Zmiany wracają do GW na piśmie.</p></div></li>
      <li><span class="idx">03</span><div><h3>Lider odpowiada za tempo</h3><p>Ustawia robotę, rozwiązuje problemy na miejscu i trzyma kontakt z generalnym wykonawcą.</p></div></li>
      <li><span class="idx">04</span><div><h3>Ludzie wracają, bo warunki są jasne</h3><p>Forma współpracy, zakwaterowanie i stawki ustalone przed wyjazdem.</p></div></li>
    </ul>
  </div>
</section>
<section class="section section--alt">
  <div class="container">
    <div class="stats stats--4 reveal">
      <div class="stat"><div class="num"><span data-count="12">0</span><span class="unit">+</span></div><span class="label">Realizacji</span></div>
      <div class="stat"><div class="num"><span data-count="4">0</span></div><span class="label">Kraje</span></div>
      <div class="stat"><div class="num"><span data-count="24">0</span><span class="unit">mies.</span></div><span class="label">Najdłuższy projekt</span></div>
      <div class="stat"><div class="num"><span data-count="20">0</span><span class="unit">osób</span></div><span class="label">Największa ekipa</span></div>
    </div>
  </div>
</section>
{cta_band()}
'''
page('o-nas.html','O nas — DD Volt','Kim jest ekipa DD Volt: elektrycy i mechanicy z doświadczeniem na liniach Forda, Tesli, BMW i Audi.', ONAS)

# ---------------------------------------------------------------- kariera
KARIERA = f'''<section class="page-head on-night">
  <div class="container">
    <span class="eyebrow">Kariera</span>
    <h1 class="display-xl words">{words('Jeździsz na montaże?')} <span class="hl">{words('Jedź z ekipą, która dowozi.')}</span></h1>
    <p class="lead">Umowa albo B2B. Projekty w Niemczech, we Włoszech, na Węgrzech i w Polsce. Lider na miejscu i warunki ustalone przed wyjazdem.</p>
    <div class="tags"><span class="tag-chip tag-chip--soft">Rekrutacja otwarta</span><span class="tag-chip">Umowa / B2B</span><span class="tag-chip">Europa</span></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-header reveal"><span class="eyebrow">Oferty</span><h2 class="display">Kogo <span class="hl">szukamy</span>.</h2></div>
    <div class="grid grid-3 stagger">{job_cards()}</div>
  </div>
</section>
<section class="section section--alt">
  <div class="container">
    <div class="section-header reveal"><span class="eyebrow">Jak to wygląda</span><h2 class="display">Od telefonu <span class="hl">do hali</span>.</h2></div>
    <div class="steps">
      <div class="step"><span class="idx">01</span><h3 class="heading">Rozmowa</h3><p>Dzwonisz albo piszesz. Pytamy o doświadczenie, nie o CV na trzy strony.</p></div>
      <div class="step"><span class="idx">02</span><h3 class="heading">Warunki</h3><p>Forma, stawka, zakwaterowanie, termin. Wszystko przed wyjazdem.</p></div>
      <div class="step"><span class="idx">03</span><h3 class="heading">Wyjazd</h3><p>Jedziesz z ekipą i liderem, który zna projekt i GW.</p></div>
      <div class="step"><span class="idx">04</span><h3 class="heading">Kolejny projekt</h3><p>Dobrzy ludzie dostają propozycję następnego wyjazdu jako pierwsi.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-header reveal"><span class="eyebrow">FAQ</span><h2 class="display">Pytania <span class="hl">fachowców</span>.</h2></div>
    <div class="reveal">{faq_block(FAQ_FACHOWCY)}</div>
  </div>
</section>
{cta_band()}
'''
page('kariera.html','Kariera — DD Volt','Praca dla elektryków przemysłowych i monterów mechaników: projekty w Europie, umowa albo B2B, lider na miejscu.', KARIERA)

# ---------------------------------------------------------------- faq
FAQ = f'''<section class="page-head on-night">
  <div class="container">
    <span class="eyebrow">FAQ</span>
    <h1 class="display-xl words">{words('Pytania, które')} <span class="hl">{words('zawsze padają.')}</span></h1>
    <p class="lead">Osobno dla firm i dla fachowców. Przełącz ścieżkę w nagłówku, żeby zobaczyć drugi zestaw.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section-header reveal"><span class="eyebrow" data-for="firmy">Dla firm</span><span class="eyebrow" data-for="fachowcy">Dla fachowców</span></div>
    <div class="reveal">{faq_block(FAQ_FIRMY,'firmy')}{faq_block(FAQ_FACHOWCY,'fachowcy')}</div>
  </div>
</section>
{cta_band()}
'''
page('faq.html','FAQ — DD Volt','Najczęstsze pytania firm i fachowców o współpracę z DD Volt.', FAQ)

# ---------------------------------------------------------------- kontakt
KONTAKT = f'''<section class="page-head on-night">
  <div class="container">
    <span class="eyebrow">Kontakt</span>
    <h1 class="display-xl words" data-for="firmy">{words('Policzmy')} <span class="hl">{words('Twój projekt.')}</span></h1>
    <h1 class="display-xl words" data-for="fachowcy">{words('Napisz, gdzie')} <span class="hl">{words('robiłeś.')}</span></h1>
    <p class="lead">Odpisujemy w ciągu jednego dnia roboczego. Telefon działa szybciej.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="contact-grid">
      <div class="reveal">
        <span class="eyebrow">Bezpośrednio</span>
        <div class="contact-list">
          <a href="{PHONE_HREF}">{ICO["phone"]}{PHONE}</a>
          <a href="mailto:{EMAIL}">{ICO["mail"]}{EMAIL}</a>
        </div>
        <p class="muted" style="margin-top:32px;max-width:36ch" data-for="firmy">Do wyceny potrzebujemy: branżę, lokalizację, termin i zakres (elektryka, mechanika czy oba). Schematy mile widziane, ale nie na start.</p>
        <p class="muted" style="margin-top:32px;max-width:36ch" data-for="fachowcy">Napisz, na jakich projektach byłeś, co robiłeś i od kiedy możesz jechać. Resztę ustalimy przez telefon.</p>
      </div>
      <form class="form reveal" data-delay="1" action="{FORM_ACTION}" method="POST" novalidate>
        <div class="row">
          <div class="field"><label for="jako">Piszę jako</label>
            <select id="jako" name="jako"><option value="firma">Firma — zapytanie o projekt</option><option value="fachowiec">Fachowiec — aplikacja</option></select></div>
          <div class="field" data-required><label for="imie">Imię i nazwisko <span class="req">*</span></label><input id="imie" name="imie" autocomplete="name"><span class="error">{ICO["alert"]}Podaj imię i nazwisko.</span></div>
        </div>
        <div class="row">
          <div class="field" data-required><label for="tel">Telefon <span class="req">*</span></label><input id="tel" name="telefon" type="tel" autocomplete="tel" placeholder="+48 600 000 000"><span class="error">{ICO["alert"]}Podaj numer telefonu, żebyśmy mogli oddzwonić.</span></div>
          <div class="field"><label for="email">E-mail</label><input id="email" name="email" type="email" autocomplete="email" placeholder="jan@firma.pl"></div>
        </div>
        <div class="field"><label for="firma">Firma</label><input id="firma" name="firma" autocomplete="organization"></div>
        <div class="field" data-required><label for="msg">Wiadomość <span class="req">*</span></label><textarea id="msg" name="wiadomosc"></textarea>
          <span class="hint" data-for="firmy">Branża, lokalizacja, termin i zakres: elektryka, mechanika czy oba.</span>
          <span class="hint" data-for="fachowcy">Projekty, na których byłeś, i od kiedy możesz jechać.</span>
          <span class="error">{ICO["alert"]}Napisz kilka zdań o projekcie.</span></div>
        <div class="field"><label class="body-sm" style="display:flex;gap:10px;align-items:flex-start;font-weight:400;color:var(--ink-muted)"><input type="checkbox" name="zgoda" required style="width:18px;height:18px;min-height:0;margin-top:3px"> Wyrażam zgodę na kontakt w sprawie mojego zapytania. <a href="polityka-prywatnosci.html" style="text-decoration:underline">Polityka prywatności</a>.</label></div>
        <div class="flex">
          <button class="btn btn--lg" type="submit"><span data-for="firmy">Wyślij zapytanie</span><span data-for="fachowcy">Wyślij aplikację</span> {ICO["aur"]}</button>
          <span class="form-status">{ICO["check"]}<span></span></span>
        </div>
      </form>
    </div>
  </div>
</section>
'''
page('kontakt.html','Kontakt — DD Volt','Wyceń projekt albo aplikuj do ekipy DD Volt. Odpowiadamy w ciągu jednego dnia roboczego.', KONTAKT)

# ---------------------------------------------------------------- polityki
def legal(name, title, body):
  html = f'''<section class="page-head on-night"><div class="container"><span class="eyebrow">Dokumenty</span><h1 class="display" style="margin-top:16px">{title}</h1></div></section>
<section class="section"><div class="container"><div class="prose">{body}</div></div></section>'''
  page(name, f'{title} — DD Volt', title, html)

legal('polityka-prywatnosci.html','Polityka prywatności','''
<p>Administratorem danych osobowych jest DD Volt [uzupełnij: pełna nazwa, adres, NIP]. Kontakt: <a href="mailto:kontakt@ddvolt.pl">kontakt@ddvolt.pl</a>.</p>
<h2>Jakie dane zbieramy</h2>
<p>Dane podane w formularzu kontaktowym: imię i nazwisko, telefon, e-mail, nazwa firmy i treść wiadomości. Nie zbieramy danych w innych celach.</p>
<h2>Po co</h2>
<ul><li>Odpowiedź na zapytanie o wycenę albo aplikację (art. 6 ust. 1 lit. b RODO).</li><li>Rekrutacja, gdy piszesz jako fachowiec (art. 6 ust. 1 lit. a i b RODO).</li></ul>
<h2>Jak długo</h2>
<p>Zapytania: do zakończenia rozmów, maksymalnie 12 miesięcy. Aplikacje: do zakończenia rekrutacji, chyba że zgodzisz się na dłużej.</p>
<h2>Komu przekazujemy</h2>
<p>Dostawcy formularza (Formspree) i poczty. Nie sprzedajemy danych.</p>
<h2>Twoje prawa</h2>
<p>Dostęp, sprostowanie, usunięcie, ograniczenie, sprzeciw, przeniesienie danych i skarga do Prezesa UODO. Napisz na adres wyżej.</p>
''')

legal('polityka-cookies.html','Polityka cookies','''
<p>Strona DD Volt używa tylko tego, co potrzebne do działania.</p>
<h2>Co zapisujemy w przeglądarce</h2>
<ul><li><code>dd-audience</code> — wybrana ścieżka (firmy / fachowcy).</li><li><code>dd-theme</code> — motyw jasny albo ciemny.</li><li><code>dd-cookies</code> — informacja, że widziałeś tę belkę.</li></ul>
<p>To dane w localStorage, nie trafiają do nas ani do nikogo innego.</p>
<h2>Zewnętrzne zasoby</h2>
<ul><li>CARTO / OpenStreetMap — kafle mapy realizacji. Przy ładowaniu kafli dostawca widzi Twój adres IP.</li></ul>
<p>Czcionki i biblioteka mapy są hostowane na naszym serwerze.</p>
<h2>Brak analityki</h2>
<p>Nie używamy Google Analytics, pikseli reklamowych ani innych narzędzi śledzących.</p>
''')

print('OK')
