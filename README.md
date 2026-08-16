# Capsules

Huiru Huang’s daily lesson archive: one era at a time, 8:45 Taipei.

- Monday: Feminism
- Tuesday: Music
- Wednesday: Film
- Thursday: Literature
- Friday: History
- Saturday: Business
- Sunday: Psych / soc

Live site: <https://huirumay28.github.io/capsules/>

This is a long-form archive, not a daily paper. Each lesson is a capsule — before, the era, people, a story, after, a fun fact, and a question — meant to be read in about ten to fifteen minutes. Compare what else was happening in the world at the same time. Look out from where the capsule stands. It is not a formula of “Western frame + Asian peer.”

The homepage splits into **This week** (Monday–Sunday, Asia/Taipei) and **Previous lessons**. Search filters the archive by title, dek, subject, era, and body as you type.

On a lesson page: select any words, or tap a dotted term, for a glossary entry. If there is no entry, the page says so. It does not invent a definition.

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
  "related": [],
  "title": "Era title",
  "dek": "One-line summary.",
  "era": "c. 1848–1920",
  "reading_minutes": 12,
  "thumb": { "src": "lessons/first-wave/portrait.jpg", "alt": "..." },
  "hero": {
    "src": "lessons/first-wave/wide.jpg",
    "alt": "...",
    "caption": "What the picture is doing in the lesson, not only a credit.",
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
    { "title": "Exact track", "url": "https://...", "note": "What the recording actually is." }
  ],
  "glossary": [
    { "term": "coverture", "aliases": ["covered"], "explain": "Definition plus a short context. Do not invent." }
  ],
  "fun_fact": {
    "title": "A true aside",
    "text": "True only. Optional image: { src, alt, caption, credit, credit_url }."
  },
  "sections": [
    {
      "id": "before",
      "kicker": "Before",
      "title": "Section title",
      "blocks": [
        { "type": "p", "text": "A paragraph. Known lesson titles become links." },
        { "type": "figure", "src": "lessons/slug/img.jpg", "alt": "...", "caption": "...", "credit": "...", "credit_url": "" },
        { "type": "question", "text": "A question to leave on the table." }
      ]
    }
  ]
}
```

`subject` must be one of: `feminism`, `music` (or `rock`), `film`, `literature`, `history`, `business`, `psych`.

`related` is an array of other lesson slugs. The build also auto-links known titles and slugs in body text, and renders a Referenced / In this subject strip when there is something to show.

Block types: `p`, `figure`, `people`, `question`, `list`.

Images: Wikimedia / Library of Congress / government / public domain / clearly free licenses only. Captions explain the picture. No invented facts, quotes, numbers, or photographs. No AI images of real people.

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

## Lessons

- [First Wave](https://huirumay28.github.io/capsules/lessons/first-wave/)
- [British Invasion](https://huirumay28.github.io/capsules/lessons/british-invasion/)
- [French New Wave](https://huirumay28.github.io/capsules/lessons/french-new-wave/)
- [High modernism](https://huirumay28.github.io/capsules/lessons/high-modernism/)
- [War of Resistance](https://huirumay28.github.io/capsules/lessons/war-of-resistance/)
- [David and Goliath: how the smaller player wins](https://huirumay28.github.io/capsules/lessons/david-and-goliath/)
- [Kitty Genovese and the bystander that wasn’t](https://huirumay28.github.io/capsules/lessons/bystander-genovese/)
