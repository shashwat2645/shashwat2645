"""Shared palette + tiny SVG helpers for the profile assets.

Concept: the whole profile is a database. Hero = ER diagram, headers = SQL,
stack = schema tables, certifications = a psql result set, footer = a psql session.
Palette = a SQL-editor syntax theme (amber = Java / strings, blue = SQL keywords,
mint = identifiers / status, violet = AI, coral = accent).
"""
from html import escape

INSET = 5  # transparent breathing room inside every SVG so inline images get an even gap

C = {
    "bg0": "#080C18", "bg1": "#0C1224", "bg2": "#111A33", "bg3": "#16213F",
    "line": "#222B47", "line2": "#303C66",
    "text": "#E8ECF8", "dim": "#9AA5C4", "mute": "#707CA0",
    "white": "#FFFFFF", "offwhite": "#C8D0E4",
    "amber": "#FFB454", "coral": "#FF7A59", "blue": "#6EA8FF",
    "mint": "#5EE6B8", "violet": "#B79BFF", "rose": "#FF8FA3",
}

SANS = 'Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif'
MONO = ('"JetBrains Mono","Fira Code",ui-monospace,SFMono-Regular,"SF Mono",'
        'Menlo,Consolas,"Liberation Mono",monospace')

BASE_CSS = f"""
.s{{font-family:{SANS}}}
.m{{font-family:{MONO}}}
@keyframes blink{{0%,49%{{fill-opacity:1}}50%,100%{{fill-opacity:0}}}}
@keyframes flow{{to{{stroke-dashoffset:-20}}}}
.cur{{animation:blink 1.1s steps(1) infinite}}
.flow{{stroke-dasharray:5 5;animation:flow 1.4s linear infinite}}
@media (prefers-reduced-motion:reduce){{.cur,.flow{{animation:none}}}}
"""

COMMON_DEFS = f"""
<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#0E1529"/><stop offset="1" stop-color="{C['bg0']}"/>
</linearGradient>
"""

# ---------------------------------------------------------------- text metrics
_FONTS = {}
_INTER = {
    400: "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
    500: "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
    600: "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
    700: "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    800: "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
}
_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def tw(s, size, weight=400, mono=False):
    """Text width in px. Uses Pillow + local fonts when present, else a safe estimate."""
    try:
        from PIL import ImageFont
        key = (mono, weight if not mono else 400, size)
        if key not in _FONTS:
            path = _MONO if mono else _INTER.get(weight, _INTER[400])
            _FONTS[key] = ImageFont.truetype(path, size)
        return _FONTS[key].getlength(s)
    except Exception:
        return len(s) * size * (0.60 if mono else (0.58 if weight >= 600 else 0.55))


def wrap(s, size, maxw, weight=400, mono=False):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if tw(trial, size, weight, mono) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- svg helpers
def esc(s):
    return escape(str(s), quote=True)


def col(c):
    return C.get(c, c)


def text(x, y, s, size=14, fill="text", cls="s", weight=400, anchor="start", ls=None, op=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls is not None else ""
    o = f' fill-opacity="{op}"' if op is not None else ""
    return (f'<text class="{cls}" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'fill="{col(fill)}"{a}{l}{o}>{esc(s)}</text>')


def sql(x, y, parts, size=14, weight=500, anchor="start", cursor=False):
    """parts = [(string, colour), ...] -> one monospace <text> with coloured tspans."""
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    inner = "".join(f'<tspan fill="{col(c)}">{esc(t)}</tspan>' for t, c in parts)
    if cursor:
        inner += f'<tspan class="cur" fill="{C["amber"]}">▌</tspan>'
    return (f'<text class="m" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}"{a} '
            f'style="white-space:pre">{inner}</text>')


def rrect(x, y, w, h, r=10, fill="none", stroke=None, sw=1, op=None, extra=""):
    st = f' stroke="{col(stroke)}" stroke-width="{sw}"' if stroke else ""
    o = f' fill-opacity="{op}"' if op is not None else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
            f'fill="{col(fill) if not fill.startswith("url") else fill}"{o}{st}{extra}/>')


def chip(x, y, s, color="dim", h=24, size=11, pad=9, fill="bg3", stroke="line2", mono=True, weight=500, dot=None):
    """Returns (svg, width). (x, y) is the chip's top-left."""
    dot_w = 14 if dot else 0
    w = round(tw(s, size, weight, mono) + 2 * pad + dot_w)
    out = rrect(x, y, w, h, h / 2, fill=fill, stroke=stroke)
    tx = x + pad + dot_w
    if dot:
        out += f'<circle cx="{x + pad + 3}" cy="{y + h / 2}" r="3" fill="{col(dot)}"/>'
    out += text(tx, y + h / 2 + size * 0.36, s, size, color, "m" if mono else "s", weight)
    return out, w


def svg_doc(w, h, title, desc, body, defs="", css=""):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t d">\n<title id="t">{esc(title)}</title>'
            f'<desc id="d">{esc(desc)}</desc>\n<defs>{COMMON_DEFS}{defs}</defs>\n'
            f'<style>{BASE_CSS}{css}</style>\n{body}\n</svg>\n')


def panel(w, h, r=16, glow=None, dash=None):
    """Standard card background inside the INSET, with optional accent glow in the top-left."""
    i = INSET
    out = rrect(i, i, w - 2 * i, h - 2 * i, r, fill="url(#panel)", stroke="line2" if dash else "line",
                extra=f' stroke-dasharray="{dash}"' if dash else "")
    if glow:
        out += (f'<clipPath id="pc"><rect x="{i}" y="{i}" width="{w - 2 * i}" height="{h - 2 * i}" rx="{r}"/></clipPath>'
                f'<g clip-path="url(#pc)"><circle cx="{i}" cy="{i}" r="150" fill="url(#glow)"/></g>')
    return out


def glow_def(color, op=0.16):
    return (f'<radialGradient id="glow"><stop offset="0" stop-color="{col(color)}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{col(color)}" stop-opacity="0"/></radialGradient>')
