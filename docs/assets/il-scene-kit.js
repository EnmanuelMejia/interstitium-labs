/**
 * IL Scene Kit — shared WebGL / curriculum 3D utilities (CSP-safe, no CDN).
 * Used by Noah 3D familiar + Immersive Player (lectures / cert labs / sims).
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


  /** WebGPU capability + preference (flag path). Full WGSL renderer lands later; callers fall back to WebGL. */
  function hasWebGPU() {
    return !!(g.navigator && g.navigator.gpu);
  }
  function preferWebGPU(opts) {
    opts = opts || {};
    if (opts.forceWebGL) return false;
    if (opts.forceWebGPU) return hasWebGPU();
    try {
      if (g.location && /[?&]webgpu=1\b/.test(g.location.search || '')) return hasWebGPU();
      if (g.localStorage && g.localStorage.getItem('il-webgpu') === '1') return hasWebGPU();
    } catch (e) {}
    if (opts.webgpu === false) return false;
    if (opts.engine === 'webgpu' || opts.webgpu === true) return hasWebGPU();
    return false;
  }
  /**
   * Acquire best canvas context: WebGPU adapter probe when preferred, else WebGL.
   * Returns { api:'webgpu'|'webgl'|'none', gl?, gpu?, adapter?, canvas, label }
   */
  function acquireGraphics(canvas, opts) {
    opts = opts || {};
    var out = { api: 'none', canvas: canvas, label: 'none' };
    if (!canvas) return out;
    if (preferWebGPU(opts) && hasWebGPU()) {
      out.api = 'webgpu';
      out.gpu = g.navigator.gpu;
      out.label = 'WebGPU';
      /* Adapter request is async — callers may upgrade; procedural path still uses WebGL today. */
      try {
        g.navigator.gpu.requestAdapter().then(function (a) {
          out.adapter = a || null;
          emitSceneEvent('il-webgpu-adapter', { ok: !!a });
        }).catch(function () {
          emitSceneEvent('il-webgpu-adapter', { ok: false });
        });
      } catch (e) {}
      /* Honest dual-path: still provide WebGL for procedural mesh until WGSL port */
    }
    var gl = canvas.getContext('webgl', opts.webglAttrs || { antialias: true, alpha: !!opts.alpha, powerPreference: 'high-performance' })
      || canvas.getContext('experimental-webgl');
    if (gl) {
      out.gl = gl;
      if (out.api !== 'webgpu') { out.api = 'webgl'; out.label = 'WebGL'; }
      else out.label = 'WebGPU·WebGL-fallback';
      return out;
    }
    if (out.api === 'webgpu') return out;
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
   * Native GLB (glTF 2.0 binary) parser — CSP-safe, no Three CDN.
   * Returns { ok, meshes:[{positions,normals,indices,material}], materials, url?, reason? }.
   */
  function parseGlb(arrayBuffer) {
    try {
      if (!arrayBuffer || arrayBuffer.byteLength < 20) {
        return { ok: false, reason: 'too_short', meshes: [] };
      }
      var u8 = new Uint8Array(arrayBuffer);
      var dv = new DataView(arrayBuffer);
      if (u8[0] !== 0x67 || u8[1] !== 0x6c || u8[2] !== 0x54 || u8[3] !== 0x46) {
        return { ok: false, reason: 'bad_magic', meshes: [] };
      }
      var version = dv.getUint32(4, true);
      var total = dv.getUint32(8, true);
      if (version !== 2) return { ok: false, reason: 'unsupported_version', meshes: [] };
      var offset = 12;
      var json = null;
      var bin = null;
      while (offset + 8 <= u8.byteLength && offset < total) {
        var chunkLen = dv.getUint32(offset, true);
        var chunkType = String.fromCharCode(u8[offset + 4], u8[offset + 5], u8[offset + 6], u8[offset + 7]);
        offset += 8;
        if (chunkType.indexOf('JSON') === 0) {
          var js = '';
          for (var i = 0; i < chunkLen; i++) js += String.fromCharCode(u8[offset + i]);
          json = JSON.parse(js.trim());
        } else if (chunkType.indexOf('BIN') === 0) {
          bin = arrayBuffer.slice(offset, offset + chunkLen);
        }
        offset += chunkLen;
      }
      if (!json || !bin) return { ok: false, reason: 'missing_chunks', meshes: [] };
      var accessors = json.accessors || [];
      var views = json.bufferViews || [];
      var mats = json.materials || [];

      function readAccessor(ai) {
        var acc = accessors[ai];
        if (!acc) return null;
        var view = views[acc.bufferView];
        if (!view) return null;
        var byteOffset = (view.byteOffset || 0) + (acc.byteOffset || 0);
        var count = acc.count;
        var comp = acc.componentType;
        var type = acc.type;
        var comps = type === 'SCALAR' ? 1 : type === 'VEC2' ? 2 : type === 'VEC3' ? 3 : type === 'VEC4' ? 4 : 1;
        var bdv = new DataView(bin);
        var out;
        var j, k, o;
        if (comp === 5126) {
          out = new Float32Array(count * comps);
          for (j = 0; j < count * comps; j++) out[j] = bdv.getFloat32(byteOffset + j * 4, true);
        } else if (comp === 5123) {
          out = new Uint16Array(count * comps);
          for (j = 0; j < count * comps; j++) out[j] = bdv.getUint16(byteOffset + j * 2, true);
        } else if (comp === 5125) {
          out = new Uint32Array(count * comps);
          for (j = 0; j < count * comps; j++) out[j] = bdv.getUint32(byteOffset + j * 4, true);
        } else if (comp === 5121) {
          out = new Uint8Array(count * comps);
          for (j = 0; j < count * comps; j++) out[j] = bdv.getUint8(byteOffset + j);
        } else {
          return null;
        }
        return { data: out, count: count, type: type, componentType: comp, min: acc.min, max: acc.max };
      }

      function matColor(mi) {
        var m = mats[mi];
        if (!m || !m.pbrMetallicRoughness || !m.pbrMetallicRoughness.baseColorFactor) {
          return { color: [0.369, 0.918, 0.831], emissive: [0.05, 0.18, 0.15], name: (m && m.name) || 'default' };
        }
        var bc = m.pbrMetallicRoughness.baseColorFactor;
        var em = m.emissiveFactor || [0, 0, 0];
        return {
          color: [bc[0], bc[1], bc[2]],
          emissive: [em[0] || 0, em[1] || 0, em[2] || 0],
          name: m.name || 'mat'
        };
      }

      var meshes = [];
      var meshDefs = json.meshes || [];
      for (var mi = 0; mi < meshDefs.length; mi++) {
        var prims = meshDefs[mi].primitives || [];
        for (var pi = 0; pi < prims.length; pi++) {
          var prim = prims[pi];
          if (prim.mode != null && prim.mode !== 4) continue; /* TRIANGLES only */
          var posA = readAccessor(prim.attributes && prim.attributes.POSITION);
          var nrmA = readAccessor(prim.attributes && prim.attributes.NORMAL);
          var idxA = prim.indices != null ? readAccessor(prim.indices) : null;
          if (!posA) continue;
          var positions = posA.data instanceof Float32Array ? posA.data : new Float32Array(posA.data);
          var normals;
          if (nrmA && nrmA.data) {
            normals = nrmA.data instanceof Float32Array ? nrmA.data : new Float32Array(nrmA.data);
          } else {
            normals = new Float32Array(positions.length);
            for (k = 0; k < normals.length; k += 3) normals[k + 1] = 1;
          }
          var indices;
          if (idxA && idxA.data) {
            indices = idxA.data instanceof Uint16Array || idxA.data instanceof Uint32Array
              ? idxA.data
              : new Uint16Array(idxA.data);
          } else {
            indices = new Uint16Array(positions.length / 3);
            for (k = 0; k < indices.length; k++) indices[k] = k;
          }
          /* WebGL1 drawElements UNSIGNED_SHORT path — split if needed later; kit assets stay <65k */
          if (!(indices instanceof Uint16Array) && maxOf(indices) > 65535) {
            /* keep Uint32 — caller may use OES_element_index_uint */
          } else if (!(indices instanceof Uint16Array)) {
            indices = new Uint16Array(indices);
          }
          var mc = matColor(prim.material != null ? prim.material : 0);
          meshes.push({
            name: (meshDefs[mi].name || 'mesh') + (prims.length > 1 ? ':' + pi : ''),
            positions: positions,
            normals: normals,
            indices: indices,
            material: mc
          });
        }
      }
      return {
        ok: meshes.length > 0,
        reason: meshes.length ? undefined : 'no_triangles',
        meshes: meshes,
        materials: mats,
        asset: json.asset || {}
      };
    } catch (err) {
      return { ok: false, reason: 'parse_error', error: String(err && err.message || err), meshes: [] };
    }
  }

  function maxOf(arr) {
    var m = 0;
    for (var i = 0; i < arr.length; i++) if (arr[i] > m) m = arr[i];
    return m;
  }

  /**
   * Fetch + parse GLB via native parser (preferred) or vendored Three GLTFLoader.
   * Does not fetch CDN — CSP script-src 'self' only.
   */
  function loadGltf(url, opts) {
    opts = opts || {};
    return new Promise(function (resolve, reject) {
      if (!url) {
        resolve({ ok: false, reason: 'no_url', url: url });
        return;
      }
      /* Prefer native GLB path — no Three required */
      if (/\.glb($|\?)/i.test(url) || opts.forceNative) {
        g.fetch(url).then(function (res) {
          if (!res || !res.ok) {
            resolve({ ok: false, reason: 'http_' + (res && res.status), url: url });
            return null;
          }
          return res.arrayBuffer();
        }).then(function (buf) {
          if (!buf) return;
          var parsed = parseGlb(buf);
          parsed.url = url;
          resolve(parsed);
        }).catch(function (err) {
          resolve({ ok: false, reason: 'fetch_error', error: String(err && err.message || err), url: url, meshes: [] });
        });
        return;
      }
      if (!hasThree() || !hasGLTFLoader()) {
        resolve({ ok: false, reason: 'three_not_vendored', url: url, meshes: [] });
        return;
      }
      var Loader = g.THREE.GLTFLoader || g.GLTFLoader;
      var loader = new Loader();
      loader.load(
        url,
        function (gltf) { resolve({ ok: true, gltf: gltf, url: url, meshes: [] }); },
        opts.onProgress || null,
        function (err) { reject(err); }
      );
    });
  }

  /**
   * Unreal Pixel Streaming embed — honest stub or iframe/player mount.
   * Never fakes a live stream. Prefer dedicated /immersive/pixel-stream/ client page.
   */
  function pixelStreamEmbed(host, signalingUrl, opts) {
    opts = opts || {};
    if (!host) return null;
    host.innerHTML = '';
    host.classList.add('il-scene-kit__ps-host');
    if (!signalingUrl) {
      host.innerHTML = '<div class="il-scene-kit__ps-stub" role="status">' +
        '<p class="il-scene-kit__ps-kicker">Unreal Pixel Streaming</p>' +
        '<p>Connect a Unreal Pixel Streaming host — set signaling when UE5 streamer is up on lab GPU host.</p>' +
        '<p class="il-scene-kit__ps-hint">Pass <code>?signaling=</code>, <code>data-ps-signaling</code>, or open ' +
        '<a class="il-scene-kit__ps-link" href="/immersive/pixel-stream/">/immersive/pixel-stream/</a>. ' +
        'See <a class="il-scene-kit__ps-link" href="/ops/PIXEL-STREAMING-DEV.md">PS runbook</a> · <a class="il-scene-kit__ps-link" href="/ops/UNREAL-AND-BLENDER-PIPELINE.md">pipeline</a>.</p>' +
        '</div>';
      return { mode: 'stub', signaling: null };
    }
    /* Prefer navigating the dedicated client when mountMode=page */
    if (opts.mountMode === 'page') {
      var frame = document.createElement('iframe');
      var q = '/immersive/pixel-stream/?signaling=' + encodeURIComponent(signalingUrl);
      frame.src = q;
      frame.title = opts.title || 'Unreal Pixel Streaming';
      frame.allow = 'autoplay; fullscreen; microphone; camera';
      frame.setAttribute('allowfullscreen', 'true');
      frame.className = 'il-scene-kit__ps-frame';
      host.appendChild(frame);
      return { mode: 'client-page', iframe: frame, signaling: signalingUrl };
    }
    var iframe = document.createElement('iframe');
    iframe.src = signalingUrl;
    iframe.title = opts.title || 'Unreal Pixel Streaming';
    iframe.allow = 'autoplay; fullscreen; microphone; camera';
    iframe.setAttribute('allowfullscreen', 'true');
    iframe.className = 'il-scene-kit__ps-frame';
    host.appendChild(iframe);
    return { mode: 'iframe', iframe: iframe, signaling: signalingUrl };
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
    hasWebGPU: hasWebGPU,
    preferWebGPU: preferWebGPU,
    acquireGraphics: acquireGraphics,
    loadGltf: loadGltf,
    parseGlb: parseGlb,
    pixelStreamEmbed: pixelStreamEmbed,
    onSpeakAmp: onSpeakAmp,
    emitSceneEvent: emitSceneEvent,
    VERSION: '1.3.0'
  };

  /* Muse 3D may re-export kit when both present */
  if (g.ILMuse3D) g.ILMuse3D.kit = g.ILSceneKit;
})(typeof window !== 'undefined' ? window : this);
