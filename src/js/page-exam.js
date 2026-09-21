import { el, $, qs, mountChrome, fmtDuration, announce } from './util.js';
import { loadExam, findExamMeta } from './catalog.js';
import { buildPlan, Run } from './runner.js';
import { renderResults } from './results.js';
import * as store from './store.js';
import { enableOffline } from './offline.js';

const main = $('#main');
mountChrome(null);
enableOffline();

const examId = qs('exam');
const mode = qs('mode', 'full');
const section = qs('section');

main.textContent = '';
if (!examId) {
  main.appendChild(el('p', { class: 'err', text: 'No exam was specified in the address.' }));
} else {
  init().catch((e) => {
    main.textContent = '';
    main.appendChild(el('h1', { text: 'Could not load this exam' }));
    main.appendChild(el('p', { class: 'err', text: e.message }));
    main.appendChild(el('p', { class: 'small muted', text: 'The question bank is loaded from this site, so this usually means the page was opened from a file instead of a web address.' }));
  });
}

async function init() {
  const exam = await loadExam(examId);
  const meta = await findExamMeta(examId).catch(() => null);
  document.title = `${exam.title} — practice exam`;
  renderSetup(exam, meta);
}

function renderSetup(exam, meta) {
  main.textContent = '';
  main.appendChild(el('h1', { text: exam.title }));
  main.appendChild(el('p', { class: 'lede' },
    exam.testName, ' · ', el('span', { class: `badge ${exam.confidence}`, text: exam.confidence })));

  if (exam.confidence !== 'CONFIRMED' && exam.confidenceNote) {
    main.appendChild(el('p', { class: 'notice' },
      el('strong', null, 'What is not confirmed: '), exam.confidenceNote));
  }

  const secList = exam.sections.map((s) =>
    el('li', null, `${s.name} — ${s.questionCount} questions, `,
      s.timeLimitSec ? fmtDuration(s.timeLimitSec) : 'untimed',
      s.timeConfirmed === false ? el('span', { class: 'tag', text: 'time derived' }) : null));
  main.appendChild(el('div', { class: 'card' },
    el('h2', { style: 'margin-top:0', text: 'Format' }),
    el('ul', null, secList),
    el('p', { class: 'small muted' },
      exam.calculatorAllowed
        ? 'A calculator is allowed on this test.'
        : 'No calculator, matching real test conditions.')));

  // ---- choose how to run it
  const form = el('form', { class: 'card' });
  form.appendChild(el('h2', { style: 'margin-top:0', text: 'Start a practice run' }));

  form.appendChild(el('p', null, el('strong', null, 'What to run')));
  const modeWrap = el('div');
  const modes = [['full', 'Full exam — every section in real order']]
    .concat(exam.sections.map((s) => [`sec:${s.id}`, `Single section — ${s.name}`]));
  modes.forEach(([val, label], i) => {
    const id = `m-${i}`;
    modeWrap.appendChild(el('label', { class: 'choice', for: id },
      el('input', { type: 'radio', name: 'runmode', id, value: val, checked: i === 0 || null }),
      el('span', null, label)));
  });
  form.appendChild(modeWrap);

  form.appendChild(el('p', null, el('strong', null, 'Timing')));
  const timerWrap = el('div');
  const timers = [
    ['real', 'Real — each section gets its own countdown, and the exam moves on automatically when a section’s time runs out'],
    ['untimed', 'Untimed — no clock, same sections and same questions'],
    ['custom', 'Custom — I set the total minutes, split across sections in proportion'],
  ];
  timers.forEach(([val, label], i) => {
    const id = `t-${i}`;
    timerWrap.appendChild(el('label', { class: 'choice', for: id },
      el('input', { type: 'radio', name: 'timer', id, value: val, checked: i === 0 || null }),
      el('span', null, label)));
  });
  form.appendChild(timerWrap);

  const custom = el('p', null,
    el('label', { for: 'mins' }, 'Total minutes: '),
    el('input', { type: 'number', id: 'mins', min: '1', max: '600', value: '60',
      style: 'min-height:44px;padding:8px;border-radius:8px;border:1px solid var(--border);width:7em' }));
  custom.hidden = true;
  form.appendChild(custom);
  timerWrap.addEventListener('change', () => {
    custom.hidden = form.querySelector('input[name=timer]:checked').value !== 'custom';
  });

  if (exam.selfPaced) {
    form.appendChild(el('p', { class: 'notice', text: 'This test is administered as a single self-paced block, so timing options do not apply.' }));
  }

  form.appendChild(el('div', { class: 'btnrow' },
    el('button', { class: 'primary', type: 'submit', text: 'Start' }),
    el('a', { class: 'btn', href: `print.html?exam=${encodeURIComponent(exam.id)}`, text: 'Print view' }),
    meta && meta.trade
      ? el('a', { class: 'btn', href: `trade.html?trade=${encodeURIComponent(meta.trade.slug)}`, text: 'Back to trade' })
      : el('a', { class: 'btn', href: 'index.html', text: 'Home' })));

  form.addEventListener('submit', (ev) => {
    ev.preventDefault();
    const rm = form.querySelector('input[name=runmode]:checked').value;
    const timer = form.querySelector('input[name=timer]:checked').value;
    const minutes = Number(form.querySelector('#mins').value) || 60;
    const opts = rm.startsWith('sec:')
      ? { mode: 'section', section: rm.slice(4), timer, customMinutes: minutes }
      : { mode: 'full', timer, customMinutes: minutes };
    startRun(exam, opts, meta);
  });

  main.appendChild(form);
}

function startRun(exam, opts, meta) {
  const plan = buildPlan(exam, opts);
  main.textContent = '';
  const host = el('div');
  main.appendChild(host);
  const run = new Run(plan, host, (result) => showResults(result, exam, meta));
  run.start();
  window.scrollTo(0, 0);
}

function showResults(result, exam, meta) {
  main.textContent = '';
  const footer = el('div', { class: 'btnrow noprint' },
    el('button', { class: 'primary', text: 'Retake', onClick: () => renderSetup(exam, meta) }),
    el('a', { class: 'btn', href: 'progress.html', text: 'Progress' }),
    el('a', { class: 'btn', href: `print.html?exam=${encodeURIComponent(exam.id)}`, text: 'Print view' }),
    el('a', { class: 'btn', href: 'index.html', text: 'Home' }));
  renderResults(result, exam, main, { footer });
  announce(`Exam finished. Score ${result.pct} percent.`);
  window.scrollTo(0, 0);
  if (!store.storageAvailable()) {
    main.prepend(el('p', { class: 'notice', text: 'Browser storage is unavailable, so this attempt was not saved to your progress. Everything else works normally.' }));
  }
}
