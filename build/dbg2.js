const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({viewport:{width:1440,height:900}})).newPage();
  p.on('console', m => console.log('CONSOLE', m.type(), m.text()));
  p.on('pageerror', e => console.log('PAGEERR', e.message));
  await p.route('**/*', async r => { if (r.request().resourceType()==='document') { const resp=await r.fetch(); let t=await resp.text(); t=t.replace('data-id="d2495ad3"','id="sec-hero" data-id="d2495ad3"'); await r.fulfill({response:resp, body:t}); } else r.continue(); });
  await p.goto(process.argv[2], {waitUntil:'networkidle'}); await p.waitForTimeout(2000);
  console.log(await p.evaluate(() => { const c=document.querySelector('.lt3-cap-1'); const before=c.className; c.classList.add('on'); const cs=getComputedStyle(c); return JSON.stringify({before, after:c.className, op:cs.opacity, tr:cs.transition}); }));
  const rules = await p.evaluate(() => { const out=[]; for (const ss of document.styleSheets) { try { for (const r of ss.cssRules) { if (r.cssText.includes('lt3-cap') ) out.push(r.cssText.slice(0,200)); } } catch(e){} } return out; });
  console.log(rules.join('\n'));
  await b.close();
})();
