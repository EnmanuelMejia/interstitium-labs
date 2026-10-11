/* Noah reusable skills v1.
 * Safe, browser-local templates for the existing approved workflow tools.
 * This is not server-side/background Muse execution or a general tool builder.
 */
(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory;
  else root.NoahSkills = factory({ storage: (function () { try { return root.localStorage; } catch (_) { return null; } })(), root: root });
})(typeof window !== 'undefined' ? window : globalThis, function createSkills(options) {
  'use strict';
  options = options || {};
  var storage = options.storage || null, KEY = 'noah-skills-v1', MAX = 24, MAX_BYTES = 40000;
  var MODES = Object.freeze({
    research: Object.freeze({ label: 'Curriculum research', tools: ['catalog.search'] }),
    'study-brief': Object.freeze({ label: 'Research + approved study brief', tools: ['catalog.search', 'artifact.study-plan'] })
  });
  var builtins = Object.freeze([
    Object.freeze({ id: 'builtin-research', name: 'Research the curriculum', mode: 'research', builtIn: true }),
    Object.freeze({ id: 'builtin-study-brief', name: 'Create a study brief', mode: 'study-brief', builtIn: true })
  ]);
  function clean(text, limit) { return typeof text === 'string' ? text.replace(/[\u0000-\u001f\u007f]/g, ' ').trim().slice(0, limit) : ''; }
  function valid(x) { return x && typeof x === 'object' && !Array.isArray(x) && /^skill-[a-z0-9-]{1,75}$/.test(x.id) && clean(x.name, 80) && Object.hasOwn(MODES, x.mode); }
  function normalize(rows) {
    if (!Array.isArray(rows) || rows.length > MAX) throw new Error('Invalid Noah skills store.');
    var ids = new Set();
    return rows.map(function (item) {
      if (!valid(item) || ids.has(item.id)) throw new Error('Invalid Noah skill entry.');
      ids.add(item.id);
      return { id: item.id, name: clean(item.name, 80), mode: item.mode, builtIn: false };
    });
  }
  var raw = null, rows = [], available = true;
  function refresh() {
    if (!storage) { available = false; return; }
    try {
      var latest = storage.getItem(KEY);
      if (latest === raw) return;
      if (latest && latest.length > MAX_BYTES) throw new Error('Skills storage exceeds its size limit.');
      var parsed = latest ? JSON.parse(latest) : [];
      rows = normalize(parsed); raw = latest;
      available = true;
    } catch (e) { available = false; throw new Error('Stored skills could not be read. No changes were made.'); }
  }
  function commit(next) {
    if (!storage || !available) throw new Error('Browser storage is unavailable; skills cannot be saved.');
    var before = storage.getItem(KEY);
    if (before !== raw) { refresh(); throw new Error('Skills changed in another tab. Review them before retrying.'); }
    var safe = normalize(next), data = JSON.stringify(safe);
    if (data.length > MAX_BYTES) throw new Error('Skills storage limit reached.');
    storage.setItem(KEY, data);
    raw = data; rows = safe;
    if (options.root && options.root.dispatchEvent && options.root.CustomEvent) {
      options.root.dispatchEvent(new options.root.CustomEvent('noah:skills', { detail: { count: rows.length } }));
    }
  }
  try { refresh(); } catch (_) { /* preserve corrupt data, never overwrite it */ }
  function list() { refresh(); return builtins.map(function (x) { return Object.assign({}, x); }).concat(rows.map(function (x) { return Object.assign({}, x); })); }
  function create(spec) {
    refresh();
    if (!available) throw new Error('Browser storage is unavailable; skills cannot be saved.');
    if (rows.length >= MAX) throw new Error('Remove an old skill before creating another.');
    var name = clean(spec && spec.name, 80), mode = spec && spec.mode;
    if (!name || !Object.hasOwn(MODES, mode)) throw new Error('Choose a name and an approved skill type.');
    if (list().some(function (item) { return item.name.toLowerCase() === name.toLowerCase(); })) throw new Error('A skill with that name already exists.');
    var suffix = options.id ? options.id() : (Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10));
    var id = 'skill-' + clean(String(suffix), 75).toLowerCase().replace(/[^a-z0-9-]/g, '-');
    if (!/^skill-[a-z0-9-]{1,75}$/.test(id) || rows.some(function (item) { return item.id === id; })) throw new Error('Could not allocate a unique skill identifier.');
    var item = { id: id, name: name, mode: mode, builtIn: false };
    commit(rows.concat([item])); return Object.assign({}, item);
  }
  function remove(id) {
    refresh(); if (builtins.some(function (item) { return item.id === id; })) throw new Error('Built-in skills cannot be removed.');
    if (!rows.some(function (item) { return item.id === id; })) throw new Error('Skill not found.');
    commit(rows.filter(function (item) { return item.id !== id; }));
  }
  function launch(id, topic, runner) {
    var skill = list().find(function (item) { return item.id === id; });
    if (!skill) throw new Error('Skill not found.');
    var query = clean(topic, 160);
    if (!query) throw new Error('Enter a topic to run this skill.');
    if (!runner || typeof runner.create !== 'function') throw new Error('Noah workflows are not available.');
    var tools = MODES[skill.mode].tools;
    return runner.create({ title: query, steps: tools.map(function (tool) { return { tool: tool, input: { query: query } }; }) });
  }
  if (options.root && options.root.addEventListener) options.root.addEventListener('storage', function (event) {
    if (event.key !== KEY && event.key !== null) return;
    try { refresh(); } catch (_) { /* Never overwrite malformed storage. */ }
    if (options.root.dispatchEvent && options.root.CustomEvent) options.root.dispatchEvent(new options.root.CustomEvent('noah:skills', { detail: { external: true } }));
  });
  return Object.freeze({ list: list, create: create, remove: remove, launch: launch, modes: MODES, persistent: function () { return Boolean(storage && available); } });
});
