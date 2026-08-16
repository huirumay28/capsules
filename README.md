# Capsules

Huiru Huang’s weekday lesson archive: one era at a time.

- Monday: Feminism
- Tuesday: Rock and roll
- Wednesday: Film
- Thursday: Literature
- Friday: History

Live site: <https://huirumay28.github.io/capsules/>

This is a long-form archive, not a daily paper. Each lesson is a capsule — before, the era, people, a story, after, and a question — meant to be read in about ten to fifteen minutes.

## How to add a lesson

1. Add one JSON file to `content/lessons/`.
2. Name it `YYYY-MM-DD-slug.json` (the date in the filename is for you; the date the site uses is the `date` field).
3. Put images in `assets/lessons/<slug>/`.
4. Run `python3 build.py`.
5. Commit the content file, any new images, and the rebuilt `docs/` folder.

The homepage is generated from every file in `content/lessons/`. You do not edit the index by hand.

A lesson file needs:

```json
{
  "slug": "first-wave",
  "date": "2026-08-16",
  "subject": "feminism",
  "title": "Era title",
  "dek": "One-line summary.",
  "era": "c. 1848–1920",
  "reading_minutes": 12,
  "thumb": { "src": "lessons/first-wave/portrait.jpg", "alt": "..." },
  "hero": {
    "src": "lessons/first-wave/wide.jpg",
    "alt": "...",
    "caption": "...",
    "credit": "Library of Congress / public domain",
    "credit_url": "https://www.loc.gov/item/..."
  },
  "honesty": "Optional framing note.",
  "timeline": [
    { "year": "1848", "label": "Seneca Falls", "detail": "Short gloss." }
  ],
  "watch": [
    { "title": "Exact film title", "url": "https://...", "note": "What the film actually is." }
  ],
  "sections": [
    {
      "id": "before",
      "kicker": "Before",
      "title": "Section title",
      "blocks": [
        { "type": "p", "text": "A paragraph." },
        { "type": "figure", "src": "lessons/slug/img.jpg", "alt": "...", "caption": "...", "credit": "...", "credit_url": "" },
        { "type": "question", "text": "A question to leave on the table." }
      ]
    }
  ]
}
```

`subject` must be one of: `feminism`, `rock`, `film`, `literature`, `history`.

Block types: `p`, `figure`, `people`, `question`.

## Local preview

```bash
python3 build.py
python3 -m http.server --directory docs 8080
```

Then open <http://127.0.0.1:8080/>. Paths are relative, so the same files also work at `/capsules/` on GitHub Pages.

## How Pages deploys

The built site lives in `docs/` and is committed with each change. GitHub Pages is set to deploy from `main` / `/docs`. A `.nojekyll` file is included so GitHub does not run Jekyll on the output.

Project URL: `https://huirumay28.github.io/capsules/`

If the site 404s after the first push, open Settings → Pages and set Source to **Deploy from a branch**, branch `main`, folder `/docs`.

## First lesson

[First Wave (c. 1848–1920): who got to count as a “woman” in public](https://huirumay28.github.io/capsules/lessons/first-wave/)
