/* Interstitium Labs — Mind Maps (il-mindmap.js).
 * Distilled mind-map mechanics (see notes-integration/DISTILL.md):
 *   - auto-generated map for every CBT from its content.json structure
 *     (course → domains → lessons / labs / scenarios)
 *   - user-created custom maps, stored as notes of kind 'map' in the
 *     ILNotes vault (tree JSON in note.map), fully editable
 *   - rendering by NoahViz.mindmap (tidy-tree canvas engine)
 *   - export to PNG
 * Vanilla JS, zero dependencies, ES5-compatible. Exposes window.ILMindmap. */
(function (g) {
  'use strict';

  var VIZ_URL = 'https://interstitiumlabs.dev/assets/noah-viz.js';

  function ensureViz(cb) {
    if (g.NoahViz && g.NoahViz.mindmap) { cb(true); return; }
    if (typeof document === 'undefined') { cb(false); return; }
    var s = document.createElement('script');
    s.src = VIZ_URL; s.defer = true;
    s.onload = function () { cb(!!(g.NoahViz && g.NoahViz.mindmap)); };
    s.onerror = function () { cb(false); };
    document.head.appendChild(s);
  }

  function nid(prefix) {
    return prefix + '_' + Math.random().toString(36).slice(2, 9);
  }

  /* ---------------- tree builders ---------------- */

  /* content.json shape: { title, domains:[{id,name}], lessons:[{title,domain_id}],
     labs:[...], simulations/scenarios under domains[].scenarios */
  function buildCbtTree(content) {
    content = content || {};
    var lessonsByDomain = {};
    (content.lessons || []).forEach(function (l) {
      var d = l.domain_id || 'general';
      (lessonsByDomain[d] = lessonsByDomain[d] || []).push(l);
    });
    var labsCount = (content.labs || []).length;
    var root = { id: 'root', label: content.title || 'Bootcamp', children: [] };
    (content.domains || []).forEach(function (dom, di) {
      var dNode = { id: 'dom_' + (dom.id || di), label: dom.name || dom.id || ('Domain ' + (di + 1)), children: [] };
      (lessonsByDomain[dom.id] || []).forEach(function (l, li) {
        dNode.children.push({ id: 'les_' + di + '_' + li, label: l.title, children: [] });
      });
      var scen = (dom.scenarios || []).length;
      if (scen) dNode.children.push({ id: 'scen_' + di, label: 'Scenarios × ' + scen, children: [] });
      root.children.push(dNode);
    });
    var loose = lessonsByDomain['general'] || [];
    if (loose.length && !(content.domains || []).length) {
      loose.forEach(function (l, li) { root.children.push({ id: 'les_g_' + li, label: l.title, children: [] }); });
    }
    if (labsCount) root.children.push({ id: 'labs', label: 'Hands-on Labs × ' + labsCount, children: [] });
    if ((content.simulations || []).length) {
      root.children.push({ id: 'sims', label: 'Simulations × ' + content.simulations.length, children: [] });
    }
    return root;
  }

  function fetchCbtTree(slug, cb) {
    var url = 'https://interstitiumlabs.dev/bootcamps/' + encodeURIComponent(slug) + '/content.json';
    fetch(url).then(function (r) { return r.json(); }).then(function (content) {
      cb(buildCbtTree(content), content);
    }).catch(function () { cb(null, null); });
  }

  function blankTree(label) {
    return { id: 'root', label: label || 'My Mind Map', children: [
      { id: nid('b'), label: 'Main idea 1', children: [ { id: nid('l'), label: 'Detail', children: [] } ] },
      { id: nid('b'), label: 'Main idea 2', children: [] },
      { id: nid('b'), label: 'Main idea 3', children: [] }
    ] };
  }

  /* ---------------- tree editing (pure) ---------------- */

  function findNode(tree, id) {
    if (!tree) return null;
    if (tree.id === id) return tree;
    var kids = tree.children || [], i, hit;
    for (i = 0; i < kids.length; i++) { hit = findNode(kids[i], id); if (hit) return hit; }
    return null;
  }

  function findParent(tree, id) {
    if (!tree) return null;
    var kids = tree.children || [], i;
    for (i = 0; i < kids.length; i++) {
      if (kids[i].id === id) return tree;
      var hit = findParent(kids[i], id);
      if (hit) return hit;
    }
    return null;
  }

  function clone(tree) { return JSON.parse(JSON.stringify(tree)); }

  function addChild(tree, parentId, label) {
    var t = clone(tree), p = findNode(t, parentId);
    if (!p) return tree;
    p.children = p.children || [];
    p.children.push({ id: nid('n'), label: label || 'New branch', children: [] });
    p.collapsed = false;
    return t;
  }

  function renameNode(tree, id, label) {
    var t = clone(tree), n = findNode(t, id);
    if (n) n.label = String(label || n.label).slice(0, 90);
    return t;
  }

  function deleteNode(tree, id) {
    if (tree.id === id) return tree; /* never delete the root */
    var t = clone(tree), p = findParent(t, id);
    if (p) p.children = p.children.filter(function (c) { return c.id !== id; });
    return t;
  }

  function countNodes(tree) {
    if (!tree) return 0;
    return 1 + (tree.children || []).reduce(function (s, c) { return s + countNodes(c); }, 0);
  }

  /* ---------------- custom maps in the vault ---------------- */

  function listMaps() {
    if (!g.ILNotes) return [];
    return g.ILNotes.all().filter(function (n) { return n.kind === 'map'; });
  }

  function createMap(title) {
    if (!g.ILNotes) return null;
    var tree = blankTree(title);
    return g.ILNotes.create({ title: title || 'My Mind Map', body: '# ' + (title || 'My Mind Map') + '\n\nCustom mind map. Edit the tree in My Notes → Mind Maps.\n', kind: 'map', map: tree, tags: ['mindmap'] });
  }

  function saveMap(noteId, tree) {
    if (!g.ILNotes) return null;
    return g.ILNotes.update(noteId, { map: tree, title: tree.label });
  }

  /* ---------------- rendering ---------------- */

  var liveViz = null;

  function renderInto(canvas, tree, opts) {
    opts = opts || {};
    ensureViz(function (ok) {
      if (!ok) { if (opts.onError) opts.onError(); return; }
      if (liveViz && liveViz.destroy) { try { liveViz.destroy(); } catch (e) {} }
      liveViz = g.NoahViz.mindmap(canvas, { title: opts.title || '', root: tree }, { onNode: opts.onNode });
      if (opts.onReady) opts.onReady(liveViz);
    });
  }

  function exportPNG(canvas, name) {
    try {
      var a = document.createElement('a');
      a.href = canvas.toDataURL('image/png');
      a.download = (name || 'mind-map').replace(/[^\w\- ]+/g, '').trim().replace(/\s+/g, '-') + '.png';
      document.body.appendChild(a); a.click(); a.remove();
    } catch (e) {}
  }

  g.ILMindmap = {
    buildCbtTree: buildCbtTree, fetchCbtTree: fetchCbtTree, blankTree: blankTree,
    findNode: findNode, addChild: addChild, renameNode: renameNode, deleteNode: deleteNode,
    countNodes: countNodes, listMaps: listMaps, createMap: createMap, saveMap: saveMap,
    renderInto: renderInto, exportPNG: exportPNG, ensureViz: ensureViz, version: 1
  };
})(typeof window !== 'undefined' ? window : this);
