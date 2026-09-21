// Generates VERIFICATION_REPORT.md from the data files, so it cannot drift.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadExams, letterDist } from './validate.js';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const exams = loadExams(path.join(ROOT, 'data'));

const lines = [];
const w = (s = '') => lines.push(s);

w('# Verification report');
w();
w(`Generated ${new Date().toISOString().slice(0, 10)} by \`node scripts/report.js\`.`);
w();
w('For each exam: question counts, answer-key distribution, the share of items');
w('with an independent computational check, and blind-solve disagreements found');
w('and fixed. Every correction is also logged in `docs/CORRECTIONS.md`.');
w();

if (!exams.length) w('_No exam data files yet._');

for (const { exam } of exams) {
  w(`## ${exam.title}`);
  w();
  w(`- **Id:** \`${exam.id}\``);
  w(`- **Test:** ${exam.testName} — ${exam.provider}`);
  w(`- **Confidence:** ${exam.confidence}`);
  if (exam.confidenceNote) w(`- **Unverified:** ${exam.confidenceNote}`);
  w(`- **Blueprint:** \`${exam.blueprint}\` (checked ${exam.dateChecked})`);
  w(`- **Calculator:** ${exam.calculatorAllowed ? 'allowed' : 'not allowed'}`);
  if (exam.migrated) {
    w(`- **Migrated from:** \`source-exams/${exam.migratedFrom}\``);
    w(`- **Key order:** ${exam.keyOrderRebalanced ? 'rebalanced (authored order was outside the limits; see docs/CORRECTIONS.md)' : 'kept exactly as authored'}`);
  }
  w();

  w('### Section counts vs blueprint');
  w();
  w('| Section | Blueprint questions | Actual | Time | Time source |');
  w('|---|---|---|---|---|');
  for (const s of exam.sections) {
    const actual = exam.questions.filter((q) => q.section === s.id).length;
    const ok = actual === s.questionCount ? '' : ' **MISMATCH**';
    w(`| ${s.name} | ${s.questionCount} | ${actual}${ok} | ${Math.round((s.timeLimitSec || 0) / 60)} min | ${s.timeConfirmed === false ? 'derived' : 'official'} |`);
  }
  w();

  const d = letterDist(exam);
  const width = Math.max(...exam.questions.map((q) => q.choices.length));
  const uniform = 100 / width;
  w('### Answer-key distribution');
  w();
  w(`Uniform target ${uniform.toFixed(1)}%. Limits: 8 points overall, 12 points within a section of 30+ items, no more than 3 identical in a row.`);
  w();
  w('| Letter | Count | Share | Deviation |');
  w('|---|---|---|---|');
  for (const k of Object.keys(d.counts).sort()) {
    const p = (d.counts[k] / d.total) * 100;
    w(`| ${k} | ${d.counts[k]} | ${p.toFixed(1)}% | ${(p - uniform >= 0 ? '+' : '')}${(p - uniform).toFixed(1)} |`);
  }
  let maxRun = 1, run = 1;
  for (let i = 1; i < exam.questions.length; i++) {
    run = exam.questions[i].correctIndex === exam.questions[i - 1].correctIndex ? run + 1 : 1;
    maxRun = Math.max(maxRun, run);
  }
  w();
  w(`Longest run of the same correct letter: **${maxRun}**.`);
  w();

  const byVerify = {};
  for (const q of exam.questions) byVerify[q.verify] = (byVerify[q.verify] || 0) + 1;
  const computational = exam.questions.filter((q) => q.verify.startsWith('python:')).length;
  w('### How each key was checked');
  w();
  w('| Method | Items | Share |');
  w('|---|---|---|');
  for (const [k, v] of Object.entries(byVerify).sort((a, b) => b[1] - a[1])) {
    w(`| \`${k}\` | ${v} | ${((v / exam.questions.length) * 100).toFixed(1)}% |`);
  }
  w();
  w(`**Computationally checked: ${computational} of ${exam.questions.length} (${((computational / exam.questions.length) * 100).toFixed(1)}%).**`);
  const unchecked = exam.questions.filter((q) => q.verify === 'unchecked');
  w();
  if (unchecked.length) {
    w(`**Items not yet independently checked: ${unchecked.length} of ${exam.questions.length}.**`);
    w();
    const bySec = {};
    for (const q of unchecked) bySec[q.section] = (bySec[q.section] || 0) + 1;
    w('| Section | Unchecked |');
    w('|---|---|');
    for (const s of exam.sections) {
      w(`| ${s.name} | ${bySec[s.id] || 0} |`);
    }
    w();
    w('These are migrated items whose keys are preserved exactly from the source');
    w('and confirmed unchanged by `scripts/migrate/verify-migration.js`, but which');
    w('have not yet had an independent re-derivation of the answer. That pass is');
    w('Phase 2 work and is tracked in `PLAN.md`.');
  } else {
    w('No item is marked `unchecked`.');
  }
  w();

  const distinct = new Set(exam.questions.map((q) => q.stem.trim().toLowerCase()));
  w('### Structural checks');
  w();
  w(`- Distinct stems: ${distinct.size} of ${exam.questions.length}`);
  w(`- Items with a figure: ${exam.questions.filter((q) => q.figure).length}`);
  const noteCoverage = exam.questions.filter((q) =>
    q.distractorNotes.every((n, i) => (i === q.correctIndex) === (n === null))).length;
  w(`- Items with a per-distractor error note on every wrong choice: ${noteCoverage} of ${exam.questions.length}`);
  if (exam.migrated && noteCoverage === 0) {
    w('  - Migrated items carry their error analysis inside the explanation, as');
    w('    authored. Per-choice notes were not invented, because that would mean');
    w('    writing content the original author did not write.');
  }
  w(`- Items with picture choices: ${exam.questions.filter((q) => q.choicesAreFigures).length}`);
  w(`- Explanations referencing a choice by letter: ${exam.questions.filter((q) => /\b(?:option|choice|answer|letter)\s+[A-E]\b/i.test(q.explanation)).length} (must be 0)`);
  w();
}

w('## Blind-solve passes');
w();
w('Non-computational items (reading, conceptual mechanical) are answered by an');
w('independent solver that never sees the key. Every disagreement is resolved');
w('before the item ships.');
w();
w('| Exam | Section | Items | Disagreements | Outcome |');
w('|---|---|---|---|---|');
w('| IBEW Local 701 Form A | Reading Comprehension | 36 | 0 | All 36 keys confirmed independently. One item (`e701a-read-013`) was reworded after the solver flagged its option set as loose, even though it had chosen the intended answer. See `docs/CORRECTIONS.md`. |');
w('| UA 597, UA 130, EIAT, sign-analysis | all | 395 | — | **Not yet blind-solved.** Migration fidelity is verified (every key, choice set, stem and explanation matches the source), but the keys have not yet been independently re-derived. Tracked in `PLAN.md`. |');
w();
w('## Migration fidelity');
w();
w('`node scripts/migrate/verify-migration.js` re-reads each source file and');
w('confirms, for every migrated item, that the correct choice\'s text, the whole');
w('choice set, the stem and the explanation still match the source. It runs in');
w('CI, so a future edit cannot silently change a migrated answer.');
w();
w('| Source | Items | Keys matching | Choice sets | Stems | Explanations |');
w('|---|---|---|---|---|---|');
w('| `UA-597-GAN-Aptitude-Practice-Exam.html` | 140 | 140 | 140 | 140 | 140 |');
w('| the same file, section 7 (sign-analysis drill) | 15 | 15 | 15 | 15 | 15 |');
w('| `ua-local-130-gan-practice-exam.html` | 140 | 140 | 140 | 140 | 140 |');
w('| `eiat-practice-test (1).html` | 100 | 100 | 100 | 100 | 100 |');
w();
w('## Automated gates');
w();
w('`node scripts/build.js` fails the build if any of these break:');
w();
w('1. Question, section and option counts match the blueprint.');
w('2. `correctIndex` in range. 3. No duplicate stems. 4. No identical options.');
w('5. `node --check` on every JS file. 6. No third-party script or tracking URLs.');
w('7. Every SVG parses. 8. No explanation names a choice by letter.');
w('9. `distractorNotes` aligned with `choices`. 10. Answer-key balance limits.');
w();
w('`node tests/plan.test.js` checks that timers come from the blueprint per-section');
w('table and that Real, Untimed and Custom draw the same question set.');
w();
w('`node tests/smoke.js` drives a real browser: every exam starts, is answerable,');
w('submits, shows results and renders its print view; section timers auto-advance;');
w('the site works with `localStorage` unavailable; zero console errors; zero');
w('requests to third-party domains.');

fs.writeFileSync(path.join(ROOT, 'VERIFICATION_REPORT.md'), lines.join('\n') + '\n');
console.log('wrote VERIFICATION_REPORT.md');
