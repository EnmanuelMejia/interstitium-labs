/**
 * ILCredBroker — client for the Secure Credential Broker.
 * (Interstitium original. No dependencies, CSP-safe.)
 *
 * The client half of the pattern the owner proved with Proton Pass:
 * logins live in a secure store; Noah / Genesis (and every agent)
 * see NAMES AND STATES ONLY. This module never touches a secret
 * value — capture happens on /account/credentials/, a protected page
 * whose form posts straight to the session-gated broker API.
 *
 * Surfaces wired by this one canonical module:
 *   - Noah/Genesis Settings: a "Saved logins — secure store" section
 *     appended to the settings panel (the centerpiece of Settings).
 *   - Noah/Genesis chat: the model's [secure-login:<service>] marker
 *     becomes a secure sign-in card — never a password field in chat.
 *   - Jobs suite: portal-login status panel next to 1-click autofill.
 *
 * Backend contract (docs/_worker.js credential broker):
 *   GET    /api/credentials                  -> { ok, configured, services:[{id,label,kind,store_hint,state,updated_at}] }
 *   POST   /api/credentials/capture          { service, username, secret } -> { ok, service, state }
 *   POST   /api/credentials/mark-external    { service } -> { ok, service, state:'external' }
 *   DELETE /api/credentials/:service         -> { ok, service, state:'not_saved' }
 *   401 = signed out · 503 cred_store_not_configured = owner has not
 *   set CRED_ENC_KEY yet (capture fails closed; states still read).
 */
(function (g) {
  'use strict';

  /* Canonical service directory — MIRRORED in _worker.js (CRED_DIRECTORY). */
  var DIRECTORY = [
    { id: 'gmail',    label: 'Gmail',           kind: 'oauth' },
    { id: 'gcal',     label: 'Google Calendar', kind: 'oauth' },
    { id: 'github',   label: 'GitHub',          kind: 'oauth' },
    /* 2026-10-11 (parity-plus): OAuth token services (broker envelopes). */
    { id: 'oauth-google',    label: 'Google (OAuth tokens)',    kind: 'oauth' },
    { id: 'oauth-github',    label: 'GitHub (OAuth tokens)',    kind: 'oauth' },
    { id: 'oauth-microsoft', label: 'Microsoft (OAuth tokens)', kind: 'oauth' },
    { id: 'oauth-spotify',   label: 'Spotify (OAuth tokens)',    kind: 'oauth' },
    { id: 'oauth-meta',      label: 'Meta (OAuth tokens)',      kind: 'oauth' },
    { id: 'oauth-apple',     label: 'Apple (OAuth tokens)',     kind: 'oauth' },
    { id: 'indeed',        label: 'Indeed',          kind: 'password', store_hint: 'proton-pass' },
    { id: 'linkedin',      label: 'LinkedIn',        kind: 'password', store_hint: 'proton-pass' },
    { id: 'ziprecruiter',  label: 'ZipRecruiter',    kind: 'password', store_hint: 'proton-pass' },
    { id: 'usajobs',       label: 'USAJobs',         kind: 'password', store_hint: 'proton-pass' },
    { id: 'greenhouse',    label: 'Greenhouse (candidate portal)', kind: 'password', store_hint: 'proton-pass' },
    { id: 'lever',         label: 'Lever (candidate portal)',      kind: 'password', store_hint: 'proton-pass' },
    { id: 'ashby',         label: 'Ashby (candidate portal)',      kind: 'password', store_hint: 'proton-pass' },
    { id: 'workday',       label: 'Workday',         kind: 'password', store_hint: 'proton-pass' },
    { id: 'icims',         label: 'iCIMS',           kind: 'password', store_hint: 'proton-pass' },
    { id: 'taleo',         label: 'Taleo',           kind: 'password', store_hint: 'proton-pass' },
    { id: 'smartrecruiters', label: 'SmartRecruiters', kind: 'password', store_hint: 'proton-pass' }
  ];

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;')
      .replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function entry(id) {
    for (var i = 0; i < DIRECTORY.length; i++) if (DIRECTORY[i].id === id) return DIRECTORY[i];
    return null;
  }
  function captureUrl(service) {
    return '/account/credentials/?service=' + encodeURIComponent(service);
  }

  var cache = null; /* {signedIn, live, configured, services:[...]} */

  function status() {
    if (cache) return Promise.resolve(cache);
    return fetch('/api/credentials', { credentials: 'same-origin' })
      .then(function (r) {
        if (r.status === 401) {
          cache = { signedIn: false, live: true, configured: false, services: [] };
          return cache;
        }
        if (!r.ok) throw new Error('broker ' + r.status);
        return r.json();
      })
      .then(function (d) {
        if (cache) return cache;
        cache = { signedIn: true, live: true, configured: !!d.configured,
                  services: d.services || [] };
        return cache;
      })
      .catch(function () {
        /* Broker route not live yet (staged) — say so, never fake states. */
        cache = { signedIn: null, live: false, configured: false, services: [] };
        return cache;
      });
  }
  function invalidate() { cache = null; }

  function stateOf(st, id) {
    for (var i = 0; i < st.services.length; i++) {
      if (st.services[i].id === id) return st.services[i];
    }
    return null;
  }
  /* OAuth connection state lives in the onboarding profile (sync prefs). */
  function oauthConnected(id) {
    try {
      var p = g.NoahOnboarding && g.NoahOnboarding.getProfile && g.NoahOnboarding.getProfile();
      return !!(p && p.connections && p.connections[id]);
    } catch (e) { return false; }
  }
  function displayState(st, d) {
    var rec = stateOf(st, d.id);
    if (rec && rec.state === 'saved') return { key: 'saved', label: 'Saved — secure store' };
    if (d.kind === 'oauth' && oauthConnected(d.id)) return { key: 'connected', label: 'Connected' };
    if (rec && rec.state === 'external') return { key: 'external', label: 'In Proton Pass' };
    return { key: 'not_saved', label: 'Not saved' };
  }

  function markExternal(service) {
    return fetch('/api/credentials/mark-external', {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ service: service })
    }).then(function (r) { return r.json(); })
      .then(function (d) { invalidate(); return d; });
  }
  function revoke(service) {
    return fetch('/api/credentials/' + encodeURIComponent(service), {
      method: 'DELETE', credentials: 'same-origin'
    }).then(function (r) { return r.json(); })
      .then(function (d) { invalidate(); return d; });
  }

  function css() {
    if (document.getElementById('ilcred-css')) return;
    var s = document.createElement('style'); s.id = 'ilcred-css';
    s.textContent = [
      '.ilcred-sec{margin-top:14px;border-top:1px solid rgba(201,162,39,.18);padding-top:12px;}',
      '.ilcred-sec h4{margin:0 0 4px;font-size:13px;color:#e8e2d0;letter-spacing:.02em;}',
      '.ilcred-sec .ilcred-sub{margin:0 0 10px;font-size:12px;color:#8b93a5;line-height:1.5;}',
      '.ilcred-row{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05);flex-wrap:wrap;}',
      '.ilcred-row .nm{flex:1;min-width:130px;font-size:13px;color:#dbe4ee;}',
      '.ilcred-chip{font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid rgba(255,255,255,.18);color:#8b93a5;white-space:nowrap;}',
      '.ilcred-chip.saved{color:#34d399;border-color:rgba(52,211,153,.5);}',
      '.ilcred-chip.connected{color:#34d399;border-color:rgba(52,211,153,.5);}',
      '.ilcred-chip.external{color:#7dd3fc;border-color:rgba(125,211,252,.5);}',
      '.ilcred-row a,.ilcred-row button{font-size:12px;color:#5EEAD4;background:none;border:none;cursor:pointer;padding:2px 4px;text-decoration:none;}',
      '.ilcred-row button.warn{color:#ff8fa3;}',
      '.ilcred-card{border:1px solid rgba(201,162,39,.4);border-radius:10px;margin:8px 0;background:rgba(10,12,8,.92);overflow:hidden;}',
      '.ilcred-card .hd{padding:8px 12px;background:rgba(201,162,39,.1);font-size:12px;color:#e8c96a;}',
      '.ilcred-card .bd{padding:10px 12px;font-size:13px;color:#dbe4ee;line-height:1.55;}',
      '.ilcred-card .row{display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;}',
      '.ilcred-card a.btn,.ilcred-card button.btn{display:inline-block;background:rgba(201,162,39,.18);border:1px solid #c9a227;color:#fff;border-radius:6px;padding:6px 14px;cursor:pointer;font-size:12px;text-decoration:none;}',
      '.ilcred-card button.btn.ghost{background:transparent;border-color:rgba(255,255,255,.25);color:#cfe3ee;}'
    ].join('');
    document.head.appendChild(s);
  }

  /* ---------- Settings section (centerpiece) ---------- */
  function renderSettingsSection(wrap) {
    if (!wrap || wrap.querySelector('[data-ilcred-sec]')) return;
    css();
    var sec = document.createElement('div');
    sec.className = 'ilcred-sec'; sec.setAttribute('data-ilcred-sec', '1');
    sec.innerHTML = '<h4>🔐 Saved logins — secure store</h4>' +
      '<p class="ilcred-sub">Noah and Genesis use saved logins through the secure store. ' +
      'They see names and status only — never your passwords, and you never paste one in chat.</p>' +
      '<div class="ilcred-body"><p class="ilcred-sub">Checking the secure store…</p></div>';
    wrap.appendChild(sec);
    var body = sec.querySelector('.ilcred-body');
    if (!body) return;
    status().then(function (st) {
      if (!st.live) {
        body.innerHTML = '<p class="ilcred-sub">The secure store is still activating on this site. ' +
          'Until it is live, keep logins in Proton Pass — Noah will offer that path.</p>';
        return;
      }
      if (!st.signedIn) {
        body.innerHTML = '<p class="ilcred-sub">Sign in to manage saved logins. ' +
          '<a href="/account/" style="color:#5EEAD4">Sign in</a></p>';
        return;
      }
      var html = '';
      DIRECTORY.forEach(function (d) {
        var ds = displayState(st, d);
        var isOauthSvc = d.id.indexOf('oauth-') === 0;
        html += '<div class="ilcred-row" data-svc="' + d.id + '">' +
          '<span class="nm">' + esc(d.label) + '</span>' +
          '<span class="ilcred-chip ' + ds.key + '">' + esc(ds.label) + '</span>' +
          (ds.key === 'saved' || ds.key === 'external'
            ? '<button type="button" data-act="revoke">Remove</button>'
            : (isOauthSvc
              ? '<a href="/noah/#settings/connectors">Connect</a>'
              : '<a href="' + captureUrl(d.id) + '" target="_blank" rel="noopener">Save securely</a>' +
                (d.store_hint === 'proton-pass'
                  ? '<button type="button" data-act="external">It\'s in my Proton Pass</button>' : ''))) +
          '</div>';
      });
      body.innerHTML = html;
      body.querySelectorAll('button[data-act]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var svc = btn.parentNode.getAttribute('data-svc');
          var act = btn.getAttribute('data-act');
          btn.disabled = true; btn.textContent = 'Working…';
          var p = act === 'revoke' ? revoke(svc) : markExternal(svc);
          p.then(function () {
            var fresh = sec.cloneNode(false);
            sec.parentNode.replaceChild(fresh, sec);
            fresh.className = 'ilcred-sec'; fresh.setAttribute('data-ilcred-sec', '1');
            renderSettingsSection(fresh.parentNode);
          }).catch(function () { btn.disabled = false; btn.textContent = 'Try again'; });
        });
      });
    });
  }

  /* ---------- chat secure-entry card ---------- */
  function cardEl(service) {
    var d = entry(service) || { id: service, label: service, kind: 'password' };
    css();
    var box = document.createElement('div');
    box.className = 'ilcred-card';
    box.innerHTML =
      '<div class="hd">🔐 Secure sign-in — ' + esc(d.label) + '</div>' +
      '<div class="bd">This login is not saved yet. Enter it once on the protected page — ' +
      'it is stored encrypted, and Noah / Genesis will use it through the secure store. ' +
      'Never paste a password in chat.' +
      '<div class="row">' +
      '<a class="btn" href="' + captureUrl(d.id) + '" target="_blank" rel="noopener">Save login securely</a>' +
      (d.store_hint === 'proton-pass'
        ? '<button type="button" class="btn ghost" data-act="external">It\'s in my Proton Pass</button>' : '') +
      '</div></div>';
    var btn = box.querySelector('button[data-act="external"]');
    if (btn) btn.addEventListener('click', function () {
      btn.disabled = true; btn.textContent = 'Marking…';
      markExternal(d.id).then(function (res) {
        box.querySelector('.bd').innerHTML = res && res.ok
          ? 'Marked — ' + esc(d.label) + ' lives in your Proton Pass. When a task needs it, ' +
            'you will be pointed to the secure vault, the same as always.'
          : 'Could not mark it just now (are you signed in?). Your Proton Pass still has the login.';
      }).catch(function () { btn.disabled = false; btn.textContent = 'Try again'; });
    });
    return box;
  }

  var MARKER = /\[secure-login:([a-z0-9][a-z0-9-]{1,60})\]/;
  function convertMarkers(root) {
    if (!root) return;
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!MARKER.test(n.nodeValue || '')) return NodeFilter.FILTER_REJECT;
        if (n.parentNode && (n.parentNode.closest('.ilcred-card') || n.parentNode.closest('[data-ilcred-sec]'))) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (n) {
      var m = MARKER.exec(n.nodeValue);
      if (!m) return;
      var host = n.parentNode;
      n.nodeValue = n.nodeValue.replace(MARKER, '').trim();
      var card = cardEl(m[1]);
      if (host && host.parentNode) host.parentNode.insertBefore(card, host.nextSibling);
      else if (host) host.appendChild(card);
    });
  }

  /* ---------- Jobs panel: portal logins beside autofill ---------- */
  function renderJobsPanel(el) {
    if (!el) return;
    css();
    el.innerHTML = '<h3>Portal logins — secure store</h3>' +
      '<p class="jl-sub" style="margin:0 0 8px">When an application needs a portal sign-in, ' +
      'the agent uses your saved login through the secure store — it never asks you to paste a password.</p>' +
      '<div class="ilcred-body"><p class="jl-sub">Checking…</p></div>';
    var body = el.querySelector('.ilcred-body');
    status().then(function (st) {
      if (!st.live) { body.innerHTML = '<p class="jl-sub">Secure store activating — Proton Pass remains the store of record meanwhile.</p>'; return; }
      if (!st.signedIn) { body.innerHTML = '<p class="jl-sub"><a href="/account/">Sign in</a> to see which portal logins are saved.</p>'; return; }
      var html = '';
      DIRECTORY.filter(function (d) { return d.kind === 'password'; }).forEach(function (d) {
        var ds = displayState(st, d);
        html += '<div class="ilcred-row"><span class="nm">' + esc(d.label) + '</span>' +
          '<span class="ilcred-chip ' + ds.key + '">' + esc(ds.label) + '</span>' +
          (ds.key === 'not_saved'
            ? '<a href="' + captureUrl(d.id) + '" target="_blank" rel="noopener">Save securely</a>' : '') +
          '</div>';
      });
      body.innerHTML = html;
    });
  }

  /* ---------- boot: settings + chat augmentation ---------- */
  var observing = false;
  function boot() {
    if (observing || !document.body) return;
    observing = true;
    var scan = function () {
      document.querySelectorAll('.noah-settings-wrap').forEach(renderSettingsSection);
      var msgs = document.querySelectorAll('#noah-msgs, .noah-msgs, .noah-messages, #il-jobs-portal-logins');
      msgs.forEach(function (m) { if (m.id !== 'il-jobs-portal-logins') convertMarkers(m); });
    };
    scan();
    var pending = false;
    var obs = new MutationObserver(function () {
      if (pending) return;
      pending = true;
      setTimeout(function () { pending = false; scan(); }, 250);
    });
    obs.observe(document.body, { childList: true, subtree: true });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else { boot(); }

  g.ILCredBroker = {
    version: 1,
    DIRECTORY: DIRECTORY,
    status: status,
    invalidate: invalidate,
    captureUrl: captureUrl,
    markExternal: markExternal,
    revoke: revoke,
    cardEl: cardEl,
    renderSettingsSection: renderSettingsSection,
    renderJobsPanel: renderJobsPanel,
    convertMarkers: convertMarkers
  };
})(typeof window !== 'undefined' ? window : this);
