// Progress storage. Every access is wrapped: the app works fully with no
// storage at all (private windows, blocked site data), it just forgets.
const KEY = 'tap.v1';
const EMPTY = { attempts: [], resume: null, version: 1 };

let memory = null;          // in-memory fallback, always present
let storageOK = true;

function raw() {
  try {
    const t = '__tap_probe__';
    window.localStorage.setItem(t, '1');
    window.localStorage.removeItem(t);
    return window.localStorage;
  } catch {
    storageOK = false;
    return null;
  }
}

export function storageAvailable() {
  if (memory === null) load();
  return storageOK;
}

export function load() {
  if (memory !== null) return memory;
  const ls = raw();
  if (!ls) { memory = structuredClone(EMPTY); return memory; }
  try {
    const txt = ls.getItem(KEY);
    memory = txt ? { ...structuredClone(EMPTY), ...JSON.parse(txt) } : structuredClone(EMPTY);
  } catch {
    // Corrupt or unreadable payload: start clean rather than breaking the app.
    storageOK = false;
    memory = structuredClone(EMPTY);
  }
  return memory;
}

export function save(next) {
  memory = next;
  const ls = raw();
  if (!ls) return false;
  try {
    ls.setItem(KEY, JSON.stringify(next));
    return true;
  } catch {
    storageOK = false;   // quota or blocked mid-session
    return false;
  }
}

export function recordAttempt(attempt) {
  const st = load();
  st.attempts.unshift(attempt);
  if (st.attempts.length > 200) st.attempts.length = 200;
  save(st);
  return attempt;
}

export function attempts() { return load().attempts; }

export function setResume(r) { const st = load(); st.resume = r; save(st); }
export function getResume() { return load().resume; }
export function clearResume() { setResume(null); }

export function clearAll() {
  memory = structuredClone(EMPTY);
  const ls = raw();
  try { if (ls) ls.removeItem(KEY); } catch { /* nothing to do */ }
}

/** Per-skill accuracy across all recorded attempts. */
export function skillStats() {
  const acc = {};
  for (const a of attempts()) {
    for (const r of a.perQuestion || []) {
      for (const s of r.skills || []) {
        acc[s] = acc[s] || { right: 0, total: 0 };
        acc[s].total++;
        if (r.correct) acc[s].right++;
      }
    }
  }
  return acc;
}

export function weakSkills(minAttempted = 3, limit = 8) {
  const st = skillStats();
  return Object.entries(st)
    .filter(([, v]) => v.total >= minAttempted)
    .map(([k, v]) => ({ skill: k, ...v, pct: v.right / v.total }))
    .sort((a, b) => a.pct - b.pct || b.total - a.total)
    .slice(0, limit);
}

export function exportJSON() {
  return JSON.stringify(load(), null, 1);
}

export function importJSON(text) {
  const data = JSON.parse(text);
  if (!data || typeof data !== 'object' || !Array.isArray(data.attempts)) {
    throw new Error('That file is not a progress export from this site.');
  }
  const merged = structuredClone(EMPTY);
  merged.attempts = data.attempts;
  merged.resume = data.resume ?? null;
  save(merged);
  return merged.attempts.length;
}
