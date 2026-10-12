/* Node smoke test for WORKSTREAM 5 libraries (il-guided ext, il-mastery, il-diagnostic). */
'use strict';
var store = {};
global.localStorage = {
  getItem: function (k) { return Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null; },
  setItem: function (k, v) { store[k] = String(v); },
  removeItem: function (k) { delete store[k]; }
};
global.window = global;

var guided = require('/home/hatch/workspace/apex-audit/docs/university/js/il-guided.js');
var mastery = require('/home/hatch/workspace/apex-audit/docs/university/js/il-mastery.js');
var diag = require('/home/hatch/workspace/apex-audit/docs/university/js/il-diagnostic.js');

var fails = 0;
function ok(name, cond) {
  console.log((cond ? 'PASS' : 'FAIL') + ' ' + name);
  if (!cond) fails++;
}

var CID = 'il-01-esoteric-foundations';
var modules = [
  { id: 'm1', code: 'M1', title: 'Mod One', quiz: [
    { q: 'Q1?', choices: ['a', 'b'], answer: 0, explain: 'E1' },
    { q: 'Q2?', choices: ['a', 'b'], answer: 1, explain: 'E2' }] },
  { id: 'm2', code: 'M2', title: 'Mod Two', quiz: [
    { q: 'Q3?', choices: ['a', 'b'], answer: 1, explain: 'E3' }] },
  { id: 'm3', code: 'M3', title: 'Mod Three' } /* no quiz */
];
var infos = modules.map(function (m) { return { id: m.id, title: m.title, code: m.code, quizTotal: (m.quiz || []).length }; });

/* --- markTestOut --- */
var rec = guided.markTestOut(CID, 'm1', 80);
ok('markTestOut returns record with testOut+mastery', rec && rec.testOut === true && rec.mastery === true);
ok('getRecord shows testOut', guided.getRecord(CID, 'm1').testOut === true);

/* --- computeStates: testOut module counts as passed, unlocks next --- */
var states = guided.computeStates(CID, infos);
ok('m1 state is done (testOut, no ILProgress)', states[0].state === 'done' && states[0].testOut === true);
ok('m2 is current (unlocked by tested-out m1)', states[1].state === 'current');
ok('m3 is next teaser', states[2].state === 'next');
ok('stateFor m1 badge via rail HTML says Tested out',
  guided.pathRailHTML(CID, infos).indexOf('Tested out') !== -1);

/* stickiness: a later wrong answer cannot revoke */
guided.recomputeMastery(CID, 'm1', modules[0].quiz, function () { return '1'; });
ok('testOut sticky after low recompute', guided.getRecord(CID, 'm1').mastery === true && guided.getRecord(CID, 'm1').testOut === true);

/* --- il-mastery heat --- */
/* answer m2's only question wrong -> red; m1 green via testOut; m3 gray */
store['ilc:' + CID + ':quiz:m2:0'] = '0'; /* correct is 1 */
var heat = mastery.heatFor(CID, modules);
ok('heat m1 green (testOut)', heat[0].cell === 'green' && heat[0].label === 'Tested out');
ok('heat m2 red (0% attempted)', heat[1].cell === 'red');
ok('heat m3 gray (no quiz, untouched)', heat[2].cell === 'gray');
var counts = mastery.heatCounts(heat);
ok('heatCounts', counts.green === 1 && counts.red === 1 && counts.gray === 1);

/* repair items: only the wrong m2 answer */
var items = mastery.repairItems(CID, modules);
ok('repairItems finds 1 miss', items.length === 1 && items[0].moduleId === 'm2' && items[0].chosen === '0');
var rh = mastery.repairHTML(items, { linkFor: function (it) { return '#q-' + it.qi; } });
ok('repairHTML contains Revisit link + picked text', rh.indexOf('Revisit question') !== -1 && rh.indexOf('You picked') !== -1);
ok('repairHTML empty state', mastery.repairHTML([], {}).indexOf('No open misses') !== -1);

/* --- readiness --- */
var idx = { certs: { 'CompTIA Test+': { issuer: 'CompTIA', courses: [
  { slug: 'a', courseId: CID, code: 'IL-01', moduleCount: 3, quizModules: 2 },
  { slug: 'b', courseId: 'other-course', code: 'IL-02', moduleCount: 4, quizModules: 4 }
] } } };
var r = mastery.readinessFor('CompTIA Test+', idx);
/* IL-01: 1 of 3 mastered -> 33%; other: 0. weighted by quizModules (2,4): (33*2+0*4)/6 = 11 */
ok('readinessFor weighted pct', r && r.pct === 11 && r.courses.length === 2);
ok('readinessBand early', mastery.readinessBand(11, true).indexOf('Early') === 0);
ok('isUnmappedCert', mastery.isUnmappedCert('No certification mapped', 'N/A') === true &&
  mastery.isUnmappedCert('CompTIA Security+', 'CompTIA') === false);

/* --- diagnostic itemsFor --- */
/* m1 mastered/testOut -> skipped; m2 has quiz but answered (wrong) -> no unanswered -> skipped; m3 no quiz */
var ditems = diag.itemsFor(CID, modules);
ok('itemsFor skips mastered + fully-answered + no-quiz modules', ditems.length === 0);
/* fresh course: first unanswered per module */
var d2 = diag.itemsFor('fresh-course', modules);
ok('itemsFor fresh course samples 2 quiz modules', d2.length === 2 && d2[0].moduleId === 'm1' && d2[1].moduleId === 'm2');
ok('itemsFor picks first unanswered question', d2[0].qi === 0 && d2[0].q.q === 'Q1?');

console.log(fails ? ('\n' + fails + ' FAILURES') : '\nALL PASS');
process.exit(fails ? 1 : 0);
