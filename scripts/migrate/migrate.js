// Migrates the single-file source exams into data/<trade>/<exam>.json.
// Content, choice order and answer keys are preserved exactly; nothing is
// regenerated. Items arrive as verify:"unchecked" and are upgraded by the
// verification passes in scripts/verify/.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readHTML, runScriptCapture, stripTags } from './extract.js';
import { rebalanceExam, distribution, fixGlobalRuns } from './rebalance.js';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const out = (p) => path.join(ROOT, p);

const rebalanced = [];

function writeExam(rel, exam) {
  // Migrated content keeps its authored choice order unless the key
  // distribution breaks the limits; then it is rebalanced and logged.
  const before = distribution(exam);
  if (before.needsWork) {
    const moved = rebalanceExam(exam, `${exam.id}-rebalance-v1`);
    fixGlobalRuns(exam, 3);
    const after = distribution(exam);
    rebalanced.push({ id: exam.id, moved, before, after });
    exam.keyOrderRebalanced = true;
  } else {
    exam.keyOrderRebalanced = false;
  }
  const f = out(rel);
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, JSON.stringify(exam, null, 1), 'utf8');
  const bySec = {};
  for (const q of exam.questions) bySec[q.section] = (bySec[q.section] || 0) + 1;
  console.log(`  wrote ${rel}: ${exam.questions.length} items ${JSON.stringify(bySec)}`);
}

/**
 * Keep the source's figure markup as authored. Some figures are a single
 * <svg>, others are a fold sequence: several <svg> panels inside a layout
 * wrapper. Both are preserved; the validator checks they are balanced and
 * carry no script or event handlers.
 */
function figureOf(html) {
  if (!html) return null;
  const s = String(html).trim();
  return /<svg[\s>]/i.test(s) ? s : null;
}

/** True when a question's choices are pictures rather than text. */
function figureChoices(opts) {
  return opts.some((o) => /<svg[\s>]/i.test(String(o)));
}

/** Text choices get tags stripped; picture choices are kept as markup. */
function mapChoices(opts) {
  const asFigures = figureChoices(opts);
  return {
    choices: asFigures ? opts.map((o) => String(o).trim()) : opts.map(stripTags),
    choicesAreFigures: asFigures,
  };
}

const nullNotes = (n) => Array(n).fill(null);

// ============================================================ UA 597
function migrate597() {
  const src = readHTML(out('source-exams/UA-597-GAN-Aptitude-Practice-Exam.html'));
  const { data, errors } = runScriptCapture(src, ['Q', 'SECTIONS']);
  if (errors.length) throw new Error(`597 script errors: ${errors[0]}`);
  const SKILLS = {
    1: ['arith.fractions', 'arith.decimals', 'arith.percent'],
    2: ['series.arithmetic'],
    3: ['algebra.word', 'ratio.proportion', 'convert.units'],
    4: ['reading.detail', 'reading.inference'],
    5: ['mech.gears', 'mech.pulleys', 'mech.levers'],
    6: ['spatial.folding'],
  };
  const sections = data.SECTIONS.map((s) => ({
    id: `s${s.id}`, name: s.name, questionCount: s.n,
    timeLimitSec: s.mins * 60, timeConfirmed: false,
  }));
  const questions = data.Q.filter((q) => q.s <= 6).map((q, i) => ({
    id: `ua597a-${String(i + 1).padStart(3, '0')}`,
    section: `s${q.s}`,
    skills: q.tag ? [tagSkill(q.tag)] : SKILLS[q.s],
    type: 'mc',
    stem: stripTags(q.t),
    figure: figureOf(q.fig),
    passageId: null,
    ...mapChoices(q.o),
    correctIndex: q.a,
    explanation: stripTags(q.e),
    distractorNotes: nullNotes(q.o.length),
    difficulty: 'medium',
    verify: 'unchecked',
  }));
  writeExam('data/pipefitting/ua-597-formA.json', {
    id: 'ua-597-formA', trade: 'pipefitting',
    title: 'UA Local 597 (Pipefitters) — GAN Battery Practice Exam, Form A',
    testName: 'GAN Aptitude Battery', provider: 'GAN Human Resources',
    locals: ['UA Pipefitters Local 597 (Chicago)'],
    confidence: 'PARTIAL',
    confidenceNote: 'GAN is confirmed as the testing company by Local 597, and the section names come from the local’s own site. GAN does not publish per-section question counts or time limits, so the split used here is the one this exam was built with, not an official figure.',
    blueprint: 'docs/blueprints/pipefitting-ua-597.md',
    dateChecked: '2026-09-21',
    calculatorAllowed: false, selfPaced: false,
    migrated: true, migratedFrom: 'UA-597-GAN-Aptitude-Practice-Exam.html',
    sections, passages: [], questions,
  });

  // section 7 is the sign-analysis drill, not part of the battery
  const drill = data.Q.filter((q) => q.s === 7).map((q, i) => ({
    id: `sign-${String(i + 1).padStart(3, '0')}`,
    section: 'sign', skills: ['sign.analysis'], type: 'mc',
    stem: stripTags(q.t), figure: figureOf(q.fig), passageId: null,
    ...mapChoices(q.o), correctIndex: q.a,
    explanation: stripTags(q.e), distractorNotes: nullNotes(q.o.length),
    difficulty: 'medium', verify: 'unchecked',
  }));
  writeExam('data/drills/sign-analysis.json', {
    id: 'sign-analysis', trade: 'drills',
    title: 'Sign analysis — how one variable moves when another changes',
    testName: 'Skill drill', provider: 'This site',
    locals: [], confidence: 'CONFIRMED', confidenceNote: '',
    blueprint: 'docs/blueprints/_gan-battery.md', dateChecked: '2026-09-21',
    calculatorAllowed: false, selfPaced: true,
    migrated: true, migratedFrom: 'UA-597-GAN-Aptitude-Practice-Exam.html',
    sections: [{ id: 'sign', name: 'Sign analysis', questionCount: drill.length, timeLimitSec: null }],
    passages: [], questions: drill,
  });
}

function tagSkill(tag) {
  const map = {
    sign: 'sign.analysis', frac: 'arith.fractions', series: 'series.arithmetic',
    gear: 'mech.gears', pulley: 'mech.pulleys', lever: 'mech.levers',
    fold: 'spatial.folding', read: 'reading.detail',
  };
  return map[tag] || `source.${tag}`;
}

/**
 * The Numerical Reasoning items carry their question as a `ser` array of terms
 * rather than a stem string, and the source renders them as the series
 * followed by "Which number continues the series?".
 */
function stemOf130(q) {
  if (Array.isArray(q.ser) && q.ser.length) {
    return `Which number continues the series?   ${q.ser.map(stripTags).join(', ')}, ?`;
  }
  return stripTags(q.s);
}

// ============================================================ UA 130
function migrate130() {
  const src = readHTML(out('source-exams/ua-local-130-gan-practice-exam.html'));
  const { data, errors } = runScriptCapture(src, ['SECTIONS', 'PASSAGES']);
  if (errors.length) throw new Error(`130 script errors: ${errors[0]}`);
  const SKILLS = {
    read: ['reading.detail', 'reading.inference'],
    comp: ['arith.fractions', 'arith.decimals', 'arith.percent'],
    reas: ['series.arithmetic'],
    solve: ['algebra.word', 'ratio.proportion', 'convert.units'],
    fold: ['spatial.folding'],
    mech: ['mech.gears', 'mech.pulleys', 'mech.levers'],
  };
  const sections = data.SECTIONS.map((s) => ({
    id: s.id, name: s.name, questionCount: s.count,
    timeLimitSec: s.mins * 60, timeConfirmed: false,
  }));
  const passages = Object.entries(data.PASSAGES).map(([id, p]) => ({
    id, title: stripTags(p.t), text: p.b.map(stripTags).join('\n\n'),
  }));
  const questions = [];
  for (const s of data.SECTIONS) {
    s.q.forEach((q, i) => {
      questions.push({
        id: `ua130a-${s.id}-${String(i + 1).padStart(3, '0')}`,
        section: s.id, skills: SKILLS[s.id] || ['general'], type: 'mc',
        stem: stemOf130(q), figure: figureOf(q.fig || q.f),
        passageId: q.p || null,
        ...mapChoices(q.o), correctIndex: q.a,
        explanation: stripTags(q.e), distractorNotes: nullNotes(q.o.length),
        difficulty: 'medium', verify: 'unchecked',
      });
    });
  }
  writeExam('data/plumbing/ua-130-formA.json', {
    id: 'ua-130-formA', trade: 'plumbing',
    title: 'UA Local 130 (Plumbers) — GAN Battery Practice Exam, Form A',
    testName: 'GAN Aptitude Battery', provider: 'GAN Human Resources',
    locals: ['UA Plumbers Local 130 (Chicago)'],
    confidence: 'PARTIAL',
    confidenceNote: 'GAN is confirmed as the testing company for Local 130. GAN does not publish per-section question counts or time limits; the 140 items in 119 minutes used here match what this exam was built with, and the Reading (42 items / 25 minutes) and Problem Solving (35 / 35) figures agree with independent prep sources, but none of it is an official published figure.',
    blueprint: 'docs/blueprints/plumbing-ua-130.md',
    dateChecked: '2026-09-21',
    calculatorAllowed: false, selfPaced: false,
    migrated: true, migratedFrom: 'ua-local-130-gan-practice-exam.html',
    sections, passages, questions,
  });
}

// ============================================================ EIAT
function migrateEIAT() {
  const src = readHTML(out('source-exams/eiat-practice-test (1).html'));
  const { data, errors } = runScriptCapture(src, ['Q', 'SEC', 'READING']);
  if (errors.length) throw new Error(`EIAT script errors: ${errors[0]}`);
  const secIds = ['read', 'mech', 'math'];
  const secSkills = {
    read: ['reading.cloze'],
    mech: ['mech.gears', 'mech.pulleys', 'mech.levers', 'mech.hydraulics'],
    math: ['arith.fractions', 'arith.percent', 'algebra.linear'],
  };
  const sections = data.SEC.map((s, i) => ({
    id: secIds[i],
    name: stripTags(s.name),
    questionCount: s.last - s.first + 1,
    timeLimitSec: s.secs,
    timeConfirmed: false,
  }));

  // Cloze passages, with the numbered blanks kept as written.
  const passages = data.READING.map((p, i) => ({
    id: `eiat-p${i + 1}`, title: stripTags(p.title), text: stripTags(p.text),
  }));
  // map question number -> passage id
  const qToPassage = {};
  let n = 0;
  data.READING.forEach((p, i) => {
    p.qs.forEach(() => { n++; qToPassage[n] = `eiat-p${i + 1}`; });
  });

  const questions = Object.values(data.Q)
    .sort((a, b) => a.n - b.n)
    .map((q) => {
      const sid = secIds[q.s];
      const stem = [stripTags(q.q), q.m ? stripTags(q.m) : ''].filter(Boolean).join('  ');
      return {
        id: `eiat-a-${String(q.n).padStart(3, '0')}`,
        section: sid,
        skills: secSkills[sid],
        type: sid === 'read' ? 'cloze' : 'mc',
        stem,
        figure: figureOf(q.d),
        passageId: sid === 'read' ? (qToPassage[q.n] || null) : null,
        ...mapChoices(q.o),
        correctIndex: q.a,
        explanation: stripTags(q.e),
        distractorNotes: nullNotes(q.o.length),
        difficulty: 'medium',
        verify: 'unchecked',
      };
    });

  writeExam('data/elevator/eiat-formA.json', {
    id: 'eiat-formA', trade: 'elevator',
    title: 'Elevator Constructor (EIAT) — Practice Exam, Form A',
    testName: 'Elevator Industry Aptitude Test (EIAT)',
    provider: 'National Elevator Industry Educational Program (NEIEP)',
    locals: ['IUEC locals, including Local 2 (Chicago)'],
    confidence: 'PARTIAL',
    confidenceNote: 'The three sections and the 35 / 35 / 30 split are confirmed against the NEIEP 2024 study guide. NEIEP does not publish per-section time limits; the 25 / 25 / 40 minute split used here is the one preparation courses consistently report and is derived, not official.',
    blueprint: 'docs/blueprints/elevator-eiat.md',
    dateChecked: '2026-09-21',
    calculatorAllowed: false, selfPaced: false,
    migrated: true, migratedFrom: 'eiat-practice-test (1).html',
    sections, passages, questions,
  });
}

console.log('migrating source exams (content preserved exactly):');
migrate597();
migrate130();
migrateEIAT();
if (rebalanced.length) {
  console.log('\nrebalanced (authored key order was outside the limits):');
  for (const r of rebalanced) {
    console.log(`  ${r.id}: moved ${r.moved} keys; longest run ${r.before.maxRun} -> ${r.after.maxRun}`);
    for (const row of r.after.rows) {
      const b = r.before.rows.find((x) => x.group === row.group);
      console.log(`    ${row.group.padEnd(12)} n=${String(row.n).padEnd(4)} worst ${b.worst.toFixed(1)} -> ${row.worst.toFixed(1)} (limit ${row.limit})${row.over ? '  STILL OVER' : ''}`);
    }
  }
}
console.log('done');
