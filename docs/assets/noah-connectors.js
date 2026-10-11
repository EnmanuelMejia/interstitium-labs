/**
 * NoahConnectors — pluggable connector system for Noah AI.
 * (Interstitium original. No dependencies, CSP-safe.)
 *
 * Each connector: { id, label, icon, auth, actions:[{id,label,verbs,params,reversible}], match(text)->action }
 * Noah routes user requests to connectors via verb patterns, executes via
 * backend POST /api/noah/connectors/:id (contract documented below),
 * renders results conversationally, chains actions with confirmation gates.
 *
 * BACKEND CONTRACT (for _worker.js):
 *   POST /api/noah/connectors/:id  { action, params, confirm_token? }
 *   -> { ok:true, summary, data?, needs_confirm?, confirm_token? }
 *   -> { ok:false, error, setup_url? }
 * Until the backend implements a connector, the framework surfaces the
 * setup guidance instead of failing silently.
 *
 * Usage:
 *   NoahConnectors.handle(text) -> {handled:true, html} | {handled:false}
 *   NoahConnectors.list() -> registered connector summaries
 */
(function (g) {
  'use strict';

  var registry = {};
  var PENDING_KEY = 'noah-conn-pending';

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;')
      .replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function register(def) {
    if (!def || !def.id) return;
    registry[def.id] = def;
  }

  /* intent routing: first connector whose action pattern matches wins */
  function route(text) {
    var t = text.toLowerCase();
    var ids = Object.keys(registry);
    for (var i = 0; i < ids.length; i++) {
      var c = registry[ids[i]];
      for (var j = 0; j < (c.actions || []).length; j++) {
        var a = c.actions[j];
        for (var k = 0; k < (a.patterns || []).length; k++) {
          var m = t.match(a.patterns[k]);
          if (m) return { connector: c, action: a, match: m, text: text };
        }
      }
    }
    return null;
  }

  function paramsFrom(action, match, text) {
    var p = {};
    (action.params || []).forEach(function (name, i) {
      p[name] = match[i + 1] ? match[i + 1].trim() : '';
    });
    p._raw = text;
    return p;
  }

  function cardFor(connector, action, params, result) {
    var h = '<div class="noahconn-card">' +
      '<div class="noahconn-head"><span>' + connector.icon + ' ' + esc(connector.label) +
      '</span><span class="noahconn-act">' + esc(action.label) + '</span></div>';
    if (result && result.summary) h += '<div class="noahconn-sum">' + result.summary + '</div>';
    if (result && result.error) h += '<div class="noahconn-err">' + esc(result.error) + '</div>';
    if (result && result.setup_url) {
      h += '<div class="noahconn-setup">Needs setup: <a href="' + esc(result.setup_url) +
        '" target="_blank" rel="noopener">connect ' + esc(connector.label) + '</a></div>';
    }
    return h + '</div>';
  }

  function css() {
    if (document.getElementById('noahconn-css')) return;
    var s = document.createElement('style'); s.id = 'noahconn-css';
    s.textContent = [
      '.noahconn-card{border:1px solid rgba(94,234,212,.25);border-radius:10px;margin:8px 0;',
      'background:rgba(4,10,14,.9);overflow:hidden;}',
      '.noahconn-head{display:flex;justify-content:space-between;align-items:center;',
      'padding:8px 12px;background:rgba(94,234,212,.07);font-size:12px;color:#5EEAD4;}',
      '.noahconn-act{color:#8b93a5;}',
      '.noahconn-sum{padding:10px 12px;font-size:13px;color:#dbe4ee;line-height:1.55;}',
      '.noahconn-err{padding:10px 12px;font-size:13px;color:#ff8fa3;}',
      '.noahconn-setup{padding:0 12px 10px;font-size:12px;color:#8b93a5;}',
      '.noahconn-setup a{color:#5EEAD4;}',
      '.noahconn-confirm{padding:10px 12px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;}',
      '.noahconn-confirm button{background:rgba(201,162,39,.2);border:1px solid #c9a227;color:#fff;',
      'border-radius:6px;padding:6px 14px;cursor:pointer;font-size:12px;}',
      '.noahconn-confirm button.cancel{background:transparent;border-color:rgba(255,255,255,.2);color:#8b93a5;}',
      '.noahconn-prog{padding:8px 12px;font-size:12px;color:#8b93a5;}',
      '.noahconn-prog .bar{height:4px;background:rgba(255,255,255,.1);border-radius:2px;margin-top:6px;}',
      '.noahconn-prog .bar i{display:block;height:100%;background:#5EEAD4;border-radius:2px;transition:width .3s;}'
    ].join('');
    document.head.appendChild(s);
  }

  function callBackend(connId, actionId, params, confirmToken) {
    var body = { action: actionId, params: params };
    if (confirmToken) body.confirm_token = confirmToken;
    return fetch('/api/noah/connectors/' + encodeURIComponent(connId), {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }).then(function (r) { return r.json(); })
    .catch(function () {
      return { ok: false, error: 'Connector service unreachable.',
               setup: 'The ' + connId + ' connector needs its backend route. See NOAH_CONNECTORS.md.' };
    });
  }

  function execute(routed, host) {
    css();
    var c = routed.connector, a = routed.action;
    var params = paramsFrom(a, routed.match, routed.text);
    /* confirmation gate for irreversible actions */
    if (a.reversible === false && !params._confirmed) {
      var box = document.createElement('div');
      box.innerHTML = cardFor(c, a, params, {
        summary: 'This will <strong>' + esc(a.label.toLowerCase()) + '</strong>. Confirm to proceed.'
      });
      var row = document.createElement('div'); row.className = 'noahconn-confirm';
      var yes = document.createElement('button'); yes.textContent = 'Confirm';
      var no = document.createElement('button'); no.textContent = 'Cancel'; no.className = 'cancel';
      yes.addEventListener('click', function () {
        params._confirmed = true;
        box.querySelector('.noahconn-confirm').remove();
        run();
      });
      no.addEventListener('click', function () {
        box.querySelector('.noahconn-confirm').innerHTML = '<span style="color:#8b93a5;font-size:12px">Cancelled.</span>';
      });
      row.appendChild(yes); row.appendChild(no); box.appendChild(row);
      host.appendChild(box);
      return;
    }
    run();
    function run() {
      var prog = document.createElement('div');
      prog.className = 'noahconn-prog';
      prog.innerHTML = 'Working…<div class="bar"><i style="width:30%"></i></div>';
      host.appendChild(prog);
      callBackend(c.id, a.id, params).then(function (res) {
        prog.querySelector('i').style.width = '100%';
        setTimeout(function () { prog.remove(); }, 400);
        var box = document.createElement('div');
        box.innerHTML = cardFor(c, a, params, res);
        host.appendChild(box);
        if (res.ok && res.chain && res.chain.length && g.NoahConnectors) {
          chain(res.chain, host);
        }
      });
    }
  }

  /* autonomous chaining: [{connector, action, params}] executed in order */
  function chain(steps, host) {
    var i = 0;
    var prog = document.createElement('div');
    prog.className = 'noahconn-prog';
    prog.innerHTML = '<span class="lbl"></span><div class="bar"><i style="width:0%"></i></div>' +
      '<button type="button" class="noahconn-cancel" style="margin-top:6px">Cancel chain</button>';
    host.appendChild(prog);
    var cancelled = false;
    prog.querySelector('.noahconn-cancel').addEventListener('click', function () {
      cancelled = true;
      prog.querySelector('.lbl').textContent = 'Chain cancelled.';
    });
    (function next() {
      if (cancelled || i >= steps.length) {
        if (!cancelled) prog.querySelector('.lbl').textContent = 'Done — ' + steps.length + ' steps.';
        return;
      }
      var s = steps[i];
      var c = registry[s.connector];
      prog.querySelector('.lbl').textContent = 'Step ' + (i + 1) + '/' + steps.length + ': ' + (c ? c.label : s.connector);
      prog.querySelector('i').style.width = Math.round((i / steps.length) * 100) + '%';
      if (!c) { i++; next(); return; }
      callBackend(s.connector, s.action, s.params || {}).then(function (res) {
        var box = document.createElement('div');
        var act = (c.actions || []).filter(function (x) { return x.id === s.action; })[0] || { label: s.action };
        box.innerHTML = cardFor(c, act, s.params, res);
        host.appendChild(box);
        i++; next();
      });
    })();
  }

  /* ---------------- built-in connectors ---------------- */

  register({
    id: 'gmail', label: 'Gmail', icon: '📧',
    auth: 'oauth-google',
    actions: [
      { id: 'search', label: 'Search mail', reversible: true,
        patterns: [/search (?:my )?mail for (.+)/i, /find (?:the )?email (?:about )?(.+)/i, /check (?:my )?email/i],
        params: ['query'] },
      { id: 'read', label: 'Read thread', reversible: true,
        patterns: [/read (?:the )?email (?:about )?(.+)/i], params: ['query'] },
      { id: 'draft', label: 'Draft email', reversible: true,
        patterns: [/draft (?:an )?email to (\S+)(?: about (.+))?/i], params: ['to', 'subject'] },
      { id: 'send', label: 'Send email', reversible: false,
        patterns: [/send (?:an )?email to (\S+)(?: about (.+))?/i], params: ['to', 'subject'] }
    ]
  });

  register({
    id: 'gcal', label: 'Google Calendar', icon: '📅',
    auth: 'oauth-google',
    actions: [
      { id: 'freebusy', label: 'Check availability', reversible: true,
        patterns: [/(?:am i|are you) free (.+)/i, /check (?:my )?calendar(?: for (.+))?/i, /what(?:'s| is) on (?:my )?calendar (.+)/i],
        params: ['when'] },
      { id: 'schedule', label: 'Schedule event', reversible: false,
        patterns: [/schedule (?:a )?(.+?) (?:on|for) (.+)/i, /add (?:a )?calendar event (.+)/i],
        params: ['title', 'when'] },
      { id: 'list', label: 'Upcoming events', reversible: true,
        patterns: [/(?:what's|what is) (?:coming up|next|on my schedule)/i, /list (?:my )?upcoming events/i],
        params: [] }
    ]
  });

  register({
    id: 'github', label: 'GitHub', icon: '🐙',
    auth: 'oauth-github',
    actions: [
      { id: 'status', label: 'Repo status', reversible: true,
        patterns: [/(?:github )?status of ([\w\-\/.]+)/i, /check (?:the )?repo ([\w\-\/.]+)/i],
        params: ['repo'] },
      { id: 'prs', label: 'List PRs', reversible: true,
        patterns: [/list (?:open )?prs?(?: for| in)? ([\w\-\/.]+)?/i, /(?:show|check) pull requests/i],
        params: ['repo'] },
      { id: 'issues', label: 'List issues', reversible: true,
        patterns: [/list issues(?: for| in)? ([\w\-\/.]+)?/i],
        params: ['repo'] },
      { id: 'trigger', label: 'Trigger workflow', reversible: false,
        patterns: [/trigger (?:the )?workflow ([\w\-\/.]+) on ([\w\-\/.]+)/i, /run (?:the )?workflow ([\w\-\/.]+)/i],
        params: ['workflow', 'repo'] }
    ]
  });

  g.NoahConnectors = {
    version: 1,
    register: register,
    list: function () {
      return Object.keys(registry).map(function (id) {
        var c = registry[id];
        return { id: id, label: c.label, icon: c.icon, actions: (c.actions || []).map(function (a) { return a.id; }) };
      });
    },
    /* returns true when a connector claimed the text */
    handle: function (text, host) {
      var r = route(text);
      if (!r) return false;
      execute(r, host || document.body);
      return true;
    },
    chain: chain,
    /* 2026-10-11: setup URL for OAuth flows — used by onboarding */
    getSetupUrl: function (connId) {
      var c = registry[connId];
      if (!c) return null;
      /* v1: direct to Noah settings; v2 will return the OAuth authorize URL */
      return '/noah/#settings';
    },
    get: function (connId) { return registry[connId] || null; }
  };
})(typeof window !== 'undefined' ? window : this);
