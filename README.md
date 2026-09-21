# Trades Aptitude Practice

Practice site for Chicago-area skilled-trades apprenticeship aptitude tests
(Cook and DuPage counties). Full-length, format-faithful practice exams plus
cross-trade skill drills.

> **Unofficial practice material, not affiliated with any union, JATC, or test
> publisher.** Text names only, no logos or branded imagery. All questions are
> original, written against published test blueprints.

## What is here

- `PLAN.md` — live checklist: trades, confidence labels, phases, what is built
  and what is deferred.
- `docs/blueprints/` — one file per trade: per-section table (questions, time,
  format, calculator), provider, which locals use it, scoring, source URLs,
  date checked, and a confidence label (CONFIRMED / PARTIAL / UNKNOWN).
- `docs/CORRECTIONS.md` — every content change and every conflict found between
  research and the brief. Nothing is changed silently.
- `VERIFICATION_REPORT.md` — per exam: counts, answer-key distribution, share of
  items with a computational check, blind-solve disagreements.
- `data/` — source of truth. `data/<trade>/<exam>.json`, validated schema.
- `src/` — the site: plain HTML, CSS and vanilla JS. No framework, no tracking,
  no third-party scripts.
- `scripts/verify/` — Python builders that compute and assert every answer key.

## Run it locally

No install needed to build:

```sh
node scripts/build.js          # validate, run gates, emit dist/
node tests/server.js dist 8080 # serve it
```

Then open <http://127.0.0.1:8080>. The app loads question banks with `fetch()`
from the same host, so it needs to be served over http rather than opened as a
file. For an offline copy that needs no server, use
`dist/single/<exam>.html` — one self-contained file per exam, booklet plus
answer key, suitable for printing.

## Run the checks

```sh
node scripts/build.js      # build gates (see below)
node tests/plan.test.js    # timers come from the blueprint, not a guess
npm install                # dev-only: playwright, for the browser test
node tests/smoke.js        # real browser: start, answer, submit, results, print
node scripts/report.js     # regenerate VERIFICATION_REPORT.md
```

The build fails, rather than shipping, if any of these break:

1. Question, section and option counts match the blueprint.
2. `correctIndex` is in range. 3. No duplicate stems. 4. No identical options.
5. `node --check` passes on every JS file. 6. No third-party script or tracking
URLs. 7. Every SVG parses. 8. No explanation names a choice by letter.
9. `distractorNotes` line up with `choices`. 10. Answer-key balance limits.

## Add or change questions

Question data is **generated**, not hand-edited, so that every key is computed
and asserted rather than typed:

1. Edit or add a builder in `scripts/verify/gen_<exam>.py`. Each item computes
   its own answer (exact arithmetic via `fractions`) and asserts it, and each
   distractor names the specific mistake it represents.
2. Run `python3 scripts/verify/build_<exam>.py` to rebuild the JSON. This
   applies the deterministic seeded key rebalance and prints the letter spread.
3. Run `node scripts/build.js` to re-run every gate.
4. Run `node scripts/report.js` and commit the updated report.

Items whose keys cannot be computed (reading, conceptual mechanical) carry
`verify: "blind-solve"` and are checked by an independent solver that never
sees the key. Anything that cannot be independently checked is marked
`verify: "unchecked"` and listed in the verification report.

See `docs/SCHEMA.md` for the full question and exam schema.

## Offline use

The hosted site installs as an app and keeps working with no signal once it
has been opened online. A service worker caches the site's own files and every
exam bank, network-first so a redeploy is still picked up when there is a
connection. It never contacts another origin. For a copy that needs no browser
support at all, `dist/single/<exam>.html` is one self-contained file per exam.

## Deploy

GitHub Actions builds, runs every gate and the browser smoke test, and deploys
`dist/` to GitHub Pages only if all of it passes — see
`.github/workflows/deploy.yml`. Pushing to `main` redeploys.

First-time setup: in the repository settings, under Pages, set the source to
**GitHub Actions**.
