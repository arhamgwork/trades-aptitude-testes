// Confirms migration preserved every answer exactly.
// Re-reads the source HTML and checks that, for every migrated question, the
// text of the correct choice still matches the source's correct choice, that
// the full set of choices is unchanged, and that stems and explanations match.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readHTML, runScriptCapture, stripTags } from './extract.js';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const out = (p) => path.join(ROOT, p);
const norm = (s) => stripTags(String(s)).replace(/\s+/g, ' ').trim();
const normChoice = (s) => (/<svg[\s>]/i.test(String(s))
  ? String(s).replace(/\s+/g, ' ').trim()   // picture choice: compare markup
  : norm(s));

let problems = 0;
const fail = (m) => { problems++; console.log('  MISMATCH ' + m); };

function compare(label, sourceItems, migrated) {
  if (sourceItems.length !== migrated.length) {
    fail(`${label}: source has ${sourceItems.length} items, migrated has ${migrated.length}`);
    return;
  }
  let keysOk = 0, choicesOk = 0, stemsOk = 0, explOk = 0;
  for (let i = 0; i < sourceItems.length; i++) {
    const s = sourceItems[i];
    const m = migrated[i];
    const srcKey = normChoice(s.o[s.a]);
    const migKey = normChoice(m.choices[m.correctIndex]);
    if (srcKey !== migKey) {
      fail(`${label} #${i + 1} (${m.id}): key text changed\n      source: ${srcKey.slice(0, 90)}\n      built : ${migKey.slice(0, 90)}`);
    } else keysOk++;

    const srcSet = s.o.map(normChoice).slice().sort();
    const migSet = m.choices.map(normChoice).slice().sort();
    if (JSON.stringify(srcSet) !== JSON.stringify(migSet)) {
      fail(`${label} #${i + 1} (${m.id}): choice set changed`);
    } else choicesOk++;

    if (norm(s.stem) !== norm(m.stem)) {
      fail(`${label} #${i + 1} (${m.id}): stem changed\n      source: ${norm(s.stem).slice(0, 90)}\n      built : ${norm(m.stem).slice(0, 90)}`);
    } else stemsOk++;

    if (norm(s.e) !== norm(m.explanation)) {
      fail(`${label} #${i + 1} (${m.id}): explanation changed`);
    } else explOk++;
  }
  console.log(`  ${label}: ${keysOk}/${sourceItems.length} keys, ${choicesOk} choice sets, ${stemsOk} stems, ${explOk} explanations match source`);
}

const read = (p) => JSON.parse(fs.readFileSync(out(p), 'utf8'));

// ---- UA 597
{
  const src = readHTML(out('source-exams/UA-597-GAN-Aptitude-Practice-Exam.html'));
  const { data } = runScriptCapture(src, ['Q']);
  const exam = data.Q.filter((q) => q.s <= 6).map((q) => ({ o: q.o, a: q.a, stem: q.t, e: q.e }));
  compare('UA 597 exam', exam, read('data/pipefitting/ua-597-formA.json').questions);
  const drill = data.Q.filter((q) => q.s === 7).map((q) => ({ o: q.o, a: q.a, stem: q.t, e: q.e }));
  compare('sign-analysis drill', drill, read('data/drills/sign-analysis.json').questions);
}

// ---- UA 130
{
  const src = readHTML(out('source-exams/ua-local-130-gan-practice-exam.html'));
  const { data } = runScriptCapture(src, ['SECTIONS']);
  const items = [];
  for (const s of data.SECTIONS) for (const q of s.q) items.push({ o: q.o, a: q.a, stem: q.s, e: q.e });
  compare('UA 130 exam', items, read('data/plumbing/ua-130-formA.json').questions);
}

// ---- EIAT
{
  const src = readHTML(out('source-exams/eiat-practice-test (1).html'));
  const { data } = runScriptCapture(src, ['Q']);
  const items = Object.values(data.Q).sort((a, b) => a.n - b.n).map((q) => ({
    o: q.o, a: q.a,
    stem: [stripTags(q.q), q.m ? stripTags(q.m) : ''].filter(Boolean).join('  '),
    e: q.e,
  }));
  compare('EIAT exam', items, read('data/elevator/eiat-formA.json').questions);
}

console.log(problems ? `\nMIGRATION VERIFY FAILED (${problems})` : '\nmigration verified: every key, choice set, stem and explanation matches the source');
process.exit(problems ? 1 : 0);
