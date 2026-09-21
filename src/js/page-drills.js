import { el, $, qs, mountChrome, announce } from './util.js';
import { loadIndex, loadExam } from './catalog.js';
import { buildPlan, Run } from './runner.js';
import { renderResults } from './results.js';
import { enableOffline } from './offline.js';

const main = $('#main');
mountChrome('drills.html');
enableOffline();

const SKILL_GROUPS = [
  ['Numbers', ['arith.fractions', 'arith.decimals', 'arith.percent', 'ratio.proportion', 'arith.scientific', 'convert.units']],
  ['Geometry', ['geom.area', 'geom.volume', 'geom.perimeter']],
  ['Algebra and functions', ['algebra.linear', 'algebra.systems', 'algebra.exponents', 'algebra.polynomials', 'algebra.factoring', 'algebra.functions', 'algebra.graphs', 'algebra.inequalities', 'algebra.quadratic', 'algebra.rational', 'algebra.radicals', 'algebra.absolute', 'algebra.literal', 'algebra.variation', 'algebra.word']],
  ['Reasoning', ['series.arithmetic', 'series.geometric', 'series.alternating', 'sign.analysis', 'varrel.inequality', 'varrel.sufficiency', 'varrel.symbolic', 'varrel.ifthen']],
  ['Reading', ['reading.main-idea', 'reading.detail', 'reading.inference', 'reading.vocabulary', 'reading.purpose', 'reading.organization', 'reading.cloze']],
  ['Mechanical', ['mech.gears', 'mech.pulleys', 'mech.levers', 'mech.hydraulics', 'mech.circuits']],
  ['Spatial', ['spatial.folding', 'spatial.unfolding', 'spatial.rotation']],
  ['Rates', ['rate.work', 'rate.distance']],
];

let BANK = [];   // every question across the site, with its exam attached

loadAll().then(() => {
  const quick = qs('quick');
  const skills = (qs('skills') || '').split(',').filter(Boolean);
  if (quick && skills.length) startDrill(skills, Number(quick) || 10, 'Quick 10');
  else renderPicker();
}).catch((e) => {
  main.textContent = '';
  main.appendChild(el('p', { class: 'err', text: `Could not load the question banks: ${e.message}` }));
});

async function loadAll() {
  const idx = await loadIndex();
  const ids = idx.trades.flatMap((t) => (t.exams || []).map((e) => e.id));
  const exams = await Promise.all(ids.map((id) => loadExam(id).catch(() => null)));
  BANK = [];
  for (const ex of exams) {
    if (!ex) continue;
    for (const q of ex.questions) BANK.push({ q, exam: ex });
  }
}

function countsBySkill() {
  const c = {};
  for (const { q } of BANK) for (const s of q.skills || []) c[s] = (c[s] || 0) + 1;
  return c;
}

function renderPicker() {
  main.textContent = '';
  main.appendChild(el('h1', { text: 'Skill drills' }));
  main.appendChild(el('p', { class: 'lede', text: 'Untimed practice by skill, drawn from every exam on the site. Pick a skill, pick how many questions.' }));

  const counts = countsBySkill();
  const total = BANK.length;
  main.appendChild(el('p', { class: 'small muted', text: `${total} questions available across the site.` }));

  for (const [group, skills] of SKILL_GROUPS) {
    const avail = skills.filter((s) => counts[s]);
    if (!avail.length) continue;
    const card = el('div', { class: 'card' }, el('h2', { style: 'margin-top:0', text: group }));
    const row = el('div', { class: 'btnrow' });
    for (const s of avail) {
      row.appendChild(el('button', {
        text: `${s} (${counts[s]})`,
        onClick: () => renderCountChooser(s, counts[s]),
      }));
    }
    card.appendChild(row);
    main.appendChild(card);
  }

  const missing = SKILL_GROUPS.flatMap(([, s]) => s).filter((s) => !counts[s]);
  if (missing.length) {
    main.appendChild(el('div', { class: 'card' },
      el('h2', { style: 'margin-top:0', text: 'Planned drills' }),
      el('p', { class: 'small muted', text: 'These skill areas are in the plan but have no questions yet. They appear here rather than silently missing.' }),
      el('p', null, missing.map((s) => el('span', { class: 'tag', text: s })))));
  }
}

function renderCountChooser(skill, max) {
  main.textContent = '';
  main.appendChild(el('h1', { text: `Drill: ${skill}` }));
  main.appendChild(el('p', { class: 'lede', text: `${max} question${max === 1 ? '' : 's'} available. Drills are always untimed.` }));
  const form = el('form', { class: 'card' });
  const input = el('input', {
    type: 'number', id: 'n', min: '1', max: String(max), value: String(Math.min(10, max)),
    style: 'min-height:44px;padding:8px;border-radius:8px;border:1px solid var(--border);width:7em',
  });
  form.appendChild(el('p', null, el('label', { for: 'n' }, 'How many questions: '), input));
  form.appendChild(el('div', { class: 'btnrow' },
    el('button', { class: 'primary', type: 'submit', text: 'Start drill' }),
    ...[10, 20].filter((n) => n <= max).map((n) =>
      el('button', { type: 'button', text: `${n} questions`, onClick: () => startDrill([skill], n, `Drill: ${skill}`) })),
    el('button', { type: 'button', text: 'Back', onClick: renderPicker })));
  form.addEventListener('submit', (ev) => {
    ev.preventDefault();
    startDrill([skill], Math.max(1, Math.min(max, Number(input.value) || 10)), `Drill: ${skill}`);
  });
  main.appendChild(form);
}

function startDrill(skills, count, label) {
  const want = new Set(skills);
  const pool = BANK.filter(({ q }) => (q.skills || []).some((s) => want.has(s)));
  if (!pool.length) {
    main.textContent = '';
    main.appendChild(el('p', { class: 'err', text: 'There are no questions tagged with those skills yet.' }));
    main.appendChild(el('p', null, el('a', { href: 'drills.html', text: 'Back to skill drills' })));
    return;
  }
  // Rotate the starting point so repeat drills are not always the same items.
  const start = Math.floor(Math.random() * pool.length);
  const picked = [];
  for (let i = 0; i < Math.min(count, pool.length); i++) picked.push(pool[(start + i) % pool.length]);

  // A drill can span exams, so carry the passages the picked questions need.
  const passages = [];
  const seen = new Set();
  for (const { q, exam } of picked) {
    if (!q.passageId || seen.has(q.passageId)) continue;
    const p = (exam.passages || []).find((x) => x.id === q.passageId);
    if (p) { passages.push(p); seen.add(q.passageId); }
  }

  const pseudo = {
    id: `drill:${skills.join('+')}`,
    title: label,
    testName: 'Skill drill',
    confidence: 'CONFIRMED',
    calculatorAllowed: false,
    selfPaced: true,
    sections: [],
    passages,
    questions: picked.map(({ q }) => q),
  };
  const plan = buildPlan(pseudo, {
    mode: 'drill', timer: 'untimed', drillLabel: label,
    drillQuestions: pseudo.questions,
  });
  main.textContent = '';
  const host = el('div');
  main.appendChild(host);
  new Run(plan, host, (result) => {
    main.textContent = '';
    renderResults(result, pseudo, main, {
      footer: el('div', { class: 'btnrow noprint' },
        el('button', { class: 'primary', text: 'Another drill', onClick: renderPicker }),
        el('a', { class: 'btn', href: 'progress.html', text: 'Progress' }),
        el('a', { class: 'btn', href: 'index.html', text: 'Home' })),
    });
    announce(`Drill finished. Score ${result.pct} percent.`);
    window.scrollTo(0, 0);
  }).start();
  window.scrollTo(0, 0);
}
