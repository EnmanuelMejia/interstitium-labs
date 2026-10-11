/* =====================================================================
 * Interstitium Labs — Noah AI Voice + Model Selector (2026-10-09)
 *
 * Adds to the existing Noah AI widget (noah-ai.js):
 *  1. VOICE INPUT — microphone button using Web Speech API (SpeechRecognition).
 *     Falls back gracefully where unsupported.
 *  2. VOICE OUTPUT — speaker toggle using speechSynthesis. Noah's replies
 *     are read aloud when enabled.
 *  3. MODEL SELECTOR — dropdown populated from GET /api/noah/models.
 *     Lets the user pick the Workers AI open-source model.
 *  4. MODE TOGGLE — Tutor (Socratic, course-aware) vs General (open
 *     ChatGPT-like assistant). Sent as `mode` in the /api/noah POST body.
 *
 * This file loads after noah-ai.js and patches the widget at build time.
 * It does NOT modify noah-ai.js itself.
 * ===================================================================== */
(function (g) {
  'use strict';

  var VOICE_CSS = [
    '#noah-voice-btn{background:rgba(34,211,238,.08);border:1px solid rgba(34,211,238,.3);border-radius:12px;',
    'color:#a5e8fc;cursor:pointer;font-size:18px;padding:0 12px;min-height:44px;}',
    '#noah-voice-btn:hover{background:rgba(34,211,238,.18);}',
    '#noah-voice-btn.listening{background:rgba(239,68,68,.2);border-color:rgba(239,68,68,.6);color:#fca5a5;',
    'animation:noah-pulse 1.2s ease-in-out infinite;}',
    '@keyframes noah-pulse{0%,100%{opacity:1;}50%{opacity:.55;}}',
    '#noah-voice-btn:disabled{opacity:.4;cursor:default;}',
    '#noah-speak-btn{background:none;border:none;color:#7d8ea3;font-size:18px;cursor:pointer;padding:4px;line-height:1;}',
    '#noah-speak-btn:hover{color:#f2e8c9;}',
    '#noah-speak-btn.on{color:#34d399;}',
    '#noah-model-row{display:flex;gap:8px;padding:8px 14px;border-bottom:1px solid rgba(255,255,255,.06);',
    'background:rgba(0,0,0,.25);align-items:center;}',
    '#noah-mode-toggle{display:flex;background:rgba(255,255,255,.06);border-radius:999px;padding:2px;gap:2px;}',
    '#noah-mode-toggle button{border:none;background:none;color:#7d8ea3;font-size:11.5px;padding:5px 11px;',
    'border-radius:999px;cursor:pointer;letter-spacing:.03em;}',
    '#noah-mode-toggle button.active{background:rgba(212,175,55,.25);color:#f2e8c9;font-weight:600;}',
    '#noah-model-select{flex:1;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.15);',
    'border-radius:8px;color:#dbe4ee;font-size:11.5px;padding:5px 8px;max-width:170px;}',
    '#noah-model-select option{background:#0d141d;color:#dbe4ee;}'
  ].join('\n');

  var state = {
    voiceOut: false,
    listening: false,
    recognition: null,
    model: null,
    mode: 'general',
    models: [],
  };

  /* ---------- Speech synthesis (TTS output) ---------- */

  function speak(text) {
    if (!state.voiceOut || !('speechSynthesis' in g)) return;
    try {
      g.speechSynthesis.cancel();
      // Strip markdown for cleaner speech
      var clean = String(text || '')
        .replace(/```[\s\S]*?```/g, ' code block ')
        .replace(/`([^`]+)`/g, '$1')
        .replace(/\*\*([^*]+)\*\*/g, '$1')
        .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
        .replace(/#{1,6}\s/g, '')
        .replace(/\n{2,}/g, '. ');
      var u = new SpeechSynthesisUtterance(clean.slice(0, 2000));
      u.rate = 1.0;
      u.pitch = 1.0;
      g.speechSynthesis.speak(u);
    } catch (e) {}
  }

  function stopSpeak() {
    try { if ('speechSynthesis' in g) g.speechSynthesis.cancel(); } catch (e) {}
    try { if (g.__noahStopServerAudio) g.__noahStopServerAudio(); } catch (e) {}
  }

  /* ---------- Speech recognition (STT input) ---------- */

  function sttSupported() {
    return ('SpeechRecognition' in g) || ('webkitSpeechRecognition' in g);
  }

  function recorderSupported() {
    return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia &&
      typeof MediaRecorder !== 'undefined');
  }

  /* Server transcription via POST /api/ai/transcribe — NVIDIA Parakeet
     (parakeet-tdt-0.6b-v3) when a self-hosted upstream is configured,
     Workers AI Whisper otherwise. Takes a Blob, resolves transcript
     text ('' on failure). Audio is sent once, never stored. */
  function transcribeBlob(blob, opts) {
    opts = opts || {};
    return new Promise(function (resolve) {
      var rd = new FileReader();
      rd.onload = function () {
        var b64 = String(rd.result || '').split(',')[1] || '';
        if (!b64) { resolve(''); return; }
        fetch('/api/ai/transcribe', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ audio: b64, language: opts.language || 'auto' }),
        }).then(function (r) { return r.json(); }).then(function (d) {
          resolve(d && d.text ? String(d.text) : '');
        }).catch(function () { resolve(''); });
      };
      rd.onerror = function () { resolve(''); };
      rd.readAsDataURL(blob);
    });
  }

  /* Push-to-talk via MediaRecorder -> /api/ai/transcribe. Used where
     SpeechRecognition is unavailable (Firefox, some WebViews). */
  function toggleRecordListen(btn, inputEl, sendFn) {
    if (state.listening) {
      if (toggleListen._stopRec) toggleListen._stopRec();
      return;
    }
    if (!recorderSupported()) return;
    navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
      var mime = '';
      ['audio/webm;codecs=opus', 'audio/webm', 'audio/mp4', 'audio/ogg'].forEach(function (m) {
        if (!mime && MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(m)) mime = m;
      });
      var mr = new MediaRecorder(stream, mime ? { mimeType: mime } : undefined);
      var chunks = [];
      state.listening = true;
      btn.classList.add('listening');
      btn.setAttribute('aria-label', 'Stop listening');
      mr.ondataavailable = function (e) { if (e.data && e.data.size) chunks.push(e.data); };
      mr.onstop = function () {
        stream.getTracks().forEach(function (t) { t.stop(); });
        state.listening = false;
        btn.classList.remove('listening');
        btn.setAttribute('aria-label', 'Voice input');
        var blob = new Blob(chunks, { type: mr.mimeType || 'audio/webm' });
        if (inputEl) inputEl.value = 'Transcribing…';
        transcribeBlob(blob, {}).then(function (text) {
          if (text && text.trim()) {
            if (inputEl) inputEl.value = '';
            sendFn(text.trim());
          } else if (inputEl) {
            inputEl.value = '';
          }
        });
      };
      toggleListen._stopRec = function () { try { mr.stop(); } catch (e) {} };
      mr.start(250);
    }).catch(function () { /* mic denied: no-op, button stays available */ });
  }

  function toggleListen(btn, inputEl, sendFn) {
    if (state.listening) {
      if (toggleListen._stop) toggleListen._stop();
      if (toggleListen._stopRec) toggleListen._stopRec();
      return;
    }
    if (!sttSupported()) { toggleRecordListen(btn, inputEl, sendFn); return; }
    var SR = g.SpeechRecognition || g.webkitSpeechRecognition;
    var rec = new SR();
    rec.lang = 'en-US';
    rec.interimResults = true;
    rec.continuous = false;
    rec.maxAlternatives = 1;
    state.recognition = rec;
    state.listening = true;
    btn.classList.add('listening');
    btn.setAttribute('aria-label', 'Stop listening');

    var finalTranscript = '';
    rec.onresult = function (e) {
      var interim = '';
      for (var i = e.resultIndex; i < e.results.length; i++) {
        var t = e.results[i][0].transcript;
        if (e.results[i].isFinal) finalTranscript += t;
        else interim += t;
      }
      inputEl.value = finalTranscript + interim;
    };
    rec.onerror = function () { stopListen(); };
    rec.onend = function () {
      var wasListening = state.listening;
      stopListen();
      // Auto-send the transcribed text
      if (wasListening && finalTranscript.trim()) {
        inputEl.value = finalTranscript.trim();
        sendFn(finalTranscript.trim());
        inputEl.value = '';
      }
    };
    try { rec.start(); } catch (e) { stopListen(); }

    function stopListen() {
      state.listening = false;
      if (btn) { btn.classList.remove('listening'); btn.setAttribute('aria-label', 'Voice input'); }
      try { if (state.recognition) state.recognition.stop(); } catch (e) {}
      state.recognition = null;
    }
    // Expose for the outer toggle
    toggleListen._stop = stopListen;
  }

  /* ---------- Model fetching ---------- */

  function fetchModels(selectEl) {
    fetch('/api/noah/models', { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!d || !d.ok || !Array.isArray(d.models)) return;
        state.models = d.models;
        state.model = d.default || d.models[0].id;
        d.models.forEach(function (m) {
          var o = document.createElement('option');
          o.value = m.id;
          o.textContent = m.label;
          if (m.id === state.model) o.selected = true;
          selectEl.appendChild(o);
        });
      })
      .catch(function () {});
  }

  /* ---------- Patch the widget ---------- */

  function patch() {
    // Wait for the widget to exist
    var panel = document.getElementById('noah-panel');
    if (!panel) {
      setTimeout(patch, 500);
      return;
    }

    var style = document.createElement('style');
    style.textContent = VOICE_CSS;
    document.head.appendChild(style);

    var head = panel.querySelector('#noah-head');
    var form = panel.querySelector('#noah-form');
    var input = panel.querySelector('#noah-input');
    if (!head || !form || !input) {
      setTimeout(patch, 500);
      return;
    }

    // 1. Speaker toggle in header (before close button)
    var closeBtn = panel.querySelector('#noah-close');
    var speakBtn = document.createElement('button');
    speakBtn.id = 'noah-speak-btn';
    speakBtn.type = 'button';
    speakBtn.innerHTML = '🔊';
    speakBtn.setAttribute('aria-label', 'Toggle voice responses');
    speakBtn.title = 'Voice responses on/off';
    speakBtn.addEventListener('click', function () {
      state.voiceOut = !state.voiceOut;
      speakBtn.classList.toggle('on', state.voiceOut);
      speakBtn.innerHTML = state.voiceOut ? '🔊' : '🔇';
      if (!state.voiceOut) stopSpeak();
      try { localStorage.setItem('noah-voice-out', state.voiceOut ? '1' : '0'); } catch (e) {}
    });
    // Restore preference
    try {
      if (localStorage.getItem('noah-voice-out') === '1') {
        state.voiceOut = true;
        speakBtn.classList.add('on');
      } else {
        speakBtn.innerHTML = '🔇';
      }
    } catch (e) { speakBtn.innerHTML = '🔇'; }
    head.insertBefore(speakBtn, closeBtn);

    // 2. Model + mode row (between header and messages)
    var msgs = panel.querySelector('#noah-msgs');
    var modelRow = document.createElement('div');
    modelRow.id = 'noah-model-row';

    var modeToggle = document.createElement('div');
    modeToggle.id = 'noah-mode-toggle';
    var tutorBtn = document.createElement('button');
    tutorBtn.type = 'button';
    tutorBtn.textContent = 'Tutor';
    tutorBtn.className = 'active';
    var genBtn = document.createElement('button');
    genBtn.type = 'button';
    genBtn.textContent = 'General';
    tutorBtn.addEventListener('click', function () {
      state.mode = 'tutor';
      tutorBtn.className = 'active';
      genBtn.className = '';
      try { localStorage.setItem('noah-mode', 'tutor'); } catch (e) {}
    });
    genBtn.addEventListener('click', function () {
      state.mode = 'general';
      genBtn.className = 'active';
      tutorBtn.className = '';
      try { localStorage.setItem('noah-mode', 'general'); } catch (e) {}
    });
    try {
      if (localStorage.getItem('noah-mode') === 'general') genBtn.click();
    } catch (e) {}
    modeToggle.appendChild(tutorBtn);
    modeToggle.appendChild(genBtn);

    var modelSelect = document.createElement('select');
    modelSelect.id = 'noah-model-select';
    modelSelect.setAttribute('aria-label', 'AI model');
    modelSelect.title = 'Choose the AI model';
    modelSelect.addEventListener('change', function () {
      state.model = modelSelect.value;
      try { localStorage.setItem('noah-model', state.model); } catch (e) {}
    });
    try {
      var saved = localStorage.getItem('noah-model');
      if (saved) state.model = saved;
    } catch (e) {}

    modelRow.appendChild(modeToggle);
    modelRow.appendChild(modelSelect);
    panel.insertBefore(modelRow, msgs);
    fetchModels(modelSelect);

    // 3. Mic button in form (before send button)
    var sendBtn = panel.querySelector('#noah-send');
    var micBtn = document.createElement('button');
    micBtn.id = 'noah-voice-btn';
    micBtn.type = 'button';
    micBtn.innerHTML = '🎤';
    micBtn.setAttribute('aria-label', 'Voice input');
    micBtn.title = 'Speak your message';
    if (!sttSupported()) {
      micBtn.disabled = true;
      micBtn.title = 'Voice input not supported in this browser';
    } else {
      micBtn.addEventListener('click', function () {
        // Get the widget's sendText via the IL namespace if available
        toggleListen(micBtn, input, function (text) {
          // Simulate form submission with the transcribed text
          var evt = new Event('submit', { cancelable: true });
          // Set input value first (already done in onend), then submit
          form.dispatchEvent(evt);
        });
      });
    }
    form.insertBefore(micBtn, sendBtn);

    // 4. Speak Noah's replies: hook into message rendering via MutationObserver
    var observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (m) {
        m.addedNodes.forEach(function (node) {
          if (node.nodeType === 1 && node.classList &&
              node.classList.contains('noah-msg') && node.classList.contains('noah')) {
            // Extract text content (strip HTML)
            var text = node.textContent || '';
            // Don't speak the greeting on load (only speak after user interaction)
            if (state.voiceOut && document.hasFocus()) {
              // Small delay to let streaming finish
              setTimeout(function () { speak(node.textContent || ''); }, 1500);
            }
          }
        });
      });
    });
    observer.observe(msgs, { childList: true });

    // 5. Inject model+mode into /api/noah requests via fetch patch
    var origFetch = g.fetch;
    g.fetch = function (url, opts) {
      if (typeof url === 'string' && url.indexOf('/api/noah') === 0 &&
          !url.startsWith('/api/noah-') && opts && opts.method === 'POST' && opts.body) {
        try {
          var body = JSON.parse(opts.body);
          if (state.model) body.model = state.model;
          body.mode = state.mode;
          opts = Object.assign({}, opts, { body: JSON.stringify(body) });
        } catch (e) {}
      }
      return origFetch.call(this, url, opts);
    };
  }

  // Start patching when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(patch, 1000); });
  } else {
    setTimeout(patch, 1000);
  }

  // Public API
  g.IL = g.IL || {};
  g.IL.noahVoice = {
    speak: speak,
    stop: stopSpeak,
    transcribeBlob: transcribeBlob,
    recorderSupported: recorderSupported,
    get state() { return { voiceOut: state.voiceOut, model: state.model, mode: state.mode }; },
    setModel: function (id) { state.model = id; },
    setMode: function (m) { if (m === 'tutor' || m === 'general') state.mode = m; },
  };
})(window);

/* 2026-10-09: stopSpeak also silences server TTS */
