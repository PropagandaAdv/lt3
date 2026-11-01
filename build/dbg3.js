const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({viewport:{width:1440,height:900}})).newPage();
  await p.goto(process.argv[2], {waitUntil:'networkidle'});
  console.log(await p.evaluate(() => [...document.querySelectorAll('.e-con:not(.e-child)')].map(e => e.outerHTML.slice(0,260).replace(/\s+/g,' ')).join('\n---\n')));
  await b.close();
})();
