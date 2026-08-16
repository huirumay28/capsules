# Capsules

Huiru Huang’s weekday lesson archive: one era at a time.

- Monday: Feminism
- Tuesday: Music
- Wednesday: Film
- Thursday: Literature
- Friday: History
- Saturday: Business
- Sunday: Psych / soc

Live site: <https://huirumay28.github.io/capsules/>

This is a long-form archive, not a daily paper. Each lesson is a capsule — before, the era, people, a story, after, and a question — meant to be read in about ten to fifteen minutes. Select any words, or tap a dotted term, for the glossary. The homepage search filters the archive as you type.

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
    "caption": "What we are looking at, and why it matters.",
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
  "listen": [
    { "title": "Exact track", "url": "https://...", "note": "What the link actually is." }
  ],
  "glossary": [
    { "term": "coverture", "aliases": ["optional other name"], "explain": "Short definition plus context. Do not invent." }
  ],
  "fun_fact": {
    "title": "A true aside",
    "text": "Playful but checkable. Never invented."
  },
  "sections": [
    {
      "id": "before",
      "kicker": "Before",
      "title": "Section title",
      "blocks": [
        { "type": "p", "text": "A paragraph." },
        { "type": "figure", "src": "lessons/slug/img.jpg", "alt": "...", "caption": "...", "credit": "...", "credit_url": "", "fit": "contain" },
        { "type": "list", "items": ["Optional list block."] },
        { "type": "question", "text": "A question to leave on the table." }
      ]
    }
  ]
}
```

`subject` must be one of: `feminism`, `music` (older files may still say `rock`), `film`, `literature`, `history`, `business`, `psych`.

Block types: `p`, `figure`, `people`, `question`, `list`.

Optional figure field `fit`: `"contain"` for documents and labels (default is a large cropped photograph).

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

## Trial lessons (16 August 2026)

- [First Wave (c. 1848–1920)](https://huirumay28.github.io/capsules/lessons/first-wave/)
- [British Invasion (c. 1963–1967)](https://huirumay28.github.io/capsules/lessons/british-invasion/)
- [French New Wave (c. 1958–1964)](https://huirumay28.github.io/capsules/lessons/french-new-wave/)
- [High Modernism (c. 1910–1930)](https://huirumay28.github.io/capsules/lessons/high-modernism/)
- [1937–1945: when the world war started in China](https://huirumay28.github.io/capsules/lessons/war-of-resistance/)
