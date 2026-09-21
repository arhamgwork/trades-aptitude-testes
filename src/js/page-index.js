import { el, $, mountChrome } from './util.js';
import { loadIndex } from './catalog.js';
import * as store from './store.js';

const main = $('#main');
mountChrome('index.html');

loadIndex().then(render).catch((e) => {
  main.textContent = '';
  main.appendChild(el('p', { class: 'err', text: `Could not load the catalog: ${e.message}` }));
});

function render(idx) {
  main.textContent = '';
  main.appendChild(el('h1', { text: 'Trades Aptitude Practice' }));
  main.appendChild(el('p', { class: 'lede', text: 'Format-faithful practice exams and skill drills for Chicago-area apprenticeship aptitude tests.' }));

  if (!store.storageAvailable()) {
    main.appendChild(el('p', { class: 'notice', text: 'Browser storage is unavailable here, so progress will not be remembered between visits. Everything else works.' }));
  }

  // ---- resume
  const r = store.getResume();
  if (r) {
    main.appendChild(el('div', { class: 'card' },
      el('h2', { style: 'margin-top:0', text: 'Pick up where you left off' }),
      el('p', { class: 'muted', text: r.title || r.examId }),
      el('div', { class: 'btnrow' },
        el('a', {
          class: 'btn primary',
          href: `exam.html?exam=${encodeURIComponent(r.examId)}`,
          text: 'Resume',
        }),
        el('button', { text: 'Clear', onClick: () => { store.clearResume(); render(idx); } }))));
  }

  // ---- quick 10 from weakest skills
  const weak = store.weakSkills(3, 5);
  const q10 = el('div', { class: 'card' },
    el('h2', { style: 'margin-top:0', text: 'Quick 10' }));
  if (weak.length) {
    q10.appendChild(el('p', { class: 'muted', text: 'Ten questions drawn from the skills you are missing most.' }));
    q10.appendChild(el('p', null, weak.map((w) =>
      el('span', { class: 'tag', text: `${w.skill} ${Math.round(w.pct * 100)}%` }))));
    q10.appendChild(el('div', { class: 'btnrow' },
      el('a', {
        class: 'btn primary',
        href: `drills.html?quick=10&skills=${encodeURIComponent(weak.map((w) => w.skill).join(','))}`,
        text: 'Start Quick 10',
      })));
  } else {
    q10.appendChild(el('p', { class: 'muted', text: 'Take an exam or a drill first. Once there is attempt data, this becomes ten questions drawn from your weakest skills.' }));
    q10.appendChild(el('div', { class: 'btnrow' },
      el('a', { class: 'btn', href: 'drills.html', text: 'Browse skill drills' })));
  }
  main.appendChild(q10);

  // ---- trades
  main.appendChild(el('h2', { text: 'Trades' }));
  const grid = el('div', { class: 'grid two' });
  for (const t of idx.trades) {
    const exams = t.exams || [];
    const confs = [...new Set((t.blueprints || []).map((b) => b.confidence))];
    grid.appendChild(el('a', {
      class: 'card', href: `trade.html?trade=${encodeURIComponent(t.slug)}`,
      style: 'text-decoration:none;color:inherit;display:block',
    },
      el('h3', { style: 'margin-top:0', text: t.name },
        ...confs.map((c) => el('span', { class: `badge ${c}`, text: c, style: 'margin-left:8px' }))),
      el('p', { class: 'small muted', text: t.blurb || '' }),
      el('p', { class: 'small', text: exams.length
        ? `${exams.length} practice exam${exams.length === 1 ? '' : 's'}`
        : 'Blueprint and drills' })));
  }
  main.appendChild(grid);

  if (idx.pending && idx.pending.length) {
    main.appendChild(el('h2', { text: 'Planned' }));
    main.appendChild(el('p', { class: 'small muted', text: 'Researched but not yet built. Nothing here is guessed at — a trade appears as an exam only once its format is confirmed or explicitly marked partial.' }));
    main.appendChild(el('p', null, idx.pending.map((p) => el('span', { class: 'tag', text: p }))));
  }
}
