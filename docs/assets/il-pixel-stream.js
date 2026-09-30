/**
 * IL Pixel Streaming client — production-grade signaling/reconnect shell.
 * Honest: never fakes a live UE host or fleet. CSP-safe (no eval).
 * Config: ?signaling= | data-ps-signaling | localStorage.il-ps-signaling | IL_LOCAL_CONFIG
 */
(function (g) {
  'use strict';

  var LS_KEY = 'il-ps-signaling';
  var MAX_BACKOFF_MS = 30000;
  var state = {
    ws: null,
    pc: null,
    signaling: '',
    wantsConnect: false,
    attempt: 0,
    backoffTimer: null,
    destroyed: false
  };

  function qs(name) {
    try {
      return new URL(g.location.href).searchParams.get(name) || '';
    } catch (e) {
      return '';
    }
  }

  function log(msg) {
    var el = document.getElementById('ps-log');
    if (!el) return;
    var t = new Date().toLocaleTimeString();
    el.textContent += '[' + t + '] ' + msg + '\n';
    el.scrollTop = el.scrollHeight;
  }

  function setStatus(s) {
    var el = document.getElementById('ps-status');
    if (el) el.textContent = s;
  }

  function resolveSignaling() {
    var fromQ = qs('signaling') || qs('ps') || qs('pixel');
    if (fromQ) return fromQ.trim();
    var host = document.getElementById('ps-host');
    if (host) {
      var d = host.getAttribute('data-ps-signaling');
      if (d && d.trim()) return d.trim();
    }
    var input = document.getElementById('ps-signaling-input');
    if (input && input.value && input.value.trim()) return input.value.trim();
    try {
      var ls = localStorage.getItem(LS_KEY);
      if (ls && ls.trim()) return ls.trim();
    } catch (e) {}
    if (g.IL_LOCAL_CONFIG && g.IL_LOCAL_CONFIG.pixelStreamingSignaling) {
      return String(g.IL_LOCAL_CONFIG.pixelStreamingSignaling).trim();
    }
    return '';
  }

  function persistSignaling(url) {
    try {
      if (url) localStorage.setItem(LS_KEY, url);
      else localStorage.removeItem(LS_KEY);
    } catch (e) {}
    var host = document.getElementById('ps-host');
    if (host) host.setAttribute('data-ps-signaling', url || '');
    var input = document.getElementById('ps-signaling-input');
    if (input && url) input.value = url;
  }

  function clearMedia() {
    var video = document.getElementById('ps-video');
    if (video) {
      try {
        if (video.srcObject) {
          video.srcObject.getTracks().forEach(function (t) {
            try { t.stop(); } catch (e) {}
          });
        }
      } catch (e2) {}
      video.srcObject = null;
      video.classList.remove('is-live');
    }
  }

  function teardownPeer() {
    if (state.pc) {
      try { state.pc.close(); } catch (e) {}
      state.pc = null;
    }
    if (state.ws) {
      try {
        state.ws.onopen = null;
        state.ws.onmessage = null;
        state.ws.onerror = null;
        state.ws.onclose = null;
        if (state.ws.readyState === 0 || state.ws.readyState === 1) state.ws.close();
      } catch (e2) {}
      state.ws = null;
    }
    clearMedia();
  }

  function scheduleReconnect() {
    if (!state.wantsConnect || state.destroyed) return;
    if (state.backoffTimer) clearTimeout(state.backoffTimer);
    state.attempt += 1;
    var delay = Math.min(MAX_BACKOFF_MS, 1000 * Math.pow(2, Math.min(state.attempt - 1, 5)));
    setStatus('Reconnect in ' + Math.round(delay / 1000) + 's (attempt ' + state.attempt + ') — no fake fleet');
    log('Scheduling reconnect in ' + delay + 'ms (honest backoff; UE host must exist).');
    state.backoffTimer = setTimeout(function () {
      state.backoffTimer = null;
      if (state.wantsConnect && !state.destroyed) connect(state.signaling, { silent: true });
    }, delay);
  }

  function showStub() {
    var stubSlot = document.getElementById('ps-stub-slot');
    var host = document.getElementById('ps-host');
    if (g.ILSceneKit && ILSceneKit.pixelStreamEmbed) {
      ILSceneKit.pixelStreamEmbed(stubSlot || host, '', { title: 'UE5 Pixel Streaming' });
    } else if (stubSlot) {
      stubSlot.innerHTML =
        '<div class="il-ps-empty" role="status">' +
        '<p class="il-ps-empty__kicker">Connect a Unreal Pixel Streaming host</p>' +
        '<p>No signaling URL. Set env on the lab GPU host, then paste <code>ws://</code> / <code>wss://</code> below. ' +
        'See <a href="/ops/PIXEL-STREAMING-DEV.md">PIXEL-STREAMING-DEV</a>.</p>' +
        '</div>';
    }
  }

  function attemptWebRtc(signaling) {
    var video = document.getElementById('ps-video');
    if (!/^wss?:\/\//i.test(signaling)) {
      log('Signaling is not ws(s) — using embed mount (iframe/player URL).');
      return false;
    }
    if (typeof RTCPeerConnection === 'undefined') {
      log('RTCPeerConnection unavailable — cannot negotiate WebRTC.');
      setStatus('WebRTC unavailable in this browser');
      return false;
    }
    setStatus('Connecting signaling…');
    log('Opening WebSocket signaling: ' + signaling);
    teardownPeer();
    var ws;
    try {
      ws = new WebSocket(signaling);
    } catch (err) {
      log('WebSocket construct failed: ' + err);
      setStatus('Signaling construct failed');
      scheduleReconnect();
      return true;
    }
    state.ws = ws;
    ws.addEventListener('open', function () {
      state.attempt = 0;
      log('Signaling socket open — sending player connect (UE PS minimal).');
      setStatus('Signaling open — negotiating…');
      var stub = document.getElementById('ps-stub-slot');
      if (stub) stub.innerHTML = '';
      try {
        ws.send(JSON.stringify({ type: 'connect', peerConnectionOptions: {} }));
      } catch (e) {
        log('send connect failed: ' + e);
      }
    });
    ws.addEventListener('message', function (ev) {
      var raw = ev.data;
      var msg;
      try {
        msg = typeof raw === 'string' ? JSON.parse(raw) : raw;
      } catch (e) {
        log('Non-JSON signaling frame');
        return;
      }
      var type = msg.type || msg.Type || '';
      log('Signaling message: ' + type);
      if (type === 'offer' && msg.sdp) {
        var pc = new RTCPeerConnection({ iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] });
        state.pc = pc;
        pc.ontrack = function (tev) {
          if (video && tev.streams && tev.streams[0]) {
            video.srcObject = tev.streams[0];
            video.classList.add('is-live');
            setStatus('Live Pixel Streaming track');
            log('Remote media track attached.');
          }
        };
        pc.onicecandidate = function (c) {
          if (c.candidate && ws.readyState === 1) {
            ws.send(JSON.stringify({ type: 'iceCandidate', candidate: c.candidate }));
          }
        };
        pc.setRemoteDescription({ type: 'offer', sdp: msg.sdp })
          .then(function () {
            return pc.createAnswer();
          })
          .then(function (answer) {
            return pc.setLocalDescription(answer);
          })
          .then(function () {
            ws.send(JSON.stringify({ type: 'answer', sdp: pc.localDescription.sdp }));
            log('Answer sent.');
          })
          .catch(function (err) {
            log('SDP negotiate failed: ' + err);
            setStatus('SDP negotiate failed — is UE streamer up?');
          });
      }
      if ((type === 'iceCandidate' || type === 'iceCandidateResponse') && msg.candidate && state.pc) {
        state.pc.addIceCandidate(msg.candidate).catch(function () {});
      }
    });
    ws.addEventListener('error', function () {
      log('Signaling error (expected if no lab host).');
      setStatus('Signaling error — scaffold ready, no live UE host');
    });
    ws.addEventListener('close', function () {
      log('Signaling closed.');
      var videoEl = document.getElementById('ps-video');
      if (!videoEl || !videoEl.srcObject) {
        setStatus('Signaling closed — no live stream');
      }
      if (state.wantsConnect) scheduleReconnect();
    });
    return true;
  }

  function connect(url, opts) {
    opts = opts || {};
    url = (url || '').trim();
    if (!url) {
      setStatus('Scaffold ready — connect a Unreal Pixel Streaming host');
      log('No signaling URL. Paste ws(s)://… or see /ops/PIXEL-STREAMING-DEV.md');
      showStub();
      return;
    }
    state.signaling = url;
    state.wantsConnect = true;
    persistSignaling(url);
    var host = document.getElementById('ps-host');
    if (host) host.setAttribute('data-ps-signaling', url);
    if (!opts.silent) log('Signaling configured: ' + url);
    var usedWs = attemptWebRtc(url);
    if (!usedWs && g.ILSceneKit && ILSceneKit.pixelStreamEmbed) {
      setStatus('Mounting signaling URL via embed');
      var stubSlot = document.getElementById('ps-stub-slot');
      ILSceneKit.pixelStreamEmbed(stubSlot || host, url, { title: 'UE5 Pixel Streaming' });
    }
  }

  function disconnect() {
    state.wantsConnect = false;
    if (state.backoffTimer) {
      clearTimeout(state.backoffTimer);
      state.backoffTimer = null;
    }
    teardownPeer();
    setStatus('Disconnected — host not claimed online');
    log('Disconnected by user. No fleet implied.');
    showStub();
  }

  function clearConfig() {
    disconnect();
    persistSignaling('');
    var input = document.getElementById('ps-signaling-input');
    if (input) input.value = '';
    setStatus('Scaffold ready — set signaling when UE5 streamer is up');
    log('Cleared saved signaling.');
  }

  function boot() {
    var input = document.getElementById('ps-signaling-input');
    var initial = resolveSignaling();
    if (input && initial) input.value = initial;
    else if (input && !input.value) {
      try {
        var ls = localStorage.getItem(LS_KEY);
        if (ls) input.value = ls;
      } catch (e) {}
    }

    var btnConnect = document.getElementById('ps-btn-connect');
    var btnDisconnect = document.getElementById('ps-btn-disconnect');
    var btnClear = document.getElementById('ps-btn-clear');
    var btnSave = document.getElementById('ps-btn-save');

    if (btnConnect) {
      btnConnect.addEventListener('click', function () {
        var url = (input && input.value) || resolveSignaling();
        state.attempt = 0;
        connect(url);
      });
    }
    if (btnDisconnect) btnDisconnect.addEventListener('click', disconnect);
    if (btnClear) btnClear.addEventListener('click', clearConfig);
    if (btnSave) {
      btnSave.addEventListener('click', function () {
        var url = (input && input.value.trim()) || '';
        persistSignaling(url);
        log(url ? 'Saved signaling to localStorage.' : 'Cleared localStorage signaling.');
        setStatus(url ? 'Signaling saved (not connected)' : 'Scaffold ready');
      });
    }
    if (input) {
      input.addEventListener('keydown', function (ev) {
        if (ev.key === 'Enter') {
          state.attempt = 0;
          connect(input.value);
        }
      });
    }

    if (initial) {
      connect(initial);
    } else {
      setStatus('Scaffold ready — connect a Unreal Pixel Streaming host');
      log('No signaling URL. Pass ?signaling=wss://host/…, paste below, or see PIXEL-STREAMING-DEV.');
      showStub();
    }
  }

  g.ILPixelStream = {
    connect: connect,
    disconnect: disconnect,
    clearConfig: clearConfig,
    resolveSignaling: resolveSignaling,
    VERSION: '1.0.0'
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})(typeof window !== 'undefined' ? window : this);
