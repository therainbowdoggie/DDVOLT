"""DD Volt — cała treść strony (PL + EN) i ustawienia.

Zmieniasz tekst, telefon, projekt albo ofertę pracy? Edytuj ten plik i uruchom:
    python3 tools/build.py
Generator nadpisze pliki *.html w katalogu głównym i w /en/.
"""

# ---------------------------------------------------------------- ustawienia
SITE_URL = 'https://ddvolt.com'          # adres produkcyjny (canonical, hreflang, sitemap, og:url)
PHONE = '+48 664 607 603'
PHONE_HREF = 'tel:+48664607603'
EMAIL = 'ddvoltinfo@gmail.com'
# Formularz: załóż konto na formspree.io i wklej tu adres formularza.
# Dopóki zostaje 'TWOJ_ID', formularz otwiera program pocztowy z gotową wiadomością (mailto).
FORM_ACTION = 'https://formspree.io/f/TWOJ_ID'
YEAR = 2026

# Liczby w statystykach — jedno miejsce dla całego serwisu.
PROJECTS_COUNT = 19          # „19+ realizacji”
ROBOTS = 130                 # Mercedes-Benz, Kuppenheim
ROBOTS_WEEKS = 2
MAIN_PROJECT_MONTHS = 12     # Tesla Gigafactory

# Kraje z realizacjami. Dopisz kolejne (kod ISO, nazwa PL, nazwa EN, punkt etykiety na mapie: szer., dł.).
# Liczba krajów w statystykach liczy się sama z tej listy.
COUNTRIES = [
    ('DE', 'Niemcy', 'Germany', 53.05, 9.9),
    ('IT', 'Włochy', 'Italy', 43.2, 12.2),
    ('HU', 'Węgry', 'Hungary', 46.75, 19.6),
    ('PL', 'Polska', 'Poland', 53.35, 18.6),
]

# ---------------------------------------------------------------- strony i adresy
PAGES = {
    'home':      {'pl': 'index.html',                'en': 'en/index.html'},
    'services':  {'pl': 'oferta.html',               'en': 'en/services.html'},
    'projects':  {'pl': 'realizacje.html',           'en': 'en/projects.html'},
    'about':     {'pl': 'o-nas.html',                'en': 'en/about.html'},
    'careers':   {'pl': 'kariera.html',              'en': 'en/careers.html'},
    'faq':       {'pl': 'faq.html',                  'en': 'en/faq.html'},
    'contact':   {'pl': 'kontakt.html',              'en': 'en/contact.html'},
    'privacy':   {'pl': 'polityka-prywatnosci.html', 'en': 'en/privacy-policy.html'},
    'cookies':   {'pl': 'polityka-cookies.html',     'en': 'en/cookie-policy.html'},
}
NAV = ['services', 'projects', 'about', 'careers', 'faq', 'contact']

# ---------------------------------------------------------------- teksty wspólne
UI = {
    'pl': {
        'nav': {'services': 'Oferta', 'projects': 'Realizacje', 'about': 'O nas', 'careers': 'Kariera', 'faq': 'FAQ', 'contact': 'Kontakt'},
        'skip': 'Przejdź do treści',
        'home_aria': 'DD Volt, strona główna',
        'nav_aria': 'Główna nawigacja',
        'menu_aria': 'Menu mobilne',
        'menu_open': 'Otwórz menu', 'menu_close': 'Zamknij menu',
        'aud_aria': 'Dla kogo', 'aud_firmy': 'Dla firm', 'aud_fachowcy': 'Dla fachowców',
        'quote': 'Wyceń projekt', 'apply': 'Aplikuj', 'call': 'Zadzwoń',
        'lang_switch': 'English', 'lang_code': 'EN', 'lang_aria': 'Switch to English',
        'dock_aria': 'Szybki kontakt',
        'copied': 'Numer skopiowany',
        'footer_tag': 'Montaż elektryczny i mechaniczny linii produkcyjnych oraz instalacji przemysłowych. Działamy w całej Europie.',
        'f_site': 'Serwis', 'f_for': 'Dla kogo', 'f_contact': 'Kontakt',
        'f_firmy': 'Dla firm: wycena projektu', 'f_fachowcy': 'Dla fachowców: praca', 'f_map': 'Mapa realizacji', 'f_form': 'Formularz kontaktowy',
        'theme': 'Ciemny motyw', 'privacy': 'Polityka prywatności', 'cookies': 'Polityka cookies',
        'scope': 'Zakres prac', 'requirements': 'Wymagania', 'details': 'Szczegóły',
        'open_recruitment': 'Rekrutacja otwarta',
        'months': 'mies.', 'weeks': 'tyg.',
        'stat_projects': 'realizacji w automotive i przemyśle',
        'stat_countries': 'kraje: {list}',
        'stat_main': 'główny projekt: Tesla Gigafactory',
        'stat_robots': 'robotów zamontowanych w {w} tygodnie, Mercedes-Benz Kuppenheim',
        'stat_reply': 'roboczy na odpowiedź na zapytanie', 'stat_reply_unit': 'dzień',
        'cta_firmy_h': 'Porozmawiajmy o Twoim projekcie.',
        'cta_firmy_p': 'W sprawie wyceny podaj lokalizację, termin oraz zakres planowanych prac. Odpowiadamy w ciągu jednego dnia roboczego.',
        'cta_fach_h': 'Dołącz do zespołu DD Volt.',
        'cta_fach_p': 'Prześlij CV lub krótką informację o doświadczeniu i dostępności. Odpowiadamy w ciągu jednego dnia roboczego.',
        'clients_aria': 'Projekty, przy których pracowaliśmy',
        'sectors': {'automotive': 'Automotive', 'industry': 'Przemysł', 'buildings': 'Obiekty'},
        'all': 'Wszystkie', 'map_aria': 'Mapa realizacji w Europie', 'map_reset': 'Pokaż wszystkie', 'map_zoom_in': 'Przybliż mapę', 'map_zoom_out': 'Oddal mapę', 'map_filter_aria': 'Filtr branży',
        'map_list_aria': 'Lista realizacji',
        'loc_forms': ['lokalizacja', 'lokalizacje', 'lokalizacji'],
        'and': 'i',
    },
    'en': {
        'nav': {'services': 'Services', 'projects': 'Projects', 'about': 'About', 'careers': 'Careers', 'faq': 'FAQ', 'contact': 'Contact'},
        'skip': 'Skip to content',
        'home_aria': 'DD Volt, home page',
        'nav_aria': 'Main navigation',
        'menu_aria': 'Mobile menu',
        'menu_open': 'Open menu', 'menu_close': 'Close menu',
        'aud_aria': 'Audience', 'aud_firmy': 'For companies', 'aud_fachowcy': 'For job seekers',
        'quote': 'Request a quote', 'apply': 'Apply', 'call': 'Call us',
        'lang_switch': 'Polski', 'lang_code': 'PL', 'lang_aria': 'Przełącz na polski',
        'dock_aria': 'Quick contact',
        'copied': 'Number copied',
        'footer_tag': 'Electrical and mechanical installation of production lines and industrial systems. We work across Europe.',
        'f_site': 'Site', 'f_for': 'Who it is for', 'f_contact': 'Contact',
        'f_firmy': 'For companies: project quote', 'f_fachowcy': 'For job seekers: careers', 'f_map': 'Project map', 'f_form': 'Contact form',
        'theme': 'Dark theme', 'privacy': 'Privacy policy', 'cookies': 'Cookie policy',
        'scope': 'Scope of work', 'requirements': 'Requirements', 'details': 'Details',
        'open_recruitment': 'Now hiring',
        'months': 'mo.', 'weeks': 'wk.',
        'stat_projects': 'projects in automotive and industry',
        'stat_countries': 'countries: {list}',
        'stat_main': 'main project: Tesla Gigafactory',
        'stat_robots': 'robots installed in {w} weeks, Mercedes-Benz Kuppenheim',
        'stat_reply': 'to reply to your enquiry', 'stat_reply_unit': 'business day',
        'cta_firmy_h': 'Let’s talk about your project.',
        'cta_firmy_p': 'For a quote, tell us the location, the timeline and the scope of the planned work. We reply within one business day.',
        'cta_fach_h': 'Join the DD Volt team.',
        'cta_fach_p': 'Send us your CV or a short note about your experience and availability. We reply within one business day.',
        'clients_aria': 'Projects we have worked on',
        'sectors': {'automotive': 'Automotive', 'industry': 'Industry', 'buildings': 'Buildings'},
        'all': 'All', 'map_aria': 'Map of our projects in Europe', 'map_reset': 'Show all', 'map_zoom_in': 'Zoom in', 'map_zoom_out': 'Zoom out', 'map_filter_aria': 'Sector filter',
        'map_list_aria': 'Project list',
        'loc_forms': ['location', 'locations', 'locations'],
        'and': 'and',
    },
}

# ---------------------------------------------------------------- usługi
SERVICES = [
    {'id': {'pl': 'elektryka', 'en': 'electrical'}, 'art': 'wire',
     'title': {'pl': 'Elektryka', 'en': 'Electrical'},
     'text': {'pl': 'Wykonujemy trasy kablowe, okablowanie oraz montaż i podłączenia urządzeń przemysłowych zgodnie z dokumentacją techniczną.',
              'en': 'We install cable routes and cabling, and mount and connect industrial equipment in line with the technical documentation.'},
     'items': {'pl': ['Czytanie schematów i EPLAN', 'Montaż tras kablowych i okablowania', 'Montaż i podłączanie szaf sterowniczych', 'Podłączanie maszyn, silników i czujników'],
               'en': ['Reading schematics and EPLAN', 'Installing cable routes and cabling', 'Mounting and connecting control cabinets', 'Connecting machines, motors and sensors']}},
    {'id': {'pl': 'mechanika', 'en': 'mechanical'}, 'art': 'robot',
     'title': {'pl': 'Mechanika', 'en': 'Mechanical'},
     'text': {'pl': 'Zajmujemy się montażem mechanicznym linii produkcyjnych, instalacją robotów przemysłowych oraz przygotowaniem urządzeń do uruchomienia.',
              'en': 'We handle the mechanical assembly of production lines, install industrial robots and prepare equipment for start-up.'},
     'items': {'pl': ['Montaż robotów przemysłowych', 'Montaż i ustawianie urządzeń', 'Montaż mechaniczny linii produkcyjnych', 'Wsparcie przy uruchomieniach'],
               'en': ['Installing industrial robots', 'Installing and positioning equipment', 'Mechanical assembly of production lines', 'Commissioning support']}},
    {'id': {'pl': 'obiekty', 'en': 'buildings'}, 'art': 'building',
     'title': {'pl': 'Obiekty i budynki', 'en': 'Facilities and buildings'},
     'text': {'pl': 'Wykonujemy instalacje elektryczne w obiektach przemysłowych, komercyjnych i użyteczności publicznej.',
              'en': 'We carry out electrical installations in industrial, commercial and public buildings.'},
     'items': {'pl': ['Instalacje oświetleniowe i siłowe', 'Montaż rozdzielnic elektrycznych', 'Okablowanie i trasy kablowe', 'Instalacje elektryczne w budynkach'],
               'en': ['Lighting and power installations', 'Switchboard installation', 'Cabling and cable routes', 'Electrical installations in buildings']}},
]

# ---------------------------------------------------------------- etapy pracy
STEPS = [
    ({'pl': 'Dokumentacja', 'en': 'Documentation'},
     {'pl': 'Analizujemy dokumentację techniczną i ustalamy zakres oraz harmonogram prac.',
      'en': 'We review the technical documentation and agree the scope and schedule of the work.'}),
    ({'pl': 'Organizacja zespołu', 'en': 'Team organisation'},
     {'pl': 'Dobieramy odpowiednią ekipę i organizujemy pracę na miejscu realizacji.',
      'en': 'We select the right crew and organise the work on site.'}),
    ({'pl': 'Montaż i podłączenia', 'en': 'Assembly and connections'},
     {'pl': 'Wykonujemy montaż elektryczny i mechaniczny zgodnie z dokumentacją techniczną.',
      'en': 'We carry out the electrical and mechanical installation in line with the technical documentation.'}),
    ({'pl': 'Zakończenie prac', 'en': 'Completion'},
     {'pl': 'Sprawdzamy wykonane instalacje i przekazujemy je do dalszych etapów realizacji.',
      'en': 'We check the completed installations and hand them over for the next stages of the project.'}),
]

# ---------------------------------------------------------------- dlaczego my
WHY = [
    ('doc', {'pl': 'Znajomość dokumentacji technicznej', 'en': 'Command of technical documentation'},
     {'pl': 'Pracujemy na podstawie schematów elektrycznych, EPLAN oraz dokumentacji technicznej.',
      'en': 'We work from electrical schematics, EPLAN and technical documentation.'}),
    ('team', {'pl': 'Organizacja pracy', 'en': 'Work organisation'},
     {'pl': 'Zapewniamy sprawną koordynację prac i bieżącą współpracę z generalnym wykonawcą.',
      'en': 'We ensure smooth coordination of the work and day-to-day cooperation with the general contractor.'}),
    ('link', {'pl': 'Kompleksowy zakres usług', 'en': 'Full scope of services'},
     {'pl': 'Łączymy montaż elektryczny i mechaniczny, zapewniając sprawną realizację projektów.',
      'en': 'We combine electrical and mechanical installation to keep projects running smoothly.'}),
    ('globe', {'pl': 'Doświadczenie międzynarodowe', 'en': 'International experience'},
     {'pl': 'Posiadamy doświadczenie zdobyte przy realizacji projektów przemysłowych i automotive w Europie.',
      'en': 'Our experience comes from delivering industrial and automotive projects in Europe.'}),
]

# ---------------------------------------------------------------- realizacje
# Kolejność = kolejność na liście i w kartach. `points`: jedna lub kilka lokalizacji (pinezek).
# `approx: True` — znamy kraj, ale nie miasto; pinezka jest wtedy pusta w środku i bez nazwy miasta.
# `img`: ścieżka do zdjęcia albo logo (np. 'assets/realizacje/tesla.jpg'). Puste = karta bez zdjęcia.
PROJECTS = [
    {'id': 'tesla', 'client': 'Tesla Gigafactory', 'sector': 'automotive', 'cc': 'DE', 'img': '',
     'scope': {'pl': 'Linia produkcyjna', 'en': 'Production line'},
     'badge': {'pl': 'Główny projekt', 'en': 'Main project'},
     'points': [{'city': {'pl': 'Grünheide', 'en': 'Grünheide'}, 'lat': 52.3926, 'lon': 13.8084}],
     'text': {'pl': 'Rok pracy przy budowie linii produkcyjnej. Montaż elektryczny i mechaniczny.',
              'en': 'A year of work on building the production line. Electrical and mechanical installation.'},
     'facts': {'pl': ['12 mies.', 'Elektryka i mechanika'], 'en': ['12 months', 'Electrical and mechanical']}},
    {'id': 'mercedes', 'client': 'Mercedes-Benz', 'sector': 'automotive', 'cc': 'DE', 'img': '',
     'scope': {'pl': 'Montaż robotów', 'en': 'Robot installation'},
     'points': [{'city': {'pl': 'Kuppenheim', 'en': 'Kuppenheim'}, 'lat': 48.8275, 'lon': 8.2545}],
     'text': {'pl': 'Montaż 130 robotów przemysłowych w dwa tygodnie.',
              'en': '130 industrial robots installed in two weeks.'},
     'facts': {'pl': ['2 tygodnie', '130 robotów'], 'en': ['2 weeks', '130 robots']}},
    {'id': 'ford', 'client': 'Ford', 'sector': 'automotive', 'cc': 'DE', 'img': '',
     'scope': {'pl': 'Linia produkcyjna i lakiernia', 'en': 'Production line and paint shop'},
     'points': [{'city': {'pl': 'Kolonia', 'en': 'Cologne'}, 'lat': 50.9375, 'lon': 6.9603}],
     'text': {'pl': 'Instalacje elektryczne linii produkcyjnej i lakierni.',
              'en': 'Electrical installations for the production line and paint shop.'},
     'facts': {'pl': ['24 mies.', 'Elektryka'], 'en': ['24 months', 'Electrical']}},
    {'id': 'bmw', 'client': 'BMW', 'sector': 'automotive', 'cc': 'DE', 'img': '',
     'scope': {'pl': 'Linia produkcyjna', 'en': 'Production line'},
     'points': [{'city': {'pl': 'Monachium', 'en': 'Munich'}, 'lat': 48.1351, 'lon': 11.5820}],
     'text': {'pl': 'Montaż elektryczny i mechaniczny linii produkcyjnej, w roli podwykonawcy firmy Nadax.',
              'en': 'Electrical and mechanical installation of the production line, as a subcontractor to Nadax.'},
     'facts': {'pl': ['Elektryka i mechanika'], 'en': ['Electrical and mechanical']}},
    {'id': 'audi', 'client': 'Audi', 'sector': 'automotive', 'cc': 'HU', 'img': '',
     'scope': {'pl': 'Zakład produkcyjny', 'en': 'Production plant'},
     'points': [{'city': {'pl': 'Győr', 'en': 'Győr'}, 'lat': 47.6875, 'lon': 17.6504}],
     'text': {'pl': 'Dwa miesiące pracy na linii produkcyjnej: okablowanie i podłączenia.',
              'en': 'Two months on the production line: cabling and connections.'},
     'facts': {'pl': ['2 mies.', 'Elektryka'], 'en': ['2 months', 'Electrical']}},
    {'id': 'bergamo', 'client': {'pl': 'Lakiernia', 'en': 'Paint shop'}, 'sector': 'automotive', 'cc': 'IT', 'img': '',
     'scope': {'pl': 'Instalacje elektryczne i mechaniczne', 'en': 'Electrical and mechanical installations'},
     'points': [{'city': {'pl': 'Bergamo', 'en': 'Bergamo'}, 'lat': 45.6983, 'lon': 9.6773}],
     'text': {'pl': 'Instalacje elektryczne i mechaniczne lakierni. Trzy miesiące pracy zespołu na miejscu.',
              'en': 'Electrical and mechanical installations for a paint shop. Three months with the team on site.'},
     'facts': {'pl': ['3 mies.', 'Elektryka i mechanika'], 'en': ['3 months', 'Electrical and mechanical']}},
    {'id': 'microsoft', 'client': 'Microsoft', 'sector': 'buildings', 'cc': 'DE', 'img': '',
     'scope': {'pl': 'Serwerownia', 'en': 'Data centre'},
     'points': [{'approx': True, 'lat': 51.1657, 'lon': 10.4515}],
     'text': {'pl': 'Instalacja elektryczna serwerowni. Prowadzenie zespołu w roli lidera.',
              'en': 'Electrical installation for a data centre. Leading the crew as team leader.'},
     'facts': {'pl': ['2 mies.', 'Elektryka'], 'en': ['2 months', 'Electrical']}},
    {'id': 'frankfurt', 'client': {'pl': 'Producent wód mineralnych', 'en': 'Mineral water producer'}, 'sector': 'industry', 'cc': 'DE', 'img': '',
     'scope': {'pl': 'Linia rozlewnicza', 'en': 'Bottling line'},
     'points': [{'city': {'pl': 'Frankfurt', 'en': 'Frankfurt'}, 'lat': 50.1109, 'lon': 8.6821}],
     'text': {'pl': 'Instalacja elektryczna linii rozlewniczej w zakładzie spożywczym.',
              'en': 'Electrical installation of a bottling line at a food and beverage plant.'},
     'facts': {'pl': ['2 mies.', 'Elektryka'], 'en': ['2 months', 'Electrical']}},
    {'id': 'szkoly', 'client': {'pl': 'Szkoły', 'en': 'Schools'}, 'sector': 'buildings', 'cc': 'DE', 'img': '',
     'scope': {'pl': 'Instalacje elektryczne', 'en': 'Electrical installations'},
     'points': [{'approx': True, 'lat': 49.6, 'lon': 9.75}],
     'text': {'pl': 'Kompletne instalacje elektryczne w kilku obiektach szkolnych: oświetlenie, instalacje siłowe i rozdzielnice.',
              'en': 'Complete electrical installations in several school buildings: lighting, power and switchboards.'},
     'facts': {'pl': ['Kilka obiektów', 'Elektryka'], 'en': ['Several buildings', 'Electrical']}},
    {'id': 'zawiercie', 'client': {'pl': 'Piece przemysłowe', 'en': 'Industrial furnaces'}, 'sector': 'industry', 'cc': 'PL', 'img': '',
     'scope': {'pl': 'Instalacje elektryczne', 'en': 'Electrical installations'},
     'points': [{'city': {'pl': 'Zawiercie', 'en': 'Zawiercie'}, 'lat': 50.4879, 'lon': 19.4166}],
     'text': {'pl': 'Instalacje elektryczne pieców przemysłowych.',
              'en': 'Electrical installations for industrial furnaces.'},
     'facts': {'pl': ['Elektryka'], 'en': ['Electrical']}},
    {'id': 'silniki', 'client': {'pl': 'Podłączenie silników', 'en': 'Motor connections'}, 'sector': 'industry', 'cc': 'PL', 'img': '',
     'scope': {'pl': 'Hale produkcyjne', 'en': 'Production halls'},
     'points': [{'city': {'pl': 'Warszawa', 'en': 'Warsaw'}, 'lat': 52.2297, 'lon': 21.0122},
                {'city': {'pl': 'Częstochowa', 'en': 'Częstochowa'}, 'lat': 50.8118, 'lon': 19.1203}],
     'text': {'pl': 'Podłączenia silników i urządzeń w halach produkcyjnych.',
              'en': 'Connecting motors and equipment in production halls.'},
     'facts': {'pl': ['2 lokalizacje', 'Elektryka'], 'en': ['2 locations', 'Electrical']}},
]

# Pasek z nazwami pod hero: (nazwa, miejsce PL, miejsce EN)
CLIENTS = [
    ('Tesla', 'Grünheide', 'Grünheide'), ('Mercedes-Benz', 'Kuppenheim', 'Kuppenheim'), ('Ford', 'Kolonia', 'Cologne'),
    ('BMW', 'Monachium', 'Munich'), ('Audi', 'Győr', 'Győr'), ('Microsoft', 'serwerownia', 'data centre'),
]

# ---------------------------------------------------------------- oferty pracy
JOBS = [
    {'slug': 'elektryk', 'title': {'pl': 'Elektryk przemysłowy', 'en': 'Industrial electrician'},
     'sector': {'pl': 'Automotive', 'en': 'Automotive'},
     'req': {'pl': ['Znajomość schematów elektrycznych i EPLAN', 'Doświadczenie w instalacjach przemysłowych', 'Umiejętność samodzielnej pracy', 'Gotowość do wyjazdów zagranicznych'],
             'en': ['Knowledge of electrical schematics and EPLAN', 'Experience with industrial installations', 'Ability to work independently', 'Willingness to travel abroad']}},
    {'slug': 'monter', 'title': {'pl': 'Monter mechanik – roboty i linie', 'en': 'Mechanical fitter – robots and lines'},
     'sector': {'pl': 'Przemysł', 'en': 'Industry'},
     'req': {'pl': ['Doświadczenie w montażu linii produkcyjnych', 'Znajomość rysunku technicznego', 'Umiejętność obsługi narzędzi montażowych', 'Samodzielność i dokładność'],
             'en': ['Experience in assembling production lines', 'Ability to read technical drawings', 'Skilled use of assembly tools', 'Independence and precision']}},
    {'slug': 'pomocnik', 'title': {'pl': 'Pomocnik elektryka / montera', 'en': 'Electrician’s / fitter’s helper'},
     'sector': {'pl': 'Przemysł i automotive', 'en': 'Industry and automotive'},
     'req': {'pl': ['Chęć nauki i rozwoju zawodowego', 'Podstawowa znajomość narzędzi', 'Zaangażowanie i sumienność', 'Gotowość do wyjazdów zagranicznych'],
             'en': ['Willingness to learn and grow professionally', 'Basic knowledge of tools', 'Commitment and reliability', 'Willingness to travel abroad']}},
    {'slug': 'lider', 'title': {'pl': 'Lider zespołu – elektryka', 'en': 'Team leader – electrical'},
     'sector': {'pl': 'Automotive', 'en': 'Automotive'},
     'req': {'pl': ['Doświadczenie w prowadzeniu zespołu (minimum 5 osób)', 'Umiejętność organizacji pracy na projekcie', 'Komunikatywny angielski lub niemiecki', 'Gotowość do wyjazdów zagranicznych'],
             'en': ['Experience leading a team (at least 5 people)', 'Ability to organise work on a project', 'Communicative English or German', 'Willingness to travel abroad']}},
]
JOB_TYPE = {'pl': 'Umowa / B2B', 'en': 'Contract / B2B'}
JOB_PLACE = {'pl': 'Europa, wyjazdy', 'en': 'Europe, travel'}
JOBS_ON_HOME = 3

# ---------------------------------------------------------------- FAQ
FAQ_FIRMY = [
    ({'pl': 'Na jakim obszarze działacie?', 'en': 'Where do you operate?'},
     {'pl': 'Realizujemy projekty przemysłowe i automotive na terenie całej Europy.',
      'en': 'We deliver industrial and automotive projects throughout Europe.'}),
    ({'pl': 'Na podstawie jakiej dokumentacji pracujecie?', 'en': 'What documentation do you work from?'},
     {'pl': 'Pracujemy zgodnie ze schematami elektrycznymi, EPLAN, rysunkami technicznymi i dokumentacją projektową.',
      'en': 'We work from electrical schematics, EPLAN, technical drawings and project documentation.'}),
    ({'pl': 'Czy zajmujecie się wyłącznie elektryką?', 'en': 'Do you only do electrical work?'},
     {'pl': 'Nie. Oferujemy również montaż mechaniczny linii produkcyjnych oraz robotów przemysłowych.',
      'en': 'No. We also provide mechanical assembly of production lines and industrial robots.'}),
    ({'pl': 'Jak szybko możecie rozpocząć projekt?', 'en': 'How quickly can you start a project?'},
     {'pl': 'Termin rozpoczęcia ustalamy indywidualnie, w zależności od zakresu prac i dostępności zespołu.',
      'en': 'We agree the start date individually, depending on the scope of work and team availability.'}),
    ({'pl': 'Czy zatrudniacie osoby bez doświadczenia?', 'en': 'Do you hire people without experience?'},
     {'pl': 'Tak. Oferujemy możliwość przyuczenia osobom, które chcą rozwijać się w elektryce i mechanice przemysłowej.',
      'en': 'Yes. We offer on-the-job training to people who want to develop in industrial electrical and mechanical work.'}),
]
FAQ_FACHOWCY = [
    ({'pl': 'Jaka jest forma współpracy?', 'en': 'What form of cooperation do you offer?'},
     {'pl': 'Umowa albo B2B, do wyboru. Przy B2B pomagamy w formalnościach na początku współpracy.',
      'en': 'An employment contract or B2B, whichever you prefer. With B2B we help with the paperwork at the start.'}),
    ({'pl': 'Jak wyglądają wyjazdy?', 'en': 'What are the assignments like?'},
     {'pl': 'Projekty trwają od kilku tygodni do kilkunastu miesięcy. Zakwaterowanie i dojazd ustalamy przed wyjazdem.',
      'en': 'Projects last from a few weeks to over a year. Accommodation and travel are agreed before you leave.'}),
    ({'pl': 'Jakie są wymagania?', 'en': 'What are the requirements?'},
     {'pl': 'Zależą od stanowiska. Od elektryków oczekujemy znajomości schematów elektrycznych, od monterów doświadczenia w montażu mechanicznym. Na stanowisko pomocnika przyjmujemy również osoby bez doświadczenia.',
      'en': 'They depend on the role. Electricians need to know electrical schematics, fitters need experience in mechanical assembly. For helper roles we also take on people without experience.'}),
    ({'pl': 'Czy muszę znać język obcy?', 'en': 'Do I need to speak a foreign language?'},
     {'pl': 'Podstawy angielskiego albo niemieckiego są pomocne, ale nie na każdym stanowisku wymagane. Komunikację na projekcie prowadzi lider.',
      'en': 'Basic English or German helps, but it is not required for every role. The team leader handles communication on the project.'}),
    ({'pl': 'Jak aplikować?', 'en': 'How do I apply?'},
     {'pl': 'Wyślij zgłoszenie przez formularz kontaktowy albo zadzwoń. Możesz przesłać CV lub krótką informację o doświadczeniu i dostępności.',
      'en': 'Send an application through the contact form or call us. You can send your CV or a short note about your experience and availability.'}),
]

# ---------------------------------------------------------------- teksty stron
T = {
    'pl': {
        'home': {
            'title': 'DD Volt | Montaż elektryczny i mechaniczny linii produkcyjnych',
            'desc': 'Montaż elektryczny i mechaniczny linii produkcyjnych oraz instalacji przemysłowych. Automotive i przemysł, projekty w całej Europie.',
            'h1_firmy': 'Linie produkcyjne podłączone od A do Z.',
            'lead_firmy': 'Realizujemy projekty z zakresu montażu elektrycznego i mechanicznego linii produkcyjnych oraz instalacji przemysłowych. Od przygotowania instalacji, przez montaż i podłączenia, aż po wsparcie podczas uruchomienia. Działamy na terenie całej Europy.',
            'h1_fach': 'Praca przy montażu linii produkcyjnych w całej Europie.',
            'lead_fach': 'Zatrudniamy elektryków, monterów i pomocników. Umowa albo B2B, lider na miejscu, warunki ustalone przed wyjazdem.',
            'see_projects': 'Zobacz realizacje', 'see_jobs': 'Zobacz oferty pracy',
            'wave_aria': 'Animacja: trzy fazy prądu przemiennego',
            'offer_h': 'Elektryka i mechanika linii od A do Z.',
            'offer_p': 'Zajmujemy się montażem elektrycznym i mechanicznym linii produkcyjnych oraz instalacji przemysłowych, zgodnie z dokumentacją techniczną i obowiązującymi standardami.',
            'offer_more': 'Cała oferta',
            'map_h': 'Gdzie już pracowaliśmy.',
            'map_p': '{countries}. Wybierz punkt na mapie albo projekt z listy.',
            'map_more': 'Wszystkie realizacje',
            'steps_h': 'Od dokumentacji do realizacji.',
            'why_h': 'Doświadczenie, jakość i terminowość.',
            'why_p': 'Stawiamy na rzetelne wykonanie, dobrą organizację pracy i terminową realizację projektów. Nasze doświadczenie zdobywaliśmy przy projektach przemysłowych i automotive w całej Europie.',
            'why_btn': 'Zobacz nasze realizacje',
            'jobs_h': 'Szukamy ludzi, którzy umieją czytać schemat.',
            'jobs_p': 'Umowa albo B2B. Projekty w całej Europie, lider na miejscu, warunki ustalone przed wyjazdem.',
            'jobs_more': 'Wszystkie oferty',
            'faq_h': 'Najczęściej zadawane pytania',
            'faq_more': 'Wszystkie pytania',
        },
        'services': {
            'title': 'Oferta | DD Volt',
            'desc': 'Instalacje elektryczne i prace montażowe w przemyśle oraz branży automotive: elektryka, mechanika, obiekty i budynki.',
            'h1': 'Od projektu do sprawnej instalacji',
            'lead': 'Realizujemy instalacje elektryczne i prace montażowe w przemyśle oraz branży automotive. Od tras kablowych po podłączenie maszyn, urządzeń i robotów przemysłowych.',
            'sectors_h': 'Branże, w których pracujemy',
            'sectors': [
                ('Automotive', 'Linie produkcyjne, lakiernie i stanowiska robotów. Między innymi projekty dla Tesli, Mercedesa, Forda, BMW i Audi.'),
                ('Przemysł', 'Linie rozlewnicze, piece przemysłowe oraz podłączenia silników i urządzeń w halach produkcyjnych.'),
                ('Obiekty', 'Serwerownie, szkoły oraz obiekty komercyjne i użyteczności publicznej.'),
            ],
            'steps_h': 'Od dokumentacji do realizacji.',
            'reach_h': 'Działamy w całej Europie. Bez granic dla nowych projektów.',
            'reach_p': 'Realizujemy projekty przemysłowe i automotive w Polsce oraz za granicą. Posiadamy doświadczenie w pracy na międzynarodowych inwestycjach i jesteśmy otwarci na nowe lokalizacje.',
            'stat_countries': 'kraje z realizacjami', 'stat_projects': 'zrealizowanych projektów',
        },
        'projects': {
            'title': 'Realizacje | DD Volt',
            'desc': 'Mapa i lista realizacji DD Volt: Tesla Gigafactory, Mercedes-Benz w Kuppenheim, Ford w Kolonii, BMW w Monachium, Audi w Győr i projekty w Polsce.',
            'h1': 'Gdzie już pracowaliśmy.',
            'lead': 'Projekty przemysłowe i automotive w Niemczech, we Włoszech, na Węgrzech i w Polsce. Przy każdej realizacji podajemy zakres prac i naszą rolę.',
            'map_h': 'Mapa realizacji',
            'map_p': 'Filtruj według branży. Wybierz punkt na mapie albo projekt z listy.',
            'list_h': 'Wybrane realizacje',
        },
        'about': {
            'title': 'O nas | DD Volt',
            'desc': 'DD Volt to elektrycy i mechanicy z doświadczeniem na liniach produkcyjnych Tesli, Mercedesa, Forda, BMW i Audi.',
            'h1': 'Elektrycy i mechanicy z doświadczeniem w automotive.',
            'lead': 'DD Volt to zespół z doświadczeniem zdobytym na liniach produkcyjnych Tesli, Mercedesa, Forda, BMW i Audi. Realizujemy montaż elektryczny i mechaniczny w zakładach przemysłowych w całej Europie.',
            'story_h': 'Od Kolonii do własnej firmy.',
            'story': [
                'Zaczęło się od dwóch lat pracy na linii produkcyjnej i w lakierni Forda w Kolonii, w roli podwykonawcy firmy SICA. Później były zakład Audi na Węgrzech, serwerownia Microsoftu i szkoły w Niemczech.',
                'Rok pracy przy Tesla Gigafactory to już własna działalność. Kolejne projekty to między innymi lakiernia w Bergamo, zakład we Frankfurcie, linia BMW w Monachium, 130 robotów zamontowanych w dwa tygodnie w zakładzie Mercedesa w Kuppenheim oraz realizacje w Polsce.',
                'Dziś łączymy montaż elektryczny i mechaniczny w jednym zespole i stale go powiększamy.',
            ],
            'rules_h': 'Jak pracujemy',
            'rules': [
                ('doc', 'Praca zgodnie z dokumentacją', 'Prace realizujemy na podstawie schematów elektrycznych, EPLAN i dokumentacji technicznej.'),
                ('check', 'Jasne ustalenia', 'Zakres, termin i skład zespołu ustalamy przed rozpoczęciem prac.'),
                ('team', 'Lider na miejscu', 'Na każdym projekcie pracę zespołu koordynuje lider, który odpowiada za organizację i bieżące ustalenia.'),
                ('link', 'Przejrzyste warunki współpracy', 'Formę współpracy, zakwaterowanie i stawki ustalamy z pracownikami przed wyjazdem.'),
            ],
            'btn': 'Zobacz nasze realizacje',
        },
        'careers': {
            'title': 'Kariera | DD Volt',
            'desc': 'Praca dla elektryków przemysłowych, monterów mechaników i pomocników: projekty w Europie, umowa albo B2B, lider na miejscu.',
            'h1': 'Szukamy ludzi, którzy umieją czytać schemat.',
            'lead': 'Umowa albo B2B. Projekty w Niemczech, we Włoszech, na Węgrzech i w Polsce. Lider na miejscu i warunki ustalone przed wyjazdem.',
            'chips': ['Umowa lub B2B', 'Projekty w Europie'],
            'jobs_h': 'Aktualne oferty',
            'process_h': 'Jak wygląda rekrutacja',
            'process': [
                ('Kontakt', 'Wysyłasz zgłoszenie przez formularz albo dzwonisz. Pytamy o doświadczenie i dostępność.'),
                ('Warunki', 'Ustalamy formę współpracy, stawkę, zakwaterowanie i termin wyjazdu.'),
                ('Wyjazd', 'Jedziesz na projekt z zespołem i liderem, który zna zakres prac.'),
                ('Kolejne projekty', 'Sprawdzonym pracownikom proponujemy udział w następnych realizacjach.'),
            ],
            'faq_h': 'Pytania kandydatów',
        },
        'faq': {
            'title': 'FAQ | DD Volt',
            'desc': 'Najczęściej zadawane pytania o współpracę z DD Volt: dla firm i dla osób szukających pracy.',
            'h1': 'Najczęściej zadawane pytania',
            'lead': 'Odpowiedzi dla firm i dla osób szukających pracy. Wybierz zestaw pytań.',
        },
        'contact': {
            'title': 'Kontakt | DD Volt',
            'desc': 'Wyceń projekt albo aplikuj do zespołu DD Volt. Telefon: +48 664 607 603. Odpowiadamy w ciągu jednego dnia roboczego.',
            'h1_firmy': 'Porozmawiajmy o Twoim projekcie.',
            'h1_fach': 'Dołącz do naszego zespołu.',
            'lead': 'Odpowiadamy w ciągu jednego dnia roboczego. Możesz też zadzwonić.',
            'direct': 'Kontakt bezpośredni',
            'phone_label': 'Telefon', 'email_label': 'E-mail',
            'note': 'W sprawie wyceny podaj lokalizację, termin oraz zakres planowanych prac. Jeśli szukasz pracy, prześlij nam swoje CV lub krótką informację o doświadczeniu i dostępności.',
            'cv_mail': 'Wyślij CV e-mailem',
            'cv_subject': 'CV: aplikacja do DD Volt',
            'form': {
                'legend': 'W jakiej sprawie piszesz?', 'topic_firmy': 'Wycena projektu', 'topic_fach': 'Praca',
                'name': 'Imię i nazwisko', 'phone': 'Telefon', 'email': 'E-mail', 'optional': 'opcjonalnie',
                'company': 'Firma', 'location': 'Lokalizacja projektu', 'location_ph': 'np. Stuttgart, Niemcy',
                'date': 'Planowany termin', 'date_ph': 'np. marzec 2027',
                'scope': 'Zakres prac', 'scope_opts': ['Elektryka', 'Mechanika', 'Obiekty i budynki'],
                'role': 'Stanowisko', 'role_opts': [('elektryk', 'Elektryk przemysłowy'), ('monter', 'Monter mechanik'), ('pomocnik', 'Pomocnik'), ('lider', 'Lider zespołu')],
                'more_firmy': 'Dodaj e-mail, firmę, lokalizację i termin', 'more_fach': 'Dodaj e-mail i termin rozpoczęcia',
                'avail': 'Od kiedy możesz zacząć?', 'avail_ph': 'np. od zaraz, od 1 grudnia',
                'msg_firmy': 'Opis zakresu prac', 'msg_firmy_hint': 'Kilka zdań wystarczy. Dokumentację można przesłać później.',
                'msg_fach': 'Doświadczenie', 'msg_fach_hint': 'Napisz krótko, przy jakich projektach pracowałeś i czym się zajmowałeś.',
                'consent': 'Wyrażam zgodę na kontakt w sprawie mojego zgłoszenia.', 'consent_link': 'Polityka prywatności',
                'submit_firmy': 'Wyślij zapytanie', 'submit_fach': 'Wyślij zgłoszenie', 'sending': 'Wysyłanie…',
                'err_name': 'Podaj imię i nazwisko.', 'err_phone': 'Podaj numer telefonu, żebyśmy mogli oddzwonić.',
                'err_email': 'Sprawdź adres e-mail.', 'err_consent': 'Zaznacz zgodę, żebyśmy mogli odpowiedzieć.',
                'ok_h': 'Dziękujemy, wiadomość wysłana.', 'ok_p': 'Odpowiemy w ciągu jednego dnia roboczego.', 'ok_again': 'Wyślij kolejną wiadomość',
                'fail': 'Nie udało się wysłać wiadomości. Zadzwoń pod {phone} albo napisz na {email}.',
                'mailto': 'Otworzyliśmy Twój program pocztowy z gotową wiadomością. Wystarczy ją wysłać.',
                'draft': 'Przywróciliśmy niewysłaną wiadomość.', 'draft_clear': 'Wyczyść',
                'mail_subject_firmy': 'Zapytanie o wycenę', 'mail_subject_fach': 'Aplikacja',
            },
        },
        'privacy': {
            'title': 'Polityka prywatności | DD Volt', 'h1': 'Polityka prywatności',
            'desc': 'Jak DD Volt przetwarza dane osobowe z formularza kontaktowego: zakres, cel, okres przechowywania i Twoje prawa.',
            'body': '''
<p>Administratorem danych osobowych jest DD Volt [uzupełnij: pełna nazwa, adres, NIP]. Kontakt: <a href="mailto:{email}">{email}</a>.</p>
<h2>Jakie dane zbieramy</h2>
<p>Dane podane w formularzu kontaktowym: imię i nazwisko, telefon, adres e-mail, nazwa firmy oraz treść wiadomości. Nie zbieramy danych w innych celach.</p>
<h2>W jakim celu</h2>
<ul><li>Odpowiedź na zapytanie o wycenę (art. 6 ust. 1 lit. b RODO).</li><li>Rekrutacja, gdy wysyłasz zgłoszenie do pracy (art. 6 ust. 1 lit. a i b RODO).</li></ul>
<h2>Jak długo</h2>
<p>Zapytania przechowujemy do zakończenia rozmów, maksymalnie 12 miesięcy. Zgłoszenia do pracy do zakończenia rekrutacji, chyba że zgodzisz się na dłuższy okres.</p>
<h2>Komu przekazujemy dane</h2>
<p>Dostawcy formularza (Formspree) i poczty elektronicznej. Nie sprzedajemy danych.</p>
<h2>Twoje prawa</h2>
<p>Masz prawo dostępu do danych, ich sprostowania, usunięcia, ograniczenia przetwarzania, przeniesienia, wniesienia sprzeciwu oraz skargi do Prezesa UODO. W tych sprawach napisz na adres podany wyżej.</p>
''',
        },
        'cookies': {
            'title': 'Polityka cookies | DD Volt', 'h1': 'Polityka cookies',
            'desc': 'Strona DD Volt nie używa cookies do śledzenia ani analityki. Sprawdź, co zapisuje w przeglądarce i po co.',
            'body': '''
<p>Strona DD Volt nie używa plików cookies do śledzenia ani analityki. Zapisuje w przeglądarce tylko to, co jest potrzebne do działania.</p>
<h2>Co zapisujemy w przeglądarce</h2>
<ul>
<li><code>dd-audience</code>: wybrana wersja treści (dla firm albo dla fachowców).</li>
<li><code>dd-theme</code>: motyw jasny albo ciemny.</li>
<li><code>dd-form</code>: kopia robocza niewysłanego formularza, żeby nie zginęła po odświeżeniu strony. Znika po wysłaniu.</li>
<li><code>dd-boot</code>: informacja, że animacja powitalna została już pokazana w tej sesji.</li>
</ul>
<p>To dane w pamięci przeglądarki (localStorage i sessionStorage). Nie trafiają do nas ani do nikogo innego.</p>
<h2>Zewnętrzne zasoby</h2>
<p>Czcionki, mapa i wszystkie skrypty są hostowane razem ze stroną. Strona nie pobiera niczego z zewnętrznych serwerów.</p>
<h2>Brak analityki</h2>
<p>Nie używamy Google Analytics, pikseli reklamowych ani innych narzędzi śledzących.</p>
''',
        },
        'e404': {'title': 'Nie znaleziono strony | DD Volt', 'h1': 'Nie znaleziono strony', 'p': 'Ten adres nie istnieje albo strona została przeniesiona.', 'btn': 'Wróć na stronę główną'},
    },

    'en': {
        'home': {
            'title': 'DD Volt | Production line electrical and mechanical work',
            'desc': 'Electrical and mechanical installation of production lines and industrial systems. Automotive and industry, projects across Europe.',
            'h1_firmy': 'Production lines connected from A to Z.',
            'lead_firmy': 'We deliver electrical and mechanical installation of production lines and industrial systems. From preparing the installation, through assembly and connections, to support during commissioning. We work across Europe.',
            'h1_fach': 'Work on production line installations across Europe.',
            'lead_fach': 'We hire electricians, fitters and helpers. Employment contract or B2B, a team leader on site, terms agreed before you travel.',
            'see_projects': 'See our projects', 'see_jobs': 'See open positions',
            'wave_aria': 'Animation: three phases of alternating current',
            'offer_h': 'Electrical and mechanical work on production lines, from A to Z.',
            'offer_p': 'We carry out electrical and mechanical installation of production lines and industrial systems, in line with the technical documentation and applicable standards.',
            'offer_more': 'All services',
            'map_h': 'Where we have worked.',
            'map_p': '{countries}. Pick a point on the map or a project from the list.',
            'map_more': 'All projects',
            'steps_h': 'From documentation to delivery.',
            'why_h': 'Experience, quality and on-time delivery.',
            'why_p': 'We focus on solid workmanship, good work organisation and on-time project delivery. We gained our experience on industrial and automotive projects across Europe.',
            'why_btn': 'See our projects',
            'jobs_h': 'We are looking for people who can read a schematic.',
            'jobs_p': 'Employment contract or B2B. Projects across Europe, a team leader on site, terms agreed before you travel.',
            'jobs_more': 'All positions',
            'faq_h': 'Frequently asked questions',
            'faq_more': 'All questions',
        },
        'services': {
            'title': 'Services | DD Volt',
            'desc': 'Electrical installations and assembly work for industry and the automotive sector: electrical, mechanical, facilities and buildings.',
            'h1': 'From design to a working installation',
            'lead': 'We deliver electrical installations and assembly work for industry and the automotive sector. From cable routes to connecting machines, equipment and industrial robots.',
            'sectors_h': 'Sectors we work in',
            'sectors': [
                ('Automotive', 'Production lines, paint shops and robot cells. Projects for Tesla, Mercedes-Benz, Ford, BMW and Audi, among others.'),
                ('Industry', 'Bottling lines, industrial furnaces, and motor and equipment connections in production halls.'),
                ('Buildings', 'Data centres, schools, and commercial and public buildings.'),
            ],
            'steps_h': 'From documentation to delivery.',
            'reach_h': 'We work across Europe. No borders for new projects.',
            'reach_p': 'We deliver industrial and automotive projects in Poland and abroad. We have experience on international investments and we are open to new locations.',
            'stat_countries': 'countries with completed projects', 'stat_projects': 'completed projects',
        },
        'projects': {
            'title': 'Projects | DD Volt',
            'desc': 'Map and list of DD Volt projects: Tesla Gigafactory, Mercedes-Benz in Kuppenheim, Ford in Cologne, BMW in Munich, Audi in Győr and projects in Poland.',
            'h1': 'Where we have worked.',
            'lead': 'Industrial and automotive projects in Germany, Italy, Hungary and Poland. For each one we state the scope of work and our role.',
            'map_h': 'Project map',
            'map_p': 'Filter by sector. Pick a point on the map or a project from the list.',
            'list_h': 'Selected projects',
        },
        'about': {
            'title': 'About | DD Volt',
            'desc': 'DD Volt is a team of electricians and mechanics with experience on production lines for Tesla, Mercedes-Benz, Ford, BMW and Audi.',
            'h1': 'Electricians and mechanics with automotive experience.',
            'lead': 'DD Volt is a team with experience gained on production lines for Tesla, Mercedes-Benz, Ford, BMW and Audi. We deliver electrical and mechanical installation at industrial plants across Europe.',
            'story_h': 'From Cologne to our own company.',
            'story': [
                'It started with two years on the production line and in the paint shop at Ford in Cologne, as a subcontractor to SICA. Then came the Audi plant in Hungary, a Microsoft data centre and schools in Germany.',
                'A year at Tesla Gigafactory was already under our own business. Later projects include a paint shop in Bergamo, a plant in Frankfurt, a BMW line in Munich, 130 robots installed in two weeks at the Mercedes-Benz plant in Kuppenheim, and projects in Poland.',
                'Today we combine electrical and mechanical installation in one team, and we keep growing it.',
            ],
            'rules_h': 'How we work',
            'rules': [
                ('doc', 'Work in line with the documentation', 'We carry out the work based on electrical schematics, EPLAN and technical documentation.'),
                ('check', 'Clear arrangements', 'We agree the scope, the schedule and the crew before work begins.'),
                ('team', 'A leader on site', 'On every project a team leader coordinates the crew and is responsible for organisation and day-to-day arrangements.'),
                ('link', 'Transparent terms', 'We agree the form of cooperation, accommodation and rates with our people before they travel.'),
            ],
            'btn': 'See our projects',
        },
        'careers': {
            'title': 'Careers | DD Volt',
            'desc': 'Jobs for industrial electricians, mechanical fitters and helpers: projects in Europe, employment contract or B2B, a team leader on site.',
            'h1': 'We are looking for people who can read a schematic.',
            'lead': 'Employment contract or B2B. Projects in Germany, Italy, Hungary and Poland. A team leader on site and terms agreed before you travel.',
            'chips': ['Contract or B2B', 'Projects in Europe'],
            'jobs_h': 'Open positions',
            'process_h': 'How recruitment works',
            'process': [
                ('Contact', 'You send an application through the form or call us. We ask about your experience and availability.'),
                ('Terms', 'We agree the form of cooperation, the rate, accommodation and the travel date.'),
                ('Assignment', 'You travel to the project with the crew and a leader who knows the scope of work.'),
                ('Next projects', 'We offer proven people a place on our next projects.'),
            ],
            'faq_h': 'Questions from candidates',
        },
        'faq': {
            'title': 'FAQ | DD Volt',
            'desc': 'Frequently asked questions about working with DD Volt: for companies and for job seekers.',
            'h1': 'Frequently asked questions',
            'lead': 'Answers for companies and for job seekers. Choose a set of questions.',
        },
        'contact': {
            'title': 'Contact | DD Volt',
            'desc': 'Request a quote or apply to join the DD Volt team. Phone: +48 664 607 603. We reply within one business day.',
            'h1_firmy': 'Let’s talk about your project.',
            'h1_fach': 'Join our team.',
            'lead': 'We reply within one business day. You can also call us.',
            'direct': 'Direct contact',
            'phone_label': 'Phone', 'email_label': 'Email',
            'note': 'For a quote, tell us the location, the timeline and the scope of the planned work. If you are looking for a job, send us your CV or a short note about your experience and availability.',
            'cv_mail': 'Send your CV by email',
            'cv_subject': 'CV: application to DD Volt',
            'form': {
                'legend': 'What is your message about?', 'topic_firmy': 'Project quote', 'topic_fach': 'Job',
                'name': 'Full name', 'phone': 'Phone', 'email': 'Email', 'optional': 'optional',
                'company': 'Company', 'location': 'Project location', 'location_ph': 'e.g. Stuttgart, Germany',
                'date': 'Planned timeline', 'date_ph': 'e.g. March 2027',
                'scope': 'Scope of work', 'scope_opts': ['Electrical', 'Mechanical', 'Facilities and buildings'],
                'role': 'Position', 'role_opts': [('elektryk', 'Industrial electrician'), ('monter', 'Mechanical fitter'), ('pomocnik', 'Helper'), ('lider', 'Team leader')],
                'more_firmy': 'Add email, company, location and timeline', 'more_fach': 'Add email and start date',
                'avail': 'When can you start?', 'avail_ph': 'e.g. immediately, from 1 December',
                'msg_firmy': 'Description of the work', 'msg_firmy_hint': 'A few sentences are enough. You can send the documentation later.',
                'msg_fach': 'Experience', 'msg_fach_hint': 'Tell us briefly which projects you worked on and what you did.',
                'consent': 'I agree to be contacted about my enquiry.', 'consent_link': 'Privacy policy',
                'submit_firmy': 'Send enquiry', 'submit_fach': 'Send application', 'sending': 'Sending…',
                'err_name': 'Enter your full name.', 'err_phone': 'Enter a phone number so we can call you back.',
                'err_email': 'Check the email address.', 'err_consent': 'Tick the consent box so we can reply.',
                'ok_h': 'Thank you, your message has been sent.', 'ok_p': 'We will reply within one business day.', 'ok_again': 'Send another message',
                'fail': 'The message could not be sent. Call {phone} or write to {email}.',
                'mailto': 'We opened your email app with the message ready. Just press send.',
                'draft': 'We restored your unsent message.', 'draft_clear': 'Clear',
                'mail_subject_firmy': 'Quote request', 'mail_subject_fach': 'Job application',
            },
        },
        'privacy': {
            'title': 'Privacy policy | DD Volt', 'h1': 'Privacy policy',
            'desc': 'How DD Volt processes personal data from the contact form: scope, purpose, retention period and your rights.',
            'body': '''
<p>The controller of your personal data is DD Volt [to be completed: full name, address, tax ID]. Contact: <a href="mailto:{email}">{email}</a>.</p>
<h2>What data we collect</h2>
<p>The data you provide in the contact form: full name, phone number, email address, company name and the content of your message. We do not collect data for any other purpose.</p>
<h2>Why we collect it</h2>
<ul><li>To reply to a quote request (Article 6(1)(b) GDPR).</li><li>For recruitment, when you send a job application (Article 6(1)(a) and (b) GDPR).</li></ul>
<h2>How long we keep it</h2>
<p>Enquiries are kept until the conversation ends, for a maximum of 12 months. Job applications are kept until recruitment ends, unless you agree to a longer period.</p>
<h2>Who we share it with</h2>
<p>The form provider (Formspree) and our email provider. We do not sell data.</p>
<h2>Your rights</h2>
<p>You have the right to access, rectify and erase your data, to restrict or object to processing, to data portability, and to lodge a complaint with the President of the Polish Personal Data Protection Office (UODO). To exercise these rights, write to the address above.</p>
''',
        },
        'cookies': {
            'title': 'Cookie policy | DD Volt', 'h1': 'Cookie policy',
            'desc': 'The DD Volt website does not use cookies for tracking or analytics. See what it stores in your browser and why.',
            'body': '''
<p>The DD Volt website does not use cookies for tracking or analytics. It only stores in your browser what it needs to work.</p>
<h2>What we store in your browser</h2>
<ul>
<li><code>dd-audience</code>: the selected version of the content (for companies or for job seekers).</li>
<li><code>dd-theme</code>: light or dark theme.</li>
<li><code>dd-form</code>: a draft of an unsent form, so it is not lost when the page reloads. It is removed after sending.</li>
<li><code>dd-boot</code>: a note that the intro animation has already been shown in this session.</li>
</ul>
<p>This data stays in your browser (localStorage and sessionStorage). It is not sent to us or to anyone else.</p>
<h2>External resources</h2>
<p>Fonts, the map and all scripts are hosted together with the site. The site does not load anything from external servers.</p>
<h2>No analytics</h2>
<p>We do not use Google Analytics, advertising pixels or any other tracking tools.</p>
''',
        },
        'e404': {'title': 'Page not found | DD Volt', 'h1': 'Page not found', 'p': 'This address does not exist or the page has been moved.', 'btn': 'Back to the home page'},
    },
}
