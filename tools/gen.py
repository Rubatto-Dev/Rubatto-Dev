"""Gera os SVGs do README do perfil. Uso: python3 tools/gen.py

O quadro de contribuições (tools/contrib.py) e a ficha de linguagens
(tools/langs.py) ficam à parte, porque precisam da API do GitHub.
"""

from pathlib import Path

import pixel
import sprites

ASSETS = Path(__file__).resolve().parent.parent / "assets"
W = 840

# Preto e vermelho, como o Asta e a antimagia.
BG = "#0b0a0a"
BORDER = "#2a1212"
CREAM = "#efe6cf"
CREAM_DIM = "#cfc6b0"
RED = "#e0453a"
RED_DIM = "#5a1414"
GREY = "#8a857a"
TAG_BG = "#c21a1a"
CHIP_BG = "#161313"


def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" shape-rendering="crispEdges" role="img">'
        f"<title>{title}</title>{body}</svg>\n"
    )


def panel(h, w=W, ember=True):
    """Fundo escuro com borda e uma chama de antimagia no canto, igual em todas as seções."""
    parts = [
        f'<rect width="{w}" height="{h}" fill="{BG}"/>',
        f'<rect x="2" y="2" width="{w - 4}" height="{h - 4}" fill="none" stroke="{BORDER}" stroke-width="4"/>',
    ]
    if ember:
        parts.append(sprites.render(sprites.flame(), w - 34, 14, 3))
    return parts


def tag(x, y, label):
    """Título em faixa vermelha, com o trevo preto e a ponta direita inclinada."""
    tw = pixel.text_width(label, 3)
    w, h = tw + 24 + 37, 36
    return (
        f'<polygon points="{x},{y} {x + w + 14},{y} {x + w},{y + h} {x},{y + h}" fill="{TAG_BG}"/>'
        + sprites.render(sprites.mini_clover(BG), x + 10, y + 5, 3)
        + pixel.text(label, x + 47, y + 6, 3, BG)
    )


def wrap(text, max_chars):
    lines, line = [], ""
    for word in text.split():
        if line and len(line) + 1 + len(word) > max_chars:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + ([line] if line else [])


def chips(items, x, y, x_max, gap=10):
    """Etiquetas com faixa vermelha em cima. Devolve (partes, y da última linha)."""
    parts, x_start = [], x
    for item in items:
        cw = pixel.text_width(item, 2) + 20
        if x + cw > x_max:
            x, y = x_start, y + 38
        parts.append(f'<rect x="{x}" y="{y}" width="{cw}" height="30" fill="{CHIP_BG}"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="{cw}" height="3" fill="{TAG_BG}"/>')
        parts.append(pixel.text(item, x + 10, y + 10, 2, CREAM))
        x += cw + gap
    return parts, y


def banner():
    h = 220
    parts = panel(h, ember=False) + [
        sprites.render(sprites.clover(25), 30, 22, 3),
        pixel.text("GUILHERME RUBATTO", 250, 34, 4, CREAM),
        pixel.text("FULL-STACK DEVELOPER · AI", 250, 84, 3, RED),
        f'<g fill="{RED_DIM}">'
        + "".join(f'<rect x="{x}" y="118" width="18" height="3"/>' for x in range(250, 700, 30))
        + "</g>",
        pixel.text("MY MAGIC IS NOT GIVING UP.", 250, 132, 3, CREAM),
        pixel.text("ASTA · BLACK CLOVER", 250, 164, 2, GREY),
    ]
    for fx, fy in ((214, 18), (800, 180)):
        parts.append(sprites.render(sprites.flame(), fx, fy, 3))
    alt = "Guilherme Rubatto, full-stack developer focused on AI. My magic is not giving up."
    return svg(W, h, "".join(parts), alt)


ABOUT = [
    "Full-stack developer building LLM systems in production: RAG, tool-calling agents, and the part most "
    "people skip, measuring whether they actually work.",
    "Python and FastAPI on the back, React and TypeScript on the front, PostgreSQL in the middle.",
    "Software Engineering student at SENAI FATESG, graduating in December 2026, based in Goiania, Brazil.",
]


def about():
    body, y = [tag(16, 16, "ABOUT")], 72
    for paragraph in ABOUT:
        for line in wrap(paragraph, 64):
            body.append(pixel.text(line, 24, y, 2, CREAM_DIM))
            y += 20
        y += 10
    body.append(pixel.text("> Open to remote roles.", 24, y, 2, RED))
    h = y + 40
    alt = "About. " + " ".join(ABOUT) + " Open to remote roles."
    return svg(W, h, "".join(panel(h) + body), alt)


EXPERIENCE = [
    {
        "when": "FEB-OCT 2026",
        "role": "Software Developer",
        "where": "High-end real estate agency · Goiania, BR",
        "points": [
            "Shipped a WhatsApp automation system to production, with ~450 backend tests.",
            "Built an AI lead-qualification assistant (Claude Haiku + Sonnet), deployed behind a feature flag.",
            "Ran a Meta Ads campaign from scratch: 73 conversations in 5 days at R$4.27 each.",
            "Only developer in the company: requirements, design, code, tests and deploy.",
        ],
    },
]


def experience():
    body, y = [], 70
    for entry in EXPERIENCE:
        top = y
        body.append(pixel.text(entry["when"], 24, y + 4, 2, RED))
        body.append(pixel.text(entry["role"], 206, y, 3, CREAM))
        y += 32
        body.append(pixel.text(entry["where"], 206, y, 2, RED))
        y += 26
        for point in entry["points"]:
            for i, line in enumerate(wrap(point, 49)):
                body.append(pixel.text(("- " if i == 0 else "  ") + line, 206, y, 2, CREAM_DIM))
                y += 20
            y += 4
        # linha do tempo com um trevo marcando cada cargo
        body.append(f'<rect x="185" y="{top + 14}" width="3" height="{y - top - 18}" fill="{RED_DIM}"/>')
        body.append(sprites.render(sprites.mini_clover(RED), 173, top, 3))
        y += 16
    h = y + 8
    alt = "Experience. " + " ".join(
        f"{e['when']}: {e['role']}, {e['where']}. " + " ".join(e["points"]) for e in EXPERIENCE
    )
    return svg(W, h, "".join(panel(h) + [tag(16, 16, "EXPERIENCE")] + body), alt)


# Projeto em destaque. Os projetos novos de portfólio entram em PROJECTS
# como {"slug", "name", "pitch", "stack"} quando ficarem prontos.
FEATURED = {
    "name": "edital-radar",
    "repo": "github.com/Rubatto-Dev/edital-radar",
    "pitch": "Monitors Brazilian public tenders and surfaces the few a software vendor could realistically win. "
    "~1,100 tenders a day; a vendor can serve maybe 3.",
    "metrics": [
        ("US$0.0031", "per judgment: a free local filter drops 69% of the corpus before the paid model"),
        ("0.692>0.846", "recall from Haiku 4.5 to Sonnet 5, on an eval set written before the code"),
        ("CI GATE", "the build fails when measured quality drops, verified by breaking it on purpose"),
        ("LEDGER", "Langfuse cost per call reconciled exactly against an independent ledger"),
    ],
    "stack": ["Python", "FastAPI", "PostgreSQL", "pgvector", "Claude API", "Langfuse"],
}


def featured_project():
    p = FEATURED
    body = [tag(16, 16, "PROJECTS")]
    y = 74
    body.append(pixel.text(p["name"], 24, y, 3, CREAM))
    cta = "VIEW REPO >"
    body.append(pixel.text(cta, W - 24 - pixel.text_width(cta, 2), y + 4, 2, RED))
    y += 32
    body.append(pixel.text(p["repo"], 24, y, 2, GREY))
    y += 28
    for line in wrap(p["pitch"], 64):
        body.append(pixel.text(line, 24, y, 2, CREAM_DIM))
        y += 20
    y += 14
    for number, label in p["metrics"]:
        body.append(pixel.text(number, 24, y, 3, RED))
        lines = wrap(label, 44)
        for i, line in enumerate(lines):
            body.append(pixel.text(line, 264, y + 4 + 20 * i, 2, CREAM_DIM))
        y += max(30, 20 * len(lines) + 12)
    y += 6
    chip_parts, y = chips(p["stack"], 24, y, W - 24)
    body += chip_parts
    h = y + 50
    alt = (
        f"{p['name']}: {p['pitch']} "
        + " ".join(f"{n}: {l}." for n, l in p["metrics"])
        + f" Stack: {', '.join(p['stack'])}."
    )
    return svg(W, h, "".join(panel(h) + body), alt)


PROJECTS = [
    {
        "slug": "nf-extractor",
        "name": "nf-extractor",
        "pitch": "Reads Brazilian invoices from photos and PDFs with Claude and hands a person a "
        "side-by-side review. 29 of 30 invoices fully correct at US$0.0005 each on Haiku 5.5. "
        "The one miss was caught by the business rules before export.",
        "stack": ["TypeScript", "Next.js", "Claude API", "PostgreSQL", "Playwright"],
    },
]


def project_card(p):
    body, y = [], 22
    body.append(pixel.text(p["name"], 24, y, 3, CREAM))
    cta = "VIEW REPO >"
    body.append(pixel.text(cta, W - 24 - pixel.text_width(cta, 2), y + 4, 2, RED))
    y += 34
    for line in wrap(p["pitch"], 64):
        body.append(pixel.text(line, 24, y, 2, CREAM_DIM))
        y += 20
    y += 8
    chip_parts, y = chips(p["stack"], 24, y, W - 24)
    body += chip_parts
    h = y + 46
    alt = f"{p['name']}: {p['pitch']} Stack: {', '.join(p['stack'])}."
    return svg(W, h, "".join(panel(h, ember=False) + body), alt)


STACK = [
    ("AI", ["Claude API", "Tool calling", "RAG", "pgvector", "Langfuse", "Evals"]),
    ("Back", ["Python", "FastAPI", "SQLAlchemy", "Pydantic", "pytest", "Node.js"]),
    ("Front", ["TypeScript", "React", "Next.js", "Tailwind"]),
    ("Data", ["PostgreSQL", "SQL"]),
    ("Delivery", ["Docker", "GitHub Actions", "SonarQube", "n8n", "Vercel"]),
]


def stack():
    body, y = [], 72
    for label, items in STACK:
        body.append(pixel.text(label, 24, y + 8, 2, RED))
        chip_parts, y = chips(items, 150, y, W - 24)
        body += chip_parts
        y += 42
    h = y + 10
    alt = "Stack. " + ". ".join(f"{label}: {', '.join(items)}" for label, items in STACK) + "."
    return svg(W, h, "".join(panel(h) + [tag(16, 16, "STACK")] + body), alt)


def education():
    h = 132
    body = [
        tag(16, 16, "EDUCATION"),
        pixel.text("Software Engineering", 24, 70, 3, CREAM),
        pixel.text("SENAI FATESG · Goiania, BR · graduating Dec 2026", 24, 102, 2, GREY),
    ]
    alt = "Education: Software Engineering at SENAI FATESG, Goiania, Brazil, graduating December 2026."
    return svg(W, h, "".join(panel(h) + body), alt)


def contact_button(label, detail):
    """Botão de contato no estilo das faixas: trevo na ponta vermelha, texto ao lado."""
    w, h = 412, 64
    parts = panel(h, w=w, ember=False) + [
        f'<polygon points="4,4 60,4 50,{h - 4} 4,{h - 4}" fill="{TAG_BG}"/>',
        sprites.render(sprites.mini_clover(BG), 15, 18, 3),
        pixel.text(label, 72, 14, 3, CREAM),
        pixel.text(detail, 72, 42, 2, GREY),
    ]
    return svg(w, h, "".join(parts), f"{label}: {detail}")


def footer():
    """Fecho: o trevo no meio de uma linha vermelha."""
    grid = sprites.clover(15)
    size = len(grid) * 2
    h = size + 16
    cx = (W - size) // 2
    mid = 8 + size // 2
    parts = [
        f'<rect x="40" y="{mid - 1}" width="{cx - 60}" height="3" fill="{RED_DIM}"/>',
        f'<rect x="{cx + size + 20}" y="{mid - 1}" width="{W - 40 - (cx + size + 20)}" height="3" fill="{RED_DIM}"/>',
        sprites.render(grid, cx, 8, 2),
    ]
    return svg(W, h, "".join(parts), "Clover")


def main():
    ASSETS.mkdir(exist_ok=True)
    for old in ASSETS.glob("project-*.svg"):  # cards antigos saem; os atuais são gerados de novo
        old.unlink()
    files = {
        "banner.svg": banner(),
        "about.svg": about(),
        "experience.svg": experience(),
        "stack.svg": stack(),
        "education.svg": education(),
        "title-contact.svg": svg(W, 44, tag(2, 4, "CONTACT"), "Contact"),
        "contact-linkedin.svg": contact_button("LINKEDIN", "linkedin.com/in/guirubatto"),
        "contact-email.svg": contact_button("EMAIL", "rubattodev@gmail.com"),
        "footer.svg": footer(),
    }
    if FEATURED:
        files[f"project-{FEATURED['name']}.svg"] = featured_project()
    for p in PROJECTS:
        files[f"project-{p['slug']}.svg"] = project_card(p)
    for name, content in files.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
    print(f"{len(files)} SVGs gerados em assets/")


if __name__ == "__main__":
    main()
