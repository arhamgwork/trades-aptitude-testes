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
