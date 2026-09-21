# PLAN.md — Chicago-area trades aptitude practice site

Live checklist. Updated at every phase. Status keys:
`[ ]` todo · `[~]` in progress · `[x]` done · `[!]` blocked · `[-]` deferred

---

## Phase 0 gate — decided 2026-09-21

1. **`source-exams/` is not present** (no commits, no remote branches, nothing
   on the machine). Nothing was invented or substituted.
   **Decision: the user will re-upload `source-exams/`.** Migration waits for
   the files; the engine is built first and the four exams slot in on arrival.
   Until then the four migrated exams stay `[!]` blocked, not rebuilt.
2. **IBEW Local 134 format is disputed** (brief says GAN; could not confirm).
   **Decision: build both variants** — one ETA-format and one GAN-format exam
   for 134, each badged PARTIAL, with the open question shown on the trade
   page so neither is presented as settled.

---

## Trades and confidence

`CONFIRMED` = official source states the format · `PARTIAL` = some confirmed,
rest inferred (blueprint says exactly which) · `UNKNOWN` = no reliable format.

Provider confidence and *per-section* confidence are tracked separately,
because for the GAN trades the provider is certain and the section timings
are not.

### Tier 1 — the trades you named

| Trade | Test | Provider | Per-section | Exam plan |
|---|---|---|---|---|
| Electrical — DuPage (IBEW 701) | ETA 2-section | CONFIRMED | CONFIRMED | Full exam, 69 q / 97 min |
| Electrical — Cook (IBEW 134) | disputed | PARTIAL | PARTIAL | **Two exams**: ETA-format + GAN-format, both PARTIAL |
| Pipefitting (UA 597) | GAN battery | CONFIRMED | PARTIAL | Full exam, 140 q / ~119 min |
| Plumbing (UA 130) | GAN battery | CONFIRMED | PARTIAL | Full exam, 140 q / 119 min |
| Elevator (IUEC / NEIEP) | EIAT | CONFIRMED | PARTIAL | Full exam, 100 q / ~90 min |
| Sheet metal (SMART 73) | likely GAN | PARTIAL | PARTIAL | Full exam on GAN table, badged |

### Tier 2 — surveyed, full blueprint written before building

All are Chicago & Cook County Building Trades Council locals. GAN names these
trades on its own site but not the specific locals, so each needs its own
blueprint pass in Phase 3 before an exam is built.

| Trade | Local | Expected test | Status |
|---|---|---|---|
| Ironworkers (structural) | Local 1 | GAN — **provider confirmed** (GAN sells its test registration) | PARTIAL |
| Ironworkers (ornamental / riggers) | Local 63, 136 | GAN, likely shared with Local 1 | research pending |
| Sprinkler fitters | Local 281 | GAN | research pending |
| Steamfitters / HVACR | UA locals | GAN (same battery as 597/130) | PARTIAL |
| Carpenters / millwrights | Mid-America Carpenters Regional Council | GAN | research pending |
| Operating engineers | IUOE 150 (ASIP) | GAN | research pending |
| Boilermakers | Local 1 | GAN | research pending |
| Bricklayers / tile | BAC Local 21 | GAN | research pending |
| Roofers | Local 11 | GAN | research pending |
| Insulators (heat & frost) | Local 17 | unknown | research pending |
| Painters / glaziers | Painters DC 14 | unknown | research pending |
| Cement masons | Local 502 | unknown | research pending |
| Laborers | Laborers District Council | often no aptitude test | research pending |
| Line construction (outside) | IBEW outside locals | ETA has a separate outside/line test | research pending |
| Low-voltage / communications | IBEW 134 IN-TECH comms program | ETA has a separate telecom test | research pending |

Trades that turn out to have **no** formal aptitude test, or that stay
UNKNOWN, get a trade page with the blueprint card saying so plus general
skill drills — no fabricated exam.

---

## Exams to build

Full-length Form A per CONFIRMED/PARTIAL trade, plus Form B in Phase 4.
Every exam is per-section timed from its blueprint table.

- `electrical-701-formA` — 2 sections, 69 q
- `pipefitting-597-formA` — 6 sections, 140 q
- `plumbing-130-formA` — 6 sections, 140 q
- `elevator-eiat-formA` — 3 sections, 100 q (incl. "No answer" option)
- `sheetmetal-73-formA` — 6 sections, 140 q
- `electrical-134-eta-formA` — 2 sections, 69 q (ETA variant, PARTIAL)
- `electrical-134-gan-formA` — 6 sections, 140 q (GAN variant, PARTIAL)
- Tier 2 exams — ordered by how many Chicago apprenticeships use the test,
  so: the remaining GAN trades first (one shared battery serves many), then
  the one-off formats.

## Skill drills (cross-trade)

fractions/decimals/percents/ratios · unit conversions · geometry (area,
volume) · algebra and functions · **sign analysis** (migrating yours; four
underlying rules) · **variable relationships** (4 sub-types, samples shown
before volume) · number series · reading comprehension and cloze ·
mechanical comprehension (gears, pulleys, levers, hydraulics, circuits) ·
spatial (paper folding, cube unfolding, rotations)

---

## Folder layout

```
data/<trade>/<exam>.json     source of truth, validated schema
data/drills/<skill>.json     cross-trade drill banks
docs/blueprints/<trade>.md   per-section table, sources, confidence
docs/CORRECTIONS.md          every content change, never silent
src/                         plain HTML/CSS/vanilla JS app
scripts/build.js             dependency-free Node build + gates
scripts/verify/              Python answer-key verifiers
dist/                        deployable static site
dist/single/<exam>.html      standalone single-file exam per exam
tests/                       Playwright smoke tests (dev-only dep)
VERIFICATION_REPORT.md       counts, key distribution, check coverage
.github/workflows/deploy.yml build + gates + Pages deploy
```

---

## Phases

- [x] **Phase 0 — Inventory and plan.** Source exams checked (absent),
      blueprints researched, PLAN.md written. **Awaiting your OK.**
- [x] **Phase 1 — Engine and shell.** Schema, validator, exam runner,
      results, print view, progress, home and trade pages, one exam
      end-to-end. Ships usable.
      Done: schema + validator, 10 build gates, runner with per-section
      timers and auto-advance, Real/Untimed/Custom timing, question grid,
      flagging, keyboard shortcuts, submit confirmation, results with
      per-distractor error notes and skill breakdown, print booklet + answer
      key, single-file offline copies, progress with weak-spot links and
      JSON export/import, home/trade/drills/progress pages.
      End-to-end exam is **IBEW 701 Form A** (69 items, the one CONFIRMED
      format, so no guessing entered the engine proof): 33 algebra items
      computed and asserted in Python, 36 reading items across 4 original
      passages, blind-solved with 0 disagreements.
      Tests: 9 plan unit tests, 30 browser smoke checks, zero console errors,
      zero third-party requests.
- [ ] **Phase 2 — Migrate + drills.** `[!]` The four existing exams, blocked
      until `source-exams/` is re-uploaded; re-verified on arrival. Sign-analysis and
      variable-relationship drill sets. **Sample variable-relationship items
      shown to you before building at volume.**
- [ ] **Phase 3 — New trades.** Sheet metal first, then Tier 2 by reach.
      One section at a time, verified before moving on.
- [ ] **Phase 4 — Depth.** Form B per trade, more drills, PWA offline mode.

## Deployment

GitHub Pages from this repo, via Actions: build → gates → tests → deploy
`dist/` only if everything passes. **I will ask before the first deploy**
(that makes the URL public) and report the live URL as soon as it succeeds.

## Standing rules

- No guessed format presented as confirmed. PARTIAL is labelled on the site.
- Every answer key independently verified before it enters a data file.
- Original content only. No logos, no branded imagery, text names only.
- Unofficial-practice notice on every page.
- No tracking, analytics, or third-party scripts.
