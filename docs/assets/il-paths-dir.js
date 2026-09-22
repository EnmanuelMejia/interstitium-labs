/**
 * Path directory renderer — loads /assets/il-paths-catalog.json into [data-il-paths-dir]
 */
(function (g) {
  'use strict';

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function paint(root, catalog) {
    var exceedOnly = root.getAttribute('data-il-paths-filter') === 'exceed';
    var paths = (catalog.paths || []).filter(function (p) {
      if (exceedOnly) return String(p.id || '').indexOf('exceed') >= 0 || String(p.slug || '').indexOf('exceed') >= 0 ||
        ['k8s-cka-exceed','aws-cloud-ops','linux-rhcsa-spine','platform-sre','iac-terraform-gitops','secops-blue-team','python-systems','aleks-ops-math'].indexOf(p.slug) >= 0;
      return true;
    });
    // Prefer showing exceed cohort when filter set; else all
    if (exceedOnly) {
      paths = (catalog.paths || []).filter(function (p) {
        return ['k8s-cka-exceed','aws-cloud-ops','linux-rhcsa-spine','platform-sre','iac-terraform-gitops','secops-blue-team','python-systems','aleks-ops-math'].indexOf(p.slug) >= 0;
      });
    }

    var html = '<div class="il-paths-dir-grid">';
    paths.forEach(function (p) {
      html +=
        '<a class="il-surface il-paths-dir-card rounded-xl bg-panel p-5 shadow-[0_0_0_1px_rgba(232,238,245,0.08)]" href="' +
        esc(p.href) +
        '"><p class="font-mono text-[0.58rem] uppercase tracking-[0.18em] text-gold">' +
        esc(p.kicker || p.peer || '') +
        '</p><h3 class="mt-2 font-display text-xl tracking-[-0.02em]">' +
        esc(p.title) +
        '</h3><p class="mt-2 text-sm text-muted">' +
        esc(p.outcome || '') +
        '</p><p class="mt-3 font-mono text-[0.58rem] uppercase tracking-[0.14em] text-cyan">Enter →</p></a>';
    });
    html += '</div>';
    if (catalog.honesty) {
      html += '<p class="mt-6 text-sm text-muted">' + esc(catalog.honesty) + '</p>';
    }
    root.innerHTML = html;
  }

  function boot() {
    var nodes = document.querySelectorAll('[data-il-paths-dir]');
    if (!nodes.length) return;
    fetch('/assets/il-paths-catalog.json', { credentials: 'same-origin' })
      .then(function (r) {
        if (!r.ok) throw new Error('catalog ' + r.status);
        return r.json();
      })
      .then(function (cat) {
        for (var i = 0; i < nodes.length; i++) paint(nodes[i], cat);
      })
      .catch(function (err) {
        for (var i = 0; i < nodes.length; i++) {
          nodes[i].innerHTML = '<p class="il-honest-note">Path catalog failed to load. ' + String(err && err.message || err) + '</p>';
        }
      });
  }

  g.ILPathsDir = { boot: boot };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})(typeof window !== 'undefined' ? window : this);
