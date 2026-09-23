/**
 * IL Model Router — local-first OSS backends + demand-tier scaling for Noah / Coach.
 *
 * Product policy: scale relative to demand (T0 → T1 → T2). Auto-switch only among
 * models that are currently healthy/online. Never pretend a 70B is local GPU.
 *
 * API: selectModel({task, forceId}), chat(messages), healthCheck(),
 *      setPolicy({mode, primary, challengers}), recommend()
 *
 * Storage: localStorage il.model.router.v1 (policy), il.model.creds.v1 (base URL + key only)
 * Catalog: /assets/il-model-catalog.json
 * Never commit secrets. Optional window.IL_MUSE / IL_COACH / IL_LLM_BASE hooks.
 */
(function (g) {
  'use strict';

  var POLICY_KEY = 'il.model.router.v1';
  var CREDS_KEY = 'il.model.creds.v1';
  var HEALTH_KEY = 'il.model.health.v1';
  var CATALOG_URL = '/assets/il-model-catalog.json';
  var DEFAULT_TIMEOUT_MS = 45000;
  var HEALTH_TTL_MS = 60000;

  var catalogCache = null;
  var catalogPromise = null;

  function cfg() {
    return g.IL_MODEL_ROUTER_CFG || g.IL_MODEL_ROUTER || g.IL_MUSE || g.IL_COACH || {};
  }

  function readJSON(key, fallback) {
    try {
      var raw = g.localStorage.getItem(key);
      if (!raw) return fallback;
      var parsed = JSON.parse(raw);
      return parsed && typeof parsed === 'object' ? parsed : fallback;
    } catch (e) {
      return fallback;
    }
  }

  function writeJSON(key, val) {
    try { g.localStorage.setItem(key, JSON.stringify(val)); } catch (e) {}
  }

  function defaultPolicy(cat) {
    var d = (cat && cat.defaults) || {};
    var r = d.routing || {};
    return {
      v: 1,
      mode: r.mode || 'auto',
      primary: 'qwen2.5-coder-3b',
      challengers: ['phi-3-mini', 'qwen2.5-coder-7b'],
      demand_tier: d.demand_tier || 'T0',
      hardware_profile: d.hardware_profile || 'p920-p1000-4gb',
      backend: 'ollama',
      healthy_only: r.healthy_only !== false,
      min_samples: r.min_samples || 8,
      win_rate_margin: r.win_rate_margin || 0.08,
      latency_slack_ms: r.latency_slack_ms || 1500,
      explore_ratio: r.explore_ratio || 0.2,
      updatedAt: Date.now()
    };
  }

  function getPolicy() {
    var p = readJSON(POLICY_KEY, null);
    if (p && p.v === 1) return p;
    return defaultPolicy(catalogCache);
  }

  function setPolicy( partial ) {
    var cur = getPolicy();
    if (!partial || typeof partial !== 'object') return cur;
    if (partial.mode === 'auto' || partial.mode === 'manual') cur.mode = partial.mode;
    if (partial.primary) cur.primary = String(partial.primary);
    if (Array.isArray(partial.challengers)) cur.challengers = partial.challengers.slice();
    if (partial.demand_tier) cur.demand_tier = String(partial.demand_tier);
    if (partial.hardware_profile) cur.hardware_profile = String(partial.hardware_profile);
    if (partial.backend) cur.backend = String(partial.backend);
    if (typeof partial.healthy_only === 'boolean') cur.healthy_only = partial.healthy_only;
    if (typeof partial.min_samples === 'number') cur.min_samples = partial.min_samples;
    if (typeof partial.win_rate_margin === 'number') cur.win_rate_margin = partial.win_rate_margin;
    if (typeof partial.latency_slack_ms === 'number') cur.latency_slack_ms = partial.latency_slack_ms;
    if (typeof partial.explore_ratio === 'number') cur.explore_ratio = partial.explore_ratio;
    cur.updatedAt = Date.now();
    writeJSON(POLICY_KEY, cur);
    syncMuseHook(cur);
    return cur;
  }

  function getCreds() {
    return readJSON(CREDS_KEY, { bases: {}, keys: {} });
  }

  function setCreds(backendId, baseUrl, apiKey) {
    var c = getCreds();
    c.bases = c.bases || {};
    c.keys = c.keys || {};
    if (baseUrl != null) {
      if (baseUrl) c.bases[backendId] = String(baseUrl).replace(/\/$/, '');
      else delete c.bases[backendId];
    }
    if (apiKey != null) {
      if (apiKey) c.keys[backendId] = String(apiKey);
      else delete c.keys[backendId];
    }
    writeJSON(CREDS_KEY, c);
    return c;
  }

  function loadCatalog() {
    if (catalogCache) return Promise.resolve(catalogCache);
    if (catalogPromise) return catalogPromise;
    var embedded = g.IL_MODEL_CATALOG;
    if (embedded && embedded.models) {
      catalogCache = embedded;
      return Promise.resolve(catalogCache);
    }
    catalogPromise = fetch(CATALOG_URL, { credentials: 'omit' })
      .then(function (r) {
        if (!r.ok) throw new Error('catalog HTTP ' + r.status);
        return r.json();
      })
      .then(function (j) {
        catalogCache = j;
        catalogPromise = null;
        return j;
      })
      .catch(function (err) {
        catalogPromise = null;
        catalogCache = minimalCatalog();
        return catalogCache;
      });
    return catalogPromise;
  }

  function minimalCatalog() {
    return {
      version: 0,
      demand_tiers: {
        T0: { id: 'T0', label: 'Local P920', next_tier: 'T1', models_gpu: ['local-rules'], models_cpu: [] }
      },
      defaults: { demand_tier: 'T0', base_urls: { ollama: 'http://127.0.0.1:11434' }, routing: { healthy_only: true } },
      backends: [{ id: 'ollama', kind: 'ollama' }, { id: 'local-rules', kind: 'local', always_on: true }],
      models: [{
        id: 'local-rules', family: 'rules', label: 'Local rules', size_b: 0,
        backends: ['local-rules'], tags: ['chat'], min_vram_gb: 0, always_healthy: true,
        demand_tiers: ['T0', 'T1', 'T2'], placement: 'local'
      }]
    };
  }

  function modelById(id) {
    var cat = catalogCache || minimalCatalog();
    var models = cat.models || [];
    for (var i = 0; i < models.length; i++) if (models[i].id === id) return models[i];
    return null;
  }

  function backendById(id) {
    var cat = catalogCache || minimalCatalog();
    var backends = cat.backends || [];
    for (var i = 0; i < backends.length; i++) if (backends[i].id === id) return backends[i];
    return null;
  }

  function tierOrder(t) {
    if (t === 'T2') return 2;
    if (t === 'T1') return 1;
    return 0;
  }

  function modelAllowedOnTier(m, tier) {
    if (!m) return false;
    if (m.always_healthy) return true;
    var tiers = m.demand_tiers || ['T0'];
    return tiers.indexOf(tier) >= 0;
  }

  function baseUrlFor(backendId) {
    var c = cfg();
    var creds = getCreds();
    if (c.IL_LLM_BASE || (typeof g.IL_LLM_BASE === 'string' && g.IL_LLM_BASE)) {
      // Global override for lab-control tunnel
      if (backendId === 'ollama' || backendId === (getPolicy().backend)) {
        return String(c.IL_LLM_BASE || g.IL_LLM_BASE).replace(/\/$/, '');
      }
    }
    if (c.endpoint && (backendId === 'openai-compat' || backendId === getPolicy().backend)) {
      return String(c.endpoint).replace(/\/$/, '');
    }
    if (c.ollamaEndpoint && backendId === 'ollama') {
      return String(c.ollamaEndpoint).replace(/\/$/, '');
    }
    if (creds.bases && creds.bases[backendId]) return creds.bases[backendId];
    var cat = catalogCache || minimalCatalog();
    var bases = (cat.defaults && cat.defaults.base_urls) || {};
    return bases[backendId] || '';
  }

  function apiKeyFor(backendId) {
    var creds = getCreds();
    if (creds.keys && creds.keys[backendId]) return creds.keys[backendId];
    var c = cfg();
    // Never invent keys; only pass if operator set on window (still not committed)
    if (c.apiKey && backendId === (getPolicy().backend || 'openai-compat')) return c.apiKey;
    return '';
  }

  function readHealth() {
    return readJSON(HEALTH_KEY, { checkedAt: 0, backends: {}, models: {} });
  }

  function writeHealth(h) {
    writeJSON(HEALTH_KEY, h);
    return h;
  }

  function isHealthy(modelId, backendId) {
    var m = modelById(modelId);
    if (m && m.always_healthy) return true;
    var h = readHealth();
    var now = Date.now();
    if (now - (h.checkedAt || 0) > HEALTH_TTL_MS * 3) {
      // Stale — treat unknown as unhealthy for auto-switch (policy healthy_only)
      if (getPolicy().healthy_only && modelId !== 'local-rules') return false;
    }
    if (backendId && h.backends && h.backends[backendId]) {
      if (!h.backends[backendId].ok) return false;
    }
    if (h.models && h.models[modelId]) return !!h.models[modelId].ok;
    // If backend ok but model not probed, allow explore only when not healthy_only
    if (!getPolicy().healthy_only && backendId && h.backends && h.backends[backendId] && h.backends[backendId].ok) {
      return true;
    }
    return modelId === 'local-rules';
  }

  function fetchWithTimeout(url, opts, ms) {
    var ctrl = typeof AbortController !== 'undefined' ? new AbortController() : null;
    var t = null;
    opts = opts || {};
    if (ctrl) {
      opts = Object.assign({}, opts, { signal: ctrl.signal });
      t = setTimeout(function () { try { ctrl.abort(); } catch (e) {} }, ms || DEFAULT_TIMEOUT_MS);
    }
    return fetch(url, opts).then(function (r) {
      if (t) clearTimeout(t);
      return r;
    }, function (err) {
      if (t) clearTimeout(t);
      throw err;
    });
  }

  function healthCheck(opts) {
    opts = opts || {};
    return loadCatalog().then(function (cat) {
      var policy = getPolicy();
      var backends = cat.backends || [];
      var results = { checkedAt: Date.now(), backends: {}, models: {}, tier: policy.demand_tier };
      var jobs = [];

      backends.forEach(function (b) {
        if (b.kind === 'local' || b.always_on) {
          results.backends[b.id] = { ok: true, latencyMs: 0, kind: 'local' };
          return;
        }
        // Only probe backends allowed at current tier or below T2 remote when configured
        var tMin = b.tier_min || 'T0';
        if (tierOrder(tMin) > tierOrder(policy.demand_tier) && !baseUrlFor(b.id)) {
          results.backends[b.id] = { ok: false, reason: 'tier-skip', tier_min: tMin };
          return;
        }
        var ep = baseUrlFor(b.id);
        if (!ep) {
          results.backends[b.id] = { ok: false, reason: 'no-endpoint' };
          return;
        }
        jobs.push((function (backend, endpoint) {
          var t0 = Date.now();
          var url = backend.kind === 'ollama'
            ? endpoint + (backend.tags_path || '/api/tags')
            : endpoint.replace(/\/v1\/?$/, '/v1') + (backend.models_path || '/models');
          // openai path already includes /v1 often
          if (backend.kind === 'openai' && /\/v1$/.test(endpoint)) {
            url = endpoint + (backend.models_path || '/models');
          }
          var headers = {};
          var key = apiKeyFor(backend.id);
          if (key) headers.Authorization = 'Bearer ' + key;
          return fetchWithTimeout(url, { method: 'GET', headers: headers }, opts.timeoutMs || 5000)
            .then(function (res) {
              var entry = { ok: res.ok, status: res.status, latencyMs: Date.now() - t0 };
              results.backends[backend.id] = entry;
              if (res.ok && backend.kind === 'ollama') {
                return res.json().then(function (data) {
                  var names = {};
                  (data.models || []).forEach(function (m) {
                    if (m && m.name) names[m.name] = true;
                    if (m && m.model) names[m.model] = true;
                  });
                  (cat.models || []).forEach(function (cm) {
                    if ((cm.backends || []).indexOf(backend.id) < 0) return;
                    var pull = cm.ollama_pull || '';
                    var ok = !!(names[pull] || names[cm.id] || cm.always_healthy);
                    // Also match prefix (qwen2.5-coder:3b vs tags)
                    if (!ok && pull) {
                      Object.keys(names).forEach(function (n) {
                        if (n === pull || n.indexOf(pull.split(':')[0]) === 0) ok = true;
                      });
                    }
                    results.models[cm.id] = {
                      ok: ok,
                      backend: backend.id,
                      pull: pull
                    };
                  });
                  return entry;
                }).catch(function () { return entry; });
              }
              if (res.ok) {
                (cat.models || []).forEach(function (cm) {
                  if ((cm.backends || []).indexOf(backend.id) < 0) return;
                  if (!results.models[cm.id]) {
                    results.models[cm.id] = { ok: true, backend: backend.id, inferred: true };
                  }
                });
              }
              return entry;
            }, function (err) {
              results.backends[backend.id] = {
                ok: false,
                reason: err && err.message ? err.message : String(err),
                latencyMs: Date.now() - t0
              };
            });
        })(b, ep));
      });

      // local-rules always healthy
      results.models['local-rules'] = { ok: true, backend: 'local-rules' };

      return Promise.all(jobs).then(function () {
        writeHealth(results);
        if (g.ILAnalytics && g.ILAnalytics.track) {
          g.ILAnalytics.track('model_health_check', {
            tier: policy.demand_tier,
            backends: Object.keys(results.backends).filter(function (k) { return results.backends[k].ok; })
          });
        }
        return results;
      });
    });
  }

  function taskTags(task) {
    if (task === 'code') return ['code'];
    if (task === 'reason') return ['reason'];
    return ['chat'];
  }

  function scoreCandidate(m, task, policy) {
    var tags = m.tags || [];
    var want = taskTags(task);
    var tagScore = 0;
    want.forEach(function (t) { if (tags.indexOf(t) >= 0) tagScore += 2; });
    if (tags.indexOf('chat') >= 0) tagScore += 0.5;
    var sizePenalty = (m.size_b || 0) > 7 ? 1 : 0;
    var placementBonus = 0;
    if (m.placement === 'gpu' && policy.demand_tier === 'T0') placementBonus = 1;
    if (m.placement === 'cpu' && task === 'code' && (m.size_b || 0) >= 7) placementBonus = 0.5;
    return tagScore + placementBonus - sizePenalty;
  }

  /**
   * Select a model for a task. Auto mode explores challengers; only healthy+tier-allowed.
   */
  function selectModel(opts) {
    opts = opts || {};
    var policy = getPolicy();
    var task = opts.task || 'chat';
    if (opts.forceId) {
      var forced = modelById(opts.forceId);
      if (!forced) return { id: 'local-rules', reason: 'unknown-force', model: modelById('local-rules') };
      if (policy.healthy_only && !isHealthy(forced.id, pickBackend(forced))) {
        return {
          id: 'local-rules',
          reason: 'force-unhealthy',
          requested: opts.forceId,
          model: modelById('local-rules'),
          honesty: 'Refusing unhealthy/offline model; never pretend large local GPU.'
        };
      }
      return { id: forced.id, reason: 'force', model: forced, backend: pickBackend(forced) };
    }

    var cat = catalogCache || minimalCatalog();
    var tier = policy.demand_tier || 'T0';
    var pool = (cat.models || []).filter(function (m) {
      if (!modelAllowedOnTier(m, tier)) return false;
      if (m.id === 'local-rules') return true;
      // Honesty: forbid local GPU claims for huge models on P1000 profile
      var hp = (cat.hardware_profiles || {})[policy.hardware_profile];
      if (hp && hp.forbid_local_gpu && hp.forbid_local_gpu.indexOf(m.id) >= 0) return false;
      if (policy.healthy_only && !isHealthy(m.id, pickBackend(m))) return false;
      return true;
    });

    if (policy.mode === 'manual') {
      var primary = modelById(policy.primary);
      if (primary && pool.some(function (m) { return m.id === primary.id; })) {
        return { id: primary.id, reason: 'manual-primary', model: primary, backend: pickBackend(primary) };
      }
      var fallback = pool[0] || modelById('local-rules');
      return { id: fallback.id, reason: 'manual-fallback', model: fallback, backend: pickBackend(fallback) };
    }

    // auto: primary vs explore challenger
    var primaryId = policy.primary;
    var challengers = policy.challengers || [];
    var explore = Math.random() < (policy.explore_ratio || 0.2);
    var pickId = primaryId;
    var reason = 'auto-primary';
    if (explore && challengers.length) {
      var healthyCh = challengers.filter(function (id) {
        return pool.some(function (m) { return m.id === id; });
      });
      if (healthyCh.length) {
        pickId = healthyCh[Math.floor(Math.random() * healthyCh.length)];
        reason = 'auto-explore';
      }
    }
    var chosen = pool.filter(function (m) { return m.id === pickId; })[0];
    if (!chosen) {
      // Best score in pool
      pool.sort(function (a, b) { return scoreCandidate(b, task, policy) - scoreCandidate(a, task, policy); });
      chosen = pool[0] || modelById('local-rules');
      reason = 'auto-best-available';
    }
    return { id: chosen.id, reason: reason, model: chosen, backend: pickBackend(chosen), task: task };
  }

  function pickBackend(m) {
    if (!m) return 'local-rules';
    var policy = getPolicy();
    var preferred = policy.backend || 'ollama';
    var list = m.backends || [];
    if (list.indexOf(preferred) >= 0 && isHealthy(m.id, preferred)) return preferred;
    for (var i = 0; i < list.length; i++) {
      if (list[i] === 'local-rules') continue;
      if (!getPolicy().healthy_only || isHealthy(m.id, list[i]) || (readHealth().backends[list[i]] && readHealth().backends[list[i]].ok)) {
        if (baseUrlFor(list[i]) || list[i] === 'local-rules') return list[i];
      }
    }
    if (list.indexOf('local-rules') >= 0) return 'local-rules';
    return list[0] || 'local-rules';
  }

  function systemPrompt(ctx) {
    ctx = ctx || {};
    var lines = [
      'You are Noah / Interstitium Labs coach — Socratic DevOps tutor.',
      'Ask questions and give hints; never dump full exam answers.',
      'Topics: CIDR, Git, Kubernetes, Terraform, CI/CD, Linux.',
      'Hardware honesty: student lab may be P920 Quadro P1000 4GB — do not claim 70B local GPU.',
      'Scale policy: capacity grows relative to demand (T0 local → T1 CPU hosts → T2 remote OSS).'
    ];
    if (ctx.topic) lines.push('Topic focus: ' + ctx.topic + '.');
    if (ctx.tier) lines.push('Demand tier: ' + ctx.tier + '.');
    return lines.join('\n');
  }

  function localRulesReply(messages, ctx) {
    var last = '';
    for (var i = messages.length - 1; i >= 0; i--) {
      if (messages[i].role === 'user') { last = messages[i].content || ''; break; }
    }
    var topic = (ctx && ctx.topic) || '';
    if (g.ILCoach && typeof g.ILCoach.ask === 'function') {
      return g.ILCoach.ask(last, topic).then(function (res) {
        return {
          text: res.text || String(res),
          source: 'local-rules',
          modelId: 'local-rules',
          backendId: 'local-rules',
          latencyMs: 0,
          demand_tier: getPolicy().demand_tier
        };
      });
    }
    return Promise.resolve({
      text: 'Local rules only (no healthy LLM). Ask CIDR/Git/K8s/Terraform/CI/Linux — share what you tried. Configure Ollama (T0) or scale per demand.',
      source: 'local-rules',
      modelId: 'local-rules',
      backendId: 'local-rules',
      latencyMs: 0,
      demand_tier: getPolicy().demand_tier
    });
  }

  function callOllama(ep, model, messages, ctx, timeoutMs) {
    var pull = model.ollama_pull || model.id;
    var params = model.default_params || {};
    var body = {
      model: pull,
      stream: false,
      messages: [{ role: 'system', content: systemPrompt(ctx) }].concat(messages),
      options: {
        temperature: params.temperature != null ? params.temperature : 0.3,
        num_predict: params.num_predict || 1024
      }
    };
    var t0 = Date.now();
    return fetchWithTimeout(ep + '/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }, timeoutMs).then(function (res) {
      if (!res.ok) throw new Error('Ollama HTTP ' + res.status);
      return res.json();
    }).then(function (data) {
      var text = (data.message && data.message.content) || data.response || '';
      return {
        text: text,
        source: 'ollama',
        backendId: 'ollama',
        modelId: model.id,
        latencyMs: Date.now() - t0,
        tokensApprox: Math.ceil(text.length / 4)
      };
    });
  }

  function callOpenAI(ep, backendId, model, messages, ctx, timeoutMs) {
    var url = /\/chat\/completions$/.test(ep) ? ep : ep.replace(/\/$/, '') + '/chat/completions';
    var params = model.default_params || {};
    var body = {
      model: model.ollama_pull || model.id,
      messages: [{ role: 'system', content: systemPrompt(ctx) }].concat(messages),
      temperature: params.temperature != null ? params.temperature : 0.3,
      max_tokens: params.num_predict || 1024
    };
    var headers = { 'Content-Type': 'application/json' };
    var key = apiKeyFor(backendId);
    if (key) headers.Authorization = 'Bearer ' + key;
    var t0 = Date.now();
    return fetchWithTimeout(url, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(body)
    }, timeoutMs).then(function (res) {
      if (!res.ok) throw new Error(backendId + ' HTTP ' + res.status);
      return res.json();
    }).then(function (data) {
      var text = '';
      if (data.choices && data.choices[0]) {
        var c = data.choices[0];
        text = (c.message && c.message.content) || c.text || '';
      }
      return {
        text: text,
        source: backendId,
        backendId: backendId,
        modelId: model.id,
        latencyMs: Date.now() - t0,
        tokensApprox: (data.usage && data.usage.total_tokens) || Math.ceil(text.length / 4)
      };
    });
  }

  function invoke(sel, messages, ctx) {
    var model = sel.model || modelById(sel.id);
    var backendId = sel.backend || pickBackend(model);
    var b = backendById(backendId);
    if (!model || model.id === 'local-rules' || !b || b.kind === 'local') {
      return localRulesReply(messages, ctx);
    }
    var ep = baseUrlFor(backendId);
    if (!ep) return localRulesReply(messages, ctx);
    if (b.kind === 'ollama') return callOllama(ep, model, messages, ctx, DEFAULT_TIMEOUT_MS);
    if (b.kind === 'openai') return callOpenAI(ep, backendId, model, messages, ctx, DEFAULT_TIMEOUT_MS);
    return localRulesReply(messages, ctx);
  }

  function chat(messages, ctx) {
    ctx = ctx || {};
    return loadCatalog().then(function () {
      var policy = getPolicy();
      ctx.tier = policy.demand_tier;
      var sel = selectModel({ task: ctx.task || ctx.taskType || 'chat', forceId: ctx.forceId });
      var t0 = Date.now();
      return invoke(sel, messages, ctx).then(function (res) {
        res.demand_tier = policy.demand_tier;
        res.selectReason = sel.reason;
        if (g.ILModelAnalytics && g.ILModelAnalytics.record) {
          g.ILModelAnalytics.record({
            modelId: res.modelId,
            backendId: res.backendId,
            latencyMs: res.latencyMs != null ? res.latencyMs : (Date.now() - t0),
            ok: true,
            task: ctx.task || 'chat',
            reason: sel.reason,
            demand_tier: policy.demand_tier
          });
        }
        maybePromote();
        maybeScaleSignal();
        return res;
      }, function (err) {
        if (g.ILModelAnalytics && g.ILModelAnalytics.record) {
          g.ILModelAnalytics.record({
            modelId: sel.id,
            backendId: sel.backend,
            latencyMs: Date.now() - t0,
            ok: false,
            error: err && err.message,
            task: ctx.task || 'chat',
            demand_tier: policy.demand_tier
          });
        }
        maybeScaleSignal();
        // Fallback to local rules — never invent a 70B
        return localRulesReply(messages, ctx).then(function (local) {
          local.fallbackFrom = sel.id;
          local.error = err && err.message;
          return local;
        });
      });
    });
  }

  function maybePromote() {
    var policy = getPolicy();
    if (policy.mode !== 'auto') return;
    if (!g.ILModelAnalytics || !g.ILModelAnalytics.shouldPromote) return;
    var decision = g.ILModelAnalytics.shouldPromote(policy);
    if (decision && decision.promote && decision.challenger) {
      // Only promote if challenger currently healthy
      if (policy.healthy_only && !isHealthy(decision.challenger)) return;
      var prev = policy.primary;
      setPolicy({
        primary: decision.challenger,
        challengers: unique([prev].concat((policy.challengers || []).filter(function (c) {
          return c !== decision.challenger;
        })))
      });
      if (g.ILAnalytics && g.ILAnalytics.track) {
        g.ILAnalytics.track('model_auto_switch', {
          from: prev,
          to: decision.challenger,
          winRate: decision.winRate,
          latencyMs: decision.latencyMs,
          demand_tier: policy.demand_tier
        });
      }
    }
  }

  function unique(arr) {
    var s = {};
    var out = [];
    arr.forEach(function (x) {
      if (!x || s[x]) return;
      s[x] = true;
      out.push(x);
    });
    return out;
  }

  function maybeScaleSignal() {
    if (!g.ILModelAnalytics || !g.ILModelAnalytics.scaleRecommendation) return;
    var rec = g.ILModelAnalytics.scaleRecommendation(getPolicy(), catalogCache);
    if (rec && rec.suggest_tier && g.ILAnalytics && g.ILAnalytics.track) {
      g.ILAnalytics.track('model_scale_recommend', rec);
    }
  }

  function recommend() {
    var policy = getPolicy();
    var analyticsRec = (g.ILModelAnalytics && g.ILModelAnalytics.recommend)
      ? g.ILModelAnalytics.recommend(policy)
      : null;
    var scale = (g.ILModelAnalytics && g.ILModelAnalytics.scaleRecommendation)
      ? g.ILModelAnalytics.scaleRecommendation(policy, catalogCache)
      : null;
    var sel = selectModel({ task: 'chat' });
    return {
      primary: policy.primary,
      selected: sel,
      demand_tier: policy.demand_tier,
      next_tier: scale && scale.suggest_tier,
      scale: scale,
      analytics: analyticsRec,
      honesty: 'Auto-switch only among healthy models on the current demand tier. Scale relative to demand — recommendations only, no auto-purchase.',
      health: readHealth()
    };
  }

  function syncMuseHook(policy) {
    try {
      g.IL_MUSE = g.IL_MUSE || {};
      g.IL_COACH = g.IL_COACH || {};
      var ep = baseUrlFor(policy.backend || 'ollama');
      if (ep) {
        if (!(g.IL_MUSE.endpoint)) g.IL_MUSE.endpoint = ep;
        g.IL_MUSE.modelRouter = true;
        g.IL_MUSE.demand_tier = policy.demand_tier;
      }
      g.IL_COACH.modelRouter = true;
    } catch (e) {}
  }

  function listModels() {
    return loadCatalog().then(function (cat) {
      return (cat.models || []).slice();
    });
  }

  function getDemandTiers() {
    return loadCatalog().then(function (cat) {
      return cat.demand_tiers || {};
    });
  }


  /* —— Muse executor compatibility (lean|standard|heavy ↔ T0|T1|T2) —— */
  var TIER_MAP = { lean: 'T0', standard: 'T1', heavy: 'T2', T0: 'T0', T1: 'T1', T2: 'T2' };
  var TIER_REV = { T0: 'lean', T1: 'standard', T2: 'heavy' };

  function normalizeTierId(id) {
    return TIER_MAP[id] || 'T0';
  }

  function endpointFor(backendId) { return baseUrlFor(backendId); }
  function setEndpoint(backendId, url) { return setCreds(backendId, url, null); }

  function load() {
    var p = getPolicy();
    var creds = getCreds();
    return {
      v: 1,
      profileId: p.hardware_profile,
      primary: { backendId: p.backend || 'ollama', modelId: p.primary },
      override: p.mode === 'manual' ? { backendId: p.backend || 'ollama', modelId: p.primary } : null,
      order: [p.backend || 'ollama', 'local-rules'],
      endpoints: creds.bases || {},
      enabled: {},
      autoSwitch: p.mode === 'auto',
      demandTier: TIER_REV[p.demand_tier] || 'lean',
      demand_tier: p.demand_tier,
      updatedAt: p.updatedAt
    };
  }

  function save(s) {
    if (!s) return getPolicy();
    var partial = {};
    if (s.autoSwitch != null) partial.mode = s.autoSwitch ? 'auto' : 'manual';
    if (s.primary && s.primary.modelId) {
      partial.primary = s.primary.modelId;
      if (s.primary.backendId) partial.backend = s.primary.backendId;
    }
    if (s.demandTier) partial.demand_tier = normalizeTierId(s.demandTier);
    if (s.demand_tier) partial.demand_tier = normalizeTierId(s.demand_tier);
    if (s.endpoints) {
      Object.keys(s.endpoints).forEach(function (k) { setCreds(k, s.endpoints[k], null); });
    }
    setPolicy(partial);
    return load();
  }

  function activeTarget() {
    var p = getPolicy();
    var m = modelById(p.primary) || modelById('local-rules');
    return { backendId: pickBackend(m), modelId: m ? m.id : 'local-rules' };
  }

  function catalog() {
    var cat = catalogCache || minimalCatalog();
    // Shape Muse expects: array of backends with nested models
    return (cat.backends || []).map(function (b) {
      var models = (cat.models || []).filter(function (m) {
        return (m.backends || []).indexOf(b.id) >= 0;
      }).map(function (m) {
        return { id: m.ollama_pull || m.id, label: m.label, tier: m.placement, vramGb: m.min_vram_gb, catalogId: m.id };
      });
      return {
        id: b.id,
        label: b.label,
        kind: b.kind === 'local' ? 'local' : b.kind,
        alwaysOn: !!b.always_on,
        defaultEndpoint: (cat.defaults && cat.defaults.base_urls && cat.defaults.base_urls[b.id]) || '',
        models: models.length ? models : [{ id: 'rules', label: 'Hint engine' }],
        defaultModel: models[0] ? models[0].id : 'rules',
        notes: b.note || ''
      };
    });
  }

  function setOverride(backendId, modelId) {
    if (!backendId) {
      setPolicy({ mode: 'auto' });
      return getPolicy();
    }
    // Map ollama pull name back to catalog id when possible
    var id = modelId;
    var cat = catalogCache || minimalCatalog();
    (cat.models || []).forEach(function (m) {
      if (m.id === modelId || m.ollama_pull === modelId) id = m.id;
    });
    setPolicy({ mode: 'manual', primary: id, backend: backendId });
    return getPolicy();
  }

  function setPrimary(backendId, modelId) {
    return setOverride(backendId, modelId);
  }

  function probe(backendId) {
    return healthCheck().then(function (h) {
      var b = (h.backends || {})[backendId] || { ok: false, reason: 'unknown' };
      return b;
    });
  }

  function applyProfile(profileId) {
    setPolicy({ hardware_profile: profileId });
    return load();
  }

  function profiles() {
    var cat = catalogCache || minimalCatalog();
    return cat.hardware_profiles || {};
  }

  function chain() {
    var t = activeTarget();
    return [t, { backendId: 'local-rules', modelId: 'local-rules' }];
  }


  // Public surface — deliverable API + Noah aliases
  var api = {
    POLICY_KEY: POLICY_KEY,
    CREDS_KEY: CREDS_KEY,
    loadCatalog: loadCatalog,
    getCatalog: function () { return catalogCache; },
    selectModel: selectModel,
    chat: chat,
    healthCheck: healthCheck,
    setPolicy: setPolicy,
    getPolicy: getPolicy,
    setCreds: setCreds,
    getCreds: getCreds,
    recommend: recommend,
    modelById: modelById,
    backendById: backendById,
    baseUrlFor: baseUrlFor,
    isHealthy: isHealthy,
    listModels: listModels,
    getDemandTiers: getDemandTiers,
    systemPrompt: systemPrompt,
    readHealth: readHealth,
    // Muse aliases
    STORAGE: POLICY_KEY,
    catalog: catalog,
    profiles: profiles,
    load: load,
    save: save,
    applyProfile: applyProfile,
    setOverride: setOverride,
    setPrimary: setPrimary,
    setEndpoint: setEndpoint,
    setOrder: function () { return load(); },
    activeTarget: activeTarget,
    chain: chain,
    endpointFor: endpointFor,
    endpointForBackend: endpointFor,
    invokeOne: function (target, messages, ctx) {
      return invoke({ id: target.modelId, model: modelById(target.modelId) || { id: target.modelId, backends: [target.backendId] }, backend: target.backendId }, messages, ctx || {});
    },
    probe: probe,
    maybeAutoSwitch: maybePromote,
    normalizeTierId: normalizeTierId
  };

  g.IL_MODEL_ROUTER = api;
  g.ILModelRouter = api; // alias for older Muse drafts

  // Eager catalog + hook sync
  if (typeof fetch === 'function') {
    loadCatalog().then(function () {
      syncMuseHook(getPolicy());
    });
  } else {
    catalogCache = minimalCatalog();
    syncMuseHook(getPolicy());
  }
})(typeof window !== 'undefined' ? window : (typeof global !== 'undefined' ? global : this));
