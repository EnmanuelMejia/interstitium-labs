/*!
 * IL Floating Audio Widget (il-audio-widget.js)
 * ---------------------------------------------------------------------------
 * Singleton floating audio player. Auto-injects into any page that loads it.
 * Survives navigation by re-initializing from localStorage on each page load
 * (same theme, volume, minimized state, position).
 *
 * Requires: il-ambient-synth.js (ILAmbient singleton with getFrequencyData).
 *
 * State keys (localStorage):
 *   il-aw-theme      active theme name
 *   il-aw-volume     0..1
 *   il-aw-min        '1' when minimized
 *   il-aw-pos        JSON {x, y} drag position (viewport-relative)
 *   il-aw-muted      '1' when master-muted
 */
(function () {
  'use strict';

  // Singleton guard — rebuild-aware for SPA navigation.
  // il-spa-nav.js swaps documents via document.open/write/close: the Window
  // survives (so this flag stays set) but the widget DOM is wiped. If the
  // element is gone, rebuild it; only skip when it's already live.
  var WIDGET_ID = 'il-audio-widget';
  var rebuilding = false;
  if (window.__ilAudioWidgetDone) {
    if (document.getElementById(WIDGET_ID)) return;
    rebuilding = true;
  }
  window.__ilAudioWidgetDone = true;

  // Build generation: stale rAF loops / intervals from a previous document
  // must stop once a rebuild starts.
  window.__ilAwGen = (window.__ilAwGen || 0) + 1;
  var MY_GEN = window.__ilAwGen;

  var LS_THEME = 'il-aw-theme';
  var LS_VOL = 'il-aw-volume';
  var LS_MIN = 'il-aw-min';
  var LS_POS = 'il-aw-pos';
  var LS_MUTED = 'il-aw-muted';

  function lsGet(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { window.localStorage.setItem(k, v); } catch (e) {} }

  // Theme order for the "next" button and selector.
  var THEME_ORDER = [
    'cybersecurity', 'matrix', 'tron', 'cyberpunk', 'dune',
    'oceandeep', 'vaporwave', 'sacredgeo',
    'thrash', 'grunge', 'terminator',
    'mozart', 'chopin', 'bach', 'beethoven', 'debussy',
    'synthwave', 'techno'
  ];

  function themeLabel(name) {
    if (window.ILAmbient && window.ILAmbient.themes && window.ILAmbient.themes[name]) {
      return window.ILAmbient.themes[name].label;
    }
    return name.charAt(0).toUpperCase() + name.slice(1);
  }

  function buildWidget() {
    var root = document.createElement('div');
    root.className = 'il-aw';
    root.id = WIDGET_ID;
    root.setAttribute('role', 'region');
    root.setAttribute('aria-label', 'Ambient audio player');

    // Minimized view.
    var mini = document.createElement('div');
    mini.className = 'il-aw__mini il-aw__drag';
    mini.setAttribute('title', 'Ambient audio — click to expand');
    mini.innerHTML =
      '<canvas id="il-aw-eq-mini" width="60" height="44" aria-hidden="true"></canvas>' +
      '<span class="il-aw__mini-dot" aria-hidden="true"></span>';
    root.appendChild(mini);

    // Full view.
    var full = document.createElement('div');
    full.className = 'il-aw__full';

    full.innerHTML =
      '<div class="il-aw__header il-aw__drag">' +
        '<span class="il-aw__title">Now Playing</span>' +
        '<div class="il-aw__header-btns">' +
          '<button class="il-aw__iconbtn" data-aw="min" aria-label="Minimize player" title="Minimize">' +
            '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"/></svg>' +
          '</button>' +
          '<button class="il-aw__iconbtn" data-aw="mute" aria-label="Mute / unmute" title="Mute">' +
            '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 5 6 9H2v6h4l5 4V5z"/><line x1="23" y1="1" x2="1" y2="23"/></svg>' +
          '</button>' +
        '</div>' +
      '</div>' +
      '<div class="il-aw__art" data-art="cyberpunk" aria-hidden="true">' +
        '<span class="il-aw__art-label">Cyberpunk</span>' +
        '<span class="il-aw__art-sub">432 Hz</span>' +
      '</div>' +
      '<canvas class="il-aw__eq" id="il-aw-eq" width="520" height="88" aria-hidden="true"></canvas>' +
      '<div class="il-aw__track">' +
        '<span class="il-aw__track-name">Cyberpunk</span>' +
        '<span class="il-aw__tuning">A4 = 432 Hz</span>' +
      '</div>' +
      '<div class="il-aw__controls">' +
        '<button class="il-aw__btn" data-aw="prev" aria-label="Previous style" title="Previous style">' +
          '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M19 20 9 12l10-8v16zM7 4H5v16h2V4z"/></svg>' +
        '</button>' +
        '<button class="il-aw__btn il-aw__btn--play" data-aw="play" aria-label="Play / pause" title="Play / pause">' +
          '<svg data-aw-icon="play" width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>' +
          '<svg data-aw-icon="pause" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="display:none"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>' +
        '</button>' +
        '<button class="il-aw__btn" data-aw="next" aria-label="Next style" title="Next style">' +
          '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="m5 4 10 8-10 8V4zm12 0h2v16h-2V4z"/></svg>' +
        '</button>' +
      '</div>' +
      '<div class="il-aw__vol">' +
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M11 5 6 9H2v6h4l5 4V5z"/></svg>' +
        '<input type="range" data-aw="vol" min="0" max="100" value="70" aria-label="Volume">' +
      '</div>' +
      '<div class="il-aw__themes">' +
        '<select data-aw="theme" aria-label="Choose ambient style"></select>' +
      '</div>';

    root.appendChild(full);
    document.body.appendChild(root);
    return root;
  }

  function init() {
    if (!window.ILAmbient) { setTimeout(init, 500); return; }

    var root = document.getElementById(WIDGET_ID) || buildWidget();
    var $ = function (sel) { return root.querySelector(sel); };
    var $$ = function (sel) { return root.querySelectorAll(sel); };

    var eqCanvas = $('#il-aw-eq');
    var eqMini = $('#il-aw-eq-mini');
    var eqCtx = eqCanvas.getContext('2d');
    var eqMiniCtx = eqMini.getContext('2d');

    // ---- State ----
    var theme = lsGet(LS_THEME) || detectTheme() || 'cyberpunk';
    var volume = parseFloat(lsGet(LS_VOL));
    volume = isNaN(volume) ? 0.7 : Math.min(1, Math.max(0, volume));
    var muted = lsGet(LS_MUTED) === '1';
    // Mobile default: start as the compact mini-player unless the user has
    // an explicit saved preference (keeps it out of the way on phones).
    var minPref = lsGet(LS_MIN);
    var minimized = minPref === '1';
    if (minPref === null) {
      try { minimized = window.matchMedia('(max-width: 640px)').matches; }
      catch (e) { minimized = false; }
    }

    // ---- Theme selector ----
    var sel = $('[data-aw="theme"]');
    THEME_ORDER.forEach(function (name) {
      if (!window.ILAmbient.themes[name]) return;
      var opt = document.createElement('option');
      opt.value = name;
      opt.textContent = themeLabel(name);
      sel.appendChild(opt);
    });
    sel.value = theme;

    // ---- Apply initial state ----
    function applyTheme(name, autoplay) {
      theme = name;
      lsSet(LS_THEME, name);
      sel.value = name;
      var art = root.querySelector('.il-aw__art');
      art.setAttribute('data-art', name);
      // Crossfade: briefly dim, then restore.
      art.style.opacity = '0.25';
      setTimeout(function () { art.style.opacity = '1'; }, 220);
      root.querySelector('.il-aw__art-label').textContent = themeLabel(name);
      root.querySelector('.il-aw__track-name').textContent = themeLabel(name);
      if (autoplay !== false) {
        try { window.ILAmbient.play(name); } catch (e) {}
      } else {
        // Don't restart/crossfade when the engine is already on this theme
        // (e.g. SPA navigation rebuild) — just sync the saved preference.
        var cur = null;
        try { cur = window.ILAmbient.currentTheme(); } catch (e) {}
        if (cur !== name) { try { window.ILAmbient.setTheme(name); } catch (e) {} }
      }
      syncPlayIcon();
    }

    // ---- Controls ----
    function syncPlayIcon() {
      var playing = false;
      try { playing = window.ILAmbient.isPlaying(); } catch (e) {}
      var showPlay = !playing;
      $$('[data-aw-icon="play"]').forEach(function (el) {
        el.style.display = showPlay ? '' : 'none';
      });
      $$('[data-aw-icon="pause"]').forEach(function (el) {
        el.style.display = showPlay ? 'none' : '';
      });
      root.classList.toggle('il-aw--playing', playing);
    }

    $('[data-aw="play"]').addEventListener('click', function () {
      try { window.ILAmbient.toggle(); } catch (e) {}
      setTimeout(syncPlayIcon, 300);
    });

    $('[data-aw="next"]').addEventListener('click', function () {
      var i = THEME_ORDER.indexOf(theme);
      var next = THEME_ORDER[(i + 1) % THEME_ORDER.length];
      applyTheme(next, true);
    });

    $('[data-aw="prev"]').addEventListener('click', function () {
      var i = THEME_ORDER.indexOf(theme);
      var prev = THEME_ORDER[(i - 1 + THEME_ORDER.length) % THEME_ORDER.length];
      applyTheme(prev, true);
    });

    sel.addEventListener('change', function () {
      applyTheme(sel.value, true);
    });

    var volInput = $('[data-aw="vol"]');
    volInput.value = Math.round(volume * 100);
    if (muted) volInput.value = 0;
    volInput.addEventListener('input', function () {
      var v = parseInt(volInput.value, 10) / 100;
      muted = (v === 0);
      lsSet(LS_MUTED, muted ? '1' : '0');
      try { window.ILAmbient.setVolume(v); } catch (e) {}
      lsSet(LS_VOL, String(v));
    });

    $('[data-aw="mute"]').addEventListener('click', function () {
      muted = !muted;
      lsSet(LS_MUTED, muted ? '1' : '0');
      try { window.ILAmbient.setVolume(muted ? 0 : volume); } catch (e) {}
      volInput.value = muted ? 0 : Math.round(volume * 100);
    });

    // Minimize / expand.
    function setMinimized(min) {
      minimized = min;
      lsSet(LS_MIN, min ? '1' : '0');
      root.classList.toggle('il-aw--min', min);
    }
    $('[data-aw="min"]').addEventListener('click', function (e) {
      e.stopPropagation();
      setMinimized(true);
    });
    root.querySelector('.il-aw__mini').addEventListener('click', function () {
      setMinimized(false);
    });
    if (minimized) root.classList.add('il-aw--min');

    // ---- Draggable ----
    (function makeDraggable() {
      var pos = null;
      try { pos = JSON.parse(lsGet(LS_POS) || 'null'); } catch (e) {}
      if (pos && typeof pos.x === 'number' && typeof pos.y === 'number') {
        root.style.left = pos.x + 'px';
        root.style.top = pos.y + 'px';
        root.style.right = 'auto';
        root.style.bottom = 'auto';
      }
      var dragging = false, sx, sy, ox, oy;
      root.querySelectorAll('.il-aw__drag').forEach(function (handle) {
        handle.addEventListener('pointerdown', function (e) {
          // Don't start drag when clicking the mini-expand (that's a click).
          if (root.classList.contains('il-aw--min')) return;
          dragging = true;
          sx = e.clientX; sy = e.clientY;
          var r = root.getBoundingClientRect();
          ox = r.left; oy = r.top;
          handle.setPointerCapture(e.pointerId);
          e.preventDefault();
        });
        handle.addEventListener('pointermove', function (e) {
          if (!dragging) return;
          var nx = Math.max(0, Math.min(window.innerWidth - 80, ox + e.clientX - sx));
          var ny = Math.max(0, Math.min(window.innerHeight - 80, oy + e.clientY - sy));
          root.style.left = nx + 'px';
          root.style.top = ny + 'px';
          root.style.right = 'auto';
          root.style.bottom = 'auto';
        });
        handle.addEventListener('pointerup', function () {
          if (!dragging) return;
          dragging = false;
          var r = root.getBoundingClientRect();
          lsSet(LS_POS, JSON.stringify({ x: Math.round(r.left), y: Math.round(r.top) }));
        });
      });
    })();

    // ---- Live equalizer (device-aware) ----
    var freqData = null;
    // Scale EQ bar count by device capability: fewer bars on mobile/low-core.
    var EQ_BARS = 28;
    var EQ_BARS_MINI = 10;
    try {
      var cores = window.navigator.hardwareConcurrency || 4;
      var isMobile = window.matchMedia('(max-width: 640px)').matches;
      if (isMobile || cores <= 4) { EQ_BARS = 16; EQ_BARS_MINI = 8; }
    } catch (e) {}
    function drawEQ(canvas, g, w, h, bars) {
      g.clearRect(0, 0, w, h);
      var n = bars || 24;
      var bw = w / n;
      for (var i = 0; i < n; i++) {
        var v = 0;
        if (freqData) {
          // Map bar index across the available bins (log-ish feel).
          var bin = Math.floor(Math.pow(i / n, 1.4) * freqData.length);
          v = freqData[Math.min(bin, freqData.length - 1)] / 255;
        } else {
          // Idle shimmer when no audio.
          v = 0.04 + 0.03 * Math.sin(Date.now() / 700 + i * 0.7);
        }
        var bh = Math.max(2, v * h * 0.92);
        var x = i * bw + bw * 0.18;
        var grad = g.createLinearGradient(0, h, 0, h - bh);
        grad.addColorStop(0, '#c9a227');
        grad.addColorStop(1, '#7dd3fc');
        g.fillStyle = grad;
        g.fillRect(x, h - bh, bw * 0.64, bh);
      }
    }
    (function eqLoop() {
      // Stop stale loops from a previous document (SPA navigation rebuild).
      if (MY_GEN !== window.__ilAwGen) return;
      if (!document.contains(eqCanvas)) return;
      try {
        if (window.ILAmbient.getFrequencyData) {
          freqData = window.ILAmbient.getFrequencyData();
        }
      } catch (e) { freqData = null; }
      drawEQ(eqCanvas, eqCtx, eqCanvas.width, eqCanvas.height, EQ_BARS);
      drawEQ(eqMini, eqMiniCtx, eqMini.width, eqMini.height, EQ_BARS_MINI);
      requestAnimationFrame(eqLoop);
    })();

    // ---- Armed autoplay with widget theme ----
    try {
      if (window.ILAmbient.arm) window.ILAmbient.arm(theme);
    } catch (e) {}
    // Apply saved volume/mute.
    try { window.ILAmbient.setVolume(muted ? 0 : volume); } catch (e) {}

    // Sync play icon periodically (theme may start via first gesture).
    // Clear any interval left over from a previous document (SPA rebuild).
    try { if (window.__ilAwSyncT) clearInterval(window.__ilAwSyncT); } catch (e) {}
    window.__ilAwSyncT = setInterval(function () {
      if (MY_GEN !== window.__ilAwGen) { clearInterval(window.__ilAwSyncT); return; }
      if (!document.contains(root)) { clearInterval(window.__ilAwSyncT); return; }
      syncPlayIcon();
    }, 1200);
    setTimeout(syncPlayIcon, 800);
    applyTheme(theme, false); // set visuals without forcing play
  }

  function detectTheme() {
    var body = document.body;
    if (!body) return null;
    var t = body.getAttribute('data-il-theme');
    if (t) return t;
    var slug = body.getAttribute('data-audio-topic') || body.getAttribute('data-topic-theme');
    if (slug && window.ILAmbient && window.ILAmbient.topicTheme) {
      try { return window.ILAmbient.topicTheme(slug); } catch (e) {}
    }
    return null;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    setTimeout(init, 60);
  }
})();
