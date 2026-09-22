/**
 * IL Muse 3D — voice-reactive crystalline Monas / orrery stage (Interstitium original).
 * Self-contained WebGL (CSP-safe; no CDN). Exceeds flat Muse-class soft avatars in motion depth.
 * Driven by Lab Muse status: idle | listening | thinking | speaking.
 * NOT Meta Muse assets/code. NOT a photoreal scraped portrait.
 */
(function (g) {
  'use strict';

  var CYAN = [0.369, 0.918, 0.831];
  var GOLD = [0.831, 0.659, 0.325];
  var VOID = [0.027, 0.043, 0.086];

  var VERT = [
    'attribute vec3 aPos;',
    'attribute vec3 aNrm;',
    'uniform mat4 uMVP;',
    'uniform mat3 uN;',
    'varying vec3 vN;',
    'varying vec3 vW;',
    'void main(){',
    '  vN = normalize(uN * aNrm);',
    '  vW = aPos;',
    '  gl_Position = uMVP * vec4(aPos,1.0);',
    '}'
  ].join('\n');

  var FRAG = [
    'precision mediump float;',
    'varying vec3 vN;',
    'varying vec3 vW;',
    'uniform vec3 uColor;',
    'uniform vec3 uEmissive;',
    'uniform float uGlow;',
    'uniform float uTime;',
    'void main(){',
    '  vec3 N = normalize(vN);',
    '  vec3 L = normalize(vec3(0.35,0.85,0.45));',
    '  vec3 V = normalize(vec3(0.0,0.15,1.0));',
    '  float ndl = max(dot(N,L),0.0);',
    '  float rim = pow(1.0 - max(dot(N,V),0.0), 2.4);',
    '  float fres = pow(1.0 - max(dot(N,V),0.0), 3.0);',
    '  vec3 base = uColor * (0.22 + 0.78 * ndl);',
    '  vec3 spec = vec3(1.0) * pow(max(dot(reflect(-L,N),V),0.0), 42.0) * 0.55;',
    '  vec3 col = base + spec + uEmissive * uGlow + GOLDISH(rim) + uColor * fres * 0.35;',
    '  col += 0.04 * sin(vW.y * 18.0 + uTime * 2.0);',
    '  gl_FragColor = vec4(col, 0.96);',
    '}',
    'vec3 GOLDISH(float r){ return vec3(0.831,0.659,0.325) * r * 0.65; }'
  ].join('\n');

  /* Fix: GOLDISH used before define — rewrite FRAG cleanly */
  FRAG = [
    'precision mediump float;',
    'varying vec3 vN;',
    'varying vec3 vW;',
    'uniform vec3 uColor;',
    'uniform vec3 uEmissive;',
    'uniform float uGlow;',
    'uniform float uTime;',
    'void main(){',
    '  vec3 N = normalize(vN);',
    '  vec3 L = normalize(vec3(0.35,0.85,0.45));',
    '  vec3 V = normalize(vec3(0.0,0.15,1.0));',
    '  float ndl = max(dot(N,L),0.0);',
    '  float rim = pow(1.0 - max(dot(N,V),0.0), 2.4);',
    '  float fres = pow(1.0 - max(dot(N,V),0.0), 3.0);',
    '  vec3 gold = vec3(0.831,0.659,0.325);',
    '  vec3 base = uColor * (0.22 + 0.78 * ndl);',
    '  vec3 spec = vec3(1.0) * pow(max(dot(reflect(-L,N),V),0.0), 42.0) * 0.55;',
    '  vec3 col = base + spec + uEmissive * uGlow + gold * rim * 0.65 + uColor * fres * 0.35;',
    '  col += 0.04 * sin(vW.y * 18.0 + uTime * 2.0);',
    '  gl_FragColor = vec4(col, 0.96);',
    '}'
  ].join('\n');

  var PVERT = [
    'attribute vec3 aPos;',
    'attribute float aSize;',
    'attribute float aSeed;',
    'uniform mat4 uMVP;',
    'uniform float uTime;',
    'uniform float uAmp;',
    'varying float vA;',
    'void main(){',
    '  float spin = uTime * (0.4 + aSeed * 1.2) + aSeed * 6.28;',
    '  vec3 p = aPos;',
    '  p.xy += vec2(cos(spin), sin(spin)) * (0.08 + uAmp * 0.2);',
    '  p *= (1.0 + uAmp * 0.15);',
    '  vec4 mv = uMVP * vec4(p,1.0);',
    '  gl_Position = mv;',
    '  gl_PointSize = aSize * (1.0 + uAmp * 1.8) * (180.0 / max(mv.w, 0.4));',
    '  vA = 0.35 + 0.65 * fract(aSeed + uTime * 0.05);',
    '}'
  ].join('\n');

  var PFRAG = [
    'precision mediump float;',
    'varying float vA;',
    'uniform vec3 uColor;',
    'void main(){',
    '  vec2 c = gl_PointCoord - 0.5;',
    '  float d = dot(c,c);',
    '  if(d > 0.25) discard;',
    '  float a = (1.0 - smoothstep(0.05, 0.25, d)) * vA;',
    '  gl_FragColor = vec4(uColor, a);',
    '}'
  ].join('\n');

  function mat4Identity() {
    return new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);
  }

  function mat4Perspective(out, fovy, aspect, near, far) {
    var f = 1 / Math.tan(fovy / 2);
    var nf = 1 / (near - far);
    out[0] = f / aspect; out[1] = 0; out[2] = 0; out[3] = 0;
    out[4] = 0; out[5] = f; out[6] = 0; out[7] = 0;
    out[8] = 0; out[9] = 0; out[10] = (far + near) * nf; out[11] = -1;
    out[12] = 0; out[13] = 0; out[14] = 2 * far * near * nf; out[15] = 0;
    return out;
  }

  function mat4LookAt(out, eye, center, up) {
    var zx = eye[0] - center[0], zy = eye[1] - center[1], zz = eye[2] - center[2];
    var len = 1 / Math.max(Math.hypot(zx, zy, zz), 1e-6);
    zx *= len; zy *= len; zz *= len;
    var xx = up[1] * zz - up[2] * zy;
    var xy = up[2] * zx - up[0] * zz;
    var xz = up[0] * zy - up[1] * zx;
    len = 1 / Math.max(Math.hypot(xx, xy, xz), 1e-6);
    xx *= len; xy *= len; xz *= len;
    var yx = zy * xz - zz * xy;
    var yy = zz * xx - zx * xz;
    var yz = zx * xy - zy * xx;
    out[0] = xx; out[1] = yx; out[2] = zx; out[3] = 0;
    out[4] = xy; out[5] = yy; out[6] = zy; out[7] = 0;
    out[8] = xz; out[9] = yz; out[10] = zz; out[11] = 0;
    out[12] = -(xx * eye[0] + xy * eye[1] + xz * eye[2]);
    out[13] = -(yx * eye[0] + yy * eye[1] + yz * eye[2]);
    out[14] = -(zx * eye[0] + zy * eye[1] + zz * eye[2]);
    out[15] = 1;
    return out;
  }

  function mat4Multiply(out, a, b) {
    var a00=a[0],a01=a[1],a02=a[2],a03=a[3],a10=a[4],a11=a[5],a12=a[6],a13=a[7];
    var a20=a[8],a21=a[9],a22=a[10],a23=a[11],a30=a[12],a31=a[13],a32=a[14],a33=a[15];
    var b0,b1,b2,b3,i;
    for (i = 0; i < 4; i++) {
      b0 = b[i*4]; b1 = b[i*4+1]; b2 = b[i*4+2]; b3 = b[i*4+3];
      out[i*4] = b0*a00 + b1*a10 + b2*a20 + b3*a30;
      out[i*4+1] = b0*a01 + b1*a11 + b2*a21 + b3*a31;
      out[i*4+2] = b0*a02 + b1*a12 + b2*a22 + b3*a32;
      out[i*4+3] = b0*a03 + b1*a13 + b2*a23 + b3*a33;
    }
    return out;
  }

  function mat4FromRTS(out, rx, ry, rz, tx, ty, tz, sx, sy, sz) {
    var cx = Math.cos(rx), sxr = Math.sin(rx);
    var cy = Math.cos(ry), syr = Math.sin(ry);
    var cz = Math.cos(rz), szr = Math.sin(rz);
    var m00 = cy * cz, m01 = cy * szr, m02 = -syr;
    var m10 = sxr * syr * cz - cx * szr;
    var m11 = sxr * syr * szr + cx * cz;
    var m12 = sxr * cy;
    var m20 = cx * syr * cz + sxr * szr;
    var m21 = cx * syr * szr - sxr * cz;
    var m22 = cx * cy;
    out[0] = m00 * sx; out[1] = m01 * sx; out[2] = m02 * sx; out[3] = 0;
    out[4] = m10 * sy; out[5] = m11 * sy; out[6] = m12 * sy; out[7] = 0;
    out[8] = m20 * sz; out[9] = m21 * sz; out[10] = m22 * sz; out[11] = 0;
    out[12] = tx; out[13] = ty; out[14] = tz; out[15] = 1;
    return out;
  }

  function mat3NormalFromMat4(out, m) {
    out[0] = m[0]; out[1] = m[1]; out[2] = m[2];
    out[3] = m[4]; out[4] = m[5]; out[5] = m[6];
    out[6] = m[8]; out[7] = m[9]; out[8] = m[10];
    return out;
  }

  function compile(gl, type, src) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      try { console.warn('[ILMuse3D] shader', gl.getShaderInfoLog(sh)); } catch (e) {}
      gl.deleteShader(sh);
      return null;
    }
    return sh;
  }

  function program(gl, vs, fs) {
    var v = compile(gl, gl.VERTEX_SHADER, vs);
    var f = compile(gl, gl.FRAGMENT_SHADER, fs);
    if (!v || !f) return null;
    var p = gl.createProgram();
    gl.attachShader(p, v);
    gl.attachShader(p, f);
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      try { console.warn('[ILMuse3D] link', gl.getProgramInfoLog(p)); } catch (e) {}
      return null;
    }
    return p;
  }

  function pushTri(pos, nrm, ax,ay,az, bx,by,bz, cx,cy,cz) {
    var ux = bx - ax, uy = by - ay, uz = bz - az;
    var vx = cx - ax, vy = cy - ay, vz = cz - az;
    var nx = uy * vz - uz * vy;
    var ny = uz * vx - ux * vz;
    var nz = ux * vy - uy * vx;
    var len = Math.hypot(nx, ny, nz) || 1;
    nx /= len; ny /= len; nz /= len;
    pos.push(ax,ay,az, bx,by,bz, cx,cy,cz);
    nrm.push(nx,ny,nz, nx,ny,nz, nx,ny,nz);
  }

  function icosahedron(scale) {
    var t = (1 + Math.sqrt(5)) / 2;
    var verts = [
      [-1,t,0],[1,t,0],[-1,-t,0],[1,-t,0],
      [0,-1,t],[0,1,t],[0,-1,-t],[0,1,-t],
      [t,0,-1],[t,0,1],[-t,0,-1],[-t,0,1]
    ].map(function (v) {
      var l = Math.hypot(v[0], v[1], v[2]) || 1;
      return [v[0] / l * scale, v[1] / l * scale, v[2] / l * scale];
    });
    var faces = [
      [0,11,5],[0,5,1],[0,1,7],[0,7,10],[0,10,11],
      [1,5,9],[5,11,4],[11,10,2],[10,7,6],[7,1,8],
      [3,9,4],[3,4,2],[3,2,6],[3,6,8],[3,8,9],
      [4,9,5],[2,4,11],[6,2,10],[8,6,7],[9,8,1]
    ];
    var pos = [], nrm = [];
    faces.forEach(function (f) {
      var a = verts[f[0]], b = verts[f[1]], c = verts[f[2]];
      pushTri(pos, nrm, a[0],a[1],a[2], b[0],b[1],b[2], c[0],c[1],c[2]);
    });
    return { pos: new Float32Array(pos), nrm: new Float32Array(nrm), count: pos.length / 3 };
  }

  function torus(R, r, seg, tube) {
    var pos = [], nrm = [];
    var i, j;
    for (i = 0; i < seg; i++) {
      var a0 = (i / seg) * Math.PI * 2;
      var a1 = ((i + 1) / seg) * Math.PI * 2;
      for (j = 0; j < tube; j++) {
        var b0 = (j / tube) * Math.PI * 2;
        var b1 = ((j + 1) / tube) * Math.PI * 2;
        function pt(a, b) {
          var cx = Math.cos(a) * R, cz = Math.sin(a) * R;
          var x = cx + Math.cos(a) * Math.cos(b) * r;
          var y = Math.sin(b) * r;
          var z = cz + Math.sin(a) * Math.cos(b) * r;
          var nx = Math.cos(a) * Math.cos(b);
          var ny = Math.sin(b);
          var nz = Math.sin(a) * Math.cos(b);
          return [x, y, z, nx, ny, nz];
        }
        var p00 = pt(a0, b0), p10 = pt(a1, b0), p01 = pt(a0, b1), p11 = pt(a1, b1);
        pushTri(pos, nrm, p00[0],p00[1],p00[2], p10[0],p10[1],p10[2], p11[0],p11[1],p11[2]);
        nrm[nrm.length - 9] = p00[3]; nrm[nrm.length - 8] = p00[4]; nrm[nrm.length - 7] = p00[5];
        nrm[nrm.length - 6] = p10[3]; nrm[nrm.length - 5] = p10[4]; nrm[nrm.length - 4] = p10[5];
        nrm[nrm.length - 3] = p11[3]; nrm[nrm.length - 2] = p11[4]; nrm[nrm.length - 1] = p11[5];
        pushTri(pos, nrm, p00[0],p00[1],p00[2], p11[0],p11[1],p11[2], p01[0],p01[1],p01[2]);
        nrm[nrm.length - 9] = p00[3]; nrm[nrm.length - 8] = p00[4]; nrm[nrm.length - 7] = p00[5];
        nrm[nrm.length - 6] = p11[3]; nrm[nrm.length - 5] = p11[4]; nrm[nrm.length - 4] = p11[5];
        nrm[nrm.length - 3] = p01[3]; nrm[nrm.length - 2] = p01[4]; nrm[nrm.length - 1] = p01[5];
      }
    }
    return { pos: new Float32Array(pos), nrm: new Float32Array(nrm), count: pos.length / 3 };
  }

  function cylinder(r, h, seg) {
    var pos = [], nrm = [];
    var i, y0 = -h / 2, y1 = h / 2;
    for (i = 0; i < seg; i++) {
      var a0 = (i / seg) * Math.PI * 2;
      var a1 = ((i + 1) / seg) * Math.PI * 2;
      var x0 = Math.cos(a0) * r, z0 = Math.sin(a0) * r;
      var x1 = Math.cos(a1) * r, z1 = Math.sin(a1) * r;
      pushTri(pos, nrm, x0,y0,z0, x1,y0,z1, x1,y1,z1);
      pushTri(pos, nrm, x0,y0,z0, x1,y1,z1, x0,y1,z0);
    }
    return { pos: new Float32Array(pos), nrm: new Float32Array(nrm), count: pos.length / 3 };
  }

  function crescentShell(scale) {
    /* Approximate lunar crescent as partial torus slice via icosa warp */
    var geo = icosahedron(scale);
    var i, p = geo.pos;
    for (i = 0; i < p.length; i += 3) {
      if (p[i] > 0.15 * scale) {
        p[i] *= 0.55;
        p[i + 2] *= 1.08;
      }
      p[i + 1] *= 0.92;
    }
    return geo;
  }

  function makeMesh(gl, geo) {
    var vao = {
      pos: gl.createBuffer(),
      nrm: gl.createBuffer(),
      count: geo.count
    };
    gl.bindBuffer(gl.ARRAY_BUFFER, vao.pos);
    gl.bufferData(gl.ARRAY_BUFFER, geo.pos, gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, vao.nrm);
    gl.bufferData(gl.ARRAY_BUFFER, geo.nrm, gl.STATIC_DRAW);
    return vao;
  }

  function prefersReduced() {
    try {
      return !!(g.matchMedia && g.matchMedia('(prefers-reduced-motion: reduce)').matches);
    } catch (e) { return false; }
  }

  function fallbackHTML() {
    return '<div class="il-muse-3d__fallback" aria-hidden="true">' +
      '<div class="il-muse-3d__monas"><span class="il-muse-3d__core"></span><span class="il-muse-3d__glyph"></span></div>' +
      '</div>' +
      '<span class="il-muse-3d__badge">Dee · Monas 3D</span>';
  }

  function createInstance(slot, opts) {
    opts = opts || {};
    var root = document.createElement('div');
    root.className = 'il-muse-3d';
    root.setAttribute('data-muse-3d', '1');
    root.setAttribute('role', 'img');
    root.setAttribute('aria-label', 'Lab Muse voice-reactive 3D familiar');
    root.innerHTML = fallbackHTML();
    slot.appendChild(root);
    if (opts.cinema) slot.classList.add('il-muse-3d-slot--cinema');

    var state = {
      status: 'idle',
      avatarId: opts.avatarId || 'dee',
      amp: 0,
      speakBeat: 0,
      time: 0,
      alive: true,
      reduced: prefersReduced(),
      cinema: !!opts.cinema
    };

    var api = {
      root: root,
      slot: slot,
      setStatus: function (k) { state.status = k || 'idle'; },
      setAvatar: function (id) { state.avatarId = id || 'dee'; },
      setAmplitude: function (a) { state.amp = Math.max(0, Math.min(1, a || 0)); },
      pulseSpeak: function (v) { state.speakBeat = Math.max(state.speakBeat, v == null ? 1 : v); },
      destroy: function () {
        state.alive = false;
        try { if (raf) g.cancelAnimationFrame(raf); } catch (e) {}
        stopMic();
        if (root.parentNode) root.parentNode.removeChild(root);
      },
      getStatus: function () { return state.status; }
    };

    if (state.reduced || !g.WebGLRenderingContext) {
      root.classList.add('is-fallback');
      return api;
    }

    var canvas = document.createElement('canvas');
    canvas.setAttribute('aria-hidden', 'true');
    root.insertBefore(canvas, root.firstChild);
    var gl = canvas.getContext('webgl', {
      alpha: true,
      antialias: true,
      premultipliedAlpha: true,
      powerPreference: 'high-performance'
    }) || canvas.getContext('experimental-webgl');
    if (!gl) {
      root.classList.add('is-fallback');
      return api;
    }
    root.classList.add('is-webgl');

    var meshProg = program(gl, VERT, FRAG);
    var partProg = program(gl, PVERT, PFRAG);
    if (!meshProg || !partProg) {
      root.classList.add('is-fallback');
      root.classList.remove('is-webgl');
      return api;
    }

    var mobile = (typeof opts.mobile === 'boolean')
      ? opts.mobile
      : (g.matchMedia && g.matchMedia('(max-width: 768px)').matches);
    var segRing = mobile ? 48 : 72;
    var tubeSeg = mobile ? 10 : 14;
    var particleN = mobile ? 120 : 220;

    var core = makeMesh(gl, icosahedron(0.42));
    var moon = makeMesh(gl, crescentShell(0.55));
    var ringA = makeMesh(gl, torus(0.95, 0.025, segRing, tubeSeg));
    var ringB = makeMesh(gl, torus(1.25, 0.018, segRing, tubeSeg));
    var stem = makeMesh(gl, cylinder(0.035, 1.15, 10));
    var cross = makeMesh(gl, cylinder(0.03, 0.7, 8));

    var pPos = new Float32Array(particleN * 3);
    var pSize = new Float32Array(particleN);
    var pSeed = new Float32Array(particleN);
    var pi;
    for (pi = 0; pi < particleN; pi++) {
      var ra = Math.random() * Math.PI * 2;
      var rb = (Math.random() - 0.5) * Math.PI;
      var rr = 0.7 + Math.random() * 1.4;
      pPos[pi * 3] = Math.cos(ra) * Math.cos(rb) * rr;
      pPos[pi * 3 + 1] = Math.sin(rb) * rr * 0.7;
      pPos[pi * 3 + 2] = Math.sin(ra) * Math.cos(rb) * rr;
      pSize[pi] = 1.2 + Math.random() * 2.4;
      pSeed[pi] = Math.random();
    }
    var pBufPos = gl.createBuffer();
    var pBufSize = gl.createBuffer();
    var pBufSeed = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, pBufPos);
    gl.bufferData(gl.ARRAY_BUFFER, pPos, gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, pBufSize);
    gl.bufferData(gl.ARRAY_BUFFER, pSize, gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, pBufSeed);
    gl.bufferData(gl.ARRAY_BUFFER, pSeed, gl.STATIC_DRAW);

    var uMVP = mat4Identity();
    var uView = mat4Identity();
    var uProj = mat4Identity();
    var uModel = mat4Identity();
    var uN = new Float32Array(9);
    var tmp = mat4Identity();

    var locs = {
      mesh: {
        aPos: gl.getAttribLocation(meshProg, 'aPos'),
        aNrm: gl.getAttribLocation(meshProg, 'aNrm'),
        uMVP: gl.getUniformLocation(meshProg, 'uMVP'),
        uN: gl.getUniformLocation(meshProg, 'uN'),
        uColor: gl.getUniformLocation(meshProg, 'uColor'),
        uEmissive: gl.getUniformLocation(meshProg, 'uEmissive'),
        uGlow: gl.getUniformLocation(meshProg, 'uGlow'),
        uTime: gl.getUniformLocation(meshProg, 'uTime')
      },
      part: {
        aPos: gl.getAttribLocation(partProg, 'aPos'),
        aSize: gl.getAttribLocation(partProg, 'aSize'),
        aSeed: gl.getAttribLocation(partProg, 'aSeed'),
        uMVP: gl.getUniformLocation(partProg, 'uMVP'),
        uTime: gl.getUniformLocation(partProg, 'uTime'),
        uAmp: gl.getUniformLocation(partProg, 'uAmp'),
        uColor: gl.getUniformLocation(partProg, 'uColor')
      }
    };

    gl.enable(gl.DEPTH_TEST);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    gl.clearColor(VOID[0], VOID[1], VOID[2], 0);

    var mic = { stream: null, ctx: null, analyser: null, data: null, allowed: false };

    function stopMic() {
      try {
        if (mic.stream) mic.stream.getTracks().forEach(function (t) { t.stop(); });
      } catch (e) {}
      try { if (mic.ctx && mic.ctx.close) mic.ctx.close(); } catch (e2) {}
      mic.stream = null; mic.ctx = null; mic.analyser = null; mic.data = null; mic.allowed = false;
    }

    function ensureMic() {
      if (mic.allowed || mic._trying) return;
      if (!g.navigator || !g.navigator.mediaDevices || !g.navigator.mediaDevices.getUserMedia) return;
      mic._trying = true;
      g.navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(function (stream) {
        mic.stream = stream;
        var AC = g.AudioContext || g.webkitAudioContext;
        if (!AC) { mic._trying = false; return; }
        mic.ctx = new AC();
        var src = mic.ctx.createMediaStreamSource(stream);
        mic.analyser = mic.ctx.createAnalyser();
        mic.analyser.fftSize = 256;
        mic.analyser.smoothingTimeConstant = 0.78;
        src.connect(mic.analyser);
        mic.data = new Uint8Array(mic.analyser.frequencyBinCount);
        mic.allowed = true;
        mic._trying = false;
      }).catch(function () {
        mic._trying = false;
        mic.allowed = false;
      });
    }

    function micLevel() {
      if (!mic.allowed || !mic.analyser || !mic.data) return 0;
      mic.analyser.getByteFrequencyData(mic.data);
      var sum = 0, i, n = mic.data.length;
      for (i = 0; i < n; i++) sum += mic.data[i];
      return Math.min(1, (sum / n) / 90);
    }

    function resize() {
      var dpr = Math.min(g.devicePixelRatio || 1, mobile ? 1.75 : 2);
      var w = Math.max(1, root.clientWidth || slot.clientWidth || 320);
      var h = Math.max(1, root.clientHeight || 200);
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      gl.viewport(0, 0, canvas.width, canvas.height);
      mat4Perspective(uProj, Math.PI / 3.4, canvas.width / canvas.height, 0.1, 40);
    }

    function drawMesh(mesh, color, emissive, glow, model) {
      mat4Multiply(uMVP, uView, model);
      mat4Multiply(tmp, uProj, uMVP);
      mat3NormalFromMat4(uN, model);
      gl.useProgram(meshProg);
      gl.uniformMatrix4fv(locs.mesh.uMVP, false, tmp);
      gl.uniformMatrix3fv(locs.mesh.uN, false, uN);
      gl.uniform3fv(locs.mesh.uColor, color);
      gl.uniform3fv(locs.mesh.uEmissive, emissive);
      gl.uniform1f(locs.mesh.uGlow, glow);
      gl.uniform1f(locs.mesh.uTime, state.time);
      gl.bindBuffer(gl.ARRAY_BUFFER, mesh.pos);
      gl.enableVertexAttribArray(locs.mesh.aPos);
      gl.vertexAttribPointer(locs.mesh.aPos, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, mesh.nrm);
      gl.enableVertexAttribArray(locs.mesh.aNrm);
      gl.vertexAttribPointer(locs.mesh.aNrm, 3, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.TRIANGLES, 0, mesh.count);
    }

    var raf = 0;
    var last = 0;
    var procPhase = 0;

    function frame(ts) {
      if (!state.alive) return;
      raf = g.requestAnimationFrame(frame);
      if (!last) last = ts;
      var dt = Math.min(0.05, (ts - last) / 1000);
      last = ts;
      state.time += dt;
      state.speakBeat *= Math.pow(0.08, dt);

      if (root.clientWidth && (canvas.width === 0 || Math.abs(canvas.width / (g.devicePixelRatio || 1) - root.clientWidth) > 2)) {
        resize();
      }

      var amp = state.amp;
      var glow = 0.35;
      var spin = state.time * 0.35;
      var bob = Math.sin(state.time * 1.2) * 0.04;
      var partAmp = 0.15;
      var eyeZ = 3.35;

      if (state.status === 'listening') {
        if (!mic.allowed) ensureMic();
        var ml = micLevel();
        procPhase += dt * (8 + amp * 10);
        var procedural = 0.35 + 0.65 * (0.5 + 0.5 * Math.sin(procPhase));
        amp = Math.max(amp, mic.allowed ? ml : procedural);
        glow = 0.75 + amp * 1.35;
        spin = state.time * 0.55;
        bob = Math.sin(state.time * 6) * (0.03 + amp * 0.08);
        partAmp = 0.55 + amp * 1.1;
      } else if (state.status === 'thinking') {
        glow = 0.7 + 0.25 * Math.sin(state.time * 4);
        spin = state.time * 1.25;
        bob = Math.sin(state.time * 2.2) * 0.05;
        partAmp = 0.85 + 0.3 * Math.sin(state.time * 3);
        eyeZ = 3.15;
      } else if (state.status === 'speaking') {
        var beat = Math.max(state.speakBeat, state.amp, 0.35 + 0.35 * Math.sin(state.time * 14));
        amp = beat;
        glow = 1.05 + beat * 1.45;
        spin = state.time * 0.45;
        bob = Math.sin(state.time * 18) * (0.02 + beat * 0.06);
        partAmp = 0.45 + beat * 0.7;
      } else {
        glow = 0.32 + 0.08 * Math.sin(state.time * 1.5);
        partAmp = 0.12;
      }

      state.amp = amp;

      mat4LookAt(uView, [0, 0.15 + bob * 0.2, eyeZ], [0, 0.05, 0], [0, 1, 0]);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

      var goldOn = state.avatarId === 'sigil' ? GOLD : CYAN;
      var accent = state.avatarId === 'cap' ? GOLD : CYAN;
      var em = state.status === 'speaking' ? CYAN : (state.status === 'listening' ? GOLD : accent);

      mat4FromRTS(uModel, 0.25, spin * 0.7, 0.1, 0, 0.28 + bob, 0, 1, 1, 1);
      drawMesh(moon, goldOn, em, glow * 0.7, uModel);

      mat4FromRTS(uModel, state.time * 0.2, spin, 0, 0, bob * 0.5, 0, 1, 1, 1);
      drawMesh(core, CYAN, em, glow, uModel);

      mat4FromRTS(uModel, Math.PI / 2.2, spin * 0.4, 0.2, 0, bob, 0, 1, 1, 1);
      drawMesh(ringA, GOLD, GOLD, glow * 0.55, uModel);

      mat4FromRTS(uModel, 0.4, -spin * 0.55, Math.PI / 5, 0, bob * 0.3, 0, 1, 1, 1);
      drawMesh(ringB, CYAN, CYAN, glow * 0.4, uModel);

      mat4FromRTS(uModel, 0, 0, 0, 0, -0.15 + bob * 0.2, 0, 1, 1, 1);
      drawMesh(stem, GOLD, GOLD, glow * 0.35, uModel);

      mat4FromRTS(uModel, 0, 0, Math.PI / 2, 0, -0.35 + bob * 0.2, 0, 1, 1, 1);
      drawMesh(cross, GOLD, GOLD, glow * 0.3, uModel);

      /* particles */
      mat4FromRTS(uModel, 0, spin * 0.25, 0, 0, bob * 0.4, 0, 1, 1, 1);
      mat4Multiply(uMVP, uView, uModel);
      mat4Multiply(tmp, uProj, uMVP);
      gl.useProgram(partProg);
      gl.uniformMatrix4fv(locs.part.uMVP, false, tmp);
      gl.uniform1f(locs.part.uTime, state.time);
      gl.uniform1f(locs.part.uAmp, partAmp);
      gl.uniform3fv(locs.part.uColor, state.status === 'listening' ? GOLD : CYAN);
      gl.bindBuffer(gl.ARRAY_BUFFER, pBufPos);
      gl.enableVertexAttribArray(locs.part.aPos);
      gl.vertexAttribPointer(locs.part.aPos, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, pBufSize);
      gl.enableVertexAttribArray(locs.part.aSize);
      gl.vertexAttribPointer(locs.part.aSize, 1, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, pBufSeed);
      gl.enableVertexAttribArray(locs.part.aSeed);
      gl.vertexAttribPointer(locs.part.aSeed, 1, gl.FLOAT, false, 0, 0);
      gl.depthMask(false);
      gl.drawArrays(gl.POINTS, 0, particleN);
      gl.depthMask(true);
    }

    resize();
    raf = g.requestAnimationFrame(frame);

    var ro;
    if (g.ResizeObserver) {
      ro = new ResizeObserver(function () { resize(); });
      ro.observe(root);
    } else {
      g.addEventListener('resize', resize, { passive: true });
    }

    var onBoundary = function () { api.pulseSpeak(1); };
    var onAmp = function (ev) {
      var d = ev && ev.detail;
      if (d && typeof d.amp === 'number') api.setAmplitude(d.amp);
      if (d && d.beat) api.pulseSpeak(d.beat);
    };
    g.addEventListener('il-muse-speak-boundary', onBoundary);
    g.addEventListener('il-muse-speak-amp', onAmp);

    var _destroy = api.destroy;
    api.destroy = function () {
      g.removeEventListener('il-muse-speak-boundary', onBoundary);
      g.removeEventListener('il-muse-speak-amp', onAmp);
      if (ro) try { ro.disconnect(); } catch (e) {}
      _destroy();
    };

    /* Kick idle vitality immediately — first 3s must feel alive on phone */
    api.pulseSpeak(0.85);
    api.setAmplitude(0.55);
    try {
      var t0 = Date.now();
      var bootPulse = function () {
        if (Date.now() - t0 > 3200) return;
        api.pulseSpeak(0.35 + 0.4 * Math.random());
        api.setAmplitude(0.25 + 0.35 * Math.random());
        g.setTimeout(bootPulse, 280);
      };
      g.setTimeout(bootPulse, 180);
    } catch (eBoot) {}

    return api;
  }

  var registry = [];

  function findInstanceForSlot(slot) {
    var i;
    for (i = 0; i < registry.length; i++) {
      if (registry[i].slot === slot || registry[i].root.parentNode === slot) return registry[i];
    }
    return null;
  }

  function mount(slot, opts) {
    if (!slot) return null;
    var existing = findInstanceForSlot(slot);
    if (existing) {
      if (existing.root.parentNode !== slot) slot.appendChild(existing.root);
      if (opts && opts.avatarId) existing.setAvatar(opts.avatarId);
      if (opts && opts.cinema) slot.classList.add('il-muse-3d-slot--cinema');
      return existing;
    }
    /* Reuse orphaned instance whose root was detached by innerHTML wipe */
    for (var j = 0; j < registry.length; j++) {
      if (!registry[j].root.parentNode) {
        slot.appendChild(registry[j].root);
        registry[j].slot = slot;
        if (opts && opts.avatarId) registry[j].setAvatar(opts.avatarId);
        return registry[j];
      }
    }
    var inst = createInstance(slot, opts || {});
    registry.push(inst);
    return inst;
  }

  function reattach(inst, slot) {
    if (!inst || !slot) return;
    inst.slot = slot;
    if (inst.root.parentNode !== slot) slot.appendChild(inst.root);
  }

  function syncFromApp(app, opts) {
    if (!app) return null;
    var slot = app.querySelector('[data-muse-3d-slot]');
    if (!slot) return null;
    var cinema = !!(opts && opts.cinema) || !!app.closest('[data-il-cinema], .il-cinema-muse-host');
    var inst = mount(slot, {
      avatarId: app.getAttribute('data-avatar') || 'dee',
      cinema: cinema
    });
    if (inst) inst.setStatus(app.getAttribute('data-status') || 'idle');
    return inst;
  }

  function attachCinema(host) {
    if (!host) return null;
    var slot = host.querySelector('[data-muse-3d-slot]') || host;
    if (!slot.getAttribute || !slot.hasAttribute('data-muse-3d-slot')) {
      if (!host.querySelector('[data-muse-3d-slot]')) {
        /* cinema uses muse mount; syncFromApp handles it */
      }
    }
    var app = host.querySelector('.il-muse-app') || host.closest('.il-muse-app');
    if (app) return syncFromApp(app, { cinema: true });
    return mount(slot, { cinema: true });
  }

  if (g.ILSceneKit) {
    /* shared curriculum renderer utilities */
  }
  g.ILMuse3D = {
    mount: mount,
    reattach: reattach,
    syncFromApp: syncFromApp,
    attachCinema: attachCinema,
    CYAN: '#5EEAD4',
    GOLD: '#D4A853',
    VOID: '#070B16',
    get kit() { return g.ILSceneKit || null; },
    get immersive() { return g.ILImmersive || null; }
  };
  if (g.ILSceneKit) g.ILSceneKit.muse3d = g.ILMuse3D;
  /* compat aliases for muse boot */
  g.ILMuse3D.syncFromApp = g.ILMuse3D.syncFromApp || g.ILMuse3D.syncFromApp;
  g.ILMuse3D.syncFromApp = g.ILMuse3D.syncFromApp || g.ILMuse3D.syncFromApp;

})(typeof window !== 'undefined' ? window : this);
