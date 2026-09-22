/**
 * IL readiness radar / knowledge pie (ALEKS-inspired).
 * Mount: <div data-il-radar data-il-radar-id="prep"></div>
 * Optional JSON in data-il-radar-skills='[{"label":"Linux","value":70},...]'
 * Or uses built-in profiles. Persists self-ratings to localStorage il.radar.<id>
 */
(function (g) {
  'use strict';
  var PROFILES = {
    founders: [
      { label: 'Math', value: 60 },
      { label: 'Bash/Py', value: 70 },
      { label: 'Linux', value: 75 },
      { label: 'Azure', value: 55 },
      { label: 'IaC', value: 50 },
      { label: 'CI/CD', value: 55 },
      { label: 'Ctrs', value: 50 },
      { label: 'Obs', value: 45 },
      { label: 'STAR', value: 80 }
    ],
    learn: [
      { label: 'Foundations', value: 55 },
      { label: 'DevOps', value: 48 },
      { label: 'Cloud', value: 42 },
      { label: 'Security', value: 38 },
      { label: 'Data/AI', value: 35 },
      { label: 'Portfolio', value: 60 },
      { label: 'Interview', value: 50 }
    ],
    prep: [
      { label: 'Math', value: 50 },
      { label: 'Programming', value: 45 },
      { label: 'DevOps', value: 40 },
      { label: 'Drills', value: 35 },
      { label: 'STAR', value: 55 },
      { label: 'Labs', value: 30 }
    ]
  };

  function storageKey(id) { return 'il.radar.' + id; }

  function loadSkills(el) {
    var id = el.getAttribute('data-il-radar-id') || 'default';
    var raw = el.getAttribute('data-il-radar-skills');
    var skills;
    if (raw) {
      try { skills = JSON.parse(raw); } catch (e) { skills = null; }
    }
    if (!skills) skills = (PROFILES[id] || PROFILES.learn).map(function (s) { return { label: s.label, value: s.value }; });
    try {
      var saved = g.localStorage.getItem(storageKey(id));
      if (saved) {
        var parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length === skills.length) {
          for (var i = 0; i < skills.length; i++) {
            if (typeof parsed[i].value === 'number') skills[i].value = parsed[i].value;
          }
        }
      }
    } catch (e) {}
    return { id: id, skills: skills };
  }

  function saveSkills(id, skills) {
    try {
      g.localStorage.setItem(storageKey(id), JSON.stringify(skills.map(function (s) {
        return { label: s.label, value: s.value };
      })));
    } catch (e) {}
  }

  function polar(cx, cy, r, angleRad) {
    return { x: cx + r * Math.sin(angleRad), y: cy - r * Math.cos(angleRad) };
  }

  function buildSvg(skills) {
    var n = skills.length;
    var cx = 100, cy = 100, R = 78;
    var rings = [0.33, 0.66, 1];
    var parts = [];
    parts.push('<svg viewBox="0 0 200 200" role="img" aria-label="Readiness radar with ' + n + ' competencies">');
    parts.push('<g fill="none" stroke="rgba(232,238,245,0.12)" stroke-width="0.8">');
    rings.forEach(function (t) {
      var pts = [];
      for (var i = 0; i < n; i++) {
        var p = polar(cx, cy, R * t, (i / n) * Math.PI * 2);
        pts.push(p.x.toFixed(1) + ',' + p.y.toFixed(1));
      }
      parts.push('<polygon points="' + pts.join(' ') + '"/>');
    });
    parts.push('</g>');
    parts.push('<g stroke="rgba(232,238,245,0.08)" stroke-width="0.6">');
    for (var i = 0; i < n; i++) {
      var p = polar(cx, cy, R, (i / n) * Math.PI * 2);
      parts.push('<line x1="' + cx + '" y1="' + cy + '" x2="' + p.x.toFixed(1) + '" y2="' + p.y.toFixed(1) + '"/>');
    }
    parts.push('</g>');
    var dpts = [];
    for (var j = 0; j < n; j++) {
      var v = Math.max(0, Math.min(100, skills[j].value)) / 100;
      var q = polar(cx, cy, R * v, (j / n) * Math.PI * 2);
      dpts.push(q.x.toFixed(1) + ',' + q.y.toFixed(1));
    }
    parts.push('<polygon points="' + dpts.join(' ') + '" fill="rgba(94,234,212,0.22)" stroke="#5eead4" stroke-width="1.5"/>');
    parts.push('<circle cx="' + cx + '" cy="' + cy + '" r="2.5" fill="#c9a227"/>');
    parts.push('<g fill="#8b9bb4" font-family="JetBrains Mono, monospace" font-size="5.2" text-anchor="middle">');
    for (var k = 0; k < n; k++) {
      var lab = polar(cx, cy, R + 14, (k / n) * Math.PI * 2);
      var short = String(skills[k].label).slice(0, 8);
      parts.push('<text x="' + lab.x.toFixed(1) + '" y="' + (lab.y + 2).toFixed(1) + '">' + short.replace(/[<>&]/g, '') + '</text>');
    }
    parts.push('</g></svg>');
    return parts.join('');
  }

  function readyFringe(skills) {
    // ALEKS-style: items in mid band are "ready to learn"
    return skills.filter(function (s) { return s.value >= 35 && s.value < 70; })
      .sort(function (a, b) { return b.value - a.value; })
      .slice(0, 3);
  }

  function mount(el) {
    if (el.getAttribute('data-il-radar-ready')) return;
    var data = loadSkills(el);
    var wrap = document.createElement('div');
    wrap.className = 'il-radar';
    var svgWrap = document.createElement('div');
    svgWrap.className = 'il-radar__svg-wrap';
    svgWrap.innerHTML = buildSvg(data.skills);
    var bars = document.createElement('div');
    bars.className = 'il-radar__bars';
    data.skills.forEach(function (s, idx) {
      var row = document.createElement('div');
      var lab = document.createElement('div');
      lab.className = 'il-radar__row-label';
      lab.innerHTML = '<span></span><span></span>';
      lab.children[0].textContent = s.label;
      lab.children[1].textContent = Math.round(s.value) + '%';
      var bar = document.createElement('div');
      bar.className = 'il-radar__bar';
      bar.setAttribute('role', 'slider');
      bar.setAttribute('aria-valuemin', '0');
      bar.setAttribute('aria-valuemax', '100');
      bar.setAttribute('aria-valuenow', String(Math.round(s.value)));
      bar.setAttribute('aria-label', s.label + ' readiness');
      bar.tabIndex = 0;
      var i = document.createElement('i');
      bar.appendChild(i);
      row.appendChild(lab);
      row.appendChild(bar);
      bars.appendChild(row);
      function setVal(v) {
        v = Math.max(0, Math.min(100, v));
        s.value = v;
        i.style.width = v + '%';
        lab.children[1].textContent = Math.round(v) + '%';
        bar.setAttribute('aria-valuenow', String(Math.round(v)));
        svgWrap.innerHTML = buildSvg(data.skills);
        saveSkills(data.id, data.skills);
        paintFringe();
      }
      requestAnimationFrame(function () { i.style.width = s.value + '%'; });
      bar.addEventListener('click', function (ev) {
        var rect = bar.getBoundingClientRect();
        setVal(((ev.clientX - rect.left) / rect.width) * 100);
      });
      bar.addEventListener('keydown', function (ev) {
        var step = ev.shiftKey ? 10 : 5;
        if (ev.key === 'ArrowRight' || ev.key === 'ArrowUp') { ev.preventDefault(); setVal(s.value + step); }
        if (ev.key === 'ArrowLeft' || ev.key === 'ArrowDown') { ev.preventDefault(); setVal(s.value - step); }
      });
    });
    var fringe = document.createElement('div');
    fringe.className = 'il-honest-note';
    fringe.style.gridColumn = '1 / -1';
    function paintFringe() {
      var ready = readyFringe(data.skills);
      if (!ready.length) {
        fringe.innerHTML = '<strong>Ready-to-learn fringe:</strong> Rate skills (click bars). Items in the mid band become your next practice targets — ALEKS-style, local only.';
        return;
      }
      fringe.innerHTML = '<strong>Ready-to-learn:</strong> ' +
        ready.map(function (r) { return r.label + ' (' + Math.round(r.value) + '%)'; }).join(' · ') +
        ' — practice these next. Not an employer claim; self-rated readiness.';
    }
    paintFringe();
    wrap.appendChild(svgWrap);
    wrap.appendChild(bars);
    wrap.appendChild(fringe);
    el.innerHTML = '';
    el.appendChild(wrap);
    el.setAttribute('data-il-radar-ready', '1');
    requestAnimationFrame(function () { wrap.classList.add('is-in'); });
  }

  function boot() {
    var nodes = document.querySelectorAll('[data-il-radar]');
    for (var i = 0; i < nodes.length; i++) mount(nodes[i]);
  }

  g.ILRadar = { mount: mount, boot: boot, profiles: PROFILES };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})(typeof window !== 'undefined' ? window : this);
