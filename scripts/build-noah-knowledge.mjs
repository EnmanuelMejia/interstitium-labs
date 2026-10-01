/**
 * build-noah-knowledge.mjs — Noah answer-engine knowledge bundle.
 *
 * Crawls the site's curriculum pages (docs/learn, docs/paths, docs/academy,
 * plus coach/labs/adapt/prep/interview) and emits a compact JSON bundle at
 * docs/assets/noah-knowledge.json. The on-device Noah engine searches this
 * bundle (keyword + topic matching) and answers with cited on-site links.
 *
 * HONESTY RULE: every entry is extracted from real page content — title, meta
 * description, or first substantive paragraphs. Nothing is invented. Re-run
 * after curriculum changes:  node scripts/build-noah-knowledge.mjs
 */
import { readdirSync, readFileSync, writeFileSync, statSync } from 'node:fs';
import { join, relative, sep } from 'node:path';

const DOCS = new URL('../docs/', import.meta.url).pathname;
const OUT = new URL('../docs/assets/noah-knowledge.json', import.meta.url).pathname;

const ROOTS = ['learn', 'paths', 'academy'];
const EXTRA = [
  'coach/index.html',
  'labs/index.html',
  'labs/superlab/index.html',
  'adapt/index.html',
  'prep/index.html',
  'interview/index.html',
  'immersive/index.html',
  'cinema/index.html',
];

const STOP = new Set(('a,an,the,and,or,but,of,to,in,on,for,with,from,as,at,by,is,are,was,were,be,been,being,' +
  'it,its,this,that,these,those,you,your,we,our,they,their,he,she,his,her,will,can,may,not,no,yes,' +
  'into,over,under,between,through,than,then,so,such,all,any,each,more,most,other,some,only,also,' +
  'interstitium,labs,learn,track,path,page,guide').split(','));

function walk(dir, out) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    const st = statSync(p);
    if (st.isDirectory()) { walk(p, out); continue; }
    if (name === 'index.html') out.push(p);
  }
  return out;
}

function urlOf(file) {
  let rel = relative(DOCS, file).split(sep).join('/');
  rel = rel.replace(/\/index\.html$/, '/');
  return '/' + rel;
}

function textOf(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'")
    .replace(/\s+/g, ' ')
    .trim();
}

function unesc(s) {
  return s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'").replace(/&nbsp;/g, ' ');
}

function metaDesc(html) {
  const m = html.match(/<meta\s+name="description"\s+content="([^"]*)"/i);
  return m ? unesc(m[1]).replace(/\s+/g, ' ').trim() : '';
}

function titleOf(html) {
  const m = html.match(/<title>([^<]*)<\/title>/i);
  let t = m ? m[1].trim() : '';
  t = unesc(t).replace(/\s*[|\-–—]\s*Interstitium Labs\s*$/i, '').trim();
  return t;
}

function firstParagraphs(html, maxChars) {
  const main = html.match(/<main[\s\S]*?<\/main>/i);
  const scope = main ? main[0] : html;
  const paras = [];
  const re = /<p[^>]*>([\s\S]*?)<\/p>/gi;
  let m;
  while ((m = re.exec(scope)) && paras.join(' ').length < maxChars) {
    const t = textOf(m[1]);
    if (t.length > 60 && !/cookie|newsletter|subscribe/i.test(t)) paras.push(t);
  }
  let s = paras.join(' ');
  if (s.length > maxChars) {
    s = s.slice(0, maxChars);
    const cut = s.lastIndexOf('. ');
    s = (cut > maxChars * 0.5 ? s.slice(0, cut + 1) : s.replace(/\s+\S*$/, '')) ;
  }
  return s;
}

function keywords(url, title, desc) {
  const words = (url + ' ' + title + ' ' + desc).toLowerCase()
    .replace(/[^a-z0-9+\-#/ ]/g, ' ')
    .split(/[\s/_\-]+/)
    .filter(w => w.length > 2 && !STOP.has(w));
  return [...new Set(words)].join(' ');
}

const files = [];
for (const r of ROOTS) {
  try { walk(join(DOCS, r), files); } catch (e) { /* missing root */ }
}
for (const e of EXTRA) {
  try { const p = join(DOCS, e); statSync(p); files.push(p); } catch { /* skip */ }
}

const entries = [];
const seen = new Set();
for (const f of files.sort()) {
  const u = urlOf(f);
  if (seen.has(u) || u.includes('/404')) continue;
  seen.add(u);
  let html;
  try { html = readFileSync(f, 'utf8'); } catch { continue; }
  const t = titleOf(html);
  if (!t) continue;
  let d = metaDesc(html);
  if (d.length < 80) {
    const p = firstParagraphs(html, 420);
    if (p.length > d.length) d = p;
  }
  if (d.length > 460) d = d.slice(0, 460).replace(/\s+\S*$/, '') + '…';
  if (!d) continue;
  entries.push({ u, t, d, k: keywords(u, t, d) });
}

const bundle = {
  v: 1,
  built: new Date().toISOString().slice(0, 10),
  count: entries.length,
  entries,
};
writeFileSync(OUT, JSON.stringify(bundle));
console.log(`wrote ${OUT}: ${entries.length} entries, ${Buffer.byteLength(JSON.stringify(bundle))} bytes`);
