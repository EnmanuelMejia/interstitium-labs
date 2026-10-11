/**
 * NoahViz — cinematic visualization engine for Noah AI tutoring.
 * (Interstitium original. Canvas 2D, no dependencies, CSP-safe.)
 *
 * RHEL-reel quality bar: void-black, neon red/blue, metallic chrome text,
 * holographic labels, scanline depth. Respects prefers-reduced-motion.
 *
 * API:
 *   NoahViz.anatomy(canvas, spec)   — Systems Anatomy 4-step (DEFAULT explainer)
 *   NoahViz.flow(canvas, spec)      — animated node/edge flow diagram
 *   NoahViz.topology(canvas, spec)  — network topology, pulsing links
 *
 * anatomy spec:
 *   { title, subtitle, parts:[{id,label,x,y,desc}], flows:[{from,to,label}] }
 *   x,y in 0..1. flows reference part ids.
 *
 * flow spec:
 *   { title, nodes:[{id,label,x,y}], edges:[{from,to,label}] }
 *
 * topology spec:
 *   { title, nodes:[{id,label,x,y,kind}], links:[[idA,idB]] }
 */
(function (g) {
  'use strict';

  var RED = '#ff3b5c', BLUE = '#4da6ff', GOLD = '#c9a227';
  var CYAN = '#5EEAD4', INK = '#06080c', TXT = '#dbe4ee', DIM = '#8b93a5';

  function reduced() {
    try { return !!(g.matchMedia && g.matchMedia('(prefers-reduced-motion: reduce)').matches); }
    catch (e) { return false; }
  }

  function fit(canvas) {
    var dpr = Math.min(2, g.devicePixelRatio || 1);
    var r = canvas.getBoundingClientRect();
    var w = Math.max(280, r.width || 640), h = Math.max(220, r.height || 360);
    canvas.width = w * dpr; canvas.height = h * dpr;
    var ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, w: w, h: h };
  }

  function chromeText(ctx, text, x, y, size, align) {
    var gr = ctx.createLinearGradient(0, y - size, 0, y + size * 0.3);
    gr.addColorStop(0, '#ffffff'); gr.addColorStop(0.45, '#c8d4e2');
    gr.addColorStop(0.55, '#7d8ea3'); gr.addColorStop(1, '#e8eef5');
    ctx.fillStyle = gr;
    ctx.font = '700 ' + size + 'px "Space Grotesk", system-ui, sans-serif';
    ctx.textAlign = align || 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(text, x, y);
  }

  function holoLabel(ctx, text, x, y, color) {
    ctx.font = '600 10px "JetBrains Mono", ui-monospace, monospace';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    var w = ctx.measureText(text).width + 16;
    ctx.fillStyle = 'rgba(6,10,16,0.82)';
    ctx.strokeStyle = color; ctx.lineWidth = 1;
    roundRect(ctx, x - w / 2, y - 10, w, 20, 10); ctx.fill(); ctx.stroke();
    ctx.fillStyle = color; ctx.fillText(text, x, y + 0.5);
  }

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }

  function scanlines(ctx, w, h) {
    ctx.fillStyle = 'rgba(255,255,255,0.022)';
    for (var y = 0; y < h; y += 4) ctx.fillRect(0, y, w, 1);
  }

  function vignette(ctx, w, h) {
    var g2 = ctx.createRadialGradient(w/2, h/2, Math.min(w,h)*0.35, w/2, h/2, Math.max(w,h)*0.75);
    g2.addColorStop(0, 'rgba(0,0,0,0)'); g2.addColorStop(1, 'rgba(0,0,0,0.55)');
    ctx.fillStyle = g2; ctx.fillRect(0, 0, w, h);
  }

  function bg(ctx, w, h, t, accent) {
    var g2 = ctx.createLinearGradient(0, 0, w, h);
    g2.addColorStop(0, '#070a12'); g2.addColorStop(0.5, '#0a0f1c'); g2.addColorStop(1, '#060810');
    ctx.fillStyle = g2; ctx.fillRect(0, 0, w, h);
    /* drifting circuit traces */
    ctx.strokeStyle = accent; ctx.globalAlpha = 0.10; ctx.lineWidth = 1;
    var i, y;
    for (i = 0; i < 5; i++) {
      y = (h * (i + 0.5)) / 5 + Math.sin(t * 0.4 + i * 2) * 8;
      ctx.beginPath(); ctx.moveTo(-20, y);
      ctx.bezierCurveTo(w*0.3, y - 30, w*0.6, y + 30, w + 20, y);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }

  function node(ctx, x, y, r, color, glow, active) {
    if (active) { glow *= 1.8; r *= 1.15; }
    var g2 = ctx.createRadialGradient(x, y, 0, x, y, r * 3);
    g2.addColorStop(0, color); g2.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.globalAlpha = 0.35 * glow; ctx.fillStyle = g2;
    ctx.beginPath(); ctx.arc(x, y, r * 3, 0, 7); ctx.fill();
    ctx.globalAlpha = 1;
    g2 = ctx.createRadialGradient(x - r*0.3, y - r*0.3, 0, x, y, r);
    g2.addColorStop(0, '#ffffff'); g2.addColorStop(0.4, color); g2.addColorStop(1, '#0a0f1c');
    ctx.fillStyle = g2;
    ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
    ctx.strokeStyle = color; ctx.lineWidth = active ? 2.5 : 1.2;
    ctx.beginPath(); ctx.arc(x, y, r + 4, 0, 7); ctx.stroke();
  }

  /* ---------------- Systems Anatomy (default explainer) ---------------- */

  var ANATOMY_STEPS = [
    { k: 'whole',  cap: 'See the whole in context' },
    { k: 'open',   cap: 'Cut it open' },
    { k: 'walk',   cap: 'Walk through the process' },
    { k: 'apart',  cap: 'Pull it apart — labeled pieces' }
  ];

  function anatomy(canvas, spec) {
    var f = fit(canvas), ctx = f.ctx, W = f.w, H = f.h;
    var step = 0, t = 0, raf = 0, alive = true, playing = false, playT = 0;
    var RM = reduced();
    var parts = (spec.parts || []).map(function (p, i) {
      return { id: p.id, label: p.label, desc: p.desc || '',
               x0: p.x, y0: p.y, i: i,
               color: i % 2 ? BLUE : (i % 3 === 2 ? GOLD : CYAN) };
    });
    var flows = spec.flows || [];
    var byId = {}; parts.forEach(function (p) { byId[p.id] = p; });

    function partPos(p, s, tt) {
      var cx = W / 2, cy = H * 0.56;
      if (s === 0) return { x: p.x0 * W, y: 0.22 * H + p.y0 * H * 0.62 };
      if (s === 1) { /* exploded: push away from center */
        var dx = (p.x0 * W - cx), dy = (0.22*H + p.y0*H*0.62 - cy);
        var m = Math.hypot(dx, dy) || 1, push = 1.45;
        return { x: cx + dx / m * Math.min(m * push, W * 0.42), y: cy + dy / m * Math.min(m * push, H * 0.34) };
      }
      if (s === 3) { /* grid of labeled pieces */
        var cols = parts.length > 6 ? 3 : 2;
        var col = p.i % cols, row = Math.floor(p.i / cols);
        var rowsN = Math.ceil(parts.length / cols);
        return { x: W * (0.5 + (col - (cols-1)/2) * 0.36), y: H * (0.30 + row * (0.52 / Math.max(1, rowsN - 1 || 1))) };
      }
      return { x: p.x0 * W, y: 0.22 * H + p.y0 * H * 0.62 };
    }

    /* walk-through pulse: which flow edge is active + progress */
    function walkState(tt) {
      if (!flows.length) return null;
      var per = 2.2, total = flows.length * per;
      var lt = RM ? total - 0.01 : (tt % total);
      var idx = Math.min(flows.length - 1, Math.floor(lt / per));
      return { idx: idx, prog: (lt - idx * per) / per, flow: flows[idx] };
    }

    function draw() {
      if (!alive) return;
      bg(ctx, W, H, t, CYAN);
      var i, p, pos;

      /* title */
      chromeText(ctx, spec.title || 'Systems Anatomy', W / 2, 30, Math.min(24, W / 22));
      if (spec.subtitle) {
        ctx.fillStyle = DIM; ctx.font = '12px system-ui, sans-serif';
        ctx.textAlign = 'center'; ctx.fillText(spec.subtitle, W / 2, 52);
      }
      /* step caption */
      holoLabel(ctx, (step + 1) + ' / 4 · ' + ANATOMY_STEPS[step].cap, W / 2, H - 44, GOLD);

      if (step === 0) { /* container ring = the whole */
        ctx.strokeStyle = CYAN; ctx.globalAlpha = 0.35; ctx.lineWidth = 2;
        ctx.setLineDash([10, 8]);
        roundRect(ctx, W*0.06, H*0.16, W*0.88, H*0.60, 18); ctx.stroke();
        ctx.setLineDash([]); ctx.globalAlpha = 1;
      }

      /* flows (under parts) */
      var ws = (step === 2) ? walkState(t) : null;
      flows.forEach(function (fl, fi) {
        var a = byId[fl.from], b = byId[fl.to];
        if (!a || !b) return;
        var pa = partPos(a, step, t), pb = partPos(b, step, t);
        var active = ws && ws.idx === fi;
        ctx.strokeStyle = active ? RED : CYAN;
        ctx.globalAlpha = step === 2 ? (active ? 0.95 : 0.25) : 0.45;
        ctx.lineWidth = active ? 3 : 1.5;
        ctx.beginPath(); ctx.moveTo(pa.x, pa.y);
        var mx = (pa.x + pb.x) / 2, my = (pa.y + pb.y) / 2 - 24;
        ctx.quadraticCurveTo(mx, my, pb.x, pb.y); ctx.stroke();
        ctx.globalAlpha = 1;
        if (active && ws) { /* traveling pulse */
          var qx = (1-ws.prog)*(1-ws.prog)*pa.x + 2*(1-ws.prog)*ws.prog*mx + ws.prog*ws.prog*pb.x;
          var qy = (1-ws.prog)*(1-ws.prog)*pa.y + 2*(1-ws.prog)*ws.prog*my + ws.prog*ws.prog*pb.y;
          var gg = ctx.createRadialGradient(qx, qy, 0, qx, qy, 16);
          gg.addColorStop(0, '#fff'); gg.addColorStop(0.4, RED); gg.addColorStop(1, 'rgba(255,59,92,0)');
          ctx.fillStyle = gg; ctx.beginPath(); ctx.arc(qx, qy, 16, 0, 7); ctx.fill();
          if (fl.label) holoLabel(ctx, fl.label, qx, qy - 26, RED);
        }
      });

      /* parts */
      parts.forEach(function (pp) {
        pos = partPos(pp, step, t);
        var isActive = ws && (ws.flow.from === pp.id || ws.flow.to === pp.id);
        var r = Math.max(14, W * 0.028);
        node(ctx, pos.x, pos.y, r, pp.color, 0.8 + 0.2 * Math.sin(t * 2 + pp.i), isActive);
        holoLabel(ctx, pp.label, pos.x, pos.y + r + 18, pp.color);
        if (step === 3 && pp.desc) {
          ctx.fillStyle = DIM; ctx.font = '11px system-ui, sans-serif';
          ctx.textAlign = 'center';
          wrapText(ctx, pp.desc, pos.x, pos.y + r + 36, W * 0.30, 14);
        }
      });

      scanlines(ctx, W, H); vignette(ctx, W, H);
    }

    function wrapText(c, text, x, y, maxW, lh) {
      var words = text.split(' '), line = '', yy = y;
      words.forEach(function (w) {
        var test = line ? line + ' ' + w : w;
        if (c.measureText(test).width > maxW && line) { c.fillText(line, x, yy); line = w; yy += lh; }
        else line = test;
      });
      c.fillText(line, x, yy);
    }

    function loop(ts) {
      if (!alive) return;
      t += 0.016;
      if (playing && !RM) { playT += 0.016; if (playT > 3.2) { playT = 0; setStep((step + 1) % 4); } }
      draw();
      raf = requestAnimationFrame(loop);
    }

    function setStep(s) {
      step = Math.max(0, Math.min(3, s));
      ui();
      if (RM) draw();
    }

    /* stepper UI */
    var bar = document.createElement('div');
    bar.className = 'noahviz-bar';
    bar.innerHTML =
      '<button type="button" data-v="prev" aria-label="Previous step">‹</button>' +
      '<span class="noahviz-dots">' +
      ANATOMY_STEPS.map(function (s, i) {
        return '<button type="button" data-v="' + i + '" aria-label="' + s.cap + '"></button>';
      }).join('') + '</span>' +
      '<button type="button" data-v="next" aria-label="Next step">›</button>' +
      (RM ? '' : '<button type="button" data-v="play" aria-label="Auto-play steps">▶</button>');
    bar.addEventListener('click', function (e) {
      var v = e.target.getAttribute('data-v');
      if (v == null) return;
      if (v === 'prev') setStep(step - 1);
      else if (v === 'next') setStep(step + 1);
      else if (v === 'play') { playing = !playing; playT = 0; ui(); }
      else setStep(parseInt(v, 10));
    });
    function ui() {
      var dots = bar.querySelectorAll('[data-v]');
      dots.forEach(function (d) {
        var v = d.getAttribute('data-v');
        if (/^\d$/.test(v)) d.classList.toggle('on', parseInt(v, 10) === step);
        if (v === 'play') { d.textContent = playing ? '⏸' : '▶'; d.classList.toggle('on', playing); }
      });
    }
    canvas.parentNode.insertBefore(bar, canvas.nextSibling);
    ui();

    var css = document.getElementById('noahviz-css');
    if (!css) {
      css = document.createElement('style'); css.id = 'noahviz-css';
      css.textContent = [
        '.noahviz-bar{display:flex;align-items:center;justify-content:center;gap:10px;padding:10px 4px 2px;}',
        '.noahviz-bar button{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.16);',
        'color:#dbe4ee;border-radius:8px;min-width:34px;min-height:34px;font-size:16px;cursor:pointer;}',
        '.noahviz-bar button.on{background:rgba(201,162,39,.25);border-color:#c9a227;color:#fff;}',
        '.noahviz-bar .noahviz-dots{display:flex;gap:6px;}',
        '.noahviz-bar .noahviz-dots button{min-width:12px;min-height:12px;width:12px;height:12px;',
        'border-radius:50%;padding:0;font-size:0;}'
      ].join('');
      document.head.appendChild(css);
    }

    if (!RM) raf = requestAnimationFrame(loop); else draw();
    return {
      setStep: setStep,
      destroy: function () { alive = false; cancelAnimationFrame(raf); if (bar.parentNode) bar.parentNode.removeChild(bar); }
    };
  }

  /* ---------------- Flow diagram ---------------- */

  function flow(canvas, spec) {
    var f = fit(canvas), ctx = f.ctx, W = f.w, H = f.h;
    var t = 0, raf = 0, alive = true, RM = reduced();
    var nodes = spec.nodes || [], edges = spec.edges || [];
    var byId = {}; nodes.forEach(function (n) { byId[n.id] = n; });
    nodes.forEach(function (n, i) { n.color = i % 2 ? BLUE : CYAN; });

    function draw() {
      bg(ctx, W, H, t, BLUE);
      chromeText(ctx, spec.title || 'Flow', W / 2, 28, Math.min(22, W / 24));
      edges.forEach(function (e, ei) {
        var a = byId[e.from], b = byId[e.to]; if (!a || !b) return;
        var ax = a.x * W, ay = 0.2*H + a.y * H * 0.65, bx = b.x * W, by = 0.2*H + b.y * H * 0.65;
        ctx.strokeStyle = CYAN; ctx.globalAlpha = 0.5; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(bx, by); ctx.stroke();
        ctx.globalAlpha = 1;
        if (!RM) {
          var p = (t * 0.5 + ei * 0.33) % 1;
          var px = ax + (bx - ax) * p, py = ay + (by - ay) * p;
          ctx.fillStyle = RED; ctx.beginPath(); ctx.arc(px, py, 3.5, 0, 7); ctx.fill();
        }
        if (e.label) holoLabel(ctx, e.label, (ax+bx)/2, (ay+by)/2 - 16, DIM);
      });
      nodes.forEach(function (n, i) {
        var x = n.x * W, y = 0.2 * H + n.y * H * 0.65;
        node(ctx, x, y, Math.max(13, W * 0.026), n.color, 0.8 + 0.2 * Math.sin(t * 2 + i), false);
        holoLabel(ctx, n.label, x, y + Math.max(13, W*0.026) + 17, n.color);
      });
      scanlines(ctx, W, H); vignette(ctx, W, H);
    }
    function loop() { if (!alive) return; t += 0.016; draw(); raf = requestAnimationFrame(loop); }
    if (!RM) raf = requestAnimationFrame(loop); else draw();
    return { destroy: function () { alive = false; cancelAnimationFrame(raf); } };
  }

  /* ---------------- Topology ---------------- */

  function topology(canvas, spec) {
    var f = fit(canvas), ctx = f.ctx, W = f.w, H = f.h;
    var t = 0, raf = 0, alive = true, RM = reduced();
    var nodes = spec.nodes || [], links = spec.links || [];
    var byId = {}; nodes.forEach(function (n) { byId[n.id] = n; });
    var KIND = { core: RED, dist: BLUE, edge: CYAN, host: GOLD };

    function draw() {
      bg(ctx, W, H, t, RED);
      chromeText(ctx, spec.title || 'Topology', W / 2, 28, Math.min(22, W / 24));
      links.forEach(function (L, li) {
        var a = byId[L[0]], b = byId[L[1]]; if (!a || !b) return;
        var ax = a.x*W, ay = 0.18*H + a.y*H*0.68, bx = b.x*W, by = 0.18*H + b.y*H*0.68;
        var pulse = RM ? 0.6 : 0.45 + 0.25 * Math.sin(t * 3 + li * 1.7);
        ctx.strokeStyle = BLUE; ctx.globalAlpha = pulse; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(bx, by); ctx.stroke();
        ctx.globalAlpha = 1;
      });
      nodes.forEach(function (n, i) {
        var x = n.x*W, y = 0.18*H + n.y*H*0.68;
        var col = KIND[n.kind] || CYAN;
        var r = n.kind === 'core' ? Math.max(16, W*0.032) : Math.max(11, W*0.022);
        node(ctx, x, y, r, col, 0.85 + 0.25 * Math.sin(t * 2.4 + i * 1.3), false);
        holoLabel(ctx, n.label, x, y + r + 16, col);
      });
      scanlines(ctx, W, H); vignette(ctx, W, H);
    }
    function loop() { if (!alive) return; t += 0.016; draw(); raf = requestAnimationFrame(loop); }
    if (!RM) raf = requestAnimationFrame(loop); else draw();
    return { destroy: function () { alive = false; cancelAnimationFrame(raf); } };
  }

  /* ---------------- Knowledge Graph (Obsidian-style, distilled) ----------------
   * spec: { title, nodes:[{id,label,mastery:0..1|null,group}], edges:[{from,to}] }
   * opts: { onNode(node), legend }
   * Force-directed layout on the same canvas engine. Node color encodes
   * mastery: gold = mastered, cyan = proficient, blue = learning,
   * dim = not started / unknown. Size encodes connection count.
   * Click a node to open it (opts.onNode). Drag a node to pin it. */

  function masteryColor(m) {
    if (m == null || isNaN(m)) return DIM;
    if (m >= 0.8) return GOLD;
    if (m >= 0.5) return CYAN;
    if (m > 0.05) return BLUE;
    return DIM;
  }

  function graph(canvas, spec, opts) {
    opts = opts || {};
    var f = fit(canvas), ctx = f.ctx, W = f.w, H = f.h;
    var t = 0, raf = 0, alive = true, RM = reduced();
    var nodes = (spec.nodes || []).map(function (n, i) {
      var a = (i / Math.max(1, spec.nodes.length)) * Math.PI * 2;
      var rr = Math.min(W, H) * 0.30;
      return { id: n.id, label: n.label, mastery: (typeof n.mastery === 'number') ? n.mastery : null,
               group: n.group || '', raw: n,
               x: W / 2 + Math.cos(a) * rr * (0.4 + 0.6 * ((i * 37) % 10) / 10),
               y: H * 0.55 + Math.sin(a) * rr * 0.8, vx: 0, vy: 0, deg: 0, drag: false };
    });
    var byId = {}; nodes.forEach(function (n) { byId[n.id] = n; });
    var edges = [];
    (spec.edges || []).forEach(function (e) {
      var a = byId[e.from], b = byId[e.to];
      if (!a || !b || a === b) return;
      edges.push({ a: a, b: b }); a.deg++; b.deg++;
    });
    var maxDeg = 1; nodes.forEach(function (n) { if (n.deg > maxDeg) maxDeg = n.deg; });

    function radius(n) { return 9 + 13 * Math.sqrt(n.deg / maxDeg); }

    function stepPhysics() {
      var i, j, a, b, dx, dy, d2, fr;
      var CX = W / 2, CY = H * 0.55;
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        /* centering gravity (weak) */
        a.vx += (CX - a.x) * 0.0022; a.vy += (CY - a.y) * 0.0022;
        /* keep inside the frame */
        if (a.x < 34) a.vx += 0.6; if (a.x > W - 34) a.vx -= 0.6;
        if (a.y < 78) a.vy += 0.6; if (a.y > H - 30) a.vy -= 0.6;
        for (j = i + 1; j < nodes.length; j++) {
          b = nodes[j]; dx = a.x - b.x; dy = a.y - b.y;
          d2 = dx * dx + dy * dy; if (d2 < 1) { dx = (i - j) || 1; dy = 1; d2 = 2; }
          fr = Math.min(2600 / d2, 1.4);
          a.vx += dx * fr * 0.06; a.vy += dy * fr * 0.06;
          b.vx -= dx * fr * 0.06; b.vy -= dy * fr * 0.06;
        }
      }
      edges.forEach(function (e) {
        dx = e.b.x - e.a.x; dy = e.b.y - e.a.y;
        var d = Math.sqrt(dx * dx + dy * dy) || 1, rest = 118;
        fr = (d - rest) / d * 0.028;
        e.a.vx += dx * fr; e.a.vy += dy * fr;
        e.b.vx -= dx * fr; e.b.vy -= dy * fr;
      });
      nodes.forEach(function (n) {
        if (n.drag) { n.vx = 0; n.vy = 0; return; }
        n.vx *= 0.86; n.vy *= 0.86;
        n.x += n.vx; n.y += n.vy;
      });
    }

    var hover = null;
    function draw() {
      bg(ctx, W, H, t, BLUE);
      chromeText(ctx, spec.title || 'Knowledge Graph', W / 2, 30, Math.min(22, W / 24));
      edges.forEach(function (e) {
        var hot = hover && (e.a === hover || e.b === hover);
        ctx.strokeStyle = hot ? GOLD : CYAN;
        ctx.globalAlpha = hot ? 0.85 : 0.30; ctx.lineWidth = hot ? 2 : 1.2;
        ctx.beginPath(); ctx.moveTo(e.a.x, e.a.y); ctx.lineTo(e.b.x, e.b.y); ctx.stroke();
        ctx.globalAlpha = 1;
      });
      nodes.forEach(function (n, i) {
        var col = masteryColor(n.mastery);
        var r = radius(n);
        node(ctx, n.x, n.y, r, col, 0.75 + 0.25 * Math.sin(t * 2 + i), hover === n);
        ctx.font = '600 11px system-ui, sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'top';
        ctx.fillStyle = hover === n ? '#ffffff' : TXT;
        var lbl = n.label.length > 26 ? n.label.slice(0, 25) + '…' : n.label;
        ctx.fillText(lbl, n.x, n.y + r + 6);
      });
      if (opts.legend !== false) {
        ctx.font = '10px "JetBrains Mono", monospace'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
        var items = [[GOLD, 'Mastered'], [CYAN, 'Proficient'], [BLUE, 'Learning'], [DIM, 'Not started']];
        var lx = 14;
        items.forEach(function (it) {
          ctx.fillStyle = it[0]; ctx.beginPath(); ctx.arc(lx + 4, H - 16, 4, 0, 7); ctx.fill();
          ctx.fillStyle = DIM; ctx.fillText(it[1], lx + 12, H - 15);
          lx += 22 + ctx.measureText(it[1]).width + 16;
        });
      }
      scanlines(ctx, W, H); vignette(ctx, W, H);
    }

    function loop() { if (!alive) return; t += 0.016; stepPhysics(); draw(); raf = requestAnimationFrame(loop); }

    function pick(mx, my) {
      var best = null, bd = 1e9;
      nodes.forEach(function (n) {
        var d = Math.hypot(n.x - mx, n.y - my);
        if (d < radius(n) + 12 && d < bd) { bd = d; best = n; }
      });
      return best;
    }
    function evtPos(e) {
      var r = canvas.getBoundingClientRect();
      var sx = (canvas.width / (g.devicePixelRatio > 2 ? 2 : (g.devicePixelRatio || 1))) / r.width;
      return { x: (e.clientX - r.left), y: (e.clientY - r.top), rx: (e.clientX - r.left) * (W / r.width), ry: (e.clientY - r.top) * (H / r.height), sx: sx };
    }
    var dragN = null, moved = false;
    function onDown(e) { var p = evtPos(e); var n = pick(p.rx, p.ry); if (n) { dragN = n; n.drag = true; moved = false; } }
    function onMove(e) {
      var p = evtPos(e);
      if (dragN) { dragN.x = p.rx; dragN.y = p.ry; moved = true; if (RM) { draw(); } return; }
      var n = pick(p.rx, p.ry);
      if (n !== hover) { hover = n; canvas.style.cursor = n ? 'pointer' : 'default'; if (RM) draw(); }
    }
    function onUp(e) {
      if (dragN) {
        var wasDrag = moved; dragN.drag = false; var n = dragN; dragN = null;
        if (!wasDrag && opts.onNode) opts.onNode(n.raw);
      }
    }
    canvas.addEventListener('pointerdown', onDown);
    canvas.addEventListener('pointermove', onMove);
    canvas.addEventListener('pointerup', onUp);

    /* settle the layout quickly, then keep a gentle live simulation */
    for (var s = 0; s < 90; s++) stepPhysics();
    if (!RM) raf = requestAnimationFrame(loop); else draw();
    return {
      destroy: function () {
        alive = false; cancelAnimationFrame(raf);
        canvas.removeEventListener('pointerdown', onDown);
        canvas.removeEventListener('pointermove', onMove);
        canvas.removeEventListener('pointerup', onUp);
      }
    };
  }

  /* ---------------- Mind Map (tidy-tree) ----------------
   * spec: { title, root:{id,label,children:[...], meta} }
   * opts: { onNode(node), }
   * Horizontal tidy tree: root left, branches flow right. Clicking a
   * parent collapses/expands it; clicking any node fires opts.onNode. */

  function mindmap(canvas, spec, opts) {
    opts = opts || {};
    var f = fit(canvas), ctx = f.ctx, W = f.w, H = f.h;
    var t = 0, raf = 0, alive = true, RM = reduced();
    var root = spec.root;
    var DEPTH_COLORS = [GOLD, CYAN, BLUE, RED, '#b48be8', '#5ad1a0'];
    var pan = { x: 0, y: 0 }, placed = [];

    function visibleChildren(n) { return n.collapsed ? [] : (n.children || []); }
    function layout() {
      placed = [];
      var leaf = 0, maxDepth = 0;
      (function walk(n, depth) {
        n._depth = depth; if (depth > maxDepth) maxDepth = depth;
        var kids = visibleChildren(n);
        if (!kids.length) { n._slot = leaf++; }
        else { kids.forEach(function (k) { walk(k, depth + 1); }); n._slot = (kids[0]._slot + kids[kids.length - 1]._slot) / 2; }
        placed.push(n);
      })(root, 0);
      var leaves = Math.max(1, leaf);
      var topPad = 74, botPad = 30, leftPad = 26, rightPad = 30;
      var colW = Math.max(120, (W - leftPad - rightPad) / (maxDepth + 1));
      placed.forEach(function (n) {
        n._x = leftPad + n._depth * colW + colW * 0.42;
        n._y = topPad + (n._slot + 0.5) * ((H - topPad - botPad) / leaves);
        n._w = Math.min(colW * 0.86, 26 + ctx.measureText(trunc(n.label, 30)).width + 26);
      });
    }
    function trunc(s, n) { s = String(s == null ? '' : s); return s.length > n ? s.slice(0, n - 1) + '…' : s; }

    function draw() {
      bg(ctx, W, H, t, GOLD);
      chromeText(ctx, spec.title || 'Mind Map', W / 2, 30, Math.min(22, W / 24));
      ctx.save(); ctx.translate(pan.x, pan.y);
      /* branches first */
      placed.forEach(function (n) {
        visibleChildren(n).forEach(function (k) {
          var col = DEPTH_COLORS[Math.min(DEPTH_COLORS.length - 1, k._depth)];
          ctx.strokeStyle = col; ctx.globalAlpha = 0.55; ctx.lineWidth = Math.max(1, 3 - k._depth * 0.5);
          ctx.beginPath(); ctx.moveTo(n._x + n._w / 2, n._y);
          var mx = (n._x + n._w / 2 + k._x - k._w / 2) / 2;
          ctx.bezierCurveTo(mx, n._y, mx, k._y, k._x - k._w / 2, k._y); ctx.stroke();
          ctx.globalAlpha = 1;
        });
      });
      placed.forEach(function (n) {
        var col = DEPTH_COLORS[Math.min(DEPTH_COLORS.length - 1, n._depth)];
        var w = n._w, h = 30, x = n._x - w / 2, y = n._y - h / 2;
        ctx.fillStyle = 'rgba(8,12,22,0.92)';
        ctx.strokeStyle = col; ctx.lineWidth = n._depth === 0 ? 2.2 : 1.2;
        roundRect(ctx, x, y, w, h, 9); ctx.fill(); ctx.stroke();
        ctx.font = (n._depth === 0 ? '700 ' : '600 ') + '11.5px system-ui, sans-serif';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = TXT;
        ctx.fillText(trunc(n.label, 30), n._x, n._y + 0.5);
        var kids = n.children || [];
        if (kids.length) {
          ctx.fillStyle = col; ctx.beginPath();
          ctx.arc(n._x + w / 2, n._y, 8, 0, 7); ctx.fill();
          ctx.fillStyle = '#06080c'; ctx.font = '700 11px system-ui';
          ctx.fillText(n.collapsed ? '+' + kids.length : '–', n._x + w / 2, n._y + 0.5);
        }
      });
      ctx.restore();
      scanlines(ctx, W, H); vignette(ctx, W, H);
    }
    function loop() { if (!alive) return; t += 0.016; draw(); raf = requestAnimationFrame(loop); }

    function coords(e) {
      var r = canvas.getBoundingClientRect();
      return { x: (e.clientX - r.left) * (W / r.width) - pan.x, y: (e.clientY - r.top) * (H / r.height) - pan.y,
               px: (e.clientX - r.left) * (W / r.width), py: (e.clientY - r.top) * (H / r.height) };
    }
    var panning = null, panMoved = false;
    function onDown(e) { var p = coords(e); panning = { x: p.px, y: p.py }; panMoved = false; }
    function onMove(e) {
      if (!panning) return;
      var r = canvas.getBoundingClientRect();
      var px = (e.clientX - r.left) * (W / r.width), py = (e.clientY - r.top) * (H / r.height);
      if (Math.abs(px - panning.x) + Math.abs(py - panning.y) > 4) panMoved = true;
      pan.x += px - panning.x; pan.y += py - panning.y;
      panning = { x: px, y: py };
      if (RM) draw();
    }
    function onUp(e) {
      var wasPan = panMoved; panning = null;
      if (wasPan) return;
      var p = coords(e);
      for (var i = placed.length - 1; i >= 0; i--) {
        var n = placed[i];
        if (Math.abs(p.x - n._x) <= n._w / 2 + 8 && Math.abs(p.y - n._y) <= 17) {
          if ((n.children || []).length) { n.collapsed = !n.collapsed; layout(); if (RM) draw(); }
          if (opts.onNode) opts.onNode(n);
          return;
        }
      }
    }
    canvas.addEventListener('pointerdown', onDown);
    canvas.addEventListener('pointermove', onMove);
    canvas.addEventListener('pointerup', onUp);

    ctx.font = '600 11.5px system-ui, sans-serif';
    layout();
    if (!RM) raf = requestAnimationFrame(loop); else draw();
    return {
      relayout: function () { layout(); if (RM) draw(); },
      expandAll: function () { (function w(n) { n.collapsed = false; (n.children || []).forEach(w); })(root); layout(); if (RM) draw(); },
      destroy: function () {
        alive = false; cancelAnimationFrame(raf);
        canvas.removeEventListener('pointerdown', onDown);
        canvas.removeEventListener('pointermove', onMove);
        canvas.removeEventListener('pointerup', onUp);
      }
    };
  }

  g.NoahViz = { anatomy: anatomy, flow: flow, topology: topology, graph: graph, mindmap: mindmap, version: 2 };
})(typeof window !== 'undefined' ? window : this);
