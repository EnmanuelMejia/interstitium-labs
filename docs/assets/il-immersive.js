/**
 * IL Immersive Player — 3D-first stage for lectures, cert labs, sims, non-cert.
 * Procedural WebGL now (CSP-safe). Optional vendored Three+glTF + Unreal Pixel Streaming.
 * Shares window.ILSceneKit with Lab Muse 3D. Interstitium original art/code.
 */
(function (g) {
  'use strict';

  function K() { return g.ILSceneKit || null; }

  var VERT = [
    'attribute vec3 aPos;',
    'attribute vec3 aNrm;',
    'uniform mat4 uMVP;',
    'uniform mat3 uN;',
    'varying vec3 vN;',
    'varying vec3 vP;',
    'void main(){',
    '  vN = normalize(uN * aNrm);',
    '  vP = aPos;',
    '  gl_Position = uMVP * vec4(aPos, 1.0);',
    '}'
  ].join('\n');

  var FRAG = [
    'precision mediump float;',
    'varying vec3 vN;',
    'varying vec3 vP;',
    'uniform vec3 uColor;',
    'uniform vec3 uEmit;',
    'uniform float uGlow;',
    'uniform float uTime;',
    'void main(){',
    '  vec3 N = normalize(vN);',
    '  vec3 L = normalize(vec3(0.4, 0.9, 0.35));',
    '  vec3 V = normalize(vec3(0.0, 0.2, 1.0));',
    '  float ndl = max(dot(N, L), 0.0);',
    '  float rim = pow(1.0 - max(dot(N, V), 0.0), 2.2);',
    '  vec3 gold = vec3(0.831, 0.659, 0.325);',
    '  vec3 col = uColor * (0.2 + 0.8 * ndl) + uEmit * uGlow + gold * rim * 0.5;',
    '  col += 0.03 * sin(vP.y * 12.0 + uTime * 1.5);',
    '  gl_FragColor = vec4(col, 0.98);',
    '}'
  ].join('\n');

  function pushTri(pos, nrm, ax, ay, az, bx, by, bz, cx, cy, cz) {
    var ux = bx - ax, uy = by - ay, uz = bz - az;
    var vx = cx - ax, vy = cy - ay, vz = cz - az;
    var nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
    var len = Math.hypot(nx, ny, nz) || 1;
    nx /= len; ny /= len; nz /= len;
    pos.push(ax, ay, az, bx, by, bz, cx, cy, cz);
    nrm.push(nx, ny, nz, nx, ny, nz, nx, ny, nz);
  }

  function boxGeo(sx, sy, sz) {
    var hx = sx / 2, hy = sy / 2, hz = sz / 2, pos = [], nrm = [];
    pushTri(pos, nrm, -hx, -hy, hz, hx, -hy, hz, hx, hy, hz);
    pushTri(pos, nrm, -hx, -hy, hz, hx, hy, hz, -hx, hy, hz);
    pushTri(pos, nrm, hx, -hy, -hz, -hx, -hy, -hz, -hx, hy, -hz);
    pushTri(pos, nrm, hx, -hy, -hz, -hx, hy, -hz, hx, hy, -hz);
    pushTri(pos, nrm, -hx, hy, -hz, -hx, hy, hz, hx, hy, hz);
    pushTri(pos, nrm, -hx, hy, -hz, hx, hy, hz, hx, hy, -hz);
    pushTri(pos, nrm, -hx, -hy, hz, -hx, -hy, -hz, hx, -hy, -hz);
    pushTri(pos, nrm, -hx, -hy, hz, hx, -hy, -hz, hx, -hy, hz);
    pushTri(pos, nrm, hx, -hy, hz, hx, -hy, -hz, hx, hy, -hz);
    pushTri(pos, nrm, hx, -hy, hz, hx, hy, -hz, hx, hy, hz);
    pushTri(pos, nrm, -hx, -hy, -hz, -hx, -hy, hz, -hx, hy, hz);
    pushTri(pos, nrm, -hx, -hy, -hz, -hx, hy, hz, -hx, hy, -hz);
    return { pos: new Float32Array(pos), nrm: new Float32Array(nrm), count: pos.length / 3 };
  }

  function torusGeo(R, r, seg, tube) {
    var pos = [], nrm = [], i, j;
    for (i = 0; i < seg; i++) {
      var a0 = (i / seg) * Math.PI * 2;
      var a1 = ((i + 1) / seg) * Math.PI * 2;
      for (j = 0; j < tube; j++) {
        var b0 = (j / tube) * Math.PI * 2;
        var b1 = ((j + 1) / tube) * Math.PI * 2;
        function pt(a, b) {
          var x = (R + r * Math.cos(b)) * Math.cos(a);
          var y = r * Math.sin(b);
          var z = (R + r * Math.cos(b)) * Math.sin(a);
          var nx = Math.cos(a) * Math.cos(b);
          var ny = Math.sin(b);
          var nz = Math.sin(a) * Math.cos(b);
          return [x, y, z, nx, ny, nz];
        }
        var p00 = pt(a0, b0), p10 = pt(a1, b0), p01 = pt(a0, b1), p11 = pt(a1, b1);
        pushTri(pos, nrm, p00[0], p00[1], p00[2], p10[0], p10[1], p10[2], p11[0], p11[1], p11[2]);
        pushTri(pos, nrm, p00[0], p00[1], p00[2], p11[0], p11[1], p11[2], p01[0], p01[1], p01[2]);
      }
    }
    return { pos: new Float32Array(pos), nrm: new Float32Array(nrm), count: pos.length / 3 };
  }

  function kindDefaults(kind) {
    kind = String(kind || 'lecture').toLowerCase();
    if (kind === 'cert' || kind === 'lab' || kind === 'cert-lab') {
      return { label: 'Cert lab stage', spin: 0.35, glow: 0.55, ring: 1.15 };
    }
    if (kind === 'sim' || kind === 'simulation') {
      return { label: 'Simulation stage', spin: 0.7, glow: 0.75, ring: 1.35 };
    }
    if (kind === 'non-cert' || kind === 'noncert') {
      return { label: 'Open lab stage', spin: 0.45, glow: 0.5, ring: 1.2 };
    }
    return { label: 'Lecture stage', spin: 0.25, glow: 0.4, ring: 1.05 };
  }

  function makeMesh(gl, geo) {
    var pos = gl.createBuffer();
    var nrm = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, pos);
    gl.bufferData(gl.ARRAY_BUFFER, geo.pos, gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, nrm);
    gl.bufferData(gl.ARRAY_BUFFER, geo.nrm, gl.STATIC_DRAW);
    return { pos: pos, nrm: nrm, count: geo.count };
  }

  function cssFallback(stage) {
    stage.innerHTML = '<div class="il-immersive__fallback" aria-hidden="true"><div class="il-immersive__mono"></div></div>';
  }

  function mount(host, opts) {
    opts = opts || {};
    if (!host) return null;
    if (host.getAttribute('data-il-immersive-ready')) return host.__ilImmersive || null;

    var kit = K();
    var kind = opts.kind || host.getAttribute('data-kind') || host.getAttribute('data-il-immersive') || 'lecture';
    if (kind === '1' || kind === 'true') kind = 'lecture';
    var meta = kindDefaults(kind);
    var gltfUrl = opts.gltf || host.getAttribute('data-gltf') || '';
    var psUrl = opts.pixelStream || host.getAttribute('data-ps-signaling') || '';
    var engine = String(opts.engine || host.getAttribute('data-engine') || 'web').toLowerCase();
    var title = opts.title || host.getAttribute('data-title') || meta.label;

    host.classList.add('il-immersive');
    host.setAttribute('data-il-immersive-ready', '1');
    host.innerHTML =
      '<div class="il-immersive__stage" data-imm-stage></div>' +
      '<div class="il-immersive__hud">' +
      '<span class="il-immersive__badge">' + title + '</span>' +
      '<span class="il-immersive__engine" data-imm-engine>WebGL</span>' +
      '</div>';

    var stage = host.querySelector('[data-imm-stage]');
    var engineEl = host.querySelector('[data-imm-engine]');

    var api = {
      host: host,
      kind: kind,
      setAmp: function () {},
      setStatus: function () {},
      destroy: function () {
        host.removeAttribute('data-il-immersive-ready');
        host.__ilImmersive = null;
        host.innerHTML = '';
      }
    };
    host.__ilImmersive = api;

    if (engine === 'unreal' || engine === 'pixel' || engine === 'ue5' || psUrl) {
      if (engineEl) engineEl.textContent = 'Unreal PS';
      if (kit && kit.pixelStreamEmbed) kit.pixelStreamEmbed(stage, psUrl || '', { title: title });
      else cssFallback(stage);
      return api;
    }

    if (!kit || kit.prefersReducedMotion() || !g.WebGLRenderingContext) {
      if (engineEl) engineEl.textContent = 'CSS';
      cssFallback(stage);
      return api;
    }

    if (gltfUrl) {
      kit.emitSceneEvent('il-immersive-gltf-pending', { url: gltfUrl, kind: kind });
      kit.loadGltf(gltfUrl).then(function (res) {
        if (res && res.ok) {
          if (engineEl) engineEl.textContent = 'Three/glTF';
          stage.setAttribute('data-gltf-loaded', '1');
          kit.emitSceneEvent('il-immersive-gltf', { url: gltfUrl, ok: true });
        }
      }).catch(function () {});
    }

    /* Procedural WebGL stage (default — works without Three vendor) */
    var canvas = document.createElement('canvas');
    canvas.setAttribute('aria-hidden', 'true');
    stage.appendChild(canvas);
    var gl = canvas.getContext('webgl', { alpha: true, antialias: true, powerPreference: 'high-performance' })
      || canvas.getContext('experimental-webgl');
    if (!gl) {
      if (engineEl) engineEl.textContent = 'CSS';
      cssFallback(stage);
      return api;
    }

    var prog = kit.linkProgram(gl, VERT, FRAG);
    if (!prog) {
      cssFallback(stage);
      return api;
    }

    if (engineEl) engineEl.textContent = gltfUrl ? 'WebGL · glTF pending' : 'WebGL';

    var mobile = kit.isMobile();
    var pedestal = makeMesh(gl, boxGeo(1.2, 0.12, 1.2));
    var pillar = makeMesh(gl, boxGeo(0.28, 1.0, 0.28));
    var ring = makeMesh(gl, torusGeo(meta.ring, 0.04, mobile ? 40 : 64, mobile ? 8 : 12));
    var gem = makeMesh(gl, boxGeo(0.35, 0.35, 0.35));

    var uMVP = kit.mat4(), uView = kit.mat4(), uProj = kit.mat4(), uModel = kit.mat4(), tmp = kit.mat4();
    var uN = new Float32Array(9);
    var locs = {
      aPos: gl.getAttribLocation(prog, 'aPos'),
      aNrm: gl.getAttribLocation(prog, 'aNrm'),
      uMVP: gl.getUniformLocation(prog, 'uMVP'),
      uN: gl.getUniformLocation(prog, 'uN'),
      uColor: gl.getUniformLocation(prog, 'uColor'),
      uEmit: gl.getUniformLocation(prog, 'uEmit'),
      uGlow: gl.getUniformLocation(prog, 'uGlow'),
      uTime: gl.getUniformLocation(prog, 'uTime')
    };

    gl.enable(gl.DEPTH_TEST);
    gl.enable(gl.CULL_FACE);
    gl.clearColor(kit.VOID[0], kit.VOID[1], kit.VOID[2], 0);

    var state = { time: 0, amp: 0, status: 'idle', alive: true, raf: 0 };

    function resize() {
      var sz = kit.resizeCanvas(canvas, gl, stage, mobile);
      kit.mat4Perspective(uProj, Math.PI / 3.2, sz.aspect || (canvas.width / Math.max(canvas.height, 1)), 0.1, 40);
    }
    resize();

    function draw(mesh, color, emit, glow, model) {
      kit.mat4Multiply(tmp, uView, model);
      kit.mat4Multiply(uMVP, uProj, tmp);
      uN[0] = model[0]; uN[1] = model[1]; uN[2] = model[2];
      uN[3] = model[4]; uN[4] = model[5]; uN[5] = model[6];
      uN[6] = model[8]; uN[7] = model[9]; uN[8] = model[10];
      gl.useProgram(prog);
      gl.uniformMatrix4fv(locs.uMVP, false, uMVP);
      gl.uniformMatrix3fv(locs.uN, false, uN);
      gl.uniform3fv(locs.uColor, color);
      gl.uniform3fv(locs.uEmit, emit);
      gl.uniform1f(locs.uGlow, glow);
      gl.uniform1f(locs.uTime, state.time);
      gl.bindBuffer(gl.ARRAY_BUFFER, mesh.pos);
      gl.enableVertexAttribArray(locs.aPos);
      gl.vertexAttribPointer(locs.aPos, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, mesh.nrm);
      gl.enableVertexAttribArray(locs.aNrm);
      gl.vertexAttribPointer(locs.aNrm, 3, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.TRIANGLES, 0, mesh.count);
    }

    var last = 0;
    function frame(ts) {
      if (!state.alive) return;
      state.raf = g.requestAnimationFrame(frame);
      if (!last) last = ts;
      var dt = Math.min(0.05, (ts - last) / 1000);
      last = ts;
      state.time += dt;
      state.amp *= Math.pow(0.15, dt);

      var glow = meta.glow + state.amp * 0.9;
      var spin = state.time * meta.spin;
      if (state.status === 'thinking') spin *= 2.2;
      if (state.status === 'speaking') glow += 0.35 + state.amp;

      kit.mat4LookAt(uView, [0, 1.15, 3.2], [0, 0.35, 0], [0, 1, 0]);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

      kit.mat4FromRTS(uModel, 0, 0, 0, 0, 0, 0, 1, 1, 1);
      draw(pedestal, kit.GOLD, kit.GOLD, glow * 0.25, uModel);

      kit.mat4FromRTS(uModel, 0, spin * 0.15, 0, 0, 0.56, 0, 1, 1, 1);
      draw(pillar, kit.CYAN, kit.CYAN, glow * 0.35, uModel);

      kit.mat4FromRTS(uModel, Math.PI / 2.4, spin, 0.2, 0, 1.05, 0, 1, 1, 1);
      draw(ring, kit.GOLD, kit.CYAN, glow * 0.6, uModel);

      kit.mat4FromRTS(uModel, spin * 0.8, spin * 1.1, spin * 0.4, 0, 1.05, 0, 1, 1, 1);
      draw(gem, kit.CYAN, kit.CYAN, glow, uModel);
    }
    state.raf = g.requestAnimationFrame(frame);

    var offAmp = kit.onSpeakAmp(function (d) {
      if (d && typeof d.amp === 'number') state.amp = Math.max(state.amp, d.amp);
      if (d && (d.beat || d.boundary)) state.amp = Math.max(state.amp, 1);
    });

    var ro = null;
    if (g.ResizeObserver) {
      ro = new ResizeObserver(function () { resize(); });
      ro.observe(stage);
    } else {
      g.addEventListener('resize', resize, { passive: true });
    }

    api.setAmp = function (a) { state.amp = Math.max(0, Math.min(1, a || 0)); };
    api.setStatus = function (s) { state.status = s || 'idle'; };
    api.destroy = function () {
      state.alive = false;
      try { g.cancelAnimationFrame(state.raf); } catch (e) {}
      if (offAmp) offAmp();
      if (ro) try { ro.disconnect(); } catch (e2) {}
      host.removeAttribute('data-il-immersive-ready');
      host.__ilImmersive = null;
      host.innerHTML = '';
    };

    kit.emitSceneEvent('il-immersive-ready', { kind: kind, engine: 'webgl' });
    return api;
  }

  function mountAll(root) {
    root = root || g.document;
    if (!root || !root.querySelectorAll) return [];
    var nodes = root.querySelectorAll('[data-il-immersive]');
    var out = [], i;
    for (i = 0; i < nodes.length; i++) {
      if (nodes[i].getAttribute('data-il-scene')) continue;
      if (nodes[i]._ilImmersive) continue;
      out.push(mount(nodes[i], {}));
    }
    return out;
  }

  function boot() {
    if (!g.document) return;
    function go() { mountAll(document); }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go);
    else go();
  }

  g.ILImmersive = {
    mount: mount,
    mountAll: mountAll,
    boot: boot,
    kindDefaults: kindDefaults,
    VERSION: '1.0.0'
  };

  if (g.ILMuse3D) {
    g.ILMuse3D.immersive = g.ILImmersive;
    if (g.ILSceneKit) g.ILMuse3D.kit = g.ILSceneKit;
  }
  if (g.ILSceneKit && g.ILMuse3D) g.ILSceneKit.muse3d = g.ILMuse3D;

  boot();
})(typeof window !== 'undefined' ? window : this);
