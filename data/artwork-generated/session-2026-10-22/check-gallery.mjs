import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const base = 'data/artwork-generated/session-2026-10-22';
const browser = await chromium.launch({executablePath:'/usr/bin/google-chrome', headless:true});
const expectedImages=JSON.parse(fs.readFileSync('data/artwork-generated/batch-2174/codex-generation-summary.json')).selected_pngs;
const results = [];
try {
  for (const width of [1440, 768, 390]) {
    const page = await browser.newPage({viewport:{width,height:900}});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('file://' + path.resolve('docs/artwork-batch-2174.html'));
    await page.locator('img').evaluateAll(images => images.forEach(image => { image.loading = 'eager'; }));
    await page.waitForFunction(() => [...document.images].every(image => image.complete), {timeout:60000});
    const measured = await page.evaluate(() => ({
      cards:document.querySelectorAll('article').length,
      images:document.images.length,
      brokenImages:[...document.images].filter(image => !image.naturalWidth).map(image => image.src),
      missingAlt:[...document.images].filter(image => !image.alt.trim()).length,
      horizontalOverflow:document.documentElement.scrollWidth > innerWidth,
      summary:document.querySelector('main > p')?.textContent,
    }));
    await page.screenshot({path:`${base}/gallery-${width}.png`});
    results.push({width,...measured,errors});
    await page.close();
  }
} finally {
  await browser.close();
}
const report = {checked_at:new Date().toISOString(),results};
fs.writeFileSync(`${base}/gallery-browser-validation.json`, JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
if (results.some(result => result.cards !== 50 || result.images !== expectedImages || result.brokenImages.length || result.missingAlt || result.horizontalOverflow || result.errors.length)) process.exitCode = 1;
