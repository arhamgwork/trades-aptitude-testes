# Verification report

Generated 2026-09-21 by `node scripts/report.js`.

For each exam: question counts, answer-key distribution, the share of items
with an independent computational check, and blind-solve disagreements found
and fixed. Every correction is also logged in `docs/CORRECTIONS.md`.

## IBEW Local 701 (DuPage) — Practice Exam, Form A

- **Id:** `ibew-701-formA`
- **Test:** Electrical Training Alliance Aptitude Test — Electrical Training Alliance
- **Confidence:** CONFIRMED
- **Blueprint:** `docs/blueprints/electrical-ibew-701.md` (checked 2026-09-21)
- **Calculator:** not allowed

### Section counts vs blueprint

| Section | Blueprint questions | Actual | Time | Time source |
|---|---|---|---|---|
| Algebra and Functions | 33 | 33 | 46 min | official |
| Reading Comprehension | 36 | 36 | 51 min | official |

### Answer-key distribution

Uniform target 25.0%. Limits: 8 points overall, 12 points within a section of 30+ items, no more than 3 identical in a row.

| Letter | Count | Share | Deviation |
|---|---|---|---|
| A | 18 | 26.1% | +1.1 |
| B | 17 | 24.6% | -0.4 |
| C | 17 | 24.6% | -0.4 |
| D | 17 | 24.6% | -0.4 |

Longest run of the same correct letter: **3**.

### How each key was checked

| Method | Items | Share |
|---|---|---|
| `blind-solve` | 36 | 52.2% |
| `python:fractions` | 23 | 33.3% |
| `python:symbolic` | 10 | 14.5% |

**Computationally checked: 33 of 69 (47.8%).**

No item is marked `unchecked`.

### Structural checks

- Distinct stems: 69 of 69
- Items with a figure: 0
- Items with a per-distractor error note on every wrong choice: 69 of 69
- Explanations referencing a choice by letter: 0 (must be 0)

## Blind-solve passes

Non-computational items (reading, conceptual mechanical) are answered by an
independent solver that never sees the key. Every disagreement is resolved
before the item ships.

| Exam | Section | Items | Disagreements | Outcome |
|---|---|---|---|---|
| IBEW Local 701 Form A | Reading Comprehension | 36 | 0 | All 36 keys confirmed independently. One item (`e701a-read-013`) was reworded after the solver flagged its option set as loose, even though it had chosen the intended answer. See `docs/CORRECTIONS.md`. |

## Automated gates

`node scripts/build.js` fails the build if any of these break:

1. Question, section and option counts match the blueprint.
2. `correctIndex` in range. 3. No duplicate stems. 4. No identical options.
5. `node --check` on every JS file. 6. No third-party script or tracking URLs.
7. Every SVG parses. 8. No explanation names a choice by letter.
9. `distractorNotes` aligned with `choices`. 10. Answer-key balance limits.

`node tests/plan.test.js` checks that timers come from the blueprint per-section
table and that Real, Untimed and Custom draw the same question set.

`node tests/smoke.js` drives a real browser: every exam starts, is answerable,
submits, shows results and renders its print view; section timers auto-advance;
the site works with `localStorage` unavailable; zero console errors; zero
requests to third-party domains.
