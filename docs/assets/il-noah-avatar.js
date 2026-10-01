/**
 * IL Noah Avatar — full-featured 3D avatar system (Interstitium original).
 *
 * Self-contained WebGL (CSP-safe; no CDN, no Three.js, no external assets).
 * Four procedural avatars, all voice-reactive, driven by Noah status:
 *   idle | listening | thinking | speaking
 *   - monas : crystalline Monas / orrery (default — the classic Dee stage)
 *   - orrery: ringed worlds · orbital mechanics
 *   - sigil : radiant sigil core · counter-rotating glyph rings
 *   - wisp  : nebula ghost · drifting star-wisp
 *
 * Personalization persisted in localStorage 'il-noah-profile':
 *   { avatar, name, accent, intensity } — applied on every mount, everywhere Noah appears.
 *
 * Honesty standard: everything renders on-device in the visitor's browser.
 * No cloud rendering, no uploads, no fake "AI cloud". NOT Meta assets/code.
 */
(function (g) {
  'use strict';

  var PROFILE_KEY = 'il-noah-profile';

  var ACCENTS = {
    cyan:    { label: 'Cyan',    rgb: [0.369, 0.918, 0.831], css: '#5EEAD4' },
    gold:    { label: 'Gold',    rgb: [0.831, 0.659, 0.325], css: '#D4A853' },
    violet:  { label: 'Violet',  rgb: [0.654, 0.545, 0.980], css: '#A78BFA' },
    emerald: { label: 'Emerald', rgb: [0.204, 0.831, 0.600], css: '#34D399' }
  };
  var INTENSITY = {
    calm:     { label: 'Calm',     scale: 0.45 },
    balanced: { label: 'Balanced', scale: 1.0 },
    vivid:    { label: 'Vivid',    scale: 1.6 }
  };
  var VOID = [0.027, 0.043, 0.086];

  /* ---------------- profile store ---------------- */

  function defaultProfile() {
    return { v: 1, avatar: 'monas', name: 'Noah', accent: 'cyan', intensity: 'balanced' };
  }

  function getProfile() {
    var d = defaultProfile();
    try {
      var raw = g.localStorage && g.localStorage.getItem(PROFILE_KEY);
      if (raw) {
        var p = JSON.parse(raw) || {};
        return {
          v: 1,
          avatar: AVATARS_BY_ID[p.avatar] ? p.avatar : d.avatar,
          name: (typeof p.name === 'string' && p.name.trim()) ? p.name.trim().slice(0, 40) : d.name,
          accent: ACCENTS[p.accent] ? p.accent : d.accent,
          intensity: INTENSITY[p.intensity] ? p.intensity : d.intensity
        };
      }
    } catch (e) { /* corrupted or unavailable storage -> defaults */ }
    return d;
  }

  function saveProfile(p) {
    var d = defaultProfile();
    var clean = {
      v: 1,
      avatar: AVATARS_BY_ID[p.avatar] ? p.avatar : d.avatar,
      name: (typeof p.name === 'string' && p.name.trim()) ? p.name.trim().slice(0, 40) : d.name,
      accent: ACCENTS[p.accent] ? p.accent : d.accent,
      intensity: INTENSITY[p.intensity] ? p.intensity : d.intensity
    };
    try { if (g.localStorage) g.localStorage.setItem(PROFILE_KEY, JSON.stringify(clean)); } catch (e) {}
    return clean;
  }

  /* ---------------- math ---------------- */

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
      out[i*4]   = b0*a00 + b1*a10 + b2*a20 + b3*a30;
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

  /* ---------------- shaders ---------------- */

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
    'uniform float uAlpha;',
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
    '  gl_FragColor = vec4(col, uAlpha);',
    '}'
  ].join('\n');

  var PVERT = [
    'attribute vec3 aPos;',
    'attribute float aSize;',
    'attribute float aSeed;',
    'uniform mat4 uMVP;',
    'uniform float uTime;',
    'uniform float uAmp;',
    'uniform float uGather;',
    'uniform float uSwirl;',
    'uniform float uDrift;',
    'varying float vA;',
    'void main(){',
    '  float spin = uTime * (0.4 + aSeed * 1.2) * (1.0 + uSwirl) + aSeed * 6.28;',
    '  vec3 p = aPos;',
    '  p.xy += vec2(cos(spin), sin(spin)) * (0.08 + uAmp * 0.2);',
    '  p *= (1.0 + uAmp * 0.15) * (1.0 - uGather * 0.45);',
    '  p += vec3(sin(uTime*0.30+aSeed*6.28), cos(uTime*0.23+aSeed*4.00), sin(uTime*0.27+aSeed*5.00)) * uDrift;',
    '  vec4 mv = uMVP * vec4(p,1.0);',
    '  gl_Position = mv;',
    '  gl_PointSize = aSize * (1.0 + uAmp * 1.8) * (26.0 / max(mv.w, 0.4));',
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

  function compile(gl, type, src) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      try { console.warn('[ILNoahAvatar] shader', gl.getShaderInfoLog(sh)); } catch (e) {}
      gl.deleteShader(sh);
      return null;
    }
    return sh;
  }

  function makeProgram(gl, vs, fs) {
    var v = compile(gl, gl.VERTEX_SHADER, vs);
    var f = compile(gl, gl.FRAGMENT_SHADER, fs);
    if (!v || !f) return null;
    var p = gl.createProgram();
    gl.attachShader(p, v);
    gl.attachShader(p, f);
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      try { console.warn('[ILNoahAvatar] link', gl.getProgramInfoLog(p)); } catch (e) {}
      return null;
    }
    return p;
  }

  /* ---------------- geometry ---------------- */

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

  function pushTriN(pos, nrm, pa,na, pb,nb, pc,nc) {
    pos.push(pa[0],pa[1],pa[2], pb[0],pb[1],pb[2], pc[0],pc[1],pc[2]);
    nrm.push(na[0],na[1],na[2], nb[0],nb[1],nb[2], nc[0],nc[1],nc[2]);
  }

  function pack(pos, nrm) {
    return { pos: new Float32Array(pos), nrm: new Float32Array(nrm), count: pos.length / 3 };
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
    return pack(pos, nrm);
  }

  function octahedron(scale) {
    var s = scale;
    var v = [[0,s,0],[0,-s,0],[s,0,0],[-s,0,0],[0,0,s],[0,0,-s]];
    /* outward-CCW winding (verified): top ring 0-4-2, 0-3-4, 0-5-3, 0-2-5;
       bottom ring 1-2-4, 1-4-3, 1-3-5, 1-5-2 */
    var faces = [
      [0,4,2],[0,3,4],[0,5,3],[0,2,5],
      [1,2,4],[1,4,3],[1,3,5],[1,5,2]
    ];
    var pos = [], nrm = [];
    faces.forEach(function (f) {
      var a = v[f[0]], b = v[f[1]], c = v[f[2]];
      pushTri(pos, nrm, a[0],a[1],a[2], b[0],b[1],b[2], c[0],c[1],c[2]);
    });
    return pack(pos, nrm);
  }

  function torus(R, r, seg, tube) {
    var pos = [], nrm = [];
    var i, j;
    function pt(a, b) {
      var x = Math.cos(a) * (R + Math.cos(b) * r);
      var y = Math.sin(b) * r;
      var z = Math.sin(a) * (R + Math.cos(b) * r);
      return [[x, y, z], [Math.cos(a) * Math.cos(b), Math.sin(b), Math.sin(a) * Math.cos(b)]];
    }
    for (i = 0; i < seg; i++) {
      var a0 = (i / seg) * Math.PI * 2;
      var a1 = ((i + 1) / seg) * Math.PI * 2;
      for (j = 0; j < tube; j++) {
        var b0 = (j / tube) * Math.PI * 2;
        var b1 = ((j + 1) / tube) * Math.PI * 2;
        var p00 = pt(a0, b0), p10 = pt(a1, b0), p01 = pt(a0, b1), p11 = pt(a1, b1);
        pushTriN(pos, nrm, p00[0],p00[1], p10[0],p10[1], p11[0],p11[1]);
        pushTriN(pos, nrm, p00[0],p00[1], p11[0],p11[1], p01[0],p01[1]);
      }
    }
    return pack(pos, nrm);
  }

  function cylinder(r, h, seg) {
    var pos = [], nrm = [];
    var i, y0 = -h / 2, y1 = h / 2;
    for (i = 0; i < seg; i++) {
      var a0 = (i / seg) * Math.PI * 2;
      var a1 = ((i + 1) / seg) * Math.PI * 2;
      var x0 = Math.cos(a0) * r, z0 = Math.sin(a0) * r;
      var x1 = Math.cos(a1) * r, z1 = Math.sin(a1) * r;
      var n0 = [Math.cos(a0), 0, Math.sin(a0)];
      var n1 = [Math.cos(a1), 0, Math.sin(a1)];
      pushTriN(pos, nrm, [x0,y0,z0],n0, [x1,y0,z1],n1, [x1,y1,z1],n1);
      pushTriN(pos, nrm, [x0,y0,z0],n0, [x1,y1,z1],n1, [x0,y1,z0],n0);
    }
    return pack(pos, nrm);
  }

  function crescentShell(scale) {
    var geo = icosahedron(scale);
    var p = geo.pos, i;
    for (i = 0; i < p.length; i += 3) {
      if (p[i] > 0.15 * scale) { p[i] *= 0.55; p[i + 2] *= 1.08; }
      p[i + 1] *= 0.92;
    }
    return geo;
  }

  function makeMesh(gl, geo) {
    var m = { pos: trackBuf(gl.createBuffer()), nrm: trackBuf(gl.createBuffer()), count: geo.count };
    gl.bindBuffer(gl.ARRAY_BUFFER, m.pos);
    gl.bufferData(gl.ARRAY_BUFFER, geo.pos, gl.STATIC_DRAW);
    gl.bindBuffer(gl.ARRAY_BUFFER, m.nrm);
    gl.bufferData(gl.ARRAY_BUFFER, geo.nrm, gl.STATIC_DRAW);
    return m;
  }

  function makeParticles(gl, n, opt) {
    opt = opt || {};
    var rMin = opt.rMin == null ? 0.7 : opt.rMin;
    var rMax = opt.rMax == null ? 2.1 : opt.rMax;
    var sMin = opt.sMin == null ? 1.2 : opt.sMin;
    var sMax = opt.sMax == null ? 3.6 : opt.sMax;
    var flat = opt.flat || 0.7;
    var pos = new Float32Array(n * 3);
    var size = new Float32Array(n);
    var seed = new Float32Array(n);
    var i, ra, rb, rr;
    for (i = 0; i < n; i++) {
      ra = Math.random() * Math.PI * 2;
      rb = (Math.random() - 0.5) * Math.PI;
      rr = rMin + Math.random() * (rMax - rMin);
      pos[i * 3] = Math.cos(ra) * Math.cos(rb) * rr;
      pos[i * 3 + 1] = Math.sin(rb) * rr * flat;
      pos[i * 3 + 2] = Math.sin(ra) * Math.cos(rb) * rr;
      size[i] = sMin + Math.random() * (sMax - sMin);
      seed[i] = Math.random();
    }
    function buf(arr) {
      var b = trackBuf(gl.createBuffer());
      gl.bindBuffer(gl.ARRAY_BUFFER, b);
      gl.bufferData(gl.ARRAY_BUFFER, arr, gl.STATIC_DRAW);
      return b;
    }
    return { pos: buf(pos), size: buf(size), seed: buf(seed), count: n };
  }

  /* ---------------- avatar scenes ----------------
     Each avatar: build(gl, q) -> scene; draw(scene, rc).
     rc = { gl, t, status, amp, beat, accent, accent2, k, uView, uProj,
            mesh(mesh,color,emissive,glow,model,alpha),
            points(p,color,o,model) }                                  */

  /* ---- 1 · Monas — crystalline Monas / orrery (default) ---- */

  function buildMonas(gl, q) {
    var seg = q.mobile ? 48 : 72, tube = q.mobile ? 10 : 14;
    return {
      moon:  makeMesh(gl, crescentShell(0.55)),
      core:  makeMesh(gl, icosahedron(0.42)),
      ringA: makeMesh(gl, torus(0.95, 0.025, seg, tube)),
      ringB: makeMesh(gl, torus(1.25, 0.018, seg, tube)),
      stem:  makeMesh(gl, cylinder(0.035, 1.15, 10)),
      cross: makeMesh(gl, cylinder(0.03, 0.7, 8)),
      parts: makeParticles(gl, q.mobile ? 120 : 220, {})
    };
  }

  function drawMonas(sc, rc) {
    var t = rc.t, k = rc.k, st = rc.status;
    var amp = rc.amp, beat = rc.beat;
    var glow = 0.35, spin = t * 0.35 * k, bob = Math.sin(t * 1.2) * 0.04;
    var partAmp = 0.15, eyeZ = 3.35;
    if (st === 'listening') {
      glow = 0.75 + amp * 1.35; spin = t * 0.55 * k;
      bob = Math.sin(t * 6) * (0.03 + amp * 0.08); partAmp = 0.55 + amp * 1.1;
    } else if (st === 'thinking') {
      glow = 0.7 + 0.25 * Math.sin(t * 4); spin = t * 1.25 * k;
      bob = Math.sin(t * 2.2) * 0.05; partAmp = 0.85 + 0.3 * Math.sin(t * 3); eyeZ = 3.15;
    } else if (st === 'speaking') {
      var b = Math.max(beat, amp, 0.35 + 0.35 * Math.sin(t * 14));
      amp = b; glow = 1.05 + b * 1.45; spin = t * 0.45 * k;
      bob = Math.sin(t * 18) * (0.02 + b * 0.06); partAmp = 0.45 + b * 0.7;
    } else {
      glow = 0.32 + 0.08 * Math.sin(t * 1.5); partAmp = 0.12;
    }
    var sAmp = 1 + amp * 0.08;
    var M = mat4Identity(), em = st === 'speaking' ? rc.accent : (st === 'listening' ? rc.accent2 : rc.accent);

    mat4FromRTS(M, 0.25, spin * 0.7, 0.1, 0, 0.28 + bob, 0, sAmp, sAmp, sAmp);
    rc.mesh(sc.moon, rc.accent2, em, glow * 0.7, M);
    mat4FromRTS(M, t * 0.2 * k, spin, 0, 0, bob * 0.5, 0, sAmp, sAmp, sAmp);
    rc.mesh(sc.core, rc.accent, em, glow, M);
    mat4FromRTS(M, Math.PI / 2.2, spin * 0.4, 0.2, 0, bob, 0, 1, 1, 1);
    rc.mesh(sc.ringA, rc.accent2, rc.accent2, glow * 0.55, M);
    mat4FromRTS(M, 0.4, -spin * 0.55, Math.PI / 5, 0, bob * 0.3, 0, 1, 1, 1);
    rc.mesh(sc.ringB, rc.accent, rc.accent, glow * 0.4, M);
    mat4FromRTS(M, 0, 0, 0, 0, -0.15 + bob * 0.2, 0, 1, 1, 1);
    rc.mesh(sc.stem, rc.accent2, rc.accent2, glow * 0.35, M);
    mat4FromRTS(M, 0, 0, Math.PI / 2, 0, -0.35 + bob * 0.2, 0, 1, 1, 1);
    rc.mesh(sc.cross, rc.accent2, rc.accent2, glow * 0.3, M);

    mat4FromRTS(M, 0, spin * 0.25, 0, 0, bob * 0.4, 0, 1, 1, 1);
    rc.points(sc.parts, st === 'listening' ? rc.accent2 : rc.accent,
      { amp: partAmp, gather: 0, swirl: 0, drift: 0 }, M);
    return eyeZ;
  }

  /* ---- 2 · Orrery — ringed worlds ---- */

  function buildOrrery(gl, q) {
    var seg = q.mobile ? 40 : 64;
    var planets = [];
    var defs = [
      { ring: 0, n: 2, size: 0.055 }, { ring: 1, n: 2, size: 0.075 }, { ring: 2, n: 2, size: 0.06 }
    ];
    var pi = 0;
    defs.forEach(function (d, ri) {
      for (var i = 0; i < d.n; i++) {
        planets.push({
          mesh: makeMesh(gl, icosahedron(d.size)),
          ring: ri,
          phase: (i / d.n) * Math.PI * 2 + ri * 1.3,
          speed: (0.55 + ri * 0.28) * (ri % 2 ? -1 : 1),
          size: d.size
        });
        pi++;
      }
    });
    return {
      core: makeMesh(gl, icosahedron(0.34)),
      rings: [
        { mesh: makeMesh(gl, torus(0.70, 0.014, seg, 8)), tilt: [Math.PI / 2.4, 0.15],  prec: 0.10 },
        { mesh: makeMesh(gl, torus(1.00, 0.011, seg, 8)), tilt: [0.50, Math.PI / 6],     prec: -0.07 },
        { mesh: makeMesh(gl, torus(1.30, 0.009, seg, 8)), tilt: [Math.PI / 2.8, -0.30],  prec: 0.05 }
      ],
      radii: [0.70, 1.00, 1.30],
      planets: planets,
      parts: makeParticles(gl, q.mobile ? 90 : 160, { rMin: 1.5, rMax: 2.6 })
    };
  }

  var _omA = new Float32Array(16), _omB = new Float32Array(16), _omC = new Float32Array(16);

  function drawOrrery(sc, rc) {
    var t = rc.t, k = rc.k, st = rc.status;
    var amp = rc.amp, beat = rc.beat;
    var speedMul = 1, glow = 0.5, precMul = 1, bob = Math.sin(t * 1.1) * 0.03;
    if (st === 'listening')      { speedMul = 2.2; glow = 0.8 + amp * 1.2; }
    else if (st === 'thinking')  { speedMul = 3.0; precMul = 4.0; glow = 0.75 + 0.25 * Math.sin(t * 5); }
    else if (st === 'speaking')  { var b = Math.max(beat, amp); speedMul = 1.4; glow = 1.0 + b * 1.4; }
    else                         { glow = 0.45 + 0.08 * Math.sin(t * 1.4); }
    var M = mat4Identity();
    var coreS = 1 + (st === 'speaking' ? Math.max(beat, amp) * 0.14 : amp * 0.06);
    mat4FromRTS(M, t * 0.25 * k, t * 0.4 * k, 0, 0, bob, 0, coreS, coreS, coreS);
    rc.mesh(sc.core, rc.accent, rc.accent, glow, M);

    var ri, r;
    for (ri = 0; ri < sc.rings.length; ri++) {
      r = sc.rings[ri];
      mat4FromRTS(M, r.tilt[0] + t * r.prec * precMul * k, t * 0.12 * k, r.tilt[1], 0, bob * 0.5, 0, 1, 1, 1);
      rc.mesh(r.mesh, rc.accent2, rc.accent2, glow * 0.5, M);
    }
    var pi, p, a, R;
    for (pi = 0; pi < sc.planets.length; pi++) {
      p = sc.planets[pi]; R = sc.radii[p.ring]; r = sc.rings[p.ring];
      a = p.phase + t * p.speed * speedMul * k;
      mat4FromRTS(_omA, 0, a, 0, 0, 0, 0, 1, 1, 1);
      mat4FromRTS(_omB, 0, 0, 0, R, 0, 0, p.size / 0.06, p.size / 0.06, p.size / 0.06);
      mat4Multiply(_omC, _omA, _omB);
      mat4FromRTS(_omA, r.tilt[0], 0, r.tilt[1], 0, bob * 0.5, 0, 1, 1, 1);
      mat4Multiply(M, _omA, _omC);
      var pg = glow * (0.8 + 0.4 * Math.sin(t * 3 + p.phase));
      rc.mesh(p.mesh, rc.accent, rc.accent2, pg, M);
    }
    mat4FromRTS(M, 0, t * 0.1 * k, 0, 0, 0, 0, 1, 1, 1);
    rc.points(sc.parts, rc.accent, { amp: 0.2 + amp * 0.5, gather: 0, swirl: 0.4 * speedMul * k, drift: 0 }, M);
    return 3.6;
  }

  /* ---- 3 · Sigil — radiant sigil core ---- */

  function buildSigil(gl, q) {
    var seg = q.mobile ? 40 : 64;
    function tickRing(R, nTicks) {
      var ticks = [];
      for (var i = 0; i < nTicks; i++) {
        var a = (i / nTicks) * Math.PI * 2;
        ticks.push({ mesh: makeMesh(gl, cylinder(0.008, 0.07, 6)), ang: a, R: R });
      }
      return ticks;
    }
    var spokes = [];
    for (var s = 0; s < 8; s++) {
      spokes.push({ mesh: makeMesh(gl, cylinder(0.01, 0.5, 6)), ang: (s / 8) * Math.PI * 2 });
    }
    return {
      core: makeMesh(gl, octahedron(0.36)),
      ringIn: makeMesh(gl, torus(0.62, 0.016, seg, 8)),
      ringOut: makeMesh(gl, torus(0.86, 0.012, seg, 8)),
      ticksIn: tickRing(0.62, 12),
      ticksOut: tickRing(0.86, 16),
      spokes: spokes,
      parts: makeParticles(gl, q.mobile ? 80 : 140, { rMin: 0.9, rMax: 1.8, flat: 0.25 })
    };
  }

  var _sgA = new Float32Array(16), _sgB = new Float32Array(16), _sgC = new Float32Array(16);

  function sigilTick(rc, tick, groupM, glow) {
    mat4FromRTS(_sgA, 0, 0, tick.ang, 0, 0, 0, 1, 1, 1);
    mat4FromRTS(_sgB, 0, 0, 0, Math.cos(tick.ang) * tick.R, Math.sin(tick.ang) * tick.R, 0, 1, 1, 1);
    mat4Multiply(_sgC, _sgA, _sgB);
    var M = mat4Identity();
    mat4Multiply(M, groupM, _sgC);
    rc.mesh(tick.mesh, rc.accent2, rc.accent2, glow, M);
  }

  function drawSigil(sc, rc) {
    var t = rc.t, k = rc.k, st = rc.status;
    var amp = rc.amp, beat = rc.beat;
    var spinIn = 0.5, spinOut = -0.35, glow = 0.55, strobe = 0;
    if (st === 'listening')      { spinIn = 1.6; spinOut = -1.2; glow = 0.85 + amp * 1.1; }
    else if (st === 'thinking')  { spinIn = 3.2; spinOut = -2.6; glow = 0.8; strobe = 0.3 * Math.sin(t * 9); }
    else if (st === 'speaking')  { var b = Math.max(beat, amp); spinIn = 0.9; spinOut = -0.7; glow = 1.0 + b * 1.4; }
    else                         { glow = 0.5 + 0.1 * Math.sin(t * 1.6); }
    glow = Math.max(0.15, glow + strobe);
    var M = mat4Identity();
    var coreS = 1 + (st === 'speaking' ? Math.max(beat, amp) * 0.22 : 0.05 * Math.sin(t * 2));
    mat4FromRTS(M, t * 0.3 * k, t * 0.5 * k, 0, 0, 0, 0, coreS, coreS, coreS);
    rc.mesh(sc.core, rc.accent, rc.accent, glow * 1.1, M);

    var gIn = mat4Identity(), gOut = mat4Identity();
    mat4FromRTS(gIn, 0, 0, t * spinIn * k, 0, 0, 0, 1, 1, 1);
    mat4FromRTS(gOut, 0, 0, t * spinOut * k, 0, 0, 0, 1, 1, 1);
    rc.mesh(sc.ringIn, rc.accent, rc.accent2, glow * 0.7, gIn);
    rc.mesh(sc.ringOut, rc.accent2, rc.accent, glow * 0.55, gOut);
    var i;
    for (i = 0; i < sc.ticksIn.length; i++) sigilTick(rc, sc.ticksIn[i], gIn, glow * 0.8);
    for (i = 0; i < sc.ticksOut.length; i++) sigilTick(rc, sc.ticksOut[i], gOut, glow * 0.65);
    for (i = 0; i < sc.spokes.length; i++) {
      var sp = sc.spokes[i];
      mat4FromRTS(_sgA, 0, 0, sp.ang, 0, 0, 0, 1, 1, 1);
      mat4FromRTS(_sgB, 0, 0, 0, Math.cos(sp.ang) * 0.44, Math.sin(sp.ang) * 0.44, 0, 1, 1 + amp * 0.35, 1);
      mat4Multiply(_sgC, _sgA, _sgB);
      mat4Multiply(M, gIn, _sgC);
      rc.mesh(sp.mesh, rc.accent2, rc.accent2, glow * 0.5, M);
    }
    mat4FromRTS(M, 0, 0, t * 0.2 * k, 0, 0, 0, 1, 1, 1);
    rc.points(sc.parts, rc.accent, { amp: 0.25 + amp * 0.6, gather: 0, swirl: spinIn * 0.4, drift: 0 }, M);
    return 3.4;
  }

  /* ---- 4 · Wisp — nebula ghost ---- */

  function buildWisp(gl, q) {
    var seg = q.mobile ? 40 : 64;
    var knots = [];
    for (var i = 0; i < 5; i++) {
      knots.push({
        mesh: makeMesh(gl, icosahedron(0.05)),
        p1: i * 1.7, p2: i * 2.3, p3: i * 1.1,
        f1: 0.31 + i * 0.05, f2: 0.23 + i * 0.04, f3: 0.27 + i * 0.06
      });
    }
    return {
      core: makeMesh(gl, icosahedron(0.16)),
      ghostA: makeMesh(gl, torus(1.05, 0.02, seg, 8)),
      ghostB: makeMesh(gl, torus(1.45, 0.015, seg, 8)),
      knots: knots,
      nebula: makeParticles(gl, q.mobile ? 200 : 420,
        { rMin: 0.3, rMax: 2.3, sMin: 2.5, sMax: 7.0, flat: 0.8 })
    };
  }

  function drawWisp(sc, rc) {
    var t = rc.t, k = rc.k, st = rc.status;
    var amp = rc.amp, beat = rc.beat;
    var gather = 0, swirl = 1, drift = 0.35, glow = 0.4, knotMul = 1;
    if (st === 'listening')      { gather = 0.55; swirl = 1.8; glow = 0.7 + amp * 1.0; }
    else if (st === 'thinking')  { swirl = 3.0; knotMul = 2.0; glow = 0.65 + 0.25 * Math.sin(t * 4); drift = 0.5; }
    else if (st === 'speaking')  { var b = Math.max(beat, amp); gather = 0.15; glow = 0.9 + b * 1.2; drift = 0.3 + b * 0.3; }
    else                         { glow = 0.35 + 0.08 * Math.sin(t * 1.3); }
    var M = mat4Identity();
    var breathe = 1 + 0.06 * Math.sin(t * 1.8) + (st === 'speaking' ? Math.max(beat, amp) * 0.1 : 0);
    mat4FromRTS(M, t * 0.2 * k, t * 0.33 * k, 0, 0, 0, 0, breathe, breathe, breathe);
    rc.mesh(sc.core, rc.accent, rc.accent, glow * 0.8, M);

    mat4FromRTS(M, Math.PI / 2.5, t * 0.08 * k, 0.3, 0, 0, 0, 1, 1, 1);
    rc.mesh(sc.ghostA, rc.accent2, rc.accent2, glow * 0.35, M, 0.55);
    mat4FromRTS(M, 0.6, -t * 0.06 * k, Math.PI / 4, 0, 0, 0, 1, 1, 1);
    rc.mesh(sc.ghostB, rc.accent, rc.accent, glow * 0.3, M, 0.5);

    var i, kn;
    for (i = 0; i < sc.knots.length; i++) {
      kn = sc.knots[i];
      var x = Math.sin(t * kn.f1 * knotMul * k + kn.p1) * 1.2;
      var y = Math.sin(t * kn.f2 * knotMul * k + kn.p2) * 0.7;
      var z = Math.cos(t * kn.f3 * knotMul * k + kn.p3) * 1.2;
      mat4FromRTS(M, t * k + kn.p1, kn.p2, 0, x, y, z, 1, 1, 1);
      rc.mesh(kn.mesh, rc.accent, rc.accent2, glow * (0.9 + 0.4 * Math.sin(t * 2 + kn.p1)), M);
    }
    mat4FromRTS(M, 0, t * 0.05 * k, 0, 0, 0, 0, 1, 1, 1);
    rc.points(sc.nebula, rc.accent,
      { amp: 0.3 + amp * 0.8, gather: gather, swirl: swirl, drift: drift * k }, M);
    return 3.8;
  }

  /* ---------------- catalog ---------------- */

  var AVATARS = [
    { id: 'monas',  label: 'Monas',      hint: 'Crystalline Monas · orrery rings',   build: buildMonas,  draw: drawMonas },
    { id: 'orrery', label: 'Orrery',      hint: 'Ringed worlds · orbital mechanics',  build: buildOrrery, draw: drawOrrery },
    { id: 'sigil',  label: 'Sigil Core',  hint: 'Radiant sigil · counter-rotating glyph rings', build: buildSigil, draw: drawSigil },
    { id: 'wisp',   label: 'Wisp',        hint: 'Nebula ghost · drifting star-wisp',  build: buildWisp,  draw: drawWisp }
  ];
  var AVATARS_BY_ID = {};
  AVATARS.forEach(function (a) { AVATARS_BY_ID[a.id] = a; });

  /* ---------------- engine ---------------- */

  /* buffer tracking so avatar switches don't leak GL resources */
  var _track = null;
  function trackBuf(b) { if (_track) _track.push(b); return b; }

  function prefersReduced() {
    try {
      return !!(g.matchMedia && g.matchMedia('(prefers-reduced-motion: reduce)').matches);
    } catch (e) { return false; }
  }

  function fallbackHTML(name, label) {
    return '<div class="il-muse-3d__fallback" aria-hidden="true">' +
      '<div class="il-muse-3d__monas"><span class="il-muse-3d__core"></span><span class="il-muse-3d__glyph"></span></div>' +
      '</div>' +
      '<span class="il-muse-3d__badge" data-noah-badge title="Renders on-device in your browser · no cloud">' +
      name + ' · ' + label + ' 3D</span>';
  }

  function accentPair(key) {
    var a = ACCENTS[key] || ACCENTS.cyan;
    var second = (key === 'gold') ? ACCENTS.cyan.rgb : [0.831, 0.659, 0.325];
    return { primary: a.rgb, secondary: second, css: a.css, label: a.label };
  }

  function createInstance(slot, opts) {
    opts = opts || {};
    var prof = getProfile();
    var root = document.createElement('div');
    root.className = 'il-muse-3d';
    root.setAttribute('data-noah-avatar', '1');
    root.setAttribute('role', 'img');
    root.setAttribute('aria-label', 'Noah voice-reactive 3D avatar');
    root.innerHTML = fallbackHTML(prof.name, AVATARS_BY_ID[prof.avatar].label);
    slot.appendChild(root);
    if (opts.cinema) slot.classList.add('il-muse-3d-slot--cinema');

    var mobile = (typeof opts.mobile === 'boolean')
      ? opts.mobile
      : (g.matchMedia && g.matchMedia('(max-width: 768px)').matches);

    var state = {
      status: 'idle',
      avatar: AVATARS_BY_ID[opts.avatar] ? opts.avatar : prof.avatar,
      accentKey: ACCENTS[opts.accent] ? opts.accent : prof.accent,
      intensityKey: INTENSITY[opts.intensity] ? opts.intensity : prof.intensity,
      name: (typeof opts.name === 'string' && opts.name.trim()) ? opts.name.trim().slice(0, 40) : prof.name,
      amp: 0, speakBeat: 0, time: 0,
      alive: true, paused: false, reduced: prefersReduced(),
      cinema: !!opts.cinema, mobile: mobile,
      eyeZCur: null, bornAt: null /* status-transition smoothing fields */
    };
    var pair = accentPair(state.accentKey);
    var kScale = INTENSITY[state.intensityKey].scale;

    var api = {
      root: root, slot: slot,
      setStatus: function (s) {
        state.status = (s === 'listening' || s === 'thinking' || s === 'speaking') ? s : 'idle';
        if (state.reduced) renderStatic();
      },
      setAvatar: function (id) {
        if (!AVATARS_BY_ID[id] || id === state.avatar) return;
        state.avatar = id;
        rebuildScene();
        updateBadge();
        if (state.reduced) renderStatic();
      },
      setAccent: function (key) {
        if (!ACCENTS[key]) return;
        state.accentKey = key; pair = accentPair(key);
        if (state.reduced) renderStatic();
      },
      setIntensity: function (key) {
        if (!INTENSITY[key]) return;
        state.intensityKey = key; kScale = INTENSITY[key].scale;
        if (state.reduced) renderStatic();
      },
      setName: function (n) {
        if (typeof n === 'string' && n.trim()) { state.name = n.trim().slice(0, 40); updateBadge(); }
      },
      setAmplitude: function (a) { state.amp = Math.max(0, Math.min(1, a || 0)); },
      pulseSpeak: function (v) { state.speakBeat = Math.max(state.speakBeat, v == null ? 1 : v); },
      getStatus: function () { return state.status; },
      getAvatar: function () { return state.avatar; },
      applyProfile: function () {
        var p = getProfile();
        api.setName(p.name);
        api.setAccent(p.accent);
        api.setIntensity(p.intensity);
        api.setAvatar(p.avatar);
      },
      destroy: function () {
        state.alive = false;
        try { if (raf) g.cancelAnimationFrame(raf); } catch (e) {}
        if (io) { try { io.disconnect(); } catch (e2) {} }
        if (ro) { try { ro.disconnect(); } catch (e3) {} }
        g.removeEventListener('il-muse-speak-boundary', onBoundary);
        g.removeEventListener('il-muse-speak-amp', onAmp);
        stopMic();
        freeScene();
        var ix = registry.indexOf(api);
        if (ix >= 0) registry.splice(ix, 1);
        if (root.parentNode) root.parentNode.removeChild(root);
      }
    };

    function updateBadge() {
      var b = root.querySelector('[data-noah-badge]');
      if (b) b.textContent = state.name + ' · ' + AVATARS_BY_ID[state.avatar].label + ' 3D';
    }

    if (!g.WebGLRenderingContext) {
      root.classList.add('is-fallback');
      return api;
    }
    /* reduced-motion keeps going: one static WebGL frame, no animation loop */

    var canvas = document.createElement('canvas');
    canvas.setAttribute('aria-hidden', 'true');
    root.insertBefore(canvas, root.firstChild);
    var gl = canvas.getContext('webgl', {
      alpha: true, antialias: true, premultipliedAlpha: true, powerPreference: 'high-performance'
    }) || canvas.getContext('experimental-webgl');
    if (!gl) { root.classList.add('is-fallback'); return api; }
    root.classList.add('is-webgl');

    var meshProg = makeProgram(gl, VERT, FRAG);
    var partProg = makeProgram(gl, PVERT, PFRAG);
    if (!meshProg || !partProg) {
      root.classList.add('is-fallback');
      root.classList.remove('is-webgl');
      return api;
    }

    var L = {
      mesh: {
        aPos: gl.getAttribLocation(meshProg, 'aPos'),
        aNrm: gl.getAttribLocation(meshProg, 'aNrm'),
        uMVP: gl.getUniformLocation(meshProg, 'uMVP'),
        uN: gl.getUniformLocation(meshProg, 'uN'),
        uColor: gl.getUniformLocation(meshProg, 'uColor'),
        uEmissive: gl.getUniformLocation(meshProg, 'uEmissive'),
        uGlow: gl.getUniformLocation(meshProg, 'uGlow'),
        uTime: gl.getUniformLocation(meshProg, 'uTime'),
        uAlpha: gl.getUniformLocation(meshProg, 'uAlpha')
      },
      part: {
        aPos: gl.getAttribLocation(partProg, 'aPos'),
        aSize: gl.getAttribLocation(partProg, 'aSize'),
        aSeed: gl.getAttribLocation(partProg, 'aSeed'),
        uMVP: gl.getUniformLocation(partProg, 'uMVP'),
        uTime: gl.getUniformLocation(partProg, 'uTime'),
        uAmp: gl.getUniformLocation(partProg, 'uAmp'),
        uGather: gl.getUniformLocation(partProg, 'uGather'),
        uSwirl: gl.getUniformLocation(partProg, 'uSwirl'),
        uDrift: gl.getUniformLocation(partProg, 'uDrift'),
        uColor: gl.getUniformLocation(partProg, 'uColor')
      }
    };

    gl.enable(gl.DEPTH_TEST);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    gl.clearColor(VOID[0], VOID[1], VOID[2], 0);

    var uMVP = mat4Identity(), uView = mat4Identity(), uProj = mat4Identity();
    var uModel = mat4Identity(), uN = new Float32Array(9), tmp = mat4Identity();

    function drawMeshEntry(mesh, color, emissive, glow, model, alpha) {
      mat4Multiply(uMVP, uView, model);
      mat4Multiply(tmp, uProj, uMVP);
      mat3NormalFromMat4(uN, model);
      gl.useProgram(meshProg);
      gl.uniformMatrix4fv(L.mesh.uMVP, false, tmp);
      gl.uniformMatrix3fv(L.mesh.uN, false, uN);
      gl.uniform3fv(L.mesh.uColor, color);
      gl.uniform3fv(L.mesh.uEmissive, emissive);
      gl.uniform1f(L.mesh.uGlow, glow);
      gl.uniform1f(L.mesh.uTime, state.time);
      gl.uniform1f(L.mesh.uAlpha, alpha == null ? 0.96 : alpha);
      gl.bindBuffer(gl.ARRAY_BUFFER, mesh.pos);
      gl.enableVertexAttribArray(L.mesh.aPos);
      gl.vertexAttribPointer(L.mesh.aPos, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, mesh.nrm);
      gl.enableVertexAttribArray(L.mesh.aNrm);
      gl.vertexAttribPointer(L.mesh.aNrm, 3, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.TRIANGLES, 0, mesh.count);
    }

    function drawPointsEntry(p, color, o, model) {
      mat4Multiply(uMVP, uView, model);
      mat4Multiply(tmp, uProj, uMVP);
      gl.useProgram(partProg);
      gl.uniformMatrix4fv(L.part.uMVP, false, tmp);
      gl.uniform1f(L.part.uTime, state.time);
      gl.uniform1f(L.part.uAmp, o.amp || 0);
      gl.uniform1f(L.part.uGather, o.gather || 0);
      gl.uniform1f(L.part.uSwirl, o.swirl || 0);
      gl.uniform1f(L.part.uDrift, o.drift || 0);
      gl.uniform3fv(L.part.uColor, color);
      gl.bindBuffer(gl.ARRAY_BUFFER, p.pos);
      gl.enableVertexAttribArray(L.part.aPos);
      gl.vertexAttribPointer(L.part.aPos, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, p.size);
      gl.enableVertexAttribArray(L.part.aSize);
      gl.vertexAttribPointer(L.part.aSize, 1, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, p.seed);
      gl.enableVertexAttribArray(L.part.aSeed);
      gl.vertexAttribPointer(L.part.aSeed, 1, gl.FLOAT, false, 0, 0);
      gl.depthMask(false);
      gl.drawArrays(gl.POINTS, 0, p.count);
      gl.depthMask(true);
    }

    /* scene (re)build with GL-resource tracking */
    var scene = null, avatarDef = null;
    function freeScene() {
      if (scene && scene.buffers) {
        scene.buffers.forEach(function (b) { try { gl.deleteBuffer(b); } catch (e) {} });
      }
      scene = null;
    }
    function rebuildScene() {
      freeScene();
      avatarDef = AVATARS_BY_ID[state.avatar];
      _track = [];
      var s = avatarDef.build(gl, { mobile: state.mobile });
      s.buffers = _track;
      _track = null;
      scene = s;
    }
    rebuildScene();

    /* mic (voice-reactive listening) */
    var mic = { stream: null, ctx: null, analyser: null, data: null, allowed: false, _trying: false };
    function stopMic() {
      try { if (mic.stream) mic.stream.getTracks().forEach(function (t) { t.stop(); }); } catch (e) {}
      try { if (mic.ctx && mic.ctx.close) mic.ctx.close(); } catch (e2) {}
      mic.stream = null; mic.ctx = null; mic.analyser = null; mic.data = null; mic.allowed = false;
    }
    function ensureMic() {
      if (mic.allowed || mic._trying || state.reduced) return;
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
      }).catch(function () { mic._trying = false; mic.allowed = false; });
    }
    function micLevel() {
      if (!mic.allowed || !mic.analyser || !mic.data) return 0;
      mic.analyser.getByteFrequencyData(mic.data);
      var sum = 0, i, n = mic.data.length;
      for (i = 0; i < n; i++) sum += mic.data[i];
      return Math.min(1, (sum / n) / 90);
    }

    function resize() {
      var dpr = Math.min(g.devicePixelRatio || 1, state.mobile ? 1.5 : 2);
      var w = Math.max(1, root.clientWidth || slot.clientWidth || 320);
      var h = Math.max(1, root.clientHeight || 200);
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      gl.viewport(0, 0, canvas.width, canvas.height);
      mat4Perspective(uProj, Math.PI / 3.4, canvas.width / canvas.height, 0.1, 40);
    }

    var EYES = { monas: 3.35, orrery: 3.6, sigil: 3.4, wisp: 3.8 };

    function renderFrame() {
      var st = state.status, t = state.time;
      var amp = state.amp;
      if (st === 'listening') {
        if (!mic.allowed) ensureMic();
        var ml = micLevel();
        procPhase += 0.016 * (8 + amp * 10);
        var procedural = 0.35 + 0.65 * (0.5 + 0.5 * Math.sin(procPhase));
        amp = Math.max(amp, mic.allowed ? ml : procedural);
        state.amp = amp;
      }
      var eyeTarget = (EYES[state.avatar] || 3.4) + (st === 'thinking' ? -0.2 : 0);
      /* Smooth camera: lerp eyeZ toward the status target instead of snapping. */
      state.eyeZCur = (state.eyeZCur == null) ? eyeTarget : state.eyeZCur + (eyeTarget - state.eyeZCur) * 0.08;
      /* Wake-in: ease animation time from stillness over the first 1.5 s. */
      if (state.bornAt == null) state.bornAt = t;
      var wake = 1, age = t - state.bornAt;
      if (age < 1.5 && age >= 0) wake = (1 - Math.cos(Math.PI * age / 1.5)) / 2;
      var bob = Math.sin(t * 1.2) * 0.04;
      mat4LookAt(uView, [0, 0.15 + bob * 0.2, state.eyeZCur], [0, 0.05, 0], [0, 1, 0]);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      var rc = {
        gl: gl, t: t * wake, status: st, amp: amp, beat: state.speakBeat,
        accent: pair.primary, accent2: pair.secondary, k: kScale,
        uView: uView, uProj: uProj,
        mesh: drawMeshEntry, points: drawPointsEntry
      };
      avatarDef.draw(scene, rc);
    }

    function renderStatic() {
      if (!gl || !scene) return;
      if (root.clientWidth && canvas.width === 0) resize();
      renderFrame();
    }

    var raf = 0, last = 0, procPhase = 0, io = null, ro = null;

    function frame(ts) {
      if (!state.alive || state.paused) { raf = 0; return; }
      raf = g.requestAnimationFrame(frame);
      if (!last) last = ts;
      var dt = Math.min(0.05, (ts - last) / 1000);
      last = ts;
      state.time += dt;
      state.speakBeat *= Math.pow(0.08, dt);
      if (root.clientWidth && (canvas.width === 0 ||
          Math.abs(canvas.width / (g.devicePixelRatio || 1) - root.clientWidth) > 2)) {
        resize();
      }
      renderFrame();
    }

    function kickLoop() {
      if (state.reduced || raf || !state.alive || state.paused) return;
      last = 0;
      raf = g.requestAnimationFrame(frame);
    }

    resize();

    if (state.reduced) {
      renderStatic();
      /* layout may settle after deferred scripts run — keep the still frame correct */
      var rsT = 0;
      g.addEventListener('resize', function () {
        if (!state.alive) return;
        if (rsT) return;
        rsT = g.setTimeout(function () { rsT = 0; resize(); renderStatic(); }, 150);
      }, { passive: true });
    } else {
      kickLoop();
      /* pause when offscreen (mobile perf + battery) */
      if (g.IntersectionObserver) {
        io = new IntersectionObserver(function (entries) {
          var vis = entries.length && entries[0].isIntersecting;
          state.paused = !vis;
          if (vis) kickLoop();
          else if (raf) { try { g.cancelAnimationFrame(raf); } catch (e) {} raf = 0; }
        }, { threshold: 0.02 });
        io.observe(root);
      }
      if (g.ResizeObserver) {
        ro = new ResizeObserver(function () { resize(); });
        ro.observe(root);
      } else {
        g.addEventListener('resize', resize, { passive: true });
      }
      /* idle vitality: first 3s must feel alive on phone */
      api.pulseSpeak(0.85);
      api.setAmplitude(0.55);
      try {
        var t0 = Date.now();
        var bootPulse = function () {
          if (!state.alive || Date.now() - t0 > 3200) return;
          api.pulseSpeak(0.35 + 0.4 * Math.random());
          api.setAmplitude(0.25 + 0.35 * Math.random());
          g.setTimeout(bootPulse, 280);
        };
        g.setTimeout(bootPulse, 180);
      } catch (eBoot) {}
    }

    var onBoundary = function () { api.pulseSpeak(1); };
    var onAmp = function (ev) {
      var d = ev && ev.detail;
      if (d && typeof d.amp === 'number') api.setAmplitude(d.amp);
      if (d && d.beat) api.pulseSpeak(d.beat);
    };
    g.addEventListener('il-muse-speak-boundary', onBoundary);
    g.addEventListener('il-muse-speak-amp', onAmp);

    return api;
  }

  /* ---------------- registry / public API ---------------- */

  var registry = [];

  function findForSlot(slot) {
    for (var i = 0; i < registry.length; i++) {
      if (registry[i].slot === slot) return registry[i];
    }
    return null;
  }

  /* An instance is orphaned when its root lost its parent, or when its slot has
     left the document (e.g. a widget rebuilt its innerHTML around the slot).
     Recovery 2026-10-01: the old check missed detached-tree orphans, leaking one
     WebGL context + rAF loop per chat re-render until the renderer hung. */
  function isOrphaned(inst) {
    if (!inst || !inst.root || !inst.root.parentNode) return true;
    try {
      if (inst.slot && typeof document !== 'undefined' && !document.contains(inst.slot)) return true;
    } catch (e) {}
    return false;
  }

  function mount(slot, opts) {
    if (!slot) return null;
    var existing = findForSlot(slot);
    if (existing) {
      if (existing.root.parentNode !== slot) slot.appendChild(existing.root);
      existing.applyProfile();
      return existing;
    }
    /* reuse orphaned instance whose root was detached (e.g. widget re-render) */
    for (var j = 0; j < registry.length; j++) {
      if (isOrphaned(registry[j])) {
        slot.appendChild(registry[j].root);
        registry[j].slot = slot;
        registry[j].applyProfile();
        return registry[j];
      }
    }
    /* self-healing cap: destroy any other detached instances before allocating
       another WebGL context, so a re-render storm can never exhaust the GPU */
    for (var k = registry.length - 1; k >= 0; k--) {
      if (isOrphaned(registry[k])) {
        try { registry[k].destroy(); } catch (eD) {}
      }
    }
    var inst = createInstance(slot, opts || {});
    registry.push(inst);
    return inst;
  }

  function syncFromApp(app, opts) {
    if (!app) return null;
    var slot = app.querySelector('[data-muse-3d-slot]');
    if (!slot) return null;
    var cinema = !!(opts && opts.cinema) || !!app.closest('[data-il-cinema], .il-cinema-muse-host');
    var inst = mount(slot, { cinema: cinema });
    if (inst) inst.setStatus(app.getAttribute('data-status') || 'idle');
    return inst;
  }

  function setProfilePatch(patch) {
    var p = saveProfile(Object.assign(getProfile(), patch || {}));
    for (var i = 0; i < registry.length; i++) {
      try { registry[i].applyProfile(); } catch (e) {}
    }
    try {
      var ev;
      if (typeof CustomEvent === 'function') ev = new CustomEvent('il-noah-profile', { detail: p });
      else { ev = document.createEvent('CustomEvent'); ev.initCustomEvent('il-noah-profile', false, false, p); }
      g.dispatchEvent(ev);
    } catch (e2) {}
    return p;
  }

  g.ILNoahAvatar = {
    mount: mount,
    syncFromApp: syncFromApp,
    getProfile: getProfile,
    saveProfile: saveProfile,
    setProfilePatch: setProfilePatch,
    AVATARS: AVATARS,
    ACCENTS: ACCENTS,
    INTENSITY: INTENSITY,
    PROFILE_KEY: PROFILE_KEY,
    VERSION: '2.0.0',
    get instances() { return registry.slice(); }
  };

})(typeof window !== 'undefined' ? window : this);
