# DD Volt — strona firmowa

Statyczna strona (HTML + CSS + JS, bez frameworków) gotowa pod GitHub Pages.

## Publikacja na GitHub Pages

1. Utwórz repozytorium na GitHubie (np. `ddvolt-strona`).
2. Wgraj całą zawartość tego katalogu do gałęzi `main`.
3. W repo: **Settings → Pages → Build and deployment → Source: Deploy from a branch**, gałąź `main`, katalog `/ (root)`. Zapisz.
4. Po 1–2 minutach strona działa pod `https://<login>.github.io/<nazwa-repo>/`.
5. Własna domena: **Settings → Pages → Custom domain**, wpisz np. `ddvolt.pl` i ustaw rekordy DNS według instrukcji GitHuba.

Plik `.nojekyll` wyłącza przetwarzanie Jekyll (nie jest potrzebne).

## Struktura

```
index.html                strona główna (dwie ścieżki: firmy / fachowcy)
oferta.html               oferta + branże + proces
realizacje.html           mapa interaktywna + case study
o-nas.html                historia, zasady, liczby
kariera.html              oferty pracy + FAQ dla fachowców
faq.html                  FAQ (zestaw zależny od ścieżki)
kontakt.html              formularz + dane kontaktowe
polityka-prywatnosci.html
polityka-cookies.html
css/style.css             tokeny i komponenty (design system v1)
js/main.js                przełącznik ścieżki, animacje, liczniki, FAQ, formularz, motyw
js/map.js                 mapa realizacji (Leaflet + kafle CARTO) i DANE PROJEKTÓW
assets/favicon.svg
tools/build.py            generator stron — edytuj treść tutaj i uruchom `python3 tools/build.py`
```

## Co trzeba uzupełnić przed publikacją

- **Telefon i e-mail** — w `tools/build.py` (stałe `PHONE`, `PHONE_HREF`, `EMAIL`), potem `python3 tools/build.py`. Albo podmień ręcznie w plikach HTML (`+48 000 000 000`, `kontakt@ddvolt.pl`).
- **Formularz** — załóż darmowe konto na [formspree.io](https://formspree.io), skopiuj ID formularza i wpisz w `FORM_ACTION` (zamiast `TWOJ_ID`). Bez tego formularz pokaże komunikat, że nie jest podpięty.
- **Zdjęcia** — wszystkie kafle „Zdjęcie z realizacji" to zaślepki. Wrzuć zdjęcia do `assets/` i dodaj `<img>` w karcie (`.project .photo`) albo w hero (`.hero-art`).
- **Dane na mapie** — `js/map.js`, tablica `PROJECTS`. Pozycje z dopiskiem `note` mają lokalizację do potwierdzenia (Tesla, Microsoft, szkoły). Współrzędne: miasto.
- **Dane administratora** w polityce prywatności (nazwa, adres, NIP).
- **Nazwa** — „DD Volt" jest robocza. Zmiana: szukaj `DD Volt` w `tools/build.py` i przebuduj.

## Edycja treści

Najwygodniej przez `tools/build.py` — nagłówek i stopka są w jednym miejscu, treść sekcji w zmiennych (`SERVICES`, `PROJECTS`, `JOBS`, `FAQ_FIRMY`, `FAQ_FACHOWCY`, `STEPS`). Po zmianie:

```
python3 tools/build.py
```

Pliki HTML można też edytować bezpośrednio; wtedy nie uruchamiaj generatora, bo nadpisze zmiany.

## Fonty

Bricolage Grotesque (nagłówki), Instrument Sans (tekst), IBM Plex Mono (etykiety) — ładowane z Google Fonts. Jeśli chcesz hostować lokalnie, pobierz pliki WOFF2 i podmień `<link>` w sekcji `<head>` oraz `--font-*` w `css/style.css`.

## Mapa

Leaflet 1.9.4 (unpkg) + kafle CARTO Dark Matter (bez klucza API, darmowe do użytku niekomercyjnego i małego ruchu). Przy dużym ruchu rozważ własny klucz MapTiler/Stadia i podmień adres kafli w `js/map.js`.
