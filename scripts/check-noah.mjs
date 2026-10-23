import { readFileSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
const files = ['noah-session.js', 'noah-ai.js', 'noah-workflows.js', 'noah-skills.js', 'noah-workspace.js', 'noah-neural.js', 'noah-jobs.js'];
for (const file of files) {
  const run = spawnSync(process.execPath, ['--check', `docs/assets/${file}`], { encoding: 'utf8' });
  assert.equal(run.status, 0, run.stderr);
}
const html = readFileSync('docs/noah/index.html', 'utf8');
// Page-loaded core modules only. noah-workflows.js / noah-skills.js /
// noah-workspace.js / noah-neural.js were deliberately removed from the
// page in 642bb22 (Noah Everywhere consolidation); they stay node --check
// validated above but are no longer page script tags.
for (const file of ['noah-session.js', 'noah-ai.js']) assert.ok(html.includes(`/assets/${file}`), `${file} must be loaded`);
const jobsHtml = readFileSync('docs/jobs/index.html', 'utf8');
// Jobs Suite rebuild (16e166b): the jobs page is driven by il-jobs.js; the
// legacy noah-*.js tags, Jobright bridge link, and share-consent form were
// deliberately removed in the rebuild.
assert.ok(jobsHtml.includes('/assets/il-jobs.js'), 'il-jobs.js must be loaded');
assert.ok(existsSync('docs/assets/noah-jobs.css'));
assert.ok(html.indexOf('/assets/noah-session.js') < html.indexOf('/assets/noah-ai.js'));
for (const path of ['/assets/noah-workspace.css', '/assets/chrome/sigil-glyph.svg', '/assets/noah/noah-neural.glb']) assert.ok(existsSync(`docs${path}`), path);
const graph = JSON.parse(readFileSync('docs/assets/noah/noah-neural.json'));
assert.equal(graph.nodes.length, 96); assert.equal(graph.loopSeconds, 20);
for (const e of graph.edges) assert.ok(e.length === 2 && e.every(i => Number.isInteger(i) && i >= 0 && i < graph.nodes.length));
const glb = readFileSync('docs/assets/noah/noah-neural.glb');
assert.equal(glb.toString('ascii', 0, 4), 'glTF'); assert.equal(glb.readUInt32LE(4), 2); assert.equal(glb.readUInt32LE(8), glb.length);
const scene = JSON.parse(glb.toString('utf8', 20, 20 + glb.readUInt32LE(12)).trim());
assert.equal(scene.meshes.length, 3); assert.equal(scene.asset.version, '2.0');
const assets = JSON.parse(readFileSync('docs/assets/noah/noah-assets.json'));
for (const asset of assets.assets) {
  assert.ok(/^\/assets\/noah\/[a-z0-9.-]+$/.test(asset.path));
  const bytes = readFileSync(`docs${asset.path}`);
  assert.equal(bytes.length, asset.bytes);
  assert.equal(createHash('sha256').update(bytes).digest('hex'), asset.sha256);
}
const film = assets.assets.find(asset => asset.format === 'MP4');
assert.equal(film.durationSeconds, 20); assert.equal(film.decodedFrameCount, 480);
assert.equal(film.framesPerSecond, 24); assert.equal(film.hdr10, false);
const catalog = JSON.parse(readFileSync('docs/assets/noah-knowledge.json'));
assert.ok(catalog.entries.length >= 64);
assert.ok(catalog.entries.some(entry => entry.u === '/jobs/'));
assert.ok(catalog.entries.some(entry => entry.u === '/noah/'));
const ledger = JSON.parse(readFileSync('docs/ops/noah-capabilities.json'));
assert.ok(ledger.capabilities.length >= 50);
const manifest = JSON.parse(readFileSync('docs/manifest.webmanifest', 'utf8'));
assert.equal(manifest.theme_color, '#0a0f1d', 'PWA shell must match primary brand');
assert.ok(manifest.shortcuts.some(entry => entry.name === 'Noah AI' && entry.url.startsWith('/noah/')), 'PWA must direct users to Noah AI workspace');
assert.ok(!manifest.shortcuts.some(entry => /Lab Muse/i.test(entry.name)), 'Do not present separate Lab Muse product');
const primaryHome = readFileSync('docs/index.html', 'utf8');
// Portfolio nav link removed: href="/portfolio/" pointed to a page that was
// never built (docs/portfolio/ does not exist); dropped as a dead link in
// the nav simplification. The engineering portfolio lives at
// enmanueldmejia.com (separate site).
/* Token-exact membership in the parsed CSP source list — not a
   substring test (a substring can be spoofed by a longer host that
   merely contains the expected origin). */
const cspMatch = primaryHome.match(/http-equiv="Content-Security-Policy" content="([^"]*)"/i);
const cspTokens = cspMatch ? cspMatch[1].split(/\s+/).filter(Boolean) : [];
assert.ok(cspTokens.some(function (t) { return t === 'https://learn.interstitiumlabs.dev'; }), 'University cross-domain link must remain available');
assert.equal(readFileSync('docs/CNAME', 'utf8').trim(), 'interstitiumlabs.dev', 'Canonical apex CNAME changed');
assert.ok(existsSync('docs/ops/DOMAIN-ROUTING.md'), 'Canonical domain mapping must be documented');
console.log(`Source, workspace references, original GLB, curriculum index, and ${ledger.capabilities.length} capability rows verified.`);
