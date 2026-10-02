'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const createSkills = require('../../docs/assets/noah-skills.js');
const createRunner = require('../../docs/assets/noah-workflows.js');
function memory() {
  const values = new Map();
  return { getItem: key => values.get(key) ?? null, setItem: (key, value) => values.set(key, value) };
}
test('built-in research skill launches an actual approved read workflow', async () => {
  const runner = createRunner({ storage: memory(), fetch: async () => ({ok:true,json:async()=>({entries:[{u:'/learn/',t:'Learn SQL',k:'SQL',d:'Site lesson'}]})}) });
  const skills = createSkills({storage:memory()});
  const task = skills.launch('builtin-research','SQL',runner);
  assert.deepEqual(task.steps.map(s => s.tool),['catalog.search']);
  const done = await runner.run(task.id);
  assert.equal(done.status,'completed');
  assert.equal(done.steps[0].output.matches[0].url,'/learn/');
});
test('user-created study brief skill requires approval before writing local artifact', async () => {
  const storage = memory(), skills = createSkills({storage,id:()=> 'test-id'});
  const saved = skills.create({name:'My SQL lesson brief',mode:'study-brief'});
  const restored = createSkills({storage});
  assert.equal(restored.list().find(s=>s.id===saved.id).name,'My SQL lesson brief');
  const runner = createRunner({storage:memory(),fetch:async()=>({ok:true,json:async()=>({entries:[]})})});
  const task = restored.launch(saved.id,'SQL',runner);
  assert.deepEqual(task.steps.map(s=>s.tool),['catalog.search','artifact.study-plan']);
  const waiting=await runner.run(task.id);
  assert.equal(waiting.status,'approval');
  assert.equal(waiting.steps[1].output,null);
  const done=await runner.approve(task.id);
  assert.equal(done.status,'completed');
  assert.match(done.steps[1].output.markdown,/Topic: SQL/);
});
test('skill registry cannot enable arbitrary or external tools', () => {
  const skills=createSkills({storage:memory()});
  assert.throws(()=>skills.create({name:'Email',mode:'connector.email'}),/approved skill type/);
  assert.throws(()=>skills.launch('builtin-research','', {create(){throw Error('should not run');}}),/topic/);
  assert.equal(Object.hasOwn(skills.modes,'browser.remote'),false);
  assert.equal(Object.hasOwn(skills.modes,'connector.email'),false);
});
test('custom skill removal persists; built-in skills cannot be removed', () => {
  const storage=memory(),skills=createSkills({storage,id:()=> 'a'});
  const item=skills.create({name:'My custom research',mode:'research'});
  assert.throws(()=>skills.remove('builtin-research'),/Built-in/);
  skills.remove(item.id);
  assert.equal(createSkills({storage}).list().some(x=>x.id===item.id),false);
});
test('malformed saved skills are not silently overwritten', () => {
  const storage=memory();storage.setItem('noah-skills-v1','{broken');
  const skills=createSkills({storage});
  assert.throws(()=>skills.create({name:'x',mode:'research'}),/could not be read/);
  assert.equal(storage.getItem('noah-skills-v1'),'{broken');
});
test('stale skill view does not resurrect removed entries', () => {
  const storage=memory(),first=createSkills({storage,id:()=> 'a'});
  const item=first.create({name:'First',mode:'research'});
  const stale=createSkills({storage,id:()=> 'b'});
  first.remove(item.id);
  stale.create({name:'New',mode:'study-brief'});
  assert.equal(first.list().some(s=>s.id===item.id),false);
  assert.equal(first.list().some(s=>s.name==='New'),true);
});
