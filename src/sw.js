// Offline support. Caches this site's own files only; there is nothing
// third-party to cache, and the worker never talks to another origin.
const VERSION = 'tap-v1';
const CORE = [
  'index.html', 'trade.html', 'exam.html', 'drills.html', 'progress.html',
  'print.html', 'favicon.svg', 'manifest.webmanifest',
  'css/app.css',
  'js/util.js', 'js/store.js', 'js/catalog.js', 'js/runner.js', 'js/results.js',
  'js/page-index.js', 'js/page-trade.js', 'js/page-exam.js',
  'js/page-drills.js', 'js/page-progress.js', 'js/page-print.js',
  'data/index.json',
];

self.addEventListener('install', (ev) => {
  ev.waitUntil((async () => {
    const cache = await caches.open(VERSION);
    // Individual misses must not fail the whole install.
    await Promise.all(CORE.map((u) => cache.add(u).catch(() => {})));
    // Pull every exam bank in too, so a loaded site works fully offline.
    try {
      const res = await fetch('data/index.json');
      const idx = await res.json();
      const ids = (idx.trades || []).flatMap((t) => (t.exams || []).map((e) => e.id));
      await Promise.all([...new Set(ids)].map(
        (id) => cache.add(`data/exams/${id}.json`).catch(() => {})));
    } catch { /* offline at install time: the fetch handler will fill the cache later */ }
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', (ev) => {
  ev.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', (ev) => {
  const req = ev.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;   // never touch other origins

  ev.respondWith((async () => {
    const cache = await caches.open(VERSION);
    try {
      // Network first, so a redeploy is picked up while online.
      const fresh = await fetch(req);
      if (fresh && fresh.ok) cache.put(req, fresh.clone());
      return fresh;
    } catch {
      const hit = await cache.match(req);
      if (hit) return hit;
      if (req.mode === 'navigate') {
        const home = await cache.match('index.html');
        if (home) return home;
      }
      return new Response(
        'This page is not available offline yet. Open it once while online and it will be stored.',
        { status: 503, headers: { 'content-type': 'text/plain; charset=utf-8' } });
    }
  })());
});
