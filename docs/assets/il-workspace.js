/* Interstitium Labs — My Notes workspace (il-workspace.js).
 * Notion-style personal dashboard over the ILNotes vault:
 *   Dashboard (stats, templates, my-bootcamps database, recent notes,
 *   bookmarks) · Notes (search + list) · Knowledge Graph (NoahViz.graph)
 *   · Mind Maps (auto CBT maps + editable custom maps).
 * All data is local-first (localStorage); nothing is invented — CBT status
 * is read from the shell's own progress stores on this device.
 * Vanilla JS, zero dependencies, ES5-compatible. */
(function (g) {
  'use strict';

  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function ready(fn) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  var LEVEL_SCORE = { struggling: 0.2, developing: 0.45, proficient: 0.7, mastered: 0.95 };

  /* ---------------- CBT activity on this device ---------------- */

  function scanCbts() {
    var bySlug = {};
    try {
      for (var i = 0; i < g.localStorage.length; i++) {
        var key = g.localStorage.key(i);
        var m = /^ilb-bootcamp-(.+?)(?:-skill|-lectures)?-v1$/.exec(key || '');
        if (!m) continue;
        var slug = m[1];
        var row = bySlug[slug] || (bySlug[slug] = { slug: slug, title: slug, level: null, lessons: 0, scenarios: 0 });
        var val = null;
        try { val = JSON.parse(g.localStorage.getItem(key)); } catch (e) {}
        if (!val) continue;
        if (/-skill-v1$/.test(key)) {
          row.level = val.overall || null;
          row.domains = val.domains ? Object.keys(val.domains).length : 0;
        } else if (/-lectures-v1$/.test(key)) {
          var done = val.doneLect || val;
          row.lessons = done && typeof done === 'object' ? Object.keys(done).filter(function (k) { return done[k]; }).length : 0;
        } else {
          row.scenarios = typeof val === 'object' ? Object.keys(val).length : 0;
        }
      }
    } catch (e) {}
    return bySlug;
  }

  var cbtRows = [], cbtSort = { key: 'title', dir: 1 };

  function loadCatalogTitles(done) {
    fetch('/assets/search-index.json').then(function (r) { return r.json(); }).then(function (data) {
      var items = (data && data.items) || [];
      var titles = {};
      items.forEach(function (it) {
        var m = /^\/bootcamps\/([^/]+)\/?$/.exec(it.u || '');
        if (m) titles[m[1]] = it.t;
      });
      done(titles);
    }).catch(function () { done({}); });
  }

  function renderCbtTable() {
    var tb = $('ilw-cbt-table').querySelector('tbody');
    var rows = cbtRows.slice().sort(function (a, b) {
      var k = cbtSort.key, va = a[k], vb = b[k];
      if (typeof va === 'number' && typeof vb === 'number') return (va - vb) * cbtSort.dir;
      return String(va == null ? '' : va).localeCompare(String(vb == null ? '' : vb)) * cbtSort.dir;
    });
    tb.innerHTML = rows.map(function (r) {
      return '<tr><td>' + esc(r.title) + '</td>' +
        '<td>' + (r.level ? '<span class="ilw-level ' + esc(r.level) + '">' + esc(r.level) + '</span>' : '<span class="ilw-dim">not started</span>') + '</td>' +
        '<td>' + r.lessons + '</td><td>' + r.scenarios + '</td>' +
        '<td><a class="ilw-open" href="/bootcamps/' + encodeURIComponent(r.slug) + '/">Open →</a></td></tr>';
    }).join('');
    $('ilw-cbt-empty').hidden = rows.length > 0;
  }

  /* ---------------- dashboard ---------------- */

  function renderDashboard() {
    var notes = g.ILNotes ? g.ILNotes.all() : [];
    var links = 0;
    notes.forEach(function (n) { links += g.ILNotes.parseLinks(n.body).length; });
    var maps = notes.filter(function (n) { return n.kind === 'map'; }).length;
    var started = cbtRows.filter(function (r) { return r.level || r.lessons || r.scenarios; }).length;
    $('ilw-stats').innerHTML =
      stat(notes.length, 'Notes') + stat(links, 'Wikilinks') +
      stat(maps, 'Mind maps') + stat(started, 'Bootcamps in progress');

    $('ilw-templates').innerHTML = g.ILNotes.templates.map(function (t) {
      return '<button type="button" class="ilw-template" data-ilw-template="' + t.id + '">' +
        '<strong>' + esc(t.name) + '</strong><span>' + esc(t.desc) + '</span></button>';
    }).join('');

    var recent = notes.slice().sort(function (a, b) { return b.updatedAt - a.updatedAt; }).slice(0, 6);
    $('ilw-recent').innerHTML = recent.map(noteItem).join('') || '<li class="ilw-dim">No notes yet.</li>';

    var bms = g.ILNotes.bookmarks();
    $('ilw-bookmarks').innerHTML = bms.map(function (b) {
      /* esc() alone cannot neutralize a javascript: URL in an href —
         only http(s) and same-origin relative bookmark targets render. */
      var safeUrl = /^(https?:\/\/|\/)/i.test(String(b.url || '')) ? b.url : '#';
      return '<li><a href="' + esc(safeUrl) + '">' + esc(b.label) + '</a>' +
        ' <button type="button" class="ilw-x" data-ilw-unbookmark="' + esc(b.url) + '" aria-label="Remove bookmark">✕</button></li>';
    }).join('') || '<li class="ilw-dim">No bookmarks yet.</li>';

    renderCbtTable();
  }

  function stat(v, label) {
    return '<div class="ilw-stat"><strong>' + v + '</strong><span>' + label + '</span></div>';
  }

  function noteItem(n) {
    var tags = (n.tags || []).map(function (t) { return '<span class="ilw-tag">' + esc(t) + '</span>'; }).join(' ');
    return '<li><button type="button" class="ilw-noteitem" data-ilw-open="' + esc(n.id) + '">' +
      '<span class="ilw-notetitle">' + esc(n.title) + (n.kind === 'map' ? ' 🧠' : '') + '</span>' +
      '<span class="ilw-notemeta">' + new Date(n.updatedAt).toLocaleDateString() + ' ' + tags + '</span>' +
      '</button></li>';
  }

  /* ---------------- notes view ---------------- */

  function renderNotesList() {
    var q = $('ilw-search').value || '';
    var hits = g.ILNotes.search(q);
    $('ilw-notes-list').innerHTML = hits.map(function (h) {
      return '<li><button type="button" class="ilw-noteitem" data-ilw-open="' + esc(h.note.id) + '">' +
        '<span class="ilw-notetitle">' + esc(h.note.title) + (h.note.kind === 'map' ? ' 🧠' : '') + '</span>' +
        '<span class="ilw-notemeta">' + esc(h.excerpt) + '</span></button></li>';
    }).join('');
    $('ilw-notes-empty').hidden = hits.length > 0;
  }

  /* ---------------- graph view ---------------- */

  var graphViz = null;

  function masteryFor(note) {
    if (note.source && note.source.slug) {
      var row = null;
      cbtRows.forEach(function (r) { if (r.slug === note.source.slug) row = r; });
      if (row && row.level && LEVEL_SCORE[row.level] != null) return LEVEL_SCORE[row.level];
    }
    return null;
  }

  function buildGraphSpec() {
    var notes = g.ILNotes.all();
    var nodes = [], edges = [], seen = {};
    function addNode(id, label, mastery) {
      if (seen[id]) return;
      seen[id] = 1;
      nodes.push({ id: id, label: label, mastery: mastery });
    }
    notes.forEach(function (n) { addNode('note:' + n.id, n.title, masteryFor(n)); });
    notes.forEach(function (n) {
      g.ILNotes.parseLinks(n.body).forEach(function (t) {
        var hit = g.ILNotes.findByTitle(t);
        if (hit) {
          if (hit.id !== n.id) edges.push({ from: 'note:' + n.id, to: 'note:' + hit.id });
        } else {
          addNode('ghost:' + t, t, null);
          edges.push({ from: 'note:' + n.id, to: 'ghost:' + t });
        }
      });
    });
    return { title: 'Knowledge Graph', nodes: nodes, edges: edges };
  }

  function renderGraph() {
    var canvas = $('ilw-graph-canvas');
    if (!canvas || !g.NoahViz) return;
    if (graphViz && graphViz.destroy) { try { graphViz.destroy(); } catch (e) {} }
    graphViz = g.NoahViz.graph(canvas, buildGraphSpec(), {
      onNode: function (raw) {
        if (!raw) return;
        if (raw.id.indexOf('note:') === 0) g.ILNotes.openEditor(raw.id.slice(5));
        else if (raw.id.indexOf('ghost:') === 0) g.ILNotes.openByTitle(raw.label);
      }
    });
  }

  /* ---------------- mind maps view ---------------- */

  var mapState = { noteId: null, tree: null, selected: null, viz: null };

  function fillMapSelects() {
    var mine = g.ILMindmap ? g.ILMindmap.listMaps() : [];
    $('ilw-map-mine').innerHTML = '<option value="">Choose a custom map…</option>' + mine.map(function (n) {
      return '<option value="' + esc(n.id) + '">' + esc(n.title) + '</option>';
    }).join('');
    fetch('/assets/search-index.json').then(function (r) { return r.json(); }).then(function (data) {
      var items = ((data && data.items) || []).filter(function (it) { return /^\/bootcamps\/[^/]+\/?$/.test(it.u || ''); });
      var seen = {}, opts = '';
      items.forEach(function (it) {
        var slug = it.u.replace(/^\/bootcamps\/|\/$/g, '');
        if (seen[slug]) return; seen[slug] = 1;
        opts += '<option value="' + esc(slug) + '">' + esc(it.t) + '</option>';
      });
      $('ilw-map-cbt').innerHTML = '<option value="">Choose a bootcamp…</option>' + opts;
    }).catch(function () {});
  }

  function showMap(tree, title) {
    mapState.tree = tree; mapState.selected = null;
    $('ilw-map-editor').hidden = true;
    g.ILMindmap.renderInto($('ilw-map-canvas'), tree, {
      title: title || tree.label,
      onNode: function (n) {
        mapState.selected = n;
        if (mapState.noteId) {
          $('ilw-map-editor').hidden = false;
          $('ilw-map-label').value = n.label;
        }
      }
    });
  }

  function persistMap() {
    if (mapState.noteId && mapState.tree) g.ILMindmap.saveMap(mapState.noteId, mapState.tree);
  }

  /* ---------------- view switching ---------------- */

  function switchView(name) {
    document.querySelectorAll('[data-ilw-view]').forEach(function (b) {
      b.classList.toggle('on', b.getAttribute('data-ilw-view') === name);
    });
    ['dashboard', 'notes', 'graph', 'maps'].forEach(function (v) {
      $('ilw-view-' + v).hidden = v !== name;
    });
    if (name === 'dashboard') renderDashboard();
    if (name === 'notes') renderNotesList();
    if (name === 'graph') renderGraph();
    if (name === 'maps') fillMapSelects();
  }

  /* ---------------- boot ---------------- */

  ready(function () {
    if (!g.ILNotes || !g.ILMindmap) return;
    g.ILNotes.seedIfEmpty();

    var bySlug = scanCbts();
    loadCatalogTitles(function (titles) {
      Object.keys(bySlug).forEach(function (slug) { if (titles[slug]) bySlug[slug].title = titles[slug]; });
      cbtRows = Object.keys(bySlug).map(function (k) { return bySlug[k]; });
      renderDashboard();
    });
    cbtRows = Object.keys(bySlug).map(function (k) { return bySlug[k]; });

    document.querySelectorAll('[data-ilw-view]').forEach(function (b) {
      b.addEventListener('click', function () { switchView(b.getAttribute('data-ilw-view')); });
    });

    document.addEventListener('click', function (e) {
      var open = e.target.closest ? e.target.closest('[data-ilw-open]') : null;
      if (open) { g.ILNotes.openEditor(open.getAttribute('data-ilw-open')); return; }
      var tpl = e.target.closest ? e.target.closest('[data-ilw-template]') : null;
      if (tpl) {
        var n = g.ILNotes.createFromTemplate(tpl.getAttribute('data-ilw-template'));
        if (n) { g.ILNotes.openEditor(n.id); }
        return;
      }
      var unb = e.target.closest ? e.target.closest('[data-ilw-unbookmark]') : null;
      if (unb) { g.ILNotes.removeBookmark(unb.getAttribute('data-ilw-unbookmark')); renderDashboard(); }
    });

    $('ilw-new-note-1').addEventListener('click', function () { g.ILNotes.openEditor(null); });
    $('ilw-new-note-2').addEventListener('click', function () { g.ILNotes.openEditor(null); });
    $('ilw-export-all').addEventListener('click', function () { g.ILNotes.exportAll(); });
    $('ilw-search').addEventListener('input', renderNotesList);
    $('ilw-graph-refresh').addEventListener('click', renderGraph);

    $('ilw-cbt-table').querySelector('thead').addEventListener('click', function (e) {
      var th = e.target.closest ? e.target.closest('[data-sort]') : null;
      if (!th) return;
      var k = th.getAttribute('data-sort');
      if (cbtSort.key === k) cbtSort.dir *= -1; else { cbtSort.key = k; cbtSort.dir = 1; }
      renderCbtTable();
    });

    /* maps */
    $('ilw-map-cbt').addEventListener('change', function () {
      var slug = this.value; if (!slug) return;
      $('ilw-map-mine').value = '';
      mapState.noteId = null;
      g.ILMindmap.fetchCbtTree(slug, function (tree, content) {
        if (tree) showMap(tree, (content && content.title) || slug);
      });
    });
    $('ilw-map-mine').addEventListener('change', function () {
      var id = this.value; if (!id) return;
      $('ilw-map-cbt').value = '';
      var n = g.ILNotes.get(id);
      if (n && n.map) { mapState.noteId = id; showMap(JSON.parse(JSON.stringify(n.map)), n.title); }
    });
    $('ilw-map-new').addEventListener('click', function () {
      var name = g.prompt('Name your mind map:', 'My Mind Map');
      if (name === null) return;
      var n = g.ILMindmap.createMap(name || 'My Mind Map');
      if (n) { fillMapSelects(); $('ilw-map-mine').value = n.id; mapState.noteId = n.id; showMap(JSON.parse(JSON.stringify(n.map)), n.title); }
    });
    $('ilw-map-export').addEventListener('click', function () {
      g.ILMindmap.exportPNG($('ilw-map-canvas'), mapState.tree ? mapState.tree.label : 'mind-map');
    });
    $('ilw-map-rename').addEventListener('click', function () {
      if (!mapState.selected) return;
      mapState.tree = g.ILMindmap.renameNode(mapState.tree, mapState.selected.id, $('ilw-map-label').value);
      persistMap(); showMap(mapState.tree, mapState.tree.label);
    });
    $('ilw-map-add').addEventListener('click', function () {
      if (!mapState.selected) return;
      mapState.tree = g.ILMindmap.addChild(mapState.tree, mapState.selected.id, 'New branch');
      persistMap(); showMap(mapState.tree, mapState.tree.label);
    });
    $('ilw-map-delete').addEventListener('click', function () {
      if (!mapState.selected) return;
      mapState.tree = g.ILMindmap.deleteNode(mapState.tree, mapState.selected.id);
      mapState.selected = null;
      persistMap(); showMap(mapState.tree, mapState.tree.label);
    });

    g.addEventListener('il-notes-changed', function () {
      if (!$('ilw-view-dashboard').hidden) renderDashboard();
      if (!$('ilw-view-notes').hidden) renderNotesList();
    });

    renderDashboard();
  });
})(typeof window !== 'undefined' ? window : this);
