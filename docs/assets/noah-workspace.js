(function (g) {
  'use strict';
  var session = g.IL && g.IL.noahAI && g.IL.noahAI.session;
  var runner = g.NoahWorkflows;
  var $ = function (id) { return document.getElementById(id); };
  function node(tag, text, cls) { var e = document.createElement(tag); if (text !== undefined) e.textContent = text; if (cls) e.className = cls; return e; }
  function announce(text) { $('announcement').textContent = text; }
  function perform(action) { try { return action(); } catch (err) { announce(err.message || 'The action could not be completed.'); } }
  function button(text, action, cls) { var b = node('button', text, cls || 'quiet'); b.type = 'button'; b.addEventListener('click', function () { perform(action); }); return b; }
  function download(name, content, mime) {
    var url = URL.createObjectURL(new Blob([content], { type: mime || 'text/plain;charset=utf-8' }));
    var link = node('a'); link.href = url; link.download = name; document.body.appendChild(link); link.click(); link.remove(); setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }
  var reviewAction = null, editId = null, lastFocus = null;
  function review(title, paragraphs, action, approveLabel) {
    lastFocus = document.activeElement; $('review-title').textContent = title; $('review-body').replaceChildren();
    paragraphs.forEach(function (text) { $('review-body').appendChild(node('p', text)); });
    $('review-approve').textContent = approveLabel || 'Approve once'; reviewAction = action; $('review-dialog').showModal();
  }
  $('review-cancel').addEventListener('click', function () { $('review-dialog').close(); });
  $('review-dialog').addEventListener('close', function () { if (lastFocus && lastFocus.isConnected) lastFocus.focus(); });
  $('review-approve').addEventListener('click', async function () {
    var action = reviewAction; reviewAction = null; $('review-dialog').close();
    try { if (action) await action(); } catch (err) { announce(err.message || 'The action failed.'); }
  });
  document.querySelectorAll('[data-view]').forEach(function (b) {
    b.addEventListener('click', function () {
      var view = b.dataset.view;
      document.querySelectorAll('[data-view]').forEach(function (v) { v.setAttribute('aria-pressed', String(v === b)); });
      document.querySelectorAll('.view').forEach(function (v) { v.hidden = v.id !== 'view-' + view; });
      if (view === 'workflows') renderWorkflows();
    });
  });
  ['rail-width', 'context-width'].forEach(function (id) {
    $(id).addEventListener('input', function () { document.documentElement.style.setProperty(id === 'rail-width' ? '--nav-width' : '--context-width', this.value + 'px'); });
  });
  $('collapse-context').addEventListener('click', function () {
    var hidden = $('workspace').classList.toggle('no-context'); this.setAttribute('aria-expanded', String(!hidden)); this.textContent = hidden ? 'Show context panel' : 'Hide context panel';
  });
  if (!session || !runner) { announce('The workspace could not load. Refresh the page; public learning pages remain available.'); $('send').disabled = true; return; }
  function renderSession() {
    var state = session.snapshot(); var log = $('conversation');
    log.replaceChildren();
    if (!state.conversation.length) log.appendChild(node('p', 'Start with what you know, and where the uncertainty begins.', 'empty'));
    state.conversation.forEach(function (m) {
      var box = node('article', undefined, 'message ' + m.role);
      box.appendChild(node('small', m.role === 'user' ? 'YOU' : 'NOAH AI'));
      if (m.role === 'assistant' && g.IL.noahAI.renderReply) {
        var reply = node('div', undefined, 'reply-body'); g.IL.noahAI.renderReply(reply, m.content); box.appendChild(reply);
      } else box.appendChild(node('p', m.content));
      log.appendChild(box);
      if (m.role === 'assistant' && m.notice) box.appendChild(node('p', m.notice, 'notice'));
    });
    log.scrollTop = log.scrollHeight;
    var list = $('memory-list'); list.replaceChildren();
    if (!state.memories.length) list.appendChild(node('p', 'No saved memory. Add a note or a learning goal when it is useful.', 'empty'));
    state.memories.forEach(function (m) {
      var box = node('article', undefined, 'memory-card');
      box.appendChild(node('span', m.kind === 'goal' ? 'LEARNING GOAL' : 'MEMORY NOTE', 'status-tag'));
      box.appendChild(node('p', m.text));
      var actions = node('div', undefined, 'card-actions');
      actions.appendChild(button('Edit', function () { editId = m.id; $('edit-text').value = m.text; $('edit-dialog').showModal(); }, 'quiet'));
      actions.appendChild(button('Forget', function () { session.removeMemory(m.id); announce('The saved item was removed from this browser.'); }));
      actions.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-label', b.textContent + ' ' + (m.kind === 'goal' ? 'goal: ' : 'note: ') + m.text.slice(0, 55)); });
      box.appendChild(actions); list.appendChild(box);
    });
    $('share-memory').checked = state.preferences.shareMemoryWithRemote;
    $('share-context').checked = state.preferences.sharePageContext;
    $('goal-summary').replaceChildren();
    var goals = state.memories.filter(function (m) { return m.kind === 'goal'; });
    if (!goals.length) $('goal-summary').appendChild(node('li', 'No goals saved yet.'));
    goals.slice(0, 6).forEach(function (m) { $('goal-summary').appendChild(node('li', m.text)); });
    var context = session.captureContext(); $('page-context').textContent = context.title + ' · ' + context.path;
    $('storage-status').textContent = state.storage === 'device' ? 'Saved on this device. Cloud synchronization is unavailable.' : 'Browser storage is unavailable. Changes last only while this page is open.';
    if (state.notice) $('storage-status').textContent += ' ' + state.notice;
  }
  g.addEventListener('noah:session', renderSession);
  var submitting = false;
  $('chat-form').addEventListener('submit', async function (event) {
    event.preventDefault(); if (submitting || !this.reportValidity()) return;
    var text = $('message').value.trim(); if (!text) return;
    submitting = true; $('send').disabled = true; $('message').value = '';
    try {
      var result = await g.IL.noahAI.converse(text);
      renderSession(); announce(result.notice || (result.remote ? 'Replied through the university AI service.' : 'Answered from site knowledge on this device.'));
    } catch (_) { announce('Noah could not complete this reply. Your message remains in the conversation.'); }
    finally { submitting = false; $('send').disabled = false; $('message').focus(); }
  });
  $('message').addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) { event.preventDefault(); $('chat-form').requestSubmit(); }
  });
  $('clear-chat').addEventListener('click', function () {
    review('Clear conversation?', ['Remove Noah’s saved conversation from this browser. Explicit memory notes and goals will remain. Previously processed AI requests cannot be withdrawn.'], function () { session.clearConversation(); announce('Conversation cleared. Saved notes and goals remain.'); }, 'Clear conversation');
  });
  $('memory-form').addEventListener('submit', function (event) {
    event.preventDefault(); if (!this.reportValidity()) return;
    perform(function () { session.addMemory({ kind: $('memory-kind').value, text: $('memory-text').value }); $('memory-text').value = ''; announce('Saved on this device. You can edit or forget it at any time.'); });
  });
  $('edit-form').addEventListener('submit', function (event) {
    event.preventDefault(); if (!this.reportValidity()) return;
    perform(function () { session.updateMemory(editId, { text: $('edit-text').value }); $('edit-dialog').close(); announce('Saved memory updated.'); });
  });
  $('edit-cancel').addEventListener('click', function () { $('edit-dialog').close(); });
  $('export-session').addEventListener('click', function () { download('noah-device-data.json', session.exportData(), 'application/json'); announce('Exported the Noah conversation, notes, goals, and sharing preferences.'); });
  $('reset-session').addEventListener('click', function () {
    review('Reset Noah on this device?', ['This removes the Noah conversation, notes, goals, and sharing preferences. Other site data and workflow records are outside this reset.'], function () { session.clearAll(); announce('Noah conversation and memory reset on this device.'); }, 'Reset Noah memory');
  });
  ['share-memory', 'share-context'].forEach(function (id) {
    $(id).addEventListener('change', function () { session.setPreferences({ shareMemoryWithRemote: $('share-memory').checked, sharePageContext: $('share-context').checked }); announce('AI context-sharing preferences updated.'); });
  });
  async function runTask(id) { try { await runner.run(id); } catch (err) { announce(err.message); } renderWorkflows(); }
  function renderWorkflows() {
    var list = $('workflow-list'); list.replaceChildren();
    var tasks = runner.list();
    if (!tasks.length) list.appendChild(node('p', 'No workflows yet. Choose a topic to begin.', 'empty'));
    tasks.slice().reverse().forEach(function (task) {
      var card = node('article', undefined, 'workflow-card'); card.appendChild(node('span', task.status, 'status-tag')); card.appendChild(node('h3', task.title));
      var steps = node('ol');
      task.steps.forEach(function (s) { steps.appendChild(node('li', runner.tools[s.tool].label + ' · ' + s.status)); }); card.appendChild(steps);
      if (task.error) card.appendChild(node('p', task.error));
      var read = task.steps.find(function (s) { return s.tool === 'catalog.search' && s.output; });
      if (read) {
        var sources = node('ul'); read.output.matches.forEach(function (m) { var li = node('li'), a = node('a', m.title); a.href = m.url; li.appendChild(a); sources.appendChild(li); });
        if (read.output.matches.length) card.appendChild(sources); else card.appendChild(node('p', 'No matching rooms. The brief will say so; refine the topic for better results.'));
      }
      var actions = node('div', undefined, 'card-actions');
      if (['ready', 'paused', 'failed'].includes(task.status)) actions.appendChild(button(task.status === 'ready' ? 'Run workflow' : 'Resume workflow', function () { return runTask(task.id); }));
      if (task.status === 'running') actions.appendChild(button('Pause workflow', function () { runner.pause(task.id); renderWorkflows(); }));
      if (task.status === 'approval') actions.appendChild(button('Review next step', function () {
        review('Create this study brief?', ['Topic: ' + task.title, 'The next step writes a Markdown reading brief to this device workspace from the curriculum links shown above. It sends no email, changes no account, and makes no purchase.'], async function () { await runner.approve(task.id); renderWorkflows(); }, 'Create brief');
      }));
      if (!['completed', 'cancelled'].includes(task.status)) actions.appendChild(button('Cancel workflow', function () { runner.cancel(task.id); renderWorkflows(); }));
      var artifact = task.steps.find(function (s) { return s.tool === 'artifact.study-plan' && s.output; });
      if (artifact) actions.appendChild(button('Download study brief', function () { download(artifact.output.filename, artifact.output.markdown); }));
      if (task.status !== 'running') actions.appendChild(button('Remove workflow', function () { review('Remove saved workflow?', ['Remove the saved steps and generated brief for “' + task.title + '” from this device. Downloaded files remain in your Downloads folder.'], function () { runner.remove(task.id); renderWorkflows(); }, 'Remove workflow'); }));
      actions.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-label', b.textContent + ': ' + task.title); });
      card.appendChild(actions);
      var details = node('details'), summary = node('summary', 'Execution history'); details.appendChild(summary);
      task.events.forEach(function (e) { details.appendChild(node('p', new Date(e.at).toLocaleTimeString() + ' · ' + e.text)); }); card.appendChild(details); list.appendChild(card);
    });
    if (!runner.persistent()) announce('Workflow storage is unavailable. Keep this page open; checkpoints cannot survive closing it.');
  }
  $('workflow-form').addEventListener('submit', function (event) {
    event.preventDefault(); if (!this.reportValidity()) return;
    perform(function () { var topic = $('workflow-topic').value.trim(); runner.create({ title: topic, steps: [{ tool: 'catalog.search', input: { query: topic } }, { tool: 'artifact.study-plan', input: { query: topic } }] }); renderWorkflows(); announce('Workflow created. Run it when ready.'); });
  });
  g.addEventListener('noah:workflow', renderWorkflows);
  Object.keys(runner.tools).forEach(function (key) { var info = runner.tools[key], row = node('div', undefined, 'tool-row'); row.appendChild(node('strong', info.label)); row.appendChild(node('span', info.scope + ' · ' + (info.ready ? info.permission : 'unavailable'))); $('tool-list').appendChild(row); });
  var labels = { idle: 'Ready', researching: 'Researching', teaching: 'Teaching', executing: 'Executing workflow', approval: 'Waiting for review', error: 'Needs attention', speaking: 'Speaking', listening: 'Listening' };
  g.addEventListener('noah:activity', function (event) { $('activity').textContent = labels[event.detail && event.detail.state] || 'Ready'; });
  renderSession(); renderWorkflows();
})(window);
