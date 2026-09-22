/**
 * Admin/Coach model switcher panel — on-demand primary, auto-iterate, live scores.
 * Mount: <div data-il-model-panel></div>
 * i18n keys: model.* (EN/ES)
 */
(function (g) {
  'use strict';

  function t(key, fb) {
    try {
      if (g.ILi18n && typeof g.ILi18n.t === 'function') {
        var v = g.ILi18n.t(key);
        if (v && v !== key) return v;
      }
    } catch (e) {}
    return fb || key;
  }

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }

  function mount(root) {
    if (!root || root.getAttribute('data-il-model-panel-ready')) return;
    root.setAttribute('data-il-model-panel-ready', '1');
    root.className = (root.className ? root.className + ' ' : '') + 'il-model-panel';

    var router = g.IL_MODEL_ROUTER || g.ILModelRouter;
    var analytics = g.ILModelAnalytics || g.IL_MODEL_ANALYTICS;

    var header = el('div', 'il-model-panel__head');
    header.innerHTML =
      '<p class="il-model-panel__kicker" data-i18n="model.kicker">' + t('model.kicker', 'Model router · Scale relative to demand') + '</p>' +
      '<h2 class="il-model-panel__title" data-i18n="model.title">' + t('model.title', 'Lab LLM switcher') + '</h2>' +
      '<p class="il-model-panel__lede" data-i18n="model.lede">' +
        t('model.lede', 'T0 local P920 (3B GPU / 7B CPU) → T1 extra CPU hosts → T2 remote OSS. Auto-switch only among healthy models. Never claim 70B local GPU.') +
      '</p>';

    var controls = el('div', 'il-model-panel__controls');
    var modeLabel = el('label', 'il-model-panel__toggle');
    var modeCb = document.createElement('input');
    modeCb.type = 'checkbox';
    modeCb.id = 'il-model-auto';
    modeLabel.appendChild(modeCb);
    modeLabel.appendChild(document.createTextNode(' '));
    var modeSpan = el('span', null, t('model.auto_iterate', 'Auto-iterate (analytics promote)'));
    modeSpan.setAttribute('data-i18n', 'model.auto_iterate');
    modeLabel.appendChild(modeSpan);

    var primarySel = document.createElement('select');
    primarySel.className = 'il-model-panel__select';
    primarySel.setAttribute('aria-label', t('model.primary', 'Primary model'));
    primarySel.id = 'il-model-primary';

    var tierSel = document.createElement('select');
    tierSel.className = 'il-model-panel__select';
    tierSel.id = 'il-model-tier';
    tierSel.setAttribute('aria-label', t('model.demand_tier', 'Demand tier'));

    var applyBtn = el('button', 'il-model-panel__btn');
    applyBtn.type = 'button';
    applyBtn.setAttribute('data-i18n', 'model.apply');
    applyBtn.textContent = t('model.apply', 'Set primary');

    var healthBtn = el('button', 'il-model-panel__btn il-model-panel__btn--ghost');
    healthBtn.type = 'button';
    healthBtn.setAttribute('data-i18n', 'model.health');
    healthBtn.textContent = t('model.health', 'Health check');

    var refreshBtn = el('button', 'il-model-panel__btn il-model-panel__btn--ghost');
    refreshBtn.type = 'button';
    refreshBtn.setAttribute('data-i18n', 'model.refresh');
    refreshBtn.textContent = t('model.refresh', 'Refresh scores');

    controls.appendChild(modeLabel);
    controls.appendChild(tierSel);
    controls.appendChild(primarySel);
    controls.appendChild(applyBtn);
    controls.appendChild(healthBtn);
    controls.appendChild(refreshBtn);

    var status = el('p', 'il-model-panel__status');
    status.id = 'il-model-status';
    var scaleBox = el('div', 'il-model-panel__scale');
    scaleBox.id = 'il-model-scale';
    var tableWrap = el('div', 'il-model-panel__table-wrap');
    var table = el('table', 'il-model-panel__table');
    table.innerHTML =
      '<thead><tr>' +
      '<th data-i18n="model.col_model">' + t('model.col_model', 'Model') + '</th>' +
      '<th data-i18n="model.col_n">' + t('model.col_n', 'N') + '</th>' +
      '<th data-i18n="model.col_win">' + t('model.col_win', 'Win rate') + '</th>' +
      '<th data-i18n="model.col_p95">' + t('model.col_p95', 'p95 ms') + '</th>' +
      '<th data-i18n="model.col_err">' + t('model.col_err', 'Errors') + '</th>' +
      '<th data-i18n="model.col_health">' + t('model.col_health', 'Healthy') + '</th>' +
      '</tr></thead><tbody id="il-model-scores-body"></tbody>';
    tableWrap.appendChild(table);

    var baseRow = el('div', 'il-model-panel__base');
    baseRow.innerHTML =
      '<label class="il-model-panel__field"><span data-i18n="model.base_url">' + t('model.base_url', 'LLM base URL') + '</span></label>';
    var baseInput = document.createElement('input');
    baseInput.type = 'url';
    baseInput.className = 'il-model-panel__input';
    baseInput.id = 'il-model-base';
    baseInput.placeholder = 'http://127.0.0.1:11434 or tunnel URL';
    var keyInput = document.createElement('input');
    keyInput.type = 'password';
    keyInput.className = 'il-model-panel__input';
    keyInput.id = 'il-model-key';
    keyInput.placeholder = t('model.api_key_ph', 'API key (localStorage only — never commit)');
    keyInput.setAttribute('autocomplete', 'off');
    var saveBase = el('button', 'il-model-panel__btn il-model-panel__btn--ghost');
    saveBase.type = 'button';
    saveBase.textContent = t('model.save_endpoint', 'Save endpoint');
    saveBase.setAttribute('data-i18n', 'model.save_endpoint');
    baseRow.appendChild(baseInput);
    baseRow.appendChild(keyInput);
    baseRow.appendChild(saveBase);

    root.appendChild(header);
    root.appendChild(controls);
    root.appendChild(baseRow);
    root.appendChild(status);
    root.appendChild(scaleBox);
    root.appendChild(tableWrap);

    function paint() {
      if (!router) {
        status.textContent = t('model.missing_router', 'Router not loaded.');
        return;
      }
      var policy = router.getPolicy();
      modeCb.checked = policy.mode === 'auto';
      router.loadCatalog().then(function (cat) {
        // tiers
        tierSel.innerHTML = '';
        var tiers = cat.demand_tiers || {};
        Object.keys(tiers).forEach(function (tid) {
          var o = document.createElement('option');
          o.value = tid;
          o.textContent = tid + ' — ' + (tiers[tid].label || tid);
          if (tid === policy.demand_tier) o.selected = true;
          tierSel.appendChild(o);
        });
        // models for tier
        primarySel.innerHTML = '';
        (cat.models || []).forEach(function (m) {
          var allowed = !m.demand_tiers || m.demand_tiers.indexOf(policy.demand_tier) >= 0;
          if (!allowed && m.id !== 'local-rules') return;
          var o = document.createElement('option');
          o.value = m.id;
          o.textContent = m.label + ' (' + (m.placement || '?') + ', ' + (m.size_b || 0) + 'B)';
          if (m.id === policy.primary) o.selected = true;
          primarySel.appendChild(o);
        });
        var ep = router.baseUrlFor(policy.backend || 'ollama');
        if (ep) baseInput.value = ep;
        var health = router.readHealth ? router.readHealth() : { models: {} };
        status.textContent = t('model.status_line', 'Mode') + ': ' + policy.mode +
          ' · ' + t('model.demand_tier', 'Demand tier') + ': ' + policy.demand_tier +
          ' · ' + t('model.primary', 'Primary') + ': ' + policy.primary;

        // scale box
        var scale = analytics && analytics.scaleRecommendation
          ? analytics.scaleRecommendation(policy, cat)
          : null;
        if (scale) {
          scaleBox.innerHTML =
            '<p class="il-model-panel__scale-title" data-i18n="model.scale_title">' +
            t('model.scale_title', 'Scale relative to demand') + '</p>' +
            '<p>' + (scale.message || scale.reason || '') + '</p>' +
            (scale.suggest_tier
              ? '<p class="il-model-panel__scale-next"><strong>' + t('model.suggest_tier', 'Suggested tier') + ':</strong> ' + scale.suggest_tier + '</p>'
              : '') +
            '<p class="il-model-panel__honesty">' + (scale.honesty || '') + '</p>';
        }

        // scores table
        var body = root.querySelector('#il-model-scores-body');
        body.innerHTML = '';
        var sc = analytics && analytics.scores ? analytics.scores() : {};
        var ids = Object.keys(sc);
        if (!ids.length) {
          (cat.models || []).slice(0, 6).forEach(function (m) { ids.push(m.id); });
        }
        ids.forEach(function (id) {
          var s = sc[id] || { n: 0, winRate: 0, p95: 0, fail: 0 };
          var healthy = router.isHealthy ? router.isHealthy(id) : (id === 'local-rules');
          var tr = document.createElement('tr');
          if (id === policy.primary) tr.className = 'is-primary';
          tr.innerHTML =
            '<td>' + id + '</td>' +
            '<td>' + (s.n || 0) + '</td>' +
            '<td>' + ((s.winRate || 0) * 100).toFixed(0) + '%</td>' +
            '<td>' + Math.round(s.p95 || 0) + '</td>' +
            '<td>' + (s.fail || 0) + '</td>' +
            '<td>' + (healthy ? '✓' : '—') + '</td>';
          body.appendChild(tr);
        });
      });
    }

    modeCb.addEventListener('change', function () {
      if (!router) return;
      router.setPolicy({ mode: modeCb.checked ? 'auto' : 'manual' });
      paint();
    });

    tierSel.addEventListener('change', function () {
      if (!router) return;
      router.setPolicy({ demand_tier: tierSel.value });
      paint();
    });

    applyBtn.addEventListener('click', function () {
      if (!router) return;
      router.setPolicy({
        primary: primarySel.value,
        mode: modeCb.checked ? 'auto' : 'manual',
        demand_tier: tierSel.value
      });
      if (g.ILAnalytics && g.ILAnalytics.track) {
        g.ILAnalytics.track('model_manual_switch', { primary: primarySel.value, tier: tierSel.value });
      }
      paint();
    });

    healthBtn.addEventListener('click', function () {
      if (!router || !router.healthCheck) return;
      status.textContent = t('model.checking', 'Checking…');
      router.healthCheck().then(function () { paint(); });
    });

    refreshBtn.addEventListener('click', paint);

    saveBase.addEventListener('click', function () {
      if (!router) return;
      var policy = router.getPolicy();
      var backend = policy.backend || 'ollama';
      router.setCreds(backend, baseInput.value.trim(), keyInput.value.trim() || null);
      // Also set ollama specifically when URL looks like ollama
      if (/11434/.test(baseInput.value)) router.setCreds('ollama', baseInput.value.trim(), null);
      keyInput.value = '';
      status.textContent = t('model.saved_local', 'Endpoint saved to localStorage only.');
      paint();
    });

    paint();
    root._ilModelPaint = paint;
  }

  function boot() {
    var nodes = document.querySelectorAll('[data-il-model-panel]');
    for (var i = 0; i < nodes.length; i++) mount(nodes[i]);
  }

  g.ILModelPanel = { mount: mount, boot: boot };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})(typeof window !== 'undefined' ? window : this);
