'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const jobs = require('../../docs/assets/noah-jobs.js');
const session = require('../../docs/assets/noah-session.js');

function posting(overrides = {}) {
  return jobs.normalizeJob({ title: 'Junior Cloud Engineer', company: 'Test fixture company', url: 'https://careers.fixture-company.org/jobs/1',
    requirements: 'AWS, Linux, PowerShell, Docker and CompTIA A+ preferred. Minimum 2 years of experience.', location: 'United States', type: 'full_time', ...overrides });
}
function storage(seed = {}) {
  const data = { ...seed };
  return { data, getItem: key => data[key] || null, setItem: (key, value) => { data[key] = value; }, removeItem: key => { delete data[key]; } };
}

test('public posting links reject executable schemes, credentials and private-address forms without fetching', () => {
  for (const url of ['javascript:alert(1)', 'data:text/html,hi', 'http://careers.fixture-company.org/job', 'https://name:password@careers.fixture-company.org/job',
    'https://localhost/jobs', 'https://192.168.1.2/jobs', 'https://[::1]/jobs', 'https://127.1/jobs', 'https://internal.local/jobs', 'https://careers.fixture-company.org:444/jobs',
    '//careers.fixture-company.org/jobs', 'https://careers.fixture-company.org/\\evil']) assert.equal(jobs.safeURL(url), '', url);
  assert.equal(jobs.safeURL('https://careers.fixture-company.org/job?id=123&utm_source=test&gclid=private#section'), 'https://careers.fixture-company.org/job?id=123');
});

test('normalization removes HTML and familiar credential patterns, rejects incomplete and misattributed feeds', () => {
  const p = posting({ title: '<strong>Junior Cloud Engineer</strong>', requirements: '<script>doBad()</script><p>AWS &amp; Linux</p><p>sk-abcdefghijklmnopqrstuvwx</p>' });
  assert.equal(p.title, 'Junior Cloud Engineer');
  assert.equal(p.requirements.includes('doBad'), false);
  assert.equal(p.requirements.includes('sk-'), false);
  assert.ok(p.requirements.includes('AWS & Linux'));
  assert.equal(jobs.normalizeJob({ title: 'Incomplete' }), null);
  assert.equal(jobs.normalizeJob({ ...p, source: 'remotive' }), null);
  assert.equal(jobs.normalizeJob({ ...p, url: 'https://remotive.com/remote-jobs/1' }, 'remotive').source, 'remotive');
  for (const [raw, expected] of [
    ['<script>one<script>two</script>three</script><p>Linux</p>', 'Linux'],
    ['<style>.a{<style>.b{}</style>}</style><p>Windows</p>', 'Windows'],
    ['<!--private<!--nested-->still private--><p>AWS</p>', 'AWS'],
    ['<p title="a > b">PowerShell</p>', 'PowerShell'],
    ['<script>unfinished', ''], ['<!--unfinished', '']
  ]) assert.equal(jobs.plainText(raw), expected);
  // Decoded markup is deliberately literal text. The UI's textContent sink is the safety boundary.
  assert.equal(jobs.plainText('&lt;img src=x onerror=&quot;malicious()&quot;&gt;'), '<img src=x onerror="malicious()">');
});

test('duplicate canonical links update one posting and keep saved identity across tracking parameters', () => {
  const a = posting(), b = posting({ title: 'Updated title', url: a.url + '?utm_campaign=ignore#section' });
  assert.equal(a.id, b.id);
  const merged = jobs.mergeJobs([a], [b]);
  assert.equal(merged.length, 1);
  assert.equal(merged[0].title, 'Updated title');
  assert.equal(jobs.mergeJobs([], Array.from({ length: 250 }, (_, i) => posting({ url: 'https://careers.fixture-company.org/jobs/' + i }))).length, jobs.LIMITS.jobs);
});

test('local filters combine explicit seniority, role family, source, location and manual tracking', () => {
  assert.equal(jobs.filters().lane, 'all');
  assert.equal(jobs.normalizeState({ filters: { lane: 'cloud' } }).filters.lane, 'cloud');
  const cloud = posting(), senior = posting({ title: 'Senior DevOps Engineer', url: 'https://careers.fixture-company.org/jobs/2' });
  const support = posting({ title: 'IT Support Specialist', url: 'https://careers.fixture-company.org/jobs/3', location: 'Worldwide' });
  const all = [cloud, senior, support], stages = { [cloud.id]: 'applied', [support.id]: 'interview' };
  assert.deepEqual(jobs.filterJobs(all, { lane: 'cloud', level: 'junior', location: 'United States', type: 'full_time' }, []), [cloud]);
  assert.deepEqual(jobs.filterJobs(all, { lane: 'all', saved: true, stage: 'applied' }, [cloud.id, senior.id], stages), [cloud]);
  assert.deepEqual(jobs.filterJobs(all, { lane: 'support', stage: 'interview' }, [], stages), [support]);
  assert.equal(jobs.seniority('Cloud Engineer'), 'unspecified');
  assert.equal(jobs.seniority('Tier III Service Desk Engineer'), 'unspecified');
  assert.deepEqual(jobs.filterJobs(all, { lane: 'cloud', level: 'not-senior' }, []), [cloud]);
});

test('matching separates stated demonstration, learning and unresolved eligibility without an invented percentage', () => {
  const m = jobs.match(posting(), { skills: 'PowerShell, learning AWS, no Docker experience', aplus: true, portfolio: true });
  assert.deepEqual(m.evidenced, ['PowerShell', 'CompTIA A+']);
  assert.ok(m.gaps.includes('AWS') && m.gaps.includes('Linux') && m.gaps.includes('Docker'));
  assert.ok(m.learning.includes('AWS'));
  assert.ok(m.unknowns.some(v => v.includes('2 years')));
  assert.ok(m.unknowns.some(v => v.includes('does not establish paid')));
  assert.ok(m.unknowns.some(v => v.includes('work authorization')));
  assert.equal(m.summary.includes('%'), false);
  assert.deepEqual(jobs.match(posting(), {}).evidenced, []);
  assert.equal(jobs.profile({ support: 'yes', aplus: 1, portfolio: true }).support, false);
});

test('storage validates records and tracking stages, survives unavailable storage and forgets only its own key', () => {
  const p = posting(), db = storage({ unrelated: 'preserved', [jobs.KEY]: JSON.stringify({ jobs: [p], saved: [p.id, 'forged'], stages: { [p.id]: 'applied', forged: 'interview' }, profile: { support: 'true' } }) });
  const store = jobs.createStore(db);
  assert.deepEqual(store.snapshot().saved, [p.id]);
  assert.deepEqual(store.snapshot().stages, { [p.id]: 'applied' });
  assert.equal(store.snapshot().profile.support, false);
  store.clear(); assert.equal(db.data.unrelated, 'preserved'); assert.equal(db.data[jobs.KEY], undefined);
  for (const raw of ['{invalid', 'null', JSON.stringify({ jobs: [{ title: 'no public URL' }] }), 'x'.repeat(jobs.LIMITS.storage + 1)]) {
    assert.deepEqual(jobs.createStore(storage({ [jobs.KEY]: raw })).snapshot().jobs, []);
  }
  const transient = jobs.createStore({ getItem() { throw new Error('blocked'); }, setItem() { throw new Error('quota'); }, removeItem() { throw new Error('blocked'); } });
  transient.commit({ jobs: [p], stages: { [p.id]: 'interview' } });
  assert.equal(transient.snapshot().jobs.length, 1); assert.match(transient.notice(), /may not persist/);
});

test('a bounded consent preview includes only supplied facts and selected postings with clear truncation', () => {
  const a = posting({ requirements: 'AWS Linux '.repeat(700) }), b = posting({ url: 'https://careers.fixture-company.org/jobs/2', title: 'Junior DevOps Engineer' });
  const prompt = jobs.buildPrompt([a, b], { portfolio: true, skills: 'PowerShell', notes: 'A learning lab', aplus: false }, 'compare');
  assert.ok(prompt.length <= 3900);
  const payload = JSON.parse(prompt.slice(prompt.indexOf('{')));
  assert.equal(payload.candidate.paidYears, 'unknown');
  assert.equal(payload.candidate.CompTIAAPlusStated, false);
  assert.equal(payload.postings.length, 2);
  assert.equal(payload.postings[0].requirementsTruncated, true);
  assert.match(prompt, /untrusted reference data/);
  assert.throws(() => jobs.buildPrompt([a], {}, 'compare'), /two jobs/);
  assert.throws(() => jobs.buildPrompt([], {}, 'fit'), /Select/);
});

test('forget reports unverified saved deletion instead of implying persisted evidence disappeared', () => {
  const p = posting(), original = JSON.stringify({ jobs: [p], profile: { notes: 'Private job evidence' } });
  for (const removal of [() => { throw Error('blocked'); }, () => {}]) {
    const store = jobs.createStore({ getItem: () => original, setItem() {}, removeItem: removal });
    store.clear();
    assert.deepEqual(store.snapshot().jobs, []);
    assert.match(store.notice(), /Saved deletion could not be verified/);
    assert.match(store.notice(), /return after reloading/);
  }
  const db = storage({ [jobs.KEY]: original });
  const store = jobs.createStore(db); store.clear();
  assert.equal(store.notice(), '');
  assert.deepEqual(jobs.createStore(db).snapshot().jobs, []);
});

test('Noah sharing requires fresh consent, excludes stored history/page data and preserves real engine provenance', async () => {
  let calls = 0, optionsReceived;
  const device = { reply: 'Local fallback', remote: false, fallback: true, notice: 'Remote service unavailable.' };
  const api = { converse: async (prompt, options) => { calls++; optionsReceived = options; assert.equal(prompt, 'Reviewed text'); return device; } };
  await assert.rejects(jobs.share(api, 'Reviewed text', false), /Consent/);
  assert.equal(calls, 0);
  assert.equal(await jobs.share(api, 'Reviewed text', true), device);
  assert.equal(calls, 1);
  assert.deepEqual(optionsReceived, { forceRemote: true, shareMemoryWithRemote: false, sharePageContext: false });
  await assert.rejects(jobs.share({}, 'Reviewed text', true), /unavailable/);
});

test('consent preview uses the real privacy filter and equals the subsequently transmitted message', () => {
  const store = session.createStore({ storage: storage() });
  store.record('user', 'Unrelated private conversation');
  store.addMemory({ kind: 'note', text: 'Unrelated saved preference' });
  store.setPreferences({ shareMemoryWithRemote: true, sharePageContext: true });
  const prompt = jobs.buildPrompt([posting({ url: 'https://careers.fixture-company.org/jobs/1?gh_jid=123' })], { notes: 'api_key=qa-fixture-secret' }, 'fit');
  const reviewed = jobs.reviewPrompt({ session: store }, prompt);
  const transmitted = store.prepareRemoteMessages(reviewed, store.snapshot().conversation, { shareMemoryWithRemote: false, sharePageContext: false });
  assert.equal(transmitted.length, 1);
  assert.equal(reviewed, transmitted[0].content);
  assert.equal(jobs.reviewPrompt({ session: store }, reviewed), reviewed);
  assert.doesNotMatch(reviewed, /gh_jid|qa-fixture-secret|Unrelated/);
  assert.match(reviewed, /redacted/);
  assert.ok(reviewed.length <= 3900);
  assert.throws(() => jobs.reviewPrompt({}, prompt), /privacy filter is unavailable/);
  assert.throws(() => jobs.reviewPrompt({ session: { prepareRemoteMessages: () => [{ role: 'user', content: 'a'.repeat(3901) }] } }, prompt), /exceeds/);
});

test('local preparation states boundaries and names evidence to build rather than claiming an application occurred', () => {
  const text = jobs.preparation([posting()], { skills: 'PowerShell', portfolio: true });
  assert.match(text, /Gather a specific example/);
  assert.match(text, /paid production experience/);
  assert.match(text, /application yourself at the source/);
  assert.equal(text.includes('You have applied'), false);
});

test('published public snapshot is attributed, bounded, sanitized and requires no private candidate data', () => {
  const raw = JSON.parse(fs.readFileSync(path.join(__dirname, '../../docs/assets/noah-jobs-feed.json'), 'utf8'));
  const feed = jobs.validateFeed(raw);
  assert.ok(feed.jobs.length > 0 && feed.jobs.length <= jobs.LIMITS.feed);
  assert.equal(raw.providerDelayHours, 24);
  assert.equal(raw.documentationURL, 'https://github.com/remotive-com/remote-jobs-api');
  assert.ok(feed.jobs.every(p => p.source === 'remotive' && new URL(p.url).hostname === 'remotive.com'));
  assert.equal(Object.hasOwn(raw, 'candidate'), false);
  assert.throws(() => jobs.validateFeed({ provider: 'Forged', fetchedAt: 'invalid', jobs: [] }), /invalid/);
});
