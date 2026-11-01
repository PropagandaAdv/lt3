const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({viewport:{width:1440,height:900}})).newPage();
  await p.route('**/*', async r => { if (r.request().resourceType()==='document') { const resp=await r.fetch(); let t=await resp.text(); t=t.replace('data-id="d2495ad3"','id="sec-hero" data-id="d2495ad3"'); await r.fulfill({response:resp, body:t}); } else r.continue(); });
  await p.goto(process.argv[2], {waitUntil:'networkidle'}); await p.waitForTimeout(2500);
  console.log(JSON.stringify(await p.evaluate(() => [...document.querySelectorAll('.lt3-cap')].map(c => { const s=getComputedStyle(c), r=c.getBoundingClientRect(); return {cls:c.className, pos:s.position, op:s.opacity, z:s.zIndex, x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height), disp:s.display}; })), null, 0));
  console.log(await p.evaluate(() => { const s=document.querySelector('.lt3-stage'); const r=s.getBoundingClientRect(); return JSON.stringify({pos:getComputedStyle(s).position,h:r.height,w:r.width,top:r.top, scrim:getComputedStyle(document.querySelector('.lt3-scrim')).opacity}); }));
  await b.close();
})();
