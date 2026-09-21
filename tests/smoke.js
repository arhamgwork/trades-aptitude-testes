// Browser smoke test: every exam starts, answers, submits, shows results and
// renders its print view — with zero console errors and zero third-party requests.
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

// This environment ships Chromium at a fixed path and blocks browser downloads,
// so prefer that binary when it is present and fall back to Playwright's own.
function launchOptions() {
  const pinned = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
  const opts = { args: ['--no-sandbox', '--disable-dev-shm-usage'] };
  if (fs.existsSync(pinned)) opts.executablePath = pinned;
  return opts;
}
import { serve } from './server.js';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIST = path.join(ROOT, 'dist');

let failures = 0;
const log = (ok, msg) => {
  if (!ok) failures++;
  console.log(`${ok ? '  ok  ' : '  FAIL'} ${msg}`);
};

async function main() {
  if (!fs.existsSync(DIST)) {
    console.error('dist/ is missing — run the build first');
    process.exit(1);
  }
  const { server, port } = await serve(DIST);
  const base = `http://127.0.0.1:${port}`;
  const browser = await chromium.launch(launchOptions());
  const catalog = JSON.parse(fs.readFileSync(path.join(DIST, 'data', 'index.json'), 'utf8'));

  const pageErrors = [];
  const offsite = [];

  const ctx = await browser.newContext();
  ctx.on('page', (p) => {
    p.on('console', (m) => {
      if (m.type() === 'error') pageErrors.push(`${p.url()} :: ${m.text()}`);
    });
    p.on('pageerror', (e) => pageErrors.push(`${p.url()} :: ${e.message}`));
    p.on('request', (r) => {
      const u = new URL(r.url());
      if (u.hostname !== '127.0.0.1' && u.protocol !== 'data:' && u.protocol !== 'blob:') {
        offsite.push(r.url());
      }
    });
  });

  const page = await ctx.newPage();

  // ---------- home
  await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
  log(await page.locator('h1').first().isVisible(), 'home page renders');
  log((await page.locator('.notice').first().textContent() || '').includes('Unofficial practice material'),
    'home shows the unofficial-practice notice');

  // ---------- each trade page
  for (const t of catalog.trades) {
    await page.goto(`${base}/trade.html?trade=${t.slug}`, { waitUntil: 'networkidle' });
    log(await page.locator('h1').first().isVisible(), `trade page renders: ${t.slug}`);
    log(await page.locator('.badge').first().isVisible(), `trade page shows a confidence badge: ${t.slug}`);
  }

  // ---------- each exam: start, answer, submit, results
  for (const t of catalog.trades) {
    for (const e of t.exams) {
      await runExam(page, base, e);
      await checkPrint(page, base, e);
      await checkSingle(base, e);
    }
  }

  // ---------- timer auto-advance (the section clock must move you along)
  await checkAutoAdvance(browser, base, catalog);

  // ---------- drills + progress
  await page.goto(`${base}/drills.html`, { waitUntil: 'networkidle' });
  log(await page.locator('h1').first().isVisible(), 'skill drills page renders');
  const firstDrill = page.locator('.card button').first();
  if (await firstDrill.count()) {
    await firstDrill.click();
    await page.locator('button:has-text("10 questions"), button:has-text("Start drill")').first().click();
    await page.waitForSelector('fieldset.choices', { timeout: 5000 });
    log(true, 'a drill starts and shows questions');
    await page.locator('.choice').first().click();
    await page.locator('button:has-text("Submit")').first().click();
    await page.locator('dialog button:has-text("Submit and see results")').click();
    await page.waitForSelector('.score', { timeout: 5000 });
    log(true, 'a drill submits and shows results');
  }

  await page.goto(`${base}/progress.html`, { waitUntil: 'networkidle' });
  log(await page.locator('h1').first().isVisible(), 'progress page renders');
  log(await page.locator('table').first().isVisible().catch(() => false)
      || (await page.locator('.muted').first().isVisible()),
    'progress shows history or an empty-state message');

  // ---------- offline mode really works, not just registers
  await checkOffline(browser, base);

  // ---------- storage-unavailable path
  const blocked = await browser.newContext();
  await blocked.addInitScript(() => {
    Object.defineProperty(window, 'localStorage', {
      get() { throw new Error('blocked'); },
    });
  });
  const bp = await blocked.newPage();
  const bErr = [];
  bp.on('pageerror', (e) => bErr.push(e.message));
  await bp.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
  log(await bp.locator('h1').first().isVisible() && bErr.length === 0,
    'home still works with localStorage unavailable');
  await bp.goto(`${base}/progress.html`, { waitUntil: 'networkidle' });
  log(await bp.locator('h1').first().isVisible() && bErr.length === 0,
    'progress still works with localStorage unavailable');
  await blocked.close();

  // ---------- global assertions
  log(pageErrors.length === 0, `zero console errors (${pageErrors.length})`);
  pageErrors.slice(0, 10).forEach((e) => console.log('       ' + e));
  log(offsite.length === 0, `zero third-party requests (${offsite.length})`);
  offsite.slice(0, 10).forEach((u) => console.log('       ' + u));

  await browser.close();
  server.close();

  console.log(failures ? `\nSMOKE TEST FAILED (${failures})` : '\nsmoke test passed');
  process.exit(failures ? 1 : 0);
}

async function runExam(page, base, e) {
  await page.goto(`${base}/exam.html?exam=${e.id}`, { waitUntil: 'networkidle' });
  log(await page.locator('h1').first().isVisible(), `exam setup renders: ${e.id}`);

  // untimed full run so the test is not racing a clock
  await page.locator('input[name="timer"][value="untimed"]').check();
  await page.locator('button[type=submit]:has-text("Start")').click();
  await page.waitForSelector('fieldset.choices', { timeout: 8000 });
  log(true, `exam starts: ${e.id}`);

  // answer the first question of each section via the keyboard, then click through
  let answered = 0;
  for (let s = 0; s < e.sections.length; s++) {
    await page.keyboard.press('a');
    answered++;
    const nextSection = page.locator('button:has-text("Next section")');
    // jump to the last question of the section using the grid
    const gridBtns = page.locator('.qgrid button');
    const n = await gridBtns.count();
    if (n > 1) await gridBtns.nth(n - 1).click();
    await page.locator('.choice').first().click();
    answered++;
    if (await nextSection.count()) await nextSection.first().click();
  }
  log(answered >= e.sections.length, `questions answerable in every section: ${e.id}`);

  // flag + grid state
  await page.goto(`${base}/exam.html?exam=${e.id}`, { waitUntil: 'networkidle' });
  await page.locator('input[name="timer"][value="untimed"]').check();
  await page.locator('button[type=submit]:has-text("Start")').click();
  await page.waitForSelector('fieldset.choices');
  await page.keyboard.press('f');
  log(await page.locator('.qgrid button.flagged').count() > 0, `flagging marks the grid: ${e.id}`);
  await page.keyboard.press('b');
  log(await page.locator('.qgrid button.answered').count() > 0, `answering marks the grid: ${e.id}`);

  await page.locator('.examtop button:has-text("Submit")').click();
  await page.waitForSelector('dialog[open]');
  log(true, `submit asks for confirmation: ${e.id}`);
  await page.locator('dialog button:has-text("Submit and see results")').click();
  await page.waitForSelector('.score', { timeout: 8000 });
  const score = await page.locator('.score').textContent();
  log(/%$/.test((score || '').trim()), `results show a score: ${e.id} (${score})`);
  log(await page.locator('.review').count() === e.totalQuestions,
    `results review every question: ${e.id}`);
  log(await page.locator('table').first().isVisible(), `results show a per-section table: ${e.id}`);
}

async function checkOffline(browser, base) {
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  await page.goto(`${base}/index.html`, { waitUntil: 'networkidle' });
  const registered = await page.evaluate(async () => {
    if (!('serviceWorker' in navigator)) return false;
    const reg = await navigator.serviceWorker.ready.catch(() => null);
    return !!reg;
  });
  log(registered, 'service worker registers');
  if (!registered) { await ctx.close(); return; }

  // prime the cache with a trade page and an exam bank
  await page.goto(`${base}/trade.html?trade=electrical`, { waitUntil: 'networkidle' });
  await page.goto(`${base}/exam.html?exam=ibew-701-formA`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(600);

  await ctx.setOffline(true);
  await page.goto(`${base}/index.html`, { waitUntil: 'domcontentloaded' });
  const homeOk = await page.locator('h1').first().isVisible().catch(() => false);
  log(homeOk, 'home page loads with the network offline');

  await page.goto(`${base}/exam.html?exam=ibew-701-formA`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(400);
  const examOffline = await page.locator('button[type=submit]:has-text("Start")').count();
  log(examOffline > 0, 'an exam still loads its question bank offline');
  log(errs.length === 0, `no page errors while offline (${errs.length})`);
  await ctx.setOffline(false);
  await ctx.close();
}

async function checkAutoAdvance(browser, base, catalog) {
  const e = catalog.trades.flatMap((t) => t.exams).find((x) => x.sections.length > 1);
  if (!e) { log(true, 'auto-advance: no multi-section exam to test (skipped)'); return; }
  // Service workers are blocked here: this test rewrites the exam JSON with a
  // route, and a worker serving its cached copy would defeat that.
  const ctx = await browser.newContext({ serviceWorkers: 'block' });
  const page = await ctx.newPage();
  // Shorten the real section limits so the countdown can actually expire here.
  await page.route(`**/data/exams/${e.id}.json`, async (route) => {
    const res = await route.fetch();
    const json = await res.json();
    json.sections.forEach((s) => { s.timeLimitSec = 2; });
    await route.fulfill({ json });
  });
  await page.goto(`${base}/exam.html?exam=${e.id}`, { waitUntil: 'networkidle' });
  await page.locator('input[name="timer"][value="real"]').check();
  await page.locator('button[type=submit]:has-text("Start")').click();
  await page.waitForSelector('fieldset.choices');

  const first = await page.locator('.examtop .meta').nth(1).textContent();
  log(/Section 1 of/.test(first || ''), `starts in section 1: ${e.id}`);

  // section 1 expires -> must land in section 2 without any click
  await page.waitForFunction(
    () => /Section 2 of/.test(document.querySelectorAll('.examtop .meta')[1]?.textContent || ''),
    null, { timeout: 8000 },
  ).then(() => log(true, `section timer auto-advances to the next section: ${e.id}`))
   .catch(() => log(false, `section timer auto-advances to the next section: ${e.id}`));

  // last section expires -> exam ends and results appear on their own
  await page.waitForSelector('.score', { timeout: 10000 })
    .then(() => log(true, `final section timeout ends the exam and shows results: ${e.id}`))
    .catch(() => log(false, `final section timeout ends the exam and shows results: ${e.id}`));
  await page.close();
  await ctx.close();
}

async function checkPrint(page, base, e) {
  await page.goto(`${base}/print.html?exam=${e.id}`, { waitUntil: 'networkidle' });
  const n = await page.locator('.printq').count();
  log(n === e.totalQuestions * 2, `print view has booklet and key: ${e.id} (${n} blocks)`);
  await page.emulateMedia({ media: 'print' });
  log(await page.locator('h1').first().isVisible(), `print media renders: ${e.id}`);
  await page.emulateMedia({ media: 'screen' });
}

async function checkSingle(base, e) {
  const f = path.join(DIST, 'single', `${e.id}.html`);
  const exists = fs.existsSync(f);
  log(exists, `single-file copy exists: ${e.id}`);
  if (exists) {
    const html = fs.readFileSync(f, 'utf8');
    log(!/<script[^>]+src=/i.test(html), `single-file copy has no external scripts: ${e.id}`);
    log(html.includes('Answer key'), `single-file copy includes the answer key: ${e.id}`);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
