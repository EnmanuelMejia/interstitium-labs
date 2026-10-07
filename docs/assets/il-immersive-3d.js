/**
 * IL Immersive 3D — curriculum stage player (lectures / labs / cert / non-cert).
 * Self-contained WebGL (CSP script-src 'self'; no CDN Three).
 * Procedural scenes: hermetic | rack | k8s | math (math reuses the hermetic geometric renderer). Native .glb load via ILSceneKit.parseGlb (no Three CDN).
 * NOT Noah avatar — that is il-muse-3d.js (coach familiar only).
 * Sibling optional: il-scene-kit.js + il-immersive.js (data-kind hosts / demo /immersive/).
 * v1.4.0 (2026-10-06): skips Blender *_LOD1 duplicates (no z-fight/double draw), addresses glTF nodes by name,
 * and mounts interactive sims (il-immersive-sims.js, data-il-sim) whose state re-tints / reveals authored nodes.
 * v1.5.0 (2026-10-07): predict-then-reveal options shuffle per attempt (keyed answer no longer positional);
 * hosts four more CKA sims (netpol-isolation, rbac-authz, sched-taints, hpa-scale).
 * Boot waits for ILSceneKit when a page loads it after this file (fixes silent procedural fallback).
 * This player owns [data-il-immersive][data-il-scene] curriculum scaffolds.
 */
(function (g) {
  'use strict';

  var CYAN = [0.369, 0.918, 0.831];
  var GOLD = [0.831, 0.659, 0.325];
  var VOID = [0.027, 0.043, 0.086];
  var PAPER = [0.91, 0.933, 0.961];

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
    '  vec3 L = normalize(vec3(0.4,0.9,0.35));',
    '  vec3 V = normalize(vec3(0.0,0.2,1.0));',
    '  float ndl = max(dot(N,L),0.0);',
    '  float rim = pow(1.0 - max(dot(N,V),0.0), 2.2);',
    '  vec3 gold = vec3(0.831,0.659,0.325);',
    '  vec3 base = uColor * (0.18 + 0.82 * ndl);',
    '  vec3 spec = vec3(1.0) * pow(max(dot(reflect(-L,N),V),0.0), 36.0) * 0.45;',
    '  vec3 col = base + spec + uEmissive * uGlow + gold * rim * 0.5;',
    '  col += 0.03 * sin(vW.y * 12.0 + uTime * 1.5);',
    '  gl_FragColor = vec4(col, 0.98);',
    '}'
  ].join('\n');

  function mat4(){ return new Float32Array(16); }
  function ident(o){
    o[0]=1;o[1]=0;o[2]=0;o[3]=0;o[4]=0;o[5]=1;o[6]=0;o[7]=0;
    o[8]=0;o[9]=0;o[10]=1;o[11]=0;o[12]=0;o[13]=0;o[14]=0;o[15]=1; return o;
  }
  function persp(o, fovy, aspect, near, far){
    var f = 1 / Math.tan(fovy / 2), nf = 1 / (near - far);
    o[0]=f/aspect;o[1]=0;o[2]=0;o[3]=0;o[4]=0;o[5]=f;o[6]=0;o[7]=0;
    o[8]=0;o[9]=0;o[10]=(far+near)*nf;o[11]=-1;o[12]=0;o[13]=0;o[14]=2*far*near*nf;o[15]=0; return o;
  }
  function lookAt(o, ex,ey,ez, cx,cy,cz, ux,uy,uz){
    var zx=ex-cx, zy=ey-cy, zz=ez-cz;
    var zl = Math.hypot(zx,zy,zz) || 1; zx/=zl; zy/=zl; zz/=zl;
    var xx=uy*zz-uz*zy, xy=uz*zx-ux*zz, xz=ux*zy-uy*zx;
    var xl = Math.hypot(xx,xy,xz) || 1; xx/=xl; xy/=xl; xz/=xl;
    var yx=zy*xz-zz*xy, yy=zz*xx-zx*xz, yz=zx*xy-zy*xx;
    o[0]=xx;o[1]=yx;o[2]=zx;o[3]=0;o[4]=xy;o[5]=yy;o[6]=zy;o[7]=0;
    o[8]=xz;o[9]=yz;o[10]=zz;o[11]=0;
    o[12]=-(xx*ex+xy*ey+xz*ez);o[13]=-(yx*ex+yy*ey+yz*ez);o[14]=-(zx*ex+zy*ey+zz*ez);o[15]=1;
    return o;
  }
  function mul(o,a,b){
    var i,j,k,s;
    var t = mat4();
    for(i=0;i<4;i++) for(j=0;j<4;j++){ s=0; for(k=0;k<4;k++) s+=a[k*4+i]*b[j*4+k]; t[j*4+i]=s; }
    o.set(t); return o;
  }
  function translate(o,x,y,z){ var t=ident(mat4()); t[12]=x;t[13]=y;t[14]=z; return mul(o,o,t); }
  function scale(o,x,y,z){ var t=ident(mat4()); t[0]=x;t[5]=y;t[10]=z; return mul(o,o,t); }
  function rotateY(o,r){ var c=Math.cos(r),s=Math.sin(r),t=ident(mat4()); t[0]=c;t[2]=-s;t[8]=s;t[10]=c; return mul(o,o,t); }
  function rotateX(o,r){ var c=Math.cos(r),s=Math.sin(r),t=ident(mat4()); t[5]=c;t[6]=s;t[9]=-s;t[10]=c; return mul(o,o,t); }
  function normalFromMV(out, mv){
    out[0]=mv[0];out[1]=mv[1];out[2]=mv[2];
    out[3]=mv[4];out[4]=mv[5];out[5]=mv[6];
    out[6]=mv[8];out[7]=mv[9];out[8]=mv[10];
    return out;
  }

  function compile(gl, type, src){
    var sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      console.warn('[il-immersive-3d] shader', gl.getShaderInfoLog(sh));
      return null;
    }
    return sh;
  }

  function program(gl){
    var vs = compile(gl, gl.VERTEX_SHADER, VERT);
    var fs = compile(gl, gl.FRAGMENT_SHADER, FRAG);
    if (!vs || !fs) return null;
    var p = gl.createProgram();
    gl.attachShader(p, vs); gl.attachShader(p, fs); gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      console.warn('[il-immersive-3d] link', gl.getProgramInfoLog(p));
      return null;
    }
    return {
      p: p,
      aPos: gl.getAttribLocation(p, 'aPos'),
      aNrm: gl.getAttribLocation(p, 'aNrm'),
      uMVP: gl.getUniformLocation(p, 'uMVP'),
      uN: gl.getUniformLocation(p, 'uN'),
      uColor: gl.getUniformLocation(p, 'uColor'),
      uEmissive: gl.getUniformLocation(p, 'uEmissive'),
      uGlow: gl.getUniformLocation(p, 'uGlow'),
      uTime: gl.getUniformLocation(p, 'uTime')
    };
  }

  function boxMesh(){
    var s = 0.5;
    var p = [
      -s,-s,s,  s,-s,s,  s,s,s,  -s,s,s,
      -s,-s,-s, -s,s,-s, s,s,-s, s,-s,-s,
      -s,s,-s, -s,s,s, s,s,s, s,s,-s,
      -s,-s,-s, s,-s,-s, s,-s,s, -s,-s,s,
      s,-s,-s, s,s,-s, s,s,s, s,-s,s,
      -s,-s,-s, -s,-s,s, -s,s,s, -s,s,-s
    ];
    var n = [
      0,0,1,0,0,1,0,0,1,0,0,1,
      0,0,-1,0,0,-1,0,0,-1,0,0,-1,
      0,1,0,0,1,0,0,1,0,0,1,0,
      0,-1,0,0,-1,0,0,-1,0,0,-1,0,
      1,0,0,1,0,0,1,0,0,1,0,0,
      -1,0,0,-1,0,0,-1,0,0,-1,0,0
    ];
    var idx = [];
    for (var f=0;f<6;f++){ var i=f*4; idx.push(i,i+1,i+2,i,i+2,i+3); }
    return { pos: new Float32Array(p), nrm: new Float32Array(n), idx: new Uint16Array(idx) };
  }

  function cylMesh(seg){
    seg = seg || 12;
    var pos=[], nrm=[], idx=[];
    var i, a, x, z, r=0.5, h=0.5;
    for (i=0;i<=seg;i++){
      a = (i/seg)*Math.PI*2; x=Math.cos(a)*r; z=Math.sin(a)*r;
      pos.push(x,-h,z, x,h,z); nrm.push(x,0,z, x,0,z);
    }
    for (i=0;i<seg;i++){
      var i0=i*2, i1=i0+1, i2=i0+2, i3=i0+3;
      idx.push(i0,i2,i1, i1,i2,i3);
    }
    var base = pos.length/3;
    pos.push(0,-h,0); nrm.push(0,-1,0);
    for (i=0;i<=seg;i++){ a=(i/seg)*Math.PI*2; pos.push(Math.cos(a)*r,-h,Math.sin(a)*r); nrm.push(0,-1,0); }
    for (i=0;i<seg;i++) idx.push(base, base+1+i+1, base+1+i);
    base = pos.length/3;
    pos.push(0,h,0); nrm.push(0,1,0);
    for (i=0;i<=seg;i++){ a=(i/seg)*Math.PI*2; pos.push(Math.cos(a)*r,h,Math.sin(a)*r); nrm.push(0,1,0); }
    for (i=0;i<seg;i++) idx.push(base, base+1+i, base+1+i+1);
    return { pos: new Float32Array(pos), nrm: new Float32Array(nrm), idx: new Uint16Array(idx) };
  }

  function upload(gl, mesh){
    var vao = { mesh: mesh };
    vao.pb = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vao.pb);
    gl.bufferData(gl.ARRAY_BUFFER, mesh.pos, gl.STATIC_DRAW);
    vao.nb = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vao.nb);
    gl.bufferData(gl.ARRAY_BUFFER, mesh.nrm, gl.STATIC_DRAW);
    vao.ib = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, vao.ib);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, mesh.idx, gl.STATIC_DRAW);
    vao.count = mesh.idx.length;
    return vao;
  }

  function drawMesh(gl, prog, vao, mvp, nrm, color, emissive, glow, time){
    gl.useProgram(prog.p);
    gl.uniformMatrix4fv(prog.uMVP, false, mvp);
    gl.uniformMatrix3fv(prog.uN, false, nrm);
    gl.uniform3fv(prog.uColor, color);
    gl.uniform3fv(prog.uEmissive, emissive || color);
    gl.uniform1f(prog.uGlow, glow || 0);
    gl.uniform1f(prog.uTime, time || 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, vao.pb);
    gl.enableVertexAttribArray(prog.aPos);
    gl.vertexAttribPointer(prog.aPos, 3, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ARRAY_BUFFER, vao.nb);
    gl.enableVertexAttribArray(prog.aNrm);
    gl.vertexAttribPointer(prog.aNrm, 3, gl.FLOAT, false, 0, 0);
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, vao.ib);
    gl.drawElements(gl.TRIANGLES, vao.count, gl.UNSIGNED_SHORT, 0);
  }

  var CLIPS = {
    hermetic: [
      { id: 'idle', label: 'Idle orrery' },
      { id: 'invoke', label: 'Invoke sigil' },
      { id: 'transcribe', label: 'Transcribe' }
    ],
    /* 2026-10-01: math scene — reuses the geometric (hermetic) renderer
     * with math-appropriate clip labels. Same clip ids, same behaviors. */
    math: [
      { id: 'idle', label: 'Idle diagram' },
      { id: 'invoke', label: 'Construct figure' },
      { id: 'transcribe', label: 'Trace construction' }
    ],
    rack: [
      { id: 'idle', label: 'Idle racks' },
      { id: 'fail', label: 'Node fail' },
      { id: 'heal', label: 'Heal / replace' }
    ],
    k8s: [
      { id: 'idle', label: 'Cluster steady' },
      { id: 'schedule', label: 'Schedule pod' },
      { id: 'scale', label: 'Scale deploy' }
    ]
  };

  var CAPTIONS = {
    hermetic: {
      idle: 'Hermetica lecture — Monas geometry as living diagram (procedural v1).',
      invoke: 'Clip: invoke — gold accent pulse on the sigil axis.',
      transcribe: 'Clip: transcribe — cyan sweep across the tablet plane.'
    },
    math: {
      idle: 'Math lecture — geometric constructions as living diagram (procedural v1).',
      invoke: 'Clip: construct — gold accent pulse along the figure axis.',
      transcribe: 'Clip: trace — cyan sweep across the construction plane.'
    },
    rack: {
      idle: 'Immersive lab — 19″ rack row (procedural). Real .glb optional under /assets/immersive/.',
      fail: 'Clip: fail — amber bay indicates fault domain.',
      heal: 'Clip: heal — cyan bay restored; ticket closed.'
    },
    k8s: {
      idle: 'Immersive lab — control plane + worker mesh (procedural k8s scene).',
      schedule: 'Clip: schedule — pod lands on a worker node.',
      scale: 'Clip: scale — replica count rises across the ring.'
    }
  };

  function resolveScene(raw){
    var s = (raw || 'k8s').toLowerCase();
    if (s.indexOf('math') >= 0) return 'math';
    if (s.indexOf('hermetic') >= 0 || s.indexOf('monas') >= 0) return 'hermetic';
    if (s.indexOf('rack') >= 0 || s.indexOf('server') >= 0 || s.indexOf('dc') >= 0) return 'rack';
    return 'k8s';
  }

  function parseConfig(el){
    var cfg = { mode: '3d-first', engine: 'three', asset: '', scene: 'k8s', captions: true, webgpu: false, gltf: '' };
    var raw = el.getAttribute('data-immersive');
    var j = null;
    if (raw) {
      try {
        j = JSON.parse(raw);
        if (j.mode) cfg.mode = j.mode;
        if (j.engine) cfg.engine = j.engine;
        if (j.asset) cfg.asset = j.asset;
        if (j.captions === false) cfg.captions = false;
        if (j.webgpu != null) cfg.webgpu = !!j.webgpu;
      } catch (e) { /* ignore */ }
    }
    var sceneAttr = el.getAttribute('data-il-scene') || '';
    var eng = el.getAttribute('data-il-engine');
    if (eng) cfg.engine = eng;
    if (el.getAttribute('data-il-webgpu') === '1') cfg.webgpu = true;
    cfg.gltf = el.getAttribute('data-gltf') || el.getAttribute('data-gltf-pending') || '';
    cfg.sim = el.getAttribute('data-il-sim') || (j && j.sim) || '';
    if (!cfg.gltf && cfg.asset && cfg.asset.indexOf('/assets/') === 0) cfg.gltf = cfg.asset;
    if (cfg.asset && cfg.asset.indexOf('procedural:') === 0) {
      cfg.scene = resolveScene(cfg.asset.slice(11));
    } else if (sceneAttr) {
      cfg.scene = resolveScene(sceneAttr);
    } else if (cfg.asset) {
      cfg.scene = resolveScene(cfg.asset);
    }
    /* WebGPU flag path: prefer when requested + navigator.gpu; procedural still WebGL until WGSL port */
    try {
      if (g.ILSceneKit && g.ILSceneKit.preferWebGPU) {
        if (g.ILSceneKit.preferWebGPU({ engine: cfg.engine, webgpu: cfg.webgpu })) {
          cfg.engine = 'webgpu';
          cfg.webgpu = true;
        }
      } else if (cfg.engine === 'webgpu' && !(g.navigator && g.navigator.gpu)) {
        cfg.engine = 'three';
      }
    } catch (e2) { /* ignore */ }
    return cfg;
  }

  function prefersReduced(){
    try { return g.matchMedia && g.matchMedia('(prefers-reduced-motion: reduce)').matches; }
    catch (e) { return false; }
  }

  function t(key, fallback){
    try {
      if (g.ILi18n && typeof g.ILi18n.t === 'function') return g.ILi18n.t(key, fallback);
    } catch (e) { /* ignore */ }
    return fallback;
  }

  function buildChrome(root, cfg){
    var isLab = (cfg.scene === 'rack' || cfg.scene === 'k8s');
    var titleKey = isLab ? 'immersive.lab' : 'immersive.lecture';
    var titleFb = isLab ? 'Immersive lab' : '3D lecture';
    root.innerHTML = '';
    root.classList.add('il-immersive');
    if (root.getAttribute('data-il-compact') === '1') root.classList.add('il-immersive--compact');

    var chrome = document.createElement('div');
    chrome.className = 'il-immersive__chrome';
    chrome.setAttribute('data-il-no-body', '');
    chrome.innerHTML =
      '<div><p class="il-immersive__kicker" data-i18n="immersive.kicker">3D-first · Blender / Unreal / Three</p>' +
      '<p class="il-immersive__title" data-i18n="' + titleKey + '">' + titleFb + '</p></div>' +
      '<span class="il-immersive__badge">' + (cfg.engine || 'three') + ' · ' + cfg.scene + '</span>';
    root.appendChild(chrome);

    var stage = document.createElement('div');
    stage.className = 'il-immersive__stage';
    stage.tabIndex = 0;
    stage.setAttribute('role', 'img');
    stage.setAttribute('aria-label', titleFb + ' — ' + cfg.scene);
    root.appendChild(stage);

    var cap = document.createElement('div');
    cap.className = 'il-immersive__captions';
    cap.setAttribute('data-il-no-body', '');
    cap.setAttribute('aria-live', 'polite');
    stage.appendChild(cap);

    var controls = document.createElement('div');
    controls.className = 'il-immersive__controls';
    controls.setAttribute('data-il-no-body', '');
    controls.setAttribute('role', 'toolbar');
    root.appendChild(controls);

    var fb = document.createElement('div');
    fb.className = 'il-immersive__fallback';
    fb.innerHTML =
      '<div class="il-immersive__fallback-art" aria-hidden="true"></div>' +
      '<p data-i18n="immersive.fallback">Motion reduced — static scene</p>';
    root.appendChild(fb);

    if (g.ILi18n && typeof g.ILi18n.apply === 'function') {
      try { g.ILi18n.apply(root); } catch (e) { /* ignore */ }
    } else {
      chrome.querySelector('.il-immersive__title').textContent = t(titleKey, titleFb);
      chrome.querySelector('.il-immersive__kicker').textContent = t('immersive.kicker', '3D-first · Blender / Unreal / Three');
      fb.querySelector('p').textContent = t('immersive.fallback', 'Motion reduced — static scene');
    }

    return { stage: stage, cap: cap, controls: controls, fb: fb };
  }

  function ScenePlayer(root){
    this.root = root;
    this.cfg = parseConfig(root);
    this.clip = 'idle';
    this.t0 = performance.now();
    this.orbit = { theta: 0.55, phi: 0.35, dist: 5.2, dragging: false, lx: 0, ly: 0 };
    this.raf = 0;
    this.gl = null;
    this.alive = true;

    var ui = buildChrome(root, this.cfg);
    this.stage = ui.stage;
    this.cap = ui.cap;
    this.controls = ui.controls;

    this.setCaption(this.clip);

    if (prefersReduced()) {
      root.classList.add('is-reduced');
      this.cap.textContent = capText(this.cfg.scene, 'idle', (CAPTIONS[this.cfg.scene] || CAPTIONS.k8s).idle);
      return;
    }

    this._buildButtons();
    this._bindOrbit();
    this._lazyGL();
  }

  /* v1.4.0: browsers cap live WebGL contexts (~16 in Chromium; oldest silently lost). Pages like
   * /immersive/ mount 17+ stages, so contexts are created when a stage nears the viewport and
   * released (WEBGL_lose_context) when it leaves; parsed glTF stays in memory and re-uploads. */
  ScenePlayer.prototype._lazyGL = function (){
    var self = this;
    if (!g.IntersectionObserver) { this._wake(); return; }
    this._io = new g.IntersectionObserver(function (entries){
      for (var i = 0; i < entries.length; i++) {
        if (entries[i].isIntersecting) self._wake(); else self._sleep();
      }
    }, { rootMargin: '240px 0px' });
    this._io.observe(this.stage);
  };

  ScenePlayer.prototype._wake = function (){
    if (!this.alive || this.gl) return;
    this._initGL();
    if (!this.gl) return;
    if (this._parsed) this._uploadAuthored();
    else if (!this._probed) { this._probed = true; this._probeGlb(); }
  };

  ScenePlayer.prototype._sleep = function (){
    if (!this.gl) return;
    if (this.raf) g.cancelAnimationFrame(this.raf);
    this.raf = 0;
    try {
      var ext = this.gl.getExtension('WEBGL_lose_context');
      if (ext) ext.loseContext();
    } catch (e) { /* ignore */ }
    if (this.canvas && this.canvas.parentNode) this.canvas.parentNode.removeChild(this.canvas);
    this.gl = null;
    this.canvas = null;
    this._authored = null;
    this.root.setAttribute('data-il-gl', 'sleeping');
  };

  function clipLabel(scene, id, fallback){
    return t('immersive.clip.' + scene + '.' + id, fallback);
  }

  function capText(scene, id, fallback){
    return t('immersive.cap.' + scene + '.' + id, fallback);
  }

  ScenePlayer.prototype.setCaption = function (clipId){
    var map = CAPTIONS[this.cfg.scene] || CAPTIONS.k8s;
    var fb = map[clipId] || map.idle;
    this.cap.textContent = capText(this.cfg.scene, clipId || 'idle', fb);
  };

  ScenePlayer.prototype.refreshChrome = function (){
    if (g.ILi18n && typeof g.ILi18n.apply === 'function') {
      try { g.ILi18n.apply(this.root); } catch (e) { /* ignore */ }
    }
    var self = this;
    Array.prototype.forEach.call(this.controls.querySelectorAll('button[data-il-clip]'), function (b){
      var id = b.getAttribute('data-il-clip');
      var fb = b.getAttribute('data-il-clip-en') || b.textContent;
      b.textContent = clipLabel(self.cfg.scene, id, fb);
    });
    this.setCaption(this.clip);
  };

  ScenePlayer.prototype._buildButtons = function (){
    var self = this;
    var clips = CLIPS[this.cfg.scene] || CLIPS.k8s;
    clips.forEach(function (c){
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('data-il-clip', c.id);
      b.setAttribute('data-il-clip-en', c.label);
      b.textContent = clipLabel(self.cfg.scene, c.id, c.label);
      b.setAttribute('aria-pressed', c.id === 'idle' ? 'true' : 'false');
      b.addEventListener('click', function (){
        self.clip = c.id;
        self.t0 = performance.now();
        self.setCaption(c.id);
        Array.prototype.forEach.call(self.controls.querySelectorAll('button'), function (x){
          x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
        });
      });
      self.controls.appendChild(b);
    });
  };

  ScenePlayer.prototype._bindOrbit = function (){
    var self = this;
    var el = this.stage;
    function down(ev){
      self.orbit.dragging = true;
      self.orbit.lx = ev.clientX != null ? ev.clientX : (ev.touches && ev.touches[0].clientX);
      self.orbit.ly = ev.clientY != null ? ev.clientY : (ev.touches && ev.touches[0].clientY);
    }
    function move(ev){
      if (!self.orbit.dragging) return;
      var x = ev.clientX != null ? ev.clientX : (ev.touches && ev.touches[0].clientX);
      var y = ev.clientY != null ? ev.clientY : (ev.touches && ev.touches[0].clientY);
      var dx = x - self.orbit.lx, dy = y - self.orbit.ly;
      self.orbit.lx = x; self.orbit.ly = y;
      self.orbit.theta += dx * 0.008;
      self.orbit.phi = Math.max(-1.2, Math.min(1.35, self.orbit.phi + dy * 0.008));
      if (ev.cancelable) ev.preventDefault();
    }
    function up(){ self.orbit.dragging = false; }
    el.addEventListener('mousedown', down);
    el.addEventListener('mousemove', move);
    g.addEventListener('mouseup', up);
    el.addEventListener('touchstart', down, { passive: true });
    el.addEventListener('touchmove', move, { passive: false });
    el.addEventListener('touchend', up);
    el.addEventListener('wheel', function (ev){
      self.orbit.dist = Math.max(3.2, Math.min(9, self.orbit.dist + ev.deltaY * 0.01));
      ev.preventDefault();
    }, { passive: false });
    el.addEventListener('keydown', function (ev){
      if (ev.key === 'ArrowLeft') self.orbit.theta -= 0.12;
      if (ev.key === 'ArrowRight') self.orbit.theta += 0.12;
      if (ev.key === 'ArrowUp') self.orbit.phi = Math.min(1.35, self.orbit.phi + 0.08);
      if (ev.key === 'ArrowDown') self.orbit.phi = Math.max(-1.2, self.orbit.phi - 0.08);
    });
  };

  ScenePlayer.prototype._initGL = function (){
    var canvas = document.createElement('canvas');
    this.stage.insertBefore(canvas, this.cap);
    var gl = null;
    if (g.ILSceneKit && g.ILSceneKit.acquireGraphics) {
      var gfx = g.ILSceneKit.acquireGraphics(canvas, { webgpu: this.cfg.webgpu, engine: this.cfg.engine, alpha: false });
      gl = gfx.gl || null;
      this._gfxApi = gfx.api;
      this._gfxLabel = gfx.label;
    } else {
      gl = canvas.getContext('webgl', { antialias: true, alpha: false });
      this._gfxApi = gl ? 'webgl' : 'none';
      this._gfxLabel = gl ? 'WebGL' : 'none';
    }
    if (!gl) {
      this.root.classList.add('is-reduced');
      return;
    }
    this.gl = gl;
    this.canvas = canvas;
    this.root.setAttribute('data-il-gl', 'awake');
    this.prog = program(gl);
    if (!this.prog) { this.root.classList.add('is-reduced'); return; }
    this.box = upload(gl, boxMesh());
    this.cyl = upload(gl, cylMesh(14));
    this.particles = this._makeParticles(48);
    gl.enable(gl.DEPTH_TEST);
    gl.enable(gl.CULL_FACE);
    this._paintHud();
    this._resize();
    var self = this;
    if (!this._resizeBound) {
      this._resizeBound = true;
      g.addEventListener('resize', function (){ self._resize(); });
    }
    this._loop();
  };

  ScenePlayer.prototype._paintHud = function (){
    var badge = this.root.querySelector('.il-immersive__badge');
    if (!badge) return;
    var eng = this._gfxLabel || this.cfg.engine || 'WebGL';
    var mode = '';
    if (this._authoredOk) mode = ' · authored .glb';
    else if (this.cfg.gltf && String(this.cfg.gltf).indexOf('.pending.') >= 0) mode = ' · glTF scaffold';
    else if (this._authoredTried) mode = ' · procedural fallback';
    badge.textContent = eng + ' · ' + this.cfg.scene + mode;
    badge.setAttribute('data-il-gfx', this._gfxApi || 'webgl');
    badge.setAttribute('data-il-mesh', this._authoredOk ? 'authored' : 'procedural');
  };

  ScenePlayer.prototype._makeParticles = function (n){
    var out = [];
    for (var i = 0; i < n; i++) {
      out.push({
        a: Math.random() * Math.PI * 2,
        r: 1.2 + Math.random() * 2.4,
        y: -0.4 + Math.random() * 2.2,
        s: 0.03 + Math.random() * 0.05,
        sp: 0.35 + Math.random() * 0.9,
        gold: Math.random() > 0.62
      });
    }
    return out;
  };

  ScenePlayer.prototype._renderParticles = function (P, V, time, amp){
    if (!this.particles) return;
    for (var i = 0; i < this.particles.length; i++) {
      var p = this.particles[i];
      var a = p.a + time * p.sp * 0.35;
      var x = Math.cos(a) * p.r;
      var z = Math.sin(a) * p.r;
      var y = p.y + Math.sin(time * 1.4 + i) * 0.08;
      var col = p.gold ? GOLD : CYAN;
      var glow = 0.18 + amp * 0.45;
      this._drawObject(this.box, x, y, z, p.s, p.s, p.s, a, col, glow, time, P, V);
    }
  };

  ScenePlayer.prototype._resize = function (){
    if (!this.gl || !this.canvas) return;
    var dpr = Math.min(g.devicePixelRatio || 1, 2);
    var w = this.stage.clientWidth || 640;
    var h = this.stage.clientHeight || 280;
    this.canvas.width = Math.floor(w * dpr);
    this.canvas.height = Math.floor(h * dpr);
    this.gl.viewport(0, 0, this.canvas.width, this.canvas.height);
    this._aspect = w / Math.max(h, 1);
  };

  ScenePlayer.prototype._probeGlb = function (){
    var asset = this.cfg.gltf || this.cfg.asset || '';
    if (!asset || asset.indexOf('procedural:') === 0) return;
    var self = this;
    this._authoredTried = false;
    this._authoredOk = false;
    this._authored = null;
    if (/\.pending\.json($|\?)/i.test(asset)) {
      self.cap.textContent = (self.cap.textContent || '') + ' · glTF scaffold (pending Blender export).';
      self._paintHud();
      return;
    }
    if (!/\.glb($|\?)/i.test(asset) && asset.indexOf('/assets/immersive/') < 0) return;
    if (!self.gl) return;
    self._authoredTried = true;
    var loader = (g.ILSceneKit && g.ILSceneKit.loadGltf) ? g.ILSceneKit.loadGltf : null;
    var parse = (g.ILSceneKit && g.ILSceneKit.parseGlb) ? g.ILSceneKit.parseGlb : null;
    function applyParsed(parsed) {
      if (!parsed || !parsed.ok || !parsed.meshes || !parsed.meshes.length) {
        self._authoredOk = false;
        self.cap.textContent = (self.cap.textContent || '') + ' · procedural fallback (authored .glb unavailable).';
        self._paintHud();
        return;
      }
      self._parsed = parsed;
      self._uploadAuthored();
      try {
        if (g.ILSceneKit && g.ILSceneKit.emitSceneEvent) {
          g.ILSceneKit.emitSceneEvent('il-immersive-glb', { url: asset, meshes: parsed.meshes.length, ok: true });
        }
      } catch (e2) { /* ignore */ }
    }
    try {
      if (loader) {
        loader(asset).then(applyParsed).catch(function (){
          self._authoredOk = false;
          self.cap.textContent = (self.cap.textContent || '') + ' · procedural fallback (fetch/parse fail).';
          self._paintHud();
        });
      } else if (parse) {
        g.fetch(asset).then(function (res){
          if (!res || !res.ok) throw new Error('http');
          return res.arrayBuffer();
        }).then(function (buf){ applyParsed(parse(buf)); })
          .catch(function (){
            self._authoredOk = false;
            self.cap.textContent = (self.cap.textContent || '') + ' · procedural fallback (fetch/parse fail).';
            self._paintHud();
          });
      } else {
        self.cap.textContent = (self.cap.textContent || '') + ' · procedural fallback (no native GLB parser).';
        self._paintHud();
      }
    } catch (e) {
      self._authoredOk = false;
      self._paintHud();
    }
  };

  /** Upload parsed glTF meshes into the live context (first load or after a sleep/wake cycle). */
  ScenePlayer.prototype._uploadAuthored = function (){
    var parsed = this._parsed;
    if (!parsed || !this.gl) return; /* asleep: _wake() re-enters here */
    var reupload = !!this._uploadedOnce;
    this._uploadedOnce = true;
    var uploaded = [];
    for (var i = 0; i < parsed.meshes.length; i++) {
      var m = parsed.meshes[i];
      var name = m.node || m.name || ('mesh-' + i);
      var lod = m.lod != null ? m.lod : (/(_LOD1$|^lod1-)/i.test(name) ? 1 : 0);
      if (lod) { uploaded.push({ name: name, lod: 1 }); continue; } /* never upload LOD1 duplicates */
      var vao = upload(this.gl, {
        pos: m.positions,
        nrm: m.normals,
        idx: m.indices instanceof Uint16Array ? m.indices : new Uint16Array(m.indices)
      });
      vao.color = (m.material && m.material.color) || CYAN;
      vao.emissive = (m.material && m.material.emissive) || vao.color;
      vao.name = name;
      vao.lod = 0;
      vao.cur = vao.color.slice(0, 3);
      vao.curGlow = null;
      uploaded.push(vao);
    }
    this._authored = uploaded;
    this._authoredOk = true;
    if (!reupload) {
      var lod0 = uploaded.filter(function (v) { return !v.lod; }).length;
      this._baseCaption = (this.cap.textContent || '') + ' · authored .glb (' + lod0 + ' nodes' +
        (uploaded.length > lod0 ? ', ' + (uploaded.length - lod0) + ' LOD1 skipped' : '') + ').';
      this.cap.textContent = this._baseCaption;
      this._initSim();
    } else if (this._sim) {
      this._simApply('init');
    }
    this._paintHud();
  };

  ScenePlayer.prototype._renderAuthored = function (P, V, time, amp){
    if (!this._authored || !this._authored.length) return;
    var glowBase = 0.12 + amp * 0.35;
    var k = 0.12; /* per-frame ease toward sim target */
    for (var i = 0; i < this._authored.length; i++) {
      var vao = this._authored[i];
      if (vao.lod) continue; /* Blender LOD1 duplicate / kit proxy — never overdraw LOD0 */
      var st = vao.simStyle || null;
      if (st && st.hide) continue;
      if (!st && /^sim-/.test(vao.name)) continue; /* sim-only nodes stay hidden without a sim */
      var base = vao.color || CYAN;
      var glow = glowBase;
      /* gentle pulse on gold-ish materials */
      if (base[0] > 0.7 && base[1] > 0.5 && base[1] < 0.8) glow = 0.2 + amp * 0.45;
      var target = (st && st.color) ? st.color : base;
      if (st && st.glow != null) glow = st.glow * (st.pulse ? (0.55 + 0.45 * Math.abs(Math.sin(time * 3.4))) : 1);
      var c = vao.cur || (vao.cur = base.slice(0, 3));
      c[0] += (target[0] - c[0]) * k; c[1] += (target[1] - c[1]) * k; c[2] += (target[2] - c[2]) * k;
      vao.curGlow = vao.curGlow == null ? glow : vao.curGlow + (glow - vao.curGlow) * 0.2;
      this._drawObject(vao, 0, 0, 0, 1, 1, 1, 0, c, vao.curGlow, time, P, V);
    }
  };

  /* ── Interactive sims (state changes the scene) ───────────────────────── */
  function simStore(){
    try { return JSON.parse(g.localStorage.getItem('il.immersiveSims.v1') || '{}') || {}; } catch (e) { return {}; }
  }
  function simSave(db){
    try { g.localStorage.setItem('il.immersiveSims.v1', JSON.stringify(db)); } catch (e) { /* private mode */ }
  }
  function simTrack(name, props){
    try { if (g.ILAnalytics && g.ILAnalytics.track) g.ILAnalytics.track(name, props); } catch (e) { /* ignore */ }
    try { if (g.ILSceneKit && g.ILSceneKit.emitSceneEvent) g.ILSceneKit.emitSceneEvent('il-immersive-sim', { name: name, detail: props }); } catch (e2) { /* ignore */ }
  }
  function el(tag, cls, text){
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  ScenePlayer.prototype._initSim = function (){
    var S = g.ILImmersiveSims;
    if (!this.cfg.sim || !S || !S.get) return;
    var sim = S.get(this.cfg.sim);
    if (!sim || this._sim) return;
    var self = this;
    this._sim = sim;
    this._simState = S.merge(sim.initial, {});
    this.root.classList.add('il-immersive--sim');
    if (this.controls) this.controls.hidden = true; /* generic procedural clips are meaningless on a sim stage */
    this.root.setAttribute('data-il-sim-ready', sim.id);

    var panel = el('div', 'il-immersive__sim');
    panel.setAttribute('data-il-no-body', '');
    var head = el('div', 'il-immersive__sim-head');
    head.appendChild(el('span', 'il-immersive__sim-kicker', 'Interactive sim · ' + sim.cert));
    head.appendChild(el('span', 'il-immersive__sim-title', sim.title));
    this._simVerdict = el('span', 'il-immersive__sim-verdict', '');
    head.appendChild(this._simVerdict);
    panel.appendChild(head);

    var scen = el('div', 'il-immersive__sim-row');
    scen.setAttribute('role', 'group');
    scen.setAttribute('aria-label', 'Scenarios');
    sim.scenarios.forEach(function (sc){
      var b = el('button', 'il-immersive__sim-btn', sc.label);
      b.type = 'button';
      b.setAttribute('data-il-sim-scenario', sc.id);
      b.addEventListener('click', function (){ self._simScenario(sc); });
      scen.appendChild(b);
    });
    panel.appendChild(scen);

    var tog = el('div', 'il-immersive__sim-row il-immersive__sim-row--toggles');
    tog.setAttribute('role', 'group');
    tog.setAttribute('aria-label', 'Free play toggles');
    this._simToggles = {};
    sim.toggles.forEach(function (t){
      var b = el('button', 'il-immersive__sim-toggle', '');
      b.type = 'button';
      b.setAttribute('data-il-sim-toggle', t.id);
      b.addEventListener('click', function (){
        self._simState[t.id] = !self._simState[t.id];
        self._simPredictClose();
        self._simApply('toggle:' + t.id);
      });
      self._simToggles[t.id] = { btn: b, def: t };
      tog.appendChild(b);
    });
    panel.appendChild(tog);

    this._simPredict = el('div', 'il-immersive__sim-predict');
    this._simPredict.hidden = true;
    panel.appendChild(this._simPredict);
    this._simResult = el('p', 'il-immersive__sim-result', '');
    this._simResult.setAttribute('aria-live', 'polite');
    panel.appendChild(this._simResult);
    this._simScore = el('p', 'il-immersive__sim-score', '');
    panel.appendChild(this._simScore);
    panel.appendChild(el('p', 'il-immersive__sim-honesty', S.honesty || 'In-browser rules engine; no live infrastructure.'));

    var fb = this.root.querySelector('.il-immersive__fallback');
    this.root.insertBefore(panel, fb || null);
    this._simPanel = panel;
    this._simApply('init');
    this._simRenderScore();
  };

  ScenePlayer.prototype._simApply = function (reason){
    var S = g.ILImmersiveSims, sim = this._sim;
    if (!S || !sim) return;
    var d = sim.derive(this._simState);
    this._simDerived = d;
    for (var i = 0; i < (this._authored || []).length; i++) {
      var v = this._authored[i];
      v.simStyle = S.styleFor(v.name, d.rules);
    }
    for (var id in this._simToggles) {
      var tg = this._simToggles[id], on = !!this._simState[id];
      tg.btn.textContent = tg.def.label + ': ' + (on ? tg.def.on : tg.def.off);
      tg.btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      var risk = tg.def.risk || 'off';
      tg.btn.setAttribute('data-risk', risk === 'none' ? '0' : ((risk === 'on') === on ? '1' : '0'));
    }
    this._simVerdict.textContent = d.verdict;
    this._simVerdict.setAttribute('data-verdict', d.verdict);
    this.cap.textContent = d.caption + ' · sim (rules engine, not a live system)';
    this.root.setAttribute('data-il-sim-verdict', d.verdict);
    if (reason && reason !== 'init') simTrack('immersive_sim_state', { sim: sim.id, reason: reason, verdict: d.verdict });
  };

  ScenePlayer.prototype._simPredictClose = function (){
    if (this._simPredict) { this._simPredict.hidden = true; this._simPredict.innerHTML = ''; }
    this._simPending = null;
  };

  ScenePlayer.prototype._simScenario = function (sc){
    var self = this, S = g.ILImmersiveSims;
    if (!sc.predict) {
      this._simPredictClose();
      this._simState = S.merge(this._simState, sc.set);
      this._simResult.textContent = '';
      this._simApply('scenario:' + sc.id);
      return;
    }
    /* Predict-then-reveal: the scene does not change until the learner commits. */
    this._simPredictClose();
    this._simPending = { sc: sc, t0: (g.performance && performance.now()) || Date.now() };
    var box = this._simPredict;
    box.appendChild(el('p', 'il-immersive__sim-q', 'Predict first: ' + sc.predict.q));
    /* Shuffle display order per attempt so the keyed answer is never positional; data-il-sim-option keeps the original index. */
    var order = (S.shuffleOrder ? S.shuffleOrder(sc.predict.options.length) : sc.predict.options.map(function (_, i){ return i; }));
    order.forEach(function (idx){
      var opt = sc.predict.options[idx];
      var b = el('button', 'il-immersive__sim-opt', opt);
      b.type = 'button';
      b.setAttribute('data-il-sim-option', String(idx));
      b.addEventListener('click', function (){ self._simCommit(idx); });
      box.appendChild(b);
    });
    box.hidden = false;
    this._simResult.textContent = '';
    try { box.querySelector('button').focus(); } catch (e) { /* ignore */ }
  };

  ScenePlayer.prototype._simCommit = function (choice){
    var p = this._simPending, S = g.ILImmersiveSims, sim = this._sim;
    if (!p || !S) return;
    var ms = Math.round(((g.performance && performance.now()) || Date.now()) - p.t0);
    var res = S.scorePredict(sim.id, p.sc.id, choice);
    this._simPredictClose();
    this._simState = S.merge(this._simState, p.sc.set);
    this._simApply('scenario:' + p.sc.id);
    var db = simStore();
    var rec = db[sim.id] || (db[sim.id] = { attempts: 0, correct: 0, scenarios: {} });
    var sr = rec.scenarios[p.sc.id] || (rec.scenarios[p.sc.id] = { a: 0, c: 0, lastMs: 0 });
    rec.attempts += 1; sr.a += 1; sr.lastMs = ms;
    if (res && res.correct) { rec.correct += 1; sr.c += 1; }
    simSave(db);
    this._simResult.textContent = (res && res.correct ? 'Correct. ' : 'Not quite — answer: “' + p.sc.predict.options[res ? res.answer : 0] + '”. ') + (res ? res.why : '');
    this._simResult.setAttribute('data-correct', res && res.correct ? '1' : '0');
    simTrack('immersive_sim_predict', { sim: sim.id, scenario: p.sc.id, correct: !!(res && res.correct), ms: ms });
    this._simRenderScore();
  };

  ScenePlayer.prototype._simRenderScore = function (){
    var sim = this._sim; if (!sim || !this._simScore) return;
    var rec = simStore()[sim.id] || { attempts: 0, correct: 0, scenarios: {} };
    var next = null;
    for (var i = 0; i < sim.scenarios.length; i++) {
      var sc = sim.scenarios[i];
      if (!sc.predict) continue;
      var r = rec.scenarios[sc.id];
      if (!r || r.c === 0) { next = sc; break; }
    }
    this._simScore.textContent = 'Predictions ' + rec.correct + '/' + rec.attempts + ' correct (stored on this device)' +
      (next ? ' · next drill: ' + next.label : ' · all drills mastered');
    var btns = this._simPanel.querySelectorAll('[data-il-sim-scenario]');
    for (var j = 0; j < btns.length; j++) {
      btns[j].setAttribute('data-next', next && btns[j].getAttribute('data-il-sim-scenario') === next.id ? '1' : '0');
    }
  };

  ScenePlayer.prototype._clipAmp = function (elapsed){
    var c = this.clip;
    if (c === 'idle') return 0.15 + 0.05 * Math.sin(elapsed * 1.2);
    if (c === 'invoke' || c === 'fail') return 0.55 + 0.35 * Math.abs(Math.sin(elapsed * 3.2));
    if (c === 'transcribe' || c === 'heal') return 0.4 + 0.25 * Math.sin(elapsed * 2.1);
    if (c === 'schedule' || c === 'scale') return 0.45 + 0.3 * Math.sin(elapsed * 2.6);
    return 0.2;
  };

  ScenePlayer.prototype._drawObject = function (mesh, x,y,z, sx,sy,sz, ry, color, glow, time, P, V){
    var M = ident(mat4());
    translate(M, x,y,z);
    rotateY(M, ry || 0);
    scale(M, sx,sy,sz);
    var MV = mul(mat4(), V, M);
    var MVP = mul(mat4(), P, MV);
    var N = new Float32Array(9);
    normalFromMV(N, MV);
    drawMesh(this.gl, this.prog, mesh, MVP, N, color, color, glow, time);
  };

  ScenePlayer.prototype._renderHermetic = function (P, V, time, amp){
    var gld = GOLD, cy = CYAN;
    this._drawObject(this.cyl, 0, 0.05, 0, 2.2, 0.06, 2.2, time*0.15, [0.08,0.12,0.2], 0.05, time, P, V);
    this._drawObject(this.cyl, 0, 0.2, 0, 1.6, 0.04, 1.6, -time*0.35, cy, 0.25+amp*0.4, time, P, V);
    this._drawObject(this.cyl, 0, 0.35, 0, 1.1, 0.04, 1.1, time*0.55, gld, 0.2+amp*0.5, time, P, V);
    this._drawObject(this.box, 0, 0.85, 0, 0.55, 0.55, 0.55, time*0.4, cy, 0.35+amp, time, P, V);
    this._drawObject(this.box, 0, 1.35, 0, 0.18, 0.7, 0.18, 0, gld, 0.5+amp, time, P, V);
    this._drawObject(this.box, 0, -0.35, 0.9, 1.4, 0.08, 0.9, 0.2, [0.12,0.16,0.24], 0.08, time, P, V);
  };

  ScenePlayer.prototype._renderRack = function (P, V, time, amp){
    var i, bay, glow, col;
    this._drawObject(this.box, 0, -0.85, 0, 4.2, 0.12, 2.2, 0, [0.06,0.08,0.12], 0.02, time, P, V);
    for (i = -1; i <= 1; i++) {
      this._drawObject(this.box, i * 1.35, 0.2, 0, 1.05, 2.0, 0.7, 0, [0.1,0.14,0.2], 0.05, time, P, V);
      for (bay = 0; bay < 6; bay++) {
        glow = 0.08;
        col = CYAN;
        if (this.clip === 'fail' && i === 0 && bay === 2) { glow = 0.7 * amp; col = GOLD; }
        if (this.clip === 'heal' && i === 0 && bay === 2) { glow = 0.55 * amp; col = CYAN; }
        if (this.clip === 'idle' && ((bay + i + 3) % 4 === 0)) glow = 0.2 + 0.1 * Math.sin(time * 2 + bay);
        this._drawObject(this.box, i * 1.35, -0.55 + bay * 0.28, 0.28, 0.75, 0.1, 0.12, 0, col, glow, time, P, V);
      }
    }
  };

  ScenePlayer.prototype._renderK8s = function (P, V, time, amp){
    var self = this;
    this._drawObject(this.cyl, 0, 0.9, 0, 0.75, 0.38, 0.75, time * 0.22, GOLD, 0.42 + amp * 0.4, time, P, V);
    this._drawObject(this.box, 0, 1.38, 0, 0.38, 0.38, 0.38, time * 0.55, CYAN, 0.55 + amp * 0.5, time, P, V);
    this._drawObject(this.cyl, 0, 0.55, 0, 1.15, 0.04, 1.15, -time * 0.4, CYAN, 0.22 + amp * 0.25, time, P, V);
    var n = this.clip === 'scale' ? 7 : 5;
    for (var i = 0; i < n; i++) {
      var a = (i / n) * Math.PI * 2 + time * 0.25;
      var r = 1.85;
      var x = Math.cos(a) * r, z = Math.sin(a) * r;
      var glow = 0.15;
      if (this.clip === 'schedule' && i === Math.floor(time * 1.5) % n) glow = 0.7 * amp;
      if (this.clip === 'scale') glow = 0.25 + 0.35 * amp;
      self._drawObject(self.box, x, 0.15, z, 0.45, 0.55, 0.45, -a, CYAN, glow, time, P, V);
    }
    this._drawObject(this.cyl, 0, -0.2, 0, 3.6, 0.05, 3.6, 0, [0.08,0.12,0.18], 0.06, time, P, V);
  };

  ScenePlayer.prototype._loop = function (){
    if (!this.alive || !this.gl) return;
    var self = this;
    var gl = this.gl;
    var time = (performance.now() - this.t0) / 1000;
    var amp = this._clipAmp(time);
    var w = this.canvas.width, h = this.canvas.height;
    gl.viewport(0, 0, w, h);
    gl.clearColor(VOID[0], VOID[1], VOID[2], 1);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    var P = persp(mat4(), Math.PI / 4, this._aspect || 1.6, 0.1, 40);
    var th = this.orbit.theta + (this.orbit.dragging ? 0 : time * 0.08);
    var ph = this.orbit.phi;
    var dist = this.orbit.dist;
    var ex = Math.cos(ph) * Math.sin(th) * dist;
    var ey = Math.sin(ph) * dist + 0.6;
    var ez = Math.cos(ph) * Math.cos(th) * dist;
    var V = lookAt(mat4(), ex, ey, ez, 0, 0.4, 0, 0, 1, 0);

    if (this._authoredOk && this._authored && this._authored.length) {
      this._renderAuthored(P, V, time, amp);
    } else if (this.cfg.scene === 'hermetic' || this.cfg.scene === 'math') {
      this._renderHermetic(P, V, time, amp);
    } else if (this.cfg.scene === 'rack') {
      this._renderRack(P, V, time, amp);
    } else {
      this._renderK8s(P, V, time, amp);
    }
    this._renderParticles(P, V, time, amp);

    this.raf = g.requestAnimationFrame(function (){ self._loop(); });
  };

  ScenePlayer.prototype.destroy = function (){
    this.alive = false;
    if (this.raf) g.cancelAnimationFrame(this.raf);
  };

  var registry = [];

  function mount(el){
    if (!el || el._ilImmersive) return el._ilImmersive;
    var player = new ScenePlayer(el);
    el._ilImmersive = player;
    registry.push(player);
    return player;
  }

  function mountAll(scope){
    var root = scope || g.document;
    if (!root || !root.querySelectorAll) return [];
    var nodes = root.querySelectorAll('[data-il-immersive][data-il-scene]');
    var out = [];
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].getAttribute('data-il-immersive-ready')) continue; /* sibling il-immersive.js owns data-kind hosts */
      out.push(mount(nodes[i]));
    }
    return out;
  }

  function scaffoldDefaults(){
    /* Ensure JSON-shaped default is present on every mounted node */
    var nodes = g.document.querySelectorAll('[data-il-immersive][data-il-scene]');
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (!el.getAttribute('data-immersive')) {
        var scene = resolveScene(el.getAttribute('data-il-scene') || 'k8s');
        var eng = el.getAttribute('data-il-engine') || 'three';
        el.setAttribute('data-immersive', JSON.stringify({
          mode: '3d-first',
          engine: eng,
          asset: 'procedural:' + scene
        }));
      }
    }
  }

  var booted = false;
  function boot(){
    if (booted) return;
    booted = true;
    scaffoldDefaults();
    mountAll();
  }

  /* Deferred pages sometimes load il-scene-kit.js AFTER this file. Mounting before the kit exists
   * meant "no native GLB parser" → silent procedural fallback. Wait for DOMContentLoaded (all
   * deferred scripts have run by then) unless the kit is already present or the page is complete. */
  if (g.document && (g.document.readyState === 'loading' || (!g.ILSceneKit && g.document.readyState !== 'complete'))) {
    g.document.addEventListener('DOMContentLoaded', boot);
    g.addEventListener('load', boot);
  } else {
    boot();
  }

  g.document && g.document.addEventListener('il:i18n', function (){
    registry.forEach(function (p){
      if (p && typeof p.refreshChrome === 'function') p.refreshChrome();
    });
  });

  g.ILImmersive3D = {
    mount: mount,
    mountAll: mountAll,
    resolveScene: resolveScene,
    version: '1.5.0',
    engines: ['three', 'godot', 'unreal', 'webgpu'],
    scenes: ['hermetic', 'rack', 'k8s', 'math'],
    note: 'Curriculum scenes. Noah = il-muse-3d (separate).',
    webgpuFlag: true,
    gltfLectureHook: true,
    nativeGlb: true,
    lodSkip: true,
    sims: true
  };
})(typeof window !== 'undefined' ? window : this);
