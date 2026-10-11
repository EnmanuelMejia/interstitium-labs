/* Noah/Genesis Settings — the canonical Settings home (2026-10-11).
 *
 * Full-application fold-in: one Settings surface inside Noah (mirrored
 * for Genesis — same page, tutor-aware) holding account & profile, the
 * Secure Store (per-user saved logins), connectors, goals, reminders &
 * briefing, memory controls, files & documents, payments, voice & tutor,
 * permissions, devices, activity, and privacy & data.
 *
 * Entry points (<=2 taps from the Noah panel):
 *   - the "⚙ Settings" sidebar button on /noah/
 *   - the /noah/#settings deep link (the target the floating widget's
 *     settings card already points at)
 *   - window.ILSettings.open(section?)
 *
 * Secure Store rules (enforced server-side by the credential broker,
 * /api/credentials): values are encrypted at rest, are NEVER returned
 * by any endpoint, never rendered here, and never logged. This client
 * never holds a secret at all — capture happens only on the protected
 * /account/credentials/ page hosted by the broker's own module.
 *
 * Signed-out visitors get honest sign-in prompts per section — account
 * data needs an account to follow you. */
(function () {
  'use strict';
  if (window.ILSettings) return;
  if (!document.getElementById('newChatBtn')) return; /* /noah/ only */

  var state = {
    open: false, me: undefined, /* undefined=unknown, null=signed out */
    vault: null, vaultState: '', connectors: null, goals: null,
    reminders: null, remindersState: '', briefing: null, certs: null,
    activity: null, loaded: {}
  };

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function $(id) { return document.getElementById(id); }
  function api(path, opts) {
    opts = opts || {};
    var headers = { accept: 'application/json' };
    if (opts.body != null) headers['content-type'] = 'application/json';
    return fetch(path, {
      method: opts.method || 'GET', credentials: 'same-origin', headers: headers,
      body: opts.body != null ? JSON.stringify(opts.body) : undefined
    }).then(function (res) {
      return res.json().catch(function () { return { ok: false, error: 'bad_response' }; })
        .then(function (j) { return { status: res.status, j: j }; });
    });
  }
  function tutorId() {
    try {
      var p = JSON.parse(localStorage.getItem('il-noah-profile') || '{}');
      return p && p.avatar === 'genesis' ? 'genesis' : 'noah';
    } catch (e) { return 'noah'; }
  }
  function tutorName() { return tutorId() === 'genesis' ? 'Genesis' : 'Noah'; }
  function obProfile() {
    try { return JSON.parse(localStorage.getItem('noah-user-profile') || '{}') || {}; }
    catch (e) { return {}; }
  }
  function saveObProfile(p) {
    try { localStorage.setItem('noah-user-profile', JSON.stringify(p)); } catch (e) {}
    if (window.NoahOnboarding && NoahOnboarding.saveProfile) {
      try { NoahOnboarding.saveProfile(p); } catch (e) {}
    }
  }
  function fmtDate(iso) {
    if (!iso) return '';
    var d = new Date(iso);
    if (isNaN(d.getTime())) return esc(String(iso).slice(0, 10));
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
  }
  function fmtDateTime(iso) {
    if (!iso) return '';
    var d = new Date(iso);
    if (isNaN(d.getTime())) return esc(String(iso).slice(0, 16).replace('T', ' '));
    return d.toLocaleString(undefined, { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
  }
  function signInNote(what) {
    return '<p class="ils-note">Sign in to use ' + esc(what) + ' — they follow your account, not this browser.</p>' +
      '<p><a class="ils-btn" href="/account/">Sign in</a></p>';
  }

  /* ---------------- CSS ---------------- */
  var css = [
    '#settingsBtn{position:relative}',
    '.ils-overlay{position:fixed;inset:0;background:rgba(4,6,12,.55);z-index:70;opacity:0;pointer-events:none;transition:opacity .2s}',
    '.ils-overlay.on{opacity:1;pointer-events:auto}',
    '.ils-panel{position:fixed;top:0;right:0;height:100dvh;width:min(460px,96vw);z-index:71;',
    'background:var(--panel,#10141d);color:var(--text,#e8e4da);border-left:1px solid rgba(201,162,39,.25);',
    'transform:translateX(105%);transition:transform .25s ease;display:flex;flex-direction:column;',
    'box-shadow:-18px 0 50px rgba(0,0,0,.5)}',
    '.ils-panel.on{transform:none}',
    '.ils-head{display:flex;align-items:center;gap:.6rem;padding:1rem 1.1rem;border-bottom:1px solid rgba(255,255,255,.08)}',
    '.ils-head h2{font-size:1.05rem;margin:0;flex:1}',
    '.ils-head button{background:none;border:1px solid rgba(255,255,255,.15);color:inherit;border-radius:8px;padding:.3rem .6rem;cursor:pointer}',
    '.ils-nav{display:flex;gap:.4rem;flex-wrap:wrap;padding:.7rem 1.1rem;border-bottom:1px solid rgba(255,255,255,.06)}',
    '.ils-nav a{font-size:.78rem;color:inherit;text-decoration:none;border:1px solid rgba(255,255,255,.14);border-radius:999px;padding:.25rem .6rem;white-space:nowrap}',
    '.ils-nav a:hover{border-color:rgba(201,162,39,.6)}',
    '.ils-body{overflow-y:auto;padding:0 1.1rem 2rem;flex:1}',
    '.ils-sec{padding:1.05rem 0 .4rem;border-bottom:1px solid rgba(255,255,255,.06)}',
    '.ils-sec:last-child{border-bottom:none}',
    '.ils-sec h3{font-size:.98rem;margin:0 0 .55rem;display:flex;align-items:center;gap:.45rem}',
    '.ils-note{color:var(--muted,#9aa7b8);font-size:.85rem;line-height:1.45;margin:.35rem 0}',
    '.ils-row{display:flex;align-items:center;gap:.6rem;padding:.5rem 0;border-top:1px solid rgba(255,255,255,.05)}',
    '.ils-row:first-of-type{border-top:none}',
    '.ils-row .ils-grow{flex:1;min-width:0}',
    '.ils-row .ils-sub{color:var(--muted,#9aa7b8);font-size:.8rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}',
    '.ils-pill{font-size:.72rem;border-radius:999px;padding:.12rem .55rem;border:1px solid rgba(255,255,255,.18);white-space:nowrap}',
    '.ils-pill.on{border-color:rgba(52,211,153,.6);color:#34d399}',
    '.ils-pill.off{color:var(--muted,#9aa7b8)}',
    '.ils-btn{display:inline-block;background:rgba(201,162,39,.14);border:1px solid rgba(201,162,39,.45);color:inherit;',
    'border-radius:9px;padding:.42rem .8rem;font:inherit;font-size:.85rem;cursor:pointer;text-decoration:none}',
    '.ils-btn:hover{background:rgba(201,162,39,.24)}',
    '.ils-btn.ghost{background:none;border-color:rgba(255,255,255,.18)}',
    '.ils-btn.danger{background:rgba(185,28,28,.16);border-color:rgba(185,28,28,.55)}',
    '.ils-btn:disabled{opacity:.5;cursor:default}',
    '.ils-form{display:flex;flex-direction:column;gap:.5rem;margin:.6rem 0}',
    '.ils-form label{font-size:.8rem;color:var(--muted,#9aa7b8);display:flex;flex-direction:column;gap:.25rem}',
    '.ils-form input,.ils-form select{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);',
    'border-radius:9px;color:inherit;padding:.55rem .65rem;font:inherit;font-size:.9rem;width:100%;box-sizing:border-box}',
    '.ils-status{font-size:.85rem;min-height:1.1em;margin:.3rem 0}',
    '.ils-status.err{color:#fca5a5}.ils-status.ok{color:#34d399}',
    '.ils-tutors{display:flex;gap:.6rem;margin:.5rem 0}',
    '.ils-tutor{flex:1;border:1px solid rgba(255,255,255,.15);border-radius:12px;padding:.7rem;text-align:center;cursor:pointer;background:none;color:inherit;font:inherit}',
    '.ils-tutor.sel{border-color:rgba(201,162,39,.7);background:rgba(201,162,39,.08)}',
    '.ils-tutor .ils-tname{font-weight:700;display:block;margin-top:.3rem}',
    '.ils-tutor .ils-tsub{font-size:.75rem;color:var(--muted,#9aa7b8)}',
    '.ils-switch{display:flex;align-items:center;gap:.6rem;cursor:pointer;padding:.4rem 0}',
    '.ils-switch input{width:1.1rem;height:1.1rem;accent-color:#c9a227}',
    '.ils-brief{background:rgba(201,162,39,.07);border:1px solid rgba(201,162,39,.25);border-radius:12px;padding:.7rem .85rem;margin:.4rem 0}',
    '.ils-brief p{margin:.25rem 0;font-size:.9rem;line-height:1.45}',
    '.ils-del-confirm{display:none;margin-top:.5rem}',
    '.ils-del-confirm.on{display:block}'
  ].join('\n');
  var style = document.createElement('style');
  style.id = 'ils-css';
  style.textContent = css;
  document.head.appendChild(style);

  /* ---------------- Panel skeleton ---------------- */
  var newBtn = $('newChatBtn');
  var settingsBtn = document.createElement('button');
  settingsBtn.className = 'new-chat';
  settingsBtn.id = 'settingsBtn';
  settingsBtn.type = 'button';
  settingsBtn.innerHTML = '⚙ Settings';
  var anchor = $('goalsBtn') || newBtn;
  anchor.parentNode.insertBefore(settingsBtn, anchor.nextSibling);

  var overlay = document.createElement('div');
  overlay.className = 'ils-overlay';
  var panel = document.createElement('aside');
  panel.className = 'ils-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', 'Settings');
  panel.innerHTML =
    '<div class="ils-head"><h2>⚙ Settings · <span id="ilsTutorName">Noah</span></h2>' +
    '<button type="button" id="ilsClose" aria-label="Close settings">✕</button></div>' +
    '<nav class="ils-nav" aria-label="Settings sections">' +
    ['today|☀ Today', 'account|Account', 'vault|🔐 Secure Store', 'connectors|Connectors',
     'goals|Goals', 'reminders|Reminders', 'memory|Memory', 'files|Files',
     'payments|Payments', 'voice|Voice', 'privacy|Privacy & data']
      .map(function (s) {
        var p = s.split('|');
        return '<a href="#settings/' + p[0] + '" data-ils-nav="' + p[0] + '">' + p[1] + '</a>';
      }).join('') +
    '</nav>' +
    '<div class="ils-body" id="ilsBody">' +
    '<section class="ils-sec" id="ils-sec-today"><h3>☀ Today</h3><div data-ils-slot="today"><p class="ils-note">Loading your briefing…</p></div></section>' +
    '<section class="ils-sec" id="ils-sec-account"><h3>👤 Account &amp; profile</h3><div data-ils-slot="account"><p class="ils-note">Loading…</p></div></section>' +
    '<section class="ils-sec" id="ils-sec-vault"><h3>🔐 Secure Store</h3><div data-ils-slot="vault"><p class="ils-note">Loading…</p></div></section>' +
    '<section class="ils-sec" id="ils-sec-connectors"><h3>🔌 Connectors</h3><div data-ils-slot="connectors"><p class="ils-note">Loading…</p></div></section>' +
    '<section class="ils-sec" id="ils-sec-goals"><h3>🎯 Goals</h3><div data-ils-slot="goals"><p class="ils-note">Loading…</p></div></section>' +
    '<section class="ils-sec" id="ils-sec-reminders"><h3>⏰ Reminders</h3><div data-ils-slot="reminders"><p class="ils-note">Loading…</p></div></section>' +
    '<section class="ils-sec" id="ils-sec-memory"><h3>🧠 Memory</h3><div data-ils-slot="memory"><p class="ils-note">Loading…</p></div></section>' +
    '<section class="ils-sec" id="ils-sec-files"><h3>📁 Files &amp; documents</h3><div data-ils-slot="files"><p class="ils-note">Loading…</p></div></section>' +
    '<section class="ils-sec" id="ils-sec-payments"><h3>💳 Payments</h3><div data-ils-slot="payments"></div></section>' +
    '<section class="ils-sec" id="ils-sec-voice"><h3>🎙 Voice &amp; tutor</h3><div data-ils-slot="voice"></div></section>' +
    '<section class="ils-sec" id="ils-sec-perms"><h3>🛡 Permissions &amp; approvals</h3><div data-ils-slot="perms"></div></section>' +
    '<section class="ils-sec" id="ils-sec-devices"><h3>📱 Devices</h3><div data-ils-slot="devices"></div></section>' +
    '<section class="ils-sec" id="ils-sec-activity"><h3>🕘 Recent account activity</h3><div data-ils-slot="activity"><p class="ils-note">Loading…</p></div></section>' +
    '<section class="ils-sec" id="ils-sec-privacy"><h3>🔒 Privacy &amp; data</h3><div data-ils-slot="privacy"></div></section>' +
    '<section class="ils-sec" id="ils-sec-about"><h3>ℹ About &amp; legal</h3>' +
    '<p class="ils-note">Interstitium Labs — Noah and Genesis are AI assistants; answers are AI-generated and can be wrong. Verify important facts.</p>' +
    '<p><a class="ils-btn ghost" href="/privacy/">Privacy, in plain language</a> ' +
    '<a class="ils-btn ghost" href="/about/">About Interstitium Labs</a></p></section>' +
    '</div>';
  document.body.appendChild(overlay);
  document.body.appendChild(panel);

  function slot(name) { return panel.querySelector('[data-ils-slot="' + name + '"]'); }
  function openPanel(section) {
    state.open = true;
    overlay.classList.add('on');
    panel.classList.add('on');
    var tn = $('ilsTutorName');
    if (tn) tn.textContent = tutorName();
    loadAll();
    if (section) {
      setTimeout(function () {
        var el = $('ils-sec-' + section);
        if (el) el.scrollIntoView({ block: 'start', behavior: 'smooth' });
      }, 280);
    }
    var c = $('ilsClose');
    if (c) c.focus();
  }
  function closePanel() {
    state.open = false;
    overlay.classList.remove('on');
    panel.classList.remove('on');
    if (location.hash.indexOf('#settings') === 0) {
      try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {}
    }
  }
  settingsBtn.addEventListener('click', function () { state.open ? closePanel() : openPanel(); });
  overlay.addEventListener('click', closePanel);
  $('ilsClose').addEventListener('click', closePanel);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && state.open) closePanel();
  });
  panel.querySelectorAll('[data-ils-nav]').forEach(function (a) {
    a.addEventListener('click', function (ev) {
      ev.preventDefault();
      var el = $('ils-sec-' + a.getAttribute('data-ils-nav'));
      if (el) el.scrollIntoView({ block: 'start', behavior: 'smooth' });
    });
  });

  function loadAll() {
    loadMe().then(function () {
      renderAccount(); renderVoice(); renderPerms(); renderDevices(); renderPayments(); renderPrivacy();
      loadBriefing(); loadVault(); loadConnectors(); loadGoals(); loadReminders();
      renderMemory(); loadFiles(); loadActivity();
    });
  }
  function loadMe() {
    if (state.me !== undefined) return Promise.resolve();
    return api('/api/me').then(function (r) {
      state.me = (r.status === 200 && r.j && r.j.ok && r.j.email) ? String(r.j.email) : null;
    }).catch(function () { state.me = null; });
  }

  /* ---------------- Account & profile ---------------- */
  function renderAccount() {
    var el = slot('account');
    var p = obProfile();
    var t = tutorId();
    var html = '';
    if (state.me) {
      html += '<div class="ils-row"><div class="ils-grow"><div>' + esc(state.me) + '</div>' +
        '<div class="ils-sub">Signed in — your data follows this account on every device.</div></div>' +
        '<span class="ils-pill on">Signed in</span></div>';
    } else {
      html += signInNote('your account settings');
    }
    html += '<div class="ils-form"><label>Your name (how ' + esc(tutorName()) + ' greets you)' +
      '<input id="ilsName" type="text" maxlength="60" autocomplete="name" value="' + esc(p.name || '') + '" placeholder="Your name"></label></div>';
    html += '<p class="ils-note" style="margin-bottom:.2rem">Your tutor — same brain, same memory, same everything. Pick who you talk to:</p>';
    html += '<div class="ils-tutors">' +
      '<button type="button" class="ils-tutor' + (t === 'noah' ? ' sel' : '') + '" data-ils-tutor="noah">' +
      '<img src="/assets/noah/noah-avatar-3d.webp" alt="" width="52" height="52" style="border-radius:50%">' +
      '<span class="ils-tname">Noah</span><span class="ils-tsub">Default tutor</span></button>' +
      '<button type="button" class="ils-tutor' + (t === 'genesis' ? ' sel' : '') + '" data-ils-tutor="genesis">' +
      '<img src="/assets/noah/genesis-avatar-3d.webp" alt="" width="52" height="52" style="border-radius:50%">' +
      '<span class="ils-tname">Genesis</span><span class="ils-tsub">Twin tutor</span></button></div>';
    html += '<p><button type="button" class="ils-btn" id="ilsSaveProfile">Save profile</button> ' +
      (state.me ? '<button type="button" class="ils-btn ghost" id="ilsSignOut">Sign out</button>' : '') +
      '</p><p class="ils-status" id="ilsAcctStatus" role="status"></p>';
    el.innerHTML = html;
    el.querySelectorAll('[data-ils-tutor]').forEach(function (b) {
      b.addEventListener('click', function () {
        try {
          var raw = JSON.parse(localStorage.getItem('il-noah-profile') || '{}') || {};
          raw.avatar = b.getAttribute('data-ils-tutor');
          localStorage.setItem('il-noah-profile', JSON.stringify(raw));
          window.dispatchEvent(new Event('il-noah-profile'));
        } catch (e) {}
        var tn = $('ilsTutorName');
        if (tn) tn.textContent = tutorName();
        renderAccount(); renderVoice();
      });
    });
    var save = $('ilsSaveProfile');
    if (save) save.addEventListener('click', function () {
      var pp = obProfile();
      pp.name = ($('ilsName').value || '').trim().slice(0, 60);
      saveObProfile(pp);
      var st = $('ilsAcctStatus');
      if (st) { st.textContent = '✓ Profile saved.'; st.className = 'ils-status ok'; }
      if (window.ILSync && ILSync.syncNow) { try { ILSync.syncNow(); } catch (e) {} }
    });
    var so = $('ilsSignOut');
    if (so) so.addEventListener('click', function () {
      api('/api/auth/signout', { method: 'POST' }).then(function () {
        state.me = null; state.loaded = {};
        loadAll();
      });
    });
  }

  /* ---------------- Secure Store (credential broker) ----------------
   * The store itself is the canonical credential broker
   * (il-cred-broker.js + /api/credentials): a fixed service directory,
   * AES-GCM envelopes server-side, capture only on the protected
   * /account/credentials/ page. This section HOSTS the broker's own
   * Settings section so there is exactly one store and one store UI —
   * no second vault is built here. */
  function loadVault() {
    var el = slot('vault');
    el.innerHTML = '<p class="ils-note">Your saved logins for the services ' + esc(tutorName()) +
      ' works with. Values are encrypted on the server and are never shown anywhere — ' +
      'you add a login once on the protected capture page, and ' + esc(tutorName()) +
      ' only ever sees names and status.</p>' +
      '<div id="ilsCredHost"></div>' +
      '<p style="margin-top:.7rem"><a class="ils-btn" href="/account/credentials/" target="_blank" rel="noopener">' +
      'Open the secure capture page</a></p>';
    var host = el.querySelector('#ilsCredHost');
    if (window.ILCredBroker && ILCredBroker.renderSettingsSection) {
      try { ILCredBroker.renderSettingsSection(host); } catch (e) {}
    } else {
      host.innerHTML = '<p class="ils-note">The secure store module is still loading — reopen Settings in a moment.</p>';
    }
  }

  /* ---------------- Connectors ---------------- */
  function loadConnectors() {
    var el = slot('connectors');
    var local = (window.NoahConnectors && NoahConnectors.list) ? NoahConnectors.list() : [];
    api('/api/noah/connectors').then(function (r) {
      var defs = (r.j && r.j.connectors) || [];
      var byId = {};
      local.forEach(function (c) { byId[c.id] = c; });
      defs.forEach(function (c) { if (!byId[c.id]) byId[c.id] = c; });
      var ids = Object.keys(byId);
      var p = obProfile();
      var conns = p.connections || {};
      if (!ids.length) {
        el.innerHTML = '<p class="ils-note">No connectors registered yet.</p>';
        return;
      }
      el.innerHTML = '<p class="ils-note">Services ' + esc(tutorName()) + ' can act on for you. ' +
        'Irreversible actions (send, schedule, trigger) always stop for your approval first.</p>' +
        ids.map(function (id) {
          var c = byId[id];
          var connected = !!conns[id];
          return '<div class="ils-row"><div class="ils-grow"><div>' + esc(c.icon || '🔌') + ' ' +
            esc(c.label || id) + '</div><div class="ils-sub">' +
            ((c.actions || []).map(function (a) { return esc(a.label); }).join(' · ') || 'Connected service') +
            '</div></div>' +
            '<span class="ils-pill ' + (connected ? 'on' : 'off') + '">' +
            (connected ? 'Connected' : 'Not connected') + '</span></div>';
        }).join('') +
        '<p class="ils-note">Connect or disconnect a service from the ⚙ menu in the ' +
        esc(tutorName()) + ' chat panel, or just ask ' + esc(tutorName()) + ' to use it.</p>';
    }).catch(function () {
      el.innerHTML = '<p class="ils-note">Connector status could not be loaded just now.</p>';
    });
  }

  /* ---------------- Goals ---------------- */
  function loadGoals() {
    var el = slot('goals');
    if (!state.me) { el.innerHTML = signInNote('goals'); return; }
    api('/api/goals').then(function (r) {
      var goals = (r.j && r.j.goals) || [];
      var active = goals.filter(function (g) { return g.status === 'active'; }).length;
      var done = goals.filter(function (g) { return g.status === 'completed'; }).length;
      el.innerHTML = '<p class="ils-note">Tell ' + esc(tutorName()) + ' a goal and it plans and works it with you — ' +
        'tutoring, money, health, shopping, relationships.</p>' +
        '<div class="ils-row"><div class="ils-grow"><div>' + active + ' active · ' + done + ' completed</div>' +
        '<div class="ils-sub">' + goals.length + ' total</div></div>' +
        '<button type="button" class="ils-btn" id="ilsOpenGoals">Open Goals</button></div>';
      var b = $('ilsOpenGoals');
      if (b) b.addEventListener('click', function () {
        closePanel();
        var gb = $('goalsBtn');
        if (gb) gb.click();
      });
    }).catch(function () {
      el.innerHTML = '<p class="ils-note">Goal summary could not be loaded just now.</p>';
    });
  }

  /* ---------------- Reminders ---------------- */
  function loadReminders() {
    var el = slot('reminders');
    if (!state.me) { el.innerHTML = signInNote('reminders'); return; }
    api('/api/reminders').then(function (r) {
      if (r.status === 404) {
        el.innerHTML = '<p class="ils-note">Reminders arrive with the next platform update — ' +
          'your goals already nudge you when steps come due.</p>';
        return;
      }
      if (!r.j || !r.j.ok) {
        el.innerHTML = '<p class="ils-note">Reminders could not be loaded just now.</p>';
        return;
      }
      state.reminders = r.j.reminders || [];
      renderReminders();
    }).catch(function () {
      el.innerHTML = '<p class="ils-note">Reminders could not be loaded just now.</p>';
    });
  }
  function renderReminders() {
    var el = slot('reminders');
    var list = (state.reminders || []).slice().sort(function (a, b) {
      return String(a.due_at) < String(b.due_at) ? -1 : 1;
    });
    var now = Date.now();
    var html = '<p class="ils-note">Reminders surface here, in your Today briefing, and when you open ' +
      esc(tutorName()) + '. (Email/push delivery comes later.)</p>';
    if (!list.length) html += '<p class="ils-note">No reminders set.</p>';
    html += list.map(function (rm) {
      var overdue = !rm.done && new Date(rm.due_at).getTime() < now;
      return '<div class="ils-row"><div class="ils-grow"><div>' + (rm.done ? '<s>' : '') +
        esc(rm.text) + (rm.done ? '</s>' : '') + '</div>' +
        '<div class="ils-sub">' + (overdue ? '⚠ Overdue · ' : '') + fmtDateTime(rm.due_at) +
        (rm.repeat && rm.repeat !== 'none' ? ' · repeats ' + esc(rm.repeat) : '') + '</div></div>' +
        (rm.done ? '<span class="ils-pill on">Done</span>'
          : '<button type="button" class="ils-btn ghost" data-ils-rdone="' + esc(rm.id) + '">Done</button>') +
        '<button type="button" class="ils-btn ghost" data-ils-rdel="' + esc(rm.id) + '">Delete</button></div>';
    }).join('');
    html += '<form class="ils-form" id="ilsRemForm">' +
      '<label>Reminder<input id="ilsRemText" type="text" maxlength="300" required placeholder="e.g. Review VPN notes"></label>' +
      '<label>When<input id="ilsRemWhen" type="datetime-local" required></label>' +
      '<label>Repeat<select id="ilsRemRepeat"><option value="none">Never</option>' +
      '<option value="daily">Daily</option><option value="weekly">Weekly</option></select></label>' +
      '<p style="margin:.2rem 0"><button type="submit" class="ils-btn">Add reminder</button></p>' +
      '<p class="ils-status" id="ilsRemStatus" role="status"></p></form>';
    el.innerHTML = html;
    el.querySelectorAll('[data-ils-rdone]').forEach(function (b) {
      b.addEventListener('click', function () {
        api('/api/reminders/' + encodeURIComponent(b.getAttribute('data-ils-rdone')) + '/done', { method: 'POST', body: {} })
          .then(loadReminders);
      });
    });
    el.querySelectorAll('[data-ils-rdel]').forEach(function (b) {
      b.addEventListener('click', function () {
        api('/api/reminders/' + encodeURIComponent(b.getAttribute('data-ils-rdel')), { method: 'DELETE' })
          .then(loadReminders);
      });
    });
    var form = $('ilsRemForm');
    if (form) form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var st = $('ilsRemStatus');
      var when = $('ilsRemWhen').value;
      if (!when) { st.textContent = 'Pick a date and time.'; st.className = 'ils-status err'; return; }
      api('/api/reminders', {
        method: 'POST',
        body: {
          text: ($('ilsRemText').value || '').trim(),
          due_at: new Date(when).toISOString(),
          repeat: $('ilsRemRepeat').value
        }
      }).then(function (r) {
        if (r.j && r.j.ok) { loadReminders(); }
        else { st.textContent = 'Could not add: ' + esc((r.j && r.j.error) || 'error'); st.className = 'ils-status err'; }
      });
    });
  }

  /* ---------------- Today briefing ---------------- */
  function loadBriefing() {
    var el = slot('today');
    if (!state.me) {
      el.innerHTML = '<p class="ils-note">Your daily briefing — goals due, reminders, and job alerts — appears here when you sign in.</p>' +
        '<p><a class="ils-btn" href="/account/">Sign in</a></p>';
      return;
    }
    api('/api/briefing').then(function (r) {
      if (r.j && r.j.ok) { renderBriefing(r.j); return; }
      /* Fallback: goal check-in alone (endpoint predates the briefing API). */
      return api('/api/goals/checkin').then(function (c) {
        var due = (c.j && c.j.due) || [];
        renderBriefing({
          lines: due.length
            ? ['☀️ ' + due.length + (due.length === 1 ? ' goal step is' : ' goal steps are') + ' due.']
            : ['☀️ Nothing due right now — a clean slate.'],
          due_goals: due, due_reminders: []
        });
      });
    }).catch(function () {
      el.innerHTML = '<p class="ils-note">Your briefing could not be loaded just now.</p>';
    });
  }
  function renderBriefing(b) {
    var el = slot('today');
    var html = '<div class="ils-brief">';
    (b.lines && b.lines.length ? b.lines : ['☀️ Nothing due right now.']).forEach(function (ln) {
      html += '<p>' + esc(ln) + '</p>';
    });
    html += '</div>';
    (b.due_goals || []).slice(0, 4).forEach(function (d) {
      html += '<div class="ils-row"><div class="ils-grow"><div>' + esc(d.step || '') + '</div>' +
        '<div class="ils-sub">' + esc(d.title || '') + (d.overdue ? ' · overdue' : ' · due ' + fmtDate(d.due)) + '</div></div></div>';
    });
    (b.due_reminders || []).slice(0, 4).forEach(function (rm) {
      html += '<div class="ils-row"><div class="ils-grow"><div>⏰ ' + esc(rm.text || '') + '</div>' +
        '<div class="ils-sub">' + fmtDateTime(rm.due_at) + '</div></div></div>';
    });
    el.innerHTML = html;
  }

  /* ---------------- Memory ---------------- */
  function renderMemory() {
    var el = slot('memory');
    var p = obProfile();
    var bits = [];
    if (p.name) bits.push('Your name: ' + p.name);
    if (p.goals && p.goals.length) bits.push('Learning goals: ' + p.goals.join(', '));
    bits.push('Tutor: ' + tutorName());
    var histLen = 0, notesLen = 0;
    try {
      var h = JSON.parse(localStorage.getItem('noah-ai-history-v1') || '[]');
      if (Array.isArray(h)) histLen = h.length;
      var n = JSON.parse(localStorage.getItem('il-notes-v1') || '[]');
      if (Array.isArray(n)) notesLen = n.length; else if (n && typeof n === 'object') notesLen = Object.keys(n).length;
    } catch (e) {}
    var html = '<p class="ils-note">What ' + esc(tutorName()) + ' remembers lives in your profile and your ' +
      'conversations with it — synced to your account, never shared with anyone else.</p>' +
      '<div class="ils-row"><div class="ils-grow"><div>' + esc(bits.join(' · ') || 'Nothing saved yet') + '</div>' +
      '<div class="ils-sub">' + histLen + ' saved conversation messages on this device · ' + notesLen + ' notes</div></div></div>' +
      '<p><button type="button" class="ils-btn ghost" id="ilsEraseMem">Erase conversation memory</button></p>' +
      '<div class="ils-del-confirm" id="ilsEraseConfirm"><p class="ils-note">This clears your chat history with ' +
      esc(tutorName()) + ' on this device and your account. Notes, goals, and certificates are not touched.</p>' +
      '<p><button type="button" class="ils-btn danger" id="ilsEraseGo">Yes, erase conversation memory</button></p></div>' +
      '<p class="ils-status" id="ilsMemStatus" role="status"></p>';
    el.innerHTML = html;
    var tgl = $('ilsEraseMem');
    if (tgl) tgl.addEventListener('click', function () {
      $('ilsEraseConfirm').classList.toggle('on');
    });
    var go = $('ilsEraseGo');
    if (go) go.addEventListener('click', function () {
      var st = $('ilsMemStatus');
      ['noah-ai-history-v1', 'noah-session-v2'].forEach(function (k) {
        try { localStorage.removeItem(k); } catch (e) {}
      });
      var done = function () {
        st.textContent = '✓ Conversation memory erased. Reload the page for a fresh thread.';
        st.className = 'ils-status ok';
      };
      if (state.me) {
        api('/api/user/sync', { method: 'PUT', body: { store: 'noah', data: {}, updated_at: new Date().toISOString() } })
          .then(done).catch(done);
      } else done();
    });
  }

  /* ---------------- Files & documents ---------------- */
  function loadFiles() {
    var el = slot('files');
    var html = '<p class="ils-note">Your documents across Interstitium Labs, in one place.</p>' +
      '<div class="ils-row"><div class="ils-grow"><div>📝 Notes &amp; mind maps</div>' +
      '<div class="ils-sub">Your notes vault, synced to your account</div></div>' +
      '<a class="ils-btn ghost" href="/my-notes/">Open</a></div>' +
      '<div class="ils-row"><div class="ils-grow"><div>📚 PDF library</div>' +
      '<div class="ils-sub">Reference books and study PDFs</div></div>' +
      '<a class="ils-btn ghost" href="/pdf-library/">Open</a></div>';
    if (!state.me) {
      el.innerHTML = html + '<p class="ils-note">Sign in to see your certificates here.</p>';
      return;
    }
    api('/api/certificates').then(function (r) {
      var certs = (r.j && (r.j.certificates || r.j.certs)) || [];
      if (certs.length) {
        html += '<p class="ils-note" style="margin-top:.6rem">Your certificates:</p>' + certs.map(function (c) {
          var id = c.id || c.cert_id || '';
          return '<div class="ils-row"><div class="ils-grow"><div>🏅 ' + esc(c.course_title || c.title || c.course || 'Certificate') + '</div>' +
            '<div class="ils-sub">Issued ' + fmtDate(c.issued_at || c.created_at) + '</div></div>' +
            (id ? '<a class="ils-btn ghost" href="/api/certificates/verify?id=' + encodeURIComponent(id) + '" target="_blank" rel="noopener">Verify</a>' : '') +
            '</div>';
        }).join('');
      } else {
        html += '<p class="ils-note" style="margin-top:.6rem">No certificates yet — finish a course and your verifiable certificate lands here.</p>';
      }
      el.innerHTML = html;
    }).catch(function () { el.innerHTML = html; });
  }

  /* ---------------- Payments ---------------- */
  function renderPayments() {
    var el = slot('payments');
    el.innerHTML =
      '<p class="ils-note">Courses are $249 each or $999 for the full bundle (IL-27/28/29 are always free). ' +
      'Card and wallet payments run through Stripe / PayPal at checkout — your card details are never stored here.</p>' +
      '<p><a class="ils-btn" href="/enroll/">See plans &amp; enroll</a> ' +
      (state.me ? '<a class="ils-btn ghost" href="/api/account/export">My orders (in data export)</a>' : '') + '</p>' +
      '<p class="ils-note">Crypto checkout confirms manually after you submit a transaction hash — ' +
      'an order only counts as paid once it is verified.</p>';
  }

  /* ---------------- Voice & tutor ---------------- */
  function renderVoice() {
    var el = slot('voice');
    var on = false;
    try { on = localStorage.getItem('noah-voice-out') === '1'; } catch (e) {}
    el.innerHTML =
      '<label class="ils-switch"><input type="checkbox" id="ilsVoiceOut" ' + (on ? 'checked' : '') + '>' +
      '<span>Voice replies — ' + esc(tutorName()) + ' reads answers aloud</span></label>' +
      '<p class="ils-note">Dictation is always available from the 🎙 mic in the composer. ' +
      'For a full spoken conversation, run a verbal mock interview:</p>' +
      '<p><button type="button" class="ils-btn" id="ilsInterview">🎙 Start a verbal mock interview</button></p>';
    var cb = $('ilsVoiceOut');
    if (cb) cb.addEventListener('change', function () {
      try { localStorage.setItem('noah-voice-out', cb.checked ? '1' : '0'); } catch (e) {}
      var vb = $('voiceOutBtn');
      if (vb) {
        var cur = false;
        try { cur = localStorage.getItem('noah-voice-out') === '1'; } catch (e) {}
        /* Keep the header toggle in sync by re-reading state on next open;
           simplest robust path: click it if its aria state disagrees. */
        var pressed = vb.getAttribute('aria-pressed');
        if (pressed !== null && (pressed === 'true') !== cur) vb.click();
      }
    });
    var ib = $('ilsInterview');
    if (ib) ib.addEventListener('click', function () {
      closePanel();
      var mb = $('miBtn');
      if (mb) mb.click();
    });
  }

  /* ---------------- Permissions ---------------- */
  function renderPerms() {
    var el = slot('perms');
    var p = obProfile();
    var policy = p.connPolicy || {};
    var services = [['gmail', 'Gmail — send email'], ['gcal', 'Google Calendar — schedule events'], ['github', 'GitHub — trigger workflows']];
    el.innerHTML =
      '<p class="ils-note">The rule, everywhere: ' + esc(tutorName()) + ' drafts and prepares; ' +
      '<b>you</b> approve anything irreversible — sending, scheduling, buying, deleting. ' +
      'Sensitive account actions additionally need a fresh step-up approval (10 minutes, single use).</p>' +
      services.map(function (s) {
        var v = policy[s[0]] || 'ask';
        return '<div class="ils-row"><div class="ils-grow"><div>' + esc(s[1]) + '</div></div>' +
          '<select data-ils-policy="' + s[0] + '" class="ils-pill" style="background:none;color:inherit">' +
          '<option value="ask"' + (v === 'ask' ? ' selected' : '') + '>Always ask me</option>' +
          '<option value="draft"' + (v === 'draft' ? ' selected' : '') + '>Draft only, never send</option>' +
          '</select></div>';
      }).join('') +
      '<p class="ils-note">These preferences are saved to your profile and followed by ' + esc(tutorName()) +
      ' — the server still enforces approval + step-up regardless.</p>';
    el.querySelectorAll('[data-ils-policy]').forEach(function (sel) {
      sel.addEventListener('change', function () {
        var pp = obProfile();
        pp.connPolicy = pp.connPolicy || {};
        pp.connPolicy[sel.getAttribute('data-ils-policy')] = sel.value;
        saveObProfile(pp);
      });
    });
  }

  /* ---------------- Devices ---------------- */
  function renderDevices() {
    var el = slot('devices');
    var ua = navigator.userAgent || '';
    var plat = (navigator.userAgentData && navigator.userAgentData.platform) || navigator.platform || 'This device';
    el.innerHTML =
      '<div class="ils-row"><div class="ils-grow"><div>💻 This browser</div>' +
      '<div class="ils-sub">' + esc(plat) + ' · ' + esc(window.screen.width + '×' + window.screen.height) + '</div></div>' +
      '<span class="ils-pill on">Current</span></div>' +
      '<p class="ils-note">' + esc(ua.slice(0, 140)) + '</p>' +
      '<p class="ils-note">Interstitium Labs is a web platform — there are no paired devices to manage. ' +
      'Sign in on any browser and your notes, goals, and settings follow your account automatically. ' +
      'Sessions last up to 7 days; signing out here ends this browser\'s session.</p>' +
      (state.me ? '<p><button type="button" class="ils-btn ghost" id="ilsSignOut2">Sign out of this browser</button></p>' : '');
    var so = $('ilsSignOut2');
    if (so) so.addEventListener('click', function () {
      api('/api/auth/signout', { method: 'POST' }).then(function () {
        state.me = null; loadAll();
      });
    });
  }

  /* ---------------- Activity ---------------- */
  var EVENT_LABELS = {
    login_success: '🔑 Signed in', login_failure: '⚠ Failed sign-in attempt',
    magic_request: '✉ Magic link requested', signout: '👋 Signed out',
    stepup_issued: '🛡 Step-up approval issued', sensitive_action: '✅ Approved sensitive action',
    vault_save: '🔐 Login saved to Secure Store', vault_delete: '🗑 Login deleted from Secure Store',
    vault_list: '🔐 Secure Store viewed', vault_use: '🔐 Saved login used by an agent',
    admin_confirm_failed: '⚠ Failed admin confirmation'
  };
  function loadActivity() {
    var el = slot('activity');
    if (!state.me) { el.innerHTML = signInNote('your activity history'); return; }
    api('/api/account/activity').then(function (r) {
      if (r.status === 404 || !r.j || !r.j.ok) {
        el.innerHTML = '<p class="ils-note">Your sign-in and security history arrives with the next platform update. ' +
          'Every event is already recorded server-side.</p>';
        return;
      }
      var events = r.j.events || [];
      if (!events.length) {
        el.innerHTML = '<p class="ils-note">No recorded activity yet.</p>';
        return;
      }
      el.innerHTML = events.map(function (ev) {
        return '<div class="ils-row"><div class="ils-grow"><div>' +
          esc(EVENT_LABELS[ev.event] || ev.event || 'Event') + '</div>' +
          '<div class="ils-sub">' + fmtDateTime(ev.ts) + (ev.country ? ' · ' + esc(ev.country) : '') +
          (ev.extra && ev.extra.service ? ' · ' + esc(ev.extra.service) : '') + '</div></div></div>';
      }).join('');
    }).catch(function () {
      el.innerHTML = '<p class="ils-note">Activity could not be loaded just now.</p>';
    });
  }

  /* ---------------- Privacy & data ---------------- */
  function renderPrivacy() {
    var el = slot('privacy');
    el.innerHTML =
      '<p class="ils-note">Your data belongs to you: download everything we hold, erase ' +
      esc(tutorName()) + '\'s conversation memory above, or delete the whole account.</p>' +
      '<p>' + (state.me
        ? '<a class="ils-btn" href="/api/account/export">⬇ Download my data</a> '
        : '') +
      '<a class="ils-btn ghost" href="/privacy/">Privacy policy</a> ' +
      '<a class="ils-btn ghost" href="/account/">Account &amp; deletion</a></p>' +
      '<p class="ils-note">Account deletion is confirm-gated on the account page and erases your ' +
      'account record, progress, synced stores, goals, certificates, job data, reminders, and Secure Store logins. ' +
      'Payment orders are kept as financial records with your email pseudonymized, as disclosed on the privacy page.</p>';
  }

  /* ---------------- Deep link ---------------- */
  function maybeOpenFromHash() {
    var h = location.hash || '';
    if (h.indexOf('#settings') === 0) {
      var parts = h.split('/');
      openPanel(parts[1] || null);
    }
  }
  window.addEventListener('hashchange', maybeOpenFromHash);
  maybeOpenFromHash();

  window.ILSettings = {
    open: openPanel,
    close: closePanel,
    refresh: function () { state.me = undefined; state.loaded = {}; loadAll(); }
  };
})();
