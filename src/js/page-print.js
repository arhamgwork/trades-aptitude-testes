import { el, $, qs, mountChrome, LETTERS, svgFigure, DISCLAIMER, choiceBody, choiceText } from './util.js';
import { loadExam } from './catalog.js';
import { enableOffline } from './offline.js';

const main = $('#main');
mountChrome(null);
enableOffline();
const examId = qs('exam');

if (!examId) {
  main.textContent = '';
  main.appendChild(el('p', { class: 'err', text: 'No exam was specified in the address.' }));
} else {
  loadExam(examId).then(render).catch((e) => {
    main.textContent = '';
    main.appendChild(el('p', { class: 'err', text: `Could not load the exam: ${e.message}` }));
  });
}

function render(exam) {
  document.title = `${exam.title} — print`;
  main.textContent = '';

  main.appendChild(el('div', { class: 'btnrow noprint' },
    el('button', { class: 'primary', text: 'Print this page', onClick: () => window.print() }),
    el('a', { class: 'btn', href: `exam.html?exam=${encodeURIComponent(exam.id)}`, text: 'Back to exam' })));
  main.appendChild(el('p', { class: 'small muted noprint', text: 'This page holds the exam booklet followed by the answer key. Print the whole page, or use your print dialog’s page range to print just one part.' }));

  // ---------- booklet
  main.appendChild(el('h1', { text: exam.title }));
  main.appendChild(el('p', { class: 'small' }, DISCLAIMER));
  main.appendChild(el('p', { class: 'small muted' },
    `${exam.testName} · ${exam.confidence}`,
    exam.calculatorAllowed ? ' · calculator allowed' : ' · no calculator'));
  main.appendChild(el('ul', { class: 'small' }, exam.sections.map((s) =>
    el('li', { text: `${s.name}: ${s.questionCount} questions, ${Math.round((s.timeLimitSec || 0) / 60)} minutes` }))));

  let n = 0;
  const printed = new Set();
  for (const s of exam.sections) {
    main.appendChild(el('h2', { class: 'pagebreak', text: s.name }));
    main.appendChild(el('p', { class: 'small muted', text: `${s.questionCount} questions · ${Math.round((s.timeLimitSec || 0) / 60)} minutes` }));
    for (const q of exam.questions.filter((x) => x.section === s.id)) {
      n++;
      if (q.passageId && !printed.has(q.passageId)) {
        const p = (exam.passages || []).find((x) => x.id === q.passageId);
        if (p) {
          printed.add(p.id);
          const box = el('div', { class: 'passage' }, el('h3', { text: p.title }));
          for (const para of p.text.split(/\n\s*\n/)) {
            box.appendChild(el('p', { text: para.replace(/\s*\n\s*/g, ' ').trim() }));
          }
          main.appendChild(box);
        }
      }
      const b = el('div', { class: 'printq' });
      b.appendChild(el('p', null, el('strong', { text: `${n}. ` }), q.stem));
      if (q.figure) b.appendChild(svgFigure(q.figure, 'Figure'));
      b.appendChild(el('div', null, q.choices.map((c, i) =>
        el('div', { class: 'small' }, el('strong', { text: `${LETTERS[i]}. ` }), choiceBody(q, i)))));
      main.appendChild(b);
    }
  }

  // ---------- answer key
  main.appendChild(el('h1', { class: 'pagebreak', text: 'Answer key and explanations' }));
  main.appendChild(el('p', { class: 'small' }, DISCLAIMER));
  let k = 0;
  for (const s of exam.sections) {
    main.appendChild(el('h2', { text: s.name }));
    for (const q of exam.questions.filter((x) => x.section === s.id)) {
      k++;
      const b = el('div', { class: 'printq' });
      b.appendChild(el('p', null,
        el('strong', { text: `${k}. ${LETTERS[q.correctIndex]}` }),
        ` — ${q.choices[q.correctIndex]}`));
      b.appendChild(el('p', { class: 'small', text: q.explanation }));
      const wrong = q.choices
        .map((c, i) => (i === q.correctIndex ? null : `${LETTERS[i]}: ${q.distractorNotes[i]}`))
        .filter(Boolean);
      b.appendChild(el('ul', { class: 'small muted' }, wrong.map((w) => el('li', { text: w }))));
      main.appendChild(b);
    }
  }
}
