/**
 * IL Curriculum Sync — Notion-shaped SoT → immersive stamps.
 * Reads /curriculum-os/mirror.json (file SoT). Optional window.IL_NOTION_CURRICULUM override.
 * Stamps [data-il-immersive] with 3d-first hooks; never uses Notion embeds as runtime.
 * Coordinates with il-immersive-3d.js + il-immersive.js + il-muse-3d.js (does not clobber Muse).
 */
(function (g) {
  'use strict';

  var MIRROR_URL = '/curriculum-os/mirror.json';
  var VERSION = '1.1.0';

  function parseImmersive(el) {
    var raw = el.getAttribute('data-immersive');
    if (!raw) return null;
    try { return JSON.parse(raw); } catch (e) { return null; }
  }

  function assetToScene(asset) {
    if (!asset || typeof asset !== 'string') return 'k8s';
    if (asset.indexOf('hermetic') >= 0) return 'hermetic';
    if (asset.indexOf('rack') >= 0) return 'rack';
    if (asset.indexOf('k8s') >= 0 || asset.indexOf('cluster') >= 0) return 'k8s';
    return 'k8s';
  }

  function preferWebGPU(imm) {
    if (!imm || imm.webgpu === false) return false;
    if (imm.engine === 'webgpu') return true;
    try {
      var q = g.location && g.location.search;
      if (q && /[?&]webgpu=1\b/.test(q)) return true;
      if (g.localStorage && g.localStorage.getItem('il-webgpu') === '1') return true;
    } catch (e) {}
    return !!imm.webgpu;
  }

  function hasWebGPU() {
    return !!(g.navigator && g.navigator.gpu);
  }

  function stampEl(el, imm, meta) {
    if (!el || !imm) return;
    imm = Object.assign({ mode: '3d-first', captions: true, fallback: 'reduced-motion' }, imm);
    imm.mode = '3d-first';

    var useGpu = preferWebGPU(imm) && hasWebGPU();
    var engine = useGpu ? 'webgpu' : (imm.engine || 'three');
    if (engine === 'webgpu' && !hasWebGPU()) engine = 'three';

    el.setAttribute('data-immersive', JSON.stringify(imm));
    el.setAttribute('data-il-immersive', el.getAttribute('data-il-immersive') || '');
    if (!el.getAttribute('data-il-scene')) {
      el.setAttribute('data-il-scene', assetToScene(imm.asset));
    }
    el.setAttribute('data-il-engine', engine);
    if (useGpu) el.setAttribute('data-il-webgpu', '1');
    else el.removeAttribute('data-il-webgpu');

    if (meta) {
      if (meta.gltf) el.setAttribute('data-gltf', meta.gltf);
      if (meta.kind) el.setAttribute('data-kind', meta.kind);
      if (meta.title) el.setAttribute('data-title', meta.title);
      if (meta.slug) el.setAttribute('data-il-curriculum-id', meta.slug);
    }

    el.setAttribute('data-il-curriculum-synced', VERSION);
  }

  function surfaceFromPath(path) {
    if (!path) return null;
    if (path.indexOf('/labs') === 0) return 'labs';
    if (path.indexOf('/prep') === 0) return 'prep';
    if (path.indexOf('/paths') === 0) return 'paths';
    if (path.indexOf('/learn') === 0) return 'learn';
    if (path.indexOf('/immersive') === 0) return 'learn';
    return null;
  }

  function findDefaultForSurface(mirror, surface) {
    var def = (mirror.defaults && mirror.defaults.immersive) || {
      mode: '3d-first', engine: 'three', asset: 'procedural:k8s', webgpu: true
    };
    var surf = mirror.surfaces && mirror.surfaces[surface];
    if (surf && surf.defaultScene) {
      def = Object.assign({}, def, { asset: 'procedural:' + surf.defaultScene });
    }
    var path = (g.location && g.location.pathname) || '';
    var tracks = mirror.tracks || [];
    for (var i = 0; i < tracks.length; i++) {
      var t = tracks[i];
      if (t.pathUrl && path.indexOf(t.pathUrl.replace(/\/$/, '')) === 0 && t.immersive) {
        return { imm: t.immersive, meta: { slug: t.slug, title: t.name, kind: surf && surf.kind } };
      }
    }
    /* lectures / labs / certs by surfaceUrl */
    var pools = [].concat(mirror.lectures || [], mirror.labs || [], mirror.certs || []);
    for (var j = 0; j < pools.length; j++) {
      var row = pools[j];
      if (row.surfaceUrl && path.indexOf(row.surfaceUrl.replace(/\/$/, '')) === 0 && row.immersive) {
        return {
          imm: row.immersive,
          meta: {
            slug: row.slug,
            title: row.name,
            kind: row.kind || (surf && surf.kind) || 'lecture',
            gltf: row.gltf || null
          }
        };
      }
    }
    return { imm: def, meta: { kind: surf && surf.kind } };
  }

  function stampAll(mirror) {
    var path = (g.location && g.location.pathname) || '';
    var surface = surfaceFromPath(path);
    var picked = findDefaultForSurface(mirror, surface || 'learn');

    var nodes = g.document.querySelectorAll('[data-il-immersive]');
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      /* Do not touch Muse hosts */
      if (el.closest && (el.closest('[data-muse-3d-slot]') || el.closest('.il-muse-3d-slot'))) continue;
      var existing = parseImmersive(el);
      var imm = existing ? Object.assign({}, picked.imm, existing, { mode: '3d-first' }) : picked.imm;
      var meta = Object.assign({}, picked.meta);
      if (!meta.gltf) {
        var gAttr = el.getAttribute('data-gltf');
        if (gAttr) meta.gltf = gAttr;
      }
      if (!meta.kind) meta.kind = el.getAttribute('data-kind') || undefined;
      stampEl(el, imm, meta);
    }

    /* Ensure surface markers for future queries */
    if (surface) {
      var main = g.document.querySelector('main') || g.document.body;
      if (main && !main.getAttribute('data-il-curriculum-surface')) {
        main.setAttribute('data-il-curriculum-surface', surface);
      }
    }

    try {
      g.document.dispatchEvent(new CustomEvent('il:curriculum-synced', {
        detail: { version: VERSION, surface: surface, count: nodes.length }
      }));
    } catch (e) {}
  }

  function loadMirror() {
    if (g.IL_NOTION_CURRICULUM) {
      return Promise.resolve(g.IL_NOTION_CURRICULUM);
    }
    return fetch(MIRROR_URL, { credentials: 'same-origin' }).then(function (r) {
      if (!r.ok) throw new Error('mirror ' + r.status);
      return r.json();
    });
  }

  function boot() {
    loadMirror().then(function (mirror) {
      g.ILCurriculum = mirror;
      stampAll(mirror);
      /* Re-stamp after immersive players boot if they scaffold late */
      if (g.ILImmersive3D && typeof g.ILImmersive3D.mountAll === 'function') {
        try { g.ILImmersive3D.mountAll(); } catch (e) {}
      }
    }).catch(function (err) {
      try { console.warn('[il-curriculum-sync]', err && err.message ? err.message : err); } catch (e) {}
      /* Hard defaults without mirror */
      stampAll({
        defaults: { immersive: { mode: '3d-first', engine: 'three', asset: 'procedural:k8s', webgpu: true } },
        surfaces: {
          learn: { defaultScene: 'k8s', kind: 'lecture' },
          labs: { defaultScene: 'k8s', kind: 'cert' },
          prep: { defaultScene: 'rack', kind: 'lecture' },
          paths: { defaultScene: 'k8s', kind: 'lecture' }
        },
        tracks: [], lectures: [], labs: [], certs: []
      });
    });
  }

  if (g.document && g.document.readyState === 'loading') {
    g.document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  g.ILCurriculumSync = {
    version: VERSION,
    boot: boot,
    stampAll: stampAll,
    preferWebGPU: preferWebGPU,
    hasWebGPU: hasWebGPU,
    mirrorUrl: MIRROR_URL
  };
})(typeof window !== 'undefined' ? window : this);
