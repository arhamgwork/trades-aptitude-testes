// Results rendering: overall, per-section, per-question review, skill breakdown.
import { el, LETTERS, fmtDuration, svgFigure, pct, choiceBody } from './util.js';

export function renderResults(result, exam, host, opts = {}) {
  host.textContent = '';

  host.appendChild(el('h1', { text: 'Results' }));
  host.appendChild(el('p', { class: 'lede', text: exam.title }));

  if (result.reason === 'time') {
    host.appendChild(el('p', { class: 'notice', text: 'The exam ended because the final section ran out of time.' }));
  }

  host.appendChild(el('div', { class: 'card' },
    el('div', { class: 'score', text: `${result.pct}%` }),
    el('p', { class: 'muted', text: `${result.right} of ${result.total} correct` }),
    el('div', { class: 'bar' }, el('i', { style: `width:${result.pct}%` })),
    el('p', { class: 'small muted', style: 'margin-bottom:0', text: modeLine(result) })));

  // ---- per section
  host.appendChild(el('h2', { text: 'By section' }));
  const rows = result.sections.map((s) => el('tr', null,
    el('td', { text: s.name }),
    el('td', { text: `${s.right}/${s.total}` }),
    el('td', { text: `${s.pct}%` }),
    el('td', { text: fmtDuration(s.spentSec) }),
    el('td', { text: s.limitSec ? fmtDuration(s.limitSec) : 'untimed' })));
  host.appendChild(el('div', { class: 'tablewrap' },
    el('table', null,
      el('thead', null, el('tr', null,
        el('th', { text: 'Section' }), el('th', { text: 'Score' }),
        el('th', { text: '%' }), el('th', { text: 'Time used' }), el('th', { text: 'Limit' }))),
      el('tbody', null, rows))));

  // ---- skills
  const skills = skillBreakdown(result);
  if (skills.length) {
    host.appendChild(el('h2', { text: 'By skill' }));
    host.appendChild(el('div', { class: 'tablewrap' },
      el('table', null,
        el('thead', null, el('tr', null,
          el('th', { text: 'Skill' }), el('th', { text: 'Correct' }), el('th', { text: '%' }))),
        el('tbody', null, skills.map((s) => el('tr', null,
          el('td', null, el('span', { class: 'tag', text: s.skill })),
          el('td', { text: `${s.right}/${s.total}` }),
          el('td', { text: `${Math.round(s.pct * 100)}%` })))))));
  }

  // ---- review
  host.appendChild(el('h2', { text: 'Question review' }));
  host.appendChild(el('p', { class: 'small muted', text: 'Every question, with the explanation and what each wrong choice represents.' }));

  const byId = new Map(exam.questions.map((q) => [q.id, q]));
  for (const r of result.perQuestion) {
    const q = byId.get(r.id);
    if (!q) continue;
    const cls = r.picked === null ? 'skipped' : (r.correct ? 'correct' : 'wrong');
    const block = el('div', { class: `review ${cls}` });
    block.appendChild(el('p', { class: 'small muted' },
      `${r.sectionName} · `,
      r.picked === null ? 'Not answered' : (r.correct ? 'Correct' : 'Incorrect')));
    block.appendChild(el('p', null, el('strong', null, q.stem)));
    if (q.figure) block.appendChild(svgFigure(q.figure, 'Figure for this question'));

    q.choices.forEach((c, i) => {
      const isKey = i === q.correctIndex;
      const isPicked = r.picked === i;
      const o = el('div', {
        class: `opt ${isKey ? 'key' : ''} ${isPicked && !isKey ? 'picked-wrong' : ''}`.trim(),
      },
        el('strong', { text: `${LETTERS[i]}. ` }), choiceBody(q, i),
        isKey ? el('span', { class: 'tag', text: 'correct' }) : null,
        isPicked ? el('span', { class: 'tag', text: 'your answer' }) : null);
      if (!isKey && q.distractorNotes && q.distractorNotes[i]) {
        o.appendChild(el('div', { class: 'small muted', text: `This choice comes from: ${q.distractorNotes[i]}` }));
      }
      block.appendChild(o);
    });
    block.appendChild(el('p', { class: 'small' }, el('strong', null, 'Why: '), q.explanation));
    block.appendChild(el('p', { class: 'small muted' },
      q.skills.map((s) => el('span', { class: 'tag', text: s })),
      el('span', { class: 'tag', text: `checked: ${q.verify}` })));
    host.appendChild(block);
  }

  if (opts.footer) host.appendChild(opts.footer);
}

function modeLine(r) {
  const m = { full: 'Full exam', section: 'Single section', drill: 'Drill' }[r.mode] || r.mode;
  const t = { real: 'real per-section timing', untimed: 'untimed', custom: 'custom timing' }[r.timer] || r.timer;
  return `${m}, ${t}.`;
}

export function skillBreakdown(result) {
  const acc = {};
  for (const r of result.perQuestion) {
    for (const s of r.skills || []) {
      acc[s] = acc[s] || { right: 0, total: 0 };
      acc[s].total++;
      if (r.correct) acc[s].right++;
    }
  }
  return Object.entries(acc)
    .map(([skill, v]) => ({ skill, ...v, pct: v.right / v.total }))
    .sort((a, b) => a.pct - b.pct || b.total - a.total);
}

export { pct };
