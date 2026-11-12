# DD Volt — strona firmowa

Statyczna strona (HTML + CSS + JS, bez frameworków i bez zewnętrznych zasobów) w dwóch językach:
polski w katalogu głównym, angielski w `/en/`. Gotowa pod GitHub Pages.

## Wgranie na GitHub

Podmień całą zawartość repozytorium na pliki z tej paczki. Jeśli wgrywasz przez przeglądarkę
(„Add file → Upload files”), usuń najpierw stare rzeczy, których nowa wersja już nie używa:

- katalog `ddvolt/` (przypadkowa kopia całej strony),
- katalog `vendor/` (Leaflet; mapa jest teraz własna, w SVG),
- plik `css/fonts.css` i stare fonty w `assets/fonts/` (Bricolage Grotesque, Instrument Sans, IBM Plex Mono).

## Do uzupełnienia przed publikacją

Wszystko poniżej zmienia się w `tools/content.py`, a potem `python3 tools/build.py`.

| Co | Gdzie | Stan |
| --- | --- | --- |
| Formularz | `FORM_ACTION` | Wklej adres z formspree.io. Dopóki jest `TWOJ_ID`, formularz otwiera program pocztowy z gotową wiadomością. |
| Kraje z realizacjami | `COUNTRIES` | Są cztery: Niemcy, Włochy, Węgry, Polska. Dopisz pozostałe; liczba w statystykach przeliczy się sama. |
| Liczby | `PROJECTS_COUNT`, `MAIN_PROJECT_MONTHS`, `ROBOTS` | 19+, 12 mies. (Tesla), 130 robotów. Potwierdź 12 miesięcy. |
| E-mail | `EMAIL` | `kontakt@ddvolt.pl`. Sprawdź domenę (strona działa pod ddvolt.com). |
| Adres strony | `SITE_URL` | `https://ddvolt.com` (canonical, hreflang, sitemap). |
| Administrator danych | `T['pl']['privacy']` i `T['en']['privacy']` | W tekście jest znacznik „[uzupełnij: pełna nazwa, adres, NIP]”. |
| Miasta dwóch projektów | `PROJECTS` → `microsoft`, `szkoly` | Mają `approx: True` (pusta pinezka podpisana „Niemcy”). Podaj miasto i współrzędne, usuń `approx`. |
| Zdjęcia realizacji | `assets/realizacje/` + pole `img` | Opis w `assets/realizacje/README.md`. |

## Edycja treści

```
python3 tools/build.py
```

- `tools/content.py` — cała treść po polsku i angielsku, telefon, e-mail, projekty, oferty pracy, FAQ.
- `tools/build.py` — szablony stron. Generuje wszystkie pliki `*.html`, `en/*.html`, `404.html`, `sitemap.xml`, `robots.txt`.
- Plików HTML nie edytuj ręcznie: generator je nadpisuje.

Nowy projekt na mapie: dopisz pozycję w `PROJECTS` (klient, zakres, branża, kod kraju, szerokość i długość
geograficzna). Pinezka, karta i linia połączenia powstaną same. Nowy kraj dopisz też w `COUNTRIES`.

## Struktura

```
index.html, oferta.html, realizacje.html, o-nas.html, kariera.html, faq.html, kontakt.html
polityka-prywatnosci.html, polityka-cookies.html, 404.html
en/                       te same strony po angielsku (services, projects, about, careers, faq, contact…)
css/style.css             tokeny, komponenty, animacje, motyw ciemny
js/main.js                ekran startowy, ścieżka firmy/fachowcy, menu, animacje, formularz
js/map.js                 logika mapy realizacji
js/map-data.js            kontury krajów Europy (plik generowany)
assets/fonts/             Sofia Sans (zmienny, latin + latin-ext), licencja OFL
assets/realizacje/        miejsce na zdjęcia projektów
assets/og.png             grafika udostępniania 1200×630 (szablon: tools/og.html)
tools/                    generator, treść, projekcja mapy
sitemap.xml, robots.txt
```

## Jak to działa

- **Dwie ścieżki**: „Dla firm” i „Dla fachowców”. Wybór zapisuje się w przeglądarce; linki `?dla=fachowcy`
  (po angielsku `?for=jobs`) ustawiają go z zewnątrz. Oferta zawsze mówi do firm, Kariera do fachowców.
- **Telefon**: na telefonie link otwiera wybieranie numeru. Na komputerze pierwsze kliknięcie pokazuje numer
  i kopiuje go do schowka.
- **Formularz**: wymagane są tylko imię, telefon i zgoda. Niewysłana treść zapisuje się w przeglądarce
  i wraca po odświeżeniu. „Aplikuj” przy ofercie pracy otwiera formularz z zaznaczonym stanowiskiem.
- **Mapa**: własny rysunek SVG, bez kafli i kluczy API. Kontury pochodzą z Natural Earth (domena publiczna);
  `tools/make_map.py` uruchamia się tylko przy zmianie kadru mapy.
- **Ekran startowy** pokazuje się raz na sesję i znika sam, także gdyby skrypt się nie wczytał.
- **Bez cookies i analityki**: strona nie pobiera niczego z zewnętrznych serwerów, więc nie ma paska zgód.
  Jeśli dodasz analitykę, pasek trzeba będzie przywrócić.
- Działa bez JavaScriptu (treść jest widoczna, FAQ otwiera się natywnie) i szanuje ustawienie
  „ogranicz ruch” w systemie.

## Fonty

Sofia Sans (Lettersoup), licencja SIL Open Font License 1.1 — tekst w `assets/fonts/OFL.txt`.
