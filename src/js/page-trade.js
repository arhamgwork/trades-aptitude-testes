import { el, $, qs, mountChrome } from './util.js';
import { loadIndex } from './catalog.js';

const main = $('#main');
mountChrome(null);
const slug = qs('trade');

loadIndex().then((idx) => {
  const t = idx.trades.find((x) => x.slug === slug);
  if (!t) {
    main.textContent = '';
    main.appendChild(el('p', { class: 'err', text: 'That trade was not found.' }));
    main.appendChild(el('p', null, el('a', { href: 'index.html', text: 'Back to home' })));
    return;
  }
  document.title = `${t.name} — Trades Aptitude Practice`;
  render(t);
}).catch((e) => {
  main.textContent = '';
  main.appendChild(el('p', { class: 'err', text: `Could not load the catalog: ${e.message}` }));
});

function render(t) {
  main.textContent = '';
  main.appendChild(el('h1', { text: t.name }));
  if (t.blurb) main.appendChild(el('p', { class: 'lede', text: t.blurb }));

  for (const b of t.blueprints || []) main.appendChild(blueprintCard(b));

  main.appendChild(el('h2', { text: 'Full-length practice exams' }));
  const exams = t.exams || [];
  if (!exams.length) {
    main.appendChild(el('p', { class: 'muted', text: 'No exam has been built for this trade yet. The blueprint above records what is known about the real test format.' }));
  }
  for (const e of exams) {
    main.appendChild(el('div', { class: 'card' },
      el('h3', { style: 'margin-top:0' }, e.title,
        el('span', { class: `badge ${e.confidence}`, text: e.confidence, style: 'margin-left:8px' })),
      el('p', { class: 'small muted', text: `${e.totalQuestions} questions · ${e.sections.length} section${e.sections.length === 1 ? '' : 's'} · ${e.totalMinutes} minutes · ${e.calculatorAllowed ? 'calculator allowed' : 'no calculator'}` }),
      el('div', { class: 'btnrow' },
        el('a', { class: 'btn primary', href: `exam.html?exam=${encodeURIComponent(e.id)}`, text: 'Start exam' }),
        el('a', { class: 'btn', href: `print.html?exam=${encodeURIComponent(e.id)}`, text: 'Print' })),
      el('details', null,
        el('summary', { text: 'Practice one section only' }),
        el('div', { class: 'btnrow' },
          e.sections.map((s) => el('a', {
            class: 'btn',
            href: `exam.html?exam=${encodeURIComponent(e.id)}&mode=section&section=${encodeURIComponent(s.id)}`,
            text: `${s.name} (${s.questionCount} q)`,
          }))))));
  }

  main.appendChild(el('h2', { text: 'Skill drills' }));
  main.appendChild(el('p', { class: 'muted', text: 'Untimed practice by skill, drawn from every exam in the site.' }));
  main.appendChild(el('p', null,
    el('a', { class: 'btn', href: 'drills.html', text: 'Open skill drills' })));
}

function blueprintCard(b) {
  const card = el('div', { class: 'card' });
  card.appendChild(el('h2', { style: 'margin-top:0' }, 'Test blueprint ',
    el('span', { class: `badge ${b.confidence}`, text: b.confidence })));
  card.appendChild(el('p', null,
    el('strong', null, b.testName),
    b.provider && b.provider !== 'Disputed' ? ` — ${b.provider}` : ''));
  if (b.locals && b.locals.length) {
    card.appendChild(el('p', { class: 'small muted', text: `Used by: ${b.locals.join('; ')}` }));
  }

  if (b.sections && b.sections.length) {
    card.appendChild(el('div', { class: 'tablewrap' },
      el('table', null,
        el('thead', null, el('tr', null,
          el('th', { text: 'Section' }), el('th', { text: 'Questions' }),
          el('th', { text: 'Time' }), el('th', { text: 'Format' }), el('th', { text: 'Calculator' }))),
        el('tbody', null, b.sections.map((s) => el('tr', null,
          el('td', { text: s.name }),
          el('td', { text: String(s.questions) }),
          el('td', null, `${s.minutes} min`,
            s.timeConfirmed === false ? el('span', { class: 'tag', text: 'derived' }) : null),
          el('td', { text: s.format }),
          el('td', { text: s.calculator ? 'yes' : 'no' })))))));
    card.appendChild(el('p', { class: 'small muted', text: `Overall: ${b.totalQuestions} questions in ${b.totalMinutes} minutes.` }));
  } else {
    card.appendChild(el('p', { class: 'muted', text: 'No per-section table is published for this test.' }));
  }

  if (b.scoring) card.appendChild(el('p', { class: 'small' }, el('strong', null, 'Scoring: '), b.scoring));

  if (b.unverified) {
    card.appendChild(el('p', { class: 'notice' },
      el('strong', null, 'What is not confirmed: '), b.unverified));
  }

  const src = el('details', null, el('summary', { text: 'Sources and date checked' }));
  src.appendChild(el('p', { class: 'small muted', text: `Checked ${b.dateChecked}.` }));
  src.appendChild(el('ul', { class: 'small' }, (b.sources || []).map((u) =>
    el('li', null, el('a', { href: u, rel: 'noopener noreferrer', target: '_blank', text: u })))));
  if (b.doc) src.appendChild(el('p', { class: 'small muted', text: `Full blueprint: ${b.doc}` }));
  card.appendChild(src);
  return card;
}
