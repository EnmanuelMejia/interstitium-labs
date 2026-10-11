/*
 * IL Avatar Behavior Layer — Noah / Genesis on /noah/ (Interstitium Labs).
 *
 * SCOPE
 *   Behavior layer ON TOP of the existing avatar engine
 *   (il-noah-avatar.js, #avatarSlot in the header). This module never
 *   replaces, forks, or re-renders the engine: it observes the page,
 *   reflects real tutor activity as presence states on #avatarSlot,
 *   adds lightweight reactions, celebrations, a popover, and a sharing
 *   card. Vanilla JS, zero dependencies, ES5-compatible.
 *
 * TWIN PARITY
 *   Noah and Genesis run the IDENTICAL code path with identical
 *   capabilities. Identity comes only from the tutor profile in
 *   localStorage 'il-noah-profile' (.avatar is 'noah' | 'genesis'):
 *   name, live avatar media, and accent (Noah: platform gold #c9a227;
 *   Genesis variant class ilab-is-genesis: warm gold #e6c95c).
 *
 * PRESENCE STATES (tied to REAL events, never faked)
 *   idle | listening | thinking | speaking | celebrating | reacting,
 *   applied as ilab-st-<state> classes on #avatarSlot plus a small
 *   state chip. Event sources:
 *     1. MutationObserver on #noahStatusText — its text is mapped:
 *        contains 'Listen' -> listening; 'Think' / 'Working' /
 *        'typing' -> thinking; 'Speak' / 'Playing' -> speaking;
 *        anything else -> idle.
 *     2. #micBtn click -> listening for 4s or until the status text
 *        changes, whichever comes first.
 *     3. Explicit API calls (ILAvatarFx.set / celebrate / react) and
 *        document events: 'il:goal-progress' (detail.text) triggers
 *        celebrate(); 'il:avatar-celebrate' and 'il:avatar-react'
 *        mirror the API.
 *   Transient states auto-return to idle (celebrating 2.6s,
 *   reacting 1.6s). prefers-reduced-motion disables animation;
 *   the state chip still shows.
 *
 * PREFERENCES CONTRACT
 *   Stored in localStorage 'il-noah-profile' under .avatarFx =
 *   { presence: true, reactions: true, celebrate: true }, merged so
 *   other profile fields are never clobbered. ILAvatarFx.prefs()
 *   reads them; ILAvatarFx.setPref(key, value) writes and applies:
 *     presence:false  -> no state classes and no chip.
 *     celebrate:false -> celebrate() degrades to a chip-only party
 *                        glyph, with no confetti burst.
 *     reactions:false -> no in-chat react buttons are injected.
 *   A Settings UI (added separately) drives these via the same API.
 *
 * IN-CHAT REACTIONS (session-local in v1)
 *   A MutationObserver on #threadInner adds a small heart button to
 *   each new assistant message. Clicking toggles a heart badge on
 *   that message and fires ILAvatarFx.react. NOTE: the chat history
 *   store is owned by the page (il-noah-threads-v1); reactions are
 *   NOT written to it — they persist for the session only in v1.
 *
 * SHARING CARD
 *   ILAvatarFx.card() builds the twin's 1200x630-proportioned card
 *   as DOM from the live slot media. Clicking #avatarSlot opens a
 *   popover: presence line, View avatar card (split pane via
 *   window.ILSplit when present, else a modal overlay), Download PNG
 *   (canvas render, feature-detected; the button hides when canvas
 *   or a CORS-clean image is unavailable — never a fake state), and
 *   Presentation (window.ILSettings.open('voice') when available).
 */
(function () {
  'use strict';

  /* Double-load guard. */
  if (window.ILAvatarFx) return;

  var PROFILE_KEY = 'il-noah-profile';
  var STYLE_ID = 'il-avatar-fx-style';
  var ACCENT_NOAH = '#c9a227';
  var ACCENT_GENESIS = '#e6c95c';
  var FALLBACK_NOAH = '/assets/noah/noah-avatar.png';
  var FALLBACK_GENESIS = '/assets/noah/genesis-avatar-3d.webp';
  var CAPABILITY = 'Tutoring, goal planning, memory, voice, files and everyday help — one personal agent.';
  var CARD_LINE = 'Personal AI tutor & agent — Interstitium Labs';
  var CARD_URL = 'interstitiumlabs.dev/noah/';
  var STATES = ['idle', 'listening', 'thinking', 'speaking', 'celebrating', 'reacting'];
  var LABELS = {
    idle: '',
    listening: 'Listening…',
    thinking: 'Thinking…',
    speaking: 'Speaking…',
    celebrating: '🎉',
    reacting: '♥'
  };
  var PREF_DEFAULTS = { presence: true, reactions: true, celebrate: true };
  var PARTICLES = ['🎉', '✨', '⭐', '💛', '🎊', '✦', '★', '♥'];

  var booted = false;
  var currentState = 'idle';
  var chipOverride = null;
  var idleTimer = null;
  var micTimer = null;
  var statusVersion = 0;
  var slotEl = null;
  var chipEl = null;
  var popEl = null;
  var modalEl = null;

  /* ---------------- helpers ---------------- */

  function $(id) { return document.getElementById(id); }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function readProfile() {
    try {
      var raw = window.localStorage ? window.localStorage.getItem(PROFILE_KEY) : null;
      if (raw) {
        var p = JSON.parse(raw);
        if (p && typeof p === 'object') return p;
      }
    } catch (e) {}
    return {};
  }

  function writeProfile(p) {
    try {
      if (window.localStorage) window.localStorage.setItem(PROFILE_KEY, JSON.stringify(p));
    } catch (e) {}
  }

  function twinId() {
    var p = readProfile();
    return p && p.avatar === 'genesis' ? 'genesis' : 'noah';
  }

  function twinName() { return twinId() === 'genesis' ? 'Genesis AI' : 'Noah AI'; }

  function accentHex() { return twinId() === 'genesis' ? ACCENT_GENESIS : ACCENT_NOAH; }

  function isValidState(s) {
    for (var i = 0; i < STATES.length; i++) if (STATES[i] === s) return true;
    return false;
  }

  function canvasSupported() {
    try {
      var c = document.createElement('canvas');
      if (!c.getContext || !c.getContext('2d')) return false;
      return typeof c.toDataURL === 'function';
    } catch (e) { return false; }
  }

  /* Live avatar media: prefer whatever the avatar engine placed in
     the slot (img src, else video poster / derived still), so the
     twin identity is always correct. Spec fallback last. */
  function currentAvatarSrc() {
    var slot = $('avatarSlot');
    if (slot) {
      var img = null;
      try { img = slot.querySelector('img'); } catch (e) {}
      if (img) {
        var isrc = img.currentSrc || img.getAttribute('src') || img.src || '';
        if (isrc) return isrc;
      }
      var video = null;
      try { video = slot.querySelector('video'); } catch (e2) {}
      if (video) {
        if (video.poster) return video.poster;
        var vsrc = video.currentSrc || video.getAttribute('src') || video.src || '';
        if (vsrc) {
          var derived = vsrc.replace(/-animated\.mp4(\?.*)?$/, '-3d.webp');
          if (derived !== vsrc) return derived;
          return vsrc;
        }
      }
    }
    var p = readProfile();
    if (typeof p.customAvatar === 'string' && p.customAvatar.indexOf('data:image/') === 0) {
      return p.customAvatar;
    }
    return twinId() === 'genesis' ? FALLBACK_GENESIS : FALLBACK_NOAH;
  }

  function slotRect() {
    var slot = $('avatarSlot');
    if (!slot || !slot.getBoundingClientRect) return null;
    var r = slot.getBoundingClientRect();
    if (!r.width && !r.height) return null;
    return r;
  }

  /* ---------------- preferences ---------------- */

  function prefs() {
    var p = readProfile();
    var fx = (p && p.avatarFx && typeof p.avatarFx === 'object') ? p.avatarFx : {};
    return {
      presence: fx.presence !== false,
      reactions: fx.reactions !== false,
      celebrate: fx.celebrate !== false
    };
  }

  function setPref(key, value) {
    if (!PREF_DEFAULTS.hasOwnProperty(key)) return prefs();
    var p = readProfile();
    var fx = (p.avatarFx && typeof p.avatarFx === 'object') ? p.avatarFx : {};
    var merged = {
      presence: fx.presence !== false,
      reactions: fx.reactions !== false,
      celebrate: fx.celebrate !== false
    };
    merged[key] = !!value;
    p.avatarFx = merged;
    writeProfile(p);
    applyPrefs();
    return prefs();
  }

  function applyPrefs() {
    var p = prefs();
    if (!p.presence) {
      clearStateClasses();
      hideChip();
    } else {
      applyState(currentState, chipOverride);
    }
    if (!p.reactions) {
      var btns = document.querySelectorAll('.ilab-react-btn');
      for (var i = 0; i < btns.length; i++) {
        if (btns[i].parentNode) btns[i].parentNode.removeChild(btns[i]);
      }
      var msgs = document.querySelectorAll('#threadInner .msg');
      for (var j = 0; j < msgs.length; j++) msgs[j].removeAttribute('data-ilab-decorated');
    } else {
      decorateExisting();
    }
  }

  /* ---------------- styles ---------------- */

  function injectStyle() {
    if ($(STYLE_ID)) return;
    var css = [
      '#avatarSlot{--ilab-accent:' + ACCENT_NOAH + ';position:relative;cursor:pointer}',
      '#avatarSlot.ilab-is-genesis{--ilab-accent:' + ACCENT_GENESIS + '}',
      '#avatarSlot.ilab-st-listening{box-shadow:0 0 0 2px var(--ilab-accent),0 0 16px rgba(64,224,208,.45);animation:ilab-pulse 1.6s ease-in-out infinite}',
      '#avatarSlot.ilab-st-thinking{box-shadow:0 0 0 2px var(--ilab-accent),0 0 18px rgba(201,162,39,.5);animation:ilab-pulse 1.1s ease-in-out infinite}',
      '#avatarSlot.ilab-st-speaking{box-shadow:0 0 0 2px var(--ilab-accent),0 0 20px rgba(201,162,39,.55);animation:ilab-pulse .7s ease-in-out infinite}',
      '#avatarSlot.ilab-st-celebrating{box-shadow:0 0 0 3px var(--ilab-accent),0 0 26px rgba(201,162,39,.7);animation:ilab-celebrate-ring .6s ease-in-out infinite}',
      '#avatarSlot.ilab-st-reacting{box-shadow:0 0 0 2px var(--ilab-accent),0 0 18px rgba(244,114,182,.55);animation:ilab-react-pop 1.6s ease-out}',
      '#avatarSlot.ilab-is-genesis.ilab-st-listening{box-shadow:0 0 0 2px var(--ilab-accent),0 0 16px rgba(230,201,92,.5)}',
      '#avatarSlot.ilab-is-genesis.ilab-st-thinking{box-shadow:0 0 0 2px var(--ilab-accent),0 0 18px rgba(230,201,92,.55)}',
      '#avatarSlot.ilab-is-genesis.ilab-st-speaking{box-shadow:0 0 0 2px var(--ilab-accent),0 0 20px rgba(230,201,92,.6)}',
      '#avatarSlot.ilab-is-genesis.ilab-st-celebrating{box-shadow:0 0 0 3px var(--ilab-accent),0 0 26px rgba(230,201,92,.75)}',
      '@keyframes ilab-pulse{0%,100%{box-shadow:0 0 0 2px var(--ilab-accent),0 0 10px rgba(201,162,39,.3)}50%{box-shadow:0 0 0 3px var(--ilab-accent),0 0 22px rgba(201,162,39,.6)}}',
      '@keyframes ilab-celebrate-ring{0%,100%{transform:scale(1)}50%{transform:scale(1.07)}}',
      '@keyframes ilab-react-pop{0%{transform:scale(1)}25%{transform:scale(1.1)}55%{transform:scale(.97)}100%{transform:scale(1)}}',
      '.ilab-chip{position:fixed;z-index:90;transform:translateX(-50%);background:#0d1119;color:#e9edf5;',
      'border:1px solid var(--ilab-accent,#c9a227);border-radius:999px;padding:.18rem .6rem;',
      'font:600 .72rem/1.4 ui-sans-serif,system-ui,sans-serif;letter-spacing:.02em;white-space:nowrap;',
      'box-shadow:0 6px 18px rgba(0,0,0,.45);pointer-events:none;opacity:0;transition:opacity .18s ease;display:none}',
      '.ilab-chip.on{opacity:1;display:block}',
      '.ilab-burst{position:fixed;z-index:95;width:0;height:0;pointer-events:none}',
      '.ilab-particle{position:absolute;left:0;top:0;font-size:16px;line-height:1;pointer-events:none;',
      'animation:ilab-particle-fly .95s ease-out forwards}',
      '@keyframes ilab-particle-fly{0%{transform:translate(0,0) scale(.6) rotate(0deg);opacity:1}',
      '100%{transform:translate(var(--ilab-dx,0px),var(--ilab-dy,-40px)) scale(1.15) rotate(var(--ilab-rot,40deg));opacity:0}}',
      '.ilab-float{position:fixed;z-index:95;transform:translateX(-50%);font-size:20px;line-height:1;',
      'pointer-events:none;animation:ilab-float-up 1.45s ease-out forwards}',
      '@keyframes ilab-float-up{0%{transform:translate(-50%,0) scale(.8);opacity:0}',
      '18%{opacity:1}100%{transform:translate(-50%,-58px) scale(1.2);opacity:0}}',
      '#threadInner .msg{position:relative}',
      '.ilab-react-btn{position:absolute;top:6px;right:6px;z-index:3;width:26px;height:26px;border-radius:50%;',
      'border:1px solid rgba(255,255,255,.16);background:rgba(13,17,25,.72);color:#f9a8d4;font-size:13px;line-height:1;',
      'display:flex;align-items:center;justify-content:center;cursor:pointer;opacity:.35;padding:0}',
      '.ilab-react-btn:hover,.ilab-react-btn:focus-visible{opacity:1;border-color:rgba(244,114,182,.7)}',
      '.ilab-react-btn[aria-pressed="true"]{opacity:1;background:rgba(244,114,182,.22);border-color:rgba(244,114,182,.8)}',
      '.ilab-badge{display:inline-flex;align-items:center;justify-content:center;min-width:22px;height:22px;',
      'padding:0 6px;border-radius:999px;background:rgba(244,114,182,.2);border:1px solid rgba(244,114,182,.65);',
      'color:#f9a8d4;font-size:12px;line-height:1;margin-top:6px}',
      '.ilab-pop{position:fixed;z-index:96;min-width:236px;max-width:280px;background:#0d1119;color:#e9edf5;',
      'border:1px solid rgba(201,162,39,.45);border-radius:14px;padding:10px;',
      'box-shadow:0 18px 44px rgba(0,0,0,.55);font:400 .85rem/1.45 ui-sans-serif,system-ui,sans-serif}',
      '.ilab-pop-presence{font-size:.8rem;color:#c8cfdb;padding:.15rem .35rem .55rem;display:flex;align-items:center;gap:.45rem}',
      '.ilab-pop-dot{width:8px;height:8px;border-radius:50%;background:var(--ilab-accent,#c9a227);flex:0 0 8px;',
      'box-shadow:0 0 8px var(--ilab-accent,#c9a227)}',
      '.ilab-pop-btn{display:block;width:100%;text-align:left;background:rgba(255,255,255,.04);',
      'border:1px solid rgba(255,255,255,.1);color:inherit;border-radius:9px;padding:.5rem .65rem;',
      'font:inherit;font-size:.84rem;cursor:pointer;margin-top:6px}',
      '.ilab-pop-btn:hover{border-color:rgba(201,162,39,.65);background:rgba(201,162,39,.1)}',
      '.ilab-pop-btn[hidden]{display:none}',
      '.ilab-modal-overlay{position:fixed;inset:0;z-index:97;background:rgba(3,5,9,.68);',
      'display:flex;align-items:center;justify-content:center;padding:16px;overflow:auto}',
      '.ilab-modal{background:#0a0d13;border:1px solid rgba(201,162,39,.4);border-radius:16px;',
      'padding:18px;max-width:min(1240px,96vw);box-shadow:0 24px 60px rgba(0,0,0,.6)}',
      '.ilab-modal-bar{display:flex;gap:8px;justify-content:flex-end;margin-top:12px}',
      '.ilab-card{box-sizing:border-box}',
      '.ilab-card-actions{margin:12px 0 0;text-align:right}',
      '.ilab-dl-btn{background:rgba(201,162,39,.14);border:1px solid rgba(201,162,39,.55);color:#e9edf5;',
      'border-radius:9px;padding:.5rem .85rem;font:600 .85rem ui-sans-serif,system-ui,sans-serif;cursor:pointer}',
      '.ilab-dl-btn:hover{background:rgba(201,162,39,.26)}',
      '@media (prefers-reduced-motion: reduce){',
      '#avatarSlot.ilab-st-listening,#avatarSlot.ilab-st-thinking,#avatarSlot.ilab-st-speaking,',
      '#avatarSlot.ilab-st-celebrating,#avatarSlot.ilab-st-reacting{animation:none}',
      '.ilab-particle,.ilab-float{display:none}',
      '.ilab-chip{transition:none}',
      '}'
    ].join('\n');
    var style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = css;
    document.head.appendChild(style);
  }

  /* ---------------- presence state ---------------- */

  function refreshTwinClass() {
    var slot = $('avatarSlot');
    if (!slot) return;
    if (twinId() === 'genesis') slot.classList.add('ilab-is-genesis');
    else slot.classList.remove('ilab-is-genesis');
  }

  function clearStateClasses() {
    var slot = $('avatarSlot');
    if (!slot) return;
    for (var i = 0; i < STATES.length; i++) slot.classList.remove('ilab-st-' + STATES[i]);
  }

  function ensureChip() {
    if (chipEl && chipEl.parentNode) return chipEl;
    chipEl = document.createElement('div');
    chipEl.className = 'ilab-chip';
    chipEl.id = 'ilabChip';
    chipEl.setAttribute('aria-hidden', 'true');
    document.body.appendChild(chipEl);
    return chipEl;
  }

  function placeChip() {
    if (!chipEl) return;
    var r = slotRect();
    if (!r) return;
    chipEl.style.left = (r.left + r.width / 2) + 'px';
    chipEl.style.top = (r.bottom + 6) + 'px';
    chipEl.style.setProperty('--ilab-accent', accentHex());
  }

  function showChip(text) {
    ensureChip();
    chipEl.textContent = text;
    placeChip();
    chipEl.classList.add('on');
  }

  function hideChip() {
    if (chipEl) chipEl.classList.remove('on');
  }

  function clearIdleTimer() {
    if (idleTimer) { clearTimeout(idleTimer); idleTimer = null; }
  }

  function scheduleIdle(ms) {
    clearIdleTimer();
    idleTimer = setTimeout(function () {
      idleTimer = null;
      chipOverride = null;
      applyState('idle', null);
    }, ms);
  }

  function applyState(state, chipText) {
    if (!isValidState(state)) state = 'idle';
    currentState = state;
    chipOverride = chipText != null ? String(chipText) : null;
    if (state !== 'celebrating' && state !== 'reacting') clearIdleTimer();
    var p = prefs();
    var slot = $('avatarSlot');
    refreshTwinClass();
    if (!p.presence) {
      clearStateClasses();
      hideChip();
      return currentState;
    }
    if (slot) {
      clearStateClasses();
      slot.classList.add('ilab-st-' + state);
    }
    if (state === 'idle') hideChip();
    else showChip(chipOverride != null ? chipOverride : (LABELS[state] || state));
    return currentState;
  }

  function setPublic(state) {
    if (!isValidState(state)) state = 'idle';
    applyState(state, null);
    if (state === 'celebrating') scheduleIdle(2600);
    else if (state === 'reacting') scheduleIdle(1600);
    return currentState;
  }

  function state() { return currentState; }

  function stateFromStatusText(text) {
    var t = String(text == null ? '' : text);
    if (t.indexOf('Listen') !== -1) return 'listening';
    if (t.indexOf('Think') !== -1 || t.indexOf('Working') !== -1 ||
        t.indexOf('typing') !== -1 || t.indexOf('Typing') !== -1) return 'thinking';
    if (t.indexOf('Speak') !== -1 || t.indexOf('Playing') !== -1) return 'speaking';
    return 'idle';
  }

  /* ---------------- celebration + reaction fx ---------------- */

  function burst() {
    var r = slotRect();
    if (!r) return;
    var layer = document.createElement('div');
    layer.className = 'ilab-burst';
    layer.style.left = (r.left + r.width / 2) + 'px';
    layer.style.top = (r.top + r.height / 2) + 'px';
    document.body.appendChild(layer);
    for (var i = 0; i < 14; i++) {
      var span = document.createElement('span');
      span.className = 'ilab-particle';
      span.textContent = PARTICLES[i % PARTICLES.length];
      var ang = (Math.PI * 2 * i) / 14 + (Math.random() * 0.35 - 0.17);
      var dist = 44 + Math.random() * 42;
      var dx = Math.round(Math.cos(ang) * dist);
      var dy = Math.round(Math.sin(ang) * dist) - 14;
      span.style.setProperty('--ilab-dx', dx + 'px');
      span.style.setProperty('--ilab-dy', dy + 'px');
      span.style.setProperty('--ilab-rot', (Math.random() * 160 - 80) + 'deg');
      span.style.marginLeft = '-8px';
      span.style.marginTop = '-8px';
      layer.appendChild(span);
    }
    setTimeout(function () {
      if (layer.parentNode) layer.parentNode.removeChild(layer);
    }, 1100);
  }

  function floatEmoji(emoji) {
    var r = slotRect();
    if (!r) return;
    var span = document.createElement('span');
    span.className = 'ilab-float';
    span.textContent = emoji;
    span.style.left = (r.left + r.width / 2) + 'px';
    span.style.top = (r.top - 6) + 'px';
    document.body.appendChild(span);
    setTimeout(function () {
      if (span.parentNode) span.parentNode.removeChild(span);
    }, 1550);
  }

  function celebrate(reason) {
    var p = prefs();
    var raw = reason != null ? String(reason) : '';
    var text = raw.replace(/^\s+|\s+$/g, '').length ? raw.slice(0, 80) : null;
    if (!p.celebrate) {
      /* Degraded: chip-only party glyph, no burst, no reason text. */
      applyState('celebrating', '🎉');
      scheduleIdle(2600);
      return currentState;
    }
    applyState('celebrating', text || '🎉');
    scheduleIdle(2600);
    if (p.presence) burst();
    return currentState;
  }

  function react(emoji) {
    var e = emoji != null && String(emoji).length ? String(emoji).slice(0, 8) : '♥';
    applyState('reacting', e);
    scheduleIdle(1600);
    if (prefs().presence) floatEmoji(e);
    return currentState;
  }

  /* ---------------- in-chat reactions ---------------- */

  function isAssistantMsg(el) {
    if (!el || !el.classList) return false;
    if (!el.classList.contains('msg')) return false;
    if (el.classList.contains('user')) return false;
    if (el.id === 'typingRow') return false;
    /* On /noah/ every non-user .msg row is an assistant row (.msg.noah). */
    return true;
  }

  function decorateMessage(msg) {
    if (!msg || msg.getAttribute('data-ilab-decorated') === '1') return;
    if (!isAssistantMsg(msg)) return;
    if (!prefs().reactions) return;
    var bubble = null;
    try { bubble = msg.querySelector('.bubble'); } catch (e) {}
    if (!bubble) return;
    if (msg.querySelector('.ilab-react-btn')) {
      msg.setAttribute('data-ilab-decorated', '1');
      return;
    }
    msg.setAttribute('data-ilab-decorated', '1');
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'ilab-react-btn';
    btn.textContent = '♥';
    btn.title = 'React';
    btn.setAttribute('aria-label', 'React to this message');
    btn.setAttribute('aria-pressed', 'false');
    btn.addEventListener('click', function (ev) {
      if (ev && ev.stopPropagation) ev.stopPropagation();
      toggleBadge(msg, btn);
    });
    msg.appendChild(btn);
  }

  function toggleBadge(msg, btn) {
    var bubble = null;
    try { bubble = msg.querySelector('.bubble'); } catch (e) {}
    var host = bubble || msg;
    var existing = null;
    try { existing = host.querySelector('.ilab-badge'); } catch (e2) {}
    if (existing) {
      existing.parentNode.removeChild(existing);
      if (btn) btn.setAttribute('aria-pressed', 'false');
      return;
    }
    var badge = document.createElement('span');
    badge.className = 'ilab-badge';
    badge.textContent = '♥';
    badge.setAttribute('aria-label', 'You reacted with a heart');
    host.appendChild(badge);
    if (btn) btn.setAttribute('aria-pressed', 'true');
    react('♥');
  }

  function decorateNode(node) {
    if (!node || node.nodeType !== 1) return;
    if (node.classList && node.classList.contains('msg')) decorateMessage(node);
    if (node.querySelectorAll) {
      var found = node.querySelectorAll('.msg');
      for (var i = 0; i < found.length; i++) decorateMessage(found[i]);
    }
  }

  function decorateExisting() {
    var inner = $('threadInner');
    if (!inner || !inner.querySelectorAll) return;
    var found = inner.querySelectorAll('.msg');
    for (var i = 0; i < found.length; i++) decorateMessage(found[i]);
  }

  /* ---------------- sharing card ---------------- */

  function buildCard() {
    var id = twinId();
    var name = twinName();
    var accent = accentHex();
    var src = currentAvatarSrc();
    var card = document.createElement('div');
    card.className = 'ilab-card' + (id === 'genesis' ? ' ilab-card-genesis' : '');
    card.setAttribute('data-ilab-card', id);
    card.setAttribute('role', 'img');
    card.setAttribute('aria-label', name + ' — ' + CARD_LINE);
    card.style.cssText =
      'display:flex;align-items:center;gap:40px;width:1200px;max-width:100%;' +
      'aspect-ratio:1200/630;background:#06080c;border:3px solid ' + accent + ';' +
      'border-radius:20px;padding:52px 60px;color:#e9edf5;' +
      'font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;' +
      'box-shadow:inset 0 0 0 1px rgba(255,255,255,.1)';
    var img = document.createElement('img');
    img.className = 'ilab-card-img';
    img.setAttribute('src', src);
    img.setAttribute('alt', '');
    img.setAttribute('onerror', "this.style.display='none'");
    img.style.cssText =
      'width:230px;height:230px;flex:0 0 230px;border-radius:50%;object-fit:cover;' +
      'object-position:center 18%;border:4px solid ' + accent + ';background:#0d1119';
    card.appendChild(img);
    var body = document.createElement('div');
    body.className = 'ilab-card-body';
    body.style.cssText = 'min-width:0;flex:1';
    body.innerHTML =
      '<div class="ilab-card-name" style="font-size:52px;font-weight:800;letter-spacing:.01em;line-height:1.1">' + esc(name) + '</div>' +
      '<div class="ilab-card-line" style="font-size:25px;color:#c8cfdb;margin-top:14px;line-height:1.35">' + esc(CARD_LINE) + '</div>' +
      '<div class="ilab-card-cap" style="font-size:21px;color:#8b93a5;margin-top:12px;line-height:1.4">' + esc(CAPABILITY) + '</div>' +
      '<div class="ilab-card-url" style="font-size:24px;font-weight:700;color:' + accent + ';margin-top:22px">' + esc(CARD_URL) + '</div>';
    card.appendChild(body);
    return card;
  }

  function cardHTML() {
    var el = buildCard();
    return el.outerHTML || '';
  }

  function cardHTMLWithDownload() {
    var btn = '';
    if (canvasSupported()) {
      btn = '<p class="ilab-card-actions"><button type="button" class="ilab-dl-btn" data-ilab-download="1">⬇ Download PNG</button></p>';
    }
    return '<div class="ilab-card-wrap">' + cardHTML() + btn + '</div>';
  }

  function hideDownloadButtons() {
    var all = document.querySelectorAll('[data-ilab-download],[data-ilab-download-btn]');
    for (var i = 0; i < all.length; i++) {
      all[i].style.display = 'none';
      all[i].setAttribute('hidden', '');
    }
    if (popEl) {
      var pb = popEl.querySelector('[data-ilab-act="download"]');
      if (pb) pb.style.display = 'none';
    }
  }

  function triggerCanvasDownload(canvas) {
    var url = canvas.toDataURL('image/png');
    var a = document.createElement('a');
    a.href = url;
    a.download = twinId() === 'genesis' ? 'genesis-ai-card.png' : 'noah-ai-card.png';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  function downloadPNG() {
    if (!canvasSupported()) { hideDownloadButtons(); return; }
    var name = twinName();
    var accent = accentHex();
    var src = currentAvatarSrc();
    var canvas = document.createElement('canvas');
    canvas.width = 1200;
    canvas.height = 630;
    var ctx = null;
    try { ctx = canvas.getContext('2d'); } catch (e) {}
    if (!ctx) { hideDownloadButtons(); return; }

    function fitText(text, maxWidth, font) {
      ctx.font = font;
      var out = String(text);
      while (out.length > 4 && ctx.measureText(out).width > maxWidth) {
        out = out.slice(0, out.length - 2);
      }
      if (out !== String(text)) out = out.replace(/\s+$/, '') + '…';
      return out;
    }

    function paint(img) {
      ctx.fillStyle = '#06080c';
      ctx.fillRect(0, 0, 1200, 630);
      ctx.strokeStyle = accent;
      ctx.lineWidth = 6;
      ctx.strokeRect(18, 18, 1164, 594);
      ctx.strokeStyle = 'rgba(255,255,255,0.14)';
      ctx.lineWidth = 1;
      ctx.strokeRect(30, 30, 1140, 570);
      if (img) {
        try {
          ctx.save();
          ctx.beginPath();
          ctx.arc(215, 315, 148, 0, Math.PI * 2);
          ctx.closePath();
          ctx.clip();
          var iw = img.naturalWidth || img.width || 300;
          var ih = img.naturalHeight || img.height || 300;
          var scale = Math.max(296 / iw, 296 / ih);
          var dw = iw * scale;
          var dh = ih * scale;
          ctx.drawImage(img, 215 - dw / 2, 315 - dh / 2, dw, dh);
          ctx.restore();
          ctx.beginPath();
          ctx.arc(215, 315, 148, 0, Math.PI * 2);
          ctx.strokeStyle = accent;
          ctx.lineWidth = 4;
          ctx.stroke();
        } catch (e) {}
      } else {
        ctx.beginPath();
        ctx.arc(215, 315, 148, 0, Math.PI * 2);
        ctx.fillStyle = '#0d1119';
        ctx.fill();
        ctx.strokeStyle = accent;
        ctx.lineWidth = 4;
        ctx.stroke();
        ctx.fillStyle = accent;
        ctx.font = '800 92px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(name.charAt(0), 215, 348);
        ctx.textAlign = 'left';
      }
      ctx.fillStyle = '#e9edf5';
      ctx.font = '800 66px sans-serif';
      ctx.fillText(fitText(name, 720, '800 66px sans-serif'), 420, 248);
      ctx.fillStyle = '#c8cfdb';
      ctx.font = '400 29px sans-serif';
      ctx.fillText(fitText(CARD_LINE, 720, '400 29px sans-serif'), 420, 304);
      ctx.fillStyle = '#8b93a5';
      ctx.font = '400 24px sans-serif';
      ctx.fillText(fitText(CAPABILITY, 720, '400 24px sans-serif'), 420, 352);
      ctx.fillStyle = accent;
      ctx.font = '700 27px sans-serif';
      ctx.fillText(CARD_URL, 420, 428);
      try {
        triggerCanvasDownload(canvas);
      } catch (err) {
        /* Tainted canvas (CORS) or encoder failure: hide, never error. */
        hideDownloadButtons();
      }
    }

    if (src) {
      var probe = new Image();
      var settled = false;
      try { probe.crossOrigin = 'anonymous'; } catch (e2) {}
      probe.onload = function () {
        if (settled) return;
        settled = true;
        paint(probe);
      };
      probe.onerror = function () {
        if (settled) return;
        settled = true;
        hideDownloadButtons();
        paint(null);
      };
      try {
        probe.src = src;
      } catch (e3) {
        paint(null);
      }
    } else {
      paint(null);
    }
  }

  function probeDownloadImage() {
    if (!canvasSupported()) { hideDownloadButtons(); return; }
    var src = currentAvatarSrc();
    if (!src || src.indexOf('data:') === 0) return;
    var probe = new Image();
    var doneFlag = false;
    try { probe.crossOrigin = 'anonymous'; } catch (e) {}
    probe.onload = function () { doneFlag = true; };
    probe.onerror = function () {
      if (doneFlag) return;
      doneFlag = true;
      hideDownloadButtons();
    };
    try { probe.src = src; } catch (e2) {}
  }

  /* ---------------- card presentation: split pane or modal ---------------- */

  function closeModal() {
    if (modalEl && modalEl.parentNode) modalEl.parentNode.removeChild(modalEl);
    modalEl = null;
  }

  function openModal() {
    closeModal();
    var overlay = document.createElement('div');
    overlay.className = 'ilab-modal-overlay';
    var box = document.createElement('div');
    box.className = 'ilab-modal';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-label', 'Avatar card');
    box.appendChild(buildCard());
    var bar = document.createElement('div');
    bar.className = 'ilab-modal-bar';
    if (canvasSupported()) {
      var dl = document.createElement('button');
      dl.type = 'button';
      dl.className = 'ilab-dl-btn';
      dl.setAttribute('data-ilab-download-btn', '1');
      dl.textContent = '⬇ Download PNG';
      dl.addEventListener('click', function () { downloadPNG(); });
      bar.appendChild(dl);
    }
    var closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'ilab-dl-btn';
    closeBtn.textContent = 'Close';
    closeBtn.addEventListener('click', closeModal);
    bar.appendChild(closeBtn);
    box.appendChild(bar);
    overlay.appendChild(box);
    overlay.addEventListener('click', function (ev) {
      if (ev.target === overlay) closeModal();
    });
    document.body.appendChild(overlay);
    modalEl = overlay;
    probeDownloadImage();
  }

  function openCardView() {
    if (window.ILSplit && typeof window.ILSplit.open === 'function') {
      try {
        window.ILSplit.open({
          kind: 'html',
          title: 'Avatar card',
          html: cardHTMLWithDownload()
        });
        return;
      } catch (e) {}
    }
    openModal();
  }

  /* ---------------- popover ---------------- */

  function presenceLine() {
    var label = currentState === 'idle' ? 'Idle — ready' : (LABELS[currentState] || currentState);
    if (chipOverride && (currentState === 'celebrating' || currentState === 'reacting')) {
      label = chipOverride;
    }
    return twinName() + ' · ' + label;
  }

  function closePopover() {
    if (popEl && popEl.parentNode) popEl.parentNode.removeChild(popEl);
    popEl = null;
  }

  function placePopover() {
    if (!popEl) return;
    var r = slotRect();
    if (!r) return;
    var left = r.left;
    var maxLeft = (window.innerWidth || 320) - 292;
    if (left > maxLeft) left = Math.max(8, maxLeft);
    popEl.style.left = left + 'px';
    popEl.style.top = (r.bottom + 8) + 'px';
  }

  function togglePopover() {
    if (popEl) { closePopover(); return; }
    var pop = document.createElement('div');
    pop.className = 'ilab-pop';
    pop.id = 'ilabPop';
    pop.setAttribute('role', 'menu');
    pop.setAttribute('aria-label', 'Avatar menu');
    pop.style.setProperty('--ilab-accent', accentHex());

    var line = document.createElement('div');
    line.className = 'ilab-pop-presence';
    var dot = document.createElement('span');
    dot.className = 'ilab-pop-dot';
    line.appendChild(dot);
    var lineText = document.createElement('span');
    lineText.className = 'ilab-pop-presence-text';
    lineText.textContent = presenceLine();
    line.appendChild(lineText);
    pop.appendChild(line);

    function addBtn(label, act) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'ilab-pop-btn';
      b.setAttribute('data-ilab-act', act);
      b.textContent = label;
      b.addEventListener('click', function (ev) {
        if (ev && ev.stopPropagation) ev.stopPropagation();
        if (act === 'card') { closePopover(); openCardView(); }
        else if (act === 'download') { downloadPNG(); }
        else if (act === 'present') {
          closePopover();
          try {
            if (window.ILSettings && typeof window.ILSettings.open === 'function') {
              window.ILSettings.open('voice');
            }
          } catch (e) {}
        }
      });
      pop.appendChild(b);
      return b;
    }

    addBtn('🪪 View avatar card', 'card');
    var dlBtn = addBtn('⬇ Download PNG', 'download');
    dlBtn.setAttribute('data-ilab-download-btn', '1');
    if (!canvasSupported()) dlBtn.style.display = 'none';
    var presBtn = addBtn('🎛 Presentation…', 'present');
    if (!(window.ILSettings && typeof window.ILSettings.open === 'function')) {
      presBtn.style.display = 'none';
    }
    pop.addEventListener('click', function (ev) {
      if (ev && ev.stopPropagation) ev.stopPropagation();
    });
    document.body.appendChild(pop);
    popEl = pop;
    placePopover();
    probeDownloadImage();
  }

  /* ---------------- API ---------------- */

  var api = {
    set: setPublic,
    celebrate: celebrate,
    react: react,
    card: buildCard,
    prefs: prefs,
    setPref: setPref,
    state: state
  };

  /* ---------------- boot (/noah/ only) ---------------- */

  function boot() {
    if (booted) return;
    if (!document.getElementById('newChatBtn')) return;
    booted = true;

    window.ILAvatarFx = api;

    injectStyle();
    slotEl = $('avatarSlot');
    refreshTwinClass();
    ensureChip();
    applyState('idle', null);

    /* (1) Status text observer — the real tutor activity signal. */
    var statusText = $('noahStatusText');
    if (statusText && typeof MutationObserver === 'function') {
      var statusObs = new MutationObserver(function () {
        statusVersion++;
        if (micTimer) { clearTimeout(micTimer); micTimer = null; }
        var mapped = stateFromStatusText(statusText.textContent || '');
        var transientActive = (currentState === 'celebrating' || currentState === 'reacting') && !!idleTimer;
        if (transientActive) {
          if (mapped === 'idle') return;
          clearIdleTimer();
        }
        if (mapped !== currentState) applyState(mapped, null);
        placeChip();
      });
      statusObs.observe(statusText, { childList: true, characterData: true, subtree: true });
    }

    /* (2) Mic button -> listening for 4s or until status changes. */
    var micBtn = $('micBtn');
    if (micBtn) {
      micBtn.addEventListener('click', function () {
        var v = statusVersion;
        applyState('listening', null);
        if (micTimer) clearTimeout(micTimer);
        micTimer = setTimeout(function () {
          micTimer = null;
          if (currentState === 'listening' && statusVersion === v) applyState('idle', null);
        }, 4000);
      });
    }

    /* (3) Document events. */
    document.addEventListener('il:goal-progress', function (ev) {
      var detail = (ev && ev.detail) || {};
      celebrate(detail.text || detail.reason || null);
    });
    document.addEventListener('il:avatar-celebrate', function (ev) {
      var detail = (ev && ev.detail) || {};
      celebrate(detail.text || detail.reason || null);
    });
    document.addEventListener('il:avatar-react', function (ev) {
      var detail = (ev && ev.detail) || {};
      react(detail.emoji || '♥');
    });

    /* Avatar slot click -> popover. */
    if (slotEl) {
      slotEl.addEventListener('click', function (ev) {
        if (ev && ev.stopPropagation) ev.stopPropagation();
        togglePopover();
      });
    }

    /* Split-pane download buttons (data attribute delegation). */
    document.addEventListener('click', function (ev) {
      var t = ev && ev.target;
      var guard = 0;
      while (t && t !== document && guard < 8) {
        if (t.getAttribute && t.getAttribute('data-ilab-download')) {
          downloadPNG();
          return;
        }
        t = t.parentNode;
        guard++;
      }
      /* Outside click closes the popover. */
      if (popEl) {
        var insidePop = false;
        var insideSlot = false;
        var n = ev && ev.target;
        var g2 = 0;
        while (n && n !== document && g2 < 10) {
          if (n === popEl) insidePop = true;
          if (slotEl && n === slotEl) insideSlot = true;
          n = n.parentNode;
          g2++;
        }
        if (!insidePop && !insideSlot) closePopover();
      }
    });

    document.addEventListener('keydown', function (ev) {
      if (ev && ev.key === 'Escape') {
        closePopover();
        closeModal();
      }
    });

    window.addEventListener('resize', function () {
      if (chipEl && chipEl.classList.contains('on')) placeChip();
      placePopover();
    });
    window.addEventListener('scroll', function () {
      if (chipEl && chipEl.classList.contains('on')) placeChip();
      placePopover();
    }, true);

    /* Twin identity can change without a reload. */
    window.addEventListener('il-noah-profile', function () {
      refreshTwinClass();
      if (popEl) {
        var txt = popEl.querySelector('.ilab-pop-presence-text');
        if (txt) txt.textContent = presenceLine();
        popEl.style.setProperty('--ilab-accent', accentHex());
      }
    });
    window.addEventListener('storage', function (ev) {
      if (!ev || ev.key === PROFILE_KEY || ev.key === null) refreshTwinClass();
    });

    /* In-chat reactions observer. */
    var inner = $('threadInner');
    if (inner && typeof MutationObserver === 'function') {
      var threadObs = new MutationObserver(function (mutations) {
        for (var i = 0; i < mutations.length; i++) {
          var added = mutations[i].addedNodes || [];
          for (var j = 0; j < added.length; j++) decorateNode(added[j]);
        }
      });
      threadObs.observe(inner, { childList: true, subtree: true });
    }
    decorateExisting();
    applyPrefs();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
