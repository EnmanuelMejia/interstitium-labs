/**
 * IL Model Analytics — rolling scores + auto-promote + scale-relative-to-demand signals.
 *
 * Events → ILAnalytics (il.analytics.v1) and local il.insights.model.v1 / il.model.metrics.v1
 * Promote challenger when win-rate + latency thresholds met AND challenger is healthy.
 * Scale recommendations suggest next demand tier — never auto-buy hardware.
 */
(function (g) {
  'use strict';

  var METRICS_KEY = 'il.model.metrics.v1';
  var INSIGHTS_KEY = 'il.insights.model.v1';
  var MAX_EVENTS = 400;

  function read(key, fb) {
    try {
      var raw = g.localStorage.getItem(key);
      if (!raw) return fb;
      var p = JSON.parse(raw);
      return p && typeof p === 'object' ? p : fb;
    } catch (e) { return fb; }
  }

  function write(key, val) {
    try { g.localStorage.setItem(key, JSON.stringify(val)); } catch (e) {}
  }

  function emptyMetrics() {
    return { v: 1, events: [], byModel: {}, concurrencyHint: 0, updatedAt: Date.now() };
  }

  function loadMetrics() {
    var m = read(METRICS_KEY, null);
    if (m && m.v === 1) return m;
    return emptyMetrics();
  }

  function saveMetrics(m) {
    m.updatedAt = Date.now();
    if (m.events && m.events.length > MAX_EVENTS) m.events = m.events.slice(-MAX_EVENTS);
    write(METRICS_KEY, m);
    write(INSIGHTS_KEY, {
      v: 1,
      updatedAt: m.updatedAt,
      byModel: m.byModel,
      scale: m.lastScale || null,
      concurrencyHint: m.concurrencyHint || 0
    });
    return m;
  }

  function ensureModel(byModel, id) {
    if (!byModel[id]) {
      byModel[id] = {
        n: 0, ok: 0, fail: 0,
        latencies: [],
        thumbsUp: 0, thumbsDown: 0,
        wins: 0, explores: 0
      };
    }
    return byModel[id];
  }

  function percentile(sorted, p) {
    if (!sorted.length) return 0;
    var idx = Math.min(sorted.length - 1, Math.max(0, Math.ceil(p * sorted.length) - 1));
    return sorted[idx];
  }

  function rollingStats(row) {
    var lats = (row.latencies || []).slice().sort(function (a, b) { return a - b; });
    var n = row.n || 0;
    var ok = row.ok || 0;
    var thumbs = (row.thumbsUp || 0) + (row.thumbsDown || 0);
    var winRate = n ? ok / n : 0;
    if (thumbs >= 3) {
      winRate = 0.5 * winRate + 0.5 * ((row.thumbsUp || 0) / thumbs);
    }
    return {
      n: n,
      ok: ok,
      fail: row.fail || 0,
      errorRate: n ? (row.fail || 0) / n : 0,
      winRate: winRate,
      p50: percentile(lats, 0.5),
      p95: percentile(lats, 0.95),
      meanLatency: lats.length ? lats.reduce(function (a, b) { return a + b; }, 0) / lats.length : 0,
      thumbsUp: row.thumbsUp || 0,
      thumbsDown: row.thumbsDown || 0
    };
  }

  /** Pure scoring policy for promote decisions + node smoke tests. */
  function scoringPolicy(primaryStats, challengerStats, policy) {
    policy = policy || {};
    var minN = policy.min_samples || 8;
    var margin = policy.win_rate_margin != null ? policy.win_rate_margin : 0.08;
    var slack = policy.latency_slack_ms != null ? policy.latency_slack_ms : 1500;
    if (!primaryStats || !challengerStats) return { promote: false, reason: 'missing-stats' };
    if (challengerStats.n < minN || primaryStats.n < minN) {
      return { promote: false, reason: 'insufficient-samples', need: minN };
    }
    if (challengerStats.winRate < primaryStats.winRate + margin) {
      return {
        promote: false,
        reason: 'win-rate',
        primary: primaryStats.winRate,
        challenger: challengerStats.winRate,
        margin: margin
      };
    }
    var cLat = challengerStats.p95 || challengerStats.meanLatency || 0;
    var pLat = primaryStats.p95 || primaryStats.meanLatency || 0;
    if (cLat > pLat + slack) {
      return {
        promote: false,
        reason: 'latency',
        primaryP95: pLat,
        challengerP95: cLat,
        slack: slack
      };
    }
    return {
      promote: true,
      reason: 'challenger-better',
      winRate: challengerStats.winRate,
      latencyMs: cLat,
      primaryWinRate: primaryStats.winRate
    };
  }

  function record(evt) {
    if (!evt || !evt.modelId) return null;
    var m = loadMetrics();
    var now = Date.now();
    var entry = {
      t: now,
      modelId: evt.modelId,
      backendId: evt.backendId || '',
      latencyMs: evt.latencyMs || 0,
      ok: !!evt.ok,
      task: evt.task || 'chat',
      reason: evt.reason || '',
      demand_tier: evt.demand_tier || '',
      error: evt.error || null
    };
    m.events.push(entry);
    var row = ensureModel(m.byModel, evt.modelId);
    row.n += 1;
    if (evt.ok) {
      row.ok += 1;
      row.latencies.push(evt.latencyMs || 0);
      if (row.latencies.length > 100) row.latencies = row.latencies.slice(-100);
    } else {
      row.fail += 1;
    }
    if (evt.reason === 'auto-explore') row.explores += 1;
    var recent = m.events.filter(function (e) { return now - e.t < 60000; });
    m.concurrencyHint = recent.length;
    saveMetrics(m);
    if (g.ILAnalytics && g.ILAnalytics.track) {
      g.ILAnalytics.track('model_completion', {
        modelId: evt.modelId,
        backendId: evt.backendId,
        ok: !!evt.ok,
        latencyMs: evt.latencyMs || 0,
        demand_tier: evt.demand_tier || '',
        task: evt.task || 'chat'
      });
    }
    return entry;
  }

  function thumb(modelId, up) {
    var m = loadMetrics();
    var row = ensureModel(m.byModel, modelId);
    if (up) row.thumbsUp += 1;
    else row.thumbsDown += 1;
    saveMetrics(m);
    if (g.ILAnalytics && g.ILAnalytics.track) {
      g.ILAnalytics.track('model_thumb', { modelId: modelId, up: !!up });
    }
    return rollingStats(row);
  }

  function scores() {
    var m = loadMetrics();
    var out = {};
    Object.keys(m.byModel).forEach(function (id) {
      out[id] = rollingStats(m.byModel[id]);
    });
    return out;
  }

  function shouldPromote(policy) {
    policy = policy || {};
    var all = scores();
    var primary = policy.primary;
    var challengers = policy.challengers || [];
    if (!primary || !all[primary]) return { promote: false, reason: 'no-primary-stats' };
    var best = null;
    challengers.forEach(function (cid) {
      if (!all[cid]) return;
      var decision = scoringPolicy(all[primary], all[cid], policy);
      if (decision.promote) {
        if (!best || all[cid].winRate > ((all[best.challenger] && all[best.challenger].winRate) || 0)) {
          best = {
            promote: true,
            challenger: cid,
            winRate: decision.winRate,
            latencyMs: decision.latencyMs,
            primaryWinRate: decision.primaryWinRate
          };
        }
      }
    });
    return best || { promote: false, reason: 'no-challenger-ready' };
  }

  function scaleRecommendation(policy, catalog) {
    policy = policy || {};
    catalog = catalog || g.IL_MODEL_CATALOG || {};
    var defaults = catalog.defaults || {};
    var sig = defaults.scale_signals || {
      p95_latency_ms: 8000,
      error_rate: 0.15,
      concurrency_hint: 4,
      thumbs_down_rate: 0.25,
      window_events: 40
    };
    var m = loadMetrics();
    var tier = policy.demand_tier || 'T0';
    var tiers = catalog.demand_tiers || {};
    var tierInfo = tiers[tier] || {};
    var next = tierInfo.next_tier || null;
    var windowN = sig.window_events || 40;
    var recent = (m.events || []).slice(-windowN);
    if (recent.length < Math.min(10, windowN)) {
      return {
        suggest_tier: null,
        current_tier: tier,
        reason: 'insufficient-demand-sample',
        action: 'observe',
        honesty: 'Scale relative to demand — no recommendation yet.'
      };
    }
    var fails = recent.filter(function (e) { return !e.ok; }).length;
    var errorRate = fails / recent.length;
    var lats = recent.filter(function (e) { return e.ok; }).map(function (e) { return e.latencyMs || 0; }).sort(function (a, b) { return a - b; });
    var p95 = percentile(lats, 0.95);
    var conc = m.concurrencyHint || 0;
    var thumbsDown = 0, thumbsTotal = 0;
    Object.keys(m.byModel).forEach(function (id) {
      var row = m.byModel[id];
      thumbsDown += row.thumbsDown || 0;
      thumbsTotal += (row.thumbsUp || 0) + (row.thumbsDown || 0);
    });
    var tdRate = thumbsTotal ? thumbsDown / thumbsTotal : 0;
    var fires = [];
    if (p95 >= (sig.p95_latency_ms || 8000)) fires.push({ signal: 'p95_latency', value: p95, threshold: sig.p95_latency_ms });
    if (errorRate >= (sig.error_rate || 0.15)) fires.push({ signal: 'error_rate', value: errorRate, threshold: sig.error_rate });
    if (conc >= (sig.concurrency_hint || 4)) fires.push({ signal: 'concurrency', value: conc, threshold: sig.concurrency_hint });
    if (thumbsTotal >= 8 && tdRate >= (sig.thumbs_down_rate || 0.25)) {
      fires.push({ signal: 'thumbs_down_rate', value: tdRate, threshold: sig.thumbs_down_rate });
    }
    var rec = {
      current_tier: tier,
      suggest_tier: null,
      signals: fires,
      metrics: { p95: p95, errorRate: errorRate, concurrencyHint: conc, thumbsDownRate: tdRate, window: recent.length },
      action: 'hold',
      honesty: 'Recommendations only — do not auto-buy hardware or invent local 70B GPU.',
      next_tier_label: next && tiers[next] ? tiers[next].label : null
    };
    if (fires.length >= 1 && next) {
      rec.suggest_tier = next;
      rec.action = 'consider_scale';
      rec.reason = 'demand_signals';
      rec.message = 'Demand signals suggest moving toward ' + next + ' (' + (rec.next_tier_label || next) + '). Operator decision — router will not purchase hosts.';
    } else if (fires.length >= 1 && !next) {
      rec.action = 'optimize_or_quota';
      rec.reason = 'at_max_tier';
      rec.message = 'Already at highest catalog tier (T2). Optimize models, add quotas, or accept latency — still no auto-buy.';
    } else {
      rec.reason = 'within_thresholds';
      rec.message = 'Capacity OK relative to current demand.';
    }
    m.lastScale = rec;
    saveMetrics(m);
    return rec;
  }

  function recommend(policy) {
    policy = policy || (g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.getPolicy && g.IL_MODEL_ROUTER.getPolicy()) || {};
    var all = scores();
    var promo = shouldPromote(policy);
    var cat = g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.getCatalog && g.IL_MODEL_ROUTER.getCatalog();
    var scale = scaleRecommendation(policy, cat);
    return { scores: all, promote: promo, scale: scale, primary: policy.primary, demand_tier: policy.demand_tier };
  }

  function logCompletion(evt) {
    return record({
      modelId: evt.modelId,
      backendId: evt.backendId,
      latencyMs: evt.latencyMs,
      ok: evt.ok !== false,
      task: evt.taskType || evt.task,
      demand_tier: evt.demand_tier,
      error: evt.error
    });
  }

  function recommendPrimary(opts) {
    opts = opts || {};
    var policy = (g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.getPolicy && g.IL_MODEL_ROUTER.getPolicy()) || {};
    policy.min_samples = opts.winsNeeded || policy.min_samples;
    var d = shouldPromote(policy);
    if (d.promote) {
      return { switchTo: { backendId: 'ollama', modelId: d.challenger }, from: opts.current, score: d.winRate };
    }
    return null;
  }


  /* Muse lean|standard|heavy ↔ T0|T1|T2 */
  var MUSE_TIERS = [
    { id: 'lean', label: 'Lean', blurb: 'T0 — local P920: rules + ≤3B GPU / 7B CPU. Prefer lean defaults.', catalog: 'T0' },
    { id: 'standard', label: 'Standard', blurb: 'T1 — extra CPU inference hosts when demand grows.', catalog: 'T1' },
    { id: 'heavy', label: 'Heavy', blurb: 'T2 — remote OSS API / bigger GPU later. Recommend only — never auto-buy.', catalog: 'T2' }
  ];
  var MUSE_TO_CAT = { lean: 'T0', standard: 'T1', heavy: 'T2', T0: 'T0', T1: 'T1', T2: 'T2' };
  var CAT_TO_MUSE = { T0: 'lean', T1: 'standard', T2: 'heavy' };

  function tiers() { return MUSE_TIERS.slice(); }

  function setTier(id) {
    var catTier = MUSE_TO_CAT[id] || 'T0';
    if (g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.setPolicy) {
      g.IL_MODEL_ROUTER.setPolicy({ demand_tier: catTier });
    }
    var m = loadMetrics();
    m.museTier = CAT_TO_MUSE[catTier] || 'lean';
    saveMetrics(m);
    return demandStatus();
  }

  function load() {
    var m = loadMetrics();
    var policy = (g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.getPolicy) ? g.IL_MODEL_ROUTER.getPolicy() : {};
    return {
      demandTier: m.museTier || CAT_TO_MUSE[policy.demand_tier] || 'lean',
      byModel: m.byModel,
      events: m.events,
      lastScale: m.lastScale
    };
  }

  function demandStatus() {
    var policy = (g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.getPolicy) ? g.IL_MODEL_ROUTER.getPolicy() : { demand_tier: 'T0' };
    var museId = CAT_TO_MUSE[policy.demand_tier] || 'lean';
    var tierObj = MUSE_TIERS.filter(function (t) { return t.id === museId; })[0] || MUSE_TIERS[0];
    var cat = (g.IL_MODEL_ROUTER && g.IL_MODEL_ROUTER.getCatalog) ? g.IL_MODEL_ROUTER.getCatalog() : {};
    var scale = scaleRecommendation(policy, cat);
    var sc = scores();
    var ranking = Object.keys(sc).map(function (id) {
      return { modelId: id, backendId: 'ollama', winRate: sc[id].winRate, p95: sc[id].p95, n: sc[id].n };
    }).sort(function (a, b) { return (b.winRate - a.winRate) || (a.p95 - b.p95); });
    return {
      tier: tierObj,
      suggestedTier: scale.suggest_tier ? (CAT_TO_MUSE[scale.suggest_tier] || scale.suggest_tier) : null,
      suggestReason: scale.message || scale.reason,
      scaleNote: 'Scale relative to demand. Prefer lean (T0) defaults; grow to T1/T2 when signals fire — never auto-buy hardware.',
      ranking: ranking,
      scale: scale
    };
  }

  function setThumb(backendId, modelId, v) {
    return thumb(modelId, v > 0 || v === true || v === 'up');
  }

  var api = {
    METRICS_KEY: METRICS_KEY,
    INSIGHTS_KEY: INSIGHTS_KEY,
    record: record,
    thumb: thumb,
    scores: scores,
    shouldPromote: shouldPromote,
    scoringPolicy: scoringPolicy,
    scaleRecommendation: scaleRecommendation,
    recommend: recommend,
    loadMetrics: loadMetrics,
    logCompletion: logCompletion,
    recommendPrimary: recommendPrimary,
    rollingStats: rollingStats,
    // Muse aliases
    load: load,
    setTier: setTier,
    demandStatus: demandStatus,
    tiers: tiers,
    setThumb: setThumb
  };

  g.ILModelAnalytics = api;
  g.IL_MODEL_ANALYTICS = api;

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = api;
  }
})(typeof window !== 'undefined' ? window : (typeof global !== 'undefined' ? global : this));
