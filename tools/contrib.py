"""Desenha o quadro de contribuições do último ano em assets/contributions.svg.

Uso: GITHUB_TOKEN=... python3 tools/contrib.py <login>

Roda todo dia na Action .github/workflows/contributions.yml. As contribuições
privadas só entram na conta se "Include private contributions on my profile"
estiver ligado nas configurações do perfil.
"""

import json
import os
import sys
import urllib.request
from datetime import date
from pathlib import Path

import pixel
from gen import CREAM, GREY, RED, W, panel, svg, tag

ASSETS = Path(__file__).resolve().parent.parent / "assets"
LEVELS = ["#1c1717", "#4a1212", "#7a1616", "#b01e1e", "#ff4a3d"]
BEST = CREAM
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "rubatto-dev-profile"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if "errors" in payload:
        raise SystemExit(f"GitHub respondeu com erro: {payload['errors']}")
    cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[(d["date"], d["contributionCount"]) for d in w["contributionDays"]] for w in cal["weeks"]]
    return cal["totalContributions"], weeks


def level_of(count, cuts):
    if count == 0:
        return 0
    return 1 + sum(count > c for c in cuts)


def render(total, weeks):
    cell, step = 11, 13
    x0 = (W - len(weeks) * step) // 2
    grid_y = 96
    counts = sorted(c for w in weeks for _, c in w if c)
    cuts = [counts[len(counts) * k // 4] for k in (1, 2, 3)] if counts else [0, 0, 0]
    best_date, best = max(((d, c) for w in weeks for d, c in w), key=lambda t: t[1], default=("", 0))

    body = [tag(16, 16, "CONTRIBUTIONS")]
    total_label = f"{total:,} in the last year"
    body.append(pixel.text(total_label, W - 56 - pixel.text_width(total_label, 2), 28, 2, CREAM))  # sem tapar a chama

    last_month, last_x = None, -99
    for i, week in enumerate(weeks):
        x = x0 + i * step
        month = int(week[0][0][5:7])
        if month != last_month and x - last_x > 34:
            body.append(pixel.text(MONTHS[month - 1], x, grid_y - 22, 2, GREY))
            last_x = x
        last_month = month
        for d, c in week:
            weekday = date.fromisoformat(d).isoweekday() % 7  # domingo = 0
            color = BEST if d == best_date and best else LEVELS[level_of(c, cuts)]
            body.append(f'<rect x="{x}" y="{grid_y + weekday * step}" width="{cell}" height="{cell}" fill="{color}"/>')

    legend_y = grid_y + 7 * step + 14
    body.append(pixel.text("less", x0, legend_y, 2, GREY))
    lx = x0 + pixel.text_width("less", 2) + 10
    for color in LEVELS:
        body.append(f'<rect x="{lx}" y="{legend_y + 2}" width="{cell}" height="{cell}" fill="{color}"/>')
        lx += step
    body.append(pixel.text("more", lx + 6, legend_y, 2, GREY))
    if best:
        best_label = f"best day: {best_date}, {best} contributions"
        bx = x0 + len(weeks) * step - pixel.text_width(best_label, 2)
        body.append(f'<rect x="{bx - 20}" y="{legend_y + 2}" width="{cell}" height="{cell}" fill="{BEST}"/>')
        body.append(pixel.text(best_label, bx, legend_y, 2, RED))

    h = legend_y + 36
    alt = f"Contributions in the last year, public and private: {total}. Best day: {best_date}, {best} contributions."
    return svg(W, h, "".join(panel(h) + body), alt)


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "Rubatto-Dev"
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("Defina GITHUB_TOKEN (localmente: GITHUB_TOKEN=$(gh auth token)).")
    total, weeks = fetch(login, token)
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "contributions.svg").write_text(render(total, weeks), encoding="utf-8")
    print(f"assets/contributions.svg: {total} contribuições")


if __name__ == "__main__":
    main()
