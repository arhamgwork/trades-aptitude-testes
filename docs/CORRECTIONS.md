# Corrections log

Every content change made to migrated material, and every conflict found
between the project brief and official sources, is recorded here. Nothing is
changed silently.

Format: date — what was believed — what was found — what was done.

---

## 2026-09-21 — IBEW Local 134 test format (OPEN, not yet changed)

**Believed (project brief):** IBEW Local 134 (Cook County) uses the GAN
battery; IBEW Local 701 (DuPage) uses the ETA/NJATC two-section format.

**Found:** The Local 701 half is confirmed — DuPage JATC publishes "Part I
Algebra, Part II Reading Comprehension", matching the Electrical Training
Alliance test (33 q / 46 min + 36 q / 51 min, stanine 1-9).

The Local 134 half could not be confirmed and the evidence is genuinely
mixed. EJATT publishes no format. GAN's own site lists "electricians" among
the Chicagoland trades it tests, and EJATT hands out a study guide at
registration (GAN sells one; ETA's is free online) — both consistent with
GAN. Against that, EJATT is an IBEW 134 + NECA trust and IBEW/NECA JATCs
nationally use the ETA test.

**Done:** Nothing changed. Flagged to the user at the Phase 0 gate. The
Local 134 blueprint is marked PARTIAL and documents both possibilities and
the resolution path. No Local 134 exam will be built until this is settled.

---

## 2026-09-21 — `source-exams/` not present

**Believed (project brief):** `./source-exams/` contains four previously
built single-file HTML exams to be migrated exactly.

**Found:** The repository has no commits and no files at all. The remote has
zero branches. No `source-exams/` directory, and no matching HTML files,
exist anywhere on the machine.

**Done:** Nothing invented or substituted. Raised with the user at the
Phase 0 gate.

---

## 2026-09-21 — decisions taken at the Phase 0 gate

- **`source-exams/`:** user will re-upload the folder. No substitute exams
  will be written for the four migrated trades in the meantime; they remain
  blocked rather than regenerated.
- **IBEW Local 134:** build **both** variants (ETA-format and GAN-format),
  each badged PARTIAL, with the unresolved question shown on the trade page.
  Neither is presented as the confirmed format.

---

## 2026-09-21 — IBEW 701 Form A, item e701a-read-013 reworded

**Found by:** blind-solve verification pass (independent solver, key withheld).

The solver chose the intended answer, so the key was not wrong. It flagged the
options as loose: the correct choice glossed "donates" as "gives up without
being directed to", which is imprecise, while the distractor "lends on the
condition that it be returned" drew partial support from the passage's later
mention of restoring spent reserves.

**Done:** key reworded to "contributes automatically, without being commanded";
the repayment distractor reworded and its error note now explains that
restoring reserves is a separate control action, not a condition on the
inertial contribution. No key changed position.

## 2026-09-21 — IBEW 701 Form A, three duplicate distractors fixed at build time

The item builder refuses two choices that render identically. It caught three
items where two distractors encoded different mistakes that happened to produce
the same value (slope item, absolute-value item, mixture item). Each had one
distractor replaced with a distinct, real error mode. No key was affected.

---

## 2026-09-21 — `source-exams/` arrived; four exams migrated

The user re-uploaded the source files. All four were found and migrated. No
substitute was ever written. Files are now in `source-exams/`.

**Counts, taken from the sources themselves rather than assumed:**

| Exam | Sections | Items | Minutes |
|---|---|---|---|
| UA 597 (pipefitters) | 6 | 140 | 112 |
| UA 130 (plumbers) | 6 | 140 | 119 |
| EIAT (elevator) | 3 | 100 | 90 |
| Sign-analysis drill (was section 7 of the 597 file) | 1 | 15 | untimed |

The IBEW/GAN file the brief described as "Local 134 / GAN, 6 sections plus a
sign-analysis drill" turned out to be the **UA 597** file, whose seventh
section is that drill. It has been migrated as the 597 exam plus a separate
cross-trade sign-analysis drill set. There is no separate Local 134 exam in the
sources; the two Local 134 variants agreed at the Phase 0 gate are still to be
built.

**Verified:** `node scripts/migrate/verify-migration.js` re-reads each source
and confirms, for all 395 migrated items, that the correct choice's text, the
full choice set, the stem and the explanation all still match the source.

## 2026-09-21 — content-corruption bug found and fixed during migration

The tag stripper treated a bare `<` in mathematics as the start of an HTML tag,
so the sign-analysis stem `If x < 0 and y > 0, then x × y is` was being stored
as `If x 0, then x × y is`. Caught by the migration verifier, not by eye.

**Done:** the stripper now requires a tag name immediately after the angle
bracket. Re-migrated and re-verified; the stem is stored correctly and no
migrated item contains residual HTML.

## 2026-09-21 — answer-key order rebalanced on three migrated exams

Per the brief, migrated choice order is kept and only reported unless it falls
outside the limits. Three did, so they were rebalanced with a deterministic
seeded assignment. Rebalancing moves a key's position only; the correct text,
the choice set, the stem and the explanation are unchanged, and the migration
verifier above re-confirms that after every rebuild.

| Exam | Worst deviation before | After | Longest identical-letter run |
|---|---|---|---|
| EIAT | 69.3 points (reading was 94% A) | 10.0 | 32 → 3 |
| UA 597 | 35.0 points | 3.0 | 6 → 3 |
| Sign-analysis drill | 25.0 points (C never correct) | 5.0 | 3 → 3 |

**UA 130 was left exactly as authored** — its distribution was already inside
the limits (worst 12.9 points) with a longest run of 3.

No explanation in any migrated exam refers to a choice by letter, so
rebalancing could not break one; the build gate re-checks this.

Terminal options that are part of the real format — EIAT's "No answer" and
UA 130's "None of these", both always last — are pinned and never moved. Where
such an option is itself the correct answer, that key is left in place.
