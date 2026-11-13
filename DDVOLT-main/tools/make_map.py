#!/usr/bin/env python3
"""Generuje js/map-data.js — kontury krajów Europy jako ścieżki SVG.

Źródło: Natural Earth 1:50m (domena publiczna) w paczce npm `world-atlas`:
    npm pack world-atlas@2 && tar xzf world-atlas-*.tgz
    python3 tools/make_map.py package/countries-50m.json

Uruchamiaj tylko wtedy, gdy chcesz zmienić kadr albo dokładność mapy.
Wynik jest już w repozytorium, a zwykły build (tools/build.py) go nie potrzebuje."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import geo

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = sys.argv[1] if len(sys.argv) > 1 else 'package/countries-50m.json'

# ISO 3166-1 numeric -> alpha-2 (kraje widoczne w kadrze)
ISO = {
    '008': 'AL', '020': 'AD', '040': 'AT', '112': 'BY', '056': 'BE', '070': 'BA', '100': 'BG', '191': 'HR',
    '196': 'CY', '203': 'CZ', '208': 'DK', '233': 'EE', '246': 'FI', '250': 'FR', '276': 'DE', '300': 'GR',
    '348': 'HU', '372': 'IE', '380': 'IT', '428': 'LV', '438': 'LI', '440': 'LT', '442': 'LU', '807': 'MK',
    '470': 'MT', '498': 'MD', '492': 'MC', '499': 'ME', '528': 'NL', '578': 'NO', '616': 'PL', '620': 'PT',
    '642': 'RO', '643': 'RU', '674': 'SM', '688': 'RS', '703': 'SK', '705': 'SI', '724': 'ES', '752': 'SE',
    '756': 'CH', '792': 'TR', '804': 'UA', '826': 'GB', '336': 'VA', '012': 'DZ', '788': 'TN', '504': 'MA',
    '833': 'IM', '831': 'GG', '832': 'JE', '248': 'AX', '234': 'FO',
}
BYNAME = {'Kosovo': 'XK', 'N. Cyprus': 'CY-N'}

topo = json.load(open(SRC))
sx, sy = topo['transform']['scale']
tx, ty = topo['transform']['translate']
arcs = []
for a in topo['arcs']:
    x = y = 0
    pts = []
    for dx, dy in a:
        x += dx; y += dy
        pts.append((x * sx + tx, y * sy + ty))
    arcs.append(pts)


def ring(idx):
    out = []
    for i in idx:
        pts = arcs[i] if i >= 0 else arcs[~i][::-1]
        out.extend(pts if not out else pts[1:])
    return out


def clip(poly, inside, cross):
    """Sutherland–Hodgman dla jednej krawędzi okna."""
    out = []
    for i, cur in enumerate(poly):
        prev = poly[i - 1]
        ci, pi = inside(cur), inside(prev)
        if ci:
            if not pi:
                out.append(cross(prev, cur))
            out.append(cur)
        elif pi:
            out.append(cross(prev, cur))
    return out


def clip_rect(poly, x0, y0, x1, y1):
    def ix(p, q, x): t = (x - p[0]) / (q[0] - p[0]); return (x, p[1] + t * (q[1] - p[1]))
    def iy(p, q, y): t = (y - p[1]) / (q[1] - p[1]); return (p[0] + t * (q[0] - p[0]), y)
    for inside, cross in (
        (lambda p: p[0] >= x0, lambda p, q: ix(p, q, x0)),
        (lambda p: p[0] <= x1, lambda p, q: ix(p, q, x1)),
        (lambda p: p[1] >= y0, lambda p, q: iy(p, q, y0)),
        (lambda p: p[1] <= y1, lambda p, q: iy(p, q, y1)),
    ):
        if len(poly) < 3:
            return []
        poly = clip(poly, inside, cross)
    return poly


def simplify(pts, tol):
    """Douglas–Peucker (iteracyjnie)."""
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = pts[a]; bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        L = dx * dx + dy * dy
        best, bi = 0.0, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            if L == 0:
                d = (px - ax) ** 2 + (py - ay) ** 2
            else:
                t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L))
                d = (px - ax - t * dx) ** 2 + (py - ay - t * dy) ** 2
            if d > best:
                best, bi = d, i
        if best > tol * tol:
            keep[bi] = True
            stack.append((a, bi)); stack.append((bi, b))
    return [p for p, k in zip(pts, keep) if k]


def area(pts):
    return abs(sum(pts[i - 1][0] * p[1] - p[0] * pts[i - 1][1] for i, p in enumerate(pts))) / 2


def num(v):
    s = ('%.1f' % v).rstrip('0').rstrip('.')
    if s in ('-0', ''):
        s = '0'
    return s.replace('0.', '.', 1) if s.startswith('0.') or s.startswith('-0.') else s


def path(rings):
    out = []
    for r in rings:
        q = [(round(x, 1), round(y, 1)) for x, y in r]
        d = 'M' + num(q[0][0]) + ' ' + num(q[0][1]) + 'l'
        prev = q[0]
        seg = []
        for p in q[1:]:
            dx, dy = round(p[0] - prev[0], 1), round(p[1] - prev[1], 1)
            if dx == 0 and dy == 0:
                continue
            a, b = num(dx), num(dy)
            seg.append(a if not seg or a.startswith('-') else ' ' + a)
            seg.append(b if b.startswith('-') else ' ' + b)
            prev = p
        out.append(d + ''.join(seg) + 'z')
    return ''.join(out)


M = 24  # margines poza kadrem, żeby przycięte krawędzie nie były widoczne
countries = {}
for g in topo['objects']['countries']['geometries']:
    code = ISO.get(str(g.get('id')).zfill(3)) if g.get('id') is not None else None
    code = code or BYNAME.get(g['properties']['name'])
    if not code:
        continue
    polys = g['arcs'] if g['type'] == 'MultiPolygon' else [g['arcs']]
    rings = []
    for poly in polys:
        outer = ring(poly[0])  # wysp i dziur wewnętrznych (enklaw) nie potrzebujemy
        ll = clip_rect(outer, -32, 27, 52, 74)
        if len(ll) < 3:
            continue
        xy = [geo.project(lo, la) for lo, la in ll]
        xy = clip_rect(xy, -M, -M, geo.WIDTH + M, geo.HEIGHT + M)
        if len(xy) < 3:
            continue
        xy = simplify(xy, 0.45)
        if len(xy) >= 3 and area(xy) >= 1.6:
            rings.append(xy)
    if rings:
        countries[code] = path(rings)

js = ('/* DD Volt — kontury mapy Europy. Plik generowany: tools/make_map.py (Natural Earth 1:50m, domena publiczna). */\n'
      'window.DDV_MAP=' + json.dumps({'w': geo.WIDTH, 'h': geo.HEIGHT, 'c': countries}, separators=(',', ':'), ensure_ascii=False) + ';\n')
(ROOT / 'js' / 'map-data.js').write_text(js, encoding='utf-8')
print(len(countries), 'krajów,', len(js) // 1024, 'kB ->', 'js/map-data.js')
