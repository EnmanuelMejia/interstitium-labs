/**
 * IL Scene Kit — shared WebGL / curriculum 3D utilities (CSP-safe, no CDN).
 * Used by Lab Muse 3D familiar + Immersive Player (lectures / cert labs / sims).
 * Palette: cyan #5EEAD4 · gold #D4A853 · void #070B16. Interstitium original.
 * Optional Three.js/glTF path: see docs/ops/IMMERSIVE-3D.md (vendored when present).
 */
(function (g) {
  'use strict';

  var CYAN = [0.369, 0.918, 0.831];
  var GOLD = [0.831, 0.659, 0.325];
  var VOID = [0.027, 0.043, 0.086];

  function prefersReducedMotion() {
    try { return !!(g.matchMedia && g.matchMedia('(prefers-reduced-motion: reduce)').matches); }
    catch (e) { return false; }
  }

  function isMobile() {
    try { return !!(g.matchMedia && g.matchMedia('(max-width: 768px)').matches); }
    catch (e) { return false; }
  }

  function dprCap(max) {
    var d = g.devicePixelRatio || 1;
    return Math.min(d, max == null ? (isMobile() ? 1.75 : 2) : max);
  }

  function compileShader(gl, type, src) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      try { console.warn('[ILSceneKit] shader', gl.getShaderInfoLog(sh)); } catch (e) {}
      gl.deleteShader(sh);
      return null;
    }
    return sh;
  }

  function linkProgram(gl, vsSrc, fsSrc) {
    var vs = compileShader(gl, gl.VERTEX_SHADER, vsSrc);
    var fs = compileShader(gl, gl.FRAGMENT_SHADER, fsSrc);
    if (!vs || !fs) return null;
    var p = gl.createProgram();
    gl.attachShader(p, vs);
    gl.attachShader(p, fs);
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
      try { console.warn('[ILSceneKit] link', gl.getProgramInfoLog(p)); } catch (e) {}
      return null;
    }
    return p;
  }

  function resizeCanvas(canvas, gl, root, mobile) {
    var dpr = dprCap(mobile ? 1.75 : 2);
    var w = Math.max(1, (root && root.clientWidth) || canvas.clientWidth || 320);
    var h = Math.max(1, (root && root.clientHeight) || canvas.clientHeight || 180);
    canvas.width = Math.floor(w * dpr);
    canvas.height = Math.floor(h * dpr);
    if (gl) gl.viewport(0, 0, canvas.width, canvas.height);
    return { w: w, h: h, dpr: dpr, aspect: w / h };
  }

  /* —— minimal mat4 —— */
  function mat4() { return new Float32Array(16); }
  function mat4Identity(out) {
    out = out || mat4();
    out[0]=1;out[1]=0;out[2]=0;out[3]=0;
    out[4]=0;out[5]=1;out[6]=0;out[7]=0;
    out[8]=0;out[9]=0;out[10]=1;out[11]=0;
    out[12]=0;out[13]=0;out[14]=0;out[15]=1;
    return out;
  }
  function mat4Perspective(out, fovy, aspect, near, far) {
    var f = 1 / Math.tan(fovy / 2), nf = 1 / (near - far);
    out[0]=f/aspect;out[1]=0;out[2]=0;out[3]=0;
    out[4]=0;out[5]=f;out[6]=0;out[7]=0;
    out[8]=0;out[9]=0;out[10]=(far+near)*nf;out[11]=-1;
    out[12]=0;out[13]=0;out[14]=(2*far*near)*nf;out[15]=0;
    return out;
  }
  function mat4LookAt(out, eye, center, up) {
    var zx=eye[0]-center[0], zy=eye[1]-center[1], zz=eye[2]-center[2];
    var len=1/Math.max(Math.hypot(zx,zy,zz),1e-6); zx*=len; zy*=len; zz*=len;
    var xx=up[1]*zz-up[2]*zy, xy=up[2]*zx-up[0]*zz, xz=up[0]*zy-up[1]*zx;
    len=1/Math.max(Math.hypot(xx,xy,xz),1e-6); xx*=len; xy*=len; xz*=len;
    var yx=zy*xz-zz*xy, yy=zz*xx-zx*xz, yz=zx*xy-zy*xx;
    out[0]=xx;out[1]=yx;out[2]=zx;out[3]=0;
    out[4]=xy;out[5]=yy;out[6]=zy;out[7]=0;
    out[8]=xz;out[9]=yz;out[10]=zz;out[11]=0;
    out[12]=-(xx*eye[0]+xy*eye[1]+xz*eye[2]);
    out[13]=-(yx*eye[0]+yy*eye[1]+yz*eye[2]);
    out[14]=-(zx*eye[0]+zy*eye[1]+zz*eye[2]);
    out[15]=1;
    return out;
  }
  function mat4Multiply(out, a, b) {
    var a00=a[0],a01=a[1],a02=a[2],a03=a[3],a10=a[4],a11=a[5],a12=a[6],a13=a[7];
    var a20=a[8],a21=a[9],a22=a[10],a23=a[11],a30=a[12],a31=a[13],a32=a[14],a33=a[15];
    var i,b0,b1,b2,b3;
    for (i=0;i<4;i++){
      b0=b[i*4];b1=b[i*4+1];b2=b[i*4+2];b3=b[i*4+3];
      out[i*4]=b0*a00+b1*a10+b2*a20+b3*a30;
      out[i*4+1]=b0*a01+b1*a11+b2*a21+b3*a31;
      out[i*4+2]=b0*a02+b1*a12+b2*a22+b3*a32;
      out[i*4+3]=b0*a03+b1*a13+b2*a23+b3*a33;
    }
    return out;
  }
  function mat4FromRTS(out, rx, ry, rz, tx, ty, tz, sx, sy, sz) {
    var cx=Math.cos(rx),sxr=Math.sin(rx),cy=Math.cos(ry),syr=Math.sin(ry),cz=Math.cos(rz),szr=Math.sin(rz);
    var m00=cy*cz,m01=cy*szr,m02=-syr;
    var m10=sxr*syr*cz-cx*szr,m11=sxr*syr*szr+cx*cz,m12=sxr*cy;
    var m20=cx*syr*cz+sxr*szr,m21=cx*syr*szr-sxr*cz,m22=cx*cy;
    out[0]=m00*sx;out[1]=m01*sx;out[2]=m02*sx;out[3]=0;
    out[4]=m10*sy;out[5]=m11*sy;out[6]=m12*sy;out[7]=0;
    out[8]=m20*sz;out[9]=m21*sz;out[10]=m22*sz;out[11]=0;
    out[12]=tx;out[13]=ty;out[14]=tz;out[15]=1;
    return out;
  }

  /** Detect vendored Three (optional). Place at /assets/vendor/three.min.js */
  function hasThree() {
    return !!(g.THREE && g.THREE.WebGLRenderer);
  }

  function hasGLTFLoader() {
    return !!(g.THREE && (g.THREE.GLTFLoader || g.GLTFLoader));
  }

  /**
   * Load glTF/GLB when Three+GLTFLoader are vendored; else resolve null (caller uses procedural).
   * Does not fetch CDN — CSP script-src 'self' only.
   */
  function loadGltf(url, opts) {
    opts = opts || {};
    return new Promise(function (resolve, reject) {
      if (!hasThree() || !hasGLTFLoader()) {
        resolve({ ok: false, reason: 'three_not_vendored', url: url });
        return;
      }
      var Loader = g.THREE.GLTFLoader || g.GLTFLoader;
      var loader = new Loader();
      loader.load(
        url,
        function (gltf) { resolve({ ok: true, gltf: gltf, url: url }); },
        opts.onProgress || null,
        function (err) { reject(err); }
      );
    });
  }

  /** Unreal Pixel Streaming embed helper — iframe only when signaling URL provided. */
  function pixelStreamEmbed(host, signalingUrl, opts) {
    opts = opts || {};
    if (!host) return null;
    host.innerHTML = '';
    if (!signalingUrl) {
      host.innerHTML = '<div class="il-scene-kit__ps-stub" role="status">' +
        '<p class="il-scene-kit__ps-kicker">Unreal Pixel Streaming</p>' +
        '<p>Scaffold ready. Set <code>data-ps-signaling</code> or pass signaling URL when UE5 streamer is up. See IMMERSIVE-3D.md.</p>' +
        '</div>';
      return { mode: 'stub' };
    }
    var iframe = document.createElement('iframe');
    iframe.src = signalingUrl;
    iframe.title = opts.title || 'Unreal Pixel Streaming';
    iframe.allow = 'autoplay; fullscreen; microphone; camera';
    iframe.setAttribute('allowfullscreen', 'true');
    iframe.className = 'il-scene-kit__ps-frame';
    host.appendChild(iframe);
    return { mode: 'iframe', iframe: iframe };
  }

  /** Shared voice-amp bus — Muse TTS + immersive lecture stages. */
  function onSpeakAmp(fn) {
    var h = function (ev) { fn(ev && ev.detail ? ev.detail : { amp: 0 }); };
    var b = function () { fn({ amp: 1, beat: 1, boundary: 1 }); };
    g.addEventListener('il-muse-speak-amp', h);
    g.addEventListener('il-muse-speak-boundary', b);
    return function off() {
      g.removeEventListener('il-muse-speak-amp', h);
      g.removeEventListener('il-muse-speak-boundary', b);
    };
  }

  function emitSceneEvent(name, detail) {
    try { g.dispatchEvent(new CustomEvent(name, { detail: detail || {} })); } catch (e) {}
  }

  g.ILSceneKit = {
    CYAN: CYAN, GOLD: GOLD, VOID: VOID,
    HEX: { cyan: '#5EEAD4', gold: '#D4A853', void: '#070B16' },
    prefersReducedMotion: prefersReducedMotion,
    isMobile: isMobile,
    dprCap: dprCap,
    compileShader: compileShader,
    linkProgram: linkProgram,
    resizeCanvas: resizeCanvas,
    mat4: mat4,
    mat4Identity: mat4Identity,
    mat4Perspective: mat4Perspective,
    mat4LookAt: mat4LookAt,
    mat4Multiply: mat4Multiply,
    mat4FromRTS: mat4FromRTS,
    hasThree: hasThree,
    hasGLTFLoader: hasGLTFLoader,
    loadGltf: loadGltf,
    pixelStreamEmbed: pixelStreamEmbed,
    onSpeakAmp: onSpeakAmp,
    emitSceneEvent: emitSceneEvent,
    VERSION: '1.0.0'
  };

  /* Muse 3D may re-export kit when both present */
  if (g.ILMuse3D) g.ILMuse3D.kit = g.ILSceneKit;
})(typeof window !== 'undefined' ? window : this);
