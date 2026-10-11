/* =====================================================================
 * Interstitium Labs — Verbal Mock Interview (2026-10-11)
 *
 * Noah or Genesis interview YOU — out loud. Spoken questions (server
 * neural TTS via /api/noah/tts), spoken answers (browser
 * SpeechRecognition with live interim captions; MediaRecorder ->
 * /api/ai/transcribe — Parakeet ASR endpoint — where SR is
 * unavailable), adaptive
 * follow-ups from the parameterized interview engine
 * (POST /api/noah/interview), live delivery metrics (pace, fillers,
 * answer length), and a full coached debrief when you finish.
 *
 * For ANY visitor: the setup asks role, company (optional), level and
 * length. Nothing about any specific person is baked in. Transcripts
 * and settings live only in this browser's localStorage.
 *
 * Entry points: the /noah/ header button (#miBtn) or ?mode=interview,
 * plus a deep-link button injected into the floating widget panel.
 * Public API: window.ILMockInterview.open()
 *
 * 2026-10-11 (gap-closing): setup carries a plain-language voice
 * privacy notice — AI-provider transcription, in-memory processing,
 * audio never stored or sold, transcripts on-device only.
 * ===================================================================== */
(function (g) {
  'use strict';

  var SETTINGS_KEY = 'il-mock-interview-settings-v1';
  var SESSIONS_KEY = 'il-mock-interviews-v1';
  var ABS = 'https://interstitiumlabs.dev';

  var ROLE_PRESETS = [
    'IT Infrastructure Engineer', 'Network Engineer', 'Systems Administrator',
    'IT Support Specialist', 'Solutions Engineer', 'SOC Analyst',
    'Data Analyst', 'Software Engineer'
  ];
  var LEVELS = ['Entry-level', 'Junior', 'Mid-level', 'Senior', 'Lead'];
  var VOICES = [
    { id: 'narrator', label: 'Narrator — authoritative' },
    { id: 'guide',    label: 'Guide — warm' },
    { id: 'scholar',  label: 'Scholar — measured' },
    { id: 'sage',     label: 'Sage — deep' },
    { id: 'spark',    label: 'Spark — energetic' }
  ];
  var FILLER_RE = /\b(um+|uh+|uhm|erm|like|you know|basically|actually|literally|i mean|sort of|kind of)\b/gi;

  /* ---------------- settings / tutor ---------------- */
  function loadSettings() {
    var d = { voice: '', speed: 1.0 };
    try {
      var raw = localStorage.getItem(SETTINGS_KEY);
      if (raw) { var p = JSON.parse(raw); if (p && typeof p === 'object') { d.voice = p.voice || ''; d.speed = Math.max(0.8, Math.min(1.3, Number(p.speed) || 1)); } }
    } catch (e) {}
    return d;
  }
  function saveSettings() { try { localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings)); } catch (e) {} }
  var settings = loadSettings();

  function currentTutor() {
    try {
      var p = JSON.parse(localStorage.getItem('il-noah-profile') || '{}');
      if (p && p.avatar === 'genesis') return 'genesis';
    } catch (e) {}
    return 'noah';
  }
  function tutorName() { return session.tutor === 'genesis' ? 'Genesis' : 'Noah'; }
  function tutorVideo() { return ABS + '/assets/noah/' + (session.tutor === 'genesis' ? 'genesis' : 'noah') + '-avatar-animated.mp4'; }
  function defaultVoice() {
    if (settings.voice) return settings.voice;
    return session.tutor === 'genesis' ? 'guide' : 'narrator';
  }

  /* ---------------- session state ---------------- */
  var session = null;
  function newSession() {
    return {
      id: 'mi' + Date.now().toString(36),
      tutor: currentTutor(),
      setup: null,               // { role, company, level, length }
      targetQuestions: 8,
      questionsAsked: 0,
      phase: 'opening',          // opening | main | candidate | closing
      history: [],               // { role: 'interviewer'|'candidate', content }
      metrics: [],               // per candidate answer in main phases
      startedAt: 0, timerId: null, elapsedSec: 0,
      debrief: '',
      busy: false, over: false
    };
  }

  /* ---------------- styles ---------------- */
  var CSS = [
    '#mi-overlay{position:fixed;inset:0;z-index:300;background:rgba(4,6,10,.92);backdrop-filter:blur(10px);display:flex;align-items:center;justify-content:center;padding:14px}',
    '#mi-overlay[hidden]{display:none}',
    '.mi-card{background:#0a0d13;border:1px solid rgba(201,162,39,.25);border-radius:18px;width:min(880px,100%);max-height:94dvh;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.6)}',
    '.mi-head{display:flex;align-items:center;gap:12px;padding:12px 18px;border-bottom:1px solid rgba(255,255,255,.08)}',
    '.mi-head h2{margin:0;font-size:1.02rem;letter-spacing:.04em;flex:1}',
    '.mi-head h2 span{color:#c9a227}',
    '.mi-pill{font-size:.72rem;color:#8b93a5;border:1px solid rgba(255,255,255,.12);border-radius:999px;padding:.28rem .7rem;white-space:nowrap}',
    '.mi-pill.live{color:#40e0d0;border-color:rgba(64,224,208,.45)}',
    '.mi-x{background:transparent;border:1px solid rgba(255,255,255,.14);color:#8b93a5;border-radius:9px;width:34px;height:34px;cursor:pointer;font-size:1rem}',
    '.mi-x:hover{color:#fff}',
    '.mi-body{overflow-y:auto;padding:18px}',
    '.mi-body h3{margin:.2em 0 .6em;font-size:1rem;color:#e9edf5}',
    '.mi-body p{color:#8b93a5;line-height:1.55;font-size:.9rem}',
    '.mi-label{display:block;font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:#5d6577;margin:14px 0 6px}',
    '.mi-input,.mi-select{width:100%;background:#0d1119;border:1px solid rgba(255,255,255,.12);border-radius:10px;color:#e9edf5;padding:.65rem .8rem;font-size:.92rem;font-family:inherit}',
    '.mi-input:focus,.mi-select:focus{outline:none;border-color:rgba(201,162,39,.6)}',
    '.mi-chips{display:flex;flex-wrap:wrap;gap:7px}',
    '.mi-chip{background:#11161f;border:1px solid rgba(255,255,255,.12);color:#c7cede;border-radius:999px;padding:.42rem .85rem;font-size:.8rem;cursor:pointer}',
    '.mi-chip:hover{border-color:#c9a227;color:#c9a227}',
    '.mi-chip.on{background:rgba(201,162,39,.16);border-color:#c9a227;color:#e8c34a}',
    '.mi-row{display:flex;gap:12px;flex-wrap:wrap}.mi-row>div{flex:1;min-width:180px}',
    '.mi-range{width:100%;accent-color:#c9a227}',
    '.mi-start{margin-top:22px;width:100%;background:linear-gradient(135deg,#e8c34a,#c9a227);color:#111;border:0;border-radius:12px;padding:.85rem;font-size:1rem;font-weight:700;cursor:pointer;letter-spacing:.02em}',
    '.mi-start:disabled{opacity:.4;cursor:default}',
    '.mi-ghost{background:transparent;border:1px solid rgba(255,255,255,.16);color:#c7cede;border-radius:10px;padding:.6rem 1rem;font-size:.86rem;cursor:pointer}',
    '.mi-ghost:hover{border-color:#c9a227;color:#e8c34a}',
    '.mi-ghost.danger:hover{border-color:#f87171;color:#f87171}',
    '/* stage */',
    '.mi-stage{display:flex;flex-direction:column;align-items:center;gap:10px;padding:6px 0 2px}',
    '.mi-avatarwrap{width:132px;height:132px;border-radius:50%;overflow:hidden;position:relative;border:2px solid rgba(255,255,255,.14);transition:border-color .3s, box-shadow .3s}',
    '.mi-avatarwrap video{width:100%;height:100%;object-fit:cover;object-position:center 18%}',
    '.mi-stage[data-state="speaking"] .mi-avatarwrap{border-color:#c9a227;box-shadow:0 0 0 5px rgba(201,162,39,.18),0 0 34px rgba(201,162,39,.35);animation:miPulse 1.6s ease-in-out infinite}',
    '.mi-stage[data-state="listening"] .mi-avatarwrap{border-color:#40e0d0;box-shadow:0 0 0 5px rgba(64,224,208,.16),0 0 34px rgba(64,224,208,.32)}',
    '.mi-stage[data-state="thinking"] .mi-avatarwrap{border-color:#a78bfa;box-shadow:0 0 24px rgba(167,139,250,.3)}',
    '@keyframes miPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.025)}}',
    '.mi-statustext{font-size:.86rem;color:#c7cede;min-height:1.2em;text-align:center}',
    '.mi-statustext b{color:#e8c34a}',
    '.mi-hud{display:flex;flex-wrap:wrap;gap:7px;justify-content:center;min-height:26px}',
    '.mi-hudchip{font-size:.72rem;color:#8b93a5;background:#0d1119;border:1px solid rgba(255,255,255,.09);border-radius:999px;padding:.24rem .65rem}',
    '.mi-hudchip b{color:#e9edf5;font-weight:600}',
    '.mi-question{font-size:1.06rem;line-height:1.5;color:#e9edf5;text-align:center;max-width:640px;min-height:1.5em}',
    '.mi-interim{font-size:.88rem;color:#40e0d0;min-height:1.3em;text-align:center;max-width:640px;font-style:italic}',
    '.mi-controls{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;padding:12px 18px;border-top:1px solid rgba(255,255,255,.08)}',
    '.mi-micbtn{background:linear-gradient(135deg,#e8c34a,#c9a227);color:#111;border:0;border-radius:999px;padding:.8rem 1.6rem;font-size:.95rem;font-weight:700;cursor:pointer}',
    '.mi-micbtn:disabled{opacity:.4;cursor:default}',
    '.mi-micbtn.rec{background:linear-gradient(135deg,#f87171,#dc2626);color:#fff;animation:miPulse 1.2s infinite}',
    '.mi-log{border-top:1px solid rgba(255,255,255,.08);padding:14px 18px;overflow-y:auto;max-height:32dvh;display:flex;flex-direction:column;gap:10px}',
    '.mi-msg{font-size:.88rem;line-height:1.55;max-width:92%}',
    '.mi-msg .who{font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;color:#5d6577;display:block;margin-bottom:2px}',
    '.mi-msg.iv{align-self:flex-start;color:#dbe2ef}.mi-msg.iv .who{color:#c9a227}',
    '.mi-msg.me{align-self:flex-end;color:#9fd8d2;text-align:right}.mi-msg.me .who{color:#40e0d0}',
    '.mi-typebar{display:none;gap:8px;padding:0 18px 12px}',
    '.mi-typebar.open{display:flex}',
    '.mi-typebar input{flex:1}',
    '.mi-past{border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:12px 14px;margin-top:10px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}',
    '.mi-past .meta{flex:1;min-width:200px;font-size:.86rem;color:#c7cede}',
    '.mi-past .meta small{display:block;color:#5d6577;font-size:.74rem;margin-top:2px}',
    '.mi-debrief{font-size:.92rem;line-height:1.6;color:#dbe2ef}',
    '.mi-debrief h2{font-size:1.05rem;margin:1.1em 0 .4em;color:#e8c34a}.mi-debrief h3{color:#e9edf5}',
    '.mi-debrief p{margin:.5em 0;color:#c7cede}.mi-debrief ul{margin:.4em 0;padding-left:1.25em;color:#c7cede}.mi-debrief li{margin:.25em 0}',
    '.mi-note{font-size:.78rem;color:#5d6577;margin-top:10px;line-height:1.5}',
    '@media (max-width:640px){.mi-avatarwrap{width:104px;height:104px}.mi-question{font-size:1rem}}',
    '@media (prefers-reduced-motion:reduce){.mi-stage[data-state="speaking"] .mi-avatarwrap{animation:none}.mi-micbtn.rec{animation:none}}'
  ].join('\n');

  /* ---------------- speech out (server TTS, chunked + prefetch) ---------------- */
  var ttsDead = false;          // latch: server TTS failed -> browser voice for the session
  var speakGen = 0;             // generation counter; bump cancels pending speech
  var currentAudio = null;

  function chunkText(text) {
    var clean = String(text || '').replace(/\s+/g, ' ').trim();
    if (!clean) return [];
    var parts = clean.match(/[^.!?]+[.!?]+["')\]]*\s*|[^.!?]+$/g) || [clean];
    var chunks = [], cur = '';
    parts.forEach(function (p) {
      if (cur && (cur + p).length > 300) { chunks.push(cur.trim()); cur = ''; }
      cur += p;
    });
    if (cur.trim()) chunks.push(cur.trim());
    return chunks.length ? chunks : [clean];
  }
  function fetchTtsBlob(text, voice, speed) {
    var ctl = new AbortController();
    var to = setTimeout(function () { try { ctl.abort(); } catch (e) {} }, 20000);
    return fetch('/api/noah/tts', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text, voice: voice, speed: speed }),
      signal: ctl.signal
    }).then(function (r) {
      clearTimeout(to);
      if (!r.ok) throw new Error('tts ' + r.status);
      return r.blob();
    }).then(function (b) {
      if (!b || b.size < 800) throw new Error('tts empty');
      return (g.URL || window.URL).createObjectURL(b);
    });
  }
  function playUrl(url) {
    return new Promise(function (resolve) {
      var a = new Audio(url);
      currentAudio = a;
      var done = function () {
        try { (g.URL || window.URL).revokeObjectURL(url); } catch (e) {}
        if (currentAudio === a) currentAudio = null;
        resolve();
      };
      a._miDone = done; // stopSpeaking() settles playback explicitly (pause alone never fires onended)
      a.onended = done; a.onerror = done;
      var p = a.play();
      if (p && p.catch) p.catch(done);
    });
  }
  function synthSpeak(text, rate) {
    return new Promise(function (resolve) {
      if (!('speechSynthesis' in g)) { resolve(); return; }
      try {
        var clean = String(text).replace(/```[\s\S]*?```/g, ' code block ').replace(/[*#>`]/g, '').slice(0, 1800);
        var u = new SpeechSynthesisUtterance(clean);
        u.rate = rate || 1;
        u.onend = function () { resolve(); };
        u.onerror = function () { resolve(); };
        g.speechSynthesis.speak(u);
        // safety: never hang the interview on a stuck utterance
        setTimeout(resolve, Math.max(4000, clean.length * 130));
      } catch (e) { resolve(); }
    });
  }
  function stopSpeaking() {
    speakGen++;
    try {
      if (currentAudio) {
        var a = currentAudio; currentAudio = null;
        try { a.pause(); } catch (e) {}
        if (a._miDone) a._miDone();
      }
    } catch (e) {}
    try { if ('speechSynthesis' in g) g.speechSynthesis.cancel(); } catch (e) {}
  }
  /* Speak text; resolves when finished (or cancelled). Streams: chunk i+1
     is fetched while chunk i plays, so long questions start fast. */
  function speak(text) {
    var gen = ++speakGen;
    var voice = defaultVoice();
    var speed = settings.speed || 1;
    setStage('speaking');
    if (ttsDead || !('fetch' in g)) {
      return synthSpeak(text, speed).then(function () { if (gen === speakGen) setStage('idle'); });
    }
    var chunks = chunkText(text);
    var urls = new Array(chunks.length).fill(null);
    var fetches = chunks.map(function (c, i) {
      return fetchTtsBlob(c, voice, speed).then(function (u) { urls[i] = u; }).catch(function () { ttsDead = true; });
    });
    var chain = Promise.resolve();
    chunks.forEach(function (c, i) {
      chain = chain.then(function () {
        if (gen !== speakGen) return;
        return fetches[i].then(function () {
          if (gen !== speakGen) return;
          if (urls[i]) return playUrl(urls[i]);
          return synthSpeak(c, speed); // per-chunk fallback
        });
      });
    });
    return chain.then(function () { if (gen === speakGen) setStage('idle'); });
  }

  /* ---------------- speech in (SR primary, recorder->STT fallback) ---------------- */
  var activeRecog = null, activeRecorder = null, listeningNow = false, srDead = false;
  var srSupported = function () { return !!(g.SpeechRecognition || g.webkitSpeechRecognition); };

  function analyzeAnswer(text, seconds) {
    var words = (String(text).match(/\S+/g) || []).length;
    var fillers = (String(text).match(FILLER_RE) || []).length;
    var wpm = seconds > 4 && words > 0 ? Math.round(words / (seconds / 60)) : null;
    return { words: words, fillers: fillers, seconds: Math.round(seconds), wpm: wpm };
  }

  /* Resolve with the final transcript. onInterim(text) streams partials. */
  function listenSR(onInterim) {
    return new Promise(function (resolve) {
      var SR = g.SpeechRecognition || g.webkitSpeechRecognition;
      var rec = new SR();
      activeRecog = rec;
      rec.lang = 'en-US'; rec.continuous = true; rec.interimResults = true; rec.maxAlternatives = 1;
      var finalText = '', interim = '', heard = false, settled = false, permDenied = false;
      var t0 = Date.now(), lastResultAt = Date.now();
      var silenceTimer = setInterval(function () {
        if (heard && Date.now() - lastResultAt > 3000) finish();
        if (Date.now() - t0 > 180000) finish();
      }, 400);
      function finish() {
        if (settled) return; settled = true;
        clearInterval(silenceTimer);
        try { rec.stop(); } catch (e) {}
        activeRecog = null; listeningNow = false;
        resolve(permDenied ? PERMISSION_DENIED : (finalText + ' ' + interim).replace(/\s+/g, ' ').trim());
      }
      rec.onresult = function (ev) {
        lastResultAt = Date.now();
        interim = '';
        for (var i = ev.resultIndex; i < ev.results.length; i++) {
          var r = ev.results[i];
          if (r.isFinal) finalText += r[0].transcript + ' ';
          else interim += r[0].transcript;
        }
        if (finalText || interim) heard = true;
        if (onInterim) onInterim((finalText + ' ' + interim).replace(/\s+/g, ' ').trim());
      };
      rec.onerror = function (ev) {
        if (ev.error === 'not-allowed' || ev.error === 'service-not-allowed') { permDenied = true; finish(); }
        if (ev.error === 'network' || ev.error === 'audio-capture') { srDead = true; finish(); }
        // 'no-speech' / 'aborted' etc: keep listening via silence logic; onend settles
      };
      rec.onend = function () { if (!settled) finish(); };
      rec._miFinish = finish;
      try { rec.start(); listeningNow = true; } catch (e) { finish(); }
    });
  }
  var PERMISSION_DENIED = '\u0001MI_PERM_DENIED';

  function listenRecorder(onInterim) {
    return new Promise(function (resolve) {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || typeof MediaRecorder === 'undefined') {
        resolve(PERMISSION_DENIED); return;
      }
      navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
        var mime = '';
        ['audio/webm;codecs=opus', 'audio/webm', 'audio/mp4', 'audio/ogg'].forEach(function (m) {
          if (!mime && MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(m)) mime = m;
        });
        var mr = new MediaRecorder(stream, mime ? { mimeType: mime } : undefined);
        activeRecorder = { mr: mr, stream: stream, resolve: resolve };
        var chunks = [];
        mr.ondataavailable = function (e) { if (e.data && e.data.size) chunks.push(e.data); };
        mr.onstop = function () {
          stream.getTracks().forEach(function (t) { t.stop(); });
          var blob = new Blob(chunks, { type: mr.mimeType || 'audio/webm' });
          var rd = new FileReader();
          rd.onload = function () {
            var b64 = String(rd.result || '').split(',')[1] || '';
            if (!b64) { resolve(''); return; }
            if (onInterim) onInterim('Transcribing…');
            fetch('/api/ai/transcribe', {
              method: 'POST', headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ audio: b64, language: 'en' })
            }).then(function (r) { return r.json(); }).then(function (d) {
              resolve(d && d.text ? String(d.text) : '');
            }).catch(function () { resolve(''); });
          };
          rd.onerror = function () { resolve(''); };
          rd.readAsDataURL(blob);
        };
        listeningNow = true;
        mr.start(250);
      }).catch(function () { resolve(PERMISSION_DENIED); });
    });
  }
  function finishListening() {
    if (activeRecog && activeRecog._miFinish) { activeRecog._miFinish(); return; }
    if (activeRecorder) {
      var ar = activeRecorder; activeRecorder = null; listeningNow = false;
      try { ar.mr.stop(); } catch (e) { ar.resolve(''); }
    }
  }
  function listen(onInterim) {
    function recorderPath() {
      return listenRecorder(onInterim).then(function (t) {
        if (t === PERMISSION_DENIED) throw new Error('perm');
        return t || '';
      });
    }
    if (srSupported() && !srDead) {
      return listenSR(onInterim).then(function (t) {
        if (t === PERMISSION_DENIED) throw new Error('perm');
        if (srDead) return recorderPath(); // SR service died mid-answer -> Whisper path
        return t || '';
      }).catch(function (e) {
        if (e && e.message === 'perm') return recorderPath();
        return '';
      });
    }
    return recorderPath();
  }

  /* ---------------- DOM ---------------- */
  var overlay = null, els = {};
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function esc(s) { return String(s == null ? '' : s); }

  function buildOverlay() {
    if (overlay) return;
    var st = document.createElement('style');
    st.textContent = CSS;
    document.head.appendChild(st);
    overlay = el('div');
    overlay.id = 'mi-overlay';
    overlay.hidden = true;
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-label', 'Verbal mock interview');
    overlay.innerHTML =
      '<div class="mi-card">' +
        '<div class="mi-head"><h2>🎙 Mock Interview · <span id="miTutorName">Noah</span></h2>' +
          '<span class="mi-pill" id="miTimer" hidden>00:00</span>' +
          '<span class="mi-pill live" id="miQCount" hidden>Q 0/8</span>' +
          '<button class="mi-x" id="miClose" type="button" aria-label="Close mock interview">✕</button></div>' +
        '<div class="mi-body" id="miBody"></div>' +
        '<div class="mi-log" id="miLog" hidden></div>' +
        '<div class="mi-typebar" id="miTypebar">' +
          '<input class="mi-input" id="miTypeInput" type="text" placeholder="Type your answer, then Send…" aria-label="Type your answer">' +
          '<button class="mi-ghost" id="miTypeSend" type="button">Send</button></div>' +
        '<div class="mi-controls" id="miControls" hidden>' +
          '<button class="mi-micbtn" id="miMainBtn" type="button" disabled>…</button>' +
          '<button class="mi-ghost" id="miTypeToggle" type="button">⌨ Type instead</button>' +
          '<button class="mi-ghost danger" id="miEnd" type="button">End interview</button></div>' +
      '</div>';
    document.body.appendChild(overlay);
    els.body = overlay.querySelector('#miBody');
    els.log = overlay.querySelector('#miLog');
    els.timer = overlay.querySelector('#miTimer');
    els.qcount = overlay.querySelector('#miQCount');
    els.controls = overlay.querySelector('#miControls');
    els.mainBtn = overlay.querySelector('#miMainBtn');
    els.typebar = overlay.querySelector('#miTypebar');
    els.typeInput = overlay.querySelector('#miTypeInput');
    overlay.querySelector('#miClose').addEventListener('click', closeInterview);
    overlay.querySelector('#miEnd').addEventListener('click', function () { endInterview(true); });
    overlay.querySelector('#miTypeToggle').addEventListener('click', function () {
      els.typebar.classList.toggle('open');
      if (els.typebar.classList.contains('open')) els.typeInput.focus();
    });
    overlay.querySelector('#miTypeSend').addEventListener('click', submitTyped);
    els.typeInput.addEventListener('keydown', function (ev) { if (ev.key === 'Enter') submitTyped(); });
    els.mainBtn.addEventListener('click', onMainBtn);
  }

  /* ---------------- stage (inside body during live session) ---------------- */
  function renderStage() {
    els.body.innerHTML =
      '<div class="mi-stage" id="miStage" data-state="idle">' +
        '<div class="mi-avatarwrap"><video id="miAvatarVid" src="' + tutorVideo() + '" autoplay loop muted playsinline preload="auto"></video></div>' +
        '<div class="mi-statustext" id="miStatus">Setting up…</div>' +
        '<div class="mi-question" id="miQuestion"></div>' +
        '<div class="mi-interim" id="miInterim"></div>' +
        '<div class="mi-hud" id="miHud"></div>' +
      '</div>';
    els.stage = els.body.querySelector('#miStage');
    els.status = els.body.querySelector('#miStatus');
    els.question = els.body.querySelector('#miQuestion');
    els.interim = els.body.querySelector('#miInterim');
    els.hud = els.body.querySelector('#miHud');
    els.log.hidden = false;
    els.log.replaceChildren();
    els.controls.hidden = false;
    els.timer.hidden = false;
    els.qcount.hidden = false;
  }
  function setStage(state) {
    if (els.stage) els.stage.setAttribute('data-state', state);
    var page = document.getElementById('noahStatusText');
    if (page) page.textContent = state === 'listening' ? 'Listening…' : state === 'speaking' ? tutorName() + ' is speaking…' : state === 'thinking' ? 'Thinking…' : 'Ready';
  }
  function setStatus(html) { if (els.status) els.status.innerHTML = html; }
  function addLog(role, text) {
    if (!els.log) return;
    var row = el('div', 'mi-msg ' + (role === 'interviewer' ? 'iv' : 'me'));
    var who = el('span', 'who', role === 'interviewer' ? tutorName() + ' · Interviewer' : 'You');
    row.appendChild(who);
    row.appendChild(document.createTextNode(text));
    els.log.appendChild(row);
    els.log.scrollTop = els.log.scrollHeight;
  }
  function hud(html) { if (els.hud) els.hud.innerHTML = html; }
  function fmtClock(sec) {
    var m = Math.floor(sec / 60), s = sec % 60;
    return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
  }
  function updateHud(last) {
    var h = '<span class="mi-hudchip">⏱ <b>' + fmtClock(session.elapsedSec) + '</b></span>' +
      '<span class="mi-hudchip">Question <b>' + Math.min(session.questionsAsked + (session.phase === 'candidate' || session.phase === 'closing' ? session.targetQuestions : 1), session.targetQuestions) + '/' + session.targetQuestions + '</b></span>';
    if (last) {
      h += '<span class="mi-hudchip">Last answer <b>' + fmtClock(last.seconds) + '</b></span>' +
        (last.wpm ? '<span class="mi-hudchip">Pace <b>' + last.wpm + ' wpm</b></span>' : '') +
        '<span class="mi-hudchip">Fillers <b>' + last.fillers + '</b></span>' +
        '<span class="mi-hudchip">Words <b>' + last.words + '</b></span>';
    }
    hud(h);
    els.qcount.textContent = 'Q ' + session.questionsAsked + '/' + session.targetQuestions;
  }

  /* ---------------- setup view ---------------- */
  function renderSetup() {
    els.log.hidden = true; els.controls.hidden = true; els.timer.hidden = true; els.qcount.hidden = true;
    els.typebar.classList.remove('open');
    var tn = overlay.querySelector('#miTutorName');
    if (tn) tn.textContent = tutorName();
    var past = loadSessions();
    var pastHtml = '';
    if (past.length) {
      pastHtml = '<h3 style="margin-top:26px">Past interviews</h3>' + past.slice(0, 6).map(function (s, i) {
        return '<div class="mi-past"><div class="meta"><b>' + esc(s.setup.role) + '</b>' +
          (s.setup.company ? ' · ' + esc(s.setup.company) : '') + ' · ' + esc(s.setup.level) +
          '<small>' + new Date(s.date).toLocaleString() + ' · ' + s.history.filter(function (m) { return m.role === 'candidate'; }).length + ' answers · with ' + (s.tutor === 'genesis' ? 'Genesis' : 'Noah') + '</small></div>' +
          '<button class="mi-ghost" data-mi-view="' + i + '" type="button">Review</button>' +
          '<button class="mi-ghost" data-mi-dl="' + i + '" type="button">Download</button></div>';
      }).join('');
    }
    els.body.innerHTML =
      '<h3>Practice out loud — like the real thing</h3>' +
      '<p>' + tutorName() + ' will interview you by voice: spoken questions, follow-ups based on what you actually say, ' +
      'and a full coached debrief at the end. Find a quiet spot and answer out loud.</p>' +
      '<span class="mi-label">Role you are interviewing for</span>' +
      '<div class="mi-chips" id="miRoleChips">' + ROLE_PRESETS.map(function (r) {
        return '<button class="mi-chip" type="button" data-role="' + esc(r) + '">' + esc(r) + '</button>';
      }).join('') + '</div>' +
      '<input class="mi-input" id="miRole" type="text" placeholder="…or type any role, e.g. IT Infrastructure Engineer" style="margin-top:10px" maxlength="120">' +
      '<div class="mi-row">' +
        '<div><span class="mi-label">Company (optional)</span><input class="mi-input" id="miCompany" type="text" placeholder="e.g. the company you are targeting" maxlength="120"></div>' +
        '<div><span class="mi-label">Level</span><select class="mi-select" id="miLevel">' +
          LEVELS.map(function (l) { return '<option' + (l === 'Mid-level' ? ' selected' : '') + '>' + l + '</option>'; }).join('') + '</select></div>' +
      '</div>' +
      '<div class="mi-row">' +
        '<div><span class="mi-label">Session length</span><select class="mi-select" id="miLength">' +
          '<option value="express">Express — about 20 minutes</option>' +
          '<option value="full">Full — about 45 minutes</option></select></div>' +
        '<div><span class="mi-label">Interviewer voice</span><select class="mi-select" id="miVoice">' +
          VOICES.map(function (v) { return '<option value="' + v.id + '"' + (v.id === defaultVoice() ? ' selected' : '') + '>' + v.label + '</option>'; }).join('') + '</select></div>' +
      '</div>' +
      '<span class="mi-label">Voice speed · <span id="miSpeedVal">' + (settings.speed || 1).toFixed(2) + '×</span></span>' +
      '<input class="mi-range" id="miSpeed" type="range" min="0.8" max="1.3" step="0.05" value="' + (settings.speed || 1) + '">' +
      '<button class="mi-start" id="miStart" type="button">Start the interview</button>' +
      '<p class="mi-note">🔒 Your voice, your business: the interviewer\u2019s questions are spoken with an AI-generated voice, and your answers are transcribed by AI speech providers (Whisper-class models) only to run this practice session. Where your browser supports it, transcription happens locally on your device instead. Audio is processed in memory \u2014 never stored, never sold, and never used to train models. Your transcript is saved only in this browser, on this device, and you can delete it any time from Past interviews.</p>' +
      pastHtml;
    var roleInput = els.body.querySelector('#miRole');
    els.body.querySelectorAll('[data-role]').forEach(function (b) {
      b.addEventListener('click', function () {
        els.body.querySelectorAll('[data-role]').forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on');
        roleInput.value = b.getAttribute('data-role');
      });
    });
    var speed = els.body.querySelector('#miSpeed');
    speed.addEventListener('input', function () {
      settings.speed = Number(speed.value);
      els.body.querySelector('#miSpeedVal').textContent = settings.speed.toFixed(2) + '×';
      saveSettings();
    });
    els.body.querySelector('#miVoice').addEventListener('change', function (ev) {
      settings.voice = ev.target.value; saveSettings();
    });
    els.body.querySelector('#miStart').addEventListener('click', function () {
      var role = roleInput.value.trim();
      if (!role) { roleInput.focus(); roleInput.style.borderColor = '#f87171'; return; }
      startSession({
        role: role,
        company: els.body.querySelector('#miCompany').value.trim(),
        level: els.body.querySelector('#miLevel').value,
        length: els.body.querySelector('#miLength').value
      });
    });
    els.body.querySelectorAll('[data-mi-view]').forEach(function (b) {
      b.addEventListener('click', function () { reviewSession(loadSessions()[Number(b.getAttribute('data-mi-view'))]); });
    });
    els.body.querySelectorAll('[data-mi-dl]').forEach(function (b) {
      b.addEventListener('click', function () { downloadSession(loadSessions()[Number(b.getAttribute('data-mi-dl'))]); });
    });
  }

  /* ---------------- persistence ---------------- */
  function loadSessions() {
    try { var d = JSON.parse(localStorage.getItem(SESSIONS_KEY) || '[]'); return Array.isArray(d) ? d : []; }
    catch (e) { return []; }
  }
  function saveSession() {
    try {
      var all = loadSessions();
      all.unshift({
        id: session.id, date: Date.now(), tutor: session.tutor, setup: session.setup,
        history: session.history, metrics: session.metrics, debrief: session.debrief
      });
      localStorage.setItem(SESSIONS_KEY, JSON.stringify(all.slice(0, 20)));
    } catch (e) {}
  }
  function downloadSession(s) {
    if (!s) return;
    var md = '# Mock interview — ' + s.setup.role + (s.setup.company ? ' at ' + s.setup.company : '') + '\n' +
      new Date(s.date).toLocaleString() + ' · Level: ' + s.setup.level + ' · Interviewer: ' + (s.tutor === 'genesis' ? 'Genesis' : 'Noah') + '\n\n## Transcript\n\n' +
      s.history.map(function (m) { return '**' + (m.role === 'interviewer' ? 'Interviewer' : 'Candidate') + ':** ' + m.content; }).join('\n\n') +
      (s.debrief ? '\n\n## Debrief\n\n' + s.debrief : '');
    var a = document.createElement('a');
    a.href = (g.URL || window.URL).createObjectURL(new Blob([md], { type: 'text/markdown' }));
    a.download = 'mock-interview-' + s.id + '.md';
    document.body.appendChild(a); a.click(); a.remove();
  }
  function reviewSession(s) {
    if (!s) return;
    els.log.hidden = true; els.controls.hidden = true;
    els.body.innerHTML = '<h3>' + esc(s.setup.role) + (s.setup.company ? ' · ' + esc(s.setup.company) : '') + '</h3>' +
      '<p>' + new Date(s.date).toLocaleString() + ' · ' + esc(s.setup.level) + '</p>' +
      '<div class="mi-log" style="border:0;max-height:38dvh;padding:0">' +
      s.history.map(function (m) {
        return '<div class="mi-msg ' + (m.role === 'interviewer' ? 'iv' : 'me') + '"><span class="who">' + (m.role === 'interviewer' ? 'Interviewer' : 'You') + '</span>' + esc(m.content) + '</div>';
      }).join('') + '</div>' +
      (s.debrief ? '<div class="mi-debrief" id="miReviewDebrief"></div>' : '<p class="mi-note">No debrief was generated for this session.</p>') +
      '<div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap"><button class="mi-ghost" id="miBackSetup" type="button">← New interview</button>' +
      '<button class="mi-ghost" id="miReviewDl" type="button">Download transcript</button></div>';
    if (s.debrief) renderMarkdown(els.body.querySelector('#miReviewDebrief'), s.debrief);
    els.body.querySelector('#miBackSetup').addEventListener('click', renderSetup);
    els.body.querySelector('#miReviewDl').addEventListener('click', function () { downloadSession(s); });
  }
  function renderMarkdown(host, md) {
    if (!host) return;
    if (g.IL && IL.noahAI && IL.noahAI.renderReply) IL.noahAI.renderReply(host, md);
    else host.textContent = md;
  }

  /* ---------------- interview engine calls ---------------- */
  function interviewCall(payload) {
    var ctl = new AbortController();
    var to = setTimeout(function () { try { ctl.abort(); } catch (e) {} }, 45000);
    return fetch('/api/noah/interview', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload), signal: ctl.signal
    }).then(function (r) { clearTimeout(to); return r.json(); });
  }
  function turnPayload() {
    return {
      action: 'turn', setup: session.setup, tutor: session.tutor,
      state: { questionsAsked: session.questionsAsked, targetQuestions: session.targetQuestions, phase: session.phase },
      history: session.history
    };
  }

  /* ---------------- live flow ---------------- */
  function startSession(setup) {
    session = newSession();
    session.setup = setup;
    session.targetQuestions = setup.length === 'full' ? 14 : 8;
    session.tutor = currentTutor();
    overlay.querySelector('#miTutorName').textContent = tutorName();
    renderStage();
    session.startedAt = Date.now();
    session.timerId = setInterval(function () {
      session.elapsedSec = Math.floor((Date.now() - session.startedAt) / 1000);
      els.timer.textContent = fmtClock(session.elapsedSec);
      var hudEl = els.hud && els.hud.querySelector('.mi-hudchip b');
      if (hudEl) hudEl.textContent = fmtClock(session.elapsedSec);
    }, 1000);
    updateHud(null);
    setStatus('<b>' + tutorName() + '</b> is joining as your interviewer…');
    nextInterviewerTurn();
  }

  function nextInterviewerTurn() {
    if (!session || session.over) return;
    session.busy = true;
    setStage('thinking');
    setStatus('<b>' + tutorName() + '</b> is thinking…');
    els.mainBtn.disabled = true; els.mainBtn.textContent = '…';
    interviewCall(turnPayload()).then(function (d) {
      session.busy = false;
      if (!session || session.over) return;
      if (!d || !d.say) throw new Error('empty');
      session.history.push({ role: 'interviewer', content: d.say });
      addLog('interviewer', d.say);
      els.question.textContent = d.say;
      if (session.phase === 'opening') session.phase = 'main';
      if (d.marker === 'WRAP' && session.phase === 'main') session.phase = 'candidate';
      var done = d.marker === 'DONE' || session.phase === 'closing';
      // Barge-in: the candidate can cut the interviewer off and answer.
      els.mainBtn.disabled = false; els.mainBtn.textContent = '✋ Interrupt & answer';
      session._speaking = true;
      speak(d.say).then(function () {
        session._speaking = false;
        if (!session || session.over) return;
        if (done) { finishAndDebrief(); return; }
        beginListening();
      });
    }).catch(function () {
      session.busy = false;
      setStatus('The interviewer hit a connection snag. Tap below to retry.');
      els.mainBtn.disabled = false; els.mainBtn.textContent = '↻ Retry';
      session._retry = true;
    });
  }

  function beginListening() {
    if (!session || session.over) return;
    setStage('listening');
    setStatus(session.phase === 'candidate'
      ? 'Your turn — ask <b>' + tutorName() + '</b> anything about the role. Say “that’s all” when you are done.'
      : '<b>Listening…</b> answer out loud, then pause — or tap Done.');
    els.interim.textContent = '';
    els.mainBtn.disabled = false;
    els.mainBtn.classList.add('rec');
    els.mainBtn.textContent = session._typed ? 'Send answer' : '✓ Done answering';
    session._answerStartedAt = Date.now();
    if (session._typed) return; // text mode: wait for Send
    var got = '';
    listen(function (interim) {
      got = interim;
      if (els.interim) els.interim.textContent = interim ? '“' + interim + '”' : '';
    }).then(function (text) {
      els.mainBtn.classList.remove('rec');
      submitAnswer(text);
    }).catch(function () {
      els.mainBtn.classList.remove('rec');
      // Microphone unavailable: fall back to typing rather than dead-ending.
      session._typed = true;
      els.typebar.classList.add('open');
      setStatus('Microphone is unavailable here — type your answer below and tap Send.');
      els.mainBtn.disabled = false; els.mainBtn.textContent = 'Send answer';
      els.typeInput.focus();
    });
  }

  function submitTyped() {
    var v = els.typeInput.value.trim();
    if (!v || !session || session.busy || session.over) return;
    els.typeInput.value = '';
    finishListening();
    submitAnswer(v);
  }

  function submitAnswer(text) {
    if (!session || session.over) return;
    text = String(text || '').replace(/\s+/g, ' ').trim();
    var seconds = Math.max(1, (Date.now() - (session._answerStartedAt || Date.now())) / 1000);
    els.interim.textContent = '';
    if (!text) {
      setStatus('I didn’t catch that — tap the mic and try again, or type your answer.');
      els.mainBtn.disabled = false; els.mainBtn.textContent = '🎙 Answer again';
      session._retryListen = true;
      return;
    }
    session.history.push({ role: 'candidate', content: text });
    addLog('candidate', text);
    els.question.textContent = '';
    if (session.phase === 'main' || session.phase === 'opening') {
      var m = analyzeAnswer(text, seconds);
      m.q = session.questionsAsked + 1;
      session.metrics.push(m);
      session.questionsAsked++;
      updateHud(m);
      if (session.questionsAsked >= session.targetQuestions) session.phase = 'candidate';
    } else if (session.phase === 'candidate') {
      if (/that'?s all|no more questions|i'?m (all )?(done|set)|no,? that'?s it/i.test(text)) {
        session.phase = 'closing';
      }
    }
    setStage('thinking');
    nextInterviewerTurn();
  }

  function onMainBtn() {
    if (!session || session.over) return;
    if (session._retry) { session._retry = false; nextInterviewerTurn(); return; }
    if (session._retryListen) { session._retryListen = false; beginListening(); return; }
    if (session._typed) { submitTyped(); return; }
    if (session._speaking) { stopSpeaking(); return; } // barge-in: speak() continuation opens the mic
    // "Done answering" while listening.
    finishListening();
  }

  function endInterview(manual) {
    if (!session || session.over) return;
    stopSpeaking();
    finishListening();
    if (session.history.filter(function (m) { return m.role === 'candidate'; }).length >= 1) {
      session.phase = 'closing';
      finishAndDebrief();
    } else {
      closeInterview();
    }
  }

  function finishAndDebrief() {
    if (!session || session.over) return;
    session.over = true;
    if (session.timerId) clearInterval(session.timerId);
    els.controls.hidden = true;
    els.typebar.classList.remove('open');
    setStage('thinking');
    setStatus('<b>' + tutorName() + '</b> is writing your debrief…');
    els.question.textContent = '';
    interviewCall({
      action: 'debrief', setup: session.setup, tutor: session.tutor,
      history: session.history, metrics: session.metrics
    }).then(function (d) {
      session.debrief = (d && d.debrief) ? d.debrief : '';
      saveSession();
      renderDebrief();
      if (session.debrief) {
        setStage('speaking');
        speak('Your debrief is ready below. ' + firstDebriefLine(session.debrief));
      }
    }).catch(function () {
      saveSession();
      renderDebrief('The debrief could not be generated just now (connection) — your transcript is saved under Past interviews, and you can re-run a debrief by reviewing it later.');
    });
  }
  function firstDebriefLine(md) {
    var m = /##\s*Overall impression\s*\n+([^\n#]+)/i.exec(md || '');
    return m ? m[1].trim().slice(0, 220) : 'Your debrief is ready below.';
  }
  function avgMetric(key) {
    if (!session.metrics.length) return null;
    var vals = session.metrics.map(function (m) { return m[key]; }).filter(function (v) { return v != null; });
    if (!vals.length) return null;
    return Math.round(vals.reduce(function (a, b) { return a + b; }, 0) / vals.length);
  }
  function renderDebrief(fallbackNote) {
    var statChips =
      '<span class="mi-hudchip">Answers <b>' + session.metrics.length + '</b></span>' +
      '<span class="mi-hudchip">Total time <b>' + fmtClock(session.elapsedSec) + '</b></span>' +
      (avgMetric('wpm') ? '<span class="mi-hudchip">Avg pace <b>' + avgMetric('wpm') + ' wpm</b></span>' : '') +
      '<span class="mi-hudchip">Total fillers <b>' + session.metrics.reduce(function (a, m) { return a + m.fillers; }, 0) + '</b></span>' +
      '<span class="mi-hudchip">Total words <b>' + session.metrics.reduce(function (a, m) { return a + m.words; }, 0) + '</b></span>';
    els.body.innerHTML =
      '<div class="mi-stage" data-state="idle"><div class="mi-avatarwrap"><video src="' + tutorVideo() + '" autoplay loop muted playsinline></video></div>' +
      '<div class="mi-statustext"><b>Interview complete.</b> Here is your debrief, ' + (session.tutor === 'genesis' ? 'from Genesis' : 'from Noah') + '.</div>' +
      '<div class="mi-hud">' + statChips + '</div></div>' +
      (fallbackNote ? '<p class="mi-note">' + esc(fallbackNote) + '</p>' : '') +
      '<div class="mi-debrief" id="miDebriefBody" style="margin-top:14px"></div>' +
      '<div style="display:flex;gap:10px;margin-top:18px;flex-wrap:wrap">' +
        '<button class="mi-ghost" id="miAgain" type="button">↻ Practice again</button>' +
        '<button class="mi-ghost" id="miDl2" type="button">Download transcript</button>' +
        '<button class="mi-ghost" id="miDone2" type="button">Done</button></div>';
    if (session.debrief) renderMarkdown(els.body.querySelector('#miDebriefBody'), session.debrief);
    els.body.querySelector('#miAgain').addEventListener('click', renderSetup);
    els.body.querySelector('#miDone2').addEventListener('click', closeInterview);
    els.body.querySelector('#miDl2').addEventListener('click', function () {
      downloadSession({ id: session.id, date: Date.now(), tutor: session.tutor, setup: session.setup, history: session.history, debrief: session.debrief });
    });
    els.body.scrollTop = 0;
  }

  /* ---------------- open / close ---------------- */
  function openInterview() {
    buildOverlay();
    session = newSession();
    session.tutor = currentTutor();
    overlay.hidden = false;
    document.body.style.overflow = 'hidden';
    renderSetup();
  }
  function closeInterview() {
    stopSpeaking();
    finishListening();
    if (session && session.timerId) clearInterval(session.timerId);
    if (session) session.over = true;
    if (overlay) overlay.hidden = true;
    document.body.style.overflow = '';
    setStage('idle');
  }

  /* ---------------- entry points ---------------- */
  function wirePageButton() {
    var btn = document.getElementById('miBtn');
    if (btn && !btn._miWired) { btn._miWired = true; btn.addEventListener('click', openInterview); }
  }
  function wireWidgetLink() {
    var panel = document.getElementById('noah-panel');
    if (!panel || panel.querySelector('[data-mi-link]')) return;
    var b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('data-mi-link', '1');
    b.textContent = '🎙 Verbal mock interview';
    b.style.cssText = 'display:block;width:calc(100% - 28px);margin:8px 14px;padding:9px 12px;background:rgba(201,162,39,.12);border:1px solid rgba(201,162,39,.4);color:#e8c34a;border-radius:10px;font-size:.84rem;font-weight:600;cursor:pointer';
    b.addEventListener('click', function () { window.open(ABS + '/noah/?mode=interview', '_blank'); });
    var head = panel.querySelector('.noah-head, header, [class*="head"]') || panel.firstElementChild;
    if (head && head.parentNode) head.parentNode.insertBefore(b, head.nextSibling);
    else panel.insertBefore(b, panel.firstChild);
  }
  function boot() {
    wirePageButton();
    wireWidgetLink();
    var tries = 0;
    var iv = setInterval(function () {
      wireWidgetLink();
      if (++tries > 12) clearInterval(iv);
    }, 1500);
    try {
      if (/[?&]mode=interview\b/.test(location.search)) setTimeout(openInterview, 600);
    } catch (e) {}
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();

  g.ILMockInterview = { open: openInterview, close: closeInterview };
})(window);
