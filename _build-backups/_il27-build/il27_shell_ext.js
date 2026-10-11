
/* =====================================================================
 * IL-27 extension — IT Infrastructure Specialist: Zero Trust Infrastructure Mastery.
 *
 * Everything below is scoped to courseId
 * 'il-27-it-infrastructure-specialist-threatlocker-mastery' and must not alter
 * rendering for any other course. All state uses the existing Progress
 * system (localStorage ilc:<courseId>:<key> + /api/progress sync).
 *
 * Framing: independent preparation and practice material. Not affiliated with,
 * endorsed by, or sponsored by any vendor named herein; confers no
 * certification. No vendor text is reproduced.
 * ===================================================================== */
function isIL27() {
  return typeof COURSE !== 'undefined' && COURSE &&
    COURSE.courseId === 'il-27-it-infrastructure-specialist-threatlocker-mastery';
}

/* ---- normCourse wrapper: carry IL-27 top-level keys through ---- */
var _il27_normCourse = normCourse;
normCourse = function (raw) {
  var c = _il27_normCourse(raw);
  if (raw && raw.courseId === 'il-27-it-infrastructure-specialist-threatlocker-mastery') {
    ['fastTrack', 'mathLab', 'scriptingLab', 'animations', 'installLabs', 'toolLabs',
     'branchingScenarios', 'clickSims', 'studyGuide', 'dossier', 'dossierUrl',
     'interactivityAudit', 'jdMatrix'].forEach(function (k) {
      if (raw[k] !== undefined) c[k] = raw[k];
    });
  }
  return c;
};

/* ============================== Fast Track tab ============================== */
var il27CdTimer = null;

function il27CountdownTick(host, targetMs) {
  var now = Date.now();
  var diff = Math.max(0, targetMs - now);
  var d = Math.floor(diff / 86400000);
  var h = Math.floor(diff % 86400000 / 3600000);
  var m = Math.floor(diff % 3600000 / 60000);
  var s = Math.floor(diff % 60000 / 1000);
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  host.innerHTML =
    '<div class="il27-cd-grid">' +
    '<div class="il27-cd-cell"><b>' + d + '</b><span>days</span></div>' +
    '<div class="il27-cd-cell"><b>' + pad(h) + '</b><span>hours</span></div>' +
    '<div class="il27-cd-cell"><b>' + pad(m) + '</b><span>min</span></div>' +
    '<div class="il27-cd-cell"><b>' + pad(s) + '</b><span>sec</span></div>' +
    '</div>' +
    (diff <= 0 ? '<p class="small"><b>Interview time.</b> Breathe, walk in with your 60-second answers ready.</p>'
               : '<p class="small muted">Until the interview · ' + esc(new Date(targetMs).toString()) + '</p>');
}

function il27BuildFastTrack(root) {
  var ft = COURSE.fastTrack || {};
  var targetMs = new Date(ft.interviewDate || '2026-10-13T09:00:00-04:00').getTime();
  root.innerHTML = heroHTML() +
    '<div class="card il27-countdown"><h2>Interview countdown</h2>' +
    '<div class="il27-cd" data-cd></div>' +
    (ft.interviewDayNote ? '<p class="small muted">' + esc(ft.interviewDayNote) + '</p>' : '') +
    '</div>' +
    '<h2 class="section-title">' + esc(ft.title || '6-day interview fast track') + '</h2>' +
    '<p class="section-sub">' + esc(ft.framing || '') + '</p>' +
    '<div id="il27-ft-days"></div>' +
    '<h2 class="section-title">Fast-track modules</h2>' +
    '<p class="section-sub">Compressed sprint modules for the interview week — quiz-first, cards-second. ' +
    'Day plans above tell you which to take each day.</p>' +
    '<div id="il27-ft-mods"></div>' +
    '<div id="il27-ft-noah"></div>';

  var cdHost = root.querySelector('[data-cd]');
  function tick() {
    if (!document.body.contains(cdHost)) { return; }
    il27CountdownTick(cdHost, targetMs);
  }
  if (il27CdTimer) { try { clearInterval(il27CdTimer); } catch (e) {} }
  tick();
  il27CdTimer = setInterval(tick, 1000);

  var daysEl = $('#il27-ft-days', root);
  (ft.plan || []).forEach(function (d) {
    var card = el('div', 'card');
    card.innerHTML = '<h3>Day ' + esc(String(d.day)) + ' — ' + esc(d.theme || '') + '</h3>' +
      '<p class="small muted">' + esc(d.date || '') + ' · ' + esc(String(d.minutes || '')) + ' min planned</p>' +
      '<ul class="obj-list">' + (d.tasks || []).map(function (t) {
        return '<li>' + esc(t) + '</li>';
      }).join('') + '</ul>' +
      ((d.modules || []).length ? '<p class="small"><b>Modules:</b> ' +
        d.modules.map(function (mid) { return '<span class="mono">' + esc(mid) + '</span>'; }).join(', ') + '</p>' : '') +
      (d.questionBank ? '<p class="small"><b>Question bank:</b> ' + esc(d.questionBank) + '</p>' : '');
    daysEl.appendChild(card);
  });

  var modsEl = $('#il27-ft-mods', root);
  var ftMods = (COURSE.modules || []).filter(function (m) { return m.fastTrack; })
    .sort(function (a, b) { return (a.fastTrackDay || 0) - (b.fastTrackDay || 0); });
  if (!ftMods.length) {
    modsEl.appendChild(el('div', 'card', '<p class="muted">No fast-track modules shipped in this course document.</p>'));
  } else {
    ftMods.forEach(function (m) { modsEl.appendChild(moduleHTML(m)); });
  }
  $('#il27-ft-noah', root).appendChild(noahPanel('Fast Track — ' + COURSE.title, COURSE.title));
}

/* ============================== Objectives tab ============================== */
var IL27_MASTERY_LEVELS = ['Not started', 'Developing', 'Proficient', 'Mastery'];

function il27BuildObjectives(root) {
  var objs = COURSE.objectives || [];
  root.innerHTML = heroHTML() +
    '<h2 class="section-title">Objectives</h2>' +
    '<p class="section-sub">Rate your mastery per course objective. Ratings persist on this device ' +
    'and feed the mastery signals below — re-rate after each study block.</p>' +
    '<div class="card" id="il27-obj-sum"></div>' +
    '<div id="il27-obj-list"></div>';

  var listEl = $('#il27-obj-list', root);
  var sumEl = $('#il27-obj-sum', root);

  function getLevel(i) {
    var v = parseInt(Progress.get('obj27:' + i, '0'), 10);
    return isNaN(v) ? 0 : Math.min(3, Math.max(0, v));
  }

  function renderSummary() {
    var counts = [0, 0, 0, 0];
    objs.forEach(function (_, i) { counts[getLevel(i)]++; });
    var total = objs.length || 1;
    var score = objs.reduce(function (s, _, i) { return s + getLevel(i); }, 0) / (total * 3);
    sumEl.innerHTML = '<h3>Mastery signals</h3>' +
      '<div class="il27-obj-bars">' +
      IL27_MASTERY_LEVELS.map(function (label, li) {
        var pct = Math.round(counts[li] / total * 100);
        return '<div class="il27-obj-bar"><span class="il27-obj-bar-label">' + esc(label) + '</span>' +
          '<div class="il27-obj-bar-track"><div class="il27-obj-bar-fill il27-lvl-' + li + '" style="width:' + pct + '%"></div></div>' +
          '<span class="il27-obj-bar-n">' + counts[li] + '/' + total + '</span></div>';
      }).join('') + '</div>' +
      '<p class="small muted">Overall objective mastery: <b>' + Math.round(score * 100) + '%</b> · ' +
      counts[3] + ' objectives at Mastery.</p>';
  }

  objs.forEach(function (o, i) {
    var card = el('div', 'card il27-obj-card');
    var btns = el('div', 'btn-row il27-obj-btns');
    function paint() {
      var lvl = getLevel(i);
      card.innerHTML = '<h3>Objective ' + (i + 1) + '</h3><p>' + esc(typeof o === 'string' ? o : (o.title || o.text || '')) + '</p>';
      card.appendChild(btns);
      btns.innerHTML = '';
      IL27_MASTERY_LEVELS.forEach(function (label, li) {
        var b = el('button', 'btn' + (li === lvl ? ' primary' : ''), esc(label));
        b.type = 'button';
        b.setAttribute('aria-pressed', li === lvl ? 'true' : 'false');
        b.addEventListener('click', function () {
          Progress.set('obj27:' + i, String(li));
          paint();
          renderSummary();
        });
        btns.appendChild(b);
      });
      var note = el('p', 'small muted', 'Current signal: <b>' + esc(IL27_MASTERY_LEVELS[getLevel(i)]) + '</b>');
      card.appendChild(note);
    }
    paint();
    listEl.appendChild(card);
  });
  renderSummary();
}

/* ================== Adaptive lab engines (mathLab + scriptingLab) ==================
 * Knowledge check → personalized path → mastery progression → re-checks → mastery map.
 * All state via Progress (localStorage ilc:<courseId>:<key> + /api/progress sync).
 */
var IL27_LAB_LEVELS = ['novice', 'developing', 'proficient', 'mastery'];
var IL27_LAB_LEVEL_LABELS = ['Novice', 'Developing', 'Proficient', 'Mastery'];

function il27NormAnswer(s) {
  return String(s == null ? '' : s).trim().toLowerCase().replace(/\s+/g, ' ').replace(/^0b/, '').replace(/^0x/, '');
}

function il27Shuffle(arr) {
  var a = arr.slice();
  for (var i = a.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var t = a[i]; a[i] = a[j]; a[j] = t;
  }
  return a;
}

/* Instantiate parameterized generators (range-int + option variables; notEqual honored).
 * Auto-checkable only for binary/decimal/hex conversion templates; other topics practice from the bank. */
function il27InstantiateGenerator(gen) {
  var vars = gen.variables || {};
  var vals = {};
  var keys = Object.keys(vars);
  for (var i = 0; i < keys.length; i++) {
    var k = keys[i], spec = vars[k];
    if (spec.range && spec.type === 'int') {
      vals[k] = spec.range[0] + Math.floor(Math.random() * (spec.range[1] - spec.range[0] + 1));
    } else if (spec.options) {
      var opts = spec.options.slice();
      if (spec.notEqual && vals[spec.notEqual] !== undefined) {
        opts = opts.filter(function (o) { return o !== vals[spec.notEqual]; });
      }
      vals[k] = opts[Math.floor(Math.random() * opts.length)];
    } else {
      return null;
    }
  }
  var q = gen.template || '';
  keys.forEach(function (k) { q = q.split('{' + k + '}').join(String(vals[k])); });
  return { q: q, vals: vals, id: gen.id };
}

function il27SolveConversion(inst) {
  var v = inst.vals;
  if (v.value === undefined || !v.from_base || !v.to_base) return null;
  var n;
  if (v.from_base === 'binary') { n = parseInt(String(v.value), 10); n = il27BinDigitsToInt(n); }
  else if (v.from_base === 'decimal') { n = v.value; }
  else if (v.from_base === 'hex') { n = parseInt(String(v.value), 16); }
  else return null;
  if (isNaN(n)) return null;
  if (v.to_base === 'binary') return n.toString(2);
  if (v.to_base === 'decimal') return String(n);
  if (v.to_base === 'hex') return n.toString(16).toUpperCase();
  return null;
}

function il27BinDigitsToInt(digits) {
  var s = String(digits), n = 0;
  for (var i = 0; i < s.length; i++) { n = n * 2 + (s[i] === '1' ? 1 : 0); }
  return n;
}

function il27AdaptiveLab(host, lab) {
  var eng = String(lab.engine || lab.id || 'lab').replace(/[^a-z0-9-]/gi, '').toLowerCase();
  var topics = lab.topics || [];
  var kc = lab.knowledgeCheck || [];
  var bank = lab.exerciseBank || {};
  var gens = lab.generators || [];

  var PK = 'alab:' + eng + ':';
  function mapGet() { var m = {}; try { m = JSON.parse(Progress.get(PK + 'map', '{}')); } catch (e) {} return m; }
  function mapSet(m) { Progress.set(PK + 'map', JSON.stringify(m)); }
  function tState(m, tid) {
    return m[tid] || { level: 0, streak: 0, attempts: 0, correct: 0, lastRecheck: null };
  }
  function kcGet() { var m = {}; try { m = JSON.parse(Progress.get(PK + 'kc', '{}')); } catch (e) {} return m; }
  function kcSet(m) { Progress.set(PK + 'kc', JSON.stringify(m)); }

  var card = el('div', 'card il27-alab');
  card.innerHTML = '<h3>' + esc(lab.title || 'Adaptive lab') + '</h3>' +
    '<p class="small muted">Knowledge check → personalized path → mastery progression → re-checks → mastery map. ' +
    'Progress persists on this device.</p>' +
    '<div class="btn-row il27-alab-nav" role="tablist" aria-label="Adaptive lab stages"></div>' +
    '<div class="il27-alab-body"></div>';
  host.appendChild(card);
  var nav = card.querySelector('.il27-alab-nav');
  var body = card.querySelector('.il27-alab-body');

  var stages = [
    { id: 'check', label: '1 · Knowledge check' },
    { id: 'path', label: '2 · My path' },
    { id: 'practice', label: '3 · Practice' },
    { id: 'map', label: '4 · Mastery map' }
  ];
  var active = 'check';
  var pathOrder = [];
  var practiceIdx = 0;

  stages.forEach(function (st, si) {
    var b = el('button', 'btn' + (si === 0 ? ' on' : ''), esc(st.label));
    b.type = 'button'; b.setAttribute('role', 'tab');
    b.addEventListener('click', function () {
      active = st.id;
      Array.prototype.forEach.call(nav.children, function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      renderStage();
    });
    nav.appendChild(b);
  });

  function topicById(tid) {
    for (var i = 0; i < topics.length; i++) if (topics[i].id === tid) return topics[i];
    return { id: tid, title: tid };
  }

  /* ---------- stage 1: knowledge check ---------- */
  function renderCheck() {
    body.innerHTML = '';
    if (!kc.length) {
      body.appendChild(el('p', 'muted', 'No knowledge-check questions shipped for this lab.'));
      return;
    }
    var saved = kcGet();
    var answers = {};
    kc.forEach(function (q, qi) {
      var wrap = el('div', 'il27-q');
      wrap.innerHTML = '<p><b>Q' + (qi + 1) + '.</b> ' + esc(q.q) +
        ' <span class="muted small">[' + esc(q.topic || 'general') + ']</span></p>';
      var opts = el('div', 'il27-opts');
      (q.choices || []).forEach(function (ch) {
        var b = el('button', 'btn', esc(ch));
        b.type = 'button';
        b.addEventListener('click', function () {
          answers[qi] = ch;
          Array.prototype.forEach.call(opts.children, function (x) { x.classList.remove('on'); });
          b.classList.add('on');
        });
        opts.appendChild(b);
      });
      wrap.appendChild(opts);
      body.appendChild(wrap);
    });
    var sub = el('button', 'btn primary', 'Score my knowledge check');
    sub.type = 'button';
    var out = el('div', 'il27-kc-out');
    sub.addEventListener('click', function () {
      var per = {}, shown = 0, right = 0;
      kc.forEach(function (q, qi) {
        var t = q.topic || 'general';
        per[t] = per[t] || { right: 0, total: 0 };
        per[t].total++;
        var ok = il27NormAnswer(answers[qi]) === il27NormAnswer(q.answer);
        if (ok) { per[t].right++; right++; }
        shown++;
      });
      kcSet(per);
      var order = Object.keys(per).sort(function (a, b) {
        var sa = per[a].right / per[a].total, sb = per[b].right / per[b].total;
        return sa - sb;
      });
      pathOrder = order;
      Progress.set(PK + 'path', JSON.stringify(order));
      out.innerHTML = '<div class="card"><h3>Result: ' + right + '/' + shown + '</h3>' +
        '<ul class="obj-list">' + Object.keys(per).map(function (t) {
          var p = per[t], pct = Math.round(p.right / p.total * 100);
          return '<li><b>' + esc(topicById(t).title) + '</b>: ' + p.right + '/' + p.total +
            ' (' + pct + '%)</li>';
        }).join('') + '</ul>' +
        '<p class="small">Your personalized path (weakest first): <b>' +
        order.map(function (t) { return esc(topicById(t).title); }).join(' → ') + '</b>. ' +
        'Head to <b>2 · My path</b> to start practicing.</p></div>';
    });
    body.appendChild(sub);
    body.appendChild(out);
  }

  /* ---------- stage 2: personalized path ---------- */
  function renderPath() {
    body.innerHTML = '';
    var per = kcGet();
    var order = pathOrder.length ? pathOrder : (function () {
      try { return JSON.parse(Progress.get(PK + 'path', '[]')); } catch (e) { return []; }
    })();
    if (!order.length) {
      order = topics.map(function (t) { return t.id; });
    }
    var intro = el('p', 'small muted',
      'Practice order is personalized: weakest knowledge-check topics first, strongest last. ' +
      'Complete a topic to unlock the next. Promotion: 8 consecutive correct answers moves a topic up one level.');
    body.appendChild(intro);
    var map = mapGet();
    order.forEach(function (tid, idx) {
      var st = tState(map, tid);
      var t = topicById(tid);
      var sc = per[tid];
      var row = el('div', 'il27-path-row');
      row.innerHTML = '<div><b>' + (idx + 1) + '. ' + esc(t.title) + '</b>' +
        '<div class="small muted">' + esc(t.description || '') + '</div>' +
        (sc ? '<div class="small">Knowledge check: ' + sc.right + '/' + sc.total + '</div>' : '') + '</div>' +
        '<div class="small"><span class="il27-lvl-pill il27-lvl-' + st.level + '">' +
        esc(IL27_LAB_LEVEL_LABELS[st.level]) + '</span></div>';
      var go = el('button', 'btn', 'Practice');
      go.type = 'button';
      go.addEventListener('click', function () {
        practiceIdx = 0;
        active = 'practice';
        Array.prototype.forEach.call(nav.children, function (x, xi) { x.classList.toggle('on', xi === 2); });
        renderStage();
      });
      row.appendChild(go);
      body.appendChild(row);
    });
    if (!order.length) body.appendChild(el('p', 'muted', 'No topics shipped for this lab.'));
  }

  /* ---------- stage 3: practice with mastery progression ---------- */
  function buildQueue(tid) {
    var q = [];
    (bank[tid] || []).forEach(function (e) {
      q.push({ q: e.q, answer: e.answer, steps: e.solutionSteps || [], kind: 'bank' });
    });
    gens.forEach(function (g) {
      if (g.topic !== tid) return;
      for (var i = 0; i < 4; i++) {
        var inst = il27InstantiateGenerator(g);
        if (!inst) continue;
        var sol = il27SolveConversion(inst);
        if (sol === null) continue;
        q.push({ q: inst.q, answer: sol, steps: ['Solve via decimal as the pivot, then convert to the target base.'], kind: 'generated' });
      }
    });
    return il27Shuffle(q);
  }

  function renderPractice() {
    body.innerHTML = '';
    var per = kcGet();
    var order = pathOrder.length ? pathOrder : (function () {
      try { return JSON.parse(Progress.get(PK + 'path', '[]')); } catch (e) { return []; }
    })();
    if (!order.length) order = topics.map(function (t) { return t.id; });
    if (!order.length) { body.appendChild(el('p', 'muted', 'No topics to practice.')); return; }

    var tid = order[Math.min(practiceIdx, order.length - 1)];
    var t = topicById(tid);
    var map = mapGet();
    var st = tState(map, tid);

    var head = el('div', 'card');
    head.innerHTML = '<h3>Practicing: ' + esc(t.title) + '</h3>' +
      '<p class="small muted">' + esc(t.description || '') + '</p>' +
      '<p class="small">Level: <span class="il27-lvl-pill il27-lvl-' + st.level + '">' +
      esc(IL27_LAB_LEVEL_LABELS[st.level]) + '</span> · streak <b>' + st.streak +
      '</b>/8 · attempts <b>' + st.attempts + '</b></p>' +
      '<div class="btn-row">' +
      '<button class="btn" data-prev type="button">← Prev topic</button>' +
      '<button class="btn" data-next type="button">Next topic →</button></div>';
    body.appendChild(head);
    head.querySelector('[data-prev]').addEventListener('click', function () {
      practiceIdx = (practiceIdx + order.length - 1) % order.length;
      renderPractice();
    });
    head.querySelector('[data-next]').addEventListener('click', function () {
      practiceIdx = (practiceIdx + 1) % order.length;
      renderPractice();
    });

    var queue = buildQueue(tid);
    if (!queue.length) {
      body.appendChild(el('p', 'muted', 'No practice exercises shipped for this topic yet.'));
      return;
    }
    var qi = 0;
    var exWrap = el('div', 'il27-ex');
    body.appendChild(exWrap);

    function renderExercise() {
      var item = queue[qi % queue.length];
      exWrap.innerHTML = '<div class="card"><p><b>Exercise ' + ((qi % queue.length) + 1) + '/' +
        queue.length + '</b> <span class="muted small">(' + esc(item.kind) + ')</span></p>' +
        '<p>' + esc(item.q) + '</p>' +
        '<div class="il27-ex-row"><input type="text" data-ans aria-label="Your answer" ' +
        'placeholder="Type your answer…">' +
        '<button class="btn primary" data-check type="button">Check</button></div>' +
        '<div data-fb></div></div>';
      var input = exWrap.querySelector('[data-ans]');
      var fb = exWrap.querySelector('[data-fb]');
      function check() {
        var ok = il27NormAnswer(input.value) === il27NormAnswer(item.answer);
        var m2 = mapGet();
        var s2 = tState(m2, tid);
        s2.attempts++;
        var promoted = false;
        if (ok) {
          s2.correct++; s2.streak++;
          if (s2.streak >= 8 && s2.level < 3) {
            s2.level++; s2.streak = 0; promoted = true;
          }
        } else {
          s2.streak = 0;
        }
        m2[tid] = s2;
        mapSet(m2);
        fb.innerHTML = '<p class="' + (ok ? 'il27-ok' : 'il27-bad') + '">' +
          (ok ? '✓ Correct.' : '✗ Not quite — accepted answer: <b>' + esc(item.answer) + '</b>.') +
          (promoted ? ' <b>Promoted to ' + esc(IL27_LAB_LEVEL_LABELS[s2.level]) + '!</b>' : '') + '</p>' +
          (item.steps.length ? '<ol class="small">' + item.steps.map(function (x) {
            return '<li>' + esc(x) + '</li>';
          }).join('') + '</ol>' : '') +
          '<div class="btn-row"><button class="btn" data-nx type="button">Next exercise →</button></div>';
        fb.querySelector('[data-nx]').addEventListener('click', function () {
          qi++;
          renderPracticeQueueOnly();
        });
        function renderPracticeQueueOnly() { renderPractice(); }
      }
      exWrap.querySelector('[data-check]').addEventListener('click', check);
      input.addEventListener('keydown', function (e) { if (e.key === 'Enter') check(); });
      try { input.focus(); } catch (e) {}
    }
    renderExercise();

    /* re-check for proficient+ topics */
    if (st.level >= 2) {
      var rc = el('div', 'card');
      rc.innerHTML = '<h3>Spaced re-check</h3><p class="small muted">This topic is ' +
        esc(IL27_LAB_LEVEL_LABELS[st.level]) + '. Answer 3 questions to confirm it sticks — ' +
        'a miss drops the topic one level and queues remedial practice.</p>' +
        '<button class="btn" data-rc type="button">Start re-check (3 questions)</button><div data-rcb></div>';
      body.appendChild(rc);
      rc.querySelector('[data-rc]').addEventListener('click', function () {
        var pool = [];
        kc.forEach(function (q) { if ((q.topic || 'general') === tid) pool.push(q); });
        (bank[tid] || []).forEach(function (e) { pool.push({ q: e.q, answer: e.answer, choices: null }); });
        pool = il27Shuffle(pool).slice(0, 3);
        var host2 = rc.querySelector('[data-rcb]');
        host2.innerHTML = '';
        if (!pool.length) { host2.appendChild(el('p', 'muted', 'No re-check questions available for this topic.')); return; }
        var ri = 0, rRight = 0;
        function renderR() {
          if (ri >= pool.length) {
            var m3 = mapGet();
            var s3 = tState(m3, tid);
            if (rRight === pool.length) {
              s3.lastRecheck = new Date().toISOString();
              host2.innerHTML = '<p class="il27-ok">✓ Re-check passed (' + rRight + '/' + pool.length +
                '). Level holds.</p>';
            } else {
              s3.level = Math.max(0, s3.level - 1);
              s3.streak = 0;
              host2.innerHTML = '<p class="il27-bad">✗ Re-check: ' + rRight + '/' + pool.length +
                ' — dropped to <b>' + esc(IL27_LAB_LEVEL_LABELS[s3.level]) +
                '</b>. Practice the topic again to climb back.</p>';
            }
            m3[tid] = s3;
            mapSet(m3);
            return;
          }
          var item = pool[ri];
          var w = el('div', 'il27-q');
          w.innerHTML = '<p><b>Re-check ' + (ri + 1) + '/3.</b> ' + esc(item.q) + '</p>';
          if (item.choices && item.choices.length) {
            var opts = el('div', 'il27-opts');
            item.choices.forEach(function (ch) {
              var b = el('button', 'btn', esc(ch));
              b.type = 'button';
              b.addEventListener('click', function () {
                if (il27NormAnswer(ch) === il27NormAnswer(item.answer)) rRight++;
                ri++;
                renderR();
              });
              opts.appendChild(b);
            });
            w.appendChild(opts);
          } else {
            w.innerHTML += '<div class="il27-ex-row"><input type="text" data-ra aria-label="Your answer">' +
              '<button class="btn primary" data-rb type="button">Check</button></div>';
            w.querySelector('[data-rb]').addEventListener('click', function () {
              if (il27NormAnswer(w.querySelector('[data-ra]').value) === il27NormAnswer(item.answer)) rRight++;
              ri++;
              renderR();
            });
          }
          host2.innerHTML = '';
          host2.appendChild(w);
        }
        renderR();
      });
    }
  }

  /* ---------- stage 4: mastery map ---------- */
  function renderMap() {
    body.innerHTML = '';
    var map = mapGet();
    var per = kcGet();
    var grid = el('div', 'il27-heat');
    topics.forEach(function (t) {
      var st = tState(map, t.id);
      var sc = per[t.id];
      var cell = el('div', 'il27-heat-cell il27-lvl-' + st.level);
      cell.innerHTML = '<b>' + esc(t.title) + '</b>' +
        '<span>' + esc(IL27_LAB_LEVEL_LABELS[st.level]) + '</span>' +
        '<span class="small">streak ' + st.streak + ' · ' + st.attempts + ' attempts</span>' +
        (sc ? '<span class="small">KC ' + sc.right + '/' + sc.total + '</span>' : '');
      grid.appendChild(cell);
    });
    body.appendChild(grid);
    var mastered = topics.filter(function (t) { return tState(map, t.id).level >= 3; }).length;
    body.appendChild(el('p', 'small muted',
      mastered + '/' + topics.length + ' topics at Mastery. The engine always serves your weakest ' +
      'topic first (70/30 weak/strong mix). Export your map any time:'));
    var exp = el('button', 'btn', 'Copy mastery map JSON');
    exp.type = 'button';
    exp.addEventListener('click', function () {
      var txt = JSON.stringify({ engine: eng, updatedAt: new Date().toISOString(), map: mapGet() }, null, 1);
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(txt);
          exp.textContent = '✓ Copied';
        }
      } catch (e) {}
    });
    body.appendChild(exp);
  }

  function renderStage() {
    if (active === 'check') renderCheck();
    else if (active === 'path') renderPath();
    else if (active === 'practice') renderPractice();
    else renderMap();
  }
  renderStage();
}

/* ================== IL-27 animation renderers (8 specs) ==================
 * SVG/Canvas interactive visuals: topology, AD tree, Zero Trust flow,
 * DHCP DORA, DNS chain, GPO order, backup rotation, IR lifecycle.
 */
function il27AnimWrap(spec) {
  var w = el('div', 'il27-anim card');
  w.innerHTML = '<h3>' + esc(spec.title || 'Interactive visual') + '</h3>' +
    '<p class="small muted">' + esc(spec.description || '') + '</p>' +
    '<div class="il27-anim-body"></div>';
  return w;
}

function il27SvgTag(w, h, inner) {
  return '<svg viewBox="0 0 ' + w + ' ' + h + '" width="100%" role="img" ' +
    'style="max-width:760px;display:block;margin:0 auto;background:#0e1622;border-radius:8px">' +
    inner + '</svg>';
}

function il27NodeBox(id, x, y, w, h, label, sub, on) {
  return '<g id="' + id + '" class="il27-node' + (on ? ' on' : '') + '">' +
    '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="8" ' +
    'fill="#16202e" stroke="#3a4a5f" stroke-width="2"/>' +
    '<text x="' + (x + w / 2) + '" y="' + (y + h / 2 - 2) + '" text-anchor="middle" ' +
    'fill="#e8eef4" font-size="13" font-weight="600">' + label + '</text>' +
    (sub ? '<text x="' + (x + w / 2) + '" y="' + (y + h / 2 + 15) + '" text-anchor="middle" ' +
      'fill="#8fa3b8" font-size="11">' + sub + '</text>' : '') + '</g>';
}

function il27Wire(x1, y1, x2, y2, id) {
  return '<line ' + (id ? 'id="' + id + '" ' : '') + 'x1="' + x1 + '" y1="' + y1 +
    '" x2="' + x2 + '" y2="' + y2 + '" stroke="#3a4a5f" stroke-width="2"/>';
}

/* Generic step-through player: steps = [{hl:[ids], dim:[ids], caption}]. */
function il27Stepper(body, svgHTML, steps) {
  var idx = 0;
  var stage = el('div', 'il27-anim-stage');
  var cap = el('p', 'small il27-cap');
  var row = el('div', 'btn-row');
  var prev = el('button', 'btn', '← Prev');
  var next = el('button', 'btn primary', 'Next →');
  var ctr = el('span', 'small muted');
  prev.type = 'button'; next.type = 'button';
  row.appendChild(prev); row.appendChild(next); row.appendChild(ctr);
  body.appendChild(stage); body.appendChild(cap); body.appendChild(row);

  function paint() {
    stage.innerHTML = svgHTML;
    var st = steps[idx];
    (st.hl || []).forEach(function (id) {
      var g = stage.querySelector('#' + id);
      if (g) {
        var r = g.querySelector('rect, circle, ellipse');
        if (r) { r.setAttribute('stroke', '#62d8e9'); r.setAttribute('stroke-width', '3'); }
      }
    });
    (st.dim || []).forEach(function (id) {
      var g = stage.querySelector('#' + id);
      if (g) g.setAttribute('opacity', '0.35');
    });
    cap.textContent = (idx + 1) + '/' + steps.length + ' — ' + st.caption;
    ctr.textContent = 'Step ' + (idx + 1) + ' of ' + steps.length;
    prev.disabled = idx === 0;
    next.disabled = idx === steps.length - 1;
  }
  prev.addEventListener('click', function () { if (idx > 0) { idx--; paint(); } });
  next.addEventListener('click', function () { if (idx < steps.length - 1) { idx++; paint(); } });
  paint();
}

/* ---- ANIM-03: Zero Trust request flow (step-through) ---- */
function il27AnimZT(body, spec) {
  var ids = ['a-client', 'a-engine', 'a-ident', 'a-device', 'a-allow', 'a-decide'];
  var labels = [
    ['Workstation', '10.0.1.44'],
    ['Policy engine', 'evaluate'],
    ['Identity', 'MFA check'],
    ['Device posture', 'healthy?'],
    ['Allowlist', 'app allowed?'],
    ['Decision', 'allow / deny']
  ];
  var inner = '';
  labels.forEach(function (L, i) {
    var x = 20 + i * 118;
    inner += il27NodeBox(ids[i], x, 60, 104, 64, L[0], L[1]);
    if (i < labels.length - 1) inner += il27Wire(x + 104, 92, x + 118, 92);
  });
  var steps = [
    { hl: ['a-client'], dim: ids.slice(1), caption: '1 · A user on the LAN workstation requests the file share. Nothing is trusted yet.' },
    { hl: ['a-client', 'a-engine'], dim: ids.slice(2), caption: '2 · The request hits the policy engine — every request is evaluated, every time.' },
    { hl: ['a-engine', 'a-ident'], dim: ids.slice(3), caption: '3 · Identity is verified (MFA, session risk). Identity alone is not enough.' },
    { hl: ['a-ident', 'a-device'], dim: ids.slice(4), caption: '4 · Device posture is checked: patched, encrypted, EDR healthy.' },
    { hl: ['a-device', 'a-allow'], dim: ['a-decide'], caption: '5 · The requested app must be on the explicit allowlist — default deny.' },
    { hl: ['a-decide'], dim: ids.slice(0, 5), caption: '6 · Decision: allow with least privilege, or deny. Logged either way.' }
  ];
  il27Stepper(body, il27SvgTag(740, 180, inner), steps);
}

/* ---- ANIM-04: DHCP DORA sequence ---- */
function il27AnimDORA(body, spec) {
  var inner =
    il27NodeBox('a-pc', 40, 70, 130, 70, 'Client', '00:11:22:33:44:55') +
    il27NodeBox('a-dhcp', 570, 70, 130, 70, 'DHCP server', '10.0.0.5') +
    il27NodeBox('a-p1', 230, 30, 280, 34, 'DISCOVER', 'broadcast → 255.255.255.255') +
    il27NodeBox('a-p2', 230, 74, 280, 34, 'OFFER', 'unicast · offers 10.0.1.100') +
    il27NodeBox('a-p3', 230, 118, 280, 34, 'REQUEST', 'broadcast · "I want 10.0.1.100"') +
    il27NodeBox('a-p4', 230, 162, 280, 34, 'ACK', 'unicast · lease confirmed');
  var all = ['a-pc', 'a-dhcp', 'a-p1', 'a-p2', 'a-p3', 'a-p4'];
  var steps = [
    { hl: ['a-pc', 'a-p1'], dim: ['a-dhcp', 'a-p2', 'a-p3', 'a-p4'], caption: 'D · DISCOVER: the client broadcasts — it has no IP yet, so it shouts to everyone.' },
    { hl: ['a-dhcp', 'a-p2'], dim: ['a-pc', 'a-p1', 'a-p3', 'a-p4'], caption: 'O · OFFER: the server unicasts back an offered address (10.0.1.100) plus options.' },
    { hl: ['a-pc', 'a-p3'], dim: ['a-dhcp', 'a-p1', 'a-p2', 'a-p4'], caption: 'R · REQUEST: the client broadcasts its choice so other servers back off.' },
    { hl: ['a-dhcp', 'a-p4'], dim: ['a-pc', 'a-p1', 'a-p2', 'a-p3'], caption: 'A · ACK: the server confirms the lease. DORA complete — the client now has an address.' }
  ];
  il27Stepper(body, il27SvgTag(740, 220, inner), steps);
}

/* ---- ANIM-05: DNS resolution chain ---- */
function il27AnimDNS(body, spec) {
  var ids = ['a-stub', 'a-fwd', 'a-root', 'a-tld', 'a-auth'];
  var labels = [
    ['Stub resolver', 'workstation'],
    ['pfSense', 'forwarder'],
    ['Root hints', '". " zone'],
    ['TLD', '".com"'],
    ['Authoritative', 'example.com']
  ];
  var inner = '';
  labels.forEach(function (L, i) {
    var x = 20 + i * 142;
    inner += il27NodeBox(ids[i], x, 60, 128, 64, L[0], L[1]);
    if (i < labels.length - 1) inner += il27Wire(x + 128, 92, x + 142, 92);
  });
  inner += '<text x="370" y="170" text-anchor="middle" fill="#8fa3b8" font-size="12">query: files.example.com → answer walks back down the chain</text>';
  var steps = [
    { hl: ['a-stub'], dim: ids.slice(1), caption: '1 · The app asks the stub resolver for files.example.com.' },
    { hl: ['a-stub', 'a-fwd'], dim: ids.slice(2), caption: '2 · The stub forwards to pfSense (the configured forwarder).' },
    { hl: ['a-fwd', 'a-root'], dim: ids.slice(3), caption: '3 · pfSense asks a root server, which refers down: "ask .com".' },
    { hl: ['a-fwd', 'a-tld'], dim: ['a-root', 'a-auth'], caption: '4 · The .com TLD server refers down: "ask example.com\'s nameserver".' },
    { hl: ['a-fwd', 'a-auth'], dim: ['a-root', 'a-tld'], caption: '5 · The authoritative server answers: files.example.com = 93.184.216.34.' },
    { hl: ids, dim: [], caption: '6 · The answer walks back down the chain and is cached at each layer.' }
  ];
  il27Stepper(body, il27SvgTag(760, 200, inner), steps);
}

/* ---- ANIM-02: AD forest / domain tree (click to expand) ---- */
function il27AnimAD(body, spec) {
  var ous = [
    ['ou-ws', 'Workstations', ['WS-FIN-01', 'WS-HR-02']],
    ['ou-srv', 'Servers', ['LAB-DC01', 'LAB-FS01']],
    ['ou-usr', 'Users', ['jdoe', 'asmith']],
    ['ou-grp', 'Groups', ['GG-Finance', 'GG-IT-Admins']],
    ['ou-svc', 'ServiceAccounts', ['svc-backup', 'svc-monitor']]
  ];
  var inner = il27NodeBox('a-root', 300, 20, 160, 60, 'lab.local', 'domain root (click me)');
  ous.forEach(function (o, i) {
    var x = 20 + i * 146;
    inner += '<g id="' + o[0] + '" style="display:none;cursor:pointer">' +
      il27NodeBox(o[0] + '-box', x, 120, 132, 54, o[1], 'OU (click)') +
      o[2].map(function (leaf, li) {
        return '<g id="' + o[0] + '-leaf' + li + '" style="display:none">' +
          '<rect x="' + (x + 6) + '" y="' + (196 + li * 30) + '" width="120" height="24" rx="5" ' +
          'fill="#101826" stroke="#3a4a5f"/>' +
          '<text x="' + (x + 66) + '" y="' + (212 + li * 30) + '" text-anchor="middle" ' +
          'fill="#9fd8e8" font-size="11">' + leaf + '</text></g>';
      }).join('') + '</g>';
    inner += il27Wire(380, 80, x + 66, 120);
  });
  var stage = el('div', 'il27-anim-stage');
  stage.innerHTML = il27SvgTag(760, 300, inner);
  body.appendChild(stage);
  body.appendChild(el('p', 'small muted', 'Click the domain root to expand the five OUs; click an OU to expand its objects.'));
  var rootG = stage.querySelector('#a-root');
  rootG.style.cursor = 'pointer';
  var open = false;
  rootG.addEventListener('click', function () {
    open = !open;
    ous.forEach(function (o) {
      var g = stage.querySelector('#' + o[0]);
      if (g) g.style.display = open ? '' : 'none';
    });
  });
  ous.forEach(function (o) {
    var g = stage.querySelector('#' + o[0]);
    g.addEventListener('click', function (e) {
      e.stopPropagation();
      o[2].forEach(function (_, li) {
        var leaf = stage.querySelector('#' + o[0] + '-leaf' + li);
        if (leaf) leaf.style.display = leaf.style.display === 'none' ? '' : 'none';
      });
    });
  });
}

/* ---- ANIM-06: GPO processing order (LSDOU, later wins) ---- */
function il27AnimGPO(body, spec) {
  var layers = [
    ['L', 'Local', 'Screen-saver timeout = 15 min'],
    ['S', 'Site', 'Screen-saver timeout = 10 min'],
    ['D', 'Domain', 'Screen-saver timeout = 5 min'],
    ['O', 'OU', 'Screen-saver timeout = 2 min']
  ];
  var applied = [];
  var stage = el('div', 'il27-anim-stage');
  var out = el('div', 'card il27-gpo-out');
  var row = el('div', 'btn-row');
  body.appendChild(stage); body.appendChild(row); body.appendChild(out);

  function paint() {
    var inner = '';
    layers.forEach(function (L, i) {
      var on = applied.indexOf(i) !== -1;
      inner += il27NodeBox('a-gpo-' + i, 60, 20 + i * 74, 300, 58,
        L[0] + ' — ' + L[1], L[2].split('= ')[1], on);
      if (on) {
        var r = null;
      }
      if (i < layers.length - 1) inner += il27Wire(210, 78 + i * 74, 210, 94 + i * 74);
    });
    stage.innerHTML = il27SvgTag(420, 330, inner);
    applied.forEach(function (i) {
      var g = stage.querySelector('#a-gpo-' + i + ' rect');
      if (g) { g.setAttribute('stroke', '#62d8e9'); g.setAttribute('stroke-width', '3'); }
    });
    var eff = applied.length ? layers[applied[applied.length - 1]][2] : 'no policies applied yet';
    out.innerHTML = '<h3>Effective setting</h3><p><b>' + esc(eff) + '</b></p>' +
      '<p class="small muted">LSDOU processes Local → Site → Domain → OU. Later layers win on conflict ' +
      '(unless Enforced / Block Inheritance changes the math). Applied so far: ' +
      (applied.length ? applied.map(function (i) { return layers[i][0]; }).join(' → ') : 'none') + '.</p>';
  }
  layers.forEach(function (L, i) {
    var b = el('button', 'btn', 'Apply ' + L[1]);
    b.type = 'button';
    b.addEventListener('click', function () {
      if (applied.indexOf(i) === -1) applied.push(i);
      paint();
    });
    row.appendChild(b);
  });
  var reset = el('button', 'btn', 'Reset');
  reset.type = 'button';
  reset.addEventListener('click', function () { applied = []; paint(); });
  row.appendChild(reset);
  paint();
}

/* ---- ANIM-08: Incident response lifecycle (clickable wheel) ---- */
function il27AnimIR(body, spec) {
  var phases = [
    ['Preparation', 'Playbooks, tooling, and training before anything happens.'],
    ['Detection & Analysis', 'Alerts triage; scope the incident; preserve evidence.'],
    ['Containment', 'Isolate hosts, block C2, stop the bleeding — short and long term.'],
    ['Eradication', 'Remove the attacker foothold: malware, persistence, bad accounts.'],
    ['Recovery', 'Restore systems to production, verify clean, monitor closely.'],
    ['Lessons Learned', 'Blameless postmortem; feed findings back into Preparation.']
  ];
  var cx = 210, cy = 150, R = 105;
  var inner = '';
  var pos = [];
  phases.forEach(function (p, i) {
    var a = -Math.PI / 2 + i * Math.PI * 2 / phases.length;
    var x = cx + R * Math.cos(a), y = cy + R * Math.sin(a);
    pos.push([x, y]);
    var x2 = cx + R * Math.cos(a + Math.PI * 2 / phases.length), y2 = cy + R * Math.sin(a + Math.PI * 2 / phases.length);
    inner += '<line x1="' + x.toFixed(1) + '" y1="' + y.toFixed(1) + '" x2="' + x2.toFixed(1) + '" y2="' + y2.toFixed(1) +
      '" stroke="#3a4a5f" stroke-width="2" marker-end="url(#ilh-arrow)"/>';
  });
  inner = '<defs><marker id="ilh-arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">' +
    '<path d="M0,0 L8,4 L0,8" fill="none" stroke="#3a4a5f" stroke-width="1.5"/></marker></defs>' + inner;
  phases.forEach(function (p, i) {
    var x = pos[i][0], y = pos[i][1];
    inner += '<g id="a-ir-' + i + '" style="cursor:pointer">' +
      '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="34" fill="#16202e" stroke="#3a4a5f" stroke-width="2"/>' +
      '<text x="' + x.toFixed(1) + '" y="' + (y - 4).toFixed(1) + '" text-anchor="middle" fill="#e8eef4" font-size="12" font-weight="700">' + (i + 1) + '</text>' +
      '<text x="' + x.toFixed(1) + '" y="' + (y + 14).toFixed(1) + '" text-anchor="middle" fill="#8fa3b8" font-size="9">' +
      p[0].split(' ')[0] + '</text></g>';
  });
  var stage = el('div', 'il27-anim-stage');
  stage.innerHTML = il27SvgTag(420, 300, inner);
  var desc = el('div', 'card');
  desc.innerHTML = '<h3>Click a phase</h3><p class="small muted">The lifecycle is a loop — Lessons Learned feeds Preparation.</p>';
  body.appendChild(stage); body.appendChild(desc);
  phases.forEach(function (p, i) {
    var g = stage.querySelector('#a-ir-' + i);
    g.addEventListener('click', function () {
      phases.forEach(function (_, j) {
        var c = stage.querySelector('#a-ir-' + j + ' circle');
        if (c) { c.setAttribute('stroke', '#3a4a5f'); c.setAttribute('stroke-width', '2'); }
      });
      var c = stage.querySelector('#a-ir-' + i + ' circle');
      if (c) { c.setAttribute('stroke', '#62d8e9'); c.setAttribute('stroke-width', '3'); }
      desc.innerHTML = '<h3>' + (i + 1) + ' · ' + esc(p[0]) + '</h3><p>' + esc(p[1]) + '</p>';
    });
  });
}

/* ---- ANIM-01: Network topology builder (canvas) ---- */
function il27AnimTopo(body, spec) {
  var TYPES = [
    ['firewall', '#e26d5a'], ['switch', '#62d8e9'], ['server', '#c9a227'],
    ['workstation', '#7fb069'], ['printer', '#9b8cf0'], ['cloud', '#8fa3b8']
  ];
  var sel = 'switch';
  var nodes = [];
  var drag = null;

  var bar = el('div', 'btn-row');
  TYPES.forEach(function (t) {
    var b = el('button', 'btn' + (t[0] === sel ? ' on' : ''), t[0]);
    b.type = 'button';
    b.addEventListener('click', function () {
      sel = t[0];
      Array.prototype.forEach.call(bar.children, function (x) { x.classList.remove('on'); });
      b.classList.add('on');
    });
    bar.appendChild(b);
  });
  var reset = el('button', 'btn', 'Reset');
  reset.type = 'button';
  reset.addEventListener('click', function () { nodes = []; draw(); paintLinks(); });
  bar.appendChild(reset);

  var cv = document.createElement('canvas');
  cv.width = 720; cv.height = 380;
  cv.style.cssText = 'width:100%;max-width:720px;background:#0e1622;border-radius:8px;cursor:crosshair;display:block;margin:8px auto';
  var linksEl = el('p', 'small muted', 'Click the canvas to place the selected device. Drag devices to move them. Links connect devices in placement order.');
  body.appendChild(bar); body.appendChild(cv); body.appendChild(linksEl);

  function colorFor(t) {
    for (var i = 0; i < TYPES.length; i++) if (TYPES[i][0] === t) return TYPES[i][1];
    return '#fff';
  }
  function draw() {
    var ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, cv.width, cv.height);
    ctx.strokeStyle = '#2c3a4d'; ctx.lineWidth = 2;
    for (var i = 1; i < nodes.length; i++) {
      ctx.beginPath();
      ctx.moveTo(nodes[i - 1].x, nodes[i - 1].y);
      ctx.lineTo(nodes[i].x, nodes[i].y);
      ctx.stroke();
    }
    nodes.forEach(function (n) {
      ctx.fillStyle = '#16202e';
      ctx.strokeStyle = colorFor(n.type);
      ctx.lineWidth = 2.5;
      if (n.type === 'cloud') {
        ctx.beginPath(); ctx.ellipse(n.x, n.y, 34, 20, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      } else {
        ctx.beginPath(); ctx.rect(n.x - 30, n.y - 22, 60, 44); ctx.fill(); ctx.stroke();
      }
      ctx.fillStyle = '#e8eef4'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(n.type, n.x, n.y + 4);
    });
  }
  function paintLinks() {
    linksEl.textContent = nodes.length < 2
      ? 'Click the canvas to place the selected device. Drag devices to move them.'
      : nodes.map(function (n) { return n.type; }).join(' → ') + '  (' + (nodes.length - 1) + ' links)';
  }
  function pos(e) {
    var r = cv.getBoundingClientRect();
    return { x: (e.clientX - r.left) * (cv.width / r.width), y: (e.clientY - r.top) * (cv.height / r.height) };
  }
  cv.addEventListener('mousedown', function (e) {
    var p = pos(e);
    for (var i = nodes.length - 1; i >= 0; i--) {
      var n = nodes[i];
      if (Math.abs(p.x - n.x) < 34 && Math.abs(p.y - n.y) < 26) { drag = n; return; }
    }
    nodes.push({ type: sel, x: Math.round(p.x), y: Math.round(p.y) });
    draw(); paintLinks();
  });
  cv.addEventListener('mousemove', function (e) {
    if (!drag) return;
    var p = pos(e);
    drag.x = Math.round(p.x); drag.y = Math.round(p.y);
    draw();
  });
  window.addEventListener('mouseup', function () { if (drag) { drag = null; paintLinks(); } });
  draw();
}

/* ---- ANIM-07: Backup rotation visualizer (canvas GFS calendar) ---- */
function il27AnimBackup(body, spec) {
  var info = el('div', 'card');
  var cv = document.createElement('canvas');
  cv.width = 720; cv.height = 300;
  cv.style.cssText = 'width:100%;max-width:720px;background:#0e1622;border-radius:8px;display:block;margin:8px auto;cursor:pointer';
  body.appendChild(cv);
  body.appendChild(info);

  var cells = [];
  function kindFor(week, dow) {
    if (week === 0 && dow === 0) return ['grandfather', '#c9a227', 'Monthly FULL (grandfather)'];
    if (dow === 0) return ['father', '#62d8e9', 'Weekly FULL (father)'];
    return ['son', '#3f6f7f', 'Daily incremental (son)'];
  }
  function draw() {
    var ctx = cv.getContext('2d');
    ctx.clearRect(0, 0, cv.width, cv.height);
    cells = [];
    var cw = 96, ch = 44, ox = 24, oy = 30;
    var days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    ctx.fillStyle = '#8fa3b8'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
    days.forEach(function (d, i) { ctx.fillText(d, ox + i * cw + cw / 2, oy - 8); });
    for (var w = 0; w < 4; w++) {
      for (var d = 0; d < 7; d++) {
        var x = ox + d * cw, y = oy + w * ch;
        var k = kindFor(w, d);
        ctx.fillStyle = k[1];
        ctx.globalAlpha = 0.85;
        ctx.fillRect(x + 2, y + 2, cw - 4, ch - 4);
        ctx.globalAlpha = 1;
        ctx.fillStyle = '#0e1622'; ctx.font = 'bold 10px sans-serif';
        ctx.fillText(k[0].toUpperCase(), x + cw / 2, y + ch / 2 + 4);
        cells.push({ x: x, y: y, w: cw, h: ch, week: w + 1, dow: days[d], kind: k });
      }
    }
    ctx.fillStyle = '#8fa3b8'; ctx.font = '11px sans-serif'; ctx.textAlign = 'left';
    ctx.fillText('Legend:', 24, 268);
    ctx.fillStyle = '#c9a227'; ctx.fillRect(80, 258, 14, 14);
    ctx.fillStyle = '#8fa3b8'; ctx.fillText('grandfather = monthly full', 100, 269);
    ctx.fillStyle = '#62d8e9'; ctx.fillRect(260, 258, 14, 14);
    ctx.fillStyle = '#8fa3b8'; ctx.fillText('father = weekly full', 280, 269);
    ctx.fillStyle = '#3f6f7f'; ctx.fillRect(420, 258, 14, 14);
    ctx.fillStyle = '#8fa3b8'; ctx.fillText('son = daily incremental', 440, 269);
  }
  function paintInfo(week, dow, kind) {
    info.innerHTML = '<h3>Week ' + week + ' · ' + dow + '</h3><p><b>' + esc(kind[2]) + '</b></p>' +
      '<p class="small muted">Grandfather-Father-Son: daily incrementals (sons) ride on weekly fulls (fathers), ' +
      'which ride on monthly fulls (grandfathers). Restores walk the chain: latest full + incrementals since. ' +
      'Retention example: 7 daily, 4 weekly, 12 monthly.</p>';
  }
  cv.addEventListener('click', function (e) {
    var r = cv.getBoundingClientRect();
    var x = (e.clientX - r.left) * (cv.width / r.width), y = (e.clientY - r.top) * (cv.height / r.height);
    for (var i = 0; i < cells.length; i++) {
      var c = cells[i];
      if (x >= c.x && x <= c.x + c.w && y >= c.y && y <= c.y + c.h) {
        paintInfo(c.week, c.dow, c.kind);
        return;
      }
    }
  });
  draw();
  paintInfo(1, 'Mon', kindFor(0, 0));
}

function il27RenderAnimation(spec) {
  var wrap = il27AnimWrap(spec);
  var body = wrap.querySelector('.il27-anim-body');
  try {
    if (spec.id === 'IL27-ANIM-01') il27AnimTopo(body, spec);
    else if (spec.id === 'IL27-ANIM-02') il27AnimAD(body, spec);
    else if (spec.id === 'IL27-ANIM-03') il27AnimZT(body, spec);
    else if (spec.id === 'IL27-ANIM-04') il27AnimDORA(body, spec);
    else if (spec.id === 'IL27-ANIM-05') il27AnimDNS(body, spec);
    else if (spec.id === 'IL27-ANIM-06') il27AnimGPO(body, spec);
    else if (spec.id === 'IL27-ANIM-07') il27AnimBackup(body, spec);
    else if (spec.id === 'IL27-ANIM-08') il27AnimIR(body, spec);
    else body.appendChild(el('p', 'muted', 'No renderer for animation spec ' + spec.id + '.'));
  } catch (e) {
    body.appendChild(el('p', 'muted', 'This visual failed to render: ' + String(e && e.message || e)));
  }
  return wrap;
}

/* ================== module hook: attach animations ================== */
var _il27_moduleHTML = moduleHTML;
moduleHTML = function (m) {
  var w = _il27_moduleHTML(m);
  if (!isIL27()) return w;
  var anims = (COURSE.animations || []).filter(function (a) { return a.moduleId === m.id; });
  if (!anims.length) return w;
  var body = w.querySelector('.mod-body');
  if (!body) return w;
  body.appendChild(el('h3', '', 'Interactive visuals'));
  anims.forEach(function (a) { body.appendChild(il27RenderAnimation(a)); });
  return w;
};

/* ================== extra lab sections for IL-27 ================== */
function il27InstallLabCard(lab) {
  var card = el('div', 'card');
  var cps = lab.checkpoints || [];
  var inner = '<h3>' + esc(lab.tool || lab.id) + '</h3>' +
    '<p class="small muted">' + esc(lab.category || '') +
    (lab.estimatedMinutes ? ' · ' + lab.estimatedMinutes + ' min' : '') + '</p>' +
    '<p class="small"><b>Platforms:</b> ' + esc((lab.platforms || []).join(', ')) + '</p>' +
    ((lab.gates || []).length ? '<p class="small"><b>Gate:</b> ' + esc(lab.gates.join(' · ')) + '</p>' : '') +
    (lab.costNote ? '<p class="small muted">' + esc(lab.costNote) + '</p>' : '') +
    '<h4 class="section-title" style="font-size:0.9em">Checkpoints</h4><ul class="obj-list">';
  card.innerHTML = inner + '</ul>';
  var ul = card.querySelector('ul');
  cps.forEach(function (cp, i) {
    var li = document.createElement('li');
    var key = 'install:' + lab.id + ':cp:' + i;
    var done = Progress.get(key) === '1';
    var cb = document.createElement('input');
    cb.type = 'checkbox'; cb.checked = done;
    cb.setAttribute('aria-label', 'Checkpoint ' + (i + 1));
    var span = el('span', '', esc(cp));
    if (done) span.style.textDecoration = 'line-through';
    cb.addEventListener('change', function () {
      Progress.set(key, cb.checked ? '1' : null);
      span.style.textDecoration = cb.checked ? 'line-through' : '';
    });
    li.appendChild(cb); li.appendChild(document.createTextNode(' ')); li.appendChild(span);
    ul.appendChild(li);
  });
  if ((lab.troubleshoot || []).length) {
    card.appendChild(el('h4', 'section-title', 'Troubleshooting'));
    var tb = el('ul', 'obj-list small');
    lab.troubleshoot.forEach(function (t) { tb.appendChild(el('li', '', esc(t))); });
    card.appendChild(tb);
  }
  return card;
}

function il27ToolLabCard(lab) {
  var card = el('div', 'card');
  var done = Progress.get('toollab:' + lab.id) === '1';
  card.innerHTML = '<h3>' + esc(lab.title || lab.id) + '</h3>' +
    '<p class="small muted">' + esc(lab.brief || '') + '</p>' +
    ((lab.requiresInstall || lab.requiresLab) ?
      '<p class="small"><b>Requires:</b> ' + esc([lab.requiresInstall, lab.requiresLab].filter(Boolean).join(' + ')) + '</p>' : '') +
    '<ol class="small">' + (lab.steps || []).map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('') + '</ol>' +
    (lab.deliverable ? '<p class="small"><b>Deliverable:</b> ' + esc(lab.deliverable) + '</p>' : '') +
    (lab.checkpoint ? '<p class="small"><b>Checkpoint:</b> ' + esc(lab.checkpoint) + '</p>' : '');
  var b = el('button', 'btn' + (done ? '' : ' primary'), done ? '✓ Complete' : 'Mark complete');
  b.type = 'button';
  b.addEventListener('click', function () {
    var now = !(Progress.get('toollab:' + lab.id) === '1');
    Progress.set('toollab:' + lab.id, now ? '1' : null);
    b.textContent = now ? '✓ Complete' : 'Mark complete';
    b.classList.toggle('primary', !now);
  });
  card.appendChild(b);
  return card;
}

function il27ClickSimCard(sim) {
  var card = el('div', 'card');
  card.innerHTML = '<h3>' + esc(sim.title || sim.id) + '</h3>' +
    '<p class="small muted">' + esc(sim.tool || '') + ' · ' + esc(sim.moduleId || '') + '</p>' +
    '<div class="il27-clickstep small"></div>' +
    '<div class="btn-row"><button class="btn" data-p type="button">← Prev</button>' +
    '<button class="btn primary" data-n type="button">Next →</button></div>';
  var steps = sim.steps || [];
  var i = 0;
  var stepEl = card.querySelector('.il27-clickstep');
  function paint() {
    stepEl.innerHTML = steps.length
      ? '<p><b>Step ' + (i + 1) + '/' + steps.length + '.</b></p><p>' + esc(steps[i]) + '</p>'
      : '<p class="muted">No steps shipped.</p>';
  }
  card.querySelector('[data-p]').addEventListener('click', function () { if (i > 0) { i--; paint(); } });
  card.querySelector('[data-n]').addEventListener('click', function () { if (i < steps.length - 1) { i++; paint(); } });
  paint();
  return card;
}

function il27BranchCard(br) {
  var card = el('div', 'card');
  card.innerHTML = '<h3>' + esc(br.title || br.id) + '</h3>' +
    '<p class="small muted">Branching scenario — ' + esc(br.moduleId || '') + '. Choose; read the feedback; continue.</p>' +
    '<div class="il27-branch-body"></div>';
  var body = card.querySelector('.il27-branch-body');
  var nodes = br.nodes || {};
  var doneKey = 'branch:' + br.id;

  function renderNode(key) {
    var n = nodes[key];
    body.innerHTML = '';
    if (!n) {
      body.appendChild(el('p', 'il27-ok', '✓ Scenario complete. ' +
        (Progress.get(doneKey) === '1' ? 'Logged as complete.' : '')));
      Progress.set(doneKey, '1');
      return;
    }
    body.appendChild(el('p', '', esc(n.text || '')));
    (n.choices || []).forEach(function (ch) {
      var b = el('button', 'btn', esc(ch.label || ''));
      b.type = 'button';
      b.style.display = 'block';
      b.style.margin = '6px 0';
      b.style.textAlign = 'left';
      b.addEventListener('click', function () {
        body.innerHTML = '<div class="card"><p>' + esc(ch.feedback || 'Noted.') + '</p>' +
          '<button class="btn primary" data-c type="button">Continue →</button></div>';
        body.querySelector('[data-c]').addEventListener('click', function () { renderNode(ch.next); });
      });
      body.appendChild(b);
    });
    if (!(n.choices || []).length) {
      var fin = el('button', 'btn primary', 'Finish scenario');
      fin.type = 'button';
      fin.addEventListener('click', function () { renderNode('__end__'); });
      body.appendChild(fin);
    }
  }
  renderNode(br.start);
  return card;
}

function il27ExtraLabs(root) {
  var sec = el('div', 'il27-extra-labs');
  sec.innerHTML = '<h2 class="section-title" style="margin-top:2em">Adaptive lab engines</h2>' +
    '<p class="section-sub">Knowledge check → personalized path → mastery progression → re-checks → mastery map.</p>' +
    '<div class="il27-engines"></div>';
  root.appendChild(sec);
  var engHost = sec.querySelector('.il27-engines');
  [['mathLab', COURSE.mathLab], ['scriptingLab', COURSE.scriptingLab]].forEach(function (pair) {
    if (pair[1]) il27AdaptiveLab(engHost, pair[1]);
  });

  function addSection(title, sub, items, cardFn, emptyMsg) {
    if (!items || !items.length) return;
    var h = el('h2', 'section-title', title);
    h.style.marginTop = '2em';
    root.appendChild(h);
    root.appendChild(el('p', 'section-sub', sub));
    var grid = el('div', 'il27-lab-grid');
    items.forEach(function (it) { grid.appendChild(cardFn(it)); });
    root.appendChild(grid);
  }
  addSection('Install labs', 'Get the homelab tools installed — checkpoints persist as you tick them.',
    COURSE.installLabs, il27InstallLabCard);
  addSection('Tool labs', 'Chained tool exercises with deliverables.',
    COURSE.toolLabs, il27ToolLabCard);
  addSection('Click-through sims', 'Step through admin-console workflows one click at a time.',
    COURSE.clickSims, il27ClickSimCard);
  addSection('Branching scenarios', 'Troubleshooting stories where your choices change the outcome.',
    COURSE.branchingScenarios, il27BranchCard);
}

/* ================== wiring (IL-27 only) ================== */
BUILDERS.fasttrack = il27BuildFastTrack;
BUILDERS.objectives = il27BuildObjectives;
var _il27_BUILDERS_labs = BUILDERS.labs;
BUILDERS.labs = function (root) {
  _il27_BUILDERS_labs(root);
  if (isIL27()) il27ExtraLabs(root);
};
