// Shared helpers. No dependencies, no network beyond this site's own files.
export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
export const LETTERS = ['A', 'B', 'C', 'D', 'E'];

export function el(tag, attrs, ...kids) {
  const n = document.createElement(tag);
  // Callers pass null for "no attributes", which a default parameter would not
  // catch, so normalise here rather than at every call site.
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === 'class') n.className = v;
    else if (k === 'text') n.textContent = v;
    else if (k.startsWith('on') && typeof v === 'function') {
      n.addEventListener(k.slice(2).toLowerCase(), v);
    } else n.setAttribute(k, v === true ? '' : String(v));
  }
  for (const kid of kids.flat()) {
    if (kid === null || kid === undefined || kid === false) continue;
    n.appendChild(typeof kid === 'string' ? document.createTextNode(kid) : kid);
  }
  return n;
}

export function fmtClock(sec) {
  const s = Math.max(0, Math.round(sec));
  const m = Math.floor(s / 60);
  return `${String(m).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
}

export function fmtDuration(sec) {
  const s = Math.max(0, Math.round(sec));
  const m = Math.floor(s / 60);
  const rem = s % 60;
  if (m < 60) return rem ? `${m} min ${rem}s` : `${m} min`;
  return `${Math.floor(m / 60)} h ${m % 60} min`;
}

export function qs(name, dflt = null) {
  return new URLSearchParams(location.search).get(name) ?? dflt;
}

export function pct(n, d) { return d ? Math.round((n / d) * 100) : 0; }

/** Render a trusted inline SVG string from our own validated data files. */
export function svgFigure(markup, label) {
  const fig = el('figure', { class: 'fig' });
  const holder = el('div', { role: 'img', 'aria-label': label || 'figure' });
  holder.innerHTML = markup;
  fig.appendChild(holder);
  return fig;
}

/**
 * Render one choice. Paper-folding style questions use pictures rather than
 * text, so the choice body is markup from our own validated data files.
 */
export function choiceBody(q, i) {
  const raw = q.choices[i];
  if (!q.choicesAreFigures) return el('span', null, raw);
  const holder = el('span', { class: 'choicefig', role: 'img', 'aria-label': `Option ${LETTERS[i]}, diagram` });
  holder.innerHTML = raw;
  return holder;
}

/** Plain-text stand-in for a picture choice, for print and screen readers. */
export function choiceText(q, i) {
  return q.choicesAreFigures ? `Diagram ${LETTERS[i]}` : q.choices[i];
}

export function announce(msg) {
  let live = document.getElementById('live-region');
  if (!live) {
    live = el('div', {
      id: 'live-region', 'aria-live': 'polite', 'aria-atomic': 'true',
      style: 'position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap',
    });
    document.body.appendChild(live);
  }
  live.textContent = msg;
}

export function siteHeader(current) {
  const links = [
    ['index.html', 'Home'], ['drills.html', 'Skill drills'],
    ['progress.html', 'Progress'],
  ];
  return el('header', { class: 'site' },
    el('div', { class: 'bar' },
      el('a', { class: 'brand', href: 'index.html', text: 'Trades Aptitude Practice' }),
      el('nav', { 'aria-label': 'Main' },
        links.map(([href, label]) => el('a', {
          href, text: label, 'aria-current': href === current ? 'page' : null,
        })))));
}

export const DISCLAIMER =
  'Unofficial practice material, not affiliated with any union, JATC, or test publisher.';

export function disclaimerNote() {
  return el('p', { class: 'notice', text: DISCLAIMER });
}

export function mountChrome(current) {
  document.body.prepend(siteHeader(current));
}
