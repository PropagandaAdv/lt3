const { chromium } = require('playwright');
const url = process.argv[2];
const out = '/home/user/lt3/review/shots/';
(async () => {
  const b = await chromium.launch();
  for (const [name, vp, pts] of [['d', {width:1440,height:900}, [0,0.12,0.5,0.78,0.97]], ['m', {width:390,height:844}, [0,0.2]]]) {
    const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: 1, isMobile: name==='m' });
    const p = await ctx.newPage();
    const errs = [];
    p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
    p.on('pageerror', e => errs.push('PAGEERR '+e.message));
    if (process.env.FIXID) { await p.route('**/*', async r => { const q=r.request(); if (q.resourceType()==='document') { const resp=await r.fetch(); let t=await resp.text(); for (const kv of process.env.FIXID.split(',')) { const [id,css]=kv.split(':'); t=t.replace('data-id="'+id+'"','id="'+css+'" data-id="'+id+'"'); } if (process.env.FIXJS) { t=t.replace("(function(){\nvar root=document.getElementById('sec-hero')","document.addEventListener('DOMContentLoaded',function(){\nvar root=document.getElementById('sec-hero')").replace('})();\n</script>','});\n</script>'); } await r.fulfill({response:resp, body:t}); } else r.continue(); }); }
    await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 }).catch(e => errs.push('goto '+e.message));
    await p.waitForTimeout(2500);
    const info = await p.evaluate(() => ({h: document.documentElement.scrollHeight, hero: !!document.getElementById('sec-hero'), title: document.title, vid: !!document.querySelector('.lt3-vid'), ok: !!document.querySelector('.lt3-media.ok'), hdr: !!document.querySelector('.lt3-header'), ovx: document.documentElement.scrollWidth > innerWidth}));
    console.log(name, JSON.stringify(info), errs.slice(0,5).join(' | '));
    const H = info.h - vp.height;
    for (const f of pts) {
      await p.evaluate(y => window.scrollTo(0, y), Math.round((name==='d'? 6.0*vp.height : H) * f));
      await p.waitForTimeout(1400);
      await p.screenshot({ path: `${out}${name}_${String(Math.round(f*100)).padStart(3,'0')}.png` });
    }
    await ctx.close();
  }
  await b.close();
})();
