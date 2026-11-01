// usage: node render.mjs stills 1 3.2 8.6 ...   -> stills/t_<t>.png
//        node render.mjs cover                  -> cover.png
//        node render.mjs frames [fps] [workers] -> frames/f_00000.png ...
import { createRequire } from 'module';
const { chromium } = createRequire(import.meta.url)('playwright'); // global Playwright install
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const url = 'file://' + path.join(dir, 'film.html');
const [mode, ...rest] = process.argv.slice(2);

const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
async function openPage(q = '') {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  page.on('console', m => console.log('[page]', m.text()));
  page.on('pageerror', e => { console.log('[error]', e.message); process.exitCode = 1; });
  await page.goto(url + q);
  await page.evaluate(() => window.ready);
  return page;
}
const png = page => page.evaluate(() => document.getElementById('c').toDataURL('image/png').split(',')[1]);
async function grab(page, t, file) {
  await page.evaluate(t => renderAt(t), t);
  fs.writeFileSync(file, Buffer.from(await png(page), 'base64'));
}

if (mode === 'stills') {
  fs.mkdirSync(path.join(dir, 'stills'), { recursive: true });
  const page = await openPage();
  for (const t of rest.map(Number)) await grab(page, t, path.join(dir, 'stills', `t_${t.toFixed(2)}.png`));
} else if (mode === 'cover') {
  const page = await openPage('?cover');
  fs.writeFileSync(path.join(dir, 'cover.png'), Buffer.from(await png(page), 'base64'));
} else {
  const fps = +(rest[0] || 30), workers = +(rest[1] || 4);
  const page0 = await openPage(); const dur = await page0.evaluate(() => T.DUR); await page0.close();
  const total = Math.round(dur * fps), out = path.join(dir, 'frames'); fs.mkdirSync(out, { recursive: true });
  let next = 0; const t0 = Date.now();
  await Promise.all(Array.from({ length: workers }, async () => {
    const page = await openPage();
    while (next < total) {
      const i = next++;
      await grab(page, i / fps, path.join(out, `f_${String(i).padStart(5, '0')}.png`));
      if (i % 100 === 0) console.log(`frame ${i}/${total} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
  }));
}
await browser.close();
