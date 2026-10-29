"""Desenha a ficha de linguagens por bytes de código em assets/languages.svg.

Uso: python3 tools/langs.py <login>   (precisa do gh logado)

Soma os bytes de cada linguagem em todos os repositórios próprios, públicos e
privados, sem forks. Roda à mão, não na Action: o token da Action não enxerga
os repositórios privados.
"""

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pixel
from gen import CREAM, CREAM_DIM, GREY, W, panel, svg, tag

ASSETS = Path(__file__).resolve().parent.parent / "assets"
COLORS = ["#ff4a3d", "#c21a1a", "#efe6cf", "#7a1616", "#8a857a", "#4a1212"]
OTHER = "#2a2626"


def gh(*args):
    return json.loads(subprocess.run(["gh", "api", *args], check=True, capture_output=True, text=True).stdout)


def measure(login):
    repos = gh("--paginate", "user/repos?affiliation=owner&per_page=100")
    totals, counted = {}, 0
    for repo in repos:
        if repo["fork"] or repo["owner"]["login"] != login:
            continue
        counted += 1
        for lang, size in gh(f"repos/{login}/{repo['name']}/languages").items():
            totals[lang] = totals.get(lang, 0) + size
    return totals, counted


def render(totals, counted, when):
    total = sum(totals.values()) or 1
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    top, rest = ranked[:6], ranked[6:]
    rows = [(lang, size / total * 100, COLORS[i]) for i, (lang, size) in enumerate(top)]
    if rest:
        rows.append(("other", sum(s for _, s in rest) / total * 100, OTHER))

    body = [tag(16, 16, "LANGUAGES")]
    note = f"{counted} repos · {when}"
    body.append(pixel.text(note, W - 56 - pixel.text_width(note, 2), 28, 2, GREY))  # sem tapar a chama
    # barra empilhada com a fatia de cada linguagem
    x, bar_w, y = 24, W - 48, 76
    for i, (_, pct, color) in enumerate(rows):
        seg = round(bar_w * pct / 100) if i < len(rows) - 1 else 24 + bar_w - x
        body.append(f'<rect x="{x}" y="{y}" width="{max(seg, 0)}" height="18" fill="{color}"/>')
        x += seg
    # legenda em duas colunas
    y = 114
    for i, (lang, pct, color) in enumerate(rows):
        col, row = i % 2, i // 2
        lx, ly = 24 + col * 400, y + row * 28
        body.append(f'<rect x="{lx}" y="{ly + 1}" width="14" height="14" fill="{color}"/>')
        body.append(pixel.text(lang, lx + 24, ly, 2, CREAM))
        label = f"{pct:.1f}%"
        body.append(pixel.text(label, lx + 360 - pixel.text_width(label, 2), ly, 2, CREAM_DIM))
    h = y + ((len(rows) + 1) // 2) * 28 + 20
    alt = f"Languages on GitHub by bytes of code across {counted} repositories, measured on {when}: " + ", ".join(
        f"{lang} {pct:.1f}%" for lang, pct, _ in rows
    ) + "."
    return svg(W, h, "".join(panel(h) + body), alt)


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "Rubatto-Dev"
    totals, counted = measure(login)
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "languages.svg").write_text(render(totals, counted, date.today().isoformat()), encoding="utf-8")
    print(f"assets/languages.svg: {counted} repositórios")


if __name__ == "__main__":
    main()
