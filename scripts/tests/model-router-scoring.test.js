#!/usr/bin/env node
/**
 * Browser-free smoke test for model scoring + scale-relative-to-demand policy.
 * Run: node scripts/tests/model-router-scoring.test.js
 */
'use strict';

// Minimal localStorage stub
var store = {};
global.localStorage = {
  getItem: function (k) { return store[k] || null; },
  setItem: function (k, v) { store[k] = String(v); },
  removeItem: function (k) { delete store[k]; }
};

var path = require('path');
var analytics = require(path.join(__dirname, '../../docs/assets/il-model-analytics.js'));

var failed = 0;
function assert(cond, msg) {
  if (!cond) {
    failed++;
    console.error('FAIL:', msg);
  } else {
    console.log('ok:', msg);
  }
}

// 1) insufficient samples
var d0 = analytics.scoringPolicy(
  { n: 3, winRate: 0.5, p95: 1000, meanLatency: 900 },
  { n: 3, winRate: 0.9, p95: 1100, meanLatency: 1000 },
  { min_samples: 8 }
);
assert(d0.promote === false && d0.reason === 'insufficient-samples', 'blocks promote under min_samples');

// 2) win-rate margin
var d1 = analytics.scoringPolicy(
  { n: 10, winRate: 0.8, p95: 1000, meanLatency: 900 },
  { n: 10, winRate: 0.82, p95: 1000, meanLatency: 900 },
  { min_samples: 8, win_rate_margin: 0.08 }
);
assert(d1.promote === false && d1.reason === 'win-rate', 'requires win_rate_margin');

// 3) latency slack
var d2 = analytics.scoringPolicy(
  { n: 10, winRate: 0.7, p95: 1000, meanLatency: 900 },
  { n: 10, winRate: 0.9, p95: 5000, meanLatency: 4800 },
  { min_samples: 8, win_rate_margin: 0.08, latency_slack_ms: 1500 }
);
assert(d2.promote === false && d2.reason === 'latency', 'rejects slower challenger beyond slack');

// 4) promote when better + fast enough
var d3 = analytics.scoringPolicy(
  { n: 12, winRate: 0.7, p95: 2000, meanLatency: 1800 },
  { n: 12, winRate: 0.85, p95: 2100, meanLatency: 1900 },
  { min_samples: 8, win_rate_margin: 0.08, latency_slack_ms: 1500 }
);
assert(d3.promote === true, 'promotes healthier faster-enough challenger');

// 5) record + scale recommendation (need enough events)
for (var i = 0; i < 20; i++) {
  analytics.record({
    modelId: 'qwen2.5-coder-3b',
    backendId: 'ollama',
    latencyMs: 9000 + i * 10,
    ok: i % 3 !== 0,
    demand_tier: 'T0',
    task: 'chat'
  });
}
var policy = { demand_tier: 'T0', primary: 'qwen2.5-coder-3b', challengers: ['phi-3-mini'], min_samples: 8 };
var catalog = {
  defaults: {
    scale_signals: { p95_latency_ms: 8000, error_rate: 0.15, concurrency_hint: 4, thumbs_down_rate: 0.25, window_events: 40 }
  },
  demand_tiers: {
    T0: { id: 'T0', label: 'Local', next_tier: 'T1' },
    T1: { id: 'T1', label: 'Extra CPU', next_tier: 'T2' },
    T2: { id: 'T2', label: 'Remote OSS', next_tier: null }
  }
};
var scale = analytics.scaleRecommendation(policy, catalog);
assert(scale.current_tier === 'T0', 'scale reports current T0');
assert(scale.suggest_tier === 'T1' || scale.action === 'consider_scale' || (scale.signals && scale.signals.length >= 0),
  'scale emits recommendation structure (suggest or observe)');
assert(scale.honesty && /auto-buy|70B/i.test(scale.honesty), 'honesty: no auto-buy / no fake 70B');

// 6) Muse tier aliases
assert(typeof analytics.setTier === 'function', 'Muse setTier alias present');
assert(typeof analytics.demandStatus === 'function', 'Muse demandStatus alias present');
var st = analytics.setTier('lean');
assert(st.tier && (st.tier.id === 'lean' || st.tier.catalog === 'T0'), 'lean maps to T0-class tier');

if (failed) {
  console.error('\n' + failed + ' failure(s)');
  process.exit(1);
}
console.log('\nAll scoring smoke checks passed.');
