// Loads the site's own JSON data. Same-origin fetch only.
const cache = new Map();

async function getJSON(path) {
  if (cache.has(path)) return cache.get(path);
  const p = fetch(path, { cache: 'no-cache' }).then((r) => {
    if (!r.ok) throw new Error(`Could not load ${path} (${r.status})`);
    return r.json();
  });
  cache.set(path, p);
  return p;
}

export function loadIndex() { return getJSON('data/index.json'); }
export function loadExam(id) { return getJSON(`data/exams/${id}.json`); }
export function loadDrill(skillFile) { return getJSON(`data/drills/${skillFile}.json`); }

export async function findExamMeta(id) {
  const idx = await loadIndex();
  for (const t of idx.trades) {
    const e = (t.exams || []).find((x) => x.id === id);
    if (e) return { exam: e, trade: t };
  }
  return null;
}
