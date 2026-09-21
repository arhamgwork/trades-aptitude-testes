// Dependency-free build: validates data, emits dist/ and dist/single/.
// Fails loudly rather than shipping a broken site.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { validateExam, loadExams, letterDist, walk } from './validate.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'src');
const DATA = path.join(ROOT, 'data');
const DIST = path.join(ROOT, 'dist');

const errors = [];
const warn = [];

function rmrf(p) { fs.rmSync(p, { recursive: true, force: true }); }
function mkdirp(p) { fs.mkdirSync(p, { recursive: true }); }

function copyTree(from, to) {
  mkdirp(to);
  for (const e of fs.readdirSync(from, { withFileTypes: true })) {
    const a = path.join(from, e.name);
    const b = path.join(to, e.name);
    if (e.isDirectory()) copyTree(a, b);
    else fs.copyFileSync(a, b);
  }
}

// ---------------------------------------------------------------- gate: JS syntax
function gateNodeCheck() {
  const files = [...walk(SRC), ...walk(path.join(ROOT, 'scripts'))]
    .filter((f) => f.endsWith('.js'));
  for (const f of files) {
    try {
      execFileSync(process.execPath, ['--check', f], { stdio: 'pipe' });
    } catch (e) {
      errors.push(`node --check failed: ${path.relative(ROOT, f)}\n${e.stderr?.toString() || ''}`);
    }
  }
  return files.length;
}

// ---------------------------------------------------------------- gate: no third-party
const ALLOWED_INLINE = [];   // nothing external is allowed at runtime
function gateNoThirdParty(dir) {
  const re = /(?:src|href)\s*=\s*["']([a-z]+:)?\/\/[^"']+["']/gi;
  const tracking = /(google-analytics|googletagmanager|gtag\(|doubleclick|facebook\.net|hotjar|segment\.io|mixpanel|sentry\.io|plausible|matomo)/i;
  for (const f of walk(dir)) {
    if (!/\.(html|js|css)$/.test(f)) continue;
    const txt = fs.readFileSync(f, 'utf8');
    let m;
    while ((m = re.exec(txt))) {
      if (ALLOWED_INLINE.some((a) => m[0].includes(a))) continue;
      errors.push(`${path.relative(ROOT, f)}: external resource reference: ${m[0].slice(0, 80)}`);
    }
    if (tracking.test(txt)) {
      errors.push(`${path.relative(ROOT, f)}: looks like tracking/analytics code`);
    }
  }
}

// ---------------------------------------------------------------- catalog
function buildCatalog(exams) {
  const tradesMeta = JSON.parse(fs.readFileSync(path.join(DATA, 'trades.json'), 'utf8'));
  const byTrade = {};
  for (const { exam } of exams) {
    (byTrade[exam.trade] = byTrade[exam.trade] || []).push({
      id: exam.id,
      title: exam.title,
      testName: exam.testName,
      confidence: exam.confidence,
      confidenceNote: exam.confidenceNote || '',
      calculatorAllowed: exam.calculatorAllowed,
      totalQuestions: exam.questions.length,
      totalMinutes: Math.round(
        exam.sections.reduce((a, s) => a + (s.timeLimitSec || 0), 0) / 60),
      sections: exam.sections.map((s) => ({
        id: s.id, name: s.name, questionCount: s.questionCount,
        timeLimitSec: s.timeLimitSec, timeConfirmed: s.timeConfirmed !== false,
      })),
    });
  }
  const trades = tradesMeta.trades.map((t) => ({ ...t, exams: byTrade[t.slug] || [] }));
  for (const slug of Object.keys(byTrade)) {
    if (!trades.find((t) => t.slug === slug)) {
      errors.push(`data/trades.json has no entry for trade "${slug}" used by an exam`);
    }
  }
  return { generatedAt: new Date().toISOString(), trades, pending: tradesMeta.pending || [] };
}

// ---------------------------------------------------------------- single-file exam
function singleFile(exam) {
  const css = fs.readFileSync(path.join(SRC, 'css', 'app.css'), 'utf8');
  const json = JSON.stringify(exam).replace(/</g, '\\u003c');
  const L = ['A', 'B', 'C', 'D', 'E'];
  const esc = (s) => String(s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  let body = '';
  let n = 0;
  const printed = new Set();
  for (const s of exam.sections) {
    body += `<h2 class="pagebreak">${esc(s.name)}</h2>`;
    body += `<p class="small muted">${s.questionCount} questions · ${Math.round((s.timeLimitSec || 0) / 60)} minutes</p>`;
    for (const q of exam.questions.filter((x) => x.section === s.id)) {
      n++;
      if (q.passageId && !printed.has(q.passageId)) {
        const p = (exam.passages || []).find((x) => x.id === q.passageId);
        if (p) {
          printed.add(p.id);
          body += `<div class="passage"><h3>${esc(p.title)}</h3>`;
          for (const para of p.text.split(/\n\s*\n/)) {
            body += `<p>${esc(para.replace(/\s*\n\s*/g, ' ').trim())}</p>`;
          }
          body += `</div>`;
        }
      }
      body += `<div class="printq"><p><strong>${n}.</strong> ${esc(q.stem)}</p>`;
      if (q.figure) body += `<figure class="fig">${q.figure}</figure>`;
      body += q.choices.map((c, i) => `<div class="small">${L[i]}. ${esc(c)}</div>`).join('');
      body += `</div>`;
    }
  }

  let key = '';
  let k = 0;
  for (const s of exam.sections) {
    key += `<h2>${esc(s.name)}</h2>`;
    for (const q of exam.questions.filter((x) => x.section === s.id)) {
      k++;
      key += `<div class="printq"><p><strong>${k}. ${L[q.correctIndex]}</strong> — ${esc(q.choices[q.correctIndex])}</p>`;
      key += `<p class="small">${esc(q.explanation)}</p><ul class="small muted">`;
      q.choices.forEach((c, i) => {
        if (i === q.correctIndex) return;
        key += `<li>${L[i]}: ${esc(q.distractorNotes[i] || '')}</li>`;
      });
      key += `</ul></div>`;
    }
  }

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(exam.title)} — offline copy</title>
<style>${css}</style>
</head>
<body>
<div class="wrap">
<p class="notice">Unofficial practice material, not affiliated with any union, JATC, or test publisher.</p>
<h1>${esc(exam.title)}</h1>
<p class="small muted">${esc(exam.testName)} · ${esc(exam.confidence)} · ${exam.calculatorAllowed ? 'calculator allowed' : 'no calculator'}</p>
<p class="small muted">Standalone offline copy: the booklet, then the answer key. Everything is in this one file, so it works with no network and no other files.</p>
<div class="btnrow noprint"><button onclick="window.print()">Print</button></div>
${body}
<h1 class="pagebreak">Answer key and explanations</h1>
${key}
</div>
<script type="application/json" id="exam-data">${json}</script>
</body>
</html>`;
}

// ---------------------------------------------------------------- main
function main() {
  const exams = loadExams(DATA);
  for (const { file, exam } of exams) validateExam(exam, file, errors);

  const jsCount = gateNodeCheck();
  gateNoThirdParty(SRC);

  if (!exams.length) warn.push('no exam data files found');

  if (errors.length) {
    console.error(`BUILD FAILED — ${errors.length} problem(s):`);
    errors.forEach((e) => console.error('  ' + e));
    process.exit(1);
  }

  rmrf(DIST);
  mkdirp(DIST);
  copyTree(SRC, DIST);

  // data: flatten exams to data/exams/<id>.json so the app can fetch by id
  mkdirp(path.join(DIST, 'data', 'exams'));
  for (const { exam } of exams) {
    fs.writeFileSync(
      path.join(DIST, 'data', 'exams', `${exam.id}.json`),
      JSON.stringify(exam), 'utf8');
  }
  const catalog = buildCatalog(exams);
  if (errors.length) {
    console.error('BUILD FAILED — catalog:');
    errors.forEach((e) => console.error('  ' + e));
    process.exit(1);
  }
  fs.writeFileSync(path.join(DIST, 'data', 'index.json'), JSON.stringify(catalog), 'utf8');

  // single-file offline copies
  mkdirp(path.join(DIST, 'single'));
  for (const { exam } of exams) {
    fs.writeFileSync(path.join(DIST, 'single', `${exam.id}.html`), singleFile(exam), 'utf8');
  }

  // a .nojekyll so GitHub Pages serves files beginning with underscores
  fs.writeFileSync(path.join(DIST, '.nojekyll'), '');

  // re-scan the emitted site
  gateNoThirdParty(DIST);
  if (errors.length) {
    console.error('BUILD FAILED — emitted site:');
    errors.forEach((e) => console.error('  ' + e));
    process.exit(1);
  }

  const totalQ = exams.reduce((a, { exam }) => a + exam.questions.length, 0);
  console.log(`build OK`);
  console.log(`  exams: ${exams.length}, questions: ${totalQ}`);
  console.log(`  js files checked: ${jsCount}`);
  for (const { exam } of exams) {
    const d = letterDist(exam);
    const parts = Object.entries(d.counts).sort()
      .map(([k, v]) => `${k}=${Math.round((v / d.total) * 100)}%`).join(' ');
    console.log(`  ${exam.id}: ${d.total} q, key spread ${parts}`);
  }
  warn.forEach((w) => console.log(`  note: ${w}`));
}

main();
