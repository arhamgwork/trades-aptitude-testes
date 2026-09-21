// Unit tests for the run-plan builder: timers must come from the blueprint.
import assert from 'node:assert/strict';
import { buildPlan } from '../src/js/runner.js';

const exam = {
  id: 'x', title: 'X', selfPaced: false,
  sections: [
    { id: 'a', name: 'A', questionCount: 2, timeLimitSec: 2760 },
    { id: 'b', name: 'B', questionCount: 2, timeLimitSec: 3060 },
  ],
  questions: [
    { id: 'q1', section: 'a' }, { id: 'q2', section: 'a' },
    { id: 'q3', section: 'b' }, { id: 'q4', section: 'b' },
  ],
};

let n = 0;
const t = (name, fn) => { fn(); n++; console.log(`  ok   ${name}`); };

t('real timing uses the blueprint per-section limits, not one lump total', () => {
  const p = buildPlan(exam, { mode: 'full', timer: 'real' });
  assert.equal(p.sections.length, 2);
  assert.equal(p.sections[0].timeLimitSec, 2760);
  assert.equal(p.sections[1].timeLimitSec, 3060);
});

t('real timing keeps the real section order', () => {
  const p = buildPlan(exam, { mode: 'full', timer: 'real' });
  assert.deepEqual(p.sections.map((s) => s.id), ['a', 'b']);
});

t('untimed keeps the same sections and questions but drops every clock', () => {
  const p = buildPlan(exam, { mode: 'full', timer: 'untimed' });
  assert.deepEqual(p.sections.map((s) => s.timeLimitSec), [null, null]);
  assert.equal(p.sections.flatMap((s) => s.questions).length, 4);
});

t('custom splits the requested total proportionally to real time', () => {
  const p = buildPlan(exam, { mode: 'full', timer: 'custom', customMinutes: 97 });
  const total = p.sections.reduce((a, s) => a + s.timeLimitSec, 0);
  assert.ok(Math.abs(total - 97 * 60) <= 2, `total ${total}`);
  // 2760:3060 is the real ratio; the split must preserve it
  const ratio = p.sections[0].timeLimitSec / p.sections[1].timeLimitSec;
  assert.ok(Math.abs(ratio - 2760 / 3060) < 0.01, `ratio ${ratio}`);
});

t('custom halved still preserves the ratio', () => {
  const p = buildPlan(exam, { mode: 'full', timer: 'custom', customMinutes: 48 });
  const ratio = p.sections[0].timeLimitSec / p.sections[1].timeLimitSec;
  assert.ok(Math.abs(ratio - 2760 / 3060) < 0.02, `ratio ${ratio}`);
});

t('all three timer modes draw the same question set, so scores compare', () => {
  const ids = (p) => p.sections.flatMap((s) => s.questions.map((q) => q.id)).sort().join(',');
  const real = buildPlan(exam, { mode: 'full', timer: 'real' });
  const un = buildPlan(exam, { mode: 'full', timer: 'untimed' });
  const cu = buildPlan(exam, { mode: 'full', timer: 'custom', customMinutes: 30 });
  assert.equal(ids(real), ids(un));
  assert.equal(ids(real), ids(cu));
});

t('single-section mode runs only that section at its real limit', () => {
  const p = buildPlan(exam, { mode: 'section', section: 'b', timer: 'real' });
  assert.equal(p.sections.length, 1);
  assert.equal(p.sections[0].id, 'b');
  assert.equal(p.sections[0].timeLimitSec, 3060);
});

t('a self-paced exam is never given a clock', () => {
  const sp = { ...exam, selfPaced: true };
  const p = buildPlan(sp, { mode: 'full', timer: 'real' });
  assert.deepEqual(p.sections.map((s) => s.timeLimitSec), [null, null]);
  assert.equal(p.timer, 'untimed');
});

t('drills are always untimed', () => {
  const p = buildPlan(exam, {
    mode: 'drill', timer: 'real', drillQuestions: exam.questions, drillLabel: 'd',
  });
  assert.equal(p.timer, 'untimed');
  assert.equal(p.sections[0].timeLimitSec, null);
});

console.log(`\nplan tests passed (${n})`);
