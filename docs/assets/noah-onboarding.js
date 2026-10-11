/**
 * NoahOnboarding — first-run experience + API/service setup for Noah AI.
 * (Interstitium original. No dependencies, CSP-safe.)
 *
 * Features:
 *   - First-visit detection via localStorage 'noah-onboarded'
 *   - Welcome flow guided by the 3D Operator avatar
 *   - Service connection onboarding (Gmail, Calendar, GitHub)
 *   - Preference setup (learning goals, interests, notifications)
 *   - Progressive disclosure (feature unlock tracking)
 *   - Returning user recognition (welcome-back with context)
 *   - API key management UI (user's own keys for services)
 *
 * All within the unified shell — no external pages.
 * Cinematic dark theme. "Less is more."
 */
(function (g) {
  'use strict';

  var ONBOARDED_KEY = 'noah-onboarded';
  var PROFILE_KEY = 'noah-user-profile';
  var FEATURES_KEY = 'noah-unlocked-features';

  /* Progressive disclosure: features unlock as the user engages */
  var FEATURE_LADDER = [
    { id: 'chat',        label: 'Chat with Noah',       trigger: 'onboard' },
    { id: 'viz',         label: 'Visual explanations', trigger: 'asks:3' },
    { id: 'docs',        label: 'Document rendering',  trigger: 'asks:5' },
    { id: 'connectors',  label: 'Connected services',  trigger: 'manual' },
    { id: 'voice',       label: 'Voice mode',          trigger: 'asks:10' },
    { id: 'api',         label: 'API access',          trigger: 'manual' }
  ];

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;')
      .replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function isOnboarded() {
    try { return localStorage.getItem(ONBOARDED_KEY) === '1'; } catch (e) { return true; }
  }

  function getProfile() {
    try {
      var p = JSON.parse(localStorage.getItem(PROFILE_KEY) || '{}');
      return p && typeof p === 'object' ? p : {};
    } catch (e) { return {}; }
  }

  function saveProfile(p) {
    try { localStorage.setItem(PROFILE_KEY, JSON.stringify(p)); } catch (e) {}
  }

  function getUnlocked() {
    try { return JSON.parse(localStorage.getItem(FEATURES_KEY) || '["chat"]'); }
    catch (e) { return ['chat']; }
  }

  function unlock(id) {
    try {
      var u = getUnlocked();
      if (u.indexOf(id) === -1) { u.push(id); localStorage.setItem(FEATURES_KEY, JSON.stringify(u)); }
    } catch (e) {}
  }

  /* ---- Welcome overlay ---- */
  var overlay = null;
  var step = 0;

  var STEPS = [
    {
      title: 'Meet Noah',
      body: 'I\'m Noah — your AI tutor and assistant, built into every page of Interstitium Labs. Ask me anything, and I\'ll explain it with living visualizations.',
      cta: 'Next'
    },
    {
      title: 'What are you here to learn?',
      body: 'goals',
      cta: 'Next'
    },
    {
      title: 'Connect your services',
      body: 'services',
      cta: 'Next'
    },
    {
      title: 'You\'re ready',
      body: 'Press <kbd>⌘K</kbd> anywhere to search. Click my orb (bottom-right) to chat. I\'ll guide you from here.',
      cta: 'Start learning'
    }
  ];

  var GOALS = [
    'IT Infrastructure & Networking',
    'Cybersecurity',
    'AI & Machine Learning',
    'Cloud & DevOps',
    'Programming',
    'Data Science',
    'Career prep / interviews',
    'Just exploring'
  ];

  /* ---- Selected tutor (Noah default / Genesis) ----
     The tutor choice lives in the avatar profile ('il-noah-profile',
     owned by il-noah-avatar.js). The onboarding always shows the
     selected tutor's photo likeness — never an empty slot. */
  function selectedTutor() {
    try {
      if (g.ILNoahAvatar && g.ILNoahAvatar.getProfile) {
        var a = g.ILNoahAvatar.getProfile().avatar;
        if (a === 'genesis' || a === 'noah') return a;
      }
    } catch (e) {}
    try {
      var p = JSON.parse(localStorage.getItem('il-noah-profile') || '{}');
      if (p && p.avatar === 'genesis') return 'genesis';
    } catch (e) {}
    return 'noah';
  }

  function tutorName() { return selectedTutor() === 'genesis' ? 'Genesis' : 'Noah'; }

  function tutorImg() {
    return '/assets/noah/' + selectedTutor() + '-avatar-3d.webp';
  }

  function personalize(text) {
    return selectedTutor() === 'genesis' ? String(text).replace(/Noah/g, 'Genesis') : text;
  }

  /* Mount the live avatar engine over the fallback <img>. The <img> is
     rendered synchronously in renderStep, so the slot is NEVER empty;
     if the engine is still loading (parallel loader chains race), retry
     briefly, then keep the <img>. Never force the procedural 'operator'
     avatar — at onboarding sizes it renders as a near-black scene and
     reads as an empty circle. */
  function mountAvatarWithFallback(slot) {
    if (!slot) return;
    var tutor = selectedTutor();
    var tries = 0;
    (function attempt() {
      if (!document.body || !document.body.contains(slot)) return; // step changed / done
      if (g.ILNoahAvatar && g.ILNoahAvatar.mount) {
        try {
          var inst = g.ILNoahAvatar.mount(slot, { avatar: tutor });
          if (inst && slot.querySelector('[data-noah-avatar]')) {
            var fb = slot.querySelector('.noah-ob-avatar-img');
            if (fb && fb.parentNode) fb.parentNode.removeChild(fb);
            if (inst.setStatus) inst.setStatus('speaking');
            return;
          }
        } catch (e) {}
      }
      if (++tries < 10) setTimeout(attempt, 300);
    })();
  }

  /* ---- Services (connectors) ----
     Static fallback so the step ALWAYS names the services, even if the
     connector framework has not loaded yet. Status is reported honestly
     from local connection state — never faked. */
  var FALLBACK_SERVICES = [
    { id: 'gmail', label: 'Gmail', icon: '📧' },
    { id: 'gcal', label: 'Google Calendar', icon: '📅' },
    { id: 'github', label: 'GitHub', icon: '🐙' }
  ];

  function serviceList() {
    try {
      if (g.NoahConnectors && g.NoahConnectors.list) {
        var list = g.NoahConnectors.list();
        if (list && list.length) return list;
      }
    } catch (e) {}
    return FALLBACK_SERVICES;
  }

  function renderStep() {
    var s = STEPS[step];
    var bodyHtml = '';
    if (s.body === 'goals') {
      bodyHtml = '<div class="noah-ob-goals">' + GOALS.map(function (goal, i) {
        return '<button class="noah-ob-goal" data-goal="' + esc(goal) + '">' + esc(goal) + '</button>';
      }).join('') + '</div><p class="noah-ob-hint">Pick one or more — I\'ll tailor my suggestions.</p>';
    } else if (s.body === 'services') {
      bodyHtml = renderServices();
    } else {
      bodyHtml = '<p>' + personalize(s.body) + '</p>';
    }

    overlay.innerHTML =
      '<div class="noah-ob-card">' +
        '<div class="noah-ob-avatar" data-noah-3d-slot>' +
          '<img class="noah-ob-avatar-img" src="' + tutorImg() + '" alt="' + esc(tutorName()) + '" width="120" height="120" decoding="async">' +
        '</div>' +
        '<div class="noah-ob-progress">' + (step + 1) + ' / ' + STEPS.length + '</div>' +
        '<h2>' + esc(personalize(s.title)) + '</h2>' +
        '<div class="noah-ob-body">' + bodyHtml + '</div>' +
        '<div class="noah-ob-actions">' +
          (step > 0 ? '<button class="noah-ob-back">Back</button>' : '') +
          '<button class="noah-ob-next">' + esc(s.cta) + '</button>' +
          '<button class="noah-ob-skip">Skip</button>' +
        '</div>' +
      '</div>';

    // Enhance the fallback <img> with the live avatar engine (photo tutor).
    mountAvatarWithFallback(overlay.querySelector('[data-noah-3d-slot]'));

    bindStep();
  }

  function renderServices() {
    var connectors = serviceList();
    var keys = getApiKeys();
    var p = getProfile();
    return '<div class="noah-ob-services">' + connectors.map(function (c) {
      var connected = !!(keys[c.id] || (p.connections && p.connections[c.id]));
      return '<div class="noah-ob-service" data-conn="' + esc(c.id) + '">' +
        '<span class="noah-ob-service-icon">' + esc(c.icon || '🔌') + '</span>' +
        '<span class="noah-ob-service-label">' + esc(c.label) + '</span>' +
        '<span class="noah-ob-service-status ' + (connected ? 'on' : 'off') + '">' +
          (connected ? 'Connected' : 'Not connected') + '</span>' +
        '<button class="noah-ob-connect">Connect</button>' +
      '</div>';
    }).join('') + '</div><p class="noah-ob-hint">Connect services to let ' + esc(tutorName()) + ' act on your behalf. You can do this anytime from ' + esc(tutorName()) + '\'s settings.</p>';
  }

  function bindStep() {
    var next = overlay.querySelector('.noah-ob-next');
    var back = overlay.querySelector('.noah-ob-back');
    var skip = overlay.querySelector('.noah-ob-skip');

    if (next) next.addEventListener('click', function () {
      collectStep();
      if (step < STEPS.length - 1) { step++; renderStep(); }
      else finish();
    });
    if (back) back.addEventListener('click', function () { step--; renderStep(); });
    if (skip) skip.addEventListener('click', finish);

    // Goal selection (toggle)
    var goals = overlay.querySelectorAll('.noah-ob-goal');
    goals.forEach(function (btn) {
      if (getProfile().goals && getProfile().goals.indexOf(btn.dataset.goal) !== -1) {
        btn.classList.add('selected');
      }
      btn.addEventListener('click', function () { btn.classList.toggle('selected'); });
    });

    // Service connect buttons
    var connects = overlay.querySelectorAll('.noah-ob-connect');
    connects.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var svc = btn.closest('.noah-ob-service');
        var id = svc ? svc.dataset.conn : '';
        startOAuth(id, btn);
      });
    });
  }

  function collectStep() {
    var s = STEPS[step];
    if (s.body === 'goals') {
      var selected = [];
      overlay.querySelectorAll('.noah-ob-goal.selected').forEach(function (b) {
        selected.push(b.dataset.goal);
      });
      var p = getProfile();
      p.goals = selected;
      saveProfile(p);
    }
  }

  function startOAuth(connectorId, btn) {
    // OAuth placeholder: in production, redirects to the service's OAuth flow
    // via /api/noah/connectors/:id?action=auth_url, then handles the callback.
    // For now, surface guidance.
    try {
      if (g.NoahConnectors && g.NoahConnectors.getSetupUrl) {
        var url = g.NoahConnectors.getSetupUrl(connectorId);
        if (url) { window.open(url, '_blank', 'noopener'); return; }
      }
    } catch (e) {}
    if (btn) { btn.textContent = 'Coming soon'; btn.disabled = true; }
  }

  function finish() {
    try { localStorage.setItem(ONBOARDED_KEY, '1'); } catch (e) {}
    unlock('chat');
    if (overlay && overlay.parentNode) overlay.parentNode.removeChild(overlay);
    overlay = null;
    // Notify Noah widget that onboarding completed
    try { g.dispatchEvent(new CustomEvent('noah-onboarded', { detail: getProfile() })); } catch (e) {}
  }

  function show() {
    if (overlay) return;
    overlay = document.createElement('div');
    overlay.id = 'noah-onboarding';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-label', 'Welcome to Noah AI');
    document.body.appendChild(overlay);
    step = 0;
    renderStep();
  }

  /* ---- Returning user recognition ---- */
  function welcomeBack() {
    var p = getProfile();
    var visits = 0;
    try {
      visits = parseInt(localStorage.getItem('noah-visits') || '0', 10) + 1;
      localStorage.setItem('noah-visits', String(visits));
    } catch (e) {}
    return { profile: p, visits: visits };
  }

  /* ---- API key management ---- */
  function getApiKeys() {
    try { return JSON.parse(localStorage.getItem('noah-api-keys') || '{}'); }
    catch (e) { return {}; }
  }

  function setApiKey(service, key) {
    try {
      var keys = getApiKeys();
      if (key) keys[service] = key; else delete keys[service];
      localStorage.setItem('noah-api-keys', JSON.stringify(keys));
      return true;
    } catch (e) { return false; }
  }

  function renderSettings() {
    var keys = getApiKeys();
    var connectors = serviceList();
    var p = getProfile();

    var html = '<div class="noah-settings">';
    html += '<h3>Connected services</h3>';
    if (connectors.length) {
      html += '<div class="noah-settings-services">' + connectors.map(function (c) {
        var connected = !!(keys[c.id] || (p.connections && p.connections[c.id]));
        return '<div class="noah-settings-row">' +
          '<span>' + esc(c.icon || '🔌') + ' ' + esc(c.label) + '</span>' +
          '<span class="noah-settings-status ' + (connected ? 'on' : 'off') + '">' +
            (connected ? 'Connected' : 'Not connected') + '</span>' +
          '<button data-svc="' + esc(c.id) + '" data-act="' + (connected ? 'disconnect' : 'connect') + '">' +
            (connected ? 'Disconnect' : 'Connect') + '</button>' +
        '</div>';
      }).join('') + '</div>';
    } else {
      html += '<p class="noah-ob-hint">No connectors registered yet.</p>';
    }

    html += '<h3>API keys</h3><p class="noah-ob-hint">Add your own API keys for services. Stored only in this browser.</p>';
    html += '<div class="noah-settings-keys">' +
      '<div class="noah-settings-row"><label>OpenAI <input type="password" data-key="openai" placeholder="sk-…" value="' + esc(keys.openai ? '••••••••' : '') + '"></label></div>' +
      '<div class="noah-settings-row"><label>Anthropic <input type="password" data-key="anthropic" placeholder="sk-ant-…" value="' + esc(keys.anthropic ? '••••••••' : '') + '"></label></div>' +
    '</div>';

    html += '<h3>Preferences</h3>';
    html += '<div class="noah-settings-row"><label>Learning goals <input type="text" data-pref="goals-text" value="' + esc((p.goals || []).join(', ')) + '" placeholder="e.g. networking, Python"></label></div>';

    html += '<div class="noah-settings-actions"><button class="noah-settings-save">Save</button><button class="noah-settings-close">Close</button></div>';
    html += '</div>';
    return html;
  }

  /* ---- Public API ---- */
  g.NoahOnboarding = {
    isOnboarded: isOnboarded,
    show: show,
    finish: finish,
    getProfile: getProfile,
    saveProfile: saveProfile,
    welcomeBack: welcomeBack,
    getUnlocked: getUnlocked,
    unlock: unlock,
    getApiKeys: getApiKeys,
    setApiKey: setApiKey,
    renderSettings: renderSettings,
    FEATURE_LADDER: FEATURE_LADDER,
    VERSION: '1.0.0'
  };

  /* Auto-show on first visit (unless suppressed) */
  function autoInit() {
    try {
      if (document.body && document.body.hasAttribute('data-no-onboard')) return;
      if (isOnboarded()) { welcomeBack(); return; }
      // Delay slightly so the page settles first
      setTimeout(function () {
        if (!isOnboarded()) show();
      }, 1500);
    } catch (e) {}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoInit);
  } else {
    setTimeout(autoInit, 100);
  }

})(typeof window !== 'undefined' ? window : this);
