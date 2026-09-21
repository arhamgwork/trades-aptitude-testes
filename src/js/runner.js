// Exam runner: builds a run plan, drives per-section timers, renders questions,
// collects answers, and produces a result object.
import { el, $, LETTERS, fmtClock, svgFigure, announce, pct } from './util.js';
import * as store from './store.js';

/**
 * Build the plan for one run.
 * mode: 'full' | 'section' | 'drill'
 * timer: 'real' | 'untimed' | 'custom'
 */
export function buildPlan(exam, opts) {
  const { mode, timer, section, customMinutes, drillQuestions, drillLabel } = opts;
  let sections;

  if (mode === 'drill') {
    sections = [{
      id: 'drill', name: drillLabel || 'Drill', timeLimitSec: null,
      questions: drillQuestions,
    }];
    return { exam, mode, timer: 'untimed', sections, selfPaced: true };
  }

  const wanted = mode === 'section'
    ? exam.sections.filter((s) => s.id === section)
    : exam.sections;

  sections = wanted.map((s) => ({
    id: s.id,
    name: s.name,
    timeConfirmed: s.timeConfirmed !== false,
    timeLimitSec: s.timeLimitSec,
    questions: exam.questions.filter((q) => q.section === s.id),
  }));

  if (timer === 'untimed' || exam.selfPaced) {
    sections.forEach((s) => { s.timeLimitSec = null; });
  } else if (timer === 'custom') {
    // Split the requested total across sections in proportion to real time,
    // so scores stay comparable with a Real run.
    const total = wanted.reduce((a, s) => a + (s.timeLimitSec || 0), 0);
    const budget = Math.max(1, Number(customMinutes) || 1) * 60;
    sections.forEach((s, i) => {
      s.timeLimitSec = total
        ? Math.max(30, Math.round((wanted[i].timeLimitSec / total) * budget))
        : Math.round(budget / sections.length);
    });
  }

  return {
    exam, mode, timer: exam.selfPaced ? 'untimed' : timer, sections,
    selfPaced: !!exam.selfPaced,
  };
}

export class Run {
  constructor(plan, host, onFinish) {
    this.plan = plan;
    this.host = host;
    this.onFinish = onFinish;
    this.answers = new Map();      // qid -> choice index
    this.flags = new Set();
    this.si = 0;                   // section index
    this.qi = 0;                   // question index within section
    this.sectionSpent = {};        // section id -> seconds used
    this.startedAt = Date.now();
    this._tick = null;
    this._sectionStart = null;
    this._remaining = null;
    this._submitted = false;
  }

  get section() { return this.plan.sections[this.si]; }
  get questions() { return this.section.questions; }
  get question() { return this.questions[this.qi]; }

  start() {
    this._enterSection(0);
    this._bindKeys();
  }

  _enterSection(i) {
    this.si = i;
    this.qi = 0;
    const s = this.section;
    this._sectionStart = Date.now();
    this._remaining = s.timeLimitSec;
    this._stopTick();
    if (s.timeLimitSec !== null && s.timeLimitSec !== undefined) {
      this._tick = setInterval(() => this._onTick(), 250);
    }
    this.render();
    announce(`Section ${i + 1} of ${this.plan.sections.length}: ${s.name}`);
  }

  _onTick() {
    const elapsed = (Date.now() - this._sectionStart) / 1000;
    this._remaining = Math.max(0, this.section.timeLimitSec - elapsed);
    this._paintTimer();
    if (this._remaining <= 0) {
      this._stopTick();
      this._advanceSectionOnTimeout();
    }
  }

  _stopTick() { if (this._tick) { clearInterval(this._tick); this._tick = null; } }

  _recordSpent() {
    const s = this.section;
    const spent = (Date.now() - this._sectionStart) / 1000;
    this.sectionSpent[s.id] = (this.sectionSpent[s.id] || 0) + spent;
  }

  _advanceSectionOnTimeout() {
    this._recordSpent();
    const last = this.si >= this.plan.sections.length - 1;
    if (last) {
      this.finish('time');
    } else {
      // The real proctored test moves you along; so does this.
      announce('Time is up for this section. Moving to the next section.');
      this._enterSection(this.si + 1);
    }
  }

  nextSection() {
    this._recordSpent();
    if (this.si >= this.plan.sections.length - 1) return this.confirmSubmit();
    this._enterSection(this.si + 1);
  }

  _bindKeys() {
    this._keyHandler = (ev) => {
      if (ev.metaKey || ev.ctrlKey || ev.altKey) return;
      const tag = (ev.target.tagName || '').toLowerCase();
      if (tag === 'input' && ev.target.type !== 'radio') return;
      if (tag === 'textarea' || document.querySelector('dialog[open]')) return;
      const k = ev.key.toUpperCase();
      const q = this.question;
      if (!q) return;
      const n = q.choices.length;
      let idx = -1;
      if (/^[1-9]$/.test(k)) idx = Number(k) - 1;
      else if (/^[A-E]$/.test(k)) idx = LETTERS.indexOf(k);
      if (idx >= 0 && idx < n) { ev.preventDefault(); this.answer(q.id, idx); return; }
      if (k === 'N') { ev.preventDefault(); this.go(this.qi + 1); }
      else if (k === 'P') { ev.preventDefault(); this.go(this.qi - 1); }
      else if (k === 'F') { ev.preventDefault(); this.toggleFlag(q.id); }
    };
    document.addEventListener('keydown', this._keyHandler);
  }

  answer(qid, idx) {
    this.answers.set(qid, idx);
    this.render();
    announce(`Answered ${LETTERS[idx]}`);
  }

  toggleFlag(qid) {
    if (this.flags.has(qid)) this.flags.delete(qid); else this.flags.add(qid);
    this.render();
    announce(this.flags.has(qid) ? 'Flagged for review' : 'Flag removed');
  }

  go(i) {
    if (i < 0 || i >= this.questions.length) return;
    this.qi = i;
    this.render();
  }

  confirmSubmit() {
    const unanswered = this.plan.sections
      .flatMap((s) => s.questions)
      .filter((q) => !this.answers.has(q.id)).length;
    const flagged = this.flags.size;
    const dlg = el('dialog', { 'aria-labelledby': 'sub-h' },
      el('h2', { id: 'sub-h', text: 'Submit this exam?' }),
      el('p', {
        text: unanswered
          ? `${unanswered} question${unanswered === 1 ? '' : 's'} still unanswered${flagged ? `, ${flagged} flagged` : ''}.`
          : `All questions answered${flagged ? `, ${flagged} flagged` : ''}.`,
      }),
      el('p', { class: 'small muted', text: 'Unanswered questions are scored as incorrect, the same as on the real test.' }),
      el('div', { class: 'btnrow' },
        el('button', { class: 'primary', text: 'Submit and see results', onClick: () => { dlg.close(); this.finish('submitted'); } }),
        el('button', { text: 'Keep working', onClick: () => dlg.close() })));
    document.body.appendChild(dlg);
    dlg.showModal();
  }

  finish(reason) {
    if (this._submitted) return;
    this._submitted = true;
    this._stopTick();
    document.removeEventListener('keydown', this._keyHandler);
    if (this._sectionStart) this._recordSpent();
    const result = this.grade(reason);
    store.clearResume();
    store.recordAttempt(result);
    this.onFinish(result);
  }

  grade(reason) {
    const perQuestion = [];
    const sections = [];
    for (const s of this.plan.sections) {
      let right = 0;
      for (const q of s.questions) {
        const picked = this.answers.has(q.id) ? this.answers.get(q.id) : null;
        const correct = picked === q.correctIndex;
        if (correct) right++;
        perQuestion.push({
          id: q.id, section: s.id, sectionName: s.name, skills: q.skills,
          picked, correct, correctIndex: q.correctIndex,
        });
      }
      sections.push({
        id: s.id, name: s.name, total: s.questions.length, right,
        pct: pct(right, s.questions.length),
        spentSec: Math.round(this.sectionSpent[s.id] || 0),
        limitSec: s.timeLimitSec ?? null,
      });
    }
    const total = perQuestion.length;
    const right = perQuestion.filter((r) => r.correct).length;
    return {
      attemptId: `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`,
      examId: this.plan.exam.id,
      examTitle: this.plan.exam.title,
      mode: this.plan.mode,
      timer: this.plan.timer,
      finishedAt: new Date().toISOString(),
      reason,
      total, right, pct: pct(right, total),
      sections, perQuestion,
      answers: Object.fromEntries(this.answers),
      flagged: Array.from(this.flags),
    };
  }

  _paintTimer() {
    const t = $('#timer', this.host);
    if (!t) return;
    if (this._remaining === null || this._remaining === undefined) {
      t.textContent = 'No time limit';
      t.classList.remove('low');
      return;
    }
    t.textContent = fmtClock(this._remaining);
    t.classList.toggle('low', this._remaining <= 60);
  }

  render() {
    const s = this.section;
    const q = this.question;
    const host = this.host;
    host.textContent = '';

    const nsec = this.plan.sections.length;
    const top = el('div', { class: 'examtop' },
      el('div', null,
        el('div', { class: 'timer', id: 'timer', role: 'timer', 'aria-live': 'off' }, '—'),
        el('div', { class: 'meta', text: s.timeLimitSec ? 'Time left in this section' : 'Untimed' })),
      el('div', { class: 'meta' },
        nsec > 1 ? `Section ${this.si + 1} of ${nsec} · ` : '',
        s.name, ' · ',
        `Question ${this.qi + 1} of ${this.questions.length}`),
      el('div', { class: 'btnrow', style: 'margin:0 0 0 auto' },
        el('button', { text: 'Submit', onClick: () => this.confirmSubmit() })));
    host.appendChild(top);

    if (s.timeLimitSec && s.timeConfirmed === false) {
      host.appendChild(el('p', {
        class: 'notice',
        text: 'This section’s time limit is derived, not published by the test provider. See the blueprint on the trade page.',
      }));
    }

    const exam = this.plan.exam;
    if (q.passageId) {
      const p = (exam.passages || []).find((x) => x.id === q.passageId);
      if (p) {
        const box = el('section', { class: 'passage', 'aria-label': `Passage: ${p.title}`, tabindex: '0' },
          el('h3', { text: p.title }));
        for (const para of p.text.split(/\n\s*\n/)) {
          box.appendChild(el('p', { text: para.replace(/\s*\n\s*/g, ' ').trim() }));
        }
        host.appendChild(box);
      }
    }

    const fs = el('fieldset', { class: 'choices' },
      el('legend', null,
        el('span', { class: 'muted small' }, `${this.qi + 1}. `),
        q.stem));
    if (q.figure) fs.appendChild(svgFigure(q.figure, 'Figure for this question'));

    q.choices.forEach((c, i) => {
      const id = `c${this.si}-${this.qi}-${i}`;
      const input = el('input', {
        type: 'radio', name: `q-${q.id}`, id, value: String(i),
        onChange: () => this.answer(q.id, i),
      });
      if (this.answers.get(q.id) === i) input.checked = true;
      fs.appendChild(el('label', { class: 'choice', for: id },
        input, el('span', { class: 'lab', text: LETTERS[i] + '.' }), el('span', null, c)));
    });
    host.appendChild(fs);

    const flagged = this.flags.has(q.id);
    host.appendChild(el('div', { class: 'btnrow' },
      el('button', { text: '← Previous', onClick: () => this.go(this.qi - 1), disabled: this.qi === 0 }),
      el('button', { text: 'Next →', onClick: () => this.go(this.qi + 1), disabled: this.qi === this.questions.length - 1 }),
      el('button', {
        text: flagged ? '⚑ Unflag' : '⚐ Flag for review',
        'aria-pressed': flagged ? 'true' : 'false',
        onClick: () => this.toggleFlag(q.id),
      }),
      this.qi === this.questions.length - 1 && this.si < nsec - 1
        ? el('button', { class: 'primary', text: 'Next section →', onClick: () => this.nextSection() })
        : null));

    const grid = el('div', { class: 'qgrid', role: 'group', 'aria-label': 'Question navigation' });
    this.questions.forEach((qq, i) => {
      grid.appendChild(el('button', {
        text: String(i + 1),
        class: [this.answers.has(qq.id) ? 'answered' : '', this.flags.has(qq.id) ? 'flagged' : ''].join(' ').trim(),
        'aria-current': i === this.qi ? 'true' : null,
        'aria-label': `Question ${i + 1}${this.answers.has(qq.id) ? ', answered' : ', not answered'}${this.flags.has(qq.id) ? ', flagged' : ''}`,
        onClick: () => this.go(i),
      }));
    });
    host.appendChild(grid);
    host.appendChild(el('div', { class: 'legend' },
      el('span', null, el('i', { class: 'swatch answered' }), 'answered'),
      el('span', null, el('i', { class: 'swatch flagged' }), 'flagged'),
      el('span', null, 'Keys: 1-5 or A-E to answer, N next, P previous, F flag')));

    this._paintTimer();
    // Keep a resume marker so the home page can offer to pick this back up.
    store.setResume({
      examId: exam.id, mode: this.plan.mode, timer: this.plan.timer,
      section: s.id, at: Date.now(), title: exam.title,
    });
  }
}
