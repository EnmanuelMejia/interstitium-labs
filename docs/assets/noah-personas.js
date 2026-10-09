/* =====================================================================
 * Interstitium Labs — Noah AI Persona & Voice Expansion (2026-10-09)
 *
 * Adds to the Noah AI widget (patches noah-ai.js + noah-voice.js at runtime):
 *
 *  1. PERSONA SELECTOR — 5 original speaking styles (Visionary, Engineer,
 *     Philosopher, Mentor, Trickster). Each sends a `persona` param to
 *     POST /api/noah. All original — no real-person impersonation.
 *
 *  2. VOICE SELECTOR — lists browser speechSynthesis voices with descriptive
 *     labels (Scholar, Narrator, Guide, Sage, Spark). Each persona maps to
 *     a preferred voice profile (rate/pitch/voice).
 *
 *  3. AVATAR PICKER — visual picker for the 4 procedural avatars
 *     (monas, orrery, sigil, wisp) + accent colors. Uses il-noah-avatar.js.
 *
 *  4. ADAPTIVE VOICE TECH —
 *     - Adaptive speech rate: analyzes text complexity, slows for dense
 *       technical content, speeds for casual conversation.
 *     - Emotion-aware TTS: detects encouraging vs. serious vs. playful tone,
 *       adjusts pitch and rate accordingly.
 *     - Lip-sync: drives avatar "speaking" state via speechSynthesis
 *       boundary events for word-level sync.
 *
 * Loads after noah-voice.js. Patches the widget DOM at build time.
 * Does NOT modify noah-ai.js or noah-voice.js directly.
 * ===================================================================== */
(function (g) {
  'use strict';

  var PERSONA_CSS = [
    '#noah-persona-row{display:flex;gap:8px;padding:8px 14px;border-bottom:1px solid rgba(255,255,255,.06);',
    'background:rgba(0,0,0,.25);align-items:center;flex-wrap:wrap;}',
    '#noah-persona-select{flex:1;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.15);',
    'border-radius:8px;color:#dbe4ee;font-size:11.5px;padding:5px 8px;min-width:120px;}',
    '#noah-persona-select option{background:#0d141d;color:#dbe4ee;}',
    '#noah-voice-select{flex:1;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.15);',
    'border-radius:8px;color:#dbe4ee;font-size:11.5px;padding:5px 8px;min-width:120px;}',
    '#noah-voice-select option{background:#0d141d;color:#dbe4ee;}',
    '.noah-persona-label{font-size:10px;color:#7d8ea3;letter-spacing:.08em;text-transform:uppercase;}',
    '#noah-avatar-row{display:flex;gap:6px;padding:8px 14px;border-bottom:1px solid rgba(255,255,255,.06);',
    'background:rgba(0,0,0,.2);align-items:center;flex-wrap:wrap;}',
    '.noah-avatar-opt{width:36px;height:36px;border-radius:50%;border:2px solid rgba(255,255,255,.15);',
    'cursor:pointer;padding:0;background:rgba(255,255,255,.04);display:flex;align-items:center;justify-content:center;',
    'font-size:16px;transition:border-color .2s;}',
    '.noah-avatar-opt:hover{border-color:rgba(34,211,238,.5);}',
    '.noah-avatar-opt.active{border-color:#d4af37;box-shadow:0 0 8px rgba(212,175,55,.4);}',
    '.noah-accent-opt{width:24px;height:24px;border-radius:50%;border:2px solid rgba(255,255,255,.2);',
    'cursor:pointer;padding:0;}',
    '.noah-accent-opt.active{border-color:#fff;box-shadow:0 0 6px rgba(255,255,255,.5);}',
    '#noah-adaptive-note{font-size:10px;color:#5a6b7d;padding:4px 14px;text-align:center;}',
  ].join('\n');

  /* ---------- Persona definitions (must match backend NOAH_PERSONAS) ---------- */

  var PERSONAS = {
    visionary:   { label: 'Visionary',   icon: '🔭', voice: { rate: 1.05, pitch: 1.0  }, avatar: 'sigil',  accent: 'gold'    },
    engineer:    { label: 'Engineer',    icon: '⚙️', voice: { rate: 0.95, pitch: 0.9  }, avatar: 'orrery', accent: 'cyan'    },
    philosopher: { label: 'Philosopher', icon: '🏛️', voice: { rate: 0.85, pitch: 0.85 }, avatar: 'monas',  accent: 'violet'  },
    mentor:      { label: 'Mentor',      icon: '🌱', voice: { rate: 0.95, pitch: 1.1  }, avatar: 'wisp',   accent: 'emerald' },
    trickster:   { label: 'Trickster',   icon: '🃏', voice: { rate: 1.15, pitch: 1.2  }, avatar: 'sigil',  accent: 'cyan'    },
  };
  var PERSONA_ORDER = ['visionary', 'engineer', 'philosopher', 'mentor', 'trickster'];

  var AVATARS = {
    monas:  { label: 'Monas',  icon: '💠' },
    orrery: { label: 'Orrery', icon: '🪐' },
    sigil:  { label: 'Sigil',  icon: '✨' },
    wisp:   { label: 'Wisp',   icon: '🌌' },
  };
  var ACCENTS = {
    cyan:    { label: 'Cyan',    css: '#5EEAD4' },
    gold:    { label: 'Gold',    css: '#D4A853' },
    violet:  { label: 'Violet',  css: '#A78BFA' },
    emerald: { label: 'Emerald', css: '#34D399' },
  };

  /* Voice profiles — descriptive labels, NOT named after real people.
     All mapped to natural, human-like voices. Robotic/synthetic voices
     are excluded by the pickBestVoice() filter below. */
  var VOICE_PROFILES = [
    { id: 'scholar',  label: 'Scholar 📖',  desc: 'Measured, precise — Athena', rate: 0.92, pitch: 0.95, ttsVoice: 'avocado_v2:MAI_01' },
    { id: 'narrator', label: 'Narrator 🎙️', desc: 'Warm, engaging — Zeus',     rate: 1.0,  pitch: 1.0,  ttsVoice: 'avocado_v2:MAI_03' },
    { id: 'guide',    label: 'Guide 🧭',    desc: 'Clear, encouraging — Luna', rate: 1.0,  pitch: 1.1,  ttsVoice: 'avocado_v2:MAI_01' },
    { id: 'sage',     label: 'Sage 🦉',     desc: 'Deep, contemplative — Apollo', rate: 0.85, pitch: 0.8, ttsVoice: 'avocado_v2:MAI_03' },
    { id: 'spark',    label: 'Spark ⚡',    desc: 'Energetic, quick — Mars',   rate: 1.15, pitch: 1.15, ttsVoice: 'avocado_v2:MAI_01' },
  ];

  /* Server-side TTS voice IDs ranked by naturalness (per skill docs).
     MAI_01 (Warm) and MAI_03 (Smooth) are the recommended production-quality set. */
  var TTS_VOICE_RANKING = [
    'avocado_v2:MAI_01',  // Warm — most natural
    'avocado_v2:MAI_03',  // Smooth — most natural
    'avocado_v2:rumi',
    'avocado_v2:chip',
    'avocado_v2:briggs',
  ];

  var state = {
    persona: 'visionary',
    voiceProfile: 'narrator',
    browserVoice: null, // actual SpeechSynthesisVoice
    avatar: 'sigil',
    accent: 'gold',
    personas: [], // fetched from /api/noah/models
  };

  /* ---------- Adaptive speech analysis ---------- */

  /**
   * Analyze text complexity to determine optimal speech rate.
   * Dense technical content -> slower. Casual conversation -> faster.
   * Returns rate multiplier 0.8 - 1.2.
   */
  function analyzeComplexity(text) {
    var t = String(text || '');
    if (!t.length) return 1.0;

    var words = t.split(/\s+/).length;
    var sentences = Math.max(t.split(/[.!?]+/).length, 1);
    var avgWordsPerSentence = words / sentences;

    // Technical indicators
    var techTerms = (t.match(/\b(function|class|interface|algorithm|quantum|neural|tensor|api|sdk|framework|protocol|encryption|async|await|promise|callback|recursion|polymorphism|encapsulation)\b/gi) || []).length;
    var codeBlocks = (t.match(/```/g) || []).length / 2;
    var numbers = (t.match(/\d+/g) || []).length;

    var complexity = 0;
    if (avgWordsPerSentence > 20) complexity += 0.3;
    if (avgWordsPerSentence > 30) complexity += 0.2;
    if (techTerms > 5) complexity += 0.3;
    if (codeBlocks > 0) complexity += 0.4;
    if (numbers > 10) complexity += 0.2;

    // Map complexity 0-1.5 to rate 1.15 (simple) -> 0.8 (complex)
    var rate = 1.15 - (Math.min(complexity, 1.5) * 0.23);
    return Math.max(0.8, Math.min(1.15, rate));
  }

  /**
   * Detect emotional tone for TTS adjustment.
   * Returns { pitch: multiplier, rate: multiplier, label }
   */
  function detectEmotion(text) {
    var t = String(text || '').toLowerCase();

    var encouraging = (t.match(/\b(great|excellent|amazing|wonderful|proud|celebrate|success|achieve|brilliant|fantastic|congratulations)\b/g) || []).length;
    var serious = (t.match(/\b(critical|urgent|warning|danger|risk|failure|error|breach|vulnerability|threat|caution)\b/g) || []).length;
    var playful = (t.match(/\b(ha|haha|funny|joke|playful|absurd|ridiculous|hilarious|whimsical)\b/g) || []).length;
    var questioning = (t.match(/\?/g) || []).length;

    if (encouraging >= 2) return { pitch: 1.15, rate: 1.05, label: 'encouraging' };
    if (serious >= 2)     return { pitch: 0.9,  rate: 0.9,  label: 'serious' };
    if (playful >= 2)     return { pitch: 1.2,  rate: 1.1,  label: 'playful' };
    if (questioning >= 3) return { pitch: 1.1,  rate: 0.95, label: 'inquiring' };
    return { pitch: 1.0, rate: 1.0, label: 'neutral' };
  }

  /* ---------- Server-side TTS (5 genuinely distinct voices) ----------
     POST /api/noah/tts -> audio/mpeg. Tries the server first; falls back
     to browser speechSynthesis only if the server fails. */
  var serverAudio = null;
  var serverTtsFailed = false; // latch: stop hammering a dead endpoint

  function stopServerAudio() {
    try {
      if (serverAudio) { serverAudio.pause(); serverAudio.src = ''; serverAudio = null; }
    } catch (e) {}
    setAvatarState('idle');
  }

  function serverSpeak(text) {
    if (serverTtsFailed) return false;
    if (!('fetch' in g)) return false;
    try {
      stopServerAudio();
      if ('speechSynthesis' in g) { try { g.speechSynthesis.cancel(); } catch (e) {} }
      var ctl = new AbortController();
      var timeout = setTimeout(function () { try { ctl.abort(); } catch (e) {} }, 25000);
      fetch('/api/noah/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: String(text || '').slice(0, 800), voice: state.voiceProfile || 'narrator', speed: 1.0 }),
        signal: ctl.signal,
      }).then(function (resp) {
        clearTimeout(timeout);
        if (!resp.ok) throw new Error('tts ' + resp.status);
        return resp.blob();
      }).then(function (blob) {
        if (!blob || blob.size < 1000) throw new Error('tts empty');
        var url = (g.URL || window.URL).createObjectURL(blob);
        var audio = new Audio(url);
        serverAudio = audio;
        audio.onended = function () {
          try { (g.URL || window.URL).revokeObjectURL(url); } catch (e) {}
          if (serverAudio === audio) serverAudio = null;
          setAvatarState('idle');
        };
        audio.onerror = function () {
          try { (g.URL || window.URL).revokeObjectURL(url); } catch (e) {}
          if (serverAudio === audio) serverAudio = null;
          setAvatarState('idle');
          browserSpeak(text); // last-resort fallback
        };
        setAvatarState('speaking');
        var p = audio.play();
        if (p && p.catch) p.catch(function () {
          setAvatarState('idle');
          browserSpeak(text);
        });
      }).catch(function () {
        clearTimeout(timeout);
        serverTtsFailed = true; // don't retry server this session
        setAvatarState('idle');
        browserSpeak(text);
      });
      return true;
    } catch (e) { return false; }
  }

  // Expose a stop hook so the widget's mute/stop also silences server audio.
  try {
    g.__noahStopServerAudio = stopServerAudio;
    if (g.IL) g.IL.noahStopServerAudio = stopServerAudio;
  } catch (e) {}

  /* ---------- Enhanced speak with adaptive tech ---------- */

  function adaptiveSpeak(text, baseRate, basePitch) {
    // Prefer server-side TTS (5 distinct natural voices). Fall back to
    // browser speechSynthesis only if the server path fails.
    if (serverSpeak(text)) return;
    browserSpeak(text, baseRate, basePitch);
  }

  function browserSpeak(text, baseRate, basePitch) {
    if (!('speechSynthesis' in g)) return;
    try {
      g.speechSynthesis.cancel();

      var clean = String(text || '')
        .replace(/```[\s\S]*?```/g, ' code block ')
        .replace(/`([^`]+)`/g, '$1')
        .replace(/\*\*([^*]+)\*\*/g, '$1')
        .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
        .replace(/#{1,6}\s/g, '')
        .replace(/\n{2,}/g, '. ');

      var complexityRate = analyzeComplexity(clean);
      var emotion = detectEmotion(clean);

      var persona = PERSONAS[state.persona] || PERSONAS.visionary;
      var voiceProf = VOICE_PROFILES.find(function (v) { return v.id === state.voiceProfile; }) || VOICE_PROFILES[1];

      // Combine: persona base × voice profile × adaptive × emotion
      var finalRate = (baseRate || persona.voice.rate) * voiceProf.rate * complexityRate * emotion.rate;
      var finalPitch = (basePitch || persona.voice.pitch) * voiceProf.pitch * emotion.pitch;

      // Clamp to safe ranges
      finalRate = Math.max(0.5, Math.min(2.0, finalRate));
      finalPitch = Math.max(0.5, Math.min(2.0, finalPitch));

      var u = new SpeechSynthesisUtterance(clean.slice(0, 2000));
      u.rate = finalRate;
      u.pitch = finalPitch;
      if (state.browserVoice) u.voice = state.browserVoice;

      // Lip-sync: drive avatar speaking state via boundary events
      var avatarCtl = getAvatarCtl();
      u.onstart = function () { setAvatarState('speaking'); };
      u.onend = function () { setAvatarState('idle'); };
      u.onerror = function () { setAvatarState('idle'); };
      // Word-level sync for smoother animation
      u.onboundary = function (e) {
        if (e.name === 'word' && avatarCtl && avatarCtl.pulse) {
          try { avatarCtl.pulse(); } catch (err) {}
        }
      };

      g.speechSynthesis.speak(u);

      // Debug info (visible in console)
      if (g.console && g.console.debug) {
        g.console.debug('[Noah voice] rate=' + finalRate.toFixed(2) +
          ' pitch=' + finalPitch.toFixed(2) +
          ' emotion=' + emotion.label +
          ' complexityRate=' + complexityRate.toFixed(2));
      }
    } catch (e) {}
  }

  function getAvatarCtl() {
    // Try to find the avatar controller from noah-ai.js
    try {
      if (g.IL && g.IL.noahAvatarCtl) return g.IL.noahAvatarCtl;
    } catch (e) {}
    return null;
  }

  function setAvatarState(s) {
    var ctl = getAvatarCtl();
    if (ctl && ctl.setState) {
      try { ctl.setState(s); } catch (e) {}
    }
  }

  /* ---------- Browser voice enumeration ---------- */

  function getBrowserVoices() {
    if (!('speechSynthesis' in g)) return [];
    try {
      return g.speechSynthesis.getVoices().filter(function (v) {
        return v.lang.startsWith('en');
      });
    } catch (e) { return []; }
  }

  function pickBestVoice(voices, profileId) {
    if (!voices.length) return null;

    // EXCLUDE robotic/synthetic-sounding voices
    var roboticPatterns = /robot|synthetic|espeak|festival|flite|pico|svox|eloquence|dectalk/i;
    var natural = voices.filter(function (v) {
      return !roboticPatterns.test(v.name);
    });
    // If all are flagged robotic, fall back to full list (better than silence)
    var pool = natural.length ? natural : voices;

    // Build a ranked list of preferred voices (best first)
    var keywords = ['google us english', 'natural', 'human', 'neural', 'wavenet', 'samantha', 'alex', 'daniel', 'karen', 'moira', 'tessa'];
    var ranked = [];
    // First: keyword matches in priority order
    for (var i = 0; i < keywords.length; i++) {
      var matches = pool.filter(function (v) {
        return v.name.toLowerCase().includes(keywords[i]) && ranked.indexOf(v) === -1;
      });
      ranked = ranked.concat(matches);
    }
    // Then: premium/enhanced
    var premium = pool.filter(function (v) {
      var n = v.name.toLowerCase();
      return (n.includes('premium') || n.includes('enhanced') || n.includes('plus')) && ranked.indexOf(v) === -1;
    });
    ranked = ranked.concat(premium);
    // Then: remaining voices
    pool.forEach(function (v) {
      if (ranked.indexOf(v) === -1) ranked.push(v);
    });

    // Distribute different voices to different profiles for distinctness
    // Each profile gets a different offset into the ranked list
    var profileOrder = ['scholar', 'narrator', 'guide', 'sage', 'spark'];
    var profileIdx = profileOrder.indexOf(profileId);
    if (profileIdx === -1) profileIdx = 0;

    // Use profile index to pick a different voice from the ranked list
    // This ensures Scholar, Narrator, Guide, Sage, Spark all sound different
    return ranked[profileIdx % ranked.length] || ranked[0];
  }

  /* ---------- Avatar picker ---------- */

  function applyAvatar(avatarId, accentId) {
    state.avatar = avatarId;
    state.accent = accentId;
    try {
      // Update the il-noah-avatar profile
      var profile = { avatar: avatarId, accent: accentId };
      if (g.localStorage) {
        var existing = {};
        try { existing = JSON.parse(g.localStorage.getItem('il-noah-profile') || '{}'); } catch (e) {}
        existing.avatar = avatarId;
        existing.accent = accentId;
        g.localStorage.setItem('il-noah-profile', JSON.stringify(existing));
      }
      // Trigger re-render if avatar system exposes it
      if (g.NoahAvatar && g.NoahAvatar.applyProfile) {
        g.NoahAvatar.applyProfile(profile);
      }
      localStorage.setItem('noah-persona-avatar', avatarId);
      localStorage.setItem('noah-persona-accent', accentId);
    } catch (e) {}
  }

  /* ---------- Fetch personas from backend ---------- */

  function fetchPersonas(personaSelect) {
    fetch('/api/noah/models', { credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!d || !d.ok || !Array.isArray(d.personas)) return;
        state.personas = d.personas;
        // Rebuild persona select with backend data
        personaSelect.innerHTML = '';
        d.personas.forEach(function (p) {
          var o = document.createElement('option');
          o.value = p.id;
          var local = PERSONAS[p.id];
          o.textContent = (local ? local.icon + ' ' : '') + p.label + ' — ' + p.desc;
          if (p.id === (d.defaultPersona || 'visionary')) o.selected = true;
          personaSelect.appendChild(o);
        });
        var saved = null;
        try { saved = localStorage.getItem('noah-persona'); } catch (e) {}
        if (saved && PERSONAS[saved]) {
          personaSelect.value = saved;
          setPersona(saved, false);
        } else {
          setPersona(d.defaultPersona || 'visionary', false);
        }
      })
      .catch(function () {});
  }

  function setPersona(personaId, save) {
    if (!PERSONAS[personaId]) return;
    state.persona = personaId;
    var p = PERSONAS[personaId];

    // Auto-switch avatar to persona's preferred style (unless user customized)
    var userCustomized = false;
    try { userCustomized = localStorage.getItem('noah-avatar-custom') === '1'; } catch (e) {}
    if (!userCustomized) {
      applyAvatar(p.avatar, p.accent);
      syncAvatarPicker();
    }

    // Auto-switch voice profile to match persona energy
    var voiceMap = {
      visionary: 'narrator', engineer: 'scholar', philosopher: 'sage',
      mentor: 'guide', trickster: 'spark',
    };
    state.voiceProfile = voiceMap[personaId] || 'narrator';
    syncVoiceSelect();

    if (save !== false) {
      try { localStorage.setItem('noah-persona', personaId); } catch (e) {}
    }
  }

  function syncAvatarPicker() {
    document.querySelectorAll('.noah-avatar-opt').forEach(function (el) {
      el.classList.toggle('active', el.dataset.avatar === state.avatar);
    });
    document.querySelectorAll('.noah-accent-opt').forEach(function (el) {
      el.classList.toggle('active', el.dataset.accent === state.accent);
    });
  }

  function syncVoiceSelect() {
    var sel = document.getElementById('noah-voice-select');
    if (sel) sel.value = state.voiceProfile;
  }

  /* ---------- Patch the widget ---------- */

  function patch() {
    var panel = document.getElementById('noah-panel');
    if (!panel) { setTimeout(patch, 500); return; }

    // Wait for noah-voice.js to have patched (model row exists)
    var modelRow = document.getElementById('noah-model-row');
    if (!modelRow) { setTimeout(patch, 500); return; }

    var style = document.createElement('style');
    style.textContent = PERSONA_CSS;
    document.head.appendChild(style);

    var msgs = panel.querySelector('#noah-msgs');
    if (!msgs) { setTimeout(patch, 500); return; }

    // --- Persona + Voice row (above model row) ---
    var personaRow = document.createElement('div');
    personaRow.id = 'noah-persona-row';

    var personaLabel = document.createElement('span');
    personaLabel.className = 'noah-persona-label';
    personaLabel.textContent = 'Persona';

    var personaSelect = document.createElement('select');
    personaSelect.id = 'noah-persona-select';
    personaSelect.setAttribute('aria-label', 'Noah persona');
    personaSelect.title = 'Choose Noah\'s speaking style';
    // Temporary options until backend fetch completes
    PERSONA_ORDER.forEach(function (id) {
      var o = document.createElement('option');
      o.value = id;
      o.textContent = PERSONAS[id].icon + ' ' + PERSONAS[id].label;
      personaSelect.appendChild(o);
    });
    personaSelect.addEventListener('change', function () {
      setPersona(personaSelect.value, true);
    });

    var voiceLabel = document.createElement('span');
    voiceLabel.className = 'noah-persona-label';
    voiceLabel.textContent = 'Voice';

    var voiceSelect = document.createElement('select');
    voiceSelect.id = 'noah-voice-select';
    voiceSelect.setAttribute('aria-label', 'Voice style');
    voiceSelect.title = 'Choose voice character';
    VOICE_PROFILES.forEach(function (vp) {
      var o = document.createElement('option');
      o.value = vp.id;
      o.textContent = vp.label;
      o.title = vp.desc;
      voiceSelect.appendChild(o);
    });
    voiceSelect.value = state.voiceProfile;
    voiceSelect.addEventListener('change', function () {
      state.voiceProfile = voiceSelect.value;
      // Update browser voice to match
      var voices = getBrowserVoices();
      state.browserVoice = pickBestVoice(voices, state.voiceProfile);
      try { localStorage.setItem('noah-voice-profile', state.voiceProfile); } catch (e) {}
    });

    // Restore saved voice profile
    try {
      var savedVoice = localStorage.getItem('noah-voice-profile');
      if (savedVoice && VOICE_PROFILES.some(function (v) { return v.id === savedVoice; })) {
        state.voiceProfile = savedVoice;
        voiceSelect.value = savedVoice;
      }
    } catch (e) {}

    personaRow.appendChild(personaLabel);
    personaRow.appendChild(personaSelect);
    personaRow.appendChild(voiceLabel);
    personaRow.appendChild(voiceSelect);
    panel.insertBefore(personaRow, modelRow);

    fetchPersonas(personaSelect);

    // --- Avatar picker row (below model row) ---
    var avatarRow = document.createElement('div');
    avatarRow.id = 'noah-avatar-row';

    var avatarLabel = document.createElement('span');
    avatarLabel.className = 'noah-persona-label';
    avatarLabel.textContent = 'Avatar';
    avatarRow.appendChild(avatarLabel);

    Object.keys(AVATARS).forEach(function (id) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'noah-avatar-opt' + (id === state.avatar ? ' active' : '');
      btn.dataset.avatar = id;
      btn.innerHTML = AVATARS[id].icon;
      btn.title = AVATARS[id].label;
      btn.setAttribute('aria-label', 'Avatar: ' + AVATARS[id].label);
      btn.addEventListener('click', function () {
        applyAvatar(id, state.accent);
        syncAvatarPicker();
        try { localStorage.setItem('noah-avatar-custom', '1'); } catch (e) {}
      });
      avatarRow.appendChild(btn);
    });

    var accentLabel = document.createElement('span');
    accentLabel.className = 'noah-persona-label';
    accentLabel.textContent = 'Color';
    accentLabel.style.marginLeft = '8px';
    avatarRow.appendChild(accentLabel);

    Object.keys(ACCENTS).forEach(function (id) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'noah-accent-opt' + (id === state.accent ? ' active' : '');
      btn.dataset.accent = id;
      btn.style.background = ACCENTS[id].css;
      btn.title = ACCENTS[id].label;
      btn.setAttribute('aria-label', 'Accent: ' + ACCENTS[id].label);
      btn.addEventListener('click', function () {
        applyAvatar(state.avatar, id);
        syncAvatarPicker();
        try { localStorage.setItem('noah-avatar-custom', '1'); } catch (e) {}
      });
      avatarRow.appendChild(btn);
    });

    panel.insertBefore(avatarRow, msgs);

    // --- Adaptive note ---
    var note = document.createElement('div');
    note.id = 'noah-adaptive-note';
    note.textContent = '🎯 Adaptive voice: rate & tone adjust to content';
    panel.insertBefore(note, msgs);

    // --- Voice quality indicator ---
    var voiceNote = document.createElement('div');
    voiceNote.id = 'noah-voice-quality';
    voiceNote.style.cssText = 'font-size:10px;color:#5a6b7d;padding:2px 14px;text-align:center;';
    function updateVoiceNote() {
      var v = state.browserVoice;
      if (v) {
        voiceNote.textContent = '🔊 Voice: ' + v.name + ' (' + v.lang + ')';
        voiceNote.title = 'Active speech voice. Change in your browser/OS voice settings for different options.';
      } else {
        voiceNote.textContent = '🔇 No speech voice available';
      }
    }
    panel.insertBefore(voiceNote, msgs);

    // --- Restore saved avatar ---
    try {
      var savedAvatar = localStorage.getItem('noah-persona-avatar');
      var savedAccent = localStorage.getItem('noah-persona-accent');
      if (savedAvatar && AVATARS[savedAvatar]) state.avatar = savedAvatar;
      if (savedAccent && ACCENTS[savedAccent]) state.accent = savedAccent;
      syncAvatarPicker();
    } catch (e) {}

    // --- Initialize browser voices ---
    function initVoices() {
      var voices = getBrowserVoices();
      if (voices.length) {
        state.browserVoice = pickBestVoice(voices, state.voiceProfile);
        updateVoiceNote();
      }
    }
    if ('speechSynthesis' in g) {
      initVoices();
      // Voices may load async
      g.speechSynthesis.onvoiceschanged = initVoices;
    }

    // --- Patch fetch to include persona ---
    // noah-voice.js already patches fetch for model+mode; we chain ours
    var origFetch = g.fetch;
    g.fetch = function (url, opts) {
      if (typeof url === 'string' && url.indexOf('/api/noah') === 0 &&
          !url.startsWith('/api/noah-') && opts && opts.method === 'POST' && opts.body) {
        try {
          var body = JSON.parse(opts.body);
          body.persona = state.persona;
          opts = Object.assign({}, opts, { body: JSON.stringify(body) });
        } catch (e) {}
      }
      return origFetch.call(this, url, opts);
    };

    // --- Override the voice output with adaptive version ---
    // Patch IL.noahVoice.speak to use adaptiveSpeak
    if (g.IL && g.IL.noahVoice) {
      var origSpeak = g.IL.noahVoice.speak;
      g.IL.noahVoice.speak = function (text) {
        // Check if voice output is enabled via noah-voice.js state
        // We use adaptiveSpeak which respects the same toggle via its own check
        var voiceState = g.IL.noahVoice.state;
        if (voiceState && voiceState.voiceOut) {
          adaptiveSpeak(text);
        }
      };
      g.IL.noahVoice.adaptiveSpeak = adaptiveSpeak;
      g.IL.noahVoice.setPersona = function (p) {
        setPersona(p, true);
        var sel = document.getElementById('noah-persona-select');
        if (sel) sel.value = p;
      };
      g.IL.noahVoice.getPersona = function () { return state.persona; };
      g.IL.noahVoice.setVoiceProfile = function (v) {
        state.voiceProfile = v;
        syncVoiceSelect();
      };
    }
  }

  // Start patching
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(patch, 2000); });
  } else {
    setTimeout(patch, 2000);
  }

  // Public API
  g.IL = g.IL || {};
  g.IL.noahPersonas = {
    setPersona: function (p) {
      setPersona(p, true);
      var sel = document.getElementById('noah-persona-select');
      if (sel) sel.value = p;
    },
    getPersona: function () { return state.persona; },
    getPersonas: function () { return Object.keys(PERSONAS); },
    setVoiceProfile: function (v) { state.voiceProfile = v; syncVoiceSelect(); },
    adaptiveSpeak: adaptiveSpeak,
    analyzeComplexity: analyzeComplexity,
    detectEmotion: detectEmotion,
  };
})(window);

/* 2026-10-09: server TTS via /api/noah/tts (5 distinct voices) */

/* tts debug */

/* tts shape2 */
