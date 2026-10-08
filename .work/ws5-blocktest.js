/* Execute the real WORKSTREAM 5 block (extracted from course-shell.js) under
   DOM stubs to catch reference errors and exercise quiz/repair/diagnostic wiring.
   Sloppy mode on purpose: the block's function declarations must leak to module
   scope like they do inside the course-shell IIFE. */
var fs = require('fs');
var shell = fs.readFileSync('/home/hatch/workspace/apex-audit/docs/university/course-shell.js', 'utf8');
var marker = 'WORKSTREAM 5 (2026-10-08): KodeKloud-pattern 10X implementation pass.';
var mpos = shell.indexOf(marker);
if (mpos < 0) { console.error('block not found'); process.exit(1); }
var start = shell.lastIndexOf('/*', mpos);
var end = shell.lastIndexOf('})();');
var block = shell.slice(start, end);
if (block.indexOf('e_ws5_deep') < 0) { console.error('block truncated'); process.exit(1); }

var fails = 0;
function ok(name, cond) { console.log((cond ? 'PASS' : 'FAIL') + ' ' + name); if (!cond) fails++; }

/* ---------- stubs ---------- */
var store = {};
global.localStorage = {
  getItem: function (k) { return Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null; },
  setItem: function (k, v) { store[k] = String(v); },
  removeItem: function (k) { delete store[k]; }
};
function mkClassList(init) {
  var s = {};
  (init || '').split(' ').forEach(function (c) { if (c) s[c] = 1; });
  return {
    contains: function (c) { return !!s[c]; },
    add: function (c) { s[c] = 1; },
    remove: function (c) { delete s[c]; },
    toggle: function (c, f) { if (f === undefined) f = !s[c]; if (f) s[c] = 1; else delete s[c]; },
    _dump: function () { var a = []; for (var k in s) if (s[k]) a.push(k); return a.join(' '); },
    _load: function (v) { s = {}; String(v || '').split(' ').forEach(function (c) { if (c) s[c] = 1; }); }
  };
}
var allEls = [];
function mkEl(tag, cls) {
  var el = {
    tagName: (tag || 'div').toUpperCase(), children: [],
    classList: mkClassList(cls), style: {}, dataset: {},
    _attrs: {}, _listeners: {}, textContent: '', innerHTML: '',
    id: '', parentNode: null,
    setAttribute: function (k, v) { this._attrs[k] = v; },
    getAttribute: function (k) { return this._attrs[k]; },
    addEventListener: function (t, fn) { (this._listeners[t] = this._listeners[t] || []).push(fn); },
    appendChild: function (c) { c.parentNode = this; this.children.push(c); return c; },
    insertBefore: function (n, ref) {
      n.parentNode = this;
      var ix = this.children.indexOf(ref);
      if (ix < 0) this.children.push(n); else this.children.splice(ix, 0, n);
      return n;
    },
    insertAdjacentHTML: function (pos, html) {
      this.innerHTML = (pos === 'afterbegin' ? html : '') + this.innerHTML + (pos === 'afterbegin' ? '' : html);
    },
    querySelector: function (sel) {
      if (sel === '.ilctx') return this.innerHTML.indexOf('ilctx') >= 0 ? {} : null;
      if (sel === '.ilcompare-row') return this.innerHTML.indexOf('ilcompare-row') >= 0 ? {} : null;
      if (sel === 'h3') return { textContent: 'Stub Lab Title' };
      if (sel === '.prompt') return { textContent: 'Stub prompt' };
      if (sel === '.q') return { textContent: 'Stub question text' };
      return null;
    },
    querySelectorAll: function () { return []; },
    scrollIntoView: function () {},
    click: function () { (this._listeners.click || []).forEach(function (fn) { fn({ preventDefault: function () {} }); }); }
  };
  Object.defineProperty(el, 'className', {
    get: function () { return el.classList._dump(); },
    set: function (v) { el.classList._load(v); }
  });
  allEls.push(el);
  return el;
}
var observers = [];
global.MutationObserver = function (cb) {
  var o = { cb: cb, observe: function () {}, disconnect: function () { o.dead = true; } };
  observers.push(o); return o;
};
global.document = {
  createElement: function (t) { return mkEl(t); },
  getElementById: function (id) { for (var i = 0; i < allEls.length; i++) if (allEls[i].id === id) return allEls[i]; return null; },
  querySelectorAll: function () { return []; }
};
global.window = global;
global.__ilOpenModule = function () {};

global.esc = function (s) { return String(s == null ? '' : s); };
global.COURSE = {
  code: 'IL-99', title: 'Test Course', courseId: 'test-course',
  modules: [
    { id: 'm1', code: 'M1', title: 'Mod One', quiz: [
      { q: 'What is 2+2?', choices: ['3', '4', '5'], answer: 1, explain: 'Because 4.' },
      { q: 'Q2?', choices: ['a', 'b'], answer: 1, explain: 'E2' }] },
    { id: 'm2', code: 'M2', title: 'Mod Two', quiz: [
      { q: 'Q3?', choices: ['a', 'b'], answer: 1, explain: 'E3' }] }
  ]
};
/* mirror course-shell Progress key prefixing */
function pkey(k) { return 'ilc:' + COURSE.courseId + ':' + k; }
global.Progress = {
  get: function (k, d) { k = pkey(k); return Object.prototype.hasOwnProperty.call(store, k) ? store[k] : (d === undefined ? null : d); },
  set: function (k, v) { k = pkey(k); if (v == null) delete store[k]; else store[k] = String(v); }
};
global.showTab = function () {};
global.queryParam = function () { return null; };
global.IL = { noahTutor: { noahReady: function () { return true; }, openWithPrefill: function (t) { global.__prefill = t; return true; } } };
global.ILMastery = require('/home/hatch/workspace/apex-audit/docs/university/js/il-mastery.js');
global.ILGuided = require('/home/hatch/workspace/apex-audit/docs/university/js/il-guided.js');
global.ILDiag = require('/home/hatch/workspace/apex-audit/docs/university/js/il-diagnostic.js');

global.buildTermPane = function (root) { var c = mkEl('div', 'scriptlab'); root.appendChild(c); };
global.buildScriptPane = function (root) { var c = mkEl('div', 'scriptlab'); root.appendChild(c); };
global.buildDrillsPane = function (root) { var c = mkEl('div', 'drill'); root.appendChild(c); };
global.buildPolicyPane = function (root) {};
global.buildScenPane = function (root) {};
global.buildTrainerPane = function (root) {};
global.il26_renderHandsOnLab = function (m, host) { var c = mkEl('div', 'scriptlab'); host.appendChild(c); };
global.il26_renderMockTask = function (m, host) { var c = mkEl('div', 'scriptlab'); host.appendChild(c); };
global.il26_renderModuleDrills = function (m, host) { var c = mkEl('div', 'scriptlab'); host.appendChild(c); };
global.buildMock = function (root) {};
global.buildStudy = function (root) {
  var list = mkEl('div'); list.id = 'mod-list'; root.appendChild(list);
  root.querySelector = function (sel) { return sel === '#mod-list' ? list : null; };
};
global.quizHTML = function (mod, qi, q) { return mkEl('div', 'quiz'); };

/* ---------- run the real block ---------- */
try {
  eval(block);
  ok('block evaluates without throwing', true);
} catch (e) {
  console.log('EVAL ERROR:', e && e.stack);
  process.exit(1);
}

/* pane wrappers prepend context bars */
var root = mkEl('div');
buildScriptPane(root);
ok('script pane: YOU ARE HERE bar injected', root.children[0].innerHTML.indexOf('YOU ARE HERE') >= 0);
ok('script pane: env descriptor present', root.children[0].innerHTML.indexOf('no real infrastructure') >= 0);
ok('script pane: course code in bar', root.children[0].innerHTML.indexOf('IL-99') >= 0);
var root2 = mkEl('div');
buildDrillsPane(root2);
ok('drill pane: bar injected into .drill card', root2.children[0].innerHTML.indexOf('YOU ARE HERE') >= 0);
ok('drill pane: practice descriptor', root2.children[0].innerHTML.indexOf('Simulated practice') >= 0);

/* module lab wrappers carry module context */
var host = mkEl('div');
il26_renderHandsOnLab({ id: 'm1', code: 'M1', title: 'Mod One' }, host);
ok('hands-on lab: module context in bar', host.children[0].innerHTML.indexOf('Mod One') >= 0);
var host2 = mkEl('div');
il26_renderMockTask({ id: 'm1', code: 'M1', title: 'Mod One' }, host2);
ok('mock task: assessment descriptor', host2.children[0].innerHTML.indexOf('Simulated assessment') >= 0);

/* quiz wrapper: stable id + compare button on fresh answer */
var mod = { id: 'm1', title: 'Mod One' };
var q = { q: 'What is 2+2?', choices: ['3', '4', '5'], answer: 1, explain: 'Because 4.' };
Progress.set('quiz:m1:0', '0'); /* learner picked '3' (wrong) */
var box = quizHTML(mod, 0, q);
ok('quiz box gets stable id', box.id === 'quiz-m1-0');
box.classList.add('answered');
observers.forEach(function (o) { if (!o.dead) o.cb(); });
var btn = null;
(function find(n) { (n.children || []).forEach(function (c) { if (c.classList && c.classList.contains('ilcompare-btn')) btn = c; find(c); }); })(box);
ok('compare button appended after answer', !!btn);
if (btn) btn.click();
ok('prefill primed with pick vs official + honesty line', !!global.__prefill &&
  global.__prefill.indexOf('The learner picked: 3') >= 0 &&
  global.__prefill.indexOf('The official answer is: 4') >= 0 &&
  global.__prefill.indexOf('never claim to be Muse') >= 0);

/* buildStudy mounts diag + repair; miss clears on correct retry */
var sroot = mkEl('div');
buildStudy(sroot);
var ws5 = null;
sroot.children.forEach(function (c) { if (c.id === 'il-ws5') ws5 = c; });
ok('buildStudy mounts il-ws5 wrapper', !!ws5);
var dslot = null, rslot = null;
if (ws5) ws5.children.forEach(function (c) { if (c.id === 'il-diag') dslot = c; if (c.id === 'il-repair') rslot = c; });
ok('diagnostic card mounts (eligible questions exist)', !!dslot && dslot.innerHTML.indexOf('Test out') >= 0);
ok('repair section lists the miss', !!rslot && rslot.innerHTML.indexOf('Repair queue') >= 0 && rslot.innerHTML.indexOf('What is 2+2?') >= 0);
Progress.set('quiz:m1:0', '1'); /* correct on retry */
ws5_refreshRepair();
ok('miss clears after correct retry', rslot.innerHTML.indexOf('No open misses') >= 0);
ok('session repaired counter shown', rslot.innerHTML.indexOf('1 repaired') >= 0);

console.log(fails ? ('\n' + fails + ' FAILURES') : '\nALL PASS');
process.exit(fails ? 1 : 0);
