// Deterministic answer-key rebalance for migrated exams.
//
// Migrated content is kept as authored wherever possible. The brief allows one
// exception: if a migrated exam's key distribution falls outside the limits, it
// is rebalanced. This moves choices within a question and carries the key with
// them, so the correct text never changes — only its position.
//
// Terminal options such as "No answer" are a real feature of the format and are
// pinned in place rather than shuffled.
import crypto from 'node:crypto';

const PINNED = /^(no answer|none of these|none of the above|all of the above)$/i;

function shuffled(seq, seed) {
  const out = list(seq);
  let pool = Buffer.from(crypto.createHash('sha256').update(seed).digest());
  let i = 0;
  for (let k = out.length - 1; k > 0; k--) {
    if (i + 4 > pool.length) {
      pool = Buffer.concat([pool, crypto.createHash('sha256').update(pool).digest()]);
    }
    const j = pool.readUInt32BE(i) % (k + 1);
    i += 4;
    [out[k], out[j]] = [out[j], out[k]];
  }
  return out;
}
const list = (s) => Array.from(s);

function breakRuns(targets, maxRun = 3) {
  const n = targets.length;
  for (let i = maxRun; i < n; i++) {
    const w = targets.slice(i - maxRun, i + 1);
    if (new Set(w).size !== 1) continue;
    let done = false;
    for (let j = i + 1; j < n && !done; j++) {
      if (targets[j] !== targets[i] && (j + 1 >= n || targets[j + 1] !== targets[i])) {
        [targets[i], targets[j]] = [targets[j], targets[i]];
        done = true;
      }
    }
    if (!done) {
      for (let j = i - maxRun - 1; j >= 0; j--) {
        if (targets[j] !== targets[i]) { [targets[i], targets[j]] = [targets[j], targets[i]]; break; }
      }
    }
  }
  return targets;
}

/** Indices a key is allowed to occupy: everything except pinned terminals. */
function movableIndices(q) {
  const idx = [];
  for (let i = 0; i < q.choices.length; i++) {
    if (PINNED.test(String(q.choices[i]).trim()) && i === q.choices.length - 1) continue;
    idx.push(i);
  }
  return idx;
}

export function rebalanceExam(exam, seed) {
  const groups = {};
  exam.questions.forEach((q, i) => {
    const key = `${q.section}/${q.choices.length}`;
    (groups[key] = groups[key] || []).push(i);
  });

  let moved = 0;
  for (const [key, idxs] of Object.entries(groups).sort()) {
    // Questions whose key is currently on a pinned option keep it there:
    // "No answer" is sometimes genuinely the right answer.
    const free = idxs.filter((i) => {
      const q = exam.questions[i];
      const mv = movableIndices(q);
      return mv.includes(q.correctIndex);
    });
    if (!free.length) continue;
    const slots = movableIndices(exam.questions[free[0]]);
    let targets = free.map((_, n) => slots[n % slots.length]);
    targets = shuffled(targets, `${seed}:${key}`);
    targets = breakRuns(targets, 3);

    free.forEach((qi, pos) => {
      const q = exam.questions[qi];
      const target = targets[pos];
      const cur = q.correctIndex;
      if (cur === target) return;
      const order = [...q.choices.keys()];
      [order[cur], order[target]] = [order[target], order[cur]];
      q.choices = order.map((k) => q.choices[k]);
      q.distractorNotes = order.map((k) => q.distractorNotes[k]);
      q.correctIndex = target;
      moved++;
    });
  }
  return moved;
}

/** Move a question's key to `target` by permuting its own choices. */
function placeKey(q, target) {
  const cur = q.correctIndex;
  if (cur === target) return;
  const order = [...q.choices.keys()];
  [order[cur], order[target]] = [order[target], order[cur]];
  q.choices = order.map((k) => q.choices[k]);
  q.distractorNotes = order.map((k) => q.distractorNotes[k]);
  q.correctIndex = target;
}

/**
 * Break runs of more than `maxRun` identical correct letters across the whole
 * exam, including across section boundaries. Keys are swapped between two
 * questions in the same (section, width) group, so each group's letter
 * distribution is preserved exactly.
 */
export function fixGlobalRuns(exam, maxRun = 3) {
  const groupOf = (q) => `${q.section}/${q.choices.length}`;
  const qs = exam.questions;
  let swaps = 0;
  for (let i = maxRun; i < qs.length; i++) {
    const window = qs.slice(i - maxRun, i + 1);
    if (new Set(window.map((q) => q.correctIndex)).size !== 1) continue;
    const g = groupOf(qs[i]);
    const movable = movableIndices(qs[i]);
    if (!movable.includes(qs[i].correctIndex)) continue;
    for (let j = 0; j < qs.length; j++) {
      if (j === i || groupOf(qs[j]) !== g) continue;
      if (qs[j].correctIndex === qs[i].correctIndex) continue;
      const mvj = movableIndices(qs[j]);
      if (!mvj.includes(qs[j].correctIndex) || !mvj.includes(qs[i].correctIndex)) continue;
      // would the swap create a fresh run at j?
      const neighbours = [qs[j - 1], qs[j + 1]].filter(Boolean).map((q) => q.correctIndex);
      if (neighbours.includes(qs[i].correctIndex)) continue;
      const a = qs[i].correctIndex, b = qs[j].correctIndex;
      placeKey(qs[i], b);
      placeKey(qs[j], a);
      swaps++;
      break;
    }
  }
  return swaps;
}

/** Report a per-(section,width) distribution and whether it is inside limits. */
export function distribution(exam) {
  const L = 'ABCDE';
  const groups = {};
  for (const q of exam.questions) {
    const k = `${q.section}/w${q.choices.length}`;
    (groups[k] = groups[k] || []).push(q);
  }
  const rows = [];
  for (const [k, qs] of Object.entries(groups)) {
    const w = qs[0].choices.length;
    const uniform = 100 / w;
    const counts = {};
    qs.forEach((q) => { const l = L[q.correctIndex]; counts[l] = (counts[l] || 0) + 1; });
    const shares = [...Array(w)].map((_, i) => ({
      letter: L[i], n: counts[L[i]] || 0, pct: (100 * (counts[L[i]] || 0)) / qs.length,
    }));
    const worst = Math.max(...shares.map((s) => Math.abs(s.pct - uniform)));
    const limit = qs.length >= 30 ? 12 : 20;
    rows.push({ group: k, n: qs.length, width: w, uniform, shares, worst, limit, over: worst > limit });
  }
  let run = 1, maxRun = 1;
  for (let i = 1; i < exam.questions.length; i++) {
    run = exam.questions[i].correctIndex === exam.questions[i - 1].correctIndex ? run + 1 : 1;
    maxRun = Math.max(maxRun, run);
  }
  return { rows, maxRun, needsWork: rows.some((r) => r.over) || maxRun > 3 };
}
