import puppeteer from '/Users/danielstroebel/Projekte/empiria/site/node_modules/puppeteer-core/lib/esm/puppeteer/puppeteer-core.js';
import fs from 'fs';
const [,, modus, ...zeiten] = process.argv;
const b = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args:['--allow-file-access-from-files'] });
const p = await b.newPage(); await p.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
await p.goto('file://' + process.cwd() + '/film.html', { waitUntil: 'networkidle0' }); await p.evaluate(() => document.fonts.ready);
const setze = async t => p.evaluate(t => { document.getAnimations().forEach(a => { a.pause(); a.currentTime = t * 1000; }); }, t);
if (modus === 'bilder') { for (const t of zeiten) { await setze(+t); await p.screenshot({ path: `bild-${t}.png` }); } }
else { fs.mkdirSync('fr', { recursive: true }); const fps = 25, n = 55 * fps; for (let i = 0; i < n; i++) { await setze(i / fps); await p.screenshot({ path: `fr/f${String(i).padStart(4, '0')}.png` }); } }
await b.close();
