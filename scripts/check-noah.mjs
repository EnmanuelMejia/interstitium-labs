import { readFileSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
const files = ['noah-session.js', 'noah-ai.js', 'noah-workflows.js', 'noah-workspace.js', 'noah-neural.js', 'noah-jobs.js'];
for (const file of files) {
  const run = spawnSync(process.execPath, ['--check', `docs/assets/${file}`], { encoding: 'utf8' });
  assert.equal(run.status, 0, run.stderr);
}
const html = readFileSync('docs/noah/index.html', 'utf8');
for (const file of files.filter(file => file !== 'noah-jobs.js')) assert.ok(html.includes(`/assets/${file}`), `${file} must be loaded`);
const jobsHtml = readFileSync('docs/jobs/index.html', 'utf8');
for (const file of ['noah-session.js', 'noah-ai.js', 'noah-jobs.js']) assert.ok(jobsHtml.includes(`/assets/${file}`));
assert.ok(jobsHtml.includes('https://jobright.ai/jobs/recommend'));
assert.ok(jobsHtml.includes('id="share-consent"'));
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
console.log(`Source, workspace references, original GLB, curriculum index, and ${ledger.capabilities.length} capability rows verified.`);
