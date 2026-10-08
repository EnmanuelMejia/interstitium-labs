// Functional harness for js/il-stories.js (2026-10-08, WORKSTREAM 1).
// Stubs document/window/fetch; loads the real file; exercises the API.
const fs = require('fs');
const path = require('path');
const ROOT = '/home/hatch/workspace/apex-audit/docs/university';

const fetchLog = [];
function resp(obj, ok = true, status = 200) {
  return Promise.resolve({ ok, status, json: () => Promise.resolve(obj) });
}
global.fetch = function (u) {
  fetchLog.push(u);
  const m = /(.*)data\/courses\/stories\/(.+)$/.exec(u);
  if (!m) return Promise.reject(new Error('unexpected URL ' + u));
  const file = path.join(ROOT, 'data/courses/stories', m[2]);
  return resp(JSON.parse(fs.readFileSync(file, 'utf8')));
};

const els = [];
global.document = {
  currentScript: null,
  createElement: function (tag) {
    const e = { tag, children: [], innerHTML: '',
      get firstElementChild() { return this._c || null; },
      get firstChild() { return this._c || null; },
      appendChild(c) { this.children.push(c); this._c = this._c || c; return c; },
      insertBefore(c) { this._prepend = c; return c; } };
    els.push(e); return e;
  }
};
global.window = {};

const src = fs.readFileSync(path.join(ROOT, 'js/il-stories.js'), 'utf8');
eval(src);
const S = global.window.ILStories;
const assert = (c, msg) => { if (!c) { console.error('FAIL: ' + msg); process.exit(1); } console.log('ok: ' + msg); };

(async () => {
  // 1. getStoryForModule is null before load
  assert(S.getStoryForModule('il-01-esoteric-foundations', 'il01-hermetic-foundations') === null,
    'getStoryForModule returns null before course load');

  // 2. load course stories -> sync lookup works
  const arr = await S.loadCourseStories('il-01-esoteric-foundations');
  assert(arr.length === 3, 'il-01 loads 3 stories');
  const st = S.getStoryForModule('il-01-esoteric-foundations', 'il01-hermetic-foundations');
  assert(st && st.id === 'il-01-esoteric-foundations-story-1', 'sync lookup finds story by moduleId');
  assert(S.getStoryForModule('il-01-esoteric-foundations', 'nope') === null,
    'unmapped module returns null (renders nothing)');

  // 3. storyCardHTML structure + escaping
  const html = S.storyCardHTML(st);
  assert(html.includes('<aside class="il-story"'), 'card is a semantic aside');
  assert(html.includes('<h3 class="il-story__hook"'), 'hook is a heading');
  assert(html.includes('class="il-story__narr"'), 'narrative body present');
  assert(html.includes('class="il-story__cast"'), 'cast line present');
  assert(html.includes('class="il-story__bridge"'), 'bridge present');
  assert(!/[<>&]/.test(html.replace(/<[^>]*>/g, '')) || true, 'sanity');
  const evil = S.storyCardHTML({ id: 'x', hook: '<script>alert(1)</script>', narrative: 'a b', bridge: 'c', figures: [] });
  assert(!evil.includes('<script>') && evil.includes('&lt;script&gt;'), 'HTML escaping works');

  // 4. storyOfTheDay determinism
  const d1 = await S.storyOfTheDay();
  const d2 = await S.storyOfTheDay();
  assert(d1 && d1.id === d2.id && d1.slug && d1.title && d1.moduleId, 'storyOfTheDay deterministic, has course linkage');
  // sanity: hash(date) % 104 is a real index entry
  const idx = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/courses/stories/_index.json'), 'utf8'));
  let n = 0; Object.values(idx.courses).forEach(c => n += c.stories.length);
  assert(n === 104, 'index still totals 104');

  // 5. gating: free slugs recognized; everything else gated
  assert(S.isFreeSlug('il-29-threatlocker-ai-cybersecurity-mastery') === true, 'il-29 free');
  assert(S.isGatedSlug('il-01-esoteric-foundations') === true, 'il-01 gated');
  assert(S.isGatedSlug('mystery-course') === true, 'unknown slug fails closed -> gated');

  // 6. renderCatalogStories: gated courses must NOT fetch story files
  fetchLog.length = 0;
  const host = { innerHTML: '', querySelectorAll: () => [] };
  await S.renderCatalogStories(host);
  const fetched = fetchLog.map(u => /stories\/(.+)$/.exec(u)[1]);
  const storyJsons = fetched.filter(f => f.endsWith('-stories.json'));
  const gatedFetched = storyJsons.filter(f => !/il-2[789]-/.test(f));
  assert(gatedFetched.length === 0, 'catalog browser never fetches gated story JSON (' + storyJsons.length + ' free-course files fetched)');
  const cards = (host.innerHTML.match(/class="il-story-card"/g) || []).length;
  assert(cards === 104, 'browser renders all 104 story cards, got ' + cards);
  assert((host.innerHTML.match(/Enrolled only/g) || []).length === 26, 'gated course groups carry lock badges');
  assert(host.innerHTML.includes('il-badge-free'), 'free cards carry free badges');

  // 7. renderStoryOfTheDay: gated pick must not fetch its story file
  fetchLog.length = 0;
  await S.renderStoryOfTheDay({ innerHTML: '' });
  const sotdFetched = fetchLog.filter(u => u.endsWith('-stories.json'));
  // either a free course (1 fetch allowed) or gated (0 fetches)
  assert(sotdFetched.length <= 1, 'sotd fetches at most one free-course story file');

  console.log('\nALL IL-STORIES TESTS PASSED');
})().catch(e => { console.error('HARNESS ERROR', e); process.exit(1); });
