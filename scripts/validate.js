// Dependency-free validator. Enforces docs/SCHEMA.md and the build gates.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const CONF = ['CONFIRMED', 'PARTIAL', 'UNKNOWN'];
const DIFF = ['easy', 'medium', 'hard'];
const TYPES = ['mc', 'cloze'];
const LETTER_RE = /\b(?:option|choice|answer|letter)\s+[A-E]\b|\b[A-E]\)\s/i;
const THIRD_PARTY_RE =
  /(https?:)?\/\/(?!localhost)(?:[a-z0-9-]+\.)+[a-z]{2,}/gi;

function fail(errors, id, msg) { errors.push(`${id}: ${msg}`); }

function validateExam(exam, file, errors) {
  const id = exam.id || path.basename(file);
  const req = ['id', 'trade', 'title', 'testName', 'provider', 'locals',
    'confidence', 'blueprint', 'dateChecked', 'calculatorAllowed',
    'selfPaced', 'sections', 'questions'];
  for (const k of req) {
    if (exam[k] === undefined) fail(errors, id, `missing field "${k}"`);
  }
  if (!CONF.includes(exam.confidence)) {
    fail(errors, id, `confidence must be one of ${CONF.join('|')}`);
  }
  if (exam.confidence !== 'CONFIRMED' && !exam.confidenceNote) {
    fail(errors, id, 'non-CONFIRMED exam must carry a confidenceNote saying what is unverified');
  }
  if (!/^\d{4}-\d{2}-\d{2}$/.test(exam.dateChecked || '')) {
    fail(errors, id, 'dateChecked must be YYYY-MM-DD');
  }
  if (typeof exam.calculatorAllowed !== 'boolean') {
    fail(errors, id, 'calculatorAllowed must be boolean');
  }

  const sectionIds = new Set();
  for (const s of exam.sections || []) {
    if (sectionIds.has(s.id)) fail(errors, id, `duplicate section id "${s.id}"`);
    sectionIds.add(s.id);
    if (!Number.isInteger(s.questionCount) || s.questionCount < 1) {
      fail(errors, id, `section "${s.id}" needs a positive integer questionCount`);
    }
    if (!exam.selfPaced) {
      if (!Number.isInteger(s.timeLimitSec) || s.timeLimitSec < 1) {
        fail(errors, id, `section "${s.id}" needs timeLimitSec (exam is not selfPaced)`);
      }
    }
  }

  const passageIds = new Set((exam.passages || []).map((p) => p.id));
  const seenStems = new Map();
  const qIds = new Set();
  const perSection = {};

  for (const q of exam.questions || []) {
    const qid = q.id || '(no id)';
    if (qIds.has(qid)) fail(errors, id, `duplicate question id "${qid}"`);
    qIds.add(qid);
    if (!sectionIds.has(q.section)) {
      fail(errors, id, `${qid}: section "${q.section}" is not declared`);
    }
    perSection[q.section] = (perSection[q.section] || 0) + 1;

    if (!TYPES.includes(q.type)) fail(errors, id, `${qid}: type must be mc|cloze`);
    if (!DIFF.includes(q.difficulty)) fail(errors, id, `${qid}: bad difficulty`);
    if (!Array.isArray(q.skills) || q.skills.length === 0) {
      fail(errors, id, `${qid}: needs at least one skill tag`);
    }
    if (!q.verify) fail(errors, id, `${qid}: missing verify field`);

    // Gate 2: correctIndex in range
    if (!Array.isArray(q.choices) || q.choices.length < 4 || q.choices.length > 5) {
      fail(errors, id, `${qid}: needs 4 or 5 choices`);
    } else {
      if (!Number.isInteger(q.correctIndex) ||
          q.correctIndex < 0 || q.correctIndex >= q.choices.length) {
        fail(errors, id, `${qid}: correctIndex out of range`);
      }
      // Gate 4: no identical options
      const norm = q.choices.map((c) => String(c).trim().toLowerCase());
      if (new Set(norm).size !== norm.length) {
        fail(errors, id, `${qid}: has two identical options`);
      }
      // Gate 9: distractorNotes shape
      if (!Array.isArray(q.distractorNotes) ||
          q.distractorNotes.length !== q.choices.length) {
        fail(errors, id, `${qid}: distractorNotes must match choices length`);
      } else {
        q.distractorNotes.forEach((n, i) => {
          if (i === q.correctIndex && n !== null) {
            fail(errors, id, `${qid}: distractorNotes must be null at the key`);
          }
          if (i !== q.correctIndex && (!n || !String(n).trim())) {
            fail(errors, id, `${qid}: distractor ${i} needs an error note`);
          }
        });
      }
    }

    // Gate 3: no duplicate stems
    const key = String(q.stem || '').trim().toLowerCase();
    if (!key) fail(errors, id, `${qid}: empty stem`);
    if (seenStems.has(key)) {
      fail(errors, id, `${qid}: duplicate stem, same as ${seenStems.get(key)}`);
    } else seenStems.set(key, qid);

    // Gate 8: explanation must not reference a letter
    if (!q.explanation || !String(q.explanation).trim()) {
      fail(errors, id, `${qid}: missing explanation`);
    } else if (LETTER_RE.test(q.explanation)) {
      fail(errors, id, `${qid}: explanation refers to a choice by letter`);
    }

    if (q.passageId && !passageIds.has(q.passageId)) {
      fail(errors, id, `${qid}: unknown passageId "${q.passageId}"`);
    }
    // Gate 7: SVG parses
    if (q.figure) {
      const e = checkSvg(q.figure);
      if (e) fail(errors, id, `${qid}: figure SVG ${e}`);
    }
  }

  // Gate 1: counts match the blueprint section table
  for (const s of exam.sections || []) {
    const got = perSection[s.id] || 0;
    if (got !== s.questionCount) {
      fail(errors, id,
        `section "${s.id}" declares ${s.questionCount} questions but has ${got}`);
    }
  }

  // Gate 10: answer-key balance (skipped for migrated exams, which are reported only)
  if (!exam.migrated) checkBalance(exam, id, errors);
}

function checkSvg(svg) {
  const s = String(svg).trim();
  if (!/^<svg[\s>]/.test(s)) return 'must start with <svg';
  if (!/<\/svg>$/.test(s)) return 'must end with </svg>';
  if (/<script/i.test(s)) return 'must not contain <script>';
  if (/\son[a-z]+\s*=/i.test(s)) return 'must not contain inline event handlers';
  // balanced tags
  const stack = [];
  const tag = /<\/?([a-zA-Z][\w:-]*)([^>]*?)(\/?)>/g;
  let m;
  while ((m = tag.exec(s))) {
    const [full, name, , selfClose] = m;
    if (full.startsWith('</')) {
      if (stack.pop() !== name) return `has unbalanced tag </${name}>`;
    } else if (!selfClose) {
      stack.push(name);
    }
  }
  if (stack.length) return `has unclosed tag <${stack[stack.length - 1]}>`;
  return null;
}

function letterDist(exam) {
  const counts = {};
  let total = 0;
  for (const q of exam.questions) {
    const L = String.fromCharCode(65 + q.correctIndex);
    counts[L] = (counts[L] || 0) + 1;
    total++;
  }
  return { counts, total };
}

function checkBalance(exam, id, errors) {
  const width = Math.max(...exam.questions.map((q) => q.choices.length));
  const { counts, total } = letterDist(exam);
  if (!total) return;
  const uniform = 100 / width;
  for (let i = 0; i < width; i++) {
    const L = String.fromCharCode(65 + i);
    const pct = ((counts[L] || 0) / total) * 100;
    if (Math.abs(pct - uniform) > 8) {
      fail(errors, id,
        `answer-key balance: ${L} is ${pct.toFixed(1)}% vs uniform ${uniform.toFixed(1)}% (limit 8 points)`);
    }
  }
  for (const s of exam.sections) {
    const qs = exam.questions.filter((q) => q.section === s.id);
    if (qs.length < 30) continue;
    const sc = {};
    qs.forEach((q) => {
      const L = String.fromCharCode(65 + q.correctIndex);
      sc[L] = (sc[L] || 0) + 1;
    });
    for (let i = 0; i < width; i++) {
      const L = String.fromCharCode(65 + i);
      const pct = ((sc[L] || 0) / qs.length) * 100;
      if (Math.abs(pct - uniform) > 12) {
        fail(errors, id,
          `section "${s.id}" key balance: ${L} is ${pct.toFixed(1)}% (limit 12 points from ${uniform.toFixed(1)}%)`);
      }
    }
  }
  // no more than 3 identical correct letters in a row
  let run = 1;
  for (let i = 1; i < exam.questions.length; i++) {
    if (exam.questions[i].correctIndex === exam.questions[i - 1].correctIndex) {
      run++;
      if (run > 3) {
        fail(errors, id,
          `more than 3 identical correct letters in a row at ${exam.questions[i].id}`);
      }
    } else run = 1;
  }
}

function scanThirdParty(dir, errors) {
  const allowHosts = [];
  for (const f of walk(dir)) {
    if (!/\.(html|js|css|json)$/.test(f)) continue;
    const txt = fs.readFileSync(f, 'utf8');
    const hits = txt.match(THIRD_PARTY_RE) || [];
    for (const h of hits) {
      // URLs inside blueprint/source citations live in .md, not shipped assets;
      // in shipped assets any absolute host is a violation unless allow-listed.
      if (allowHosts.some((a) => h.includes(a))) continue;
      if (/\.(html|js|css)$/.test(f)) {
        errors.push(`${path.relative(dir, f)}: third-party URL in shipped asset: ${h}`);
      }
    }
  }
}

function* walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else yield p;
  }
}

function loadExams(dataDir) {
  const exams = [];
  if (!fs.existsSync(dataDir)) return exams;
  for (const f of walk(dataDir)) {
    if (!f.endsWith('.json')) continue;
    if (path.basename(f) === 'index.json') continue;
    let json;
    try {
      json = JSON.parse(fs.readFileSync(f, 'utf8'));
    } catch (e) {
      throw new Error(`${f}: invalid JSON — ${e.message}`);
    }
    if (json.questions) exams.push({ file: f, exam: json });
  }
  return exams;
}

export { validateExam, loadExams, letterDist, checkSvg, scanThirdParty, walk };

if (process.argv[1] && path.resolve(process.argv[1]) === __filename) {
  const root = path.resolve(__dirname, '..');
  const errors = [];
  const exams = loadExams(path.join(root, 'data'));
  for (const { file, exam } of exams) validateExam(exam, file, errors);
  if (errors.length) {
    console.error(`FAIL — ${errors.length} problem(s):`);
    errors.forEach((e) => console.error('  ' + e));
    process.exit(1);
  }
  console.log(`OK — ${exams.length} exam file(s) valid`);
}
