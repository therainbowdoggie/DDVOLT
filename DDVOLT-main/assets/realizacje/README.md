# Zdjęcia i loga realizacji

Wrzuć tu pliki (JPG, WebP albo PNG, najlepiej 1600 px szerokości, proporcje 16:10), a potem
w `tools/content.py` przy danym projekcie wpisz ścieżkę w polu `img`, na przykład:

```python
{'id': 'tesla', 'client': 'Tesla Gigafactory', ..., 'img': 'assets/realizacje/tesla.jpg',
```

Po zmianie uruchom `python3 tools/build.py`. Zdjęcie pojawi się w karcie na stronie Realizacje
i w panelu projektu przy mapie. Projekt bez zdjęcia wyświetla się jako karta z samym tekstem.

Loga klientów (Tesla, Mercedes-Benz, Ford, BMW, Audi, Microsoft) to zastrzeżone znaki towarowe.
Przed publikacją potrzebna jest zgoda właściciela marki; to samo dotyczy zdjęć z zakładów (NDA).
