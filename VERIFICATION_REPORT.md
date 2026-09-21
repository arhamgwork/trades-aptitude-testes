# Verification report

Generated 2026-09-21 by `node scripts/report.js`.

For each exam: question counts, answer-key distribution, the share of items
with an independent computational check, and blind-solve disagreements found
and fixed. Every correction is also logged in `docs/CORRECTIONS.md`.

## Sign analysis — how one variable moves when another changes

- **Id:** `sign-analysis`
- **Test:** Skill drill — This site
- **Confidence:** CONFIRMED
- **Blueprint:** `docs/blueprints/_gan-battery.md` (checked 2026-09-21)
- **Calculator:** not allowed
- **Migrated from:** `source-exams/UA-597-GAN-Aptitude-Practice-Exam.html`
- **Key order:** rebalanced (authored order was outside the limits; see docs/CORRECTIONS.md)

### Section counts vs blueprint

| Section | Blueprint questions | Actual | Time | Time source |
|---|---|---|---|---|
| Sign analysis | 15 | 15 | 0 min | official |

### Answer-key distribution

Uniform target 25.0%. Limits: 8 points overall, 12 points within a section of 30+ items, no more than 3 identical in a row.

| Letter | Count | Share | Deviation |
|---|---|---|---|
| A | 4 | 26.7% | +1.7 |
| B | 4 | 26.7% | +1.7 |
| C | 4 | 26.7% | +1.7 |
| D | 3 | 20.0% | -5.0 |

Longest run of the same correct letter: **3**.

### How each key was checked

| Method | Items | Share |
|---|---|---|
| `unchecked` | 15 | 100.0% |

**Computationally checked: 0 of 15 (0.0%).**

**Items not yet independently checked: 15 of 15.**

| Section | Unchecked |
|---|---|
| Sign analysis | 15 |

These are migrated items whose keys are preserved exactly from the source
and confirmed unchanged by `scripts/migrate/verify-migration.js`, but which
have not yet had an independent re-derivation of the answer. That pass is
Phase 2 work and is tracked in `PLAN.md`.

### Structural checks

- Distinct stems: 15 of 15
- Items with a figure: 0
- Items with a per-distractor error note on every wrong choice: 0 of 15
  - Migrated items carry their error analysis inside the explanation, as
    authored. Per-choice notes were not invented, because that would mean
    writing content the original author did not write.
- Items with picture choices: 0
- Explanations referencing a choice by letter: 0 (must be 0)

## Variable relationships — all four sub-types

- **Id:** `variable-relationships`
- **Test:** Skill drill — This site
- **Confidence:** CONFIRMED
- **Blueprint:** `docs/blueprints/_gan-battery.md` (checked 2026-09-21)
- **Calculator:** not allowed

### Section counts vs blueprint

| Section | Blueprint questions | Actual | Time | Time source |
|---|---|---|---|---|
| Inequality chains | 15 | 15 | 0 min | official |
| Two-statement sufficiency | 15 | 15 | 0 min | official |
| Symbolic and functional substitution | 15 | 15 | 0 min | official |
| If-then chains | 15 | 15 | 0 min | official |

### Answer-key distribution

Uniform target 20.0%. Limits: 8 points overall, 12 points within a section of 30+ items, no more than 3 identical in a row.

| Letter | Count | Share | Deviation |
|---|---|---|---|
| A | 15 | 25.0% | +5.0 |
| B | 15 | 25.0% | +5.0 |
| C | 15 | 25.0% | +5.0 |
| D | 12 | 20.0% | +0.0 |
| E | 3 | 5.0% | -15.0 |

Longest run of the same correct letter: **2**.

### How each key was checked

| Method | Items | Share |
|---|---|---|
| `python:exhaustive (all assignments over the search range enumerated)` | 15 | 25.0% |
| `python:substitution (evaluated directly; each distractor reproduced from its named error)` | 15 | 25.0% |
| `python:truth-table (8 assignments, 1 satisfying)` | 6 | 10.0% |
| `python:truth-table (4 assignments, 1 satisfying)` | 5 | 8.3% |
| `python:truth-table (4 assignments, 2 satisfying)` | 4 | 6.7% |
| `python:exhaustive (37 models)` | 2 | 3.3% |
| `python:exhaustive (2024 models)` | 1 | 1.7% |
| `python:exhaustive (9139 models)` | 1 | 1.7% |
| `python:exhaustive (276 models)` | 1 | 1.7% |
| `python:exhaustive (16206 models)` | 1 | 1.7% |
| `python:exhaustive (288 models)` | 1 | 1.7% |
| `python:exhaustive (21 models)` | 1 | 1.7% |
| `python:exhaustive (1540 models)` | 1 | 1.7% |
| `python:exhaustive (552 models)` | 1 | 1.7% |
| `python:exhaustive (190 models)` | 1 | 1.7% |
| `python:exhaustive (144 models)` | 1 | 1.7% |
| `python:exhaustive (6 models)` | 1 | 1.7% |
| `python:exhaustive (35 models)` | 1 | 1.7% |
| `python:exhaustive (588 models)` | 1 | 1.7% |

**Computationally checked: 60 of 60 (100.0%).**

No item is marked `unchecked`.

### Structural checks

- Distinct stems: 60 of 60
- Items with a figure: 0
- Items with a per-distractor error note on every wrong choice: 60 of 60
- Items with picture choices: 0
- Explanations referencing a choice by letter: 0 (must be 0)

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
- Items with picture choices: 0
- Explanations referencing a choice by letter: 0 (must be 0)

## Elevator Constructor (EIAT) — Practice Exam, Form A

- **Id:** `eiat-formA`
- **Test:** Elevator Industry Aptitude Test (EIAT) — National Elevator Industry Educational Program (NEIEP)
- **Confidence:** PARTIAL
- **Unverified:** The three sections and the 35 / 35 / 30 split are confirmed against the NEIEP 2024 study guide. NEIEP does not publish per-section time limits; the 25 / 25 / 40 minute split used here is the one preparation courses consistently report and is derived, not official.
- **Blueprint:** `docs/blueprints/elevator-eiat.md` (checked 2026-09-21)
- **Calculator:** not allowed
- **Migrated from:** `source-exams/eiat-practice-test (1).html`
- **Key order:** rebalanced (authored order was outside the limits; see docs/CORRECTIONS.md)

### Section counts vs blueprint

| Section | Blueprint questions | Actual | Time | Time source |
|---|---|---|---|---|
| Part 1 · Reading comprehension | 35 | 35 | 25 min | derived |
| Part 2 · Mechanical comprehension | 35 | 35 | 25 min | derived |
| Part 3 · Mathematics | 30 | 30 | 40 min | derived |

### Answer-key distribution

Uniform target 20.0%. Limits: 8 points overall, 12 points within a section of 30+ items, no more than 3 identical in a row.

| Letter | Count | Share | Deviation |
|---|---|---|---|
| A | 28 | 28.0% | +8.0 |
| B | 28 | 28.0% | +8.0 |
| C | 27 | 27.0% | +7.0 |
| D | 14 | 14.0% | -6.0 |
| E | 3 | 3.0% | -17.0 |

Longest run of the same correct letter: **3**.

### How each key was checked

| Method | Items | Share |
|---|---|---|
| `unchecked` | 100 | 100.0% |

**Computationally checked: 0 of 100 (0.0%).**

**Items not yet independently checked: 100 of 100.**

| Section | Unchecked |
|---|---|
| Part 1 · Reading comprehension | 35 |
| Part 2 · Mechanical comprehension | 35 |
| Part 3 · Mathematics | 30 |

These are migrated items whose keys are preserved exactly from the source
and confirmed unchanged by `scripts/migrate/verify-migration.js`, but which
have not yet had an independent re-derivation of the answer. That pass is
Phase 2 work and is tracked in `PLAN.md`.

### Structural checks

- Distinct stems: 100 of 100
- Items with a figure: 35
- Items with a per-distractor error note on every wrong choice: 0 of 100
  - Migrated items carry their error analysis inside the explanation, as
    authored. Per-choice notes were not invented, because that would mean
    writing content the original author did not write.
- Items with picture choices: 0
- Explanations referencing a choice by letter: 0 (must be 0)

## UA Local 597 (Pipefitters) — GAN Battery Practice Exam, Form A

- **Id:** `ua-597-formA`
- **Test:** GAN Aptitude Battery — GAN Human Resources
- **Confidence:** PARTIAL
- **Unverified:** GAN is confirmed as the testing company by Local 597, and the section names come from the local’s own site. GAN does not publish per-section question counts or time limits, so the split used here is the one this exam was built with, not an official figure.
- **Blueprint:** `docs/blueprints/pipefitting-ua-597.md` (checked 2026-09-21)
- **Calculator:** not allowed
- **Migrated from:** `source-exams/UA-597-GAN-Aptitude-Practice-Exam.html`
- **Key order:** rebalanced (authored order was outside the limits; see docs/CORRECTIONS.md)

### Section counts vs blueprint

| Section | Blueprint questions | Actual | Time | Time source |
|---|---|---|---|---|
| Numerical Computation | 25 | 25 | 15 min | derived |
| Number Series | 20 | 20 | 12 min | derived |
| Problem Solving | 25 | 25 | 25 min | derived |
| Reading Comprehension | 25 | 25 | 30 min | derived |
| Mechanical Aptitude | 25 | 25 | 18 min | derived |
| Spatial Relations | 20 | 20 | 12 min | derived |

### Answer-key distribution

Uniform target 25.0%. Limits: 8 points overall, 12 points within a section of 30+ items, no more than 3 identical in a row.

| Letter | Count | Share | Deviation |
|---|---|---|---|
| A | 38 | 27.1% | +2.1 |
| B | 34 | 24.3% | -0.7 |
| C | 34 | 24.3% | -0.7 |
| D | 34 | 24.3% | -0.7 |

Longest run of the same correct letter: **3**.

### How each key was checked

| Method | Items | Share |
|---|---|---|
| `unchecked` | 140 | 100.0% |

**Computationally checked: 0 of 140 (0.0%).**

**Items not yet independently checked: 140 of 140.**

| Section | Unchecked |
|---|---|
| Numerical Computation | 25 |
| Number Series | 20 |
| Problem Solving | 25 |
| Reading Comprehension | 25 |
| Mechanical Aptitude | 25 |
| Spatial Relations | 20 |

These are migrated items whose keys are preserved exactly from the source
and confirmed unchanged by `scripts/migrate/verify-migration.js`, but which
have not yet had an independent re-derivation of the answer. That pass is
Phase 2 work and is tracked in `PLAN.md`.

### Structural checks

- Distinct stems: 121 of 140
- Items with a figure: 45
- Items with a per-distractor error note on every wrong choice: 0 of 140
  - Migrated items carry their error analysis inside the explanation, as
    authored. Per-choice notes were not invented, because that would mean
    writing content the original author did not write.
- Items with picture choices: 20
- Explanations referencing a choice by letter: 0 (must be 0)

## UA Local 130 (Plumbers) — GAN Battery Practice Exam, Form A

- **Id:** `ua-130-formA`
- **Test:** GAN Aptitude Battery — GAN Human Resources
- **Confidence:** PARTIAL
- **Unverified:** GAN is confirmed as the testing company for Local 130. GAN does not publish per-section question counts or time limits; the 140 items in 119 minutes used here match what this exam was built with, and the Reading (42 items / 25 minutes) and Problem Solving (35 / 35) figures agree with independent prep sources, but none of it is an official published figure.
- **Blueprint:** `docs/blueprints/plumbing-ua-130.md` (checked 2026-09-21)
- **Calculator:** not allowed
- **Migrated from:** `source-exams/ua-local-130-gan-practice-exam.html`
- **Key order:** kept exactly as authored

### Section counts vs blueprint

| Section | Blueprint questions | Actual | Time | Time source |
|---|---|---|---|---|
| Reading Comprehension | 42 | 42 | 25 min | derived |
| Numerical Computation | 28 | 28 | 21 min | derived |
| Numerical Reasoning | 10 | 10 | 10 min | derived |
| Problem Solving | 35 | 35 | 35 min | derived |
| Paper Folding | 12 | 12 | 15 min | derived |
| Mechanical Comprehension | 13 | 13 | 13 min | derived |

### Answer-key distribution

Uniform target 20.0%. Limits: 8 points overall, 12 points within a section of 30+ items, no more than 3 identical in a row.

| Letter | Count | Share | Deviation |
|---|---|---|---|
| A | 35 | 25.0% | +5.0 |
| B | 36 | 25.7% | +5.7 |
| C | 32 | 22.9% | +2.9 |
| D | 31 | 22.1% | +2.1 |
| E | 6 | 4.3% | -15.7 |

Longest run of the same correct letter: **3**.

### How each key was checked

| Method | Items | Share |
|---|---|---|
| `unchecked` | 140 | 100.0% |

**Computationally checked: 0 of 140 (0.0%).**

**Items not yet independently checked: 140 of 140.**

| Section | Unchecked |
|---|---|
| Reading Comprehension | 42 |
| Numerical Computation | 28 |
| Numerical Reasoning | 10 |
| Problem Solving | 35 |
| Paper Folding | 12 |
| Mechanical Comprehension | 13 |

These are migrated items whose keys are preserved exactly from the source
and confirmed unchanged by `scripts/migrate/verify-migration.js`, but which
have not yet had an independent re-derivation of the answer. That pass is
Phase 2 work and is tracked in `PLAN.md`.

### Structural checks

- Distinct stems: 119 of 140
- Items with a figure: 25
- Items with a per-distractor error note on every wrong choice: 0 of 140
  - Migrated items carry their error analysis inside the explanation, as
    authored. Per-choice notes were not invented, because that would mean
    writing content the original author did not write.
- Items with picture choices: 12
- Explanations referencing a choice by letter: 0 (must be 0)

## GAN Aptitude Battery — Practice Exam, Form B

- **Id:** `gan-battery-formB`
- **Test:** GAN Aptitude Battery — GAN Human Resources
- **Confidence:** PARTIAL
- **Unverified:** GAN is confirmed as the testing company for several Chicago-area locals, and the section names come from those locals' own sites. GAN publishes no per-section question counts or time limits, so the 25/20/25/25/25/20 split and the timings here follow the structure Local 597 uses and are derived, not official. Sheet Metal Local 73 publishes no format at all, so its use of this battery is inferred from GAN listing sheet metal among the trades it tests.
- **Blueprint:** `docs/blueprints/_gan-battery.md` (checked 2026-09-21)
- **Calculator:** not allowed

### Section counts vs blueprint

| Section | Blueprint questions | Actual | Time | Time source |
|---|---|---|---|---|
| Numerical Computation | 25 | 25 | 15 min | derived |
| Number Series | 20 | 20 | 12 min | derived |
| Problem Solving | 25 | 25 | 25 min | derived |
| Reading Comprehension | 25 | 25 | 30 min | derived |
| Mechanical Aptitude | 25 | 25 | 18 min | derived |
| Spatial Relations | 20 | 20 | 12 min | derived |

### Answer-key distribution

Uniform target 25.0%. Limits: 8 points overall, 12 points within a section of 30+ items, no more than 3 identical in a row.

| Letter | Count | Share | Deviation |
|---|---|---|---|
| A | 38 | 27.1% | +2.1 |
| B | 34 | 24.3% | -0.7 |
| C | 34 | 24.3% | -0.7 |
| D | 34 | 24.3% | -0.7 |

Longest run of the same correct letter: **3**.

### How each key was checked

| Method | Items | Share |
|---|---|---|
| `python:fractions` | 50 | 35.7% |
| `blind-solve` | 25 | 17.9% |
| `python:rule-check (rule re-applied to every printed term)` | 20 | 14.3% |
| `python:fold-model+reverse-check` | 20 | 14.3% |
| `conceptual:blind-solve` | 7 | 5.0% |
| `python:gear-ratio` | 4 | 2.9% |
| `python:mechanical-advantage` | 4 | 2.9% |
| `python:torque-balance` | 4 | 2.9% |
| `python:pressure` | 3 | 2.1% |
| `python:circuit` | 3 | 2.1% |

**Computationally checked: 108 of 140 (77.1%).**

No item is marked `unchecked`.

### Structural checks

- Distinct stems: 121 of 140
- Items with a figure: 42
- Items with a per-distractor error note on every wrong choice: 140 of 140
- Items with picture choices: 20
- Explanations referencing a choice by letter: 0 (must be 0)

## Blind-solve passes

Non-computational items (reading, conceptual mechanical) are answered by an
independent solver that never sees the key. Every disagreement is resolved
before the item ships.

| Exam | Section | Items | Disagreements | Outcome |
|---|---|---|---|---|
| IBEW Local 701 Form A | Reading Comprehension | 36 | 0 | All 36 keys confirmed independently. One item (`e701a-read-013`) was reworded after the solver flagged its option set as loose, even though it had chosen the intended answer. See `docs/CORRECTIONS.md`. |
| UA 597, UA 130, EIAT, sign-analysis | all | 395 | — | **Not yet blind-solved.** Migration fidelity is verified (every key, choice set, stem and explanation matches the source), but the keys have not yet been independently re-derived. Tracked in `PLAN.md`. |

## Migration fidelity

`node scripts/migrate/verify-migration.js` re-reads each source file and
confirms, for every migrated item, that the correct choice's text, the whole
choice set, the stem and the explanation still match the source. It runs in
CI, so a future edit cannot silently change a migrated answer.

| Source | Items | Keys matching | Choice sets | Stems | Explanations |
|---|---|---|---|---|---|
| `UA-597-GAN-Aptitude-Practice-Exam.html` | 140 | 140 | 140 | 140 | 140 |
| the same file, section 7 (sign-analysis drill) | 15 | 15 | 15 | 15 | 15 |
| `ua-local-130-gan-practice-exam.html` | 140 | 140 | 140 | 140 | 140 |
| `eiat-practice-test (1).html` | 100 | 100 | 100 | 100 | 100 |

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
