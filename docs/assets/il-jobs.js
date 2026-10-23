/* Jobs Suite dashboard client — Interstitium Labs (original, no deps).
   Talks to /api/jobs/* on the flagship worker. Account data when signed
   in; on-device mirror (localStorage) when not. */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function api(path, opts) {
    opts = opts || {};
    opts.credentials = 'same-origin';
    if (opts.body && typeof opts.body !== 'string') {
      opts.body = JSON.stringify(opts.body);
      opts.headers = Object.assign({ 'Content-Type': 'application/json' }, opts.headers || {});
    }
    return fetch(path, opts).then(function (r) {
      return r.json().catch(function () { return { ok: false, error: 'bad_response', _status: r.status }; })
        .then(function (j) { j._status = r.status; return j; });
    });
  }
  function setStatus(id, msg, isErr) {
    var el = $(id); if (!el) return;
    el.textContent = msg || '';
    el.classList.toggle('err', !!isErr);
  }
  function fmtDate(iso) {
    if (!iso) return '';
    var d = new Date(iso);
    return isNaN(d.getTime()) ? '' : d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
  }
  function fmtSalary(s) {
    if (!s || (!s.min && !s.max)) return '';
    var f = function (n) { return '$' + Math.round(n).toLocaleString(); };
    if (s.min && s.max && s.min !== s.max) return f(s.min) + ' – ' + f(s.max);
    return f(s.max || s.min);
  }

  var state = {
    me: null, jobs: new Map(), page: 1, lastQuery: null,
    profile: null, tracker: [], resumeHtml: '', letterHtml: '',
  };

  /* ---------- tabs ---------- */
  function showTab(name) {
    document.querySelectorAll('.jl-tabs [data-tab]').forEach(function (b) {
      b.setAttribute('aria-selected', b.getAttribute('data-tab') === name ? 'true' : 'false');
    });
    document.querySelectorAll('.jl-panel').forEach(function (p) {
      p.classList.toggle('on', p.id === 'panel-' + name);
    });
    if (location.hash !== '#' + name) history.replaceState(null, '', '#' + name);
    if (name === 'tracker') renderTracker();
    if (name === 'alerts') renderAlerts();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
  document.querySelectorAll('.jl-tabs [data-tab]').forEach(function (b) {
    b.addEventListener('click', function () { showTab(b.getAttribute('data-tab')); });
  });

  /* ---------- session ---------- */
  function initSession() {
    return api('/api/me').then(function (d) {
      if (d && d.ok && d.email) {
        state.me = d.email;
        $('acct-state').innerHTML = 'Signed in as <b>' + esc(d.email) + '</b> — profile, tracker &amp; alerts sync to your account.';
        $('tracker-sub').textContent = 'Synced to your account — your pipeline follows you to every device.';
      } else {
        $('acct-state').innerHTML = 'Not signed in — everything works, stored on this device. <a href="/account/">Sign in</a> to make it follow you.';
      }
    }).catch(function () {
      $('acct-state').textContent = 'Session check unavailable — working on-device.';
    });
  }
  function showTier(tier) {
    if (!tier) return;
    var el = $('tier-state');
    var c = tier.credits || {};
    el.hidden = false;
    el.innerHTML = 'Plan: <b>' + esc(tier.tier) + '</b>' +
      (tier.tier === 'free' ? ' · Resumes ' + (c.resume ? c.resume.remaining : '–') + '/day left · Letters ' + (c.coverletter ? c.coverletter.remaining : '–') + '/day left' : ' · unlimited generation');
  }

  /* ---------- sources ---------- */
  function initSources() {
    return api('/api/jobs/sources').then(function (d) {
      if (!d || !d.sources) return;
      var sel = $('f-source');
      d.sources.forEach(function (s) {
        var o = document.createElement('option');
        o.value = s.id; o.textContent = s.label + (s.status === 'needs_key' ? ' (key pending)' : '');
        sel.appendChild(o);
      });
      $('source-status').innerHTML = d.sources.map(function (s) {
        return '<span class="jl-tag' + (s.status === 'live' ? ' ok' : ' warn') + '">' +
          esc(s.label) + (s.status === 'live' ? ' · live' : ' · key pending') + '</span>';
      }).join('');
    }).catch(function () {});
  }

  /* ---------- job cards ---------- */
  function jobCard(j) {
    var sig = [];
    sig.push('<span class="jl-tag">' + esc(j.signals.level) + '</span>');
    if (j.remote) sig.push('<span class="jl-tag ok">remote</span>');
    if (j.signals.clearance) sig.push('<span class="jl-tag warn">clearance</span>');
    if (j.signals.sponsorship === 'yes') sig.push('<span class="jl-tag ok">sponsorship</span>');
    if (j.signals.sponsorship === 'no') sig.push('<span class="jl-tag">no sponsorship</span>');
    var sal = fmtSalary(j.signals.salary);
    if (sal) sig.push('<span class="jl-tag ok">' + esc(sal) + '</span>');
    if (j.also_on && j.also_on.length) sig.push('<span class="jl-tag">also on ' + esc(j.also_on.join(', ')) + '</span>');
    var id = esc(j.id);
    return '<article class="jl-job">' +
      '<h3><a href="' + esc(j.url) + '" target="_blank" rel="noopener">' + esc(j.title) + '</a></h3>' +
      '<p class="jl-meta">' + esc(j.company) + ' · ' + esc(j.location || '—') +
      (j.posted_at ? ' · ' + fmtDate(j.posted_at) : '') +
      '<span class="jl-badge">' + esc(j.source_label) + '</span></p>' +
      '<div class="jl-tags">' + sig.join('') + '</div>' +
      (j.description ? '<p class="jl-desc">' + esc(j.description.slice(0, 240)) + '…</p>' : '') +
      '<div class="jl-acts">' +
      '<a class="btn sm" href="' + esc(j.url) + '" target="_blank" rel="noopener">Apply ↗</a>' +
      '<button class="btn sec sm" data-act="match" data-id="' + id + '">Match</button>' +
      '<button class="btn sec sm" data-act="resume" data-id="' + id + '">Resume</button>' +
      '<button class="btn sec sm" data-act="letter" data-id="' + id + '">Letter</button>' +
      '<button class="btn sec sm" data-act="company" data-id="' + id + '">360°</button>' +
      '<button class="btn sec sm" data-act="track" data-id="' + id + '">+ Track</button>' +
      '</div></article>';
  }
  function wireCards(container) {
    container.querySelectorAll('[data-act]').forEach(function (b) {
      b.addEventListener('click', function () {
        var j = state.jobs.get(b.getAttribute('data-id'));
        if (!j) return;
        var act = b.getAttribute('data-act');
        if (act === 'match') { pickJob('match', j); showTab('match'); }
        if (act === 'resume') { pickJob('resume', j); showTab('resume'); }
        if (act === 'letter') { pickJob('letter', j); showTab('letter'); }
        if (act === 'company') { $('co-name').value = j.company; showTab('company'); runCompany(); }
        if (act === 'track') { trackJob(j, b); }
      });
    });
  }
  function postingText(j) {
    return (j.title || '') + ' at ' + (j.company || '') + '\n' + (j.location || '') + '\n\n' + (j.description || '');
  }
  function refreshPickers() {
    ['match-job', 'resume-job', 'letter-job'].forEach(function (id) {
      var sel = $(id); if (!sel) return;
      var cur = sel.value;
      var first = sel.options[0] ? sel.options[0].outerHTML : '';
      sel.innerHTML = first + Array.from(state.jobs.values()).map(function (j) {
        return '<option value="' + esc(j.id) + '">' + esc(j.title) + ' — ' + esc(j.company) + '</option>';
      }).join('');
      if (cur) sel.value = cur;
    });
  }
  function pickJob(tab, j) {
    var sel = $(tab + '-job'), ta = $(tab + '-posting');
    if (sel) { refreshPickers(); sel.value = j.id; }
    if (ta) ta.value = postingText(j);
  }
  ['match', 'resume', 'letter'].forEach(function (tab) {
    var sel = $(tab + '-job');
    if (sel) sel.addEventListener('change', function () {
      var j = state.jobs.get(sel.value);
      var ta = $(tab + '-posting');
      if (j && ta) ta.value = postingText(j);
    });
  });

  /* ---------- search ---------- */
  function currentQuery(page) {
    return {
      q: $('q').value.trim(), location: $('loc').value.trim(),
      source: $('f-source').value, level: $('f-level').value, type: $('f-type').value,
      posted_days: $('f-posted').value, salary_min: $('f-salary').value,
      sponsorship: $('f-spons').value, remote: $('f-remote').checked ? '1' : '',
      clearance: $('f-clear').checked ? '1' : '', page: page, limit: 25,
    };
  }
  function runSearch(page, append) {
    var qs = new URLSearchParams(currentQuery(page));
    setStatus('search-status', page > 1 ? 'Loading more…' : 'Searching the board…');
    $('search-btn').disabled = true;
    return api('/api/jobs/search?' + qs.toString()).then(function (d) {
      $('search-btn').disabled = false;
      if (!d || d.error) { setStatus('search-status', 'Search failed. Try again.', true); return; }
      (d.jobs || []).forEach(function (j) { state.jobs.set(j.id, j); });
      var html = (d.jobs || []).map(jobCard).join('');
      if (append) $('results').insertAdjacentHTML('beforeend', html);
      else $('results').innerHTML = html || '<p class="jl-sub">No listings matched. Loosen a filter or try broader keywords.</p>';
      wireCards($('results'));
      refreshPickers();
      state.page = d.page; state.total = d.total;
      setStatus('search-status', d.total + ' canonical listings across ' +
        d.sources.filter(function (s) { return s.status === 'ok'; }).length + ' live sources.');
      $('more-btn').hidden = !(d.page * d.limit < d.total);
      setStatus('more-status', d.page * d.limit < d.total ? 'Showing ' + Math.min(d.page * d.limit, d.total) + ' of ' + d.total : '');
    }).catch(function () {
      $('search-btn').disabled = false;
      setStatus('search-status', 'Search failed. Try again.', true);
    });
  }
  $('search-form').addEventListener('submit', function (e) { e.preventDefault(); runSearch(1, false); });
  $('more-btn').addEventListener('click', function () { runSearch(state.page + 1, true); });

  /* ---------- profile ---------- */
  var LS_PROFILE = 'il-jobs-profile', LS_TRACKER = 'il-jobs-tracker', LS_ALERTS = 'il-jobs-alerts';
  function lsGet(k) { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  function expRow(e) {
    e = e || {};
    return '<div class="jl-card exp-row" style="padding:12px">' +
      '<div class="jl-filters">' +
      '<div><label>Title</label><input class="x-title" value="' + esc(e.title) + '"></div>' +
      '<div><label>Company</label><input class="x-company" value="' + esc(e.company) + '"></div>' +
      '<div><label>Location</label><input class="x-loc" value="' + esc(e.location) + '"></div>' +
      '<div><label>Start – End</label><input class="x-when" value="' + esc([e.start, e.end].filter(Boolean).join(' – ')) + '"></div></div>' +
      '<label style="margin-top:8px">Bullets (one per line)</label>' +
      '<textarea class="x-bullets" rows="3">' + esc((e.bullets || []).join('\n')) + '</textarea>' +
      '<button class="btn sec sm x-del" type="button" style="margin-top:6px">Remove role</button></div>';
  }
  function eduRow(e) {
    e = e || {};
    return '<div class="jl-card edu-row" style="padding:12px"><div class="jl-filters">' +
      '<div><label>School</label><input class="e-school" value="' + esc(e.school) + '"></div>' +
      '<div><label>Credential</label><input class="e-cred" value="' + esc(e.credential) + '"></div>' +
      '<div><label>Year</label><input class="e-year" value="' + esc(e.year) + '"></div></div>' +
      '<button class="btn sec sm e-del" type="button" style="margin-top:6px">Remove</button></div>';
  }
  function fillProfileForm(p) {
    if (!p) return;
    $('pf-name').value = p.name || ''; $('pf-email').value = p.email || '';
    $('pf-phone').value = p.phone || ''; $('pf-loc').value = p.location || '';
    $('pf-headline').value = p.headline || ''; $('pf-auth').value = p.work_auth || '';
    $('pf-salary').value = p.salary_expectation || '';
    $('pf-certs').value = (p.certifications || []).join(', ');
    $('pf-summary').value = p.summary || ''; $('pf-skills').value = p.skills || '';
    var L = p.links || {};
    $('pf-li').value = L.linkedin || ''; $('pf-gh').value = L.github || '';
    $('pf-pf').value = L.portfolio || ''; $('pf-web').value = L.website || '';
    var E = p.eeo || {};
    $('pf-eeo-g').value = E.gender || ''; $('pf-eeo-r').value = E.race || '';
    $('pf-eeo-v').value = E.veteran || ''; $('pf-eeo-d').value = E.disability || '';
    $('pf-exp').innerHTML = (p.experience || []).map(expRow).join('') || expRow({});
    $('pf-edu').innerHTML = (p.education || []).map(eduRow).join('') || eduRow({});
    wireProfileRows();
  }
  function readProfileForm() {
    var exp = [];
    document.querySelectorAll('.exp-row').forEach(function (row) {
      var when = row.querySelector('.x-when').value.split('–').map(function (s) { return s.trim(); });
      var bullets = row.querySelector('.x-bullets').value.split('\n').map(function (s) { return s.trim(); }).filter(Boolean);
      var title = row.querySelector('.x-title').value.trim();
      if (title || bullets.length) exp.push({
        title: title, company: row.querySelector('.x-company').value.trim(),
        location: row.querySelector('.x-loc').value.trim(),
        start: when[0] || '', end: when[1] || '', bullets: bullets,
      });
    });
    var edu = [];
    document.querySelectorAll('.edu-row').forEach(function (row) {
      var school = row.querySelector('.e-school').value.trim();
      if (school) edu.push({ school: school, credential: row.querySelector('.e-cred').value.trim(), year: row.querySelector('.e-year').value.trim() });
    });
    return {
      name: $('pf-name').value.trim(), email: $('pf-email').value.trim(),
      phone: $('pf-phone').value.trim(), location: $('pf-loc').value.trim(),
      headline: $('pf-headline').value.trim(), work_auth: $('pf-auth').value.trim(),
      salary_expectation: $('pf-salary').value.trim(),
      certifications: $('pf-certs').value.split(',').map(function (s) { return s.trim(); }).filter(Boolean),
      summary: $('pf-summary').value.trim(), skills: $('pf-skills').value.trim(),
      links: { linkedin: $('pf-li').value.trim(), github: $('pf-gh').value.trim(), portfolio: $('pf-pf').value.trim(), website: $('pf-web').value.trim() },
      experience: exp, education: edu,
      eeo: { gender: $('pf-eeo-g').value.trim(), race: $('pf-eeo-r').value.trim(), veteran: $('pf-eeo-v').value.trim(), disability: $('pf-eeo-d').value.trim() },
    };
  }
  function wireProfileRows() {
    document.querySelectorAll('.x-del').forEach(function (b) { b.onclick = function () { b.closest('.exp-row').remove(); }; });
    document.querySelectorAll('.e-del').forEach(function (b) { b.onclick = function () { b.closest('.edu-row').remove(); }; });
  }
  $('pf-exp-add').addEventListener('click', function () { $('pf-exp').insertAdjacentHTML('beforeend', expRow({})); wireProfileRows(); });
  $('pf-edu-add').addEventListener('click', function () { $('pf-edu').insertAdjacentHTML('beforeend', eduRow({})); wireProfileRows(); });

  function loadProfile() {
    if (state.me) {
      return api('/api/jobs/profile').then(function (d) {
        state.profile = (d && d.profile) || lsGet(LS_PROFILE);
        fillProfileForm(state.profile || {});
      });
    }
    state.profile = lsGet(LS_PROFILE);
    fillProfileForm(state.profile || {});
    return Promise.resolve();
  }
  function ensureProfile() {
    var p = readProfileForm();
    if (!p.name && !state.profile) { setStatus('profile-status', 'Fill in and save your Job Profile first — generation uses only these facts.', true); showTab('profile'); return null; }
    return p.name ? p : state.profile;
  }
  $('profile-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var p = readProfileForm();
    state.profile = p; lsSet(LS_PROFILE, p);
    if (state.me) {
      api('/api/jobs/profile', { method: 'PUT', body: { profile: p } }).then(function (d) {
        setStatus('profile-status', d && d.ok ? 'Profile saved to your account.' : 'Saved on this device (account save failed).', !(d && d.ok));
      });
    } else setStatus('profile-status', 'Profile saved on this device. Sign in to sync it to your account.');
  });
  $('pf-autofill').addEventListener('click', function () {
    var p = ensureProfile(); if (!p) return;
    setStatus('profile-status', 'Building autofill payload…');
    api('/api/jobs/autofill', { method: 'POST', body: { profile: p } }).then(function (d) {
      if (!d || !d.ok) { setStatus('profile-status', 'Autofill failed: ' + ((d && d.error) || 'unknown'), true); return; }
      setStatus('profile-status', '');
      var pl = d.payload;
      var rows = Object.keys(pl).filter(function (k) { return typeof pl[k] === 'string' && pl[k]; })
        .map(function (k) { return '<tr><th style="text-transform:none;letter-spacing:0;color:var(--mut)">' + esc(k) + '</th><td>' + esc(pl[k]) + '</td></tr>'; }).join('');
      $('autofill-out').innerHTML = '<div class="jl-scroll"><table class="jl-t">' + rows + '</table></div>' +
        '<h3>Paste-ready block</h3><div class="jl-out" id="af-text">' + esc(d.text) + '</div>' +
        '<button class="btn sec sm" id="af-copy" style="margin-top:8px">Copy block</button>';
      $('af-copy').addEventListener('click', function () {
        navigator.clipboard.writeText(d.text).then(function () { $('af-copy').textContent = 'Copied ✓'; });
      });
      /* 2026-10-11: Secure Credential Broker — when an application
         needs a portal sign-in, the agent uses the saved login through
         the secure store. Show which portal logins are on file right
         beside the autofill payload (names/states only, never values). */
      try {
        var panel = document.getElementById('il-jobs-portal-logins');
        if (!panel) {
          panel = document.createElement('div');
          panel.id = 'il-jobs-portal-logins';
          panel.style.marginTop = '16px';
          $('autofill-out').appendChild(panel);
        }
        var renderPanel = function () {
          if (window.ILCredBroker) window.ILCredBroker.renderJobsPanel(panel);
        };
        if (window.ILCredBroker) renderPanel();
        else {
          var sc = document.createElement('script');
          sc.src = '/assets/il-cred-broker.js';
          sc.onload = renderPanel;
          document.head.appendChild(sc);
        }
      } catch (e) {}
    });
  });

  /* ---------- match ---------- */
  function renderMatch(d) {
    var checks = (d.ats.checks || []).map(function (c) {
      return '<li>' + (c.pass ? '✅' : '⚠️') + ' <b>' + esc(c.label) + '</b> — ' + esc(c.detail) + '</li>';
    }).join('');
    $('match-out').innerHTML =
      '<div class="jl-score" style="margin-top:12px"><div class="num">' + d.score + '</div>' +
      '<div><strong>ATS match score</strong><p class="jl-sub" style="margin:0">Keyword coverage ' + d.ats.keywordCoverage + '%</p></div></div>' +
      '<h3>Evidence found</h3><div class="jl-chips">' + (d.matched || []).map(function (s) { return '<span class="jl-chipk">' + esc(s) + '</span>'; }).join('') + '</div>' +
      '<h3>Gaps in the posting you do not evidence yet</h3><div class="jl-chips">' + (d.missing || []).map(function (s) { return '<span class="jl-chipk miss">' + esc(s) + '</span>'; }).join('') + '</div>' +
      '<ul class="jl-checks">' + checks + '</ul>' +
      (d.ai ? '<h3>AI gap analysis</h3><div class="jl-out">' + esc(d.ai) + '</div>' : '') +
      '<p class="jl-fine">Close a gap with a course, then re-score: <a href="/university/">browse the catalog</a> · <a href="/noah/?mode=interview">practice the interview</a></p>';
  }
  function runMatch(withAi) {
    var p = ensureProfile(); if (!p) { setStatus('match-status', 'Save your Job Profile first (Profile tab).', true); showTab('profile'); return; }
    var posting = $('match-posting').value.trim();
    if (!posting) { setStatus('match-status', 'Pick a searched job or paste a posting.', true); return; }
    setStatus('match-status', 'Scoring…');
    api('/api/jobs/match', { method: 'POST', body: { profile: p, posting: posting, ai: !!withAi } }).then(function (d) {
      if (!d || d.error) { setStatus('match-status', 'Match failed: ' + ((d && d.error) || ''), true); return; }
      setStatus('match-status', d.ai_error === 'credit_exhausted' ? 'Score computed. AI narrative needs a credit (free: 10/day) — try tomorrow or go premium.' : '');
      showTier(d.tier); renderMatch(d);
    });
  }
  $('match-btn').addEventListener('click', function () { runMatch(false); });
  $('match-ai-btn').addEventListener('click', function () { runMatch(true); });

  /* ---------- resume & letter ---------- */
  function openPrint(html) {
    var w = window.open('', '_blank');
    if (w) { w.document.write(html); w.document.close(); w.focus(); }
  }
  function downloadHtml(html, name) {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([html], { type: 'text/html' }));
    a.download = name; a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
  }
  function postingFor(tab) {
    var ta = $(tab + '-posting').value.trim();
    if (ta) return { posting: ta };
    var j = state.jobs.get($(tab + '-job').value);
    if (j) return { job: { title: j.title, company: j.company, description: j.description } };
    return {};
  }
  $('resume-btn').addEventListener('click', function () {
    var p = ensureProfile(); if (!p) { showTab('profile'); return; }
    var btn = $('resume-btn'); btn.disabled = true;
    setStatus('resume-status', 'The Resume Tailor is writing — this takes a few seconds…');
    api('/api/jobs/resume', { method: 'POST', body: Object.assign({ profile: p }, postingFor('resume')) }).then(function (d) {
      btn.disabled = false; showTier(d && d.tier);
      if (!d || d.error) {
        setStatus('resume-status', d && d.error === 'credit_exhausted' ? (d.message || 'Daily resume credits used.') : 'Generation failed. Try again.', true);
        return;
      }
      setStatus('resume-status', 'Done — generated by ' + (d.model || 'the router') + '.');
      state.resumeHtml = d.html || '';
      $('resume-print').hidden = !d.html; $('resume-dl').hidden = !d.html;
      $('resume-out').innerHTML =
        (d.ats ? '<div class="jl-score"><div class="num">' + d.ats.score + '</div><div><strong>ATS score vs this posting</strong><p class="jl-sub" style="margin:0">Missing: ' + esc((d.ats.missing || []).join(', ') || 'none') + '</p></div></div>' : '') +
        (d.html ? '<iframe class="jl-frame" title="Tailored resume" sandbox="allow-same-origin" srcdoc="' + esc(d.html) + '"></iframe>' : '<div class="jl-out">' + esc(d.text || '') + '</div>');
    }).catch(function () { btn.disabled = false; setStatus('resume-status', 'Generation failed. Try again.', true); });
  });
  $('resume-print').addEventListener('click', function () { if (state.resumeHtml) openPrint(state.resumeHtml); });
  $('resume-dl').addEventListener('click', function () { if (state.resumeHtml) downloadHtml(state.resumeHtml, 'resume-tailored.html'); });

  $('letter-btn').addEventListener('click', function () {
    var p = ensureProfile(); if (!p) { showTab('profile'); return; }
    var body = Object.assign({ profile: p }, postingFor('letter'));
    if (!body.posting && !body.job) { setStatus('letter-status', 'Pick a searched job or paste the posting.', true); return; }
    var btn = $('letter-btn'); btn.disabled = true;
    setStatus('letter-status', 'Writing your letter…');
    api('/api/jobs/coverletter', { method: 'POST', body: body }).then(function (d) {
      btn.disabled = false; showTier(d && d.tier);
      if (!d || d.error) {
        setStatus('letter-status', d && d.error === 'credit_exhausted' ? (d.message || 'Daily letter credits used.') : 'Generation failed. Try again.', true);
        return;
      }
      setStatus('letter-status', 'Done.');
      state.letterHtml = d.html || '';
      $('letter-print').hidden = !d.html;
      $('letter-out').innerHTML =
        (d.ats ? '<p class="jl-sub">Profile↔posting score: <strong style="color:var(--gold2)">' + d.ats.score + '/100</strong></p>' : '') +
        '<div class="jl-out">' + esc(d.letter || '') + '</div>';
    }).catch(function () { btn.disabled = false; setStatus('letter-status', 'Generation failed. Try again.', true); });
  });
  $('letter-print').addEventListener('click', function () { if (state.letterHtml) openPrint(state.letterHtml); });

  /* ---------- company 360 + outreach ---------- */
  function runCompany() {
    var name = $('co-name').value.trim();
    if (!name) { setStatus('co-status', 'Enter a company name.', true); return; }
    setStatus('co-status', 'Building the dossier…');
    api('/api/jobs/company?name=' + encodeURIComponent(name)).then(function (d) {
      if (!d || d.error) { setStatus('co-status', 'Dossier failed.', true); return; }
      setStatus('co-status', '');
      var hp = d.hiring_patterns || {};
      var lv = hp.levels || {};
      var jobs = (d.openings.jobs || []).map(function (j) {
        return '<p style="margin:4px 0"><a href="' + esc(j.url) + '" target="_blank" rel="noopener">' + esc(j.title) + '</a> <span class="jl-fine">' + esc(j.location || '') + ' · ' + esc(j.source_label) + '</span></p>';
      }).join('');
      $('co-out').innerHTML =
        (d.overview ? '<h3>' + esc(d.overview.title) + ' <span class="jl-fine">(Wikipedia)</span></h3><p class="jl-desc" style="color:var(--ink)">' + esc((d.overview.extract || '').slice(0, 700)) + '… <a href="' + esc(d.overview.url) + '" target="_blank" rel="noopener">Read more</a></p>' : '') +
        '<h3>Openings on the board: ' + d.openings.count + '</h3>' + (jobs || '<p class="jl-fine">No current openings found for this company.</p>') +
        '<h3>Tech-stack signals from their postings</h3><div class="jl-chips">' + (d.tech_stack_signals || []).map(function (s) { return '<span class="jl-chipk">' + esc(s) + '</span>'; }).join('') + '</div>' +
        '<h3>Hiring patterns</h3><p class="jl-sub">Levels — junior ' + (lv.junior || 0) + ' · mid ' + (lv.mid || 0) + ' · senior ' + (lv.senior || 0) + ' · Remote share ' + (hp.remote_share || 0) + '% · Sources: ' + esc((hp.sources || []).join(', ') || '—') + '</p>' +
        '<div class="jl-acts"><a class="btn sm" href="' + esc(d.prep.coach) + '">Practice this company\'s interview 🎙</a>' +
        '<a class="btn sec sm" href="' + esc(d.prep.drills) + '">Prep drills</a>' +
        '<a class="btn sec sm" href="' + esc(d.prep.courses) + '">Close skill gaps</a></div>';
      $('oc-company').value = name;
    });
  }
  $('co-btn').addEventListener('click', runCompany);
  function runOutreach(withDraft) {
    var body = {
      company: $('oc-company').value.trim(), domain: $('oc-domain').value.trim(),
      posting: $('match-posting').value.trim(), profile: state.profile || readProfileForm(), draft: !!withDraft,
    };
    setStatus('oc-status', 'Checking public contacts…');
    api('/api/jobs/outreach', { method: 'POST', body: body }).then(function (d) {
      if (!d || d.error) { setStatus('oc-status', 'Outreach lookup failed.', true); return; }
      setStatus('oc-status', '');
      var pubs = (d.published_contacts || []).map(function (c) { return '<li><b>' + esc(c.email) + '</b> — ' + esc(c.source) + '</li>'; }).join('');
      var pats = (d.email_format_patterns || []).map(function (p) { return '<li><code>' + esc(p.pattern) + '</code> <span class="jl-fine">(shape: ' + esc(p.example_shape) + ')</span></li>'; }).join('');
      $('oc-out').innerHTML =
        '<h3>Published contacts</h3>' + (pubs ? '<ul class="jl-checks">' + pubs + '</ul>' : '<p class="jl-fine">None published in the posting text provided.</p>') +
        (d.careers_page ? '<p class="jl-fine">Careers page: <a href="' + esc(d.careers_page) + '" target="_blank" rel="noopener">' + esc(d.careers_page) + '</a></p>' : '') +
        '<h3>Email format patterns</h3>' + (pats ? '<ul class="jl-checks">' + pats + '</ul><p class="jl-fine">' + esc(d.pattern_note || '') + '</p>' : '<p class="jl-fine">' + esc(d.pattern_note || '') + '</p>') +
        (d.draft ? '<h3>Outreach draft</h3><div class="jl-out">' + esc(d.draft) + '</div>' : '') +
        (d.draft_error === 'credit_exhausted' ? '<p class="jl-fine">Draft credits used for today (free: 2/day).</p>' : '') +
        '<p class="jl-fine">' + esc(d.governance || '') + '</p>';
    });
  }
  $('oc-btn').addEventListener('click', function () { runOutreach(false); });
  $('oc-draft-btn').addEventListener('click', function () { runOutreach(true); });

  /* ---------- tracker ---------- */
  var STATUSES = ['preparing', 'applied', 'interview', 'offer', 'closed'];
  function loadTracker() {
    if (state.me) {
      return api('/api/jobs/tracker').then(function (d) {
        state.tracker = (d && d.apps) || [];
        state.followUps = (d && d.follow_ups_due) || [];
      });
    }
    state.tracker = lsGet(LS_TRACKER) || [];
    var today = new Date().toISOString().slice(0, 10);
    state.followUps = state.tracker.filter(function (a) { return a.follow_up_at && a.follow_up_at <= today && a.status !== 'closed'; });
    return Promise.resolve();
  }
  function saveTrackerLocal() { lsSet(LS_TRACKER, state.tracker); }
  function renderTracker() {
    var due = state.followUps || [];
    $('due-box').innerHTML = due.length ?
      '<div class="jl-due">⏰ <strong>' + due.length + ' follow-up' + (due.length > 1 ? 's' : '') + ' due:</strong> ' +
      due.map(function (a) { return esc(a.company) + ' (' + esc(a.job_title) + ')'; }).join(' · ') + '</div>' : '';
    var tb = $('tracker-body');
    if (!state.tracker.length) {
      tb.innerHTML = '<tr><td colspan="7" class="jl-fine">Nothing tracked yet — add from a search card (+ Track) or the form below.</td></tr>';
      return;
    }
    tb.innerHTML = state.tracker.map(function (a) {
      var opts = STATUSES.map(function (s) { return '<option' + (s === a.status ? ' selected' : '') + '>' + s + '</option>'; }).join('');
      return '<tr data-id="' + esc(a.id) + '"><td><b>' + esc(a.company) + '</b><div class="jl-fine">' + esc(a.portal || '') + '</div></td>' +
        '<td>' + esc(a.job_title) + (a.url ? ' <a href="' + esc(a.url) + '" target="_blank" rel="noopener">↗</a>' : '') + '</td>' +
        '<td><select class="t-status">' + opts + '</select></td>' +
        '<td>' + esc(a.date_applied || '') + '</td>' +
        '<td><input type="date" class="t-follow" value="' + esc(a.follow_up_at || '') + '" style="width:auto;padding:5px"></td>' +
        '<td><input type="text" class="t-notes" value="' + esc(a.notes || '') + '" style="padding:5px"></td>' +
        '<td><button class="btn sec sm t-save">Save</button> <button class="btn sec sm t-del">✕</button></td></tr>';
    }).join('');
    tb.querySelectorAll('tr[data-id]').forEach(function (row) {
      var id = row.getAttribute('data-id');
      row.querySelector('.t-save').addEventListener('click', function () { updateTracker(id, row); });
      row.querySelector('.t-del').addEventListener('click', function () { deleteTracker(id); });
    });
  }
  function updateTracker(id, row) {
    var patch = {
      id: id, status: row.querySelector('.t-status').value,
      follow_up_at: row.querySelector('.t-follow').value || null,
      notes: row.querySelector('.t-notes').value,
    };
    if (state.me) {
      api('/api/jobs/tracker', { method: 'PUT', body: patch }).then(function (d) {
        if (d && d.ok) { state.tracker = d.apps; loadTracker().then(renderTracker); }
      });
    } else {
      var a = state.tracker.find(function (x) { return x.id === id; });
      if (a) { Object.assign(a, patch); saveTrackerLocal(); loadTracker().then(renderTracker); }
    }
  }
  function deleteTracker(id) {
    if (state.me) {
      api('/api/jobs/tracker?id=' + encodeURIComponent(id), { method: 'DELETE' }).then(function (d) {
        if (d && d.ok) { state.tracker = d.apps; renderTracker(); }
      });
    } else {
      state.tracker = state.tracker.filter(function (x) { return x.id !== id; });
      saveTrackerLocal(); renderTracker();
    }
  }
  function trackJob(j, btn) {
    var app = {
      company: j.company, job_title: j.title, location: j.location,
      portal: j.source_label, url: j.url, status: 'preparing',
    };
    if (state.me) {
      api('/api/jobs/tracker', { method: 'POST', body: { app: app } }).then(function (d) {
        if (d && d.ok) { state.tracker = d.apps; if (btn) btn.textContent = 'Tracked ✓'; }
      });
    } else {
      app.id = 'local-' + Date.now();
      app.date_applied = new Date().toISOString().slice(0, 10);
      state.tracker.unshift(app); saveTrackerLocal();
      if (btn) btn.textContent = 'Tracked ✓';
    }
  }
  $('track-add').addEventListener('submit', function (e) {
    e.preventDefault();
    trackJob({ company: $('ta-company').value.trim(), title: $('ta-title').value.trim(), location: $('ta-loc').value.trim(), source_label: $('ta-portal').value.trim(), url: '' }, null);
    e.target.reset();
    setTimeout(renderTracker, 350);
  });

  /* ---------- alerts ---------- */
  function renderAlerts() {
    var box = $('alert-list');
    if (!state.me) {
      var local = lsGet(LS_ALERTS) || [];
      box.innerHTML = local.length ?
        '<p class="jl-sub">On-device filters (sign in to sync + run digests):</p>' + local.map(function (f) { return '<span class="jl-chip">' + esc(f.name) + '</span>'; }).join(' ') :
        '<p class="jl-fine">No saved filters yet.</p>';
      return;
    }
    api('/api/jobs/alerts').then(function (d) {
      state.filters = (d && d.filters) || [];
      box.innerHTML = state.filters.length ?
        state.filters.map(function (f) {
          return '<p style="margin:6px 0"><span class="jl-chip"><b>' + esc(f.name) + '</b> · ' + esc(f.q) + (f.location ? ' · ' + esc(f.location) : '') + (f.remote ? ' · remote' : '') + '</span></p>';
        }).join('') : '<p class="jl-fine">No saved filters yet.</p>';
    });
  }
  $('alert-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var f = {
      name: $('al-name').value.trim() || ($('al-q').value.trim() + ' — ' + $('al-loc').value.trim()),
      q: $('al-q').value.trim(), location: $('al-loc').value.trim(),
      level: $('al-level').value, remote: $('al-remote').checked, source: 'all', type: 'all',
    };
    if (!state.me) {
      var local = lsGet(LS_ALERTS) || [];
      local.push(f); lsSet(LS_ALERTS, local);
      setStatus('alert-status', 'Saved on this device. Sign in to sync filters and run digests.');
      renderAlerts(); return;
    }
    var next = (state.filters || []).concat([f]);
    api('/api/jobs/alerts', { method: 'PUT', body: { filters: next } }).then(function (d) {
      if (d && d.ok) { setStatus('alert-status', 'Filter saved.'); state.filters = d.filters; renderAlerts(); }
      else setStatus('alert-status', (d && d.message) || 'Could not save the filter (tier limit?).', true);
    });
  });
  $('alert-check').addEventListener('click', function () {
    if (!state.me) { setStatus('alert-status', 'Sign in to run alert digests — filters check against your account.', true); return; }
    setStatus('alert-status', 'Alert Hunter is scanning the board…');
    api('/api/jobs/alerts/check').then(function (d) {
      if (!d || !d.ok) {
        setStatus('alert-status', d && d.error === 'credit_exhausted' ? (d.message || 'Daily digest used.') : 'Digest failed.', true);
        showTier(d && d.tier); return;
      }
      showTier(d.tier);
      var totalNew = 0, html = '';
      (d.digests || []).forEach(function (dg) {
        totalNew += dg.new_count;
        (dg.new_jobs || []).forEach(function (j) { state.jobs.set(j.id, j); html += jobCard(j); });
      });
      $('alert-out').innerHTML = html;
      wireCards($('alert-out'));
      setStatus('alert-status', totalNew ? totalNew + ' new match' + (totalNew > 1 ? 'es' : '') + ' since your last check.' : 'No new matches since your last check.');
    });
  });

  /* ---------- boot ---------- */
  initSession().then(function () {
    return Promise.all([initSources(), loadProfile(), loadTracker()]);
  }).then(function () {
    renderTracker();
    var h = (location.hash || '').slice(1);
    if (h && $('panel-' + h)) showTab(h);
    /* Deep link: /jobs/?q=...&company=... */
    var u = new URL(location.href);
    if (u.searchParams.get('q')) { $('q').value = u.searchParams.get('q'); runSearch(1, false); }
    if (u.searchParams.get('company')) { $('co-name').value = u.searchParams.get('company'); showTab('company'); runCompany(); }
  });
})();
