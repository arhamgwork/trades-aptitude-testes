// Pulls data declarations out of the single-file source exams by evaluating
// just the literal, so migration is exact rather than regex-scraped.
import fs from 'node:fs';
import vm from 'node:vm';

/** Find `<kw> NAME = <literal>` and return the literal source by brace matching. */
export function declSource(src, name) {
  const re = new RegExp(`(?:const|let|var)\\s+${name}\\s*=\\s*`, 'g');
  const m = re.exec(src);
  if (!m) return null;
  let i = m.index + m[0].length;
  const open = src[i];
  const close = open === '[' ? ']' : open === '{' ? '}' : null;
  if (!close) return null;
  let depth = 0, inStr = null, esc = false;
  for (let j = i; j < src.length; j++) {
    const c = src[j];
    if (inStr) {
      if (esc) esc = false;
      else if (c === '\\') esc = true;
      else if (c === inStr) inStr = null;
      continue;
    }
    if (c === '"' || c === "'" || c === '`') { inStr = c; continue; }
    if (c === open) depth++;
    else if (c === close) {
      depth--;
      if (depth === 0) return src.slice(i, j + 1);
    }
  }
  return null;
}

export function evalLiteral(source) {
  return vm.runInNewContext(`(${source})`, Object.create(null), { timeout: 5000 });
}

/** Replay a sequence of `push(...)` calls into an array. */
export function replayPushes(src, startMarker, pushName = 'push') {
  const start = src.indexOf(startMarker);
  if (start < 0) throw new Error(`marker not found: ${startMarker}`);
  const tail = src.slice(start);
  const calls = [];
  // Exclude `X.push(` so the helper's own definition is not replayed.
  const re = new RegExp(`(?<![.\\w])${pushName}\\s*\\(`, 'g');
  let m;
  while ((m = re.exec(tail))) {
    let i = m.index + m[0].length;
    let depth = 1, inStr = null, esc = false;
    for (; i < tail.length && depth > 0; i++) {
      const c = tail[i];
      if (inStr) {
        if (esc) esc = false;
        else if (c === '\\') esc = true;
        else if (c === inStr) inStr = null;
        continue;
      }
      if (c === '"' || c === "'" || c === '`') { inStr = c; continue; }
      if (c === '(') depth++;
      else if (c === ')') depth--;
    }
    calls.push(tail.slice(m.index + m[0].length, i - 1));
  }
  const out = [];
  const ctx = vm.createContext({
    __collect: (...args) => out.push(args),
  });
  for (const argSrc of calls) {
    vm.runInContext(`__collect(${argSrc})`, ctx, { timeout: 5000 });
  }
  return out;
}

export function readHTML(file) {
  return fs.readFileSync(file, 'utf8');
}

export function stripTags(html) {
  return String(html)
    .replace(/<br\s*\/?>/gi, ' ')
    // Only strip real HTML tags. A bare "<" in maths ("if x < 0 and y > 0")
    // must survive, so require a tag name straight after the angle bracket.
    .replace(/<\/?[a-zA-Z][a-zA-Z0-9:-]*(?:\s[^>]*)?>/g, '')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&mdash;/g, '—').replace(/&ndash;/g, '–')
    .replace(/&times;/g, '×').replace(/&divide;/g, '÷')
    .replace(/&minus;/g, '−').replace(/&deg;/g, '°')
    .replace(/&quot;/g, '"').replace(/&#39;/g, "'")
    .replace(/\s+/g, ' ')
    .trim();
}

/**
 * Run a source file's whole <script> body in a sandbox with a stub DOM, then
 * read named globals out of it. This captures every helper the data relies on
 * (figure builders, stem formatters) exactly as the source defined them.
 */
export function runScriptCapture(html, names) {
  const scripts = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)]
    .map((m) => m[1])
    .filter((s) => s.trim());
  const stubEl = () => new Proxy(function () {}, {
    get(t, k) {
      if (k === 'style' || k === 'dataset' || k === 'classList') return stubEl();
      if (k === 'children' || k === 'childNodes') return [];
      if (k === Symbol.toPrimitive || k === 'toString') return () => '';
      if (k === 'length') return 0;
      return stubEl();
    },
    set() { return true; },
    apply() { return stubEl(); },
    has() { return true; },
  });
  const doc = {
    getElementById: () => stubEl(), querySelector: () => stubEl(),
    querySelectorAll: () => [], createElement: () => stubEl(),
    addEventListener() {}, removeEventListener() {},
    body: stubEl(), documentElement: stubEl(), head: stubEl(),
  };
  const sandbox = {
    document: doc,
    window: { addEventListener() {}, removeEventListener() {}, location: { search: '', href: '' }, matchMedia: () => ({ matches: false, addEventListener() {} }) },
    navigator: { userAgent: 'node' },
    localStorage: { getItem: () => null, setItem() {}, removeItem() {} },
    setTimeout() {}, clearTimeout() {}, setInterval() {}, clearInterval() {},
    console: { log() {}, warn() {}, error() {} },
    Math, JSON, Date, Array, Object, String, Number, Boolean, RegExp, Error,
    parseInt, parseFloat, isNaN, encodeURIComponent, decodeURIComponent,
  };
  sandbox.window.document = doc;
  sandbox.globalThis = sandbox;
  const ctx = vm.createContext(sandbox);
  const errors = [];
  for (const s of scripts) {
    try {
      vm.runInContext(s, ctx, { timeout: 15000 });
    } catch (e) {
      errors.push(e.message);
    }
  }
  const out = {};
  for (const n of names) {
    try { out[n] = vm.runInContext(n, ctx); } catch { out[n] = undefined; }
  }
  return { data: out, errors };
}
