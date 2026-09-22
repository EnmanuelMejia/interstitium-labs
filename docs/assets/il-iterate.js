/**
 * Heuristic iteration loop from local analytics buffer.
 * Writes recommendations to localStorage `il.iterate.v1`.
 */
(function (global) {
  "use strict";

  var KEY = "il.iterate.v1";
  var WEEK_MS = 7 * 24 * 60 * 60 * 1000;

  function buffer() {
    return (global.ILAnalytics && global.ILAnalytics.getBuffer)
      ? global.ILAnalytics.getBuffer()
      : [];
  }

  function analyze(events) {
    var now = Date.now();
    var week = (events || []).filter(function (e) { return now - (e.t || 0) < WEEK_MS; });
    var byName = {};
    var byPage = {};
    var byLang = {};
    var ctaByHref = {};
    var views = 0, cta = 0, enroll = 0, friction = 0;
    var prepViews = 0, foundersViews = 0, prepCtas = 0, foundersCtas = 0;

    week.forEach(function (e) {
      byName[e.n] = (byName[e.n] || 0) + 1;
      byPage[e.p] = (byPage[e.p] || 0) + 1;
      byLang[e.lang || "en"] = (byLang[e.lang || "en"] || 0) + 1;
      if (e.n === "page_view") {
        views++;
        if ((e.p || "").indexOf("/prep") === 0) prepViews++;
        if ((e.p || "").indexOf("/founders") === 0) foundersViews++;
      }
      if (e.n === "cta_click" || e.n === "enroll_click" || e.n === "path_open") {
        cta++;
        var href = (e.props && e.props.href) || "unknown";
        ctaByHref[href] = (ctaByHref[href] || 0) + 1;
        if ((e.p || "").indexOf("/prep") === 0) prepCtas++;
        if ((e.p || "").indexOf("/founders") === 0) foundersCtas++;
      }
      if (e.n === "enroll_click") enroll++;
      if (e.n === "friction_reload") friction++;
    });

    var recs = [];

    if (foundersViews >= 5 && prepViews >= 5) {
      var fRate = foundersCtas / Math.max(foundersViews, 1);
      var pRate = prepCtas / Math.max(prepViews, 1);
      if (pRate + 0.05 < fRate) {
        recs.push({
          id: "prep_cta_underperform",
          severity: "med",
          title: "Prep CTA underperforms vs Founders",
          detail: "Prep CTA rate " + (pRate * 100).toFixed(1) + "% vs Founders " + (fRate * 100).toFixed(1) + "%. A/B copy or move CTA above the fold.",
          action: "Ship cta_prep_copy variant B; compare enroll_click."
        });
      }
    }

    if (views >= 8 && enroll === 0 && cta >= 3) {
      recs.push({
        id: "dead_enroll",
        severity: "high",
        title: "Dead enroll path",
        detail: "CTA activity without enroll_click this week. Check /enroll/ honesty banner and Stripe placeholders.",
        action: "Audit enroll CTAs; keep payments inactive until live links exist."
      });
    }

    if (friction >= 2) {
      recs.push({
        id: "mobile_friction",
        severity: "med",
        title: "Mobile HUD / reload friction",
        detail: "Rapid reload bursts (" + friction + "). Possible HUD vs mobile chrome collision.",
        action: "Verify il-responsive.css HUD bottom offset on 390px + safe-area."
      });
    }

    var langKeys = Object.keys(byLang);
    if (langKeys.length >= 2) {
      recs.push({
        id: "lang_mix",
        severity: "low",
        title: "Language mix present",
        detail: "Locales: " + langKeys.map(function (k) { return k + "=" + byLang[k]; }).join(", "),
        action: "Prioritize long-form translation for top non-EN chrome locales."
      });
    }

    if (views >= 10 && !(ctaByHref["/enroll/"] || ctaByHref["/enroll"])) {
      recs.push({
        id: "dead_cta_enroll",
        severity: "med",
        title: "Dead CTA: /enroll/",
        detail: "Site traffic without enroll CTA clicks recorded.",
        action: "Repeat enroll CTA mid-page; raise contrast."
      });
    }

    if (!recs.length && views > 0) {
      recs.push({
        id: "healthy_sparse",
        severity: "low",
        title: "Sparse but healthy signal",
        detail: "Not enough contrast for strong A/B calls yet.",
        action: "Revisit after ~50 page_views."
      });
    }

    if (!views) {
      recs.push({
        id: "no_data",
        severity: "low",
        title: "No local analytics yet",
        detail: "Browse founders / prep / enroll on this device to seed il.analytics.v1.",
        action: "Open key pages, click CTAs, return here."
      });
    }

    return {
      generatedAt: now,
      windowMs: WEEK_MS,
      funnel: { views: views, cta: cta, enroll: enroll },
      topPages: Object.keys(byPage).map(function (p) { return { page: p, n: byPage[p] }; })
        .sort(function (a, b) { return b.n - a.n; }).slice(0, 12),
      langMix: byLang,
      eventCounts: byName,
      recommendations: recs
    };
  }

  function run() {
    var report = analyze(buffer());
    try { global.localStorage.setItem(KEY, JSON.stringify(report)); } catch (e) {}
    return report;
  }

  function getReport() {
    try {
      var raw = global.localStorage.getItem(KEY);
      if (raw) {
        var parsed = JSON.parse(raw);
        if (parsed && parsed.generatedAt && Date.now() - parsed.generatedAt < WEEK_MS) return parsed;
      }
    } catch (e) {}
    return run();
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function card(label, n) {
    return '<div class="rounded-xl bg-panel p-5 shadow-[0_0_0_1px_rgba(232,238,245,0.08)]"><p class="font-mono text-[0.58rem] uppercase tracking-[0.16em] text-gold">' +
      esc(label) + '</p><p class="mt-2 font-display text-3xl text-paper">' + n + "</p></div>";
  }

  function render(el) {
    if (!el) return;
    var report = getReport();
    var f = report.funnel || {};
    var html = "";
    html += '<div class="grid gap-4 md:grid-cols-3">';
    html += card("Views", f.views || 0);
    html += card("CTA clicks", f.cta || 0);
    html += card("Enroll clicks", f.enroll || 0);
    html += "</div>";
    html += '<h3 class="mt-10 font-display text-xl text-paper">Recommendations</h3><ul class="mt-4 space-y-3">';
    (report.recommendations || []).forEach(function (r) {
      html += '<li class="rounded-xl bg-panel p-4 shadow-[0_0_0_1px_rgba(232,238,245,0.08)]">';
      html += '<p class="font-mono text-[0.58rem] uppercase tracking-[0.16em] text-gold">' + esc(r.severity) + "</p>";
      html += '<p class="mt-1 font-display text-lg text-paper">' + esc(r.title) + "</p>";
      html += '<p class="mt-2 text-sm text-muted">' + esc(r.detail) + "</p>";
      html += '<p class="mt-2 font-mono text-[0.62rem] text-cyan">' + esc(r.action) + "</p></li>";
    });
    html += "</ul>";
    html += '<h3 class="mt-10 font-display text-xl text-paper">Top pages</h3><ol class="mt-3 space-y-1 font-mono text-sm text-muted">';
    (report.topPages || []).forEach(function (p) {
      html += "<li>" + esc(p.page) + " · " + p.n + "</li>";
    });
    html += "</ol>";
    html += '<h3 class="mt-10 font-display text-xl text-paper">Language mix</h3><p class="mt-2 font-mono text-sm text-muted">' +
      esc(JSON.stringify(report.langMix || {})) + "</p>";
    html += '<p class="mt-8 font-mono text-[0.58rem] uppercase tracking-[0.14em] text-muted">Generated ' +
      new Date(report.generatedAt).toLocaleString() + " · local only</p>";
    el.innerHTML = html;
  }

  global.ILIterate = { run: run, getReport: getReport, render: render, analyze: analyze };
})(typeof window !== "undefined" ? window : this);
