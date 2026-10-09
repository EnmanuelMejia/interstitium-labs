/* Subject Map — interactive MIT-style subject explorer + topic relationship graph.
   Vanilla JS, dark mode, animated, respects prefers-reduced-motion. */
(function () {
  'use strict';
  var DATA = window.IL_SUBJECT_MAP || [];
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var ACCENTS = {
    'Computer Science': '#38bdf8',
    'Mathematics': '#a78bfa',
    'Engineering': '#f472b6',
    'Physical Science': '#34d399',
    'Business': '#fbbf24',
    'Social Science': '#fb7185',
    'Arts and Humanities': '#94a3b8'
  };

  /* ---------- Subject cards ---------- */
  function renderCards() {
    var grid = document.getElementById('sm-grid');
    if (!grid) return;
    DATA.forEach(function (s, i) {
      var acc = ACCENTS[s.mitCategory] || '#38bdf8';
      var card = document.createElement('article');
      card.className = 'sm-card';
      card.style.setProperty('--acc', acc);
      card.tabIndex = 0;
      card.setAttribute('role', 'button');
      card.setAttribute('aria-label', s.mitCategory + ' — ' + s.courseCount + ' MIT courses, view topics');
      var topTopics = s.topics.slice().sort(function (a, b) { return b.mitCourseCount - a.mitCourseCount; }).slice(0, 8);
      var chips = topTopics.map(function (t) {
        var hot = t.ourCourses.length ? ' hot' : '';
        return '<span class="sm-chip' + hot + '">' + esc(t.name) + '</span>';
      }).join('');
      card.innerHTML =
        '<div class="sm-card__cat">MIT Subject Area</div>' +
        '<h2>' + esc(s.mitCategory) + '</h2>' +
        '<div class="sm-card__meta">' + s.courseCount + ' MIT OpenCourseWare courses · ' + s.topics.length + ' topics</div>' +
        '<div class="sm-card__topics">' + chips + '</div>' +
        '<div class="sm-card__ours"><b>Mapped here:</b> ' +
          (s.ourCourses.length ? s.ourCourses.map(function (c) { return '<span class="sm-chip">' + esc(c) + '</span>'; }).join(' ') : 'foundation layer') +
        '</div>';
      card.addEventListener('click', function () { openDrawer(i); });
      card.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openDrawer(i); } });
      grid.appendChild(card);
    });
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  /* ---------- Drawer ---------- */
  function openDrawer(i) {
    var s = DATA[i];
    if (!s) return;
    var d = document.getElementById('sm-drawer');
    var scrim = document.getElementById('sm-scrim');
    var acc = ACCENTS[s.mitCategory] || '#38bdf8';
    var topics = s.topics.slice().sort(function (a, b) { return b.mitCourseCount - a.mitCourseCount; });
    d.innerHTML =
      '<div class="sm-drawer__head"><div><div class="sm-card__cat" style="color:' + acc + '">MIT Subject Area</div>' +
      '<h2>' + esc(s.mitCategory) + '</h2>' +
      '<div class="sm-card__meta">' + s.courseCount + ' MIT courses · maps to ' +
        (s.ourCourses.join(', ') || 'foundation layer') + ' on Interstitium Labs</div></div>' +
      '<button class="sm-close" id="sm-close" aria-label="Close">✕ Close</button></div>' +
      '<h3 style="font-size:.95rem;color:#c7d3e4;margin:.4rem 0">Topics in this subject</h3>' +
      '<div class="sm-topicrow">' + topics.map(function (t) {
        var ours = t.ourCourses.length ? ' → <b>' + esc(t.ourCourses.join(', ')) + '</b>' : '';
        return '<span class="sm-chip' + (t.ourCourses.length ? ' hot' : '') + '" title="' + t.mitCourseCount + ' MIT courses' + esc(ours.replace(/<[^>]+>/g, '')) + '">' +
          esc(t.name) + ' <span style="opacity:.6">×' + t.mitCourseCount + '</span></span>';
      }).join('') + '</div>' +
      '<h3 style="font-size:.95rem;color:#c7d3e4;margin:.6rem 0">MIT OpenCourseWare courses <span style="font-weight:400;color:#64748b">(external links)</span></h3>' +
      '<div class="sm-mitcourses">' + s.mitCourses.map(function (c) {
        return '<a class="sm-mit sm-link" style="text-decoration:none" href="https://ocw.mit.edu/courses/' + esc(c.number.toLowerCase().replace(/\./g, '-')) + '/" target="_blank" rel="noopener">' +
          '<div class="sm-mit__num">' + esc(c.number) + ' ↗</div>' +
          '<div class="sm-mit__name">' + esc(c.name) + '</div></a>';
      }).join('') + '</div>' +
      '<p style="margin-top:1.2rem;font-size:.8rem;color:#64748b">Course materials © MIT, available under Creative Commons. Links open MIT OpenCourseWare.</p>';
    d.classList.add('open');
    scrim.classList.add('open');
    document.getElementById('sm-close').addEventListener('click', closeDrawer);
    scrim.onclick = closeDrawer;
  }
  function closeDrawer() {
    document.getElementById('sm-drawer').classList.remove('open');
    document.getElementById('sm-scrim').classList.remove('open');
  }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeDrawer(); });

  /* ---------- Topic relationship graph (canvas force layout) ---------- */
  function renderGraph() {
    var cv = document.getElementById('sm-graph');
    if (!cv || !window.IL_SUBJECT_MAP) return;
    var ctx = cv.getContext('2d');
    var W, H, dpr;
    function size() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = cv.clientWidth; H = cv.clientHeight;
      cv.width = W * dpr; cv.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    size();
    window.addEventListener('resize', size);

    // Build nodes: 7 subject hubs + their top topics (shared topics merged)
    var nodes = [], edges = [], byName = {};
    function addNode(id, label, kind, acc, r) {
      if (byName[id]) return byName[id];
      var n = { id: id, label: label, kind: kind, acc: acc, r: r,
        x: Math.random() * W, y: Math.random() * H, vx: 0, vy: 0 };
      byName[id] = n; nodes.push(n); return n;
    }
    DATA.forEach(function (s) {
      var hub = addNode('S:' + s.mitCategory, s.mitCategory, 'subject', ACCENTS[s.mitCategory] || '#38bdf8', 26);
      var tops = s.topics.slice().sort(function (a, b) { return b.mitCourseCount - a.mitCourseCount; }).slice(0, 10);
      tops.forEach(function (t) {
        var tn = addNode('T:' + t.name, t.name, 'topic', t.ourCourses.length ? '#38bdf8' : '#475569', 8 + Math.min(t.mitCourseCount, 6));
        edges.push([hub, tn]);
      });
    });

    // Simple force layout
    var running = true, ticks = 0;
    function tick() {
      if (!running) return;
      for (var i = 0; i < nodes.length; i++) {
        var a = nodes[i];
        for (var j = i + 1; j < nodes.length; j++) {
          var b = nodes[j], dx = a.x - b.x, dy = a.y - b.y, d2 = dx * dx + dy * dy + 40;
          var f = 2600 / d2;
          var d = Math.sqrt(d2);
          a.vx += (dx / d) * f; a.vy += (dy / d) * f;
          b.vx -= (dx / d) * f; b.vy -= (dy / d) * f;
        }
      }
      edges.forEach(function (e) {
        var a = e[0], b = e[1], dx = b.x - a.x, dy = b.y - a.y, d = Math.sqrt(dx * dx + dy * dy) || 1;
        var want = 120, f = (d - want) * 0.012;
        a.vx += (dx / d) * f; a.vy += (dy / d) * f;
        b.vx -= (dx / d) * f; b.vy -= (dy / d) * f;
      });
      nodes.forEach(function (n) {
        n.vx *= 0.86; n.vy *= 0.86;
        n.x += n.vx; n.y += n.vy;
        // center gravity + bounds
        n.vx += (W / 2 - n.x) * 0.004; n.vy += (H / 2 - n.y) * 0.004;
        n.x = Math.max(n.r + 8, Math.min(W - n.r - 8, n.x));
        n.y = Math.max(n.r + 8, Math.min(H - n.r - 8, n.y));
      });
      draw();
      if (++ticks < (reduceMotion ? 60 : 400)) requestAnimationFrame(tick);
      else running = false;
    }
    function draw() {
      ctx.clearRect(0, 0, W, H);
      edges.forEach(function (e) {
        ctx.strokeStyle = 'rgba(148,163,184,.14)';
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(e[0].x, e[0].y); ctx.lineTo(e[1].x, e[1].y); ctx.stroke();
      });
      nodes.forEach(function (n) {
        var g = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r * 2.2);
        g.addColorStop(0, n.acc + '55'); g.addColorStop(1, 'transparent');
        ctx.fillStyle = g;
        ctx.beginPath(); ctx.arc(n.x, n.y, n.r * 2.2, 0, 7); ctx.fill();
        ctx.fillStyle = n.kind === 'subject' ? n.acc : '#0b1220';
        ctx.strokeStyle = n.acc; ctx.lineWidth = n.kind === 'subject' ? 2.5 : 1.5;
        ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, 7); ctx.fill(); ctx.stroke();
        ctx.fillStyle = n.kind === 'subject' ? '#0b1220' : '#c7d3e4';
        ctx.font = (n.kind === 'subject' ? '700 11px' : '10px') + ' "Space Grotesk",sans-serif';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        var label = n.kind === 'subject' ? n.label.split(' ')[0] : n.label;
        ctx.fillText(n.kind === 'subject' ? n.label : '', n.x, n.y);
        if (n.kind === 'topic' && n.r > 10) {
          ctx.fillStyle = '#94a3b8';
          ctx.fillText(label.length > 14 ? label.slice(0, 13) + '…' : label, n.x, n.y + n.r + 10);
        }
      });
      // subject labels below hubs
      ctx.font = '700 12px "Space Grotesk",sans-serif'; ctx.fillStyle = '#e2e8f0'; ctx.textAlign = 'center';
      nodes.forEach(function (n) {
        if (n.kind === 'subject') ctx.fillText(n.label, n.x, n.y + n.r + 14);
      });
    }
    // Hover tooltip
    var tip = document.createElement('div');
    tip.style.cssText = 'position:absolute;pointer-events:none;background:#0b1220;border:1px solid rgba(56,189,248,.4);border-radius:.6rem;padding:.4rem .7rem;font-size:.78rem;color:#e2e8f0;display:none;z-index:5';
    cv.parentElement.style.position = 'relative';
    cv.parentElement.appendChild(tip);
    cv.addEventListener('mousemove', function (e) {
      var r = cv.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top, hit = null;
      nodes.forEach(function (n) {
        var d = Math.hypot(n.x - mx, n.y - my);
        if (d < n.r + 6) hit = n;
      });
      if (hit) {
        tip.style.display = 'block';
        tip.style.left = (mx + 14) + 'px'; tip.style.top = (my + 14) + 'px';
        tip.textContent = hit.kind === 'subject' ? hit.label + ' — MIT subject area' : hit.label + ' — topic';
      } else tip.style.display = 'none';
    });
    cv.addEventListener('mouseleave', function () { tip.style.display = 'none'; });
    tick();
  }

  document.addEventListener('DOMContentLoaded', function () {
    renderCards();
    renderGraph();
  });
})();
