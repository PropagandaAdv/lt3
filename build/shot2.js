const { chromium } = require('playwright');
const out = '/home/user/lt3/review/shots/';
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: {width:1440,height:900} });
  const p = await ctx.newPage(); const errs=[];
  p.on('console', m => { if (m.type()==='error') errs.push(m.text()); }); p.on('pageerror', e => errs.push('PAGEERR '+e.message));
  await p.goto('http://localhost:8765/', {waitUntil:'load', timeout:60000}); await p.waitForTimeout(2500);
  const info = await p.evaluate(() => ({ok: !!document.querySelector('.media.ok'), h: document.documentElement.scrollHeight, ovx: document.documentElement.scrollWidth>innerWidth}));
  console.log('desktop', JSON.stringify(info), errs.join('|'));
  const range = 7*900 - 900*1.4;
  for (const f of [0,0.15,0.45,0.78,0.97]) { await p.evaluate(y => window.scrollTo(0,y), Math.round(range*f)); await p.waitForTimeout(1600); await p.screenshot({path: out+'x_d_'+String(Math.round(f*100)).padStart(3,'0')+'.png'}); }
  const hh = await p.evaluate(() => document.getElementById('sec-hero').offsetHeight);
  for (const [n,id] of [['anime','sec-anime'],['metodo','sec-metodo'],['contatti','sec-contatti']]) { await p.evaluate(i => document.getElementById(i).scrollIntoView(), id); await p.waitForTimeout(2200); await p.screenshot({path: out+'x_d_'+n+'.png'}); }
  await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight)); await p.waitForTimeout(800); await p.screenshot({path: out+'x_d_footer.png'});
  await ctx.close();
  const m = await b.newContext({ viewport: {width:390,height:844}, isMobile:true, deviceScaleFactor:2 });
  const q = await m.newPage(); const e2=[]; q.on('pageerror', e => e2.push(e.message));
  await q.goto('http://localhost:8765/', {waitUntil:'load', timeout:60000}); await q.waitForTimeout(1500);
  console.log('mobile', JSON.stringify(await q.evaluate(()=>({h:document.documentElement.scrollHeight, ovx: document.documentElement.scrollWidth>innerWidth}))), e2.join('|'));
  await q.screenshot({path: out+'x_m_full.png', fullPage:true});
  await b.close();
})();
