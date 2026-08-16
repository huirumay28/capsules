#!/usr/bin/env python3
"""Build the Capsules static archive from content/lessons/*.json."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content" / "lessons"
ASSETS = ROOT / "assets"
OUT = ROOT / "docs"
SITE_URL = "https://huirumay28.github.io/capsules"
BASE = "/capsules"

SUBJECTS = [
    {"id": "feminism", "label": "Feminism", "weekday": "Monday"},
    {"id": "rock", "label": "Rock and roll", "weekday": "Tuesday"},
    {"id": "film", "label": "Film", "weekday": "Wednesday"},
    {"id": "literature", "label": "Literature", "weekday": "Thursday"},
    {"id": "history", "label": "History", "weekday": "Friday"},
]
SUBJECT_BY_ID = {s["id"]: s for s in SUBJECTS}

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


def load_lessons() -> list[dict]:
    lessons = []
    for path in sorted(CONTENT.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data["_file"] = path.name
        lessons.append(data)
    lessons.sort(key=lambda x: x["date"], reverse=True)
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
) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
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
<body>
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
      <p>Huiru Huang · weekday era lessons</p>
      <p><a href="https://github.com/huirumay28/capsules">Source</a></p>
    </div>
  </footer>
</body>
</html>
"""


def format_date(iso: str) -> str:
    return datetime.strptime(iso, "%Y-%m-%d").strftime("%-d %B %Y")


def render_home(lessons: list[dict]) -> str:
    cards = []
    for lesson in lessons:
        subject = SUBJECT_BY_ID[lesson["subject"]]
        thumb = lesson.get("thumb") or {}
        thumb_html = ""
        if thumb.get("src"):
            thumb_html = (
                f'<img class="card-thumb" src="{asset("", thumb["src"])}" '
                f'alt="{esc(thumb.get("alt", ""))}">'
            )
        else:
            thumb_html = '<div class="card-thumb" aria-hidden="true"></div>'
        cards.append(
            f"""
            <a class="card" href="lessons/{esc(lesson["slug"])}/" data-subject="{esc(lesson["subject"])}">
              {thumb_html}
              <div class="card-body">
                <p class="card-meta">{esc(subject["label"])} · {esc(format_date(lesson["date"]))}</p>
                <h2>{esc(lesson["title"])}</h2>
                <p>{esc(lesson["dek"])}</p>
              </div>
            </a>
            """
        )

    filters = ['<button class="filter" type="button" data-filter="all" aria-pressed="true">All</button>']
    for subject in SUBJECTS:
        filters.append(
            f'<button class="filter" type="button" data-filter="{esc(subject["id"])}" '
            f'aria-pressed="false">{esc(subject["label"])}</button>'
        )

    days = "".join(
        f"<li><strong>{esc(s['weekday'])}</strong> {esc(s['label'])}</li>" for s in SUBJECTS
    )

    body = f"""
    <section class="hero-home wrap">
      <p class="kicker">A weekday archive</p>
      <h1>Capsules</h1>
      <p class="lede">One era at a time. Long enough to sit with, short enough for a quiet hour. Huiru Huang’s lessons in feminism, rock and roll, film, literature, and history.</p>
      <ul class="weekdays">{days}</ul>
    </section>
    <section class="wrap" aria-labelledby="archive-heading">
      <h2 id="archive-heading" class="kicker">The archive</h2>
      <div class="filters" role="group" aria-label="Filter by subject">{''.join(filters)}</div>
      <div class="archive">
        {''.join(cards)}
      </div>
      <p class="empty" data-empty hidden>No capsules in this subject yet.</p>
    </section>
    <script src="{asset("", "js/archive.js")}"></script>
    """
    return page_shell(
        title="Capsules — weekday era lessons",
        description="Huiru Huang’s weekday lesson archive: feminism, rock and roll, film, literature, and history.",
        prefix="",
        canonical=f"{SITE_URL}/",
        body=body,
    )


def figure_html(prefix: str, src: str, alt: str, caption: str, credit: str, credit_url: str, cls: str) -> str:
    credit_link = (
        f'<a href="{esc(credit_url)}">{esc(credit)}</a>' if credit_url else esc(credit)
    )
    return f"""
    <figure class="{cls}">
      <img src="{asset(prefix, src)}" alt="{esc(alt)}">
      <figcaption class="caption">
        {esc(caption)}
        <span class="credit">{credit_link}</span>
      </figcaption>
    </figure>
    """


def render_blocks(prefix: str, blocks: list[dict]) -> str:
    parts = []
    for block in blocks:
        kind = block["type"]
        if kind == "p":
            parts.append(f"<p>{esc(block['text'])}</p>")
        elif kind == "question":
            parts.append(f'<div class="question"><p>{esc(block["text"])}</p></div>')
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
                        <p>{esc(person.get("text", ""))}</p>
                        {cap}
                      </div>
                    </article>
                    """
                )
            parts.append(f'<div class="people">{"".join(cards)}</div>')
        else:
            raise SystemExit(f"Unknown block type: {kind}")
    return "\n".join(parts)


def render_lesson(lesson: dict) -> str:
    prefix = "../../"
    subject = SUBJECT_BY_ID[lesson["subject"]]
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

    toc = "".join(
        f'<li><a href="#{esc(section["id"])}">{esc(section["kicker"])}</a></li>'
        for section in lesson["sections"]
    )

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
        <div class="timeline wrap" aria-label="Era timeline">
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
              {render_blocks(prefix, section["blocks"])}
            </section>
            """
        )

    watch_items = []
    for item in lesson.get("watch", []):
        watch_items.append(
            f"""<li>
              <a href="{esc(item["url"])}">{esc(item["title"])}</a>
              <span class="note">{esc(item["note"])}</span>
            </li>"""
        )
    watch_html = ""
    if watch_items:
        watch_html = f"""
        <aside class="watch" aria-labelledby="watch-heading">
          <h2 id="watch-heading">Watch</h2>
          <ol>{''.join(watch_items)}</ol>
        </aside>
        """

    body = f"""
    <article class="lesson">
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
        <nav aria-label="In this capsule">
          <ol class="toc">{toc}</ol>
        </nav>
      </div>
      {timeline_html}
      <div class="wrap prose-wrap">
        {''.join(sections)}
        {watch_html}
      </div>
    </article>
    """
    return page_shell(
        title=f"{lesson['title']} — Capsules",
        description=lesson["dek"],
        prefix=prefix,
        canonical=f"{SITE_URL}/lessons/{lesson['slug']}/",
        body=body,
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
        write(OUT / "lessons" / lesson["slug"] / "index.html", render_lesson(lesson))

    index = [
        {
            "slug": lesson["slug"],
            "date": lesson["date"],
            "subject": lesson["subject"],
            "title": lesson["title"],
            "dek": lesson["dek"],
            "url": f"{BASE}/lessons/{lesson['slug']}/",
        }
        for lesson in lessons
    ]
    write(OUT / "lessons.json", json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    print(f"Built {len(lessons)} lesson(s) into {OUT}")


if __name__ == "__main__":
    build()
