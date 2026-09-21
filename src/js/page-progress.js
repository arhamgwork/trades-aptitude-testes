import { el, $, mountChrome, fmtDuration, choiceBody } from './util.js';
import * as store from './store.js';
import { loadIndex, loadExam } from './catalog.js';
import { enableOffline } from './offline.js';

const main = $('#main');
mountChrome('progress.html');
enableOffline();
render();

function render() {
  main.textContent = '';
  main.appendChild(el('h1', { text: 'Progress' }));

  if (!store.storageAvailable()) {
    main.appendChild(el('p', { class: 'notice', text: 'Browser storage is unavailable here, so attempts are kept only for this visit. Use Export below if you want to carry them somewhere else.' }));
  }

  const attempts = store.attempts();
  main.appendChild(backupCard());

  if (!attempts.length) {
    main.appendChild(el('p', { class: 'muted', text: 'No attempts recorded yet. Take an exam or a drill and the results will show up here.' }));
    return;
  }

  // ---- weak spots
  const weak = store.weakSkills(3, 10);
  const weakCard = el('div', { class: 'card' }, el('h2', { style: 'margin-top:0', text: 'Weak spots' }));
  if (weak.length) {
    weakCard.appendChild(el('p', { class: 'small muted', text: 'Skills you are missing most, counting only skills you have seen at least three times. Each one links straight to its drill.' }));
    const tbl = el('table', null,
      el('thead', null, el('tr', null,
        el('th', { text: 'Skill' }), el('th', { text: 'Correct' }),
        el('th', { text: '%' }), el('th', { text: '' }))),
      el('tbody', null, weak.map((w) => el('tr', null,
        el('td', null, el('span', { class: 'tag', text: w.skill })),
        el('td', { text: `${w.right}/${w.total}` }),
        el('td', { text: `${Math.round(w.pct * 100)}%` }),
        el('td', null, el('a', {
          class: 'btn', style: 'min-height:34px;padding:4px 10px',
          href: `drills.html?quick=10&skills=${encodeURIComponent(w.skill)}`, text: 'Drill this',
        }))))));
    weakCard.appendChild(el('div', { class: 'tablewrap' }, tbl));
  } else {
    weakCard.appendChild(el('p', { class: 'muted', text: 'Not enough data yet. A skill appears here once you have answered at least three questions tagged with it.' }));
  }
  main.appendChild(weakCard);

  // ---- per-skill accuracy
  const stats = store.skillStats();
  const rows = Object.entries(stats)
    .map(([skill, v]) => ({ skill, ...v, pct: v.right / v.total }))
    .sort((a, b) => a.skill.localeCompare(b.skill));
  if (rows.length) {
    main.appendChild(el('h2', { text: 'Per-skill accuracy' }));
    main.appendChild(el('div', { class: 'tablewrap' },
      el('table', null,
        el('thead', null, el('tr', null,
          el('th', { text: 'Skill' }), el('th', { text: 'Seen' }),
          el('th', { text: 'Correct' }), el('th', { text: '%' }))),
        el('tbody', null, rows.map((r) => el('tr', null,
          el('td', null, el('span', { class: 'tag', text: r.skill })),
          el('td', { text: String(r.total) }),
          el('td', { text: String(r.right) }),
          el('td', { text: `${Math.round(r.pct * 100)}%` })))))));
  }

  // ---- history
  main.appendChild(el('h2', { text: 'Attempt history' }));
  main.appendChild(el('div', { class: 'tablewrap' },
    el('table', null,
      el('thead', null, el('tr', null,
        el('th', { text: 'When' }), el('th', { text: 'Exam' }),
        el('th', { text: 'Mode' }), el('th', { text: 'Score' }), el('th', { text: '' }))),
      el('tbody', null, attempts.map((a) => el('tr', null,
        el('td', { text: new Date(a.finishedAt).toLocaleString() }),
        el('td', { text: a.examTitle || a.examId }),
        el('td', { text: `${a.mode}, ${a.timer}` }),
        el('td', { text: `${a.right}/${a.total} (${a.pct}%)` }),
        el('td', null, el('button', {
          text: 'Review missed',
          style: 'min-height:34px;padding:4px 10px',
          onClick: () => reviewMissed(a),
        }))))))));
}

function backupCard() {
  const card = el('div', { class: 'card' },
    el('h2', { style: 'margin-top:0', text: 'Backup' }),
    el('p', { class: 'small muted', text: 'Progress lives in this browser only. Export a file to keep it, or to move it to another device.' }));
  const status = el('p', { class: 'small' });
  const file = el('input', { type: 'file', accept: 'application/json,.json', style: 'display:none' });
  file.addEventListener('change', async () => {
    const f = file.files && file.files[0];
    if (!f) return;
    try {
      const n = store.importJSON(await f.text());
      status.textContent = `Imported ${n} attempt${n === 1 ? '' : 's'}.`;
      status.className = 'small';
      render();
    } catch (e) {
      status.textContent = `Import failed: ${e.message}`;
      status.className = 'small err';
    }
  });
  card.appendChild(el('div', { class: 'btnrow' },
    el('button', { text: 'Export progress (JSON)', onClick: doExport }),
    el('button', { text: 'Import progress', onClick: () => file.click() }),
    el('button', {
      text: 'Clear all progress',
      onClick: () => {
        if (confirm('Delete every recorded attempt on this device? This cannot be undone.')) {
          store.clearAll();
          render();
        }
      },
    })));
  card.appendChild(file);
  card.appendChild(status);
  return card;
}

function doExport() {
  const blob = new Blob([store.exportJSON()], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = el('a', { href: url, download: `trades-aptitude-progress-${new Date().toISOString().slice(0, 10)}.json` });
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

async function reviewMissed(attempt) {
  main.textContent = '';
  main.appendChild(el('h1', { text: 'Missed questions' }));
  main.appendChild(el('p', { class: 'lede', text: `${attempt.examTitle || attempt.examId} — ${new Date(attempt.finishedAt).toLocaleString()}` }));
  main.appendChild(el('div', { class: 'btnrow noprint' },
    el('button', { text: '← Back to progress', onClick: render })));

  const missed = (attempt.perQuestion || []).filter((r) => !r.correct);
  if (!missed.length) {
    main.appendChild(el('p', { class: 'muted', text: 'Nothing missed on this attempt.' }));
    return;
  }

  let exam = null;
  try {
    exam = await loadExam(attempt.examId);
  } catch { /* drill attempts have no standalone exam file */ }

  if (!exam) {
    // Fall back to searching every exam for the ids (drills mix sources).
    const idx = await loadIndex();
    const all = await Promise.all(idx.trades.flatMap((t) => (t.exams || []).map((e) => loadExam(e.id).catch(() => null))));
    const map = new Map();
    for (const ex of all) if (ex) for (const q of ex.questions) map.set(q.id, { q, exam: ex });
    renderMissed(missed, (id) => map.get(id));
    return;
  }
  const map = new Map(exam.questions.map((q) => [q.id, { q, exam }]));
  renderMissed(missed, (id) => map.get(id));
}

function renderMissed(missed, lookup) {
  const { LETTERS } = { LETTERS: ['A', 'B', 'C', 'D', 'E'] };
  for (const r of missed) {
    const hit = lookup(r.id);
    if (!hit) continue;
    const q = hit.q;
    const block = el('div', { class: `review ${r.picked === null ? 'skipped' : 'wrong'}` });
    block.appendChild(el('p', { class: 'small muted', text: r.picked === null ? 'Not answered' : 'Incorrect' }));
    block.appendChild(el('p', null, el('strong', null, q.stem)));
    q.choices.forEach((c, i) => {
      const isKey = i === q.correctIndex;
      const isPicked = r.picked === i;
      const o = el('div', { class: `opt ${isKey ? 'key' : ''} ${isPicked && !isKey ? 'picked-wrong' : ''}`.trim() },
        el('strong', { text: `${LETTERS[i]}. ` }), choiceBody(q, i),
        isKey ? el('span', { class: 'tag', text: 'correct' }) : null,
        isPicked ? el('span', { class: 'tag', text: 'your answer' }) : null);
      if (!isKey && q.distractorNotes && q.distractorNotes[i]) {
        o.appendChild(el('div', { class: 'small muted', text: `This choice comes from: ${q.distractorNotes[i]}` }));
      }
      block.appendChild(o);
    });
    block.appendChild(el('p', { class: 'small' }, el('strong', null, 'Why: '), q.explanation));
    block.appendChild(el('p', null, (q.skills || []).map((s) => el('a', {
      class: 'tag', href: `drills.html?quick=10&skills=${encodeURIComponent(s)}`, text: s,
    }))));
    main.appendChild(block);
  }
}
