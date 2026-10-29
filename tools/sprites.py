"""Sprites em pixel art gerados por código: o trevo de cinco folhas do Asta.

Os sprites são grades de cores (None = transparente). O que é aleatório usa
semente fixa, então o SVG sai igual a cada execução.
"""

import math

# Trevo de cinco folhas preto, com contorno vermelho em cada folha.
CLOVER = "#050505"
CLOVER_SHINE = "#1f1c1c"
CLOVER_CORE = "#7a1010"
# Antimagia.
AURA_HOT = "#ff4a3d"
AURA = "#c21a1a"
AURA_DIM = "#5a0b0b"


def _blank(w, h):
    return [[None] * w for _ in range(h)]


def _grow(pts):
    return pts | {(x + ox, y + oy) for (x, y) in pts for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1))}


def _clover_mask(cx, cy, r):
    """Pixels do trevo de cinco folhas em coração, centrado em (cx, cy).

    Cada folha são dois lóbulos lado a lado (o entalhe do coração fica na
    ponta de fora) e uma cunha que afina até o centro.
    """
    pts = set()
    d, rl = r * 0.66, r * 0.33
    leaves = [-90 + k * 72 for k in range(5)]
    for y in range(int(cy - r - 2), int(cy + r + 3)):
        for x in range(int(cx - r - 2), int(cx + r + 3)):
            px, py = x + 0.5, y + 0.5
            dist = math.hypot(px - cx, py - cy)
            ang = math.degrees(math.atan2(py - cy, px - cx))
            theta = min(leaves, key=lambda t: abs((ang - t + 180) % 360 - 180))
            delta = (ang - theta + 180) % 360 - 180
            if abs(delta) > 31 or dist > r:
                continue
            lobe = any(
                math.hypot(px - (cx + d * math.cos(math.radians(theta + s))),
                           py - (cy + d * math.sin(math.radians(theta + s)))) <= rl
                for s in (-17, 17)
            )
            if lobe or (dist < d and abs(delta) < 27 * dist / d):
                pts.add((x, y))
    return pts


def clover(r=25):
    """Trevo preto com contorno vermelho em volta de cada folha e brilho escuro por fora."""
    pad = 3
    size = 2 * (r + pad)
    grid = _blank(size, size)
    cx = cy = size / 2
    leaves = _clover_mask(cx, cy, r)
    rim = _grow(leaves) - leaves  # contorna cada folha, inclusive nas fendas
    glow = _grow(_grow(leaves | rim)) - leaves - rim
    for (x, y) in glow:
        if 0 <= x < size and 0 <= y < size:
            grid[y][x] = AURA_DIM
    for (x, y) in rim:
        grid[y][x] = AURA_HOT
    for (x, y) in leaves:
        # brilho discreto no alto de cada folha, para dar volume ao preto
        lit = (x - 1, y - 1) not in leaves or (x, y - 2) not in leaves
        grid[y][x] = CLOVER_SHINE if lit else CLOVER
    for oy in (-1, 0):  # miolo onde as folhas se encontram
        for ox in (-1, 0):
            grid[round(cy - 0.5) + oy][round(cx - 0.5) + ox] = CLOVER_CORE
    return grid


MINI_CLOVER = [
    "...###...",
    "..#####..",
    "##.###.##",
    "###.#.###",
    ".##.#.##.",
    "..##.##..",
    ".###.###.",
    ".###.###.",
    "..#...#..",
]


def mini_clover(color):
    """Trevo de cinco folhas em 9x9, para faixas de título e marcadores."""
    return [[color if ch == "#" else None for ch in row] for row in MINI_CLOVER]


FLAME = [
    "..#..",
    ".#o#.",
    "#ooo#",
    ".#o#.",
]


def flame():
    """Chama pequena da antimagia: borda escura, miolo vermelho."""
    colors = {"#": AURA_DIM, "o": AURA}
    return [[colors.get(ch) for ch in row] for row in FLAME]


def render(grid, x0, y0, scale):
    """Converte a grade em <rect>, juntando pixels vizinhos da mesma cor na linha."""
    by_color = {}
    for y, row in enumerate(grid):
        x = 0
        while x < len(row):
            color = row[x]
            if color is None:
                x += 1
                continue
            start = x
            while x < len(row) and row[x] == color:
                x += 1
            by_color.setdefault(color, []).append(
                f'<rect x="{x0 + start * scale}" y="{y0 + y * scale}" '
                f'width="{(x - start) * scale}" height="{scale}"/>'
            )
    return "".join(f'<g fill="{c}">{"".join(r)}</g>' for c, r in by_color.items())
