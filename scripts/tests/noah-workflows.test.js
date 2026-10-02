'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const createRunner = require('../../docs/assets/noah-workflows.js');
function memory() { const data = new Map(); return { getItem: k => data.get(k) || null, setItem: (k, v) => data.set(k, v) }; }
const spec = { title: 'Study SQL', steps: [{ tool: 'catalog.search', input: { query: 'SQL' } }, { tool: 'artifact.study-plan', input: { query: 'SQL' } }] };
const response = { ok: true, json: async () => ({ entries: [{ u: '/learn/sql/', t: 'SQL room', d: 'Real SQL exercises', k: 'sql queries' }, { u: '//evil.invalid/', t: 'SQL', k: 'sql' }] }) };
test('catalog search checkpoints; writing requires explicit approval and produces actual artifact', async () => {
  const runner = createRunner({ storage: memory(), fetch: async () => response });
  const task = runner.create(spec);
  const pending = await runner.run(task.id);
  assert.equal(pending.status, 'approval');
  assert.equal(pending.steps[0].output.matches.length, 1);
  assert.equal(pending.steps[1].output, null);
  const done = await runner.approve(task.id);
  assert.equal(done.status, 'completed');
  assert.match(done.steps[1].output.markdown, /https:\/\/interstitiumlabs.dev\/learn\/sql\//);
  assert.equal(done.steps[0].attempts, 1);
});
test('reload resumes checkpoint without rerunning completed reads or restoring approvals', async () => {
  const storage = memory(); let reads = 0;
  const runner = createRunner({ storage, fetch: async () => { reads++; return response; } });
  const task = runner.create(spec); await runner.run(task.id);
  const resumed = createRunner({ storage, fetch: async () => { reads++; return response; } });
  assert.equal(resumed.get(task.id).status, 'paused');
  assert.equal((await resumed.run(task.id)).status, 'approval');
  await resumed.approve(task.id); assert.equal(reads, 1);
});
test('external, prototype, and arbitrary tools are rejected without network execution', () => {
  const runner = createRunner({ storage: memory(), fetch: () => { throw Error('must not run'); } });
  for (const tool of ['connector.email', 'browser.remote', '__proto__', 'shell.exec']) assert.throws(() => runner.create({ title: 'bad', steps: [{ tool, input: { query: 'send secret' } }] }), /unavailable/);
});
test('cancellation prevents later writes; double run is idempotent within one runner', async () => {
  let release; let count = 0;
  const runner = createRunner({ storage: memory(), handlers: { 'catalog.search': () => { count++; return new Promise(r => { release = r; }); } } });
  const task = runner.create(spec); const running = runner.run(task.id);
  await runner.run(task.id); runner.cancel(task.id); release({ matches: [] }); await running;
  assert.equal(count, 1); assert.equal(runner.get(task.id).status, 'cancelled'); assert.equal(runner.get(task.id).steps[1].output, null);
});
test('failed tools have a bounded retry budget and do not persist private error text', async () => {
  let calls = 0; const runner = createRunner({ storage: memory(), handlers: { 'catalog.search': async () => { calls++; throw Error('secret-token'); } } });
  const task = runner.create(spec);
  await runner.run(task.id); await runner.run(task.id); await runner.run(task.id);
  assert.equal(calls, 2); assert.doesNotMatch(JSON.stringify(runner.get(task.id)), /secret-token/);
});
test('quota/storage errors are explicit and malformed persistent state is discarded', () => {
  const runner = createRunner({ storage: { getItem: () => '{broken', setItem: () => { throw Error('quota'); } } });
  assert.deepEqual(runner.list(), []); runner.create(spec); assert.equal(runner.persistent(), false);
});

test('stale tabs cannot restore a deleted workflow and preserve newer tasks on mutation', async () => {
  const storage = memory(), first = createRunner({ storage, fetch: async () => response });
  const old = first.create(spec);
  const stale = createRunner({ storage, fetch: async () => response });
  first.remove(old.id);
  const newer = first.create({ ...spec, title: 'Newer task' });
  await assert.rejects(stale.run(old.id), /not found/);
  const added = stale.create({ ...spec, title: 'Created from stale tab' });
  assert.deepEqual(first.list().map(t => t.id), [newer.id, added.id]);
  assert.equal(JSON.parse(storage.getItem('noah-workflows-v1')).some(t => t.id === old.id), false);
});

test('pending results are discarded if another tab removes the running task', async () => {
  const storage = memory(); let release;
  const runner = createRunner({ storage, handlers: { 'catalog.search': () => new Promise(resolve => { release = resolve; }) } });
  const task = runner.create(spec), pending = runner.run(task.id);
  const other = createRunner({ storage });
  other.remove(task.id);
  release({ matches: [{ title: 'Old result', url: '/learn/sql/', description: 'Should not survive removal' }] });
  const stopped = await pending;
  assert.equal(stopped.status, 'cancelled');
  assert.deepEqual(runner.list(), []);
  assert.deepEqual(JSON.parse(storage.getItem('noah-workflows-v1')), []);
});

test('pending results cannot overwrite a newer checkpoint or restore an old approval', async () => {
  const storage = memory(); let release;
  const runner = createRunner({ storage, handlers: { 'catalog.search': () => new Promise(resolve => { release = resolve; }) } });
  const task = runner.create(spec), pending = runner.run(task.id);
  const other = createRunner({ storage });
  other.cancel(task.id);
  const newer = other.create({ ...spec, title: 'Keep this newer task' });
  release({ matches: [] }); await pending;
  assert.equal(runner.get(task.id).status, 'cancelled');
  assert.equal(runner.get(task.id).steps[0].output, null);
  assert.deepEqual(runner.list().map(t => t.id), [task.id, newer.id]);
  assert.throws(() => runner.approve(task.id), /No approval/);
});

test('unreadable workflow storage cannot be overwritten as though it were a fresh empty ledger', () => {
  let writes = 0;
  const runner = createRunner({ storage: { getItem() { throw Error('blocked'); }, setItem() { writes++; } } });
  runner.create(spec);
  assert.equal(writes, 0);
  assert.equal(runner.persistent(), false);
  assert.equal(runner.list().length, 1);
});
