/* =====================================================================
 * Interstitium Labs — Noah AI Adaptive Learning Engine (2026-10-09)
 *
 * Bleeding-edge personalized tutoring:
 *
 *  1. ADAPTIVE LEARNING — tracks per-topic mastery from quiz/drill
 *     interactions, identifies weak areas, adjusts difficulty.
 *
 *  2. PERSONALIZED LEARNING PATHS — recommends modules based on
 *     performance gaps and prerequisites.
 *
 *  3. SPACED REPETITION — SM-2-inspired scheduler for review timing.
 *
 *  4. LEARNING STYLE DETECTION — analyzes interaction patterns to detect
 *     visual / hands-on / theoretical / socratic preferences.
 *
 *  5. PROGRESS ANALYTICS — dashboard showing strengths, gaps, focus areas.
 *
 *  6. SOCRATIC DEPTH CONTROL — user-adjustable questioning depth (1-5).
 *
 *  7. SESSION MEMORY — persistent cross-session recall of topics covered,
 *     concepts mastered, and open threads.
 *
 * All data stored device-local (localStorage). No cloud sync. Privacy-first.
 * Integrates with course JSON data and existing Noah widget.
 * ===================================================================== */
(function (g) {
  'use strict';

  var PROFILE_KEY = 'noah-adaptive-profile-v1';
  var MAX_TOPICS = 200;
  var MAX_SESSIONS = 50;

  var ADAPTIVE_CSS = [
    '#noah-adaptive-row{display:flex;gap:6px;padding:6px 14px;border-bottom:1px solid rgba(255,255,255,.06);',
    'background:rgba(0,0,0,.2);align-items:center;flex-wrap:wrap;}',
    '.noah-adaptive-label{font-size:10px;color:#7d8ea3;letter-spacing:.08em;text-transform:uppercase;}',
    '#noah-depth-slider{flex:1;min-width:80px;accent-color:#d4af37;}',
    '#noah-depth-val{font-size:11px;color:#d4af37;min-width:80px;}',
    '#noah-analytics-btn{background:rgba(212,175,55,.1);border:1px solid rgba(212,175,55,.3);',
    'border-radius:8px;color:#d4af37;font-size:11px;padding:4px 10px;cursor:pointer;}',
    '#noah-analytics-btn:hover{background:rgba(212,175,55,.2);}',
    '#noah-analytics-panel{max-height:300px;overflow-y:auto;padding:12px 14px;',
    'border-bottom:1px solid rgba(255,255,255,.06);background:rgba(0,0,0,.3);display:none;}',
    '#noah-analytics-panel.open{display:block;}',
    '.noah-topic-bar{display:flex;align-items:center;gap:8px;margin:4px 0;font-size:11px;}',
    '.noah-topic-name{flex:0 0 140px;color:#a5b8cc;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}',
    '.noah-topic-track{flex:1;height:6px;background:rgba(255,255,255,.08);border-radius:3px;overflow:hidden;}',
    '.noah-topic-fill{height:100%;border-radius:3px;transition:width .3s;}',
    '.noah-topic-pct{flex:0 0 36px;text-align:right;color:#7d8ea3;}',
    '.noah-review-item{display:flex;justify-content:space-between;align-items:center;',
    'padding:6px 0;border-bottom:1px solid rgba(255,255,255,.04);font-size:11px;}',
    '.noah-review-due{color:#f87171;font-size:10px;}',
    '.noah-review-soon{color:#fbbf24;font-size:10px;}',
    '.noah-style-badge{display:inline-block;background:rgba(34,211,238,.12);border:1px solid rgba(34,211,238,.3);',
    'border-radius:999px;color:#a5e8fc;font-size:10px;padding:2px 10px;margin:2px;}',
    '.noah-section-title{font-size:10px;color:#7d8ea3;letter-spacing:.08em;text-transform:uppercase;',
    'margin:10px 0 6px;}',
  ].join('\n');

  /* ---------- Profile store ---------- */

  function defaultProfile() {
    return {
      v: 1,
      topics: {},           // topicId -> { mastery: 0-1, attempts: n, correct: n, lastSeen: ts, easiness: 2.5, interval: 1, repetitions: 0, nextReview: ts }
      sessions: [],         // [{ id, startedAt, topicsCovered: [], depth: n }]
      learningStyle: {      // detected weights 0-1
        visual: 0.5,
        handsOn: 0.5,
        theoretical: 0.5,
        socratic: 0.5,
      },
      styleSignals: { visual: 0, handsOn: 0, theoretical: 0, socratic: 0 },
      socraticDepth: 3,     // 1-5, user adjustable
      totalInteractions: 0,
      weakAreas: [],        // computed
      strongAreas: [],      // computed
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
  }

  function loadProfile() {
    try {
      var raw = g.localStorage && g.localStorage.getItem(PROFILE_KEY);
      if (raw) {
        var p = JSON.parse(raw);
        if (p && p.v === 1) return p;
      }
    } catch (e) {}
    return defaultProfile();
  }

  function saveProfile(p) {
    p.updatedAt = Date.now();
    try {
      if (g.localStorage) g.localStorage.setItem(PROFILE_KEY, JSON.stringify(p));
    } catch (e) {}
    return p;
  }

  var profile = loadProfile();

  /* ---------- Topic mastery tracking ---------- */

  /**
   * Record a quiz/drill attempt.
   * @param {string} topicId - topic identifier (e.g. "il-29:module-03:zero-trust")
   * @param {boolean} correct - whether the answer was correct
   * @param {string} interactionType - 'quiz' | 'drill' | 'lab' | 'discussion'
   */
  function recordAttempt(topicId, correct, interactionType) {
    if (!topicId) return;
    var t = profile.topics[topicId] || {
      mastery: 0.5, attempts: 0, correct: 0, lastSeen: 0,
      easiness: 2.5, interval: 1, repetitions: 0, nextReview: Date.now(),
    };

    t.attempts++;
    if (correct) t.correct++;
    t.lastSeen = Date.now();

    // Update mastery: weighted moving average
    var alpha = 0.3; // learning rate
    var target = correct ? 1.0 : 0.0;
    // Partial credit for drills/labs (they're harder)
    if (!correct && (interactionType === 'drill' || interactionType === 'lab')) {
      target = 0.3; // attempted hard content counts partially
    }
    t.mastery = t.mastery * (1 - alpha) + target * alpha;
    t.mastery = Math.max(0, Math.min(1, t.mastery));

    // SM-2 spaced repetition update
    updateSpacedRepetition(t, correct ? 4 : 1); // quality 4=good, 1=wrong

    // Cap topics
    var keys = Object.keys(profile.topics);
    if (keys.length >= MAX_TOPICS && !profile.topics[topicId]) {
      // Evict least-recently-seen
      var oldest = keys[0], oldestTime = Infinity;
      keys.forEach(function (k) {
        if (profile.topics[k].lastSeen < oldestTime) {
          oldestTime = profile.topics[k].lastSeen;
          oldest = k;
        }
      });
      delete profile.topics[oldest];
    }

    profile.topics[topicId] = t;
    profile.totalInteractions++;

    // Update learning style signals based on interaction type
    updateStyleSignals(interactionType, correct);

    // Recompute weak/strong areas
    recomputeAreas();

    saveProfile(profile);
  }

  /**
   * SM-2 spaced repetition algorithm.
   * @param {object} t - topic record
   * @param {number} quality - 0-5 (0=total blackout, 5=perfect)
   */
  function updateSpacedRepetition(t, quality) {
    if (quality >= 3) {
      if (t.repetitions === 0) {
        t.interval = 1;
      } else if (t.repetitions === 1) {
        t.interval = 6;
      } else {
        t.interval = Math.round(t.interval * t.easiness);
      }
      t.repetitions++;
    } else {
      t.repetitions = 0;
      t.interval = 1;
    }

    t.easiness = t.easiness + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
    t.easiness = Math.max(1.3, t.easiness);

    t.nextReview = Date.now() + (t.interval * 24 * 60 * 60 * 1000);
  }

  /**
   * Get topics due for review (nextReview <= now), sorted by urgency.
   */
  function getDueReviews() {
    var now = Date.now();
    var due = [];
    Object.keys(profile.topics).forEach(function (id) {
      var t = profile.topics[id];
      if (t.nextReview <= now && t.attempts > 0) {
        due.push({
          id: id,
          mastery: t.mastery,
          overdue: now - t.nextReview,
          repetitions: t.repetitions,
        });
      }
    });
    due.sort(function (a, b) { return b.overdue - a.overdue; });
    return due;
  }

  /**
   * Get topics due soon (within 48h).
   */
  function getUpcomingReviews() {
    var now = Date.now();
    var soon = [];
    Object.keys(profile.topics).forEach(function (id) {
      var t = profile.topics[id];
      var in48h = now + (48 * 60 * 60 * 1000);
      if (t.nextReview > now && t.nextReview <= in48h && t.attempts > 0) {
        soon.push({ id: id, mastery: t.mastery, dueIn: t.nextReview - now });
      }
    });
    soon.sort(function (a, b) { return a.dueIn - b.dueIn; });
    return soon;
  }

  /* ---------- Learning style detection ---------- */

  var STYLE_MAP = {
    video: 'visual',
    diagram: 'visual',
    image: 'visual',
    lab: 'handsOn',
    drill: 'handsOn',
    terminal: 'handsOn',
    handsOnLab: 'handsOn',
    reading: 'theoretical',
    text: 'theoretical',
    theory: 'theoretical',
    quiz: 'socratic',
    discussion: 'socratic',
    socratic: 'socratic',
  };

  function updateStyleSignals(interactionType, correct) {
    var style = STYLE_MAP[interactionType] || 'theoretical';
    profile.styleSignals[style] = (profile.styleSignals[style] || 0) + 1;

    // Normalize to 0-1 weights
    var total = Object.keys(profile.styleSignals).reduce(function (s, k) {
      return s + profile.styleSignals[k];
    }, 0);
    if (total > 0) {
      Object.keys(profile.learningStyle).forEach(function (k) {
        profile.learningStyle[k] = (profile.styleSignals[k] || 0) / total;
      });
    }
  }

  function getDominantStyle() {
    var best = 'theoretical', bestVal = 0;
    Object.keys(profile.learningStyle).forEach(function (k) {
      if (profile.learningStyle[k] > bestVal) {
        bestVal = profile.learningStyle[k];
        best = k;
      }
    });
    return { style: best, confidence: bestVal };
  }

  /**
   * Record a content interaction (not just quiz attempts).
   * Used for style detection from page behavior.
   */
  function recordInteraction(type, topicId, metadata) {
    updateStyleSignals(type, true);
    if (topicId && profile.topics[topicId]) {
      profile.topics[topicId].lastSeen = Date.now();
    }
    profile.totalInteractions++;
    saveProfile(profile);
  }

  /* ---------- Weak/strong area analysis ---------- */

  function recomputeAreas() {
    var topics = Object.keys(profile.topics).map(function (id) {
      return { id: id, mastery: profile.topics[id].mastery, attempts: profile.topics[id].attempts };
    }).filter(function (t) { return t.attempts >= 2; }); // need minimum data

    topics.sort(function (a, b) { return a.mastery - b.mastery; });

    profile.weakAreas = topics.filter(function (t) { return t.mastery < 0.5; })
      .slice(0, 10).map(function (t) { return t.id; });
    profile.strongAreas = topics.filter(function (t) { return t.mastery >= 0.8; })
      .slice(-10).map(function (t) { return t.id; });
  }

  /* ---------- Personalized recommendations ---------- */

  /**
   * Generate learning path recommendations based on profile.
   * Returns array of { topicId, reason, priority }
   */
  function getRecommendations(courseData) {
    var recs = [];
    var due = getDueReviews();

    // Priority 1: overdue reviews
    due.slice(0, 5).forEach(function (r) {
      recs.push({
        topicId: r.id,
        reason: 'review',
        priority: 1,
        detail: 'Due for spaced review (' + r.repetitions + ' prior reviews)',
      });
    });

    // Priority 2: weak areas
    profile.weakAreas.slice(0, 5).forEach(function (id) {
      if (!recs.some(function (r) { return r.topicId === id; })) {
        recs.push({
          topicId: id,
          reason: 'weakness',
          priority: 2,
          detail: 'Needs reinforcement (' + Math.round(profile.topics[id].mastery * 100) + '% mastery)',
        });
      }
    });

    // Priority 3: prerequisites for weak areas (if course data available)
    // This would need course module graph — simplified for now

    return recs.sort(function (a, b) { return a.priority - b.priority; });
  }

  /* ---------- Session memory ---------- */

  function startSession() {
    var session = {
      id: 's-' + Date.now().toString(36),
      startedAt: Date.now(),
      topicsCovered: [],
      depth: profile.socraticDepth,
      persona: null, // set by personas module
    };
    profile.sessions.push(session);
    if (profile.sessions.length > MAX_SESSIONS) {
      profile.sessions = profile.sessions.slice(-MAX_SESSIONS);
    }
    saveProfile(profile);
    return session;
  }

  function getCurrentSession() {
    if (!profile.sessions.length) return startSession();
    var last = profile.sessions[profile.sessions.length - 1];
    // Session expires after 4 hours of inactivity
    if (Date.now() - last.startedAt > 4 * 60 * 60 * 1000) return startSession();
    return last;
  }

  function recordTopicCovered(topicId) {
    var session = getCurrentSession();
    if (session.topicsCovered.indexOf(topicId) === -1) {
      session.topicsCovered.push(topicId);
      saveProfile(profile);
    }
  }

  /**
   * Get cross-session memory summary for the AI context.
   */
  function getMemorySummary() {
    var recentSessions = profile.sessions.slice(-5);
    var allTopics = {};
    recentSessions.forEach(function (s) {
      s.topicsCovered.forEach(function (t) { allTopics[t] = true; });
    });

    return {
      topicsCovered: Object.keys(allTopics),
      weakAreas: profile.weakAreas,
      strongAreas: profile.strongAreas,
      dominantStyle: getDominantStyle(),
      socraticDepth: profile.socraticDepth,
      totalInteractions: profile.totalInteractions,
      dueReviews: getDueReviews().length,
    };
  }

  /* ---------- Adaptive context for AI ---------- */

  /**
   * Build the adaptive context string to inject into the AI system prompt.
   */
  function buildAdaptiveContext() {
    var mem = getMemorySummary();
    var parts = [];

    parts.push('LEARNER PROFILE (adaptive):');

    if (mem.topicsCovered.length) {
      parts.push('- Topics covered in recent sessions: ' + mem.topicsCovered.slice(0, 10).join(', '));
    }
    if (mem.weakAreas.length) {
      parts.push('- WEAK AREAS (prioritize these): ' + mem.weakAreas.slice(0, 5).join(', '));
    }
    if (mem.strongAreas.length) {
      parts.push('- Strong areas (can skip or go deeper): ' + mem.strongAreas.slice(0, 5).join(', '));
    }

    var style = mem.dominantStyle;
    var styleAdvice = {
      visual: 'Use diagrams, visual analogies, and spatial descriptions.',
      handsOn: 'Emphasize practical exercises, code examples, and "try it" prompts.',
      theoretical: 'Provide rigorous explanations, formal definitions, and proofs.',
      socratic: 'Lead with questions. Guide discovery rather than telling.',
    };
    parts.push('- Detected learning style: ' + style.style + ' (' + Math.round(style.confidence * 100) + '% confidence). ' +
      (styleAdvice[style.style] || ''));

    var depthLabels = ['', 'Direct answers', 'Light guidance', 'Balanced Socratic', 'Deep questioning', 'Maximum inquiry'];
    parts.push('- Socratic depth preference: ' + mem.socraticDepth + '/5 (' + depthLabels[mem.socraticDepth] + '). ' +
      'At depth 1, give direct answers. At depth 5, never give answers — only questions.');

    if (mem.dueReviews > 0) {
      parts.push('- ' + mem.dueReviews + ' topics are due for spaced review. Consider weaving review into the conversation.');
    }

    parts.push('- Total interactions: ' + mem.totalInteractions + '. Adapt difficulty: if they are struggling, simplify; if excelling, challenge.');

    return parts.join('\n');
  }

  /* ---------- UI: Analytics dashboard ---------- */

  function renderAnalytics(container) {
    var mem = getMemorySummary();
    var html = '';

    // Learning style
    html += '<div class="noah-section-title">Learning Style</div>';
    var styleLabels = { visual: '👁️ Visual', handsOn: '🔧 Hands-on', theoretical: '📐 Theoretical', socratic: '❓ Socratic' };
    Object.keys(profile.learningStyle).forEach(function (k) {
      var pct = Math.round(profile.learningStyle[k] * 100);
      if (pct > 5) {
        html += '<span class="noah-style-badge">' + (styleLabels[k] || k) + ' ' + pct + '%</span>';
      }
    });

    // Topic mastery
    var topics = Object.keys(profile.topics)
      .map(function (id) { return { id: id, t: profile.topics[id] }; })
      .filter(function (x) { return x.t.attempts > 0; })
      .sort(function (a, b) { return b.t.mastery - a.t.mastery; });

    if (topics.length) {
      html += '<div class="noah-section-title">Topic Mastery</div>';
      topics.slice(0, 15).forEach(function (x) {
        var pct = Math.round(x.t.mastery * 100);
        var color = pct >= 80 ? '#34d399' : pct >= 50 ? '#fbbf24' : '#f87171';
        var shortId = x.id.length > 30 ? '...' + x.id.slice(-27) : x.id;
        html += '<div class="noah-topic-bar">' +
          '<span class="noah-topic-name" title="' + escapeHtml(x.id) + '">' + escapeHtml(shortId) + '</span>' +
          '<div class="noah-topic-track"><div class="noah-topic-fill" style="width:' + pct + '%;background:' + color + '"></div></div>' +
          '<span class="noah-topic-pct">' + pct + '%</span></div>';
      });
    } else {
      html += '<div class="noah-section-title">Topic Mastery</div>' +
        '<div style="font-size:11px;color:#7d8ea3;">No data yet — chat with Noah or complete quizzes to build your profile.</div>';
    }

    // Due reviews
    var due = getDueReviews();
    var soon = getUpcomingReviews();
    if (due.length || soon.length) {
      html += '<div class="noah-section-title">Spaced Reviews</div>';
      due.slice(0, 5).forEach(function (r) {
        var shortId = r.id.length > 35 ? '...' + r.id.slice(-32) : r.id;
        html += '<div class="noah-review-item"><span>' + escapeHtml(shortId) + '</span>' +
          '<span class="noah-review-due">OVERDUE</span></div>';
      });
      soon.slice(0, 3).forEach(function (r) {
        var shortId = r.id.length > 35 ? '...' + r.id.slice(-32) : r.id;
        var hours = Math.round(r.dueIn / (60 * 60 * 1000));
        html += '<div class="noah-review-item"><span>' + escapeHtml(shortId) + '</span>' +
          '<span class="noah-review-soon">in ' + hours + 'h</span></div>';
      });
    }

    // Stats
    html += '<div class="noah-section-title">Stats</div>' +
      '<div style="font-size:11px;color:#a5b8cc;">' +
      profile.totalInteractions + ' interactions · ' +
      Object.keys(profile.topics).length + ' topics tracked · ' +
      profile.sessions.length + ' sessions</div>';

    container.innerHTML = html;
  }

  function escapeHtml(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /* ---------- Quiz/Drill auto-detection ---------- */

  /**
   * Auto-detect quiz interactions on course pages.
   * Looks for common quiz/drill UI patterns.
   */
  function installQuizHooks() {
    // Hook 1: MutationObserver for quiz result indicators
    var observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (m) {
        // Look for elements indicating correct/incorrect answers
        m.addedNodes.forEach(function (node) {
          if (node.nodeType !== 1) return;
          var cls = (node.className || '').toString().toLowerCase();
          var text = (node.textContent || '').toLowerCase();

          var isCorrect = cls.includes('correct') && !cls.includes('incorrect') ||
                          text.includes('correct!') || text.includes('well done');
          var isIncorrect = cls.includes('incorrect') || cls.includes('wrong') ||
                            text.includes('incorrect') || text.includes('try again');

          if (isCorrect || isIncorrect) {
            var topicId = detectTopicFromPage();
            if (topicId) {
              recordAttempt(topicId, isCorrect, 'quiz');
            }
          }
        });
      });
    });

    try {
      observer.observe(document.body, { childList: true, subtree: true });
    } catch (e) {}

    // Hook 2: Click tracking for drill/lab buttons (for style detection)
    document.addEventListener('click', function (e) {
      var t = e.target;
      while (t && t !== document.body) {
        var cls = (t.className || '').toString().toLowerCase();
        var id = (t.id || '').toLowerCase();
        var combined = cls + ' ' + id;

        if (combined.includes('video') || combined.includes('play')) {
          recordInteraction('video', detectTopicFromPage());
          break;
        } else if (combined.includes('lab') || combined.includes('terminal') || combined.includes('drill')) {
          recordInteraction('lab', detectTopicFromPage());
          break;
        } else if (combined.includes('diagram')) {
          recordInteraction('diagram', detectTopicFromPage());
          break;
        }
        t = t.parentElement;
      }
    }, true);
  }

  function detectTopicFromPage() {
    try {
      // Try data attributes first
      var host = document.querySelector('[data-noah-lesson-id], [data-il-lesson-id], [data-lesson-id]');
      if (host) {
        var id = host.getAttribute('data-noah-lesson-id') ||
                 host.getAttribute('data-il-lesson-id') ||
                 host.getAttribute('data-lesson-id');
        if (id) return id;
      }
      // Try URL pattern
      var path = window.location.pathname;
      var courseMatch = path.match(/course[?=]([^&/]+)/);
      if (courseMatch) return 'course:' + courseMatch[1];
      // Fallback: page path
      return 'page:' + path.replace(/\//g, ':').slice(0, 60);
    } catch (e) { return null; }
  }

  /* ---------- Patch the widget ---------- */

  function patch() {
    var panel = document.getElementById('noah-panel');
    if (!panel) { setTimeout(patch, 500); return; }

    // Wait for personas row (from noah-personas.js)
    var personaRow = document.getElementById('noah-persona-row');
    if (!personaRow) { setTimeout(patch, 500); return; }

    var style = document.createElement('style');
    style.textContent = ADAPTIVE_CSS;
    document.head.appendChild(style);

    var msgs = panel.querySelector('#noah-msgs');
    if (!msgs) { setTimeout(patch, 500); return; }

    // --- Adaptive row: Socratic depth slider + Analytics button ---
    var adaptiveRow = document.createElement('div');
    adaptiveRow.id = 'noah-adaptive-row';

    var depthLabel = document.createElement('span');
    depthLabel.className = 'noah-adaptive-label';
    depthLabel.textContent = 'Depth';
    depthLabel.title = 'Socratic questioning depth: 1=direct answers, 5=questions only';

    var slider = document.createElement('input');
    slider.type = 'range';
    slider.id = 'noah-depth-slider';
    slider.min = '1';
    slider.max = '5';
    slider.step = '1';
    slider.value = String(profile.socraticDepth);
    slider.setAttribute('aria-label', 'Socratic depth');

    var depthVal = document.createElement('span');
    depthVal.id = 'noah-depth-val';
    var depthLabels = ['', 'Direct', 'Light', 'Balanced', 'Deep', 'Socratic'];
    depthVal.textContent = profile.socraticDepth + '/5 ' + depthLabels[profile.socraticDepth];

    slider.addEventListener('input', function () {
      profile.socraticDepth = parseInt(slider.value, 10);
      depthVal.textContent = profile.socraticDepth + '/5 ' + depthLabels[profile.socraticDepth];
      saveProfile(profile);
      // Update current session
      var session = getCurrentSession();
      session.depth = profile.socraticDepth;
      saveProfile(profile);
    });

    // Restore saved depth
    try {
      var saved = localStorage.getItem('noah-socratic-depth');
      if (saved) {
        profile.socraticDepth = Math.max(1, Math.min(5, parseInt(saved, 10) || 3));
        slider.value = String(profile.socraticDepth);
        depthVal.textContent = profile.socraticDepth + '/5 ' + depthLabels[profile.socraticDepth];
      }
    } catch (e) {}
    slider.addEventListener('change', function () {
      try { localStorage.setItem('noah-socratic-depth', String(profile.socraticDepth)); } catch (e) {}
    });

    var analyticsBtn = document.createElement('button');
    analyticsBtn.id = 'noah-analytics-btn';
    analyticsBtn.type = 'button';
    analyticsBtn.textContent = '📊 Progress';
    analyticsBtn.title = 'View learning analytics';

    adaptiveRow.appendChild(depthLabel);
    adaptiveRow.appendChild(slider);
    adaptiveRow.appendChild(depthVal);
    adaptiveRow.appendChild(analyticsBtn);

    panel.insertBefore(adaptiveRow, personaRow);

    // --- Analytics panel (collapsible) ---
    var analyticsPanel = document.createElement('div');
    analyticsPanel.id = 'noah-analytics-panel';
    panel.insertBefore(analyticsPanel, msgs);

    analyticsBtn.addEventListener('click', function () {
      var isOpen = analyticsPanel.classList.contains('open');
      if (isOpen) {
        analyticsPanel.classList.remove('open');
      } else {
        renderAnalytics(analyticsPanel);
        analyticsPanel.classList.add('open');
      }
    });

    // --- Patch fetch to include adaptive context ---
    var origFetch = g.fetch;
    g.fetch = function (url, opts) {
      if (typeof url === 'string' && url.indexOf('/api/noah') === 0 &&
          !url.startsWith('/api/noah-') && opts && opts.method === 'POST' && opts.body) {
        try {
          var body = JSON.parse(opts.body);
          body.adaptiveContext = buildAdaptiveContext();
          body.socraticDepth = profile.socraticDepth;
          // Record topics from the conversation for session memory
          if (body.messages && body.messages.length) {
            var lastUser = null;
            for (var i = body.messages.length - 1; i >= 0; i--) {
              if (body.messages[i].role === 'user') {
                lastUser = body.messages[i].content;
                break;
              }
            }
            if (lastUser) {
              // Simple topic extraction: record the conversation topic
              var topicHint = detectTopicFromPage() || 'chat:general';
              recordTopicCovered(topicHint);
            }
          }
          opts = Object.assign({}, opts, { body: JSON.stringify(body) });
        } catch (e) {}
      }
      return origFetch.call(this, url, opts);
    };

    // --- Install quiz auto-detection ---
    installQuizHooks();

    // --- Start session ---
    getCurrentSession();
  }

  // Start patching (after personas module)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(patch, 3000); });
  } else {
    setTimeout(patch, 3000);
  }

  // Public API
  g.IL = g.IL || {};
  g.IL.noahAdaptive = {
    recordAttempt: recordAttempt,
    recordInteraction: recordInteraction,
    getRecommendations: getRecommendations,
    getDueReviews: getDueReviews,
    getMemorySummary: getMemorySummary,
    getProfile: function () { return JSON.parse(JSON.stringify(profile)); },
    setSocraticDepth: function (d) {
      profile.socraticDepth = Math.max(1, Math.min(5, d));
      saveProfile(profile);
      var slider = document.getElementById('noah-depth-slider');
      if (slider) slider.value = String(profile.socraticDepth);
    },
    resetProfile: function () {
      profile = defaultProfile();
      saveProfile(profile);
    },
  };
})(window);
