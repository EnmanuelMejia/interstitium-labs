/*!
 * IL Ambient Synth v1.0 — interstitiumlabs.dev
 * ---------------------------------------------------------------------------
 * 100% ORIGINAL procedural ambient audio, synthesized live with the Web Audio
 * API. No audio files, no samples, no recordings, no copyrighted material of
 * any kind. Every sound is generated from oscillators, filtered noise
 * (generated buffers, not recordings), LFOs, and gain envelopes.
 *
 * Styles are *inspired by* genres (dark hacker synthwave, neon synth,
 * cyberpunk ambient) — all notes, patterns, and chord voicings are original
 * compositions written for this module.
 *
 * TUNING: 432Hz concert pitch (A4 = 432Hz) throughout — every MIDI-derived
 * pitch uses CONCERT_A = 432 as its reference (see PITCH_RATIO).
 *
 * Public API:
 *   ILAmbient.play('cyberpunk')  — start a theme (fade-in ~2.5s)
 *   ILAmbient.stop()             — fade-out (~2s) and release all nodes
 *   ILAmbient.setTheme('tron')   — crossfade to another theme
 *   ILAmbient.toggle()           — play/stop toggle; returns new state
 *   ILAmbient.arm('cyberpunk')   — armed autoplay: try now, else start on
 *                                  first user tap/click/keypress anywhere
 *   ILAmbient.setVolume(0..1)    — master volume, smooth ramp
 *   ILAmbient.getVolume()        — current volume
 *   ILAmbient.isPlaying()        — boolean
 *   ILAmbient.currentTheme()     — active theme name or null
 *   ILAmbient.themes             — { name: { label, desc } }
 *   ILAmbient.saved()            — { enabled, theme } from localStorage
 *   ILAmbient.supported          — false when Web Audio is unavailable
 *
 * User preference persists in localStorage under 'il-ambient-enabled'
 * (plus 'il-ambient-theme' and 'il-ambient-volume'). Armed autoplay
 * (ILAmbient.arm) attempts playback on load and falls back to starting on
 * the first user gesture, per browser autoplay policy.
 *
 * CPU budget: each theme keeps roughly <= 8 simultaneous sound sources.
 * Generative loops use a 120 ms lookahead scheduler, not per-note timers.
 *
 * MOBILE: on small screens / low core counts, ILAmbient.reducedMotion()
 * returns true — themes should skip decorative layers (extra delays,
 * shimmer voices) when set. Device tier via ILAmbient.deviceTier():
 * 'ultrawide' | 'desktop' | 'mobile'.
 */
(function (global) {
  'use strict';

  // SPA-navigation guard: il-spa-nav.js swaps documents via
  // document.open/write/close, which keeps the Window (and this closure's
  // AudioContext) alive while re-executing page scripts. If an engine
  // already exists, keep it so audio continues uninterrupted — never
  // create a second context on top of a playing one.
  if (global.ILAmbient && global.ILAmbient.supported) return;

  /* ------------------------------ constants ----------------------------- */
  var LS_ENABLED = 'il-ambient-enabled';
  var LS_THEME   = 'il-ambient-theme';
  var LS_VOLUME  = 'il-ambient-volume';
  var FADE_IN    = 2.5;   // seconds
  var FADE_OUT   = 2.0;   // seconds
  var DEFAULT_THEME = 'cyberpunk';
  // 432Hz concert pitch (user preference, 2026-10-10): A4 = 432Hz.
  // Ratio vs standard 440Hz: 432/440 ≈ 0.98182 (≈ −31.77 cents).
  var CONCERT_A = 432;
  var PITCH_RATIO = CONCERT_A / 440;

  /* ------------------------------ utilities ----------------------------- */
  function supported() {
    return !!(global.AudioContext || global.webkitAudioContext);
  }
  function midi(m) { return CONCERT_A * Math.pow(2, (m - 69) / 12); }
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }
  function pick(arr) { return arr[(Math.random() * arr.length) | 0]; }

  function lsGet(k) {
    try { return global.localStorage.getItem(k); } catch (e) { return null; }
  }
  function lsSet(k, v) {
    try { global.localStorage.setItem(k, v); } catch (e) { /* private mode */ }
  }
  function loadPref() {
    var v = parseFloat(lsGet(LS_VOLUME));
    return {
      enabled: lsGet(LS_ENABLED) === '1',
      theme: lsGet(LS_THEME) || DEFAULT_THEME,
      volume: isNaN(v) ? 0.7 : clamp(v, 0, 1)
    };
  }
  function savePref(enabled, theme) {
    lsSet(LS_ENABLED, enabled ? '1' : '0');
    if (theme) lsSet(LS_THEME, theme);
  }

  /* ---------------- graceful degradation (no Web Audio) ------------------ */
  if (!supported()) {
    global.ILAmbient = {
      supported: false,
      themes: {},
      play: function () { return false; },
      stop: function () {},
      setTheme: function () { return false; },
      toggle: function () { return false; },
      arm: function () {},
      topicTheme: function () { return DEFAULT_THEME; },
      deviceTier: function () { return 'desktop'; },
      isLowPower: function () { return false; },
      getAnalyser: function () { return null; },
      getFrequencyData: function () { return null; },
      setVolume: function () {},
      getVolume: function () { return 0; },
      isPlaying: function () { return false; },
      currentTheme: function () { return null; },
      saved: function () { return { enabled: false, theme: DEFAULT_THEME }; }
    };
    return;
  }

  /* ------------------------------ engine state -------------------------- */
  var ctx = null;          // AudioContext (created lazily on first play)
  var master = null;       // master gain -> compressor -> destination
  var analyser = null;     // AnalyserNode tap for the widget equalizer
  var noiseBuf = null;     // procedurally generated white-noise buffer

  var state = {
    playing: false,
    theme: null,
    themeGain: null,       // per-theme bus; fades in/out on play/stop
    volume: loadPref().volume,
    timers: [],            // setInterval ids
    timeouts: [],          // setTimeout ids
    nodes: [],             // live AudioNodes for cleanup
    stopToken: 0           // invalidates stale fade-out completions
  };

  function reg(node) { state.nodes.push(node); return node; }
  function forget(node) {
    var i = state.nodes.indexOf(node);
    if (i !== -1) state.nodes.splice(i, 1);
  }
  function every(ms, fn) {
    var id = setInterval(fn, ms);
    state.timers.push(id);
    return id;
  }
  function after(ms, fn) {
    var id = setTimeout(fn, ms);
    state.timeouts.push(id);
    return id;
  }

  function ensureCtx() {
    if (!ctx) {
      var AC = global.AudioContext || global.webkitAudioContext;
      ctx = new AC();
      master = ctx.createGain();
      master.gain.value = state.volume;
      // Gentle glue compressor so layered generative voices never clip.
      var comp = ctx.createDynamicsCompressor();
      comp.threshold.value = -18;
      comp.ratio.value = 6;
      comp.attack.value = 0.01;
      comp.release.value = 0.3;
      master.connect(comp);
      // Analyser for the floating widget's live equalizer (zero-latency tap).
      analyser = ctx.createAnalyser();
      analyser.fftSize = 64; // 32 frequency bins — enough for a sleek EQ bar
      analyser.smoothingTimeConstant = 0.75;
      comp.connect(analyser);
      analyser.connect(ctx.destination);
      noiseBuf = makeNoiseBuffer(ctx);
    }
    // Autoplay policy: resume on the user gesture that called play().
    if (ctx.state === 'suspended') {
      var p = ctx.resume();
      if (p && p.catch) p.catch(function () {});
    }
    return ctx;
  }

  // Procedurally generated white noise — random data, NOT a recording.
  function makeNoiseBuffer(c) {
    var len = Math.floor(c.sampleRate * 2);
    var buf = c.createBuffer(1, len, c.sampleRate);
    var d = buf.getChannelData(0);
    for (var i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
    // Edge fades so the loop point never clicks.
    var n = Math.floor(c.sampleRate * 0.02);
    for (var j = 0; j < n; j++) {
      var w = j / n;
      d[j] *= w;
      d[len - 1 - j] *= w;
    }
    return buf;
  }

  /* --------------------------- voice primitives ------------------------- */
  // Connect a voice to its destination(s); dest may be a single node or an
  // array (e.g. [delaySend, dryOut] for echo sends that keep a dry signal).
  function connectDest(node, dest) {
    dest = dest || state.themeGain;
    if (Object.prototype.toString.call(dest) === '[object Array]') {
      dest.forEach(function (d) { node.connect(d); });
    } else {
      node.connect(dest);
    }
  }

  // Enveloped oscillator voice. Auto-stops, auto-disconnects, returns the osc
  // (handy for attaching LFOs to osc.detune / osc.frequency).
  // opts: { m (midi) | f (hz), f2 (sweep target hz), t, dur, type, detune,
  //         attack, release, peak, lp (lowpass hz), hp (highpass hz), q, dest }
  function tone(o) {
    var t = (o.t != null) ? o.t : ctx.currentTime;
    var dur = o.dur || 1;
    var osc = ctx.createOscillator();
    osc.type = o.type || 'sine';
    osc.frequency.setValueAtTime(o.m != null ? midi(o.m) : (o.f || 440), t);
    if (o.f2) osc.frequency.exponentialRampToValueAtTime(Math.max(1, o.f2), t + dur);
    if (o.detune) osc.detune.value = o.detune;

    var head = osc, filt = null;
    if (o.lp || o.hp) {
      filt = ctx.createBiquadFilter();
      if (o.lp) { filt.type = 'lowpass'; filt.frequency.value = o.lp; }
      else { filt.type = 'highpass'; filt.frequency.value = o.hp; }
      filt.Q.value = o.q || 0.7;
      osc.connect(filt);
      head = filt;
    }

    var g = ctx.createGain();
    var a = o.attack || 0.01;
    var r = (o.release != null) ? o.release : 0.25;
    var peak = o.peak || 0.2;
    var susT = t + Math.max(a, dur - r);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(Math.max(0.0002, peak), t + a);
    g.gain.setValueAtTime(Math.max(0.0002, peak), susT);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);

    head.connect(g);
    connectDest(g, o.dest);
    osc.start(t);
    osc.stop(t + dur + 0.15);
    reg(osc); reg(g); if (filt) reg(filt);
    osc.onended = function () {
      [osc, g, filt].forEach(function (n) {
        if (!n) return;
        try { n.disconnect(); } catch (e) {}
        forget(n);
      });
    };
    return osc;
  }

  // Enveloped filtered-noise hit. Buffer is generated, not sampled.
  // opts: { t, dur, type, f, f2, q, peak, attack, release, rate, dest }
  function noiseHit(o) {
    var t = (o.t != null) ? o.t : ctx.currentTime;
    var dur = o.dur || 1;
    var src = ctx.createBufferSource();
    src.buffer = noiseBuf;
    src.loop = true;
    if (o.rate) src.playbackRate.value = o.rate;

    var f = ctx.createBiquadFilter();
    f.type = o.type || 'bandpass';
    f.frequency.setValueAtTime(o.f || 1000, t);
    f.Q.value = o.q || 1;
    if (o.f2) f.frequency.exponentialRampToValueAtTime(Math.max(20, o.f2), t + dur);

    var g = ctx.createGain();
    var a = o.attack || 0.02;
    var r = (o.release != null) ? o.release : 0.3;
    var peak = o.peak || 0.1;
    var susT = t + Math.max(a, dur - r);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(Math.max(0.0002, peak), t + a);
    g.gain.setValueAtTime(Math.max(0.0002, peak), susT);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);

    src.connect(f); f.connect(g); connectDest(g, o.dest);
    src.start(t);
    src.stop(t + dur + 0.15);
    reg(src); reg(f); reg(g);
    src.onended = function () {
      [src, f, g].forEach(function (n) {
        try { n.disconnect(); } catch (e) {}
        forget(n);
      });
    };
    return src;
  }

  // Simple feedback delay send. Returns the delay input node (connect dry
  // voices to it; the wet output is mixed into the theme bus).
  function makeDelay(time, fb, wet) {
    var d = ctx.createDelay(2.0);
    d.delayTime.value = time || 0.35;
    var fbg = ctx.createGain(); fbg.gain.value = (fb != null ? fb : 0.35);
    var wetg = ctx.createGain(); wetg.gain.value = (wet != null ? wet : 0.5);
    d.connect(fbg); fbg.connect(d);
    d.connect(wetg); wetg.connect(state.themeGain);
    reg(d); reg(fbg); reg(wetg);
    return d;
  }

  // LFO -> AudioParam modulation. Returns the LFO oscillator.
  function lfo(freq, depth, param, type) {
    var o = ctx.createOscillator();
    o.type = type || 'sine';
    o.frequency.value = freq;
    var g = ctx.createGain();
    g.gain.value = depth;
    o.connect(g); g.connect(param);
    o.start();
    reg(o); reg(g);
    return o;
  }

  // Lookahead step sequencer: schedules generative events `stepDur` seconds
  // apart, always ~0.4 s ahead of the audio clock (jitter-free timing).
  function schedule(stepDur, onStep) {
    var step = 0;
    var nextT = ctx.currentTime + 0.15;
    function tick() {
      if (!ctx) return;
      while (nextT < ctx.currentTime + 0.4) {
        try { onStep(step, nextT); } catch (e) {}
        step += 1;
        nextT += stepDur;
      }
    }
    tick();
    return every(120, tick);
  }

  // Release every node and timer belonging to the current theme.
  function cleanup() {
    state.timers.forEach(clearInterval); state.timers = [];
    state.timeouts.forEach(clearTimeout); state.timeouts = [];
    state.nodes.forEach(function (n) {
      try { if (n.stop) n.stop(); } catch (e) {}
      try { n.disconnect(); } catch (e) {}
    });
    state.nodes = [];
    if (state.themeGain) {
      try { state.themeGain.disconnect(); } catch (e) {}
      state.themeGain = null;
    }
  }

  // API object handed to each theme's start() function.
  function makeApi() {
    return {
      ctx: ctx,
      out: function () { return state.themeGain; },
      noiseBuffer: function () { return noiseBuf; },
      track: function () {
        for (var i = 0; i < arguments.length; i++) reg(arguments[i]);
      },
      tone: tone,
      noise: noiseHit,
      delay: makeDelay,
      lfo: lfo,
      every: every,
      after: after,
      schedule: schedule,
      midi: midi,
      pick: pick
    };
  }

  /* ------------------------------- themes ------------------------------- */
  // Original compositions. Chord voicings and melodic patterns below were
  // written for this module; genre labels describe inspiration only.

  // -- cybersecurity: "dark hacker synthwave". Low pulsing bass, sparse
  // minor-key arps, filtered noise sweeps, occasional data blips. Tense.
  function startCybersecurity(A) {
    var out = A.out();
    // Sub drone: 55 Hz sine with a slow breathing LFO.
    var sub = A.ctx.createOscillator(); sub.type = 'sine'; sub.frequency.value = 55 * PITCH_RATIO; // A1 at 432Hz = 54Hz
    var sg = A.ctx.createGain(); sg.gain.value = 0.10;
    sub.connect(sg); sg.connect(out); sub.start();
    A.track(sub, sg);
    A.lfo(0.5, 0.03, sg.gain);

    var dly = A.delay(0.32, 0.35, 0.5);
    var bassLine = [33, 0, 33, 0, 36, 0, 33, 0, 31, 0, 31, 0, 36, 0, 38, 0];
    var arpPool = [69, 72, 76, 79, 81, 84]; // A-minor high register
    A.schedule(0.44, function (step, t) {
      var b = bassLine[step % bassLine.length];
      if (b) A.tone({ m: b, t: t, dur: 0.4, type: 'sine', peak: 0.5,
                      attack: 0.01, release: 0.15, lp: 320 });
      if (Math.random() < 0.30) { // sparse arp note, dry + echo send
        A.tone({ m: A.pick(arpPool), t: t, dur: 0.5, type: 'triangle',
                 peak: 0.10, attack: 0.01, release: 0.4, lp: 2400,
                 dest: [dly, out] });
      }
      if (Math.random() < 0.14) { // data blip, dry + echo send
        A.tone({ f: 1200 + Math.random() * 1400, t: t, dur: 0.07,
                 type: 'square', peak: 0.045, attack: 0.005, release: 0.06,
                 dest: [dly, out] });
      }
      if (step % 32 === 0) { // filtered noise sweep every ~14 s
        A.noise({ t: t, dur: 3.2, type: 'bandpass', f: 300, f2: 4200,
                  q: 1.5, peak: 0.05, attack: 1.2, release: 1.2 });
      }
    });
  }

  // -- tron: "neon synth". Bright 16th-note saw arpeggios through a resonant
  // sweeping lowpass, glowing detuned pads, soft pulse kick. Electric.
  function startTron(A) {
    var out = A.out();
    var chords = [[57, 60, 64], [53, 57, 60], [60, 64, 67], [55, 59, 62]]; // Am F C G
    // Resonant filter shared by the arp; LFO sweeps the cutoff for the glow.
    var filt = A.ctx.createBiquadFilter();
    filt.type = 'lowpass'; filt.frequency.value = 900; filt.Q.value = 6;
    filt.connect(out);
    A.track(filt);
    A.lfo(0.25, 2200, filt.frequency);

    var arpSeq = [0, 1, 2, 3, 2, 1, 2, 1]; // index 3 = root + octave
    A.schedule(0.15, function (step, t) {
      var ci = Math.floor(step / 32) % chords.length;
      var ch = chords[ci];
      if (step % 32 === 0) { // new glowing pad each chord change
        ch.forEach(function (m) {
          A.tone({ m: m, t: t, dur: 4.6, type: 'sawtooth', peak: 0.05,
                   attack: 1.4, release: 1.6, detune: 6, lp: 1600 });
        });
      }
      var n = arpSeq[step % arpSeq.length];
      var note = (n === 3) ? ch[0] + 12 : ch[n];
      A.tone({ m: note, t: t, dur: 0.14, type: 'sawtooth', peak: 0.11,
               attack: 0.005, release: 0.1, dest: filt });
      if (step % 4 === 0) { // soft pulse kick on the beat
        A.tone({ f: 150, f2: 48, t: t, dur: 0.16, type: 'sine',
                 peak: 0.4, attack: 0.004, release: 0.14 });
      }
    });
  }

  // -- cyberpunk: homepage default. Deep evolving minor-9th pads, sub-bass
  // drone, rain-like filtered noise, distant bell tones. Cinematic, vast.
  function startCyberpunk(A) {
    var out = A.out();
    var chords = [
      [57, 60, 64, 71], // Am9
      [53, 60, 64, 67], // Fmaj9
      [48, 55, 59, 62], // Cmaj9
      [52, 55, 59, 66]  // Em9
    ];

    // Rain: looped generated noise through a wandering bandpass.
    var rain = A.ctx.createBufferSource();
    rain.buffer = A.noiseBuffer(); rain.loop = true;
    var rf = A.ctx.createBiquadFilter();
    rf.type = 'bandpass'; rf.frequency.value = 5200; rf.Q.value = 0.4;
    var rg = A.ctx.createGain(); rg.gain.value = 0.012;
    rain.connect(rf); rf.connect(rg); rg.connect(out); rain.start();
    A.track(rain, rf, rg);
    A.lfo(0.11, 0.007, rg.gain);
    A.lfo(0.07, 900, rf.frequency);

    // Sub-bass drone with a very slow swell.
    var sub = A.ctx.createOscillator(); sub.type = 'sine'; sub.frequency.value = 55 * PITCH_RATIO; // A1 at 432Hz = 54Hz
    var sg = A.ctx.createGain(); sg.gain.value = 0.09;
    sub.connect(sg); sg.connect(out); sub.start();
    A.track(sub, sg);
    A.lfo(0.06, 0.035, sg.gain);

    var dly = A.delay(0.55, 0.45, 0.6); // long cavernous echo for bells

    A.schedule(9, function (step, t) {
      var ch = chords[step % chords.length];
      ch.forEach(function (m, i) { // slow-attack evolving pad
        A.tone({ m: m, t: t, dur: 11, type: 'triangle', peak: 0.055,
                 attack: 3.0, release: 4.0, detune: (i % 2 ? 5 : -5),
                 lp: 1500 });
      });
      for (var k = 0; k < 3; k++) { // distant bells: dry + cavern echo
        if (Math.random() < 0.6) {
          A.tone({ m: A.pick(ch) + 24, t: t + Math.random() * 8, dur: 4.5,
                   type: 'sine', peak: 0.07, attack: 0.01, release: 4.0,
                   dest: [dly, out] });
        }
      }
    });
  }

  // -- oceandeep: data engineering. Deep flowing pads, slow LFOs everywhere,
  // water-like filtered noise. Calm, weighty.
  function startOceandeep(A) {
    var out = A.out();
    var chords = [
      [50, 53, 57, 60], // Dm9
      [46, 50, 53, 57], // Bbmaj7
      [53, 57, 60, 64], // Fmaj7
      [48, 55, 59, 62]  // Cmaj9
    ];

    // Water: looped generated noise, bandpass swept by a slow LFO.
    var src = A.ctx.createBufferSource();
    src.buffer = A.noiseBuffer(); src.loop = true;
    var bf = A.ctx.createBiquadFilter();
    bf.type = 'bandpass'; bf.frequency.value = 800; bf.Q.value = 1;
    var ng = A.ctx.createGain(); ng.gain.value = 0.03;
    src.connect(bf); bf.connect(ng); ng.connect(out); src.start();
    A.track(src, bf, ng);
    A.lfo(0.08, 500, bf.frequency);
    A.lfo(0.11, 0.015, ng.gain);

    A.schedule(12, function (step, t) {
      var ch = chords[step % chords.length];
      ch.forEach(function (m, i) {
        A.tone({ m: m, t: t, dur: 14, type: 'triangle', peak: 0.06,
                 attack: 4.0, release: 5.0, detune: (i % 2 ? 4 : -4),
                 lp: 1100 });
      });
      if (Math.random() < 0.7) { // low swell tone from the chord root
        A.tone({ m: A.pick(ch) - 12, t: t + Math.random() * 6, dur: 5,
                 type: 'sine', peak: 0.08, attack: 0.02, release: 4.5 });
      }
    });
  }

  // -- vaporwave: web dev. Slowed-down maj7 chord stabs, chorus shimmer,
  // soft tape-like wash. Nostalgic.
  function startVaporwave(A) {
    var out = A.out();
    var chords = [
      [53, 57, 60, 64], // Fmaj7
      [52, 55, 59, 62], // Em7
      [50, 53, 57, 60], // Dm7
      [48, 52, 55, 59]  // Cmaj7
    ];

    // Soft wash underneath everything.
    var src = A.ctx.createBufferSource();
    src.buffer = A.noiseBuffer(); src.loop = true; src.playbackRate.value = 0.5;
    var wf = A.ctx.createBiquadFilter();
    wf.type = 'lowpass'; wf.frequency.value = 400;
    var wg = A.ctx.createGain(); wg.gain.value = 0.018;
    src.connect(wf); wf.connect(wg); wg.connect(out); src.start();
    A.track(src, wf, wg);
    A.lfo(0.09, 0.008, wg.gain);

    A.schedule(2.4, function (step, t) {
      var ch = chords[step % chords.length];
      ch.forEach(function (m) {
        var osc = A.tone({ m: m, t: t, dur: 2.2, type: 'sawtooth',
                           peak: 0.045, attack: 0.4, release: 1.6,
                           lp: 1900 });
        A.lfo(5.5, 5, osc.detune); // gentle chorus vibrato
      });
    });
  }

  // -- sacredgeo: math. Pure sine harmonics on phi-ratio intervals,
  // crystalline bell-like sequence. Pristine.
  function startSacredgeo(A) {
    var PHI = 1.6180339887;
    var base = 216 * PITCH_RATIO; // A3-ish reference at 432Hz; ratios do the talking
    var ratios = [1, PHI, PHI * PHI, PHI * PHI * PHI, PHI * PHI * PHI * PHI];
    A.schedule(1.4, function (step, t) {
      var r = ratios[step % ratios.length];
      A.tone({ f: base * r, t: t, dur: 3.4, type: 'sine',
               peak: 0.085, attack: 0.03, release: 3.0 });
      if (step % 8 === 0) { // low root swell every cycle
        A.tone({ f: 108 * PITCH_RATIO, t: t, dur: 5, type: 'sine',
                 peak: 0.10, attack: 1.5, release: 3.0 });
      }
      if (Math.random() < 0.3) { // faint high shimmer
        A.tone({ f: base * r * 4, t: t + 0.2, dur: 2.5, type: 'sine',
                 peak: 0.03, attack: 0.05, release: 2.2 });
      }
    });
  }

  // -- thrash: "aggressive thrash-metal" style. Palm-muted chugs on low E,
  // driving 16th-note riff in E minor, raw square-wave bite. Intense.
  // Original riff pattern; no sampled or copied material.
  function startThrash(A) {
    var out = A.out();
    // Chug riff: E minor, palm-mute feel via short square bursts + lowpass.
    var riff = [40, 40, 40, 43, 40, 40, 45, 43, 40, 40, 40, 43, 47, 45, 43, 42];
    A.schedule(0.16, function (step, t) {
      var m = riff[step % riff.length];
      // Palm-muted chug: short square, tight envelope, lowpassed bite.
      A.tone({ m: m, t: t, dur: 0.13, type: 'square', peak: 0.16,
               attack: 0.004, release: 0.09, lp: 1400 });
      // Sub thump underneath every 4th hit for weight.
      if (step % 4 === 0) {
        A.tone({ f: 82, f2: 40, t: t, dur: 0.18, type: 'sine',
                 peak: 0.35, attack: 0.004, release: 0.15 });
      }
      // Crash accent every 32 steps: noise burst.
      if (step % 32 === 24) {
        A.noise({ t: t, dur: 0.5, type: 'highpass', f: 5000,
                  peak: 0.06, attack: 0.005, release: 0.4 });
      }
    });
  }

  // -- grunge: "raw grunge" style. Detuned drop-D power chords, sludgy
  // chorus wash, heavy laid-back groove. Underground, unpolished.
  // Original chord progression; no sampled or copied material.
  function startGrunge(A) {
    var out = A.out();
    // Drop-D-ish power chord roots (D, F, Bb, C feel) — original progression.
    var chords = [[38, 45], [41, 48], [46, 53], [48, 55]];
    A.schedule(1.9, function (step, t) {
      var ch = chords[step % chords.length];
      ch.forEach(function (m) {
        // Two detuned saws per note for the sludgy wall.
        [-8, 8].forEach(function (det) {
          var osc = A.tone({ m: m, t: t, dur: 1.8, type: 'sawtooth',
                             peak: 0.07, attack: 0.05, release: 1.2,
                             detune: det, lp: 2200 });
          A.lfo(4.5, 7, osc.detune); // seasick chorus wobble
        });
      });
      // Loose kick + snare-ish backbeat.
      A.tone({ f: 120, f2: 45, t: t, dur: 0.22, type: 'sine',
               peak: 0.4, attack: 0.005, release: 0.18 });
      A.noise({ t: t + 0.95, dur: 0.18, type: 'bandpass', f: 1800,
                q: 0.8, peak: 0.12, attack: 0.004, release: 0.14 });
    });
  }

  // -- matrix: "industrial electronic" style. Dark pulsing bass synth,
  // glitchy minor arps, mechanical hats. Cold, relentless, digital.
  // Original patterns; no sampled or copied material.
  function startMatrix(A) {
    var out = A.out();
    var dly = A.delay(0.28, 0.4, 0.45);
    // Pulsing bass: 8th-note sidechain feel via amplitude gating.
    var bassNotes = [33, 33, 36, 33, 31, 33, 38, 36]; // A minor movement
    A.schedule(0.30, function (step, t) {
      var m = bassNotes[Math.floor(step / 2) % bassNotes.length];
      if (step % 2 === 0) {
        A.tone({ m: m, t: t, dur: 0.26, type: 'sawtooth', peak: 0.22,
                 attack: 0.01, release: 0.18, lp: 500 });
      }
      // Glitch arp: sparse, high, dry + echo.
      if (Math.random() < 0.22) {
        A.tone({ m: A.pick([69, 72, 76, 79, 81]), t: t, dur: 0.3,
                 type: 'square', peak: 0.06, attack: 0.005, release: 0.25,
                 lp: 3600, dest: [dly, out] });
      }
      // Mechanical hat tick.
      if (step % 2 === 1) {
        A.noise({ t: t, dur: 0.05, type: 'highpass', f: 8000,
                  peak: 0.05, attack: 0.002, release: 0.04 });
      }
      // Deep impact every 16 steps.
      if (step % 16 === 0) {
        A.tone({ f: 60, f2: 30, t: t, dur: 0.5, type: 'sine',
                 peak: 0.5, attack: 0.005, release: 0.4 });
      }
    });
  }

  // -- terminator: "mechanical relentless" style. Pounding industrial
  // kick, metallic percussion, ominous low synth motif. Unstoppable.
  // Original motif; no sampled or copied material.
  function startTerminator(A) {
    var out = A.out();
    // Relentless 4-on-floor industrial kick.
    A.schedule(0.42, function (step, t) {
      A.tone({ f: 130, f2: 42, t: t, dur: 0.24, type: 'sine',
               peak: 0.5, attack: 0.003, release: 0.2 });
      // Metallic clang off-beat.
      if (step % 2 === 1) {
        A.noise({ t: t, dur: 0.12, type: 'bandpass', f: 3200,
                  q: 4, peak: 0.07, attack: 0.003, release: 0.1 });
      }
      // Ominous motif every 8 steps: low minor-second grind.
      if (step % 8 === 0) {
        var root = 36; // C2
        [0, 1, 0, 1].forEach(function (iv, i) {
          A.tone({ m: root + iv, t: t + i * 0.42, dur: 0.4,
                   type: 'sawtooth', peak: 0.10, attack: 0.02,
                   release: 0.3, lp: 700, detune: -6 });
        });
      }
      // Hydraulic hiss sweep every 32 steps.
      if (step % 32 === 16) {
        A.noise({ t: t, dur: 1.6, type: 'bandpass', f: 900, f2: 3600,
                  q: 2, peak: 0.05, attack: 0.5, release: 0.8 });
      }
    });
  }

  // -- dune: "epic desert" style. Wind-like noise swells, deep taiko drums,
  // vast slow pads on a phrygian-dominant color. Boundless, ancient.
  // Original composition; no sampled or copied material.
  function startDune(A) {
    var out = A.out();
    // Desert wind: looped noise through a slow-wandering bandpass.
    var wind = A.ctx.createBufferSource();
    wind.buffer = A.noiseBuffer(); wind.loop = true;
    var wf = A.ctx.createBiquadFilter();
    wf.type = 'bandpass'; wf.frequency.value = 600; wf.Q.value = 0.5;
    var wg = A.ctx.createGain(); wg.gain.value = 0.05;
    wind.connect(wf); wf.connect(wg); wg.connect(out); wind.start();
    A.track(wind, wf, wg);
    A.lfo(0.05, 400, wf.frequency);
    A.lfo(0.08, 0.03, wg.gain);

    var dly = A.delay(0.7, 0.5, 0.55); // vast canyon echo
    // Phrygian-dominant flavor: E, F, G#, A — original progression.
    var pads = [
      [40, 41, 44, 47], // E phryg-dom cluster
      [38, 41, 45, 48], // D variation
      [40, 43, 47, 50]  // E major lift
    ];
    A.schedule(14, function (step, t) {
      var ch = pads[step % pads.length];
      ch.forEach(function (m, i) { // vast slow-attack swell
        A.tone({ m: m, t: t, dur: 16, type: 'triangle', peak: 0.05,
                 attack: 5.0, release: 6.0, detune: (i % 2 ? 4 : -4),
                 lp: 1200, dest: [dly, out] });
      });
      // Taiko hits: deep sine drops, irregular ritual pattern.
      var hits = [0, 3.5, 7, 10.5];
      hits.forEach(function (off) {
        A.tone({ f: 95, f2: 38, t: t + off, dur: 0.9, type: 'sine',
                 peak: 0.45, attack: 0.008, release: 0.7 });
      });
      // Distant horn call.
      if (Math.random() < 0.7) {
        A.tone({ m: A.pick(ch) - 12, t: t + 4 + Math.random() * 5,
                 dur: 6, type: 'sawtooth', peak: 0.045,
                 attack: 1.8, release: 3.5, lp: 900,
                 dest: [dly, out] });
      }
    });
  }

  // -- mozart: "bright classical" style. Elegant Alberti-bass piano patterns,
  // singing string-like lines, major-key clarity. Refined, academic.
  // Original composition; no sampled or copied material. 432Hz.
  function startMozart(A) {
    var out = A.out();
    // C major-ish progression: I - vi - IV - V (original voicings).
    var prog = [
      [48, 52, 55], // C
      [45, 48, 52], // Am
      [41, 45, 48], // F
      [43, 47, 50]  // G
    ];
    var dly = A.delay(0.4, 0.3, 0.35); // concert-hall-ish space
    A.schedule(2.2, function (step, t) {
      var ch = prog[step % prog.length];
      // Alberti bass: root-5th-3rd-5th pattern, piano-like triangle.
      var bass = [ch[0] - 12, ch[2] - 12, ch[1] - 12, ch[2] - 12];
      bass.forEach(function (m, i) {
        A.tone({ m: m, t: t + i * 0.5, dur: 0.5, type: 'triangle',
                 peak: 0.14, attack: 0.01, release: 0.4 });
      });
      // String-like chord pad: slow-attack saws, warm lowpass.
      ch.forEach(function (m) {
        A.tone({ m: m + 12, t: t, dur: 2.1, type: 'sawtooth',
                 peak: 0.035, attack: 0.6, release: 1.2, lp: 2200,
                 dest: [dly, out] });
      });
      // Sparkling melody note from the chord, high and light.
      if (Math.random() < 0.75) {
        A.tone({ m: A.pick(ch) + 24, t: t + 0.3 + Math.random() * 1.2,
                 dur: 0.9, type: 'sine', peak: 0.09,
                 attack: 0.02, release: 0.7, dest: [dly, out] });
      }
    });
  }

  // -- chopin: "nocturne" style. Expressive rubato piano, arpeggiated left
  // hand, lyrical singing right hand. Contemplative, emotional.
  // Original composition; no sampled or copied material. 432Hz.
  function startChopin(A) {
    var out = A.out();
    // E minor-ish progression with chromatic color (original).
    var prog = [
      [40, 43, 47, 52], // Em
      [45, 48, 52, 57], // Am
      [41, 45, 48, 53], // F
      [43, 47, 50, 55]  // G
    ];
    var dly = A.delay(0.65, 0.45, 0.5); // deep hall
    A.schedule(4.5, function (step, t) {
      var ch = prog[step % prog.length];
      // Left hand: slow rolling arpeggio, rubato timing feel.
      ch.forEach(function (m, i) {
        A.tone({ m: m, t: t + i * 0.55 + Math.random() * 0.08,
                 dur: 1.4, type: 'triangle', peak: 0.11,
                 attack: 0.02, release: 1.0 });
      });
      // Right hand: lyrical phrase, 2-3 notes, expressive.
      var mel = [ch[3] + 12, ch[2] + 12, ch[3] + 12 + 2];
      mel.forEach(function (m, i) {
        if (Math.random() < 0.8) {
          A.tone({ m: m, t: t + 1.2 + i * 0.9 + Math.random() * 0.15,
                   dur: 1.6, type: 'sine', peak: 0.10,
                   attack: 0.05, release: 1.2, dest: [dly, out] });
        }
      });
    });
  }

  // -- bach: "counterpoint" style. Two independent Baroque voices weaving
  // in imitation, clear and mathematical. For logic/mathematics.
  // Original subject; no sampled or copied material. 432Hz.
  function startBach(A) {
    var out = A.out();
    // Original 8-note subject in D minor-ish (all original).
    var subject = [62, 64, 65, 67, 65, 64, 62, 60];
    A.schedule(0.55, function (step, t) {
      var s = step % 32;
      // Voice 1: subject.
      var m1 = subject[s % subject.length] + (Math.floor(step / 32) % 2 ? 0 : -5);
      A.tone({ m: m1, t: t, dur: 0.5, type: 'triangle',
               peak: 0.13, attack: 0.01, release: 0.35 });
      // Voice 2: answer, offset by 4 steps (canonic imitation).
      if (step >= 4) {
        var s2 = (step - 4) % 32;
        var m2 = subject[s2 % subject.length] - 7 +
                 (Math.floor((step - 4) / 32) % 2 ? 0 : -5);
        A.tone({ m: m2, t: t, dur: 0.5, type: 'sine',
                 peak: 0.10, attack: 0.01, release: 0.35 });
      }
      // Harpsichord-ish continuo pulse every 8 steps.
      if (step % 8 === 0) {
        A.tone({ m: 38, t: t, dur: 0.4, type: 'square',
                 peak: 0.05, attack: 0.005, release: 0.3, lp: 1200 });
      }
    });
  }

  // -- beethoven: "dramatic" style. Stormy dynamic swells, powerful unison
  // hits, timpani rolls. Epic, fateful.
  // Original motifs; no sampled or copied material. 432Hz.
  function startBeethoven(A) {
    var out = A.out();
    // C minor-ish dramatic progression (original).
    var prog = [[48, 51, 55], [46, 50, 53], [48, 51, 55], [43, 47, 50]];
    A.schedule(3.2, function (step, t) {
      var ch = prog[step % prog.length];
      // Swell: strings crescendo from nothing.
      ch.forEach(function (m) {
        [-6, 6].forEach(function (det) {
          A.tone({ m: m, t: t, dur: 3.0, type: 'sawtooth',
                   peak: 0.06, attack: 1.8, release: 1.0,
                   detune: det, lp: 1800 });
        });
      });
      // Fateful unison hits: three short + one long.
      [0, 0.35, 0.7, 1.4].forEach(function (off, i) {
        var dur = (i === 3) ? 1.2 : 0.25;
        A.tone({ m: 36, t: t + off, dur: dur, type: 'square',
                 peak: 0.16, attack: 0.005, release: 0.2, lp: 900 });
      });
      // Timpani roll underneath.
      for (var k = 0; k < 6; k++) {
        A.tone({ f: 70 * PITCH_RATIO, f2: 45 * PITCH_RATIO,
                 t: t + k * 0.45, dur: 0.3, type: 'sine',
                 peak: 0.22, attack: 0.01, release: 0.25 });
      }
    });
  }

  // -- debussy: "impressionist" style. Whole-tone washes, blurred pentatonic
  // colors, bell-like resonance. Dreamlike, floating.
  // Original voicings; no sampled or copied material. 432Hz.
  function startDebussy(A) {
    var out = A.out();
    // Whole-tone clusters drifting (original).
    var washes = [
      [60, 62, 64, 66, 68],
      [58, 60, 62, 64, 66],
      [61, 63, 65, 67, 69]
    ];
    var dly = A.delay(0.8, 0.55, 0.6); // watery cathedral
    A.schedule(6, function (step, t) {
      var w = washes[step % washes.length];
      // Soft blurred attack on each tone.
      w.forEach(function (m, i) {
        A.tone({ m: m, t: t + i * 0.35 + Math.random() * 0.3,
                 dur: 5.5, type: 'sine', peak: 0.055,
                 attack: 1.5, release: 3.5, dest: [dly, out] });
      });
      // Distant bell from the pentatonic set.
      if (Math.random() < 0.7) {
        A.tone({ m: A.pick(w) + 12, t: t + 2 + Math.random() * 3,
                 dur: 4, type: 'triangle', peak: 0.06,
                 attack: 0.03, release: 3.5, dest: [dly, out] });
      }
    });
  }

  // -- synthwave: "retrowave" style. Driving 4/4 kick, gated snare, neon
  // lead arps, nostalgic 80s pulse. Distinct from tron: heavier, warmer.
  // Original patterns; no sampled or copied material. 432Hz.
  function startSynthwave(A) {
    var out = A.out();
    var bassLine = [33, 33, 33, 36, 33, 33, 31, 29]; // Am - G - F - E feel
    var dly = A.delay(0.32, 0.35, 0.4);
    A.schedule(0.24, function (step, t) {
      // Four-on-floor kick.
      A.tone({ f: 140 * PITCH_RATIO, f2: 45 * PITCH_RATIO,
               t: t, dur: 0.18, type: 'sine',
               peak: 0.45, attack: 0.004, release: 0.15 });
      // Gated snare on 2 & 4.
      if (step % 4 === 1 || step % 4 === 3) {
        A.noise({ t: t, dur: 0.16, type: 'bandpass', f: 1900,
                  q: 0.7, peak: 0.16, attack: 0.003, release: 0.13 });
      }
      // Driving 8th-note bass.
      if (step % 2 === 0) {
        var m = bassLine[Math.floor(step / 2) % bassLine.length];
        A.tone({ m: m, t: t, dur: 0.2, type: 'sawtooth', peak: 0.18,
                 attack: 0.01, release: 0.15, lp: 700 });
      }
      // Neon lead arp every bar, dry + echo.
      if (step % 16 === 0) {
        var arpNotes = [69, 72, 76, 79, 76, 72];
        arpNotes.forEach(function (n, i) {
          A.tone({ m: n, t: t + i * 0.24, dur: 0.22, type: 'square',
                   peak: 0.07, attack: 0.01, release: 0.18, lp: 3200,
                   dest: [dly, out] });
        });
      }
    });
  }

  // -- techno: "minimal" style. Deep hypnotic bassline, sparse hats,
  // atmospheric dub pads. Focus/study, late-night.
  // Original patterns; no sampled or copied material. 432Hz.
  function startTechno(A) {
    var out = A.out();
    var bassPat = [33, 0, 33, 0, 33, 36, 0, 31]; // hypnotic loop
    var dly = A.delay(0.45, 0.5, 0.45);
    A.schedule(0.30, function (step, t) {
      // Deep rolling kick (softer than synthwave).
      if (step % 2 === 0) {
        A.tone({ f: 120 * PITCH_RATIO, f2: 42 * PITCH_RATIO,
                 t: t, dur: 0.2, type: 'sine',
                 peak: 0.38, attack: 0.005, release: 0.17 });
      }
      // Hypnotic bass note.
      var b = bassPat[step % bassPat.length];
      if (b) {
        A.tone({ m: b, t: t, dur: 0.26, type: 'sawtooth', peak: 0.14,
                 attack: 0.02, release: 0.2, lp: 320 });
      }
      // Sparse hat.
      if (step % 4 === 2) {
        A.noise({ t: t, dur: 0.04, type: 'highpass', f: 9000,
                  peak: 0.04, attack: 0.002, release: 0.03 });
      }
      // Dubby atmospheric stab every 32 steps.
      if (step % 32 === 16) {
        [57, 60, 64].forEach(function (m) {
          A.tone({ m: m, t: t, dur: 1.8, type: 'triangle', peak: 0.05,
                   attack: 0.4, release: 1.2, lp: 1400,
                   dest: [dly, out] });
        });
      }
    });
  }

  var THEMES = {
    cybersecurity: { label: 'Cybersecurity', desc: 'Dark hacker synthwave — low pulse, sparse minor arps, data blips.', start: startCybersecurity },
    tron:           { label: 'Tron',           desc: 'Neon synth — bright 16th arpeggios, resonant sweeps.',              start: startTron },
    cyberpunk:      { label: 'Cyberpunk',      desc: 'Homepage default — deep minor-9th pads, rain, distant bells.',     start: startCyberpunk },
    oceandeep:      { label: 'Ocean Deep',     desc: 'Data engineering — deep flowing pads, water-like noise.',          start: startOceandeep },
    vaporwave:      { label: 'Vaporwave',      desc: 'Web dev — slowed maj7 stabs, chorus shimmer, nostalgic.',          start: startVaporwave },
    sacredgeo:      { label: 'Sacred Geometry', desc: 'Math — pure sine harmonics on phi-ratio intervals.',              start: startSacredgeo },
    thrash:         { label: 'Thrash',         desc: 'Aggressive thrash-metal style — palm-muted chugs, driving E-minor riff.', start: startThrash },
    grunge:         { label: 'Grunge',         desc: 'Raw grunge style — detuned drop-D power chords, sludgy groove.',   start: startGrunge },
    matrix:         { label: 'Matrix',         desc: 'Industrial electronic — dark pulsing bass, glitch arps.',          start: startMatrix },
    terminator:     { label: 'Terminator',     desc: 'Mechanical relentless — pounding kick, metallic percussion.',      start: startTerminator },
    dune:           { label: 'Dune',           desc: 'Epic desert — wind swells, taiko drums, vast pads.',                start: startDune },
    mozart:         { label: 'Mozart',         desc: 'Bright classical — elegant Alberti bass, singing strings.',         start: startMozart },
    chopin:         { label: 'Chopin',         desc: 'Nocturne style — expressive rubato piano, lyrical melody.',         start: startChopin },
    bach:           { label: 'Bach',           desc: 'Counterpoint — two Baroque voices in canonic imitation.',            start: startBach },
    beethoven:      { label: 'Beethoven',      desc: 'Dramatic — stormy swells, fateful unison hits, timpani.',          start: startBeethoven },
    debussy:        { label: 'Debussy',        desc: 'Impressionist — whole-tone washes, dreamlike bells.',              start: startDebussy },
    synthwave:      { label: 'Synthwave',      desc: 'Retrowave — driving 4/4, gated snare, neon lead arps.',            start: startSynthwave },
    techno:         { label: 'Techno',         desc: 'Minimal — deep hypnotic bassline, dubby atmospheric stabs.',       start: startTechno }
  };

  /* ------------------------------ transport ----------------------------- */
  function play(name) {
    name = THEMES[name] ? name : (loadPref().theme || DEFAULT_THEME);
    ensureCtx();
    if (!ctx) return false;
    if (state.playing && state.theme === name) return true; // already there
    state.stopToken++; // invalidate any pending fade-out completion
    var begin = function () {
      cleanup();
      state.themeGain = ctx.createGain();
      state.themeGain.gain.value = 0.0001;
      state.themeGain.connect(master);
      THEMES[name].start(makeApi());
      var t = ctx.currentTime; // smooth fade-in
      state.themeGain.gain.setValueAtTime(0.0001, t);
      state.themeGain.gain.exponentialRampToValueAtTime(1.0, t + FADE_IN);
      state.playing = true;
      state.theme = name;
      savePref(true, name);
    };
    if (state.playing) stop(begin); // crossfade: fade out, then begin
    else begin();
    return true;
  }

  function stop(done) {
    if (!state.playing) { if (done) done(); return; }
    var token = ++state.stopToken;
    var tg = state.themeGain;
    savePref(false, state.theme);
    state.playing = false;
    if (tg && ctx) { // smooth fade-out
      var t = ctx.currentTime;
      try {
        tg.gain.cancelScheduledValues(t);
        tg.gain.setValueAtTime(Math.max(0.0001, tg.gain.value), t);
        tg.gain.exponentialRampToValueAtTime(0.0001, t + FADE_OUT);
      } catch (e) {}
    }
    after(FADE_OUT * 1000 + 150, function () {
      if (token !== state.stopToken) return; // superseded by a newer play()
      cleanup();
      if (done) done();
    });
  }

  function setTheme(name) {
    if (!THEMES[name]) return false;
    if (state.playing) return play(name); // crossfade while playing
    savePref(loadPref().enabled, name);   // remember for the next play()
    return true;
  }

  function toggle() {
    if (state.playing) { stop(); return false; }
    play(loadPref().theme || DEFAULT_THEME);
    return true;
  }

  // Armed autoplay (user-approved 2026-10-10): attempt playback immediately;
  // if the browser blocks it (no user gesture yet), wait for the FIRST
  // pointerdown/keydown/touchstart anywhere on the page, then start.
  // After that first interaction, audio plays seamlessly. A master mute
  // toggle in the nav remains available at all times.
  var _armed = false;  function arm(themeName) {
    if (_armed || state.playing) return;
    _armed = true;
    var theme = (themeName && THEMES[themeName]) ? themeName
              : (loadPref().theme || DEFAULT_THEME);
    function firstGesture() {
      try { play(theme); } catch (e) {}
    }
    // Try immediately — succeeds if a gesture already happened.
    try {
      if (play(theme)) { _armed = false; return; }
    } catch (e) {}
    // Otherwise wait for the first user interaction anywhere.
    function onFirst() {
      _armed = false;
      try {
        document.removeEventListener('pointerdown', onFirst, true);
        document.removeEventListener('keydown', onFirst, true);
        document.removeEventListener('touchstart', onFirst, true);
      } catch (e) {}
      firstGesture();
    }
    try {
      document.addEventListener('pointerdown', onFirst, true);
      document.addEventListener('keydown', onFirst, true);
      document.addEventListener('touchstart', onFirst, true);
    } catch (e) { /* non-DOM environment */ }
  }

  function setVolume(v) {
    v = clamp(parseFloat(v) || 0, 0, 1);
    state.volume = v;
    lsSet(LS_VOLUME, String(v));
    if (master && ctx) master.gain.setTargetAtTime(v, ctx.currentTime, 0.4);
  }

  // Topic → audio theme mapping. Each site topic gets the most fitting
  // original ambient style. Falls back to DEFAULT_THEME.
  var TOPIC_AUDIO = {
    'cybersecurity':  'cybersecurity', // dark hacker synthwave
    'system-design':  'cyberpunk',      // neon cyberpunk
    'networking':     'tron',           // neon synth grid
    'cloud-devops':   'terminator',    // mechanical automation
    'ai-ml':          'matrix',         // industrial electronic AI
    'data-eng':       'oceandeep',      // deep data currents
    'programming':    'thrash',         // aggressive hacker energy
    'databases':      'sacredgeo',      // crystalline structure
    'linux-systems':  'terminator',    // relentless systems
    'math':           'sacredgeo',      // phi-ratio purity
    'web-dev':        'vaporwave',      // nostalgic web
    'blockchain':     'matrix',         // digital ledger pulse
    'crypto':         'tron',           // neon money
    'cybernetics':    'matrix',         // control-system pulse
    'esoteric':       'debussy',        // impressionist mysticism
    'om':             'dune'            // epic expansive meditation
  };
  function topicTheme(topic) {
    return TOPIC_AUDIO[topic] || DEFAULT_THEME;
  }

  // Device tier detection for performance scaling.
  // Returns 'ultrawide' | 'desktop' | 'mobile'.
  // Themes can check ILAmbient.deviceTier() to skip decorative layers.
  function deviceTier() {
    try {
      var w = window.innerWidth || 0;
      var aspect = w / (window.innerHeight || 1);
      if (aspect >= 2.9 || w >= 3440) return 'ultrawide';
      if (w <= 640) return 'mobile';
    } catch (e) {}
    return 'desktop';
  }

  // True when the device is constrained (mobile) — themes should reduce
  // voice counts, skip shimmer/delay layers, and prefer simpler patterns.
  function isLowPower() {
    try {
      if (deviceTier() === 'mobile') return true;
      var cores = window.navigator.hardwareConcurrency || 8;
      if (cores <= 4) return true;
    } catch (e) {}
    return false;
  }

  /* ------------------------------- public ------------------------------- */
  var api = {
    supported: true,
    themes: {},
    play: play,
    stop: stop,
    setTheme: setTheme,
    toggle: toggle,
    arm: arm,
    topicTheme: topicTheme,
    deviceTier: deviceTier,
    isLowPower: isLowPower,
    setVolume: setVolume,
    getVolume: function () { return state.volume; },
    isPlaying: function () { return state.playing; },
    currentTheme: function () { return state.theme; },
    saved: loadPref,
    // Live frequency data for the floating widget equalizer.
    // Returns a Uint8Array (length = analyser.frequencyBinCount) or null.
    getAnalyser: function () { return analyser; },
    getFrequencyData: function () {
      if (!analyser) return null;
      var arr = new Uint8Array(analyser.frequencyBinCount);
      analyser.getByteFrequencyData(arr);
      return arr;
    }
  };
  Object.keys(THEMES).forEach(function (k) {
    api.themes[k] = { label: THEMES[k].label, desc: THEMES[k].desc };
  });
  global.ILAmbient = api;

})(typeof window !== 'undefined' ? window : this);
