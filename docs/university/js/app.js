/* Interstitium Labs — shared app shell.
   Renders header/nav + footer into #il-header / #il-footer on every page,
   loads the sharded catalog (data/catalog/index.json + shards) with a graceful offline state, and provides
   DOM + catalog helpers. No frameworks. No network calls besides the
   catalog fetch and same-origin assets. */
(function () {
  'use strict';

  var IL = (window.IL = window.IL || {});

  /* ---------- small DOM helpers ---------- */
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    attrs = attrs || {};
    Object.keys(attrs).forEach(function (k) {
      var v = attrs[k];
      if (v == null) return;
      if (k === 'class') n.className = v;
      else if (k === 'text') n.textContent = v;
      else if (k === 'html') n.innerHTML = v;
      else if (k.indexOf('on') === 0 && typeof v === 'function') n.addEventListener(k.slice(2), v);
      else n.setAttribute(k, v);
    });
    (children || []).forEach(function (c) {
      if (c == null) return;
      n.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    });
    return n;
  }

  function fmtHours(h) {
    if (h == null || isNaN(h)) return '—';
    return Number(h).toLocaleString('en-US') + ' h';
  }

  function qs(name) {
    return new URLSearchParams(window.location.search).get(name);
  }

  IL.esc = esc;
  IL.el = el;
  IL.fmtHours = fmtHours;
  IL.qs = qs;

  /* ---------- topic themes (2026-10-09 themed-content rollout) ----------
     Academy code -> topic theme key, mirroring the "topicTheme" field added
     to data/courses/*.json. Used by card templates to set
     data-topic-theme so il-topic-themes.css activates. */
  var TOPIC_THEME_BY_CODE = {
    'IL-01': 'sacredgeo', 'IL-02': 'sacredgeo', 'IL-03': 'hackers95',
    'IL-04': 'industrial', 'IL-05': 'steampunk', 'IL-06': 'mr-robot',
    'IL-07': 'oceandeep', 'IL-08': 'hackers95', 'IL-09': 'mr-robot',
    'IL-10': 'vaporwave', 'IL-11': 'mr-robot', 'IL-12': 'exmachina',
    'IL-13': 'hackers95', 'IL-14': 'steampunk', 'IL-15': 'oceandeep',
    'IL-16': 'exmachina', 'IL-17': 'exmachina', 'IL-18': 'cyberpunk',
    'IL-19': 'steampunk', 'IL-20': 'sacredgeo', 'IL-21': 'sacredgeo',
    'IL-22': 'sacredgeo', 'IL-23': 'exmachina', 'IL-24': 'mr-robot',
    'IL-25': 'mr-robot', 'IL-26': 'oceandeep', 'IL-27': 'mr-robot',
    'IL-28': 'steampunk', 'IL-29': 'mr-robot'
  };
  IL.topicThemeForCode = function (code) {
    return TOPIC_THEME_BY_CODE[String(code || '').toUpperCase()] || '';
  };

  /* ---------- fallback academy index (verified against the live site 2026-09-30;
       used only when the sharded catalog (data/catalog/index.json) cannot be loaded) ---------- */
  var FALLBACK_ACADEMIES = [
    { code: 'IL-01', name: 'Esoteric Traditions & Digital Hermetica', hours: 420, tagline: 'The old systems, read as systems.', blurb: 'Hermeticism, Kabbalah, alchemy, and the Dee corpus studied as documented traditions, then the CCRU seminar: Land, hyperstition, the numogram, and the Cybersyn case study. Literacy is the aim; belief i' },
    { code: 'IL-02', name: 'Mathematical Maturity Engine', hours: 680, tagline: 'The ground under everything.', blurb: 'A unified spine from college algebra through probability and statistics, driven by an adaptive engine in the adaptive-learning lineage: place, fringe, gate, deepen. Includes a trade-applied Tech Math ' },
    { code: 'IL-03', name: 'Programming Language Forge', hours: 860, tagline: 'Languages as instruments, not identities.', blurb: 'Python into Java into C++ into data structures, then the systems sequence: organization, operating systems, networks, databases, software engineering. Pearson\'s programming backbone with an honest acc' },
    { code: 'IL-04', name: 'Systems, Linux, Windows & Networks', hours: 740, tagline: 'The machine, administered.', blurb: 'Linux to RHCSA, Windows systems administration, the Network+ core, and RHCE automation with Ansible. Hands-on and performance-oriented: the operating system is learned by operating it.' },
    { code: 'IL-05', name: 'Cloud, DevSecOps, Platform & SRE', hours: 2990, tagline: 'Ship it, then keep it alive.', blurb: 'The DevOps role map at cloud-native parity, the CNCF Kubernetes certification stack, Terraform as infrastructure-as-code, and zero-trust architecture per NIST SP 800-207. Pipelines, platforms, and the' },
    { code: 'IL-06', name: 'Cybersecurity & Secure Engineering', hours: 1180, tagline: 'Know the attack to earn the defense.', blurb: 'The Hackers-Arise curriculum cross-mapped topic by topic against HackTheBox, TryHackMe, OffSec, PortSwigger, SANS, CompTIA, and a leading training platform; the gaps become original Interstitium modul' },
    { code: 'IL-07', name: 'SQL, Data Engineering, Analytics & AI', hours: 1560, tagline: 'From the row to the model.', blurb: 'MongoDB University as the document-database path, the MIT/Stanford/CMU data-school spines distilled, the Stanford CS229-to-CS234 machine-learning arc with MLOps and LLM engineering, and a computing-or' },
    { code: 'IL-08', name: 'Algorithms, Compilers, Distributed & Formal', hours: 640, tagline: 'The deep core, in order.', blurb: 'MIT\'s 6-3 curriculum distilled in prerequisite order, CMU\'s systems-and-theory spine, and Stanford\'s core sequence as a cross-walk. For the learner who wants the ground truth beneath the frameworks.' },
    { code: 'IL-09', name: 'Adaptive Certification Command', hours: 1100, tagline: 'Credentials, orchestrated honestly.', blurb: 'CompTIA\'s full stack, vendor AI certifications, Oracle, Linux Foundation blockchain, and the C++/Python Institutes — orchestrated, never cloned. Every path routes to the vendor\'s own portal for the ex' },
    { code: 'IL-10', name: 'Portfolio, Career & Professional Practice', hours: 280, tagline: 'The work, presented; the career, directed.', blurb: 'The forward-deployed engineer career path with JobRight AI as the outcome layer, Humanmetrics assessment, a Babson-informed entrepreneurship track, and the quantitative-finance ladder from undergradua' },
    { code: 'IL-11', name: 'Zero Trust & Endpoint Defense', hours: 520, tagline: 'Never trust, always verify — the defender\'s discipline.', blurb: 'Distilled from the public shape of ThreatLocker\'s no-cost Zero Trust Cybersecurity Bootcamp: foundational IT, red-team attack simulation, blue-team defense, and Zero Trust principles, rebuilt as self-' },
    { code: 'IL-13', name: 'Software Engineering Interview Prep', hours: 470, tagline: 'Domain tracks, interview-ready.', blurb: 'The software-engineering interview spine — data structures and algorithms, system design, and domain tracks for backend, frontend, fullstack, mobile, embedded, and QA — distilled from the public curri' },
    { code: 'IL-14', name: 'SRE, DevOps, Cloud & Security Interview Prep', hours: 260, tagline: 'Keep it alive, then prove it in the interview.', blurb: 'The reliability-engineering interview spine — SRE, DevOps, cloud, and security engineering interview prep with system-design reps and a full mock circuit — distilled from the public curriculum shape o' },
    { code: 'IL-15', name: 'Data Engineering & Analytics Interview Prep', hours: 260, tagline: 'From the row to the offer.', blurb: 'The data interview spine — data engineering, data science, analytics, and machine-learning interview prep with SQL drills and case reps — distilled from the public curriculum shape of a leading interv' },
    { code: 'IL-16', name: 'Machine Learning & AI Engineering', hours: 430, tagline: 'The models, end to end.', blurb: 'The applied machine-learning and AI practice layer — advanced ML, generative AI, NLP, and AI-enabled software, built as hands-on practice with portfolio-grade projects — distilled from the public curr' },
    { code: 'IL-17', name: 'Agentic AI Engineering', hours: 310, tagline: 'Agents that do the work.', blurb: 'The agentic AI practice layer — foundations, role-specific applied tracks for engineers, data engineers, PMs, TPMs and EMs, low-code agents, and interview prep — distilled from the public curriculum s' },
    { code: 'IL-18', name: 'Technical Leadership Interview Prep', hours: 240, tagline: 'Lead the work, land the role.', blurb: 'The technical-leadership interview spine — TPM, engineering management, product management, and technical PM interview prep, plus generative AI fluency for PMs — distilled from the public curriculum s' },
    { code: 'IL-12', name: 'AI Engineering', hours: 875, tagline: 'From data to deployed intelligence.', blurb: 'The full AI-engineer spine — Python, data science, machine learning, deep learning, generative AI, NLP, agentic systems, and Azure AI — distilled from the public shape of a third-party Microsoft-ecosy' },
    { code: 'IL-19', name: 'MultiCloud, DevOps & AI Bootcamp', hours: 328, tagline: 'Four clouds. One discipline. Noah-tutored.', blurb: 'A hands-on, self-paced bootcamp spanning computing fundamentals, four cloud platforms (AWS, Azure, Google Cloud, Oracle Cloud), DevOps, and AI — plus certification maps, three guided missions, and a f' },
    { code: 'IL-20', name: 'Mathematics for Engineers & Scientists', hours: 72, tagline: 'Discrete math to numerical methods — the math working engineers actually use.', blurb: 'The mathematical spine of engineering and science: sixteen modules from sets, logic, and proofs through linear algebra, calculus, probability, statistics, and numerical methods. Four executable Python' },
    { code: 'IL-21', name: 'Humanities for Technologists', hours: 52, tagline: 'Philosophy, history, writing, economics — the disciplines of judgment.', blurb: 'Philosophy, history, writing, rhetoric, economics, and law as working disciplines for builders: logic and fallacies, three ethical traditions plus applied technology ethics, epistemology and the repli' },
    { code: 'IL-22', name: 'The Deep Library — Esoteric & Secret Knowledge', hours: 58, tagline: 'The mystery traditions, studied as traditions — scholarly, never credulous.', blurb: 'The deep occult library: sixteen modules on the Western mystery traditions and their counterparts — Kabbalah, Hermeticism, alchemy, astrology, tarot, Enochian magic, Rosicrucianism, Theosophy, the Gol' },
    { code: 'IL-23', name: 'The Frontier — Cutting-Edge Research Distilled', hours: 34, tagline: 'Fast-moving fields, honestly dated — the durable core plus the method.', blurb: 'Cutting-edge research distilled: ten seed modules on the durable core of fast-moving fields — transformers, quantum computing, CRISPR, fusion, brain–computer interfaces, AI agents, semiconductors, syn' },
    { code: 'IL-24', name: 'ThreatLocker Assessment Prep CBT', hours: 70, tagline: 'Zero Trust endpoint defense + security graphs + AI-aided SOC — an assessment-style computer-based training course', blurb: 'A full assessment-preparation CBT built the Interstitium way: instructor-voice lessons, hands-on labs, timed drills, branching scenarios, and a 120-minute mock circuit. You will learn ThreatLocker\'s d' },
    { code: 'IL-25', name: 'Professional Cybersecurity Certificate Prep', hours: 111, tagline: 'Think like an attacker. Defend like a professional.', blurb: 'IL-25 is a 96-hour independent practice course aligned to the public topic map of a well-known 24-week professional cybersecurity certificate program. Across three phases — risk and governance foundat' },
    { code: 'IL-26', name: 'Data Analyst Certification & Senior Mastery', hours: 414, tagline: 'From zero to senior-ready: math, SQL, stats, certs, portfolio — calibrated to the Palantir & BNY Mellon hiring bar.', blurb: 'IL-26 is a 414-hour independent practice course for data analysts, sequenced strictly from zero: a math-foundations track (arithmetic through calculus concepts), then SQL and Python, statistics and A/' },
    { code: 'IL-27', name: 'IT Infrastructure Specialist — Zero Trust Infrastructure', hours: 252, tagline: 'From first principles to Zero Trust: the complete infrastructure skill set, interview-ready.', blurb: 'An enterprise-grade, self-paced mastery course covering the full IT infrastructure stack through a Zero Trust lens: hardware and Windows/Linux administration, TCP/IP and subnetting math, Windows Serve' },
    { code: 'IL-28', name: 'DevSecOps & Cloud Infrastructure — Production Mastery', hours: 473, tagline: 'From zero to production: math, Linux, networking, containers, IaC, clouds, DevSecOps — calibrated to the BNY DevOps panel bar.', blurb: 'IL-28 is an independent, interactive DevSecOps and cloud-infrastructure bootcamp built from real BNY/BNY Mellon DevOps panel interview sessions. It runs zero-to-production: foundational math (binary, ' },
    { code: 'IL-29', name: 'ThreatLocker Zero-Trust CBT with AI — Cybersecurity Mastery', hours: 431, tagline: 'Zero-trust endpoint defense at operator depth — ThreatLocker mastery, MIT-grade security reasoning, AI-augmented triage, and interview-day readiness.', blurb: 'IL-29 is a cybersecurity mastery bootcamp built around zero-trust endpoint defense: you will operate allowlisting, ringfencing, elevation control, storage control, network control, and Detect triage t' },
    { code: 'IL-30', name: 'Post-Quantum Cryptography & Quantum-Safe Engineering', hours: 165, tagline: 'Quantum-safe cryptography at engineering depth — NIST\'s PQC standards, lattice and hash-based math, hybrid TLS, and a real migration playbook.', blurb: 'IL-30 is the quantum-safe engineering course built on NIST\'s finalized post-quantum cryptography standards: FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), and FIPS 205 (SLH-DSA), published August 2024. You wil' },
    { code: 'IL-31', name: 'AI Red-Teaming & Safety Evals Engineering', hours: 100, tagline: 'Evaluate, red-team, and harden frontier AI systems — the measurement discipline behind safe AI deployment.', blurb: 'The AI industry learned to build agents faster than it learned to measure them. This course is the missing half: how to design evaluations that honestly measure what frontier AI systems can and cannot' },
  ];

  /* ---------- catalog loader (sharded: data/catalog/index.json lists shards;
       merged here; graceful: never throws into page code) ---------- */
  var catalogState = { data: null, error: null, offline: false };

  function emptyCatalog() {
    return { academies: [], paths: [], _empty: true };
  }

  function fetchJson(url) {
    return fetch(url, { credentials: 'same-origin' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status + ' for ' + url);
      return r.json();
    });
  }

  function loadCatalog() {
    return fetchJson('data/catalog/index.json')
      .then(function (manifest) {
        var shards = (manifest && manifest.shards) || [];
        if (!shards.length) throw new Error('empty catalog manifest');
        /* 2026-10-09: resilient shard loading — one failing shard no longer kills
           the entire catalog. Each shard loads independently; failures are logged
           and skipped, so a single 404/403 can't blank every academy page. */
        return Promise.all(shards.map(function (s) {
          return fetchJson('data/catalog/' + s).catch(function (err) {
            if (window.console && console.warn) console.warn('[IL catalog] shard failed, skipped:', s, err && err.message);
            return null;
          });
        }));
      })
      .then(function (parts) {
        var academies = [], paths = [];
        parts.forEach(function (json) {
          json = json || {};
          if (Array.isArray(json.academies)) academies = academies.concat(json.academies);
          if (Array.isArray(json.paths)) paths = paths.concat(json.paths);
        });
        catalogState.data = { academies: academies, paths: paths, _empty: false };
        // Fall back to the verified academy index only if the catalog ships none.
        if (!catalogState.data.academies.length) {
          catalogState.data.academies = FALLBACK_ACADEMIES.slice();
          catalogState.data._academiesFallback = true;
        }
        document.dispatchEvent(new CustomEvent('il:catalog', { detail: catalogState.data }));
        return catalogState.data;
      })
      .catch(function (err) {
        catalogState.error = err;
        catalogState.offline = true;
        catalogState.data = emptyCatalog();
        catalogState.data.academies = FALLBACK_ACADEMIES.slice();
        catalogState.data._academiesFallback = true;
        document.dispatchEvent(new CustomEvent('il:catalog', { detail: catalogState.data }));
        return catalogState.data;
      });
  }

  IL.ready = loadCatalog();
  IL.catalogState = catalogState;
  IL.getCatalog = function () { return catalogState.data || emptyCatalog(); };
  IL.isCatalogOffline = function () { return catalogState.offline; };
  IL.onCatalog = function (fn) {
    if (catalogState.data) fn(catalogState.data);
    else document.addEventListener('il:catalog', function h(e) {
      document.removeEventListener('il:catalog', h);
      fn(e.detail);
    });
  };

  /* ---------- catalog accessors (all null-safe) ---------- */
  IL.academies = function () { return IL.getCatalog().academies || []; };
  IL.paths = function () { return IL.getCatalog().paths || []; };

  IL.academyByCode = function (code) {
    return IL.academies().find(function (a) { return a.code === code; }) || null;
  };

  IL.pathById = function (id) {
    return IL.paths().find(function (p) { return p.id === id; }) || null;
  };

  IL.pathsForAcademy = function (code) {
    return IL.paths().filter(function (p) { return p.academy === code; });
  };

  IL.assessments = function () {
    var out = [];
    IL.paths().forEach(function (p) {
      (p.assessments || []).forEach(function (a) {
        out.push(Object.assign({ pathId: p.id, pathTitle: p.title }, a));
      });
    });
    return out;
  };

  IL.assessmentById = function (id) {
    return IL.assessments().find(function (a) { return a.id === id; }) || null;
  };

  IL.totalHours = function () {
    return IL.academies().reduce(function (s, a) { return s + (Number(a.hours) || 0); }, 0);
  };

  IL.allTags = function () {
    var set = {};
    IL.paths().forEach(function (p) { (p.tags || []).forEach(function (t) { set[t] = 1; }); });
    return Object.keys(set).sort();
  };

  /* ---------- path filtering: role/skill/cert/time ---------- */
  // f = { q, type, tag, maxHours }
  IL.filterPaths = function (paths, f) {
    f = f || {};
    var q = (f.q || '').trim().toLowerCase();
    return (paths || []).filter(function (p) {
      if (f.type && p.type !== f.type) return false;
      if (f.tag && (p.tags || []).indexOf(f.tag) === -1) return false;
      if (f.maxHours && Number(p.hours) > Number(f.maxHours)) return false;
      if (q) {
        var hay = [p.title, p.subtitle, p.id, (p.tags || []).join(' '), p.academy]
          .join(' ').toLowerCase();
        // every query token must appear somewhere (skill/role/cert free text)
        var ok = q.split(/\s+/).every(function (tok) { return hay.indexOf(tok) !== -1; });
        if (!ok) return false;
      }
      return true;
    });
  };

  /* ---------- shared header ---------- */
  var NAV = [
    ['index.html', 'Home'],
    ['tracks.html', 'Tracks'],
    ['paths.html', 'Paths'],
    ['assess.html', 'Assessments'],
    ['courses.html', 'My Courses'],
    ['enroll.html', 'Enroll'],
    ['honesty.html', 'Honesty'],
    ['about.html', 'About'],
    ['https://interstitiumlabs.dev/', 'Main Site \u2197']
  ];

  function currentPage() {
    var p = window.location.pathname.split('/').pop() || 'index.html';
    return p.split('?')[0].split('#')[0] || 'index.html';
  }

  /* sub-pages that are not in NAV map to their parent tab for aria-current */
  var NAV_PARENT = {
    'path.html': 'paths.html',
    'academy.html': 'paths.html',
    'lab-generative-packing.html': 'paths.html',
    'learn.html': 'index.html'
  };

  /* 2026-10-08 (scope fix, BUG 3): the SAME floating pill nav as the main
     site (docs/index.html) — same brand lockup, same link set, same
     styling (university/css/il-pillnav.css), same zero-JS mobile
     <details> collapse. Absolute URLs so it works at any path depth.
     il-theme.js injects its toggle into .il-pillnav__row automatically. */
  var PILL_LINKS = [
    ['https://interstitiumlabs.dev/university/', 'Courses'],
    ['https://interstitiumlabs.dev/topics/', 'Topics'],
    ['https://interstitiumlabs.dev/prep/drills/', 'Practice'],
    ['https://interstitiumlabs.dev/noah/', 'Noah AI'],
    ['https://interstitiumlabs.dev/jobs/', 'Jobs'],
    ['https://interstitiumlabs.dev/about/', 'About']
  ];

  function renderHeader() {
    var host = document.getElementById('il-header');
    if (!host) return;
    var links = PILL_LINKS.map(function (item) {
      var cur = item[1] === 'Courses' ? ' aria-current="page"' : '';
      return '<a href="' + item[0] + '"' + cur + '>' + item[1] + '</a>';
    }).join('');
    var sheetLinks = PILL_LINKS.map(function (item) {
      var cur = item[1] === 'Courses' ? ' aria-current="page"' : '';
      return '<a href="' + item[0] + '"' + cur + '>' + item[1] + '</a>';
    }).join('') + '<a href="https://interstitiumlabs.dev/enroll/">Enroll</a>';
    host.innerHTML =
      '<nav class="il-pillnav" aria-label="Primary">' +
      '<div class="il-pillnav__row">' +
      '<a class="il-brand" href="https://interstitiumlabs.dev/" aria-label="Interstitium Labs home">' +
      '<img src="/assets/chrome/sigil-glyph.svg" alt="" width="38" height="38"/>' +
      '<span class="il-brand__word">Interstitium Labs<small>SCIENTIA OMNIA VINCIT</small></span></a>' +
      '<div class="il-pillnav__links">' + links + '</div>' +
      '<div style="display:flex;align-items:center;gap:.5rem">' +
      '<button type="button" class="il-search__btn" data-il-search-open aria-label="Search the site (press /)">' +
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg></button>' +
      '<details class="il-menu"><summary aria-label="Open menu">MENU</summary>' +
      '<div class="il-menu__sheet">' + sheetLinks + '</div></details>' +
      '<a class="il-btn il-btn--gold il-btn--small" href="https://interstitiumlabs.dev/enroll/">Enroll</a>' +
      '</div></div></nav>';
  }

  

  /* ---------- graceful catalog-offline notice ---------- */
  function renderOfflineNotices() {
    if (!catalogState.offline) return;
    document.querySelectorAll('[data-catalog-slot]').forEach(function (slot) {
      if (slot.dataset.offlineRendered) return;
      slot.dataset.offlineRendered = '1';
      var n = el('div', { 'class': 'notice', role: 'status' });
      n.innerHTML = '<strong>Catalog offline.</strong> The curriculum data could not be loaded ' +
        '(it is still being published). What you see below is the standing academy index. ' +
        'Retry by reloading the page — nothing here is fabricated.';
      slot.insertBefore(n, slot.firstChild);
    });
  }

  /* ---------- scroll reveal (Palantir pass) ---------- */
  /* Explicit user motion choice (il_motion_reduced: '1'/'0') wins over the OS
     preference; with no saved choice the OS preference decides. Read live —
     the hero's motion toggle can change it mid-session. Mirrors hero.js. */
  function userReducedMotion() {
    try {
      var saved = localStorage.getItem('il_motion_reduced');
      if (saved === '1') return true;
      if (saved === '0') return false;
    } catch (e) {}
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }
  function syncMotionDataset() {
    try { document.documentElement.dataset.motion = userReducedMotion() ? 'reduced' : 'full'; } catch (e) {}
  }

  function initReveals() {
    document.documentElement.classList.add('js');
    if (userReducedMotion() || !('IntersectionObserver' in window)) {
      document.querySelectorAll('.il-reveal').forEach(function (n) { n.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        // Live check: a mid-session "Reduce motion" choice stills new reveals.
        if (userReducedMotion()) { e.target.classList.add('in'); io.unobserve(e.target); return; }
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    function tag(scope) {
      var items = (scope || document).querySelectorAll(
        'main#il-main > section.block, .card, .module, .notice, .counters .counter, .terminal-storm'
      );
      items.forEach(function (n) {
        if (n.classList.contains('il-reveal')) return;
        n.classList.add('il-reveal');
        // stagger siblings sharing a parent
        var sibs = n.parentElement ? n.parentElement.querySelectorAll(':scope > .il-reveal') : [];
        var pos = sibs.length ? Array.prototype.indexOf.call(sibs, n) : 0;
        n.style.setProperty('--reveal-delay', String((pos % 6) * 55) + 'ms');
        io.observe(n);
      });
    }
    tag(document);
    // re-tag after dynamic catalog renders
    document.addEventListener('il:catalog', function () { setTimeout(function () { tag(document); }, 30); });
  }

  /* ---------- animated counters ---------- */
  var countUpIO = null;
  var countUpSeen = (typeof WeakSet !== 'undefined') ? new WeakSet() : null;
  function watchCountUps(scope) {
    if (!countUpIO) return;
    (scope || document).querySelectorAll('[data-countup]').forEach(function (n) {
      if (countUpSeen && countUpSeen.has(n)) return;
      if (countUpSeen) countUpSeen.add(n);
      countUpIO.observe(n);
    });
  }
  function initCountUp() {
    function animate(n) {
      var raw = (n.getAttribute('data-countup') || n.textContent || '').replace(/[^0-9]/g, '');
      var target = parseInt(raw, 10);
      if (!target || userReducedMotion()) return;
      var t0 = null, dur = 1100;
      function frame(t) {
        if (!t0) t0 = t;
        var p = Math.min((t - t0) / dur, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        n.textContent = Math.round(target * eased).toLocaleString('en-US');
        if (p < 1) requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    }
    if (!('IntersectionObserver' in window) || !('WeakSet' in window)) return;
    countUpIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { animate(e.target); countUpIO.unobserve(e.target); }
      });
    }, { threshold: 0.4 });
    watchCountUps(document);
    // counters render when the catalog lands — watch then too
    document.addEventListener('il:catalog', function () { setTimeout(function () { watchCountUps(document); }, 30); });
  }

  /* ---------- page transition veil ---------- */
  function initVeil() {
    var veil = document.createElement('div');
    veil.id = 'il-veil';
    veil.setAttribute('aria-hidden', 'true');
    document.body.appendChild(veil);
    if (userReducedMotion()) return;
    document.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a[href]') : null;
      if (!a) return;
      var href = a.getAttribute('href');
      if (!href || href.charAt(0) === '#' || a.target === '_blank' || a.hasAttribute('download')) return;
      var url;
      try { url = new URL(href, window.location.href); } catch (err) { return; }
      if (url.origin !== window.location.origin) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      document.body.classList.add('il-leaving');
      setTimeout(function () { window.location.href = url.href; }, 170);
    });
  }

  /* ---------- hero parallax (subtle; pantheon cinematic) ---------- */
  var parallaxOff = null;
  function initParallax() {
    if (userReducedMotion()) return;
    var sigil = document.querySelector('.pantheon-sigil');
    var copy = document.querySelector('.pantheon-copy');
    if (!sigil && !copy) return;
    var ticking = false;
    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.scrollY || 0;
        if (y < window.innerHeight * 1.2) {
          if (sigil) sigil.style.transform = 'translateY(' + (y * 0.12).toFixed(1) + 'px)';
          if (copy) copy.style.transform = 'translateY(' + (y * 0.06).toFixed(1) + 'px)';
        }
        ticking = false;
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    parallaxOff = function () { window.removeEventListener('scroll', onScroll); parallaxOff = null; };
  }

  /* ---------- command palette loader ---------- */
  function loadPalette() {
    var s = document.createElement('script');
    s.src = 'js/palette.js';
    s.defer = true;
    s.onerror = function () { /* palette is enhancement-only; never break chrome */ };
    document.body.appendChild(s);
  }

  /* ---------- boot ---------- */
  function boot() {
    renderHeader();
    syncMotionDataset(); // pages without hero.js still honor the persisted choice
    initReveals();
    initCountUp();
    initVeil();
    initParallax();
    loadPalette();
    // A mid-session toggle from the hero stills the rest of the page too.
    window.addEventListener('il:motionchange', function () {
      syncMotionDataset();
      if (userReducedMotion() && parallaxOff) parallaxOff();
    });
    IL.ready.then(renderOfflineNotices);
    // Re-run page render hooks when the catalog arrives.
    document.addEventListener('il:catalog', function () {
      if (typeof IL.renderPage === 'function') {
        try { IL.renderPage(); } catch (e) { /* page-level errors must not break chrome */ }
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
