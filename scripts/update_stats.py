#!/usr/bin/env python3
"""Renders assets/stats.svg from live GitHub (+ optional LeetCode) data.

Runs daily in .github/workflows/stats.yml. No third-party services are embedded in the
README, so there is nothing that can show "Something went wrong" - the card is just a
file in this repo.

    GH_TOKEN=... GH_USER=shashwat2645 python scripts/update_stats.py
    python scripts/update_stats.py --empty            # placeholder card (no network)
    python scripts/update_stats.py --demo /tmp/x.svg   # fake data, for previewing the layout only
"""
import argparse
import datetime as dt
import json
import math
import os
import pathlib
import sys
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from theme import C, INSET, chip, col, panel, rrect, svg_doc, text, tw  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, i = 800, INSET
LANG_COLORS = ["amber", "blue", "mint", "violet", "rose", "dim"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100,
                 orderBy: {field: STARGAZERS, direction: DESC}) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 6, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
    }
  }
}
"""


# ───────────────────────────────────────────────────────────── data
def http_json(url, payload, headers):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch_github(user, token):
    res = http_json("https://api.github.com/graphql",
                    {"query": QUERY, "variables": {"login": user}},
                    {"Authorization": f"bearer {token}", "Content-Type": "application/json",
                     "User-Agent": "profile-stats"})
    if "errors" in res or not res.get("data", {}).get("user"):
        raise RuntimeError(f"GitHub GraphQL error: {res.get('errors') or res}")
    return parse_github(res["data"]["user"])


def parse_github(u):
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = sorted((d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"])
    langs = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            langs[e["node"]["name"]] = langs.get(e["node"]["name"], 0) + e["size"]
    total_bytes = sum(langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
    cur, longest, run = 0, 0, 0
    for _, n in days:
        run = run + 1 if n > 0 else 0
        longest = max(longest, run)
    seq = [n for _, n in days]
    if seq and seq[-1] == 0:      # today may simply not have happened yet
        seq = seq[:-1]
    for n in reversed(seq):
        if n > 0:
            cur += 1
        else:
            break
    return dict(
        total=cal["totalContributions"], streak=cur, longest=longest,
        repos=u["repositories"]["totalCount"],
        stars=sum(r["stargazerCount"] for r in u["repositories"]["nodes"]),
        followers=u["followers"]["totalCount"],
        days=days[-26 * 7:],
        langs=[(n, b / total_bytes) for n, b in top],
    )


def fetch_leetcode(user):
    try:
        q = {"query": "query($u:String!){matchedUser(username:$u){submitStatsGlobal{acSubmissionNum{difficulty count}}}}",
             "variables": {"u": user}}
        res = http_json("https://leetcode.com/graphql", q,
                        {"Content-Type": "application/json", "Referer": "https://leetcode.com",
                         "User-Agent": "Mozilla/5.0"})
        nums = {x["difficulty"]: x["count"] for x in res["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]}
        return dict(all=nums["All"], easy=nums["Easy"], medium=nums["Medium"], hard=nums["Hard"])
    except Exception as e:  # LeetCode is optional; never fail the run over it
        print("leetcode skipped:", e)
        return None


def demo_data():
    import random
    random.seed(7)
    start = dt.date.today() - dt.timedelta(days=26 * 7 - 1)
    days = [((start + dt.timedelta(days=k)).isoformat(), max(0, int(random.gauss(2.2, 3)))) for k in range(26 * 7)]
    gh = dict(total=412, streak=9, longest=21, repos=18, stars=14, followers=23, days=days,
              langs=[("Python", .52), ("Java", .21), ("TypeScript", .13), ("SQL", .08), ("C++", .06)])
    return gh, dict(all=576, easy=190, medium=275, hard=111)


# ───────────────────────────────────────────────────────────── render
def render(gh, lc, user, updated, state="live"):
    H = 284
    b = panel(W, H, 18)
    x0 = i + 28
    note = {"live": f"-- github.com/{user} · refreshed {updated}",
            "empty": "-- awaiting first run: Actions › Update stats › Run workflow"}[state]
    b += text(x0, i + 34, note, 12, "mute", "m", 400)

    # legend (top right)
    lx = W - i - 28
    b += text(lx, i + 34, "more", 11, "mute", "m", 400, "end")
    for k in range(5):
        b += rrect(lx - 44 - (4 - k) * 16, i + 25, 12, 12, 3, fill=heat(k))
    b += text(lx - 44 - 4 * 16 - 8, i + 34, "less", 11, "mute", "m", 400, "end")

    # heatmap: 26 weeks x 7 rows, Sunday-first like GitHub
    cell, gap = 13, 3
    hy = i + 56
    grid = [[None] * 7 for _ in range(26)]
    if gh:
        counts = [n for _, n in gh["days"]]
        mx = max(counts) or 1
        first = dt.date.fromisoformat(gh["days"][0][0])
        offset = (first.weekday() + 1) % 7
        for k, (d, n) in enumerate(gh["days"]):
            col_i, row_i = divmod(k + offset, 7)
            if col_i < 26:
                grid[col_i][row_i] = 0 if n == 0 else math.ceil(4 * n / mx)
    for cx in range(26):
        for ry in range(7):
            lvl = grid[cx][ry]
            if gh and lvl is None:
                continue
            b += rrect(x0 + cx * (cell + gap), hy + ry * (cell + gap), cell, cell, 3, fill=heat(lvl or 0))
    b += text(x0, hy + 7 * (cell + gap) + 14, "last 26 weeks", 11, "mute", "m", 400)

    # stat grid
    def num(v):
        return "—" if v is None else f"{v:,}"
    items = [("contributions", num(gh and gh["total"]), "amber"),
             ("day streak", num(gh and gh["streak"]), "mint"),
             ("best streak", num(gh and gh["longest"]), "blue"),
             ("public repos", num(gh and gh["repos"]), "violet"),
             ("stars earned", num(gh and gh["stars"]), "rose"),
             ("followers", num(gh and gh["followers"]), "text")]
    sx, sy = 492, hy + 22
    for k, (label, val, color) in enumerate(items):
        cx_, cy_ = sx + (k % 3) * 102, sy + (k // 3) * 66
        b += text(cx_, cy_, val, 30, color, "s", 800)
        b += text(cx_, cy_ + 20, label, 10.5, "mute", "m", 500)

    # language bar (+ leetcode)
    by = hy + 7 * (cell + gap) + 44
    bar_w = 440 if lc else W - 2 * x0
    b += text(x0, by - 8, "TOP LANGUAGES", 10, "mute", "m", 700, ls=1.4)
    b += rrect(x0, by, bar_w, 10, 5, fill="bg3")
    cursor, legend_x = x0, x0
    langs = (gh or {}).get("langs") or []
    for k, (name, share) in enumerate(langs):
        w_ = max(6, bar_w * share)
        if cursor + w_ > x0 + bar_w:
            w_ = x0 + bar_w - cursor
        b += rrect(round(cursor, 1), by, round(max(w_ - 2, 4), 1), 10, 4, fill=LANG_COLORS[k])
        cursor += w_
        label = f"{name} {share * 100:.0f}%"
        b += f'<circle cx="{legend_x + 4}" cy="{by + 28}" r="3.5" fill="{col(LANG_COLORS[k])}"/>'
        b += text(legend_x + 13, by + 32, label, 11, "dim", "m", 500)
        legend_x += tw(label, 11, 500, True) + 30
    if not langs:
        b += text(x0, by + 32, "—", 11, "mute", "m", 500)

    if lc:
        lx0 = 500
        b += text(lx0, by - 8, "LEETCODE", 10, "mute", "m", 700, ls=1.4)
        b += text(lx0, by + 18, f"{lc['all']:,}", 24, "text", "s", 800)
        b += text(lx0 + tw(f"{lc['all']:,}", 24, 800) + 8, by + 17, "solved", 11, "mute", "m", 500)
        tot = (lc["easy"] + lc["medium"] + lc["hard"]) or 1
        cx_ = lx0 + 120
        seg_w = 280 - 120
        for k, (key, color) in enumerate([("easy", "mint"), ("medium", "amber"), ("hard", "coral")]):
            w_ = seg_w * lc[key] / tot
            b += rrect(round(cx_, 1), by + 4, round(max(w_ - 2, 3), 1), 8, 4, fill=color)
            b += text(round(cx_, 1), by + 32, f"{key[0].upper()} {lc[key]}", 11, color, "m", 600)
            cx_ += w_
    return svg_doc(W, H, "GitHub activity",
                   "Contribution heatmap, streaks, repository totals and top languages." if gh else "Stats pending first run.",
                   b)


def heat(level):
    if not level:
        return "#141C36"
    return {1: "#4B3A2B", 2: "#8A6431", 3: "#D69A42", 4: C["amber"]}[min(level, 4)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--empty", action="store_true")
    ap.add_argument("--demo", metavar="PATH")
    a = ap.parse_args()
    user = os.environ.get("GH_USER", "shashwat2645")
    out = ROOT / "assets" / "stats.svg"
    today = dt.date.today().isoformat()

    if a.empty:
        out.write_text(render(None, None, user, today, "empty"), encoding="utf-8")
        print("wrote placeholder", out)
        return
    if a.demo:
        gh, lc = demo_data()
        pathlib.Path(a.demo).write_text(render(gh, lc, user, today), encoding="utf-8")
        print("wrote demo", a.demo)
        return

    token = os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("GH_TOKEN is not set")
    gh = fetch_github(user, token)
    lc = fetch_leetcode(os.environ["LEETCODE_USER"]) if os.environ.get("LEETCODE_USER") else None
    out.write_text(render(gh, lc, user, today), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
