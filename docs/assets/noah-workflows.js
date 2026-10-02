/* Noah's bounded device workflow runner. No shell, connector, or account authority.
 * Saved checkpoints resume only after a user action. External tools are unavailable.
 * Browser storage is user-editable; server authorization must never trust this ledger.
 */
(function (root, factory) {
  'use strict';
  if (typeof module === 'object' && module.exports) module.exports = factory;
  else {
    var storage;
    try { storage = root.localStorage; } catch (_) { /* private mode: use memory */ }
    root.NoahWorkflows = factory({ storage: storage, fetch: root.fetch.bind(root), root: root });
  }
})(typeof window !== 'undefined' ? window : globalThis, function createRunner(options) {
  'use strict';
  options = options || {};
  var KEY = 'noah-workflows-v1', MAX_TASKS = 12, MAX_STEPS = 8, MAX_ATTEMPTS = 2;
  var storage = options.storage, active = new Set(), persistent = Boolean(storage), readable = Boolean(storage), revision = 0, observedRaw = null;
  var clock = options.now || Date.now;
  var states = new Set(['ready', 'running', 'paused', 'approval', 'completed', 'cancelled', 'failed']);
  var toolInfo = Object.freeze({
    'catalog.search': Object.freeze({ label: 'Search site curriculum', scope: 'Public site content', permission: 'read', ready: true }),
    'artifact.study-plan': Object.freeze({ label: 'Create a study brief', scope: 'This device', permission: 'write', ready: true }),
    'connector.email': Object.freeze({ label: 'Email', scope: 'External account', permission: 'unconfigured', ready: false }),
    'browser.remote': Object.freeze({ label: 'Cloud computer', scope: 'Isolated server runtime', permission: 'unconfigured', ready: false })
  });
  function clean(value, max) { return typeof value === 'string' ? value.replace(/\u0000/g, '').trim().slice(0, max) : ''; }
  function safePath(value) { return typeof value === 'string' && /^\/[a-zA-Z0-9_\-./]*$/.test(value) && !value.startsWith('//') && !value.includes('..'); }
  function copy(value) { return JSON.parse(JSON.stringify(value)); }
  function event(state, task) {
    if (options.onChange) options.onChange(copy(task));
    if (options.root) {
      options.root.dispatchEvent(new CustomEvent('noah:workflow', { detail: { task: copy(task), persistent: persistent } }));
      options.root.dispatchEvent(new CustomEvent('noah:activity', { detail: { state: state } }));
    }
  }
  function validateStep(step) {
    if (!step || !Object.hasOwn(toolInfo, step.tool) || !toolInfo[step.tool].ready) throw new Error('This tool is unavailable. No external action was taken.');
    var query = clean(step.input && step.input.query, 160);
    if (!query) throw new Error('A topic is required.');
    return { tool: step.tool, input: { query: query }, approvalRequired: step.tool === 'artifact.study-plan', status: 'pending', attempts: 0, output: null, approved: false };
  }
  function validOutput(output, tool) {
    if (!output || typeof output !== 'object') return null;
    if (tool === 'catalog.search') {
      return { matches: (Array.isArray(output.matches) ? output.matches : []).slice(0, 6).filter(function (m) { return m && safePath(m.url); }).map(function (m) {
        return { title: clean(m.title, 160), url: m.url, description: clean(m.description, 600) };
      }) };
    }
    return { filename: 'noah-study-brief.md', markdown: clean(output.markdown, 12000) };
  }
  function restore(raw) {
    try {
      if (!raw || raw.length > 300000) return [];
      var rows = JSON.parse(raw);
      if (!Array.isArray(rows)) return [];
      return rows.slice(-MAX_TASKS).filter(function (t) { return t && /^task-[a-zA-Z0-9-]{1,80}$/.test(t.id) && states.has(t.status) && Array.isArray(t.steps) && t.steps.length > 0 && t.steps.length <= MAX_STEPS; }).flatMap(function (t) {
        try {
          var steps = t.steps.map(function (s) {
            var v = validateStep(s);
            v.attempts = Number.isInteger(s.attempts) ? Math.max(0, Math.min(MAX_ATTEMPTS, s.attempts)) : 0;
            v.output = validOutput(s.output, v.tool);
            v.status = s.status === 'completed' && v.output ? 'completed' : 'pending';
            // Approval cannot survive a reload or imported/user-edited storage.
            v.approved = false;
            return v;
          });
          var status = t.status === 'running' || t.status === 'approval' ? 'paused' : t.status;
          if (status === 'completed' && steps.some(function (s) { return s.status !== 'completed'; })) status = 'paused';
          return [{ id: t.id, title: clean(t.title, 160), status: status, steps: steps, createdAt: Number(t.createdAt) || clock(), updatedAt: Number(t.updatedAt) || clock(), error: clean(t.error, 180), events: (Array.isArray(t.events) ? t.events : []).slice(-24).map(function (e) { return { at: Number(e.at) || 0, text: clean(e.text, 180) }; }) }];
        } catch (_) { return []; }
      });
    } catch (_) { persistent = false; return []; }
  }
  try { observedRaw = storage ? storage.getItem(KEY) : null; } catch (_) { persistent = false; readable = false; }
  var tasks = restore(observedRaw);
  // A storage event is useful for the display, but is not an authority check.
  // Re-read before mutations and after awaited work so a stale tab cannot revive
  // deleted tasks, overwrite newer checkpoints, or save an obsolete tool result.
  function synchronize() {
    if (!storage) return false;
    try {
      var raw = storage.getItem(KEY);
      readable = true;
      if (raw === observedRaw) return false;
      observedRaw = raw; tasks = restore(raw); revision++;
      return true;
    } catch (_) { persistent = false; readable = false; return false; }
  }
  function requireCurrent() {
    if (synchronize()) throw new Error('Workflows changed in another tab. Review the refreshed checkpoint before continuing.');
  }
  function save() {
    requireCurrent();
    try { if (!storage || !readable) throw new Error('No readable storage'); var raw = JSON.stringify(tasks); storage.setItem(KEY, raw); observedRaw = raw; persistent = true; }
    catch (_) { persistent = false; }
    return persistent;
  }
  function log(task, text) {
    task.updatedAt = clock(); task.events.push({ at: clock(), text: clean(text, 180) }); task.events = task.events.slice(-24);
    save(); event(task.status === 'approval' ? 'approval' : task.status === 'running' ? 'executing' : task.status === 'failed' ? 'error' : 'idle', task);
  }
  function find(id) { var task = tasks.find(function (t) { return t.id === id; }); if (!task) throw new Error('Workflow not found.'); return task; }
  function create(spec) {
    synchronize();
    if (!spec || !Array.isArray(spec.steps) || !spec.steps.length || spec.steps.length > MAX_STEPS) throw new Error('Use between one and eight steps.');
    var title = clean(spec.title, 160); if (!title) throw new Error('Name the workflow.');
    if (tasks.length >= MAX_TASKS) throw new Error('Remove an old workflow before adding another.');
    var id = options.id ? options.id() : 'task-' + (globalThis.crypto && crypto.randomUUID ? crypto.randomUUID() : clock() + '-' + Math.random().toString(36).slice(2));
    if (tasks.some(function (t) { return t.id === id; })) throw new Error('Duplicate workflow identifier.');
    var task = { id: id, title: title, status: 'ready', steps: spec.steps.map(validateStep), createdAt: clock(), updatedAt: clock(), events: [], error: '' };
    tasks.push(task); log(task, 'Created. Runs on this page; saved steps can be resumed.'); return copy(task);
  }
  var handlers = {
    'catalog.search': async function (input) {
      var res = await options.fetch('/assets/noah-knowledge.json', { credentials: 'omit', signal: AbortSignal.timeout(10000) });
      if (!res.ok) throw new Error('Site curriculum could not be loaded.');
      var data = await res.json();
      if (!data || !Array.isArray(data.entries)) throw new Error('Invalid curriculum index.');
      var words = input.query.toLowerCase().split(/[^a-z0-9]+/).filter(function (w) { return w.length > 1; }).slice(0, 20);
      var hits = data.entries.slice(0, 500).filter(function (e) { return e && safePath(e.u); }).map(function (e) {
        var hay = (clean(e.t, 160) + ' ' + clean(e.k, 1200) + ' ' + clean(e.d, 600)).toLowerCase();
        return { score: words.reduce(function (s, w) { return s + (hay.includes(w) ? 1 : 0); }, 0), title: clean(e.t, 160), url: e.u, description: clean(e.d, 600) };
      }).filter(function (e) { return e.score > 0; }).sort(function (a, b) { return b.score - a.score; }).slice(0, 6);
      return { matches: hits.map(function (e) { return { title: e.title, url: e.url, description: e.description }; }) };
    },
    'artifact.study-plan': async function (input, context) {
      var result = context.outputs.find(function (o) { return o && Array.isArray(o.matches); });
      var matches = result ? result.matches : [];
      var markdown = '# Noah study brief\n\nTopic: ' + input.query + '\n\nSCIENTIA OMNIA VINCIT\n\n';
      markdown += 'Generated from the public Interstitium Labs index. This is a reading brief; it does not certify mastery or a complete curriculum.\n\n';
      if (matches.length) {
        markdown += '## Relevant study rooms\n\n';
        matches.forEach(function (m) { markdown += '- [' + m.title.replace(/[\[\]\\]/g, '') + '](https://interstitiumlabs.dev' + m.url + ') — ' + m.description + '\n'; });
        markdown += '\n## One sitting\n\n1. Open one relevant study room and identify its learning objective.\n2. State your hypothesis before trying the exercise.\n3. Record the actual result and one correction.\n4. Ask Noah a specific question about the gap in your explanation.\n';
      } else markdown += 'No matching room was found. Refine the topic; no sources or lessons have been invented.\n';
      return { filename: 'noah-study-brief.md', markdown: markdown };
    }
  };
  // Dependency injection is a test seam only; production never accepts tools from task/model input.
  if (options.handlers) Object.keys(handlers).forEach(function (key) { if (options.handlers[key]) handlers[key] = options.handlers[key]; });
  async function execute(id) {
    synchronize();
    var task = find(id);
    if (active.has(id) || ['cancelled', 'completed'].includes(task.status)) return copy(task);
    var runRevision = revision;
    active.add(id); task.status = 'running'; task.error = '';
    try {
      log(task, 'Running from the last saved checkpoint.');
      for (var i = 0; i < task.steps.length; i++) {
        var step = task.steps[i];
        if (task.status === 'cancelled' || task.status === 'paused') break;
        if (step.status === 'completed') continue;
        if (step.approvalRequired && !step.approved) { task.status = 'approval'; log(task, 'Review required: create the study brief on this device.'); break; }
        if (step.attempts >= MAX_ATTEMPTS) throw new Error('Retry budget reached. Create a new workflow after fixing the cause.');
        step.attempts++; log(task, 'Step ' + (i + 1) + ': ' + toolInfo[step.tool].label + '.');
        var output = await handlers[step.tool](copy(step.input), { outputs: task.steps.slice(0, i).map(function (s) { return copy(s.output); }) });
        synchronize();
        if (runRevision !== revision) break;
        if (task.status === 'cancelled' || task.status === 'paused') { log(task, 'Stopped before saving the step result.'); break; }
        step.output = validOutput(output, step.tool);
        if (!step.output) throw new Error('The tool returned an invalid result.');
        step.status = 'completed'; log(task, 'Step ' + (i + 1) + ' saved.');
      }
      if (runRevision === revision && task.status === 'running') { task.status = 'completed'; log(task, 'All steps completed.'); }
    } catch (_) {
      if (runRevision === revision && task.status !== 'cancelled' && task.status !== 'paused') { task.status = 'failed'; task.error = 'The step failed. Check connectivity or the curriculum index; retry within the budget.'; log(task, task.error); }
    } finally { active.delete(id); }
    if (runRevision !== revision) return copy(tasks.find(function (t) { return t.id === id; }) || Object.assign({}, task, { status: 'cancelled', error: 'This workflow was removed in another tab. The pending result was discarded.' }));
    return copy(task);
  }
  async function run(id) {
    if (options.root && options.root.navigator && options.root.navigator.locks) {
      return options.root.navigator.locks.request('noah-workflow-' + id, { ifAvailable: true }, async function (lock) {
        if (!lock) throw new Error('This workflow is running in another tab.');
        return execute(id);
      });
    }
    return execute(id);
  }
  function approve(id) {
    synchronize();
    var task = find(id); if (task.status !== 'approval') throw new Error('No approval is pending.');
    var step = task.steps.find(function (s) { return s.status !== 'completed'; });
    step.approved = true; task.status = 'paused'; log(task, 'Approved once for this local step.'); return run(id);
  }
  function stop(id, state) { synchronize(); var t = find(id); if (t.status === 'completed') return copy(t); t.status = state; log(t, state === 'cancelled' ? 'Cancelled by the user.' : 'Paused by the user.'); return copy(t); }
  function remove(id) { synchronize(); if (active.has(id)) throw new Error('Stop the running workflow first.'); find(id); tasks = tasks.filter(function (t) { return t.id !== id; }); save(); }
  if (options.root && options.root.addEventListener) options.root.addEventListener('storage', function (change) {
    if (change.key !== KEY && change.key !== null) return;
    if (synchronize() && options.root.dispatchEvent) options.root.dispatchEvent(new CustomEvent('noah:workflow', { detail: { external: true, persistent: persistent } }));
  });
  return Object.freeze({ create: create, run: run, approve: approve, pause: function (id) { return stop(id, 'paused'); }, cancel: function (id) { return stop(id, 'cancelled'); }, remove: remove, list: function () { synchronize(); return copy(tasks); }, get: function (id) { synchronize(); return copy(find(id)); }, persistent: function () { return persistent; }, tools: toolInfo });
});
