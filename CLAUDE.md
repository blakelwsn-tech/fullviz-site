# FullViz site

The personal-brand site for Blake Lawson, founder of FullViz (the trade name of IKWID Consulting LLC, Costa Mesa, CA). It lives at https://www.fullviz.io and is served by GitHub Pages straight from this repo. Plain HTML, one stylesheet, a little vanilla JS. No framework and no build step.

The site's job is credibility and identity. It is not a lead-generation funnel. Visitor actions, in priority order: book a meeting, email, follow on LinkedIn.

**This repo is public.** Anything committed here is published. Read "Guardrails" before writing a word of copy.

## Guardrails

1. **Never name or describe the current engagement** in any way that could identify it. That includes page copy, HTML comments, alt text, commit messages, and this file.
2. **Only these past employers may be named:** Amazon, Target, SAP, Nuna Baby, Gorjana. No other company names: not clients, not partner firms, not vendors, not sister brands.
3. **Never invent** metrics, testimonials, client names, or results. Where proof is missing, leave a `<!-- TODO: proof -->` comment and tell Blake.
4. **Proof comes only from `raw/proof/`**, which is on Blake's machine and gitignored. Consulting-client stories are anonymized to problem, approach, outcome, with the client described by industry only.
5. **Attribution stays honest.** Company growth during Blake's tenure, projections, and market sizing are not presented as his results.
6. **Personal life stays quiet.** No family names. Use only the personal details Blake has put on the site himself.
7. **Never commit** `raw/`, `copy/`, `directions/`, `.claude/`, or `CLAUDE.local.md`. They are in `.gitignore`. Check `git status` before every commit.
8. **More rules live in `CLAUDE.local.md`**, a private file on Blake's machine that is not committed. Read it before writing about past employers or clients. If it's missing, ask Blake before writing new proof stories.
9. **Industry statistics need a source.** Any number about the industry (return rates, survey results) gets a visible link to where it came from, and the year. Check the source before publishing; do not quote figures from memory.
10. **Claims about other companies' products need checking.** For example, where a former employer's product lives today. If it can't be verified from that company's own pages, leave it out.
11. Jeff Bezos is named once, on the About page, as the source of the one-way and two-way door idea. Blake asked for that. No other executive name-dropping.

## Structure

```
index.html              Home
about.html              About
field-notes.html        Field Notes index (filter by domain), "Things I keep seeing", "Elsewhere" list
field-notes/*.html      One page per Field Note
contact.html            Contact (the booking link lives here, and only here)
404.html                Not-found page (uses absolute "/" paths, see below)
assets/css/site.css     The one stylesheet. Tokens at the top.
assets/js/site.js       Mobile menu + renders the "Elsewhere" list
assets/js/writing-data.js   The list of external writing links
assets/img/             Photos (WebP + JPEG), logo, icons, share image
partials/               Source of truth for blocks shared between pages
tools/                  Optional helpers. Nothing here runs when a page loads.
CNAME, robots.txt, sitemap.xml, .nojekyll, favicon.ico
```

### Shared blocks (header, footer, call to action, figures)

Pages contain shared blocks between marker comments:

```html
<!-- @include header -->
...copied in from partials/header.html...
<!-- @end header -->
```

To change a shared block, edit the file in `partials/`, then run:

```bash
python3 tools/sync.py
```

It rewrites every page between the markers. `{{root}}` in a partial becomes the relative path to the site root. The nav link matching the page's `<body data-page="...">` gets `aria-current="page"`. Never hand-edit between the markers; the next sync overwrites it.

Partials: `head` (fonts, CSS, icons), `header`, `footer`, `cta` (the yellow band), `scripts`, `analytics`, `swipe` (the headline highlighter), and the figures `fig-*`.

`404.html` is served by GitHub Pages for any missing URL at any depth, so sync gives it absolute paths (`/assets/...`). It only looks right on the real domain or a server rooted at this folder.

### Previewing locally

```bash
python3 -m http.server 4173
```

Then open http://localhost:4173.

## Design tokens

All in `:root` at the top of `assets/css/site.css`.

| Token | Value | Use |
|---|---|---|
| `--paper` | `#FBF4E4` | Page background, warm cream |
| `--paper-deep` | `#F3E8CE` | Quiet panels |
| `--sheet` | `#FFFDF7` | Cards and "printed" sheets |
| `--ink` | `#003366` | The logo navy. Text and lines |
| `--muted` | `#46698A` | Secondary text (5.3:1 on paper) |
| `--beam` | `#FFD43B` | The signature yellow: highlighter, buttons, the CTA band |

Yellow is never used for text or thin lines on cream; it doesn't have the contrast. It works as a filled area with navy on top (8.9:1).

| Font | Token | Use |
|---|---|---|
| Fraunces (SOFT 70, WONK 1) | `--display` | Headlines, big numbers, italic ledes |
| Hanken Grotesk | `--body` | Body copy, buttons |
| IBM Plex Mono | `--mono` | Small uppercase labels, figure labels |
| Nanum Pen Script | `--hand` | Handwritten notes and asides |

Fonts load from Google Fonts in `partials/head.html`. The Nanum request uses `&text=` to fetch only Latin characters; if a handwritten note needs a new symbol, add it there.

Type sizes are fluid `clamp()` tokens (`--h1-hero`, `--h1`, `--h2`, `--h3`, `--lede`). Section spacing is `--section`. Layout width is `--wrap` (80rem); reading width is `--measure` (36rem).

### The visual idea

A process "as documented", marked up "as it actually runs". Printed things are thin navy lines with mono labels. Markup is a navy pen (handwriting, arrows) and a yellow highlighter. The lighthouse is the brand mark: it shows where the rocks are. Hand-drawn SVG diagrams replace stock photos and icons. Sheets and cards sit slightly rotated, with yellow tape.

### Figures

`tools/diagrams.py` draws every figure with `tools/sketch.py` (a small seeded hand-drawing helper) and writes them to `partials/fig-*.html`. To change or add one:

```bash
python3 tools/diagrams.py && python3 tools/sync.py
```

Figures are inline SVG so they pick up the page fonts and colour tokens through the `f-*` classes in section 10 of the stylesheet. Each has a wide and a tall version where the layout needs it.

## Voice

First person, Blake's voice. Professional, with his humour and opinions. Playful in the details (labels, buttons, the 404, the footer), serious in the claims.

- **No em dashes. Ever.** No en dashes as separators either; write ranges as "30 to 40%".
- Plain words first. Trade terms get explained the first time ("quote to cash" is defined on the home page).
- Sentence-case headings. Oxford comma. Contractions, but not in every sentence.
- Open flat, with a plain declarative. No warm-up.
- Mix long sentences with short ones. Starting a sentence with "But", "So", or "And" is fine.
- Asides go in parentheses. Humour is dry and specific, and usually at his own expense.
- Concrete numbers over adjectives. "Return rate was over 60%", not "returns were high".
- Direct when advising the reader. Modest about himself.
- No bold for emphasis inside prose. No bulleted lists of bolded label plus description.
- Don't end a page on a tidy lesson. End on the thing itself.

Words that never appear: leverage, utilize, ensure, robust, comprehensive, impactful, passionate, delve, landscape, ecosystem, framework, synergy, alignment, best practices, bandwidth, nuanced, seamless, crucial, enhance, showcase, valuable, "at the end of the day", "the truth is", "it's worth noting", "here's the thing".

## Common edits

### Add a Field Note

Every note carries four things besides its story: **where** it happened, a **stage** (`0 to 1` for building the first version, `1 to 2` for making it work at scale), one or two **domains**, and a one-line **tagline** that says what Blake owned or which number moved.

The five domains, with the keys the filter uses:

| Key | Label |
|---|---|
| `inventory` | Inventory and planning |
| `operations` | Fulfillment and operations |
| `returns` | Returns and post-purchase |
| `product` | Product and systems |
| `finance` | Finance and data |

1. Copy `tools/field-note-template.html` to `field-notes/your-slug.html`. Use lowercase words and hyphens for the slug.
2. Fill in the capitalised placeholders: title, where, tagline, stage, domain tags, description, the scoreboard numbers, and the three sections. Replace `SLUG` in the canonical and `og:url` lines. Numbers come from `raw/proof/` only.
3. Point the "Next" link at an existing note, and point another note's "Next" link at this one so the loop includes it.
4. In `field-notes.html`, add a `<li class="card">` to the "Proof of work" list. Copy an existing card and change `data-domains` (domain keys, space-separated), the stage, the domain labels, the title, the link, the tagline, and the where line.
5. In `index.html`, "Fresh from the field" shows three cards. Swap one for the new note if it deserves the spot.
6. Add the URL to `sitemap.xml`.
7. Run `python3 tools/sync.py` to fill in the header and footer.

The filter buttons on `field-notes.html` are plain buttons with `data-filter` set to a domain key. `assets/js/site.js` shows the cards whose `data-domains` include that key. A link to `field-notes.html#returns` (or any key) opens the page already filtered. To add a domain, add a button, use the key on the cards, and add a row to the table above.

### Add a "Things I keep seeing" entry

These are Blake's own opinions, on `field-notes.html`. Add an `<article class="slip">` inside `<div class="seeing">`. Only publish an entry Blake has written or approved. If it leans on an industry number, link the source in a `<p class="source">` line.

### Add a writing link

Open `assets/js/writing-data.js` and add one line at the top of the list:

```js
{ title: "Post title", url: "https://...", source: "LinkedIn" },
```

That's the whole edit. No sync needed.

### Swap a photo

Photos are served as WebP with a JPEG fallback, at two sizes each.

| Photo | Files | Pixel sizes |
|---|---|---|
| About portrait (4:5) | `blake-portrait-480`, `blake-portrait-960` | 480×600, 960×1200 |
| Home byline (square) | `blake-face-136`, `blake-face-272` | 136×136, 272×272 |

1. Crop and resize with `sips` (arguments are height then width):

   ```bash
   sips -z 1200 960 new-photo.jpg -s format jpeg -s formatOptions 76 --out assets/img/blake-portrait-960.jpg
   ```

   Repeat for the smaller size.
2. Make the WebP versions:

   ```bash
   python3 tools/to_webp.py assets/img/blake-portrait-480.jpg assets/img/blake-portrait-960.jpg
   ```

3. If the subject changed, update the `alt` text on the `<img>`. Keep the file names and the page needs no other edit.

For a new photo somewhere else, copy the `<picture>` block from `about.html` and always set `width`, `height`, and `alt`.

### Add the booking link

It lives in one place: the first card in `contact.html`, marked with a `TODO: booking link` comment. Follow the comment. Every "Book a meeting" button on the site already points to `contact.html#book`.

### Change the header, footer, or the yellow call to action

Edit `partials/header.html`, `partials/footer.html`, or `partials/cta.html`, then run `python3 tools/sync.py`.

### Add analytics (phase 2)

Paste the snippet into `partials/analytics.html` and run `python3 tools/sync.py`. It lands before `</body>` on every page.

### Refresh the seasonal line

The last paragraph of "Off the clock" in `about.html` is about what Blake is growing right now. It's marked with a comment. Update it a few times a year.

## Open TODOs

Search the repo for `TODO` to find them all.

- Booking link (`contact.html`). Until it exists, the button opens an email.
- Substack link (`partials/footer.html`, `assets/js/writing-data.js`).
- Specific LinkedIn posts for the "Elsewhere" list.
- Two or three non-headshot photos for `about.html`.
- "Things I keep seeing" on `field-notes.html` has two entries, both Blake's. Four more drafts are waiting on his review.
- The private review list in `CLAUDE.local.md` (not committed) tracks paragraphs Blake still needs to confirm.
- Self-host the fonts (download the four families into `assets/fonts/` and replace the two Google Fonts links in `partials/head.html`).

## Deploying

Push to `main`. GitHub Pages serves the repo root. The `CNAME` file sets the custom domain to `www.fullviz.io`, and `.nojekyll` tells Pages to serve files as they are.

Before pushing: run `python3 tools/sync.py`, check `git status` shows nothing from `raw/`, `copy/`, or `directions/`, and open the changed pages at phone and desktop widths.
