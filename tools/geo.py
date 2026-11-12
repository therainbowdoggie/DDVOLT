"""Wspólna projekcja mapy (Lambert conformal conic) dla make_map.py i build.py.
Te same parametry rysują kontury krajów i ustawiają pinezki, więc zawsze do siebie pasują."""
import math

PHI1, PHI2, PHI0, LAM0 = math.radians(40), math.radians(58), math.radians(50), math.radians(10)
_n = math.log(math.cos(PHI1) / math.cos(PHI2)) / math.log(
    math.tan(math.pi / 4 + PHI2 / 2) / math.tan(math.pi / 4 + PHI1 / 2))
_F = math.cos(PHI1) * math.tan(math.pi / 4 + PHI1 / 2) ** _n / _n
_rho0 = _F / math.tan(math.pi / 4 + PHI0 / 2) ** _n


def raw(lon, lat):
    """lon/lat (stopnie) -> współrzędne projekcji bez skali (y rośnie w dół)."""
    lam, phi = math.radians(lon), math.radians(max(-85.0, min(85.0, lat)))
    rho = _F / math.tan(math.pi / 4 + phi / 2) ** _n
    th = _n * (lam - LAM0)
    return rho * math.sin(th), -(_rho0 - rho * math.cos(th))


# Kadr mapy: prostokąt w przestrzeni projekcji wyznaczony przez punkty skrajne.
_W = min(raw(-10.6, 52)[0], raw(-9.9, 37)[0])
_E = max(raw(31.5, 45)[0], raw(31.5, 59)[0])
_N = raw(10, 61.2)[1]
_S = raw(14, 35.6)[1]
WIDTH = 1000.0
SCALE = WIDTH / (_E - _W)
HEIGHT = round((_S - _N) * SCALE, 1)


def project(lon, lat):
    """lon/lat -> współrzędne w viewBox mapy (0..WIDTH, 0..HEIGHT)."""
    x, y = raw(lon, lat)
    return (x - _W) * SCALE, (y - _N) * SCALE
