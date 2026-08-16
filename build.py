#!/usr/bin/env python3
"""Build the Capsules static archive from content/lessons/*.json."""

from __future__ import annotations

import json
import re
import shutil
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content" / "lessons"
ASSETS = ROOT / "assets"
OUT = ROOT / "docs"
SITE_URL = "https://huirumay28.github.io/capsules"
BASE = "/capsules"
TAIPEI = ZoneInfo("Asia/Taipei")

SUBJECTS = [
    {"id": "feminism", "label": "Feminism", "weekday": "Monday"},
    {"id": "music", "label": "Music", "weekday": "Tuesday"},
    {"id": "film", "label": "Film", "weekday": "Wednesday"},
    {"id": "literature", "label": "Literature", "weekday": "Thursday"},
    {"id": "history", "label": "History", "weekday": "Friday"},
    {"id": "business", "label": "Business", "weekday": "Saturday"},
    {"id": "psych", "label": "Psych / soc", "weekday": "Sunday"},
]
SUBJECT_BY_ID = {s["id"]: s for s in SUBJECTS}
SUBJECT_ALIASES = {"rock": "music"}
SUBJECT_ORDER = {s["id"]: i for i, s in enumerate(SUBJECTS)}

FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,560;0,9..144,680;1,9..144,440"
    "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,560;1,8..60,400"
    "&family=Source+Sans+3:ital,wght@0,400;0,600;1,400"
    "&display=swap"
)


def esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def normalize_subject(raw: str) -> str:
    sid = SUBJECT_ALIASES.get(raw, raw)
    if sid not in SUBJECT_BY_ID:
        raise SystemExit(f"unknown subject {raw!r}")
    return sid


def taipei_today() -> date:
    return datetime.now(TAIPEI).date()


def week_bounds(today: date | None = None) -> tuple[date, date]:
    today = today or taipei_today()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def in_this_week(iso: str, today: date | None = None) -> bool:
    d = datetime.strptime(iso, "%Y-%m-%d").date()
    start, end = week_bounds(today)
    return start <= d <= end


def load_lessons() -> list[dict]:
    lessons = []
    for path in sorted(CONTENT.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_file"] = path.name
        data["subject"] = normalize_subject(data.get("subject", ""))
        data.setdefault("related", [])
        lessons.append(data)
    lessons.sort(key=lambda x: (x["date"], SUBJECT_ORDER[x["subject"]], x["slug"]), reverse=True)
    return lessons


def asset(prefix: str, rel: str) -> str:
    return f"{prefix}assets/{rel}"


def page_shell(
    *,
    title: str,
    description: str,
    prefix: str,
    canonical: str,
    body: str,
    extra_head: str = "",
    extra_js: str = "",
    subject: str = "",
) -> str:
    body_attr = f' data-subject="{esc(subject)}"' if subject else ' data-subject="home"'
    return f"""<!DOCTYPE html>
<html lang="en"{body_attr}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="icon" href="{asset(prefix, 'mark.svg')}" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="{asset(prefix, 'css/site.css')}">
  {extra_head}
</head>
<body{body_attr}>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap">
      <a class="wordmark" href="{prefix or "./"}">
        <span class="mark" aria-hidden="true"></span>
        Capsules
      </a>
      <a class="nav-meta" href="{prefix or "./"}">Archive</a>
    </div>
  </header>
  <main id="main">
    {body}
  </main>
  <footer class="site-footer">
    <div class="wrap">
      <p>Huiru Huang · daily era lessons, 8:45 Taipei</p>
      <p><a href="https://github.com/huirumay28/capsules">Source</a></p>
    </div>
  </footer>
  {extra_js}
</body>
</html>
"""


def format_date(iso: str) -> str:
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%-d %B %Y")


def collect_search_text(lesson: dict) -> str:
    parts = [
        lesson.get("title", ""),
        lesson.get("dek", ""),
        lesson.get("era", ""),
        lesson.get("honesty", ""),
        SUBJECT_BY_ID[lesson["subject"]]["label"],
        lesson["subject"],
    ]
    for item in lesson.get("timeline", []):
        parts.extend([item.get("year", ""), item.get("label", ""), item.get("detail", "")])
    fun = lesson.get("fun_fact") or {}
    parts.extend([fun.get("title", ""), fun.get("text", "")])
    for entry in lesson.get("glossary", []):
        parts.append(entry.get("term", ""))
        parts.extend(entry.get("aliases") or [])
        parts.append(entry.get("explain", ""))
    for section in lesson.get("sections", []):
        parts.extend([section.get("kicker", ""), section.get("title", "")])
        for block in section.get("blocks", []):
            kind = block.get("type")
            if kind in {"p", "question"}:
                parts.append(block.get("text", ""))
            elif kind == "list":
                parts.extend(block.get("items") or [])
            elif kind == "figure":
                parts.extend([block.get("caption", ""), block.get("alt", "")])
            elif kind == "people":
                for person in block.get("people", []):
                    parts.extend([
                        person.get("name", ""),
                        person.get("dates", ""),
                        person.get("text", ""),
                        person.get("caption", ""),
                    ])
    for item in lesson.get("watch", []) + lesson.get("listen", []):
        parts.extend([item.get("title", ""), item.get("note", "")])
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def card_html(lesson: dict, prefix: str = "") -> str:
    subject = SUBJECT_BY_ID[lesson["subject"]]
    thumb = lesson.get("thumb") or {}
    if thumb.get("src"):
        thumb_html = (
            f'<img class="card-thumb" src="{asset(prefix, thumb["src"])}" '
            f'alt="{esc(thumb.get("alt", ""))}">'
        )
    else:
        thumb_html = '<div class="card-thumb" aria-hidden="true"></div>'
    href = f"{prefix}lessons/{esc(lesson['slug'])}/"
    return f"""
            <a class="card" href="{href}"
               data-subject="{esc(lesson["subject"])}"
               data-search="{esc(collect_search_text(lesson).lower())}">
              {thumb_html}
              <div class="card-body">
                <p class="card-meta">{esc(subject["label"])} · {esc(format_date(lesson["date"]))}</p>
                <h2>{esc(lesson["title"])}</h2>
                <p>{esc(lesson["dek"])}</p>
              </div>
            </a>
            """


def render_home(lessons: list[dict]) -> str:
    today = taipei_today()
    this_week = [L for L in lessons if in_this_week(L["date"], today)]
    previous = [L for L in lessons if not in_this_week(L["date"], today)]
    this_week.sort(key=lambda x: (SUBJECT_ORDER[x["subject"]], x["slug"]))
    previous.sort(key=lambda x: (x["date"], SUBJECT_ORDER[x["subject"]]), reverse=True)

    filters = ['<button class="filter" type="button" data-filter="all" aria-pressed="true">All</button>']
    for subject in SUBJECTS:
        filters.append(
            f'<button class="filter" type="button" data-filter="{esc(subject["id"])}" '
            f'aria-pressed="false">{esc(subject["label"])}</button>'
        )

    days = "".join(
        f'<li data-subject="{esc(s["id"])}"><strong>{esc(s["weekday"])}</strong> {esc(s["label"])}</li>'
        for s in SUBJECTS
    )

    this_cards = "".join(card_html(L) for L in this_week) or ""
    prev_cards = "".join(card_html(L) for L in previous) or ""
    prev_empty_hidden = "hidden" if previous else ""
    this_empty_hidden = "hidden" if this_week else ""

    body = f"""
    <section class="hero-home wrap">
      <p class="kicker">A daily archive · 8:45 Taipei</p>
      <h1>Capsules</h1>
      <p class="lede">One era at a time. Long enough to sit with, short enough for a quiet hour. Huiru Huang’s daily lessons — look out from the place and year the capsule stands, and see what else was happening then.</p>
      <ul class="weekdays">{days}</ul>
    </section>
    <section class="wrap" aria-labelledby="archive-heading">
      <h2 id="archive-heading" class="kicker">The archive</h2>
      <div class="archive-tools">
        <label class="search-label" for="archive-search">Search the archive</label>
        <input id="archive-search" class="search" type="search" placeholder="Search titles, dek, subject, era, body…" autocomplete="off">
      </div>
      <div class="filters" role="group" aria-label="Filter by subject">{''.join(filters)}</div>
      <div class="week-block" data-week="this">
        <h2 class="block-title">This week</h2>
        <p class="block-note">Monday–Sunday, Asia/Taipei. The current week’s capsules.</p>
        <div class="archive">{this_cards}</div>
        <p class="empty" data-empty {this_empty_hidden}>No capsules this week match.</p>
      </div>
      <div class="week-block" data-week="previous">
        <h2 class="block-title">Previous lessons</h2>
        <p class="block-note">Older than this week, still filterable by subject.</p>
        <div class="archive">{prev_cards}</div>
        <p class="empty" data-empty {prev_empty_hidden}>No earlier capsules yet. This is the first week of the archive.</p>
      </div>
    </section>
    <script src="{asset("", "js/archive.js")}"></script>
    """
    return page_shell(
        title="Capsules — daily era lessons",
        description="Huiru Huang’s daily lesson archive: feminism, music, film, literature, history, business, and psych/soc.",
        prefix="",
        canonical=f"{SITE_URL}/",
        body=body,
    )


def figure_html(
    prefix: str,
    src: str,
    alt: str,
    caption: str,
    credit: str,
    credit_url: str,
    cls: str,
    fit: str = "",
) -> str:
    credit_link = (
        f'<a href="{esc(credit_url)}">{esc(credit)}</a>' if credit_url else esc(credit)
    )
    fit_cls = f" fit-{fit}" if fit else ""
    return f"""
    <figure class="{cls}{fit_cls}">
      <img src="{asset(prefix, src)}" alt="{esc(alt)}">
      <figcaption class="caption">
        {esc(caption)}
        <span class="credit">{credit_link}</span>
      </figcaption>
    </figure>
    """


def is_word_char(ch: str) -> bool:
    return ch.isalnum() or ch in {"'", "’", "-"} or ("\u4e00" <= ch <= "\u9fff")


def mark_text(text: str, glossary: list[dict], lesson_links: list[tuple[str, str]]) -> str:
    variants: list[tuple[str, str, str]] = []
    for entry in glossary or []:
        canon = entry["term"]
        for name in [canon, *(entry.get("aliases") or [])]:
            name = str(name).strip()
            if name:
                variants.append((name, "term", canon))
    for name, href in lesson_links:
        name = str(name).strip()
        if name:
            variants.append((name, "link", href))
    variants.sort(key=lambda x: len(x[0]), reverse=True)

    escaped = esc(text)
    occupied = [False] * len(escaped)
    replacements: list[tuple[int, int, str]] = []
    lower = escaped.lower()

    for name, kind, payload in variants:
        needle = esc(name)
        if not needle:
            continue
        start = 0
        nlow = needle.lower()
        while True:
            idx = lower.find(nlow, start)
            if idx < 0:
                break
            end = idx + len(needle)
            start = idx + 1
            if any(occupied[idx:end]):
                continue
            before = escaped[idx - 1] if idx > 0 else ""
            after = escaped[end] if end < len(escaped) else ""
            cjk = any("\u4e00" <= ch <= "\u9fff" for ch in name)
            if not cjk:
                if before and is_word_char(before):
                    continue
                if after and is_word_char(after):
                    continue
            for i in range(idx, end):
                occupied[i] = True
            visible = escaped[idx:end]
            if kind == "term":
                html = f'<button type="button" class="term" data-term="{esc(payload)}">{visible}</button>'
            else:
                html = f'<a class="inline-lesson" href="{esc(payload)}">{visible}</a>'
            replacements.append((idx, end, html))

    replacements.sort(key=lambda x: x[0])
    out = []
    cursor = 0
    for start, end, html in replacements:
        out.append(escaped[cursor:start])
        out.append(html)
        cursor = end
    out.append(escaped[cursor:])
    return "".join(out)


def lesson_link_pairs(current: dict, all_lessons: list[dict], prefix: str) -> list[tuple[str, str]]:
    pairs = []
    for other in all_lessons:
        if other["slug"] == current["slug"]:
            continue
        href = f"{prefix}../{esc(other['slug'])}/"
        pairs.append((other["title"], href))
        pairs.append((other["slug"], href))
        short = other["title"].split(":")[0].strip()
        if short and short != other["title"] and len(short) >= 8:
            pairs.append((short, href))
    return pairs


def render_blocks(
    prefix: str,
    blocks: list[dict],
    glossary: list[dict],
    lesson_links: list[tuple[str, str]],
) -> str:
    parts = []
    for block in blocks:
        kind = block["type"]
        if kind == "p":
            parts.append(f"<p>{mark_text(block['text'], glossary, lesson_links)}</p>")
        elif kind == "question":
            parts.append(f'<div class="question"><p>{esc(block["text"])}</p></div>')
        elif kind == "list":
            items = "".join(
                f"<li>{mark_text(item, glossary, lesson_links)}</li>" for item in block["items"]
            )
            parts.append(f'<ul class="prose-list">{items}</ul>')
        elif kind == "figure":
            parts.append(
                figure_html(
                    prefix,
                    block["src"],
                    block.get("alt", ""),
                    block.get("caption", ""),
                    block.get("credit", ""),
                    block.get("credit_url", ""),
                    "figure-study",
                    block.get("fit", ""),
                )
            )
        elif kind == "people":
            cards = []
            for person in block["people"]:
                img = ""
                if person.get("image"):
                    img = (
                        f'<img src="{asset(prefix, person["image"])}" alt="{esc(person.get("alt", ""))}">'
                    )
                cap = ""
                if person.get("caption") or person.get("credit"):
                    credit = person.get("credit", "")
                    credit_url = person.get("credit_url", "")
                    credit_html = (
                        f'<a href="{esc(credit_url)}">{esc(credit)}</a>' if credit_url else esc(credit)
                    )
                    cap = (
                        f'<p class="caption">{esc(person.get("caption", ""))}'
                        f'<span class="credit">{credit_html}</span></p>'
                    )
                cards.append(
                    f"""
                    <article class="person">
                      {img}
                      <div class="person-body">
                        <h3>{esc(person["name"])}</h3>
                        <p class="dates">{esc(person.get("dates", ""))}</p>
                        <p>{mark_text(person.get("text", ""), glossary, lesson_links)}</p>
                        {cap}
                      </div>
                    </article>
                    """
                )
            parts.append(f'<div class="people">{"".join(cards)}</div>')
        else:
            raise SystemExit(f"Unknown block type: {kind}")
    return "\n".join(parts)


def render_link_list(heading: str, heading_id: str, items: list[dict], css: str) -> str:
    if not items:
        return ""
    lis = []
    for item in items:
        lis.append(
            f"""<li>
              <a href="{esc(item["url"])}">{esc(item["title"])}</a>
              <span class="note">{esc(item.get("note", ""))}</span>
            </li>"""
        )
    return f"""
        <aside class="{css}" aria-labelledby="{heading_id}">
          <h2 id="{heading_id}">{esc(heading)}</h2>
          <ol>{''.join(lis)}</ol>
        </aside>
        """


def render_fun_fact(prefix: str, fun: dict | None) -> str:
    if not fun:
        return ""
    image_html = ""
    image = fun.get("image") or {}
    if image.get("src"):
        image_html = figure_html(
            prefix,
            image["src"],
            image.get("alt", ""),
            image.get("caption", ""),
            image.get("credit", ""),
            image.get("credit_url", ""),
            "figure-study",
            image.get("fit", ""),
        )
    return f"""
        <section class="fun-fact" id="fun-fact">
          <p class="kicker">Fun fact</p>
          <h2>{esc(fun.get("title", "A true aside"))}</h2>
          {image_html}
          <p>{esc(fun.get("text", ""))}</p>
        </section>
        """


def render_related(current: dict, all_lessons: list[dict], prefix: str) -> str:
    by_slug = {L["slug"]: L for L in all_lessons}
    referenced = []
    for slug in current.get("related") or []:
        other = by_slug.get(slug)
        if other:
            referenced.append(other)
    same = [
        L for L in all_lessons
        if L["subject"] == current["subject"] and L["slug"] != current["slug"]
    ]
    same.sort(key=lambda x: (x["date"], x["slug"]), reverse=True)
    if not referenced and not same:
        return ""

    def lis(items: list[dict]) -> str:
        out = []
        for L in items:
            sub = SUBJECT_BY_ID[L["subject"]]["label"]
            out.append(
                f'<li><a href="{prefix}../{esc(L["slug"])}/">{esc(L["title"])}</a>'
                f'<span class="note">{esc(sub)} · {esc(L.get("era", ""))}</span></li>'
            )
        return "".join(out)

    chunks = []
    if referenced:
        chunks.append(
            f'<div class="related-col"><h2>Referenced</h2><ol>{lis(referenced)}</ol></div>'
        )
    if same:
        chunks.append(
            f'<div class="related-col"><h2>In this subject</h2><ol>{lis(same)}</ol></div>'
        )
    return f'<aside class="related" aria-label="Related capsules">{"".join(chunks)}</aside>'


def render_lesson(lesson: dict, all_lessons: list[dict]) -> str:
    prefix = "../../"
    subject = SUBJECT_BY_ID[lesson["subject"]]
    glossary = lesson.get("glossary") or []
    links = lesson_link_pairs(lesson, all_lessons, prefix)
    hero = lesson.get("hero") or {}
    hero_html = ""
    if hero.get("src"):
        hero_html = figure_html(
            prefix,
            hero["src"],
            hero.get("alt", ""),
            hero.get("caption", ""),
            hero.get("credit", ""),
            hero.get("credit_url", ""),
            "hero-figure",
        )

    toc_items = [
        f'<li><a href="#{esc(section["id"])}">{esc(section["kicker"])}</a></li>'
        for section in lesson["sections"]
    ]
    if lesson.get("fun_fact"):
        toc_items.append('<li><a href="#fun-fact">Fun fact</a></li>')
    toc = "".join(toc_items)

    n = max(len(lesson.get("timeline") or []), 1)
    timeline_items = "".join(
        f"""<li>
          <span class="year">{esc(item["year"])}</span>
          <span class="label">{esc(item["label"])}</span>
          <span class="detail">{esc(item["detail"])}</span>
        </li>"""
        for item in lesson.get("timeline", [])
    )
    timeline_html = ""
    if timeline_items:
        timeline_html = f"""
        <div class="timeline wrap" aria-label="Era timeline" style="--cols:{n}">
          <ol>{timeline_items}</ol>
        </div>
        """

    sections = []
    for section in lesson["sections"]:
        sections.append(
            f"""
            <section class="section" id="{esc(section["id"])}">
              <p class="kicker">{esc(section["kicker"])}</p>
              <h2>{esc(section["title"])}</h2>
              {render_blocks(prefix, section["blocks"], glossary, links)}
            </section>
            """
        )

    watch_html = render_link_list("Watch", "watch-heading", lesson.get("watch") or [], "watch")
    listen_html = render_link_list("Listen", "listen-heading", lesson.get("listen") or [], "watch listen")
    fun_html = render_fun_fact(prefix, lesson.get("fun_fact"))
    related_html = render_related(lesson, all_lessons, prefix)

    glossary_json = json.dumps(
        [
            {
                "term": entry["term"],
                "aliases": entry.get("aliases") or [],
                "explain": entry["explain"],
            }
            for entry in glossary
        ],
        ensure_ascii=False,
    )

    panel = """
    <aside class="explain" id="explain" hidden>
      <div class="explain-inner">
        <p class="explain-hint">Select any words, or tap a dotted term.</p>
        <button type="button" class="explain-close" data-explain-close>Close</button>
        <p class="explain-term" data-explain-term></p>
        <p class="explain-body" data-explain-body></p>
      </div>
    </aside>
    """

    body = f"""
    <article class="lesson" data-has-glossary="true">
      <div class="subject-bar" aria-hidden="true"></div>
      <header class="lesson-hero wrap">
        <p class="kicker">{esc(subject["weekday"])} · {esc(subject["label"])}</p>
        <h1>{esc(lesson["title"])}</h1>
        <p class="lesson-dek">{esc(lesson["dek"])}</p>
        <p class="lesson-meta">
          <span>{esc(format_date(lesson["date"]))}</span>
          <span>{esc(lesson.get("era", ""))}</span>
          <span>About {esc(str(lesson.get("reading_minutes", 12)))} minutes</span>
        </p>
      </header>
      <div class="wrap">{hero_html}</div>
      <div class="wrap">
        <p class="honesty">{esc(lesson.get("honesty", ""))}</p>
        <p class="glossary-hint">Select any words, or tap a dotted term.</p>
        <nav aria-label="In this capsule">
          <ol class="toc">{toc}</ol>
        </nav>
      </div>
      {timeline_html}
      <div class="wrap prose-wrap">
        {''.join(sections)}
        {fun_html}
        {watch_html}
        {listen_html}
        {related_html}
      </div>
      {panel}
    </article>
    <script type="application/json" id="glossary-data">{glossary_json}</script>
    """
    return page_shell(
        title=f"{lesson['title']} — Capsules",
        description=lesson["dek"],
        prefix=prefix,
        canonical=f"{SITE_URL}/lessons/{lesson['slug']}/",
        body=body,
        extra_js=f'<script src="{asset(prefix, "js/glossary.js")}"></script>',
        subject=lesson["subject"],
    )


def render_404() -> str:
    body = """
    <section class="hero-home wrap">
      <p class="kicker">Missing</p>
      <h1>This capsule is not here.</h1>
      <p class="lede"><a href="./">Return to the archive.</a></p>
    </section>
    """
    return page_shell(
        title="Not found — Capsules",
        description="This page is not in the Capsules archive.",
        prefix="",
        canonical=f"{SITE_URL}/404.html",
        body=body,
    )


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build() -> None:
    if not CONTENT.exists():
        raise SystemExit(f"Missing content directory: {CONTENT}")
    lessons = load_lessons()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    shutil.copytree(ASSETS, OUT / "assets")
    write(OUT / "index.html", render_home(lessons))
    write(OUT / "404.html", render_404())
    write(OUT / ".nojekyll", "")

    for lesson in lessons:
        write(OUT / "lessons" / lesson["slug"] / "index.html", render_lesson(lesson, lessons))

    index = [
        {
            "slug": lesson["slug"],
            "date": lesson["date"],
            "subject": lesson["subject"],
            "title": lesson["title"],
            "dek": lesson["dek"],
            "era": lesson.get("era", ""),
            "url": f"{BASE}/lessons/{lesson['slug']}/",
            "text": collect_search_text(lesson),
        }
        for lesson in lessons
    ]
    write(OUT / "lessons.json", json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    print(f"Built {len(lessons)} lesson(s) into {OUT}")


if __name__ == "__main__":
    build()
