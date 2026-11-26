#!/usr/bin/env python3
"""Builds every SVG in ../assets and the README.md.

    python scripts/build_assets.py

Edit CFG below (text, projects, stack, links), run the script, commit. That's it.
The only thing NOT built here is assets/stats.svg - that one is refreshed daily by
.github/workflows/stats.yml via scripts/update_stats.py.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from theme import *  # noqa: F401,F403
from theme import C, INSET, col, esc, rrect, sql, svg_doc, text, tw, wrap, chip, panel, glow_def

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
USER = "shashwat2645"
W = 800                      # one grid for everything: full = 800, halves = 398, thirds = 264
HALF, THIRD, PILL = 398, 264, 158   # PILL: 4 across on desktop, 2 across on a phone
i = INSET


def repo_search(q):
    return f"https://github.com/{USER}?tab=repositories&q={q}"


# ═════════════════════════════════════════════════════════════════ CONFIG
CFG = dict(
    first="Shashwat", last="Singh",
    eyebrow="SELECT * FROM developer WHERE focus = 'java';",
    tagline="Backend engineer · Java & databases",
    subline="Schemas, query plans and APIs that stay up.",
    chips=[("Placed · Newgen & LTM", "mint", "mint"),
           ("B.Tech CSE (AI & ML) · 2027", "dim", None),
           ("Kanpur, India", "dim", None)],
    links=[  # key, label, glyph, accent, url
        ("linkedin", "LinkedIn", "in", "blue", "https://www.linkedin.com/in/singhshashwat26"),
        ("email", "Email", "@", "amber", "mailto:shashwats2604@gmail.com"),
        ("leetcode", "LeetCode", "LC", "coral", "https://leetcode.com/u/shashwat_singh_2604/"),
        ("github", "GitHub", "gh", "mint", f"https://github.com/{USER}"),
    ],
    about=[  # (text, style) - style None = body text, otherwise a palette colour (shown bold)
        ("Final-year CS (AI & ML) student at ", None), ("PSIT Kanpur", "white"),
        (". I started out building ", None), ("Python / FastAPI", "mint"),
        (" backends and I'm now going deeper on ", None), ("Java", "amber"), (" and ", None),
        ("databases", "blue"), (", the unglamorous parts that keep systems reliable.", None),
    ],
    tiles=[  # key, label, title, sub-line, accent
        ("focus", "FOCUS", "Java", "The language and its backend ecosystem.", "amber"),
        ("depth", "DEPTH", "SQL + DBMS", "Relational databases and how queries run.", "blue"),
        ("base", "BASE", "Python + FastAPI", "REST APIs, SQLAlchemy and LLM APIs.", "mint"),
    ],
    stack=[  # (table, accent, [(skill, level)])   level: "core" | "working" | "basic"
        ("languages", "amber", [("Java", "working"), ("Python", "core"), ("SQL", "core")]),
        ("databases", "blue", [("PostgreSQL", "working"), ("MySQL", "core")]),
        ("backend", "mint", [("FastAPI", "core"), ("SQLAlchemy 2.0", "core")]),
        ("ai_ml", "violet", [("pandas", "basic"), ("NumPy", "basic"), ("LLM APIs", "basic")]),
        ("frontend", "rose", [("HTML", "basic"), ("CSS", "basic"), ("JavaScript", "basic"),
                              ("Bootstrap", "basic")]),
        ("tooling", "dim", [("Git", "core"), ("GitHub", "core"), ("Postman", "basic")]),
    ],
    projects=[  # url=None -> no arrow, not clickable.  planned=True -> dashed outline
        dict(key="marketplace", kind="major project · in progress", accent="violet",
             title="Decentralized AI Marketplace",
             desc=("Federated learning on a blockchain: hospitals and banks train locally and share only "
                   "model weights; smart contracts reward contributors."),
             chips=["PyTorch", "Solidity", "Ethereum", "React"],
             url="https://github.com/VisheshDubey26/AI-Cyber-Threat-Intelligence"),
        dict(key="lexfile", kind="planned", accent="mint", planned=True,
             title="LexFile",
             desc=("Indian law assistant with sourced statute passages, document facts and "
                   "follow-up questions."),
             chips=["Python", "FastAPI", "PostgreSQL"],
             url=None),  # repo not created yet: set the URL here once it exists
        dict(key="banking", kind="in progress", accent="blue",
             title="Banking Transaction System",
             desc=("A banking backend for account balances, secure fund transfers and reliable "
                   "transaction records."),
             chips=["Java", "Spring Boot", "Maven", "PostgreSQL"],
             url=None),
        dict(key="guardian", kind="hackathon MVP", accent="amber",
             title="Deadline Guardian AI",
             desc=("Turns deadlines into plans: priority analysis, an execution planner, risk prediction "
                   "and a daily coach, powered by Gemini on a FastAPI + React stack."),
             chips=["FastAPI", "React", "Gemini", "Alembic"],
             url=repo_search("deadline")),  # swap for the exact repo URL if you like
    ],
    achievements=[  # file stem, label, title, sub-line, chip, accent
        ("ach-placement", "PLACEMENT", "Newgen · LTM", "Placed at both as a final-year student.",
         "Class of 2027", "mint"),
        ("hack-vibe2ship", "HACKATHON", "Vibe2Ship Hackathon", "Coding Ninjas × Google for Developers",
         "AI productivity · backend", "amber"),
        ("hack-isro", "HACKATHON", "Bhartiya Antariksha Hackathon 2026",
         "Indian Space Research Organisation (ISRO)", "Space tech & innovation", "violet"),
    ],
    certs=[  # credential, issuer, year, accent
        ("Agentic AI Foundations Associate", "Oracle", "2026", "coral"),
        ("AI Fluency", "Anthropic", "2026", "amber"),
        ("Generative AI Foundations", "AWS Academy", "2026", "amber"),
        ("Data Science with Python", "Wipro TalentNext", "2026", "blue"),
        ("AI Foundations Associate", "Oracle", "2025", "coral"),
    ],
    closing_email="shashwats2604@gmail.com",
)


def save(name, content):
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / name).write_text(content, encoding="utf-8")
    print("  wrote assets/" + name)


def fit(s, maxw, size, weight=700, lo=14):
    while size > lo and tw(s, size, weight) > maxw:
        size -= 1
    return size


# ═════════════════════════════════════════════════════════════════ HERO
def er_table(x, y, w, title, rows, accent, hdr=26, rh=21):
    h = hdr + rh * len(rows)
    s = rrect(x, y, w, h, 9, fill="#0F1832", stroke="line2")
    s += (f'<path d="M{x},{y + hdr} V{y + 9} A9,9 0 0 1 {x + 9},{y} H{x + w - 9} A9,9 0 0 1 {x + w},{y + 9} '
          f'V{y + hdr} Z" fill="{col(accent)}" fill-opacity=".16"/>')
    s += f'<line x1="{x}" y1="{y + hdr}" x2="{x + w}" y2="{y + hdr}" stroke="{C["line2"]}"/>'
    s += text(x + 12, y + hdr / 2 + 4.5, title, 12.5, accent, "m", 700)
    mids = []
    for k, (name, kind) in enumerate(rows):
        mid = y + hdr + k * rh + rh / 2
        mids.append(mid)
        if kind in ("PK", "FK"):
            bc = "amber" if kind == "PK" else "blue"
            s += text(x + 12, mid + 4, name, 12, "text", "m", 500)
            s += rrect(x + w - 35, mid - 7, 25, 14, 4, fill=bc, op=0.16, stroke=bc, sw=0.8)
            s += text(x + w - 22.5, mid + 3.5, kind, 8.5, bc, "m", 700, "middle")
        elif kind == "type":
            s += text(x + 12, mid + 4, name, 12, "text", "m", 500)
            s += text(x + w - 12, mid + 4, "text", 11, "mute", "m", 400, "end")
        else:
            s += text(x + 12, mid + 4, name, 12, "amber", "m", 500)
    return s, h, mids


def build_hero():
    H = 384
    pw, ph = W - 2 * i, H - 2 * i
    defs = f"""
<linearGradient id="hbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0E162C"/><stop offset="1" stop-color="{C['bg0']}"/></linearGradient>
<radialGradient id="gA" cx=".08" cy=".02" r=".7"><stop offset="0" stop-color="{C['amber']}" stop-opacity=".22"/><stop offset="1" stop-color="{C['amber']}" stop-opacity="0"/></radialGradient>
<radialGradient id="gB" cx=".98" cy="1" r=".8"><stop offset="0" stop-color="{C['blue']}" stop-opacity=".24"/><stop offset="1" stop-color="{C['blue']}" stop-opacity="0"/></radialGradient>
<linearGradient id="nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFD590"/><stop offset="1" stop-color="{C['coral']}"/></linearGradient>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#1D294B"/></pattern>
<clipPath id="hc"><rect x="{i}" y="{i}" width="{pw}" height="{ph}" rx="22"/></clipPath>"""
    b = f'<g clip-path="url(#hc)"><rect x="{i}" y="{i}" width="{pw}" height="{ph}" fill="url(#hbg)"/>'
    b += f'<rect x="{i}" y="{i}" width="{pw}" height="{ph}" fill="url(#dots)" opacity=".85"/>'
    b += f'<rect x="{i}" y="{i}" width="{pw}" height="{ph}" fill="url(#gA)"/>'
    b += f'<rect x="{i}" y="{i}" width="{pw}" height="{ph}" fill="url(#gB)"/></g>'
    b += rrect(i, i, pw, ph, 22, stroke="line")

    x0 = 44
    # eyebrow: a SQL line with a blinking cursor
    b += sql(x0, 50, [("SELECT", "blue"), (" * ", "amber"), ("FROM", "blue"), (" developer ", "mint"),
                      ("WHERE", "blue"), (" focus = ", "text"), ("'java'", "amber"), (";", "dim")],
             13, cursor=True)
    # name
    b += (f'<text class="s" x="{x0 - 2}" y="132" font-size="66" font-weight="800" letter-spacing="-2" '
          f'fill="{C["text"]}">{esc(CFG["first"])}</text>')
    b += (f'<text class="s" x="{x0 - 2}" y="198" font-size="66" font-weight="800" letter-spacing="-2" '
          f'fill="url(#nm)">{esc(CFG["last"])}</text>')
    tsz = fit(CFG["tagline"], 372, 21, 600)
    b += text(x0, 242, CFG["tagline"], tsz, "text", "s", 600)
    b += text(x0, 268, CFG["subline"], 15, "dim", "s", 400)

    # ER diagram on the right
    dx, dy, dw = 446, 92, 142
    tx, tw_ = 640, 124
    dev, dev_h, dm = er_table(dx, dy, dw, "developer",
                              [("id", "PK"), ("name", "type"), ("focus", "FK"), ("db", "FK"), ("ai", "FK")], "amber")
    tj, _, jm = er_table(tx, 58, tw_, "java", [("id", "PK"), ("'deep dive'", "val")], "amber")
    tp, _, pm = er_table(tx, 144, tw_, "postgres", [("id", "PK"), ("'going deeper'", "val")], "blue")
    ty, _, ym = er_table(tx, 230, tw_, "python", [("id", "PK"), ("'home turf'", "val")], "mint")
    lines = ""
    for ri, tgt, colr, delay in [(2, jm[0], "amber", 0), (3, pm[0], "blue", -0.9), (4, ym[0], "mint", -1.8)]:
        x1, y1, x2, y2 = dx + dw, dm[ri], tx, tgt
        d = f"M{x1},{y1} C{x1 + 34},{y1} {x2 - 34},{y2} {x2},{y2}"
        lines += (f'<path d="{d}" fill="none" stroke="{col(colr)}" stroke-opacity=".75" stroke-width="1.5" class="flow"/>'
                  f'<circle cx="{x1}" cy="{y1}" r="3.2" fill="{C["bg1"]}" stroke="{col(colr)}" stroke-width="1.5"/>'
                  f'<circle cx="{x2}" cy="{y2}" r="3.2" fill="{col(colr)}"/>'
                  f'<circle r="3.4" fill="{col(colr)}"><animateMotion dur="2.8s" begin="{delay}s" '
                  f'repeatCount="indefinite" path="{d}"/></circle>')
    b += lines + dev + tj + tp + ty
    b += text(dx, dy + dev_h + 24, "-- 3 FKs \u00b7 0 orphans", 11, "mute", "m", 400)

    # chips
    cx, cy = x0, 306
    for label, color, dot in CFG["chips"]:
        stroke = "line2" if not dot else color
        svg, cw = chip(cx, cy, label, color, h=30, size=12.5, pad=13, fill="bg2", stroke=stroke, mono=False,
                       weight=600, dot=dot)
        b += svg
        cx += cw + 10
    return svg_doc(W, H, f"{CFG['first']} {CFG['last']} — backend engineer",
                   "Hero banner drawn as an ER diagram: a developer table with foreign keys to Java, PostgreSQL and Python.",
                   b, defs)


# ═════════════════════════════════════════════════════════════════ SECTION HEADERS
HEADERS = {
    "about": ([("SELECT", "blue"), (" * ", "amber"), ("FROM", "blue"), (" about", "mint"), (";", "dim")],
              "-- who I am", "amber"),
    "stack": ([("SELECT", "blue"), (" * ", "amber"), ("FROM", "blue"), (" stack", "mint"), (";", "dim")],
              "-- what I build with", "blue"),
    "projects": ([("SELECT", "blue"), (" * ", "amber"), ("FROM", "blue"), (" projects", "mint"), (";", "dim")],
                 "-- selected work", "violet"),
    "proof": ([("SELECT", "blue"), (" * ", "amber"), ("FROM", "blue"), (" achievements", "mint"), (";", "dim")],
              "-- placement, hackathons & certs", "amber"),
    "activity": ([("EXPLAIN ANALYZE", "blue"), (" activity", "mint"), (";", "dim")],
                 "-- regenerated daily", "mint"),
    "contact": ([("INSERT INTO", "blue"), (" connections ", "mint"), ("VALUES", "blue"), (" ('you')", "amber"),
                 (";", "dim")], "-- say hi", "coral"),
}


def build_header(key):
    parts, comment, accent = HEADERS[key]
    H = 62
    b = panel(W, H, 14)
    b += rrect(i + 16, 19, 4, 24, 2, fill=accent)
    b += sql(i + 36, 39.5, parts, 21, 700)
    b += text(W - i - 22, 36.5, comment, 12.5, "mute", "m", 400, "end")
    return svg_doc(W, H, key, f"Section header: {key}", b)


# ═════════════════════════════════════════════════════════════════ ABOUT TEXT
def build_about():
    size, lh = 17, 29
    x0 = i + 38
    maxw = W - 2 * i - 38 - 30
    # split the styled segments into words, keeping per-run styles (punctuation stays attached)
    words, cur = [], []
    for t_, style in CFG["about"]:
        for ch in t_:
            if ch == " ":
                if cur:
                    words.append(cur)
                    cur = []
            elif cur and cur[-1][1] == style:
                cur[-1] = (cur[-1][0] + ch, style)
            else:
                cur.append((ch, style))
    if cur:
        words.append(cur)
    wt = lambda st: 700 if st else 500
    word_w = lambda w_: sum(tw(t_, size, wt(st)) for t_, st in w_)
    space = tw(" ", size, 500)
    lines, line, lw = [], [], 0
    for w_ in words:
        ww = word_w(w_)
        if line and lw + space + ww > maxw:
            lines.append(line)
            line, lw = [w_], ww
        else:
            lw += (space if line else 0) + ww
            line.append(w_)
    lines.append(line)

    y0 = i + 46
    H = y0 + (len(lines) - 1) * lh + 28 + i
    b = panel(W, H, 16, glow=True)
    b += rrect(i + 16, i + 22, 4, H - 2 * i - 44, 2, fill="amber")
    for n, ln in enumerate(lines):
        y = y0 + n * lh
        inner = ""
        for k, w_ in enumerate(ln):
            if k:
                inner += " "
            for t_, st in w_:
                fill = col(st) if st else C["offwhite"]
                inner += f'<tspan fill="{fill}" font-weight="{wt(st)}">{esc(t_)}</tspan>'
        b += f'<text class="s" x="{x0}" y="{y}" font-size="{size}" style="white-space:pre">{inner}</text>'
    plain = "".join(t_ for t_, _ in CFG["about"])
    return svg_doc(W, H, "About", plain, b, glow_def("amber", 0.10)), plain


# ═════════════════════════════════════════════════════════════════ ABOUT TILES
def build_tile(label, title, sub, accent):
    H = 148
    b = panel(THIRD, H, 16, glow=True)
    b += text(i + 20, i + 34, label, 11, accent, "m", 700, ls=1.6)
    size = fit(title, THIRD - 2 * i - 40, 25, 800)
    b += text(i + 20, i + 72, title, size, "text", "s", 800)
    for k, l in enumerate(wrap(sub, 13.5, THIRD - 2 * i - 40)[:3]):
        b += text(i + 20, i + 98 + k * 19, l, 13.5, "dim")
    return svg_doc(THIRD, H, title, sub, b, glow_def(accent, 0.2))


# ═════════════════════════════════════════════════════════════════ STACK TABLES
def build_stack(name, accent, rows, nrows=None):
    nrows = nrows or len(rows)          # tables in the same grid row share one height
    hdr, ch, rh = 42, 24, 30
    H = i * 2 + hdr + ch + rh * nrows + 12
    b = panel(THIRD, H, 16)
    b += rrect(i + 16, i + 15, 10, 10, 3, fill=accent)
    b += text(i + 34, i + 25, name, 14, accent, "m", 700)
    b += text(THIRD - i - 16, i + 25, f"{len(rows)} rows", 10.5, "mute", "m", 400, "end")
    y = i + hdr
    b += f'<line x1="{i}" y1="{y}" x2="{THIRD - i}" y2="{y}" stroke="{C["line"]}"/>'
    b += text(i + 16, y + 16, "SKILL", 9.5, "mute", "m", 700, ls=1.2)
    b += text(THIRD - i - 16, y + 16, "LEVEL", 9.5, "mute", "m", 700, "end", ls=1.2)
    y += ch
    for k in range(nrows):
        ry = y + k * rh
        b += f'<line x1="{i + 12}" y1="{ry}" x2="{THIRD - i - 12}" y2="{ry}" stroke="{C["line"]}" stroke-opacity="{".7" if k < len(rows) else ".35"}"/>'
        if k >= len(rows):
            continue                    # empty row: just the table rule, so short tables still read as tables
        skill, level = rows[k]
        core = level == "core"
        mid = ry + rh / 2
        if core:
            b += f'<circle cx="{i + 21}" cy="{mid}" r="4" fill="{C["amber"]}"/>'
        else:
            b += f'<circle cx="{i + 21}" cy="{mid}" r="3.6" fill="none" stroke="{C["mute"]}" stroke-width="1.4"/>'
        b += text(i + 36, mid + 5, skill, 14.5, "text" if core else "dim", "s", 600 if core else 500)
        if core:
            b += rrect(THIRD - i - 16 - 40, mid - 9, 40, 18, 9, fill="amber", op=0.14, stroke="amber", sw=0.8)
            b += text(THIRD - i - 16 - 20, mid + 3.8, "core", 10.5, "amber", "m", 700, "middle")
        else:
            b += text(THIRD - i - 16, mid + 4, level, 11, "mute", "m", 500, "end")
    return svg_doc(THIRD, H, f"{name} table", ", ".join(f"{s_} ({l_})" for s_, l_ in rows), b)


# ═════════════════════════════════════════════════════════════════ PROJECT CARDS
def build_project(idx, p):
    H = 226
    acc = p["accent"]
    if len(wrap(p["desc"], 13.5, HALF - 2 * i - 44)) > 3:
        print("  ! WARNING: project '%s' description wraps to more than 3 lines" % p["title"])
    b = panel(HALF, H, 18, glow=True, dash="6 5" if p.get("planned") else None)
    b += f'<line x1="{i + 18}" y1="{i + 0.5}" x2="{HALF - i - 18}" y2="{i + 0.5}" stroke="{col(acc)}" stroke-opacity=".7" stroke-width="1"/>'
    b += text(i + 22, i + 36, f"{idx:02d}", 12, "mute", "m", 700)
    b += text(i + 46, i + 36, p["kind"].upper(), 11, acc, "m", 700, ls=1.4)
    # link arrow square - only when the project has somewhere to link to
    if p.get("url"):
        cx, cy = HALF - i - 36, i + 30
        b += rrect(cx - 14, cy - 14, 28, 28, 8, fill="bg3", stroke="line2")
        b += (f'<path d="M{cx - 4.5},{cy + 4.5} L{cx + 4.5},{cy - 4.5} M{cx - 3.5},{cy - 4.5} H{cx + 4.5} V{cy + 3.5}" '
              f'fill="none" stroke="{col(acc)}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>')
    size = fit(p["title"], HALF - 2 * i - 44 - 40, 22, 800, lo=17)
    b += text(i + 22, i + 74, p["title"], size, "text", "s", 800)
    for k, l in enumerate(wrap(p["desc"], 13.5, HALF - 2 * i - 44)[:4]):
        b += text(i + 22, i + 100 + k * 20, l, 13.5, "dim")
    x = i + 22
    y = H - i - 22 - 24
    for c_ in p["chips"]:
        s, w_ = chip(x, y, c_, "text", h=24, size=11, pad=10, fill="bg3", stroke="line2")
        b += s
        x += w_ + 7
    return svg_doc(HALF, H, p["title"], p["desc"], b, glow_def(acc, 0.17))


# ═════════════════════════════════════════════════════════════════ ACHIEVEMENT TILES
def build_ach(stem, label, title, sub, chip_text, accent):
    H = 186
    b = panel(THIRD, H, 16, glow=True)
    b += text(i + 20, i + 32, label, 10.5, accent, "m", 700, ls=1.6)
    y = i + 62
    for l in wrap(title, 17, THIRD - 2 * i - 40, 800)[:2]:
        b += text(i + 20, y, l, 17, "text", "s", 800)
        y += 21
    y += 2
    for l in wrap(sub, 12.5, THIRD - 2 * i - 40)[:2]:
        b += text(i + 20, y, l, 12.5, "dim")
        y += 17
    s_, _ = chip(i + 20, H - i - 18 - 22, chip_text, "text", h=22, size=10.5, pad=9, fill="bg3", stroke="line2")
    b += s_
    return svg_doc(THIRD, H, title, f"{sub} \u2014 {chip_text}", b, glow_def(accent, 0.17))


# ═════════════════════════════════════════════════════════════════ CERTS (psql result set)
def build_certs():
    rows = CFG["certs"]
    top, ch, rh = i + 14, 30, 42
    H = top + ch + rh * len(rows) + 46
    b = panel(W, H, 16)
    c1, c2, c3 = i + 30, i + 450, W - i - 30
    y = top + 14
    b += text(c1 + 18, y + 4, "CREDENTIAL", 10.5, "mute", "m", 700, ls=1.4)
    b += text(c2, y + 4, "ISSUER", 10.5, "mute", "m", 700, ls=1.4)
    b += text(c3, y + 4, "YEAR", 10.5, "mute", "m", 700, "end", ls=1.4)
    y += 14
    b += f'<line x1="{i + 14}" y1="{y}" x2="{W - i - 14}" y2="{y}" stroke="{C["line2"]}"/>'
    for k, (cred, issuer, year, acc) in enumerate(rows):
        ry = y + k * rh
        mid = ry + rh / 2
        if k:
            b += f'<line x1="{i + 14}" y1="{ry}" x2="{W - i - 14}" y2="{ry}" stroke="{C["line"]}"/>'
        b += f'<circle cx="{c1 + 4}" cy="{mid}" r="4.5" fill="{col(acc)}"/>'
        b += text(c1 + 18, mid + 5.5, cred, 15.5, "white", "s", 700)
        b += text(c2, mid + 5.5, issuer, 15, "offwhite", "s", 500)
        b += text(c3, mid + 4.5, year or "\u2013", 13, "dim", "m", 500, "end")
    y += rh * len(rows)
    b += f'<line x1="{i + 14}" y1="{y}" x2="{W - i - 14}" y2="{y}" stroke="{C["line2"]}"/>'
    b += text(c1, y + 24, f"({len(rows)} rows)", 12, "mute", "m", 400)
    b += text(c3, y + 24, "ORDER BY year DESC", 11, "mute", "m", 400, "end")
    return svg_doc(W, H, "Certifications", "; ".join(f"{c_} ({i_})" for c_, i_, _, _ in rows), b)


# ═════════════════════════════════════════════════════════════════ LINK PILLS
def build_pill(label, glyph, accent):
    H = 52
    b = rrect(i, i, PILL - 2 * i, H - 2 * i, 14, fill="url(#panel)", stroke="line")
    b += rrect(i + 9, i + 9, 28, 28, 9, fill=accent, op=0.16, stroke=accent, sw=0.9)
    b += text(i + 23, i + 28, glyph, 12, accent, "m", 800, "middle")
    b += text(i + 48, i + 28.5, label, 14.5, "text", "s", 700)
    ax = PILL - i - 20
    b += (f'<path d="M{ax - 4},{i + 28} L{ax + 4},{i + 20} M{ax - 3},{i + 20} H{ax + 4} V{i + 27}" fill="none" '
          f'stroke="{C["mute"]}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    return svg_doc(PILL, H, label, f"Link to {label}", b)


# ═════════════════════════════════════════════════════════════════ FOOTER (psql session)
def build_footer():
    P = "shashwat=# "
    Pc = "shashwat-# "
    lines = [
        ("p", P, [("BEGIN", "blue"), (";", "dim")]),
        ("o", "BEGIN", None),
        ("p", P, [("INSERT INTO", "blue"), (" collaborations ", "mint"), ("(who, what)", "text")]),
        ("p", Pc, [("VALUES", "blue"), (" (", "text"), ("'you'", "amber"), (", ", "text"),
                   ("'something worth building'", "amber"), (");", "text")]),
        ("o", "INSERT 0 1", None),
        ("p", P, [("COMMIT", "blue"), (";", "dim")]),
        ("o", "COMMIT", None),
        ("c", P, []),
    ]
    lh, top = 25, i + 86
    H = top + lh * len(lines) + 18
    dur = 13.0
    css = ""
    b = panel(W, H, 18)
    b += text(i + 28, i + 36, "-- thanks for stopping by", 12.5, "mute", "m", 400)
    # little traffic-light-free title: just a hairline
    b += f'<line x1="{i + 14}" y1="{i + 52}" x2="{W - i - 14}" y2="{i + 52}" stroke="{C["line"]}"/>'
    for k, (kind, pr, parts) in enumerate(lines):
        y = top + k * lh
        start = 4 + k * 9.5            # % of the loop at which this line appears
        css += (f"@keyframes l{k}{{0%,{start:.1f}%{{opacity:0}}{start + 1.2:.1f}%,90%{{opacity:1}}96%,100%{{opacity:0}}}}"
                f".l{k}{{animation:l{k} {dur}s infinite}}")
        if kind == "o":
            g = text(i + 28, y, pr, 14.5, "dim", "m", 500)
        elif kind == "c":
            g = sql(i + 28, y, [(pr, "mint")], 14.5, 500, cursor=True)
        else:
            g = sql(i + 28, y, [(pr, "mint")] + parts, 14.5, 500)
        b += f'<g class="l{k} ln">{g}</g>'
    css += "@media (prefers-reduced-motion:reduce){.ln{animation:none!important;opacity:1}}"
    return svg_doc(W, H, "psql session", "An animated psql session that inserts you into collaborations.", b, "", css)


# ═════════════════════════════════════════════════════════════════ README
def build_readme():
    img = lambda f, w, alt: f'<img src="assets/{f}" width="{w}" alt="{alt}">'
    pills = "\n".join("  <a href=\"%s\">%s</a>" % (u, img("link-%s.svg" % k, PILL, l))
                      for k, l, _, _, u in CFG["links"])
    tiles = "\n".join("  " + img("tile-%s.svg" % k, THIRD, t) for k, _, t, _, _ in CFG["tiles"])
    stack = "\n".join("  " + img("stack-%s.svg" % n, THIRD, n) for n, _, _ in CFG["stack"])
    def proj(p):
        im = img("project-%s.svg" % p["key"], HALF, p["title"])
        return '  <a href="%s">%s</a>' % (p["url"], im) if p.get("url") else "  " + im
    projs = "\n".join(proj(p) for p in CFG["projects"])
    hacks = "\n".join("  " + img("%s.svg" % a[0], THIRD, a[2]) for a in CFG["achievements"])
    hdr = lambda k, alt: '<p align="center">%s</p>' % img("h-%s.svg" % k, W, alt)
    about_alt = build_about()[1].replace('"', "&quot;")
    hero_alt = "%s %s: backend engineer, Java and databases" % (CFG["first"], CFG["last"])
    return f"""<!-- Generated by scripts/build_assets.py - edit CFG there, not this file. -->
<p align="center">
  {img("hero.svg", W, hero_alt)}
</p>

<p align="center">
{pills}
</p>

{hdr("about", "SELECT * FROM about")}

<p align="center">
  {img("about-text.svg", W, about_alt)}
</p>

<p align="center">
{tiles}
</p>

{hdr("stack", "SELECT * FROM stack")}

<p align="center">
{stack}
</p>

<p align="center"><sub><b>●</b> core, what I'd happily be interviewed on &nbsp;·&nbsp; <b>○</b> working knowledge</sub></p>

{hdr("projects", "SELECT * FROM projects")}

<p align="center">
{projs}
</p>

{hdr("proof", "SELECT * FROM achievements")}

<p align="center">
{hacks}
</p>

<p align="center">
  {img("certs.svg", W, "Certifications: Oracle, Anthropic, AWS Academy, Wipro TalentNext")}
</p>

{hdr("activity", "EXPLAIN ANALYZE activity")}

<p align="center">
  {img("stats.svg", W, "GitHub activity: contributions, streak, repositories and top languages")}
</p>

{hdr("contact", "INSERT INTO connections VALUES ('you')")}

<p align="center">
  {img("footer.svg", W, "psql session: INSERT INTO collaborations VALUES ('you', 'something worth building'); COMMIT;")}
</p>

<p align="center"><sub>Prefer plain text? <a href="mailto:{CFG["closing_email"]}">{CFG["closing_email"]}</a></sub></p>
"""


def main():
    print("building assets...")
    save("hero.svg", build_hero())
    for k in HEADERS:
        save(f"h-{k}.svg", build_header(k))
    save("about-text.svg", build_about()[0])
    for k, label, title, sub, acc in CFG["tiles"]:
        save(f"tile-{k}.svg", build_tile(label, title, sub, acc))
    stack = CFG["stack"]
    for g in range(0, len(stack), 3):            # tables that sit in the same row share one height
        group = stack[g:g + 3]
        nrows = max(len(r) for _, _, r in group)
        for name, acc, rows in group:
            save(f"stack-{name}.svg", build_stack(name, acc, rows, nrows))
    for n, p in enumerate(CFG["projects"], 1):
        save(f"project-{p['key']}.svg", build_project(n, p))
    for stem, *rest in CFG["achievements"]:
        save(f"{stem}.svg", build_ach(stem, *rest))
    save("certs.svg", build_certs())
    for k, label, glyph, acc, _ in CFG["links"]:
        save(f"link-{k}.svg", build_pill(label, glyph, acc))
    save("footer.svg", build_footer())
    (ROOT / "README.md").write_text(build_readme(), encoding="utf-8")
    print("  wrote README.md")


if __name__ == "__main__":
    main()
