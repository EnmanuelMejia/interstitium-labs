/**
 * Interstitium Labs — privacy-friendly first-party analytics
 * API: ILAnalytics.track(name, props)
 * Ring buffer: localStorage `il.analytics.v1`
 * Optional beacon: docs/analytics/config.js → endpoint
 * A/B: localStorage `il.exp.v1`
 */
(function (global) {
  "use strict";

  var BUF_KEY = "il.analytics.v1";
  var EXP_KEY = "il.exp.v1";
  var cfg = global.IL_ANALYTICS || {};
  var maxBuffer = cfg.maxBuffer || 400;
  var sampleRate = typeof cfg.sampleRate === "number" ? cfg.sampleRate : 1;

  function readBuf() {
    try {
      var raw = global.localStorage.getItem(BUF_KEY);
      if (!raw) return [];
      var parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      return [];
    }
  }

  function writeBuf(arr) {
    try {
      global.localStorage.setItem(BUF_KEY, JSON.stringify(arr.slice(-maxBuffer)));
    } catch (e) {}
  }

  function pagePath() {
    try { return global.location.pathname || "/"; } catch (e) { return "/"; }
  }

  function currentLang() {
    try {
      if (global.ILi18n && typeof global.ILi18n.getLang === "function") return global.ILi18n.getLang();
      return global.localStorage.getItem("il.lang") ||
        (global.document.documentElement && global.document.documentElement.lang) || "en";
    } catch (e) { return "en"; }
  }

  function beacon(evt) {
    var endpoint = cfg.endpoint;
    if (!endpoint) return;
    var body = JSON.stringify(evt);
    try {
      if (global.navigator && typeof global.navigator.sendBeacon === "function") {
        global.navigator.sendBeacon(endpoint, new Blob([body], { type: "application/json" }));
        return;
      }
    } catch (e) {}
    try {
      fetch(endpoint, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: body,
        keepalive: true,
        mode: "cors",
        credentials: "omit"
      }).catch(function () {});
    } catch (e2) {}
  }

  function track(name, props) {
    if (!name) return null;
    if (sampleRate < 1 && Math.random() > sampleRate) return null;
    var evt = {
      n: String(name),
      t: Date.now(),
      p: pagePath(),
      lang: currentLang(),
      props: props && typeof props === "object" ? props : {}
    };
    var buf = readBuf();
    buf.push(evt);
    writeBuf(buf);
    beacon(evt);
    try {
      global.document.dispatchEvent(new CustomEvent("il:analytics", { detail: evt }));
    } catch (e) {}
    return evt;
  }

  function getBuffer() { return readBuf(); }
  function clearBuffer() {
    try { global.localStorage.removeItem(BUF_KEY); } catch (e) {}
  }

  function getExperiments() {
    try {
      var raw = global.localStorage.getItem(EXP_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) { return {}; }
  }

  function assignVariant(expId, variants) {
    var list = variants && variants.length ? variants : ["A", "B"];
    var store = getExperiments();
    if (store[expId] && list.indexOf(store[expId]) >= 0) return store[expId];
    var pick = list[Math.floor(Math.random() * list.length)];
    store[expId] = pick;
    try { global.localStorage.setItem(EXP_KEY, JSON.stringify(store)); } catch (e) {}
    track("exp_assign", { exp: expId, variant: pick });
    return pick;
  }

  function applyCTAExperiments() {
    var prepVar = assignVariant("cta_prep_copy", ["A", "B"]);
    var enrollVar = assignVariant("cta_enroll_copy", ["A", "B"]);
    var prepNodes = global.document.querySelectorAll('[data-il-exp="cta_prep_copy"]');
    for (var i = 0; i < prepNodes.length; i++) {
      prepNodes[i].setAttribute("data-il-variant", prepVar);
      if (prepVar === "B" && prepNodes[i].childElementCount === 0) {
        prepNodes[i].textContent = prepNodes[i].getAttribute("data-il-exp-b") || "Crush Prep";
      }
    }
    var enNodes = global.document.querySelectorAll('[data-il-exp="cta_enroll_copy"]');
    for (var j = 0; j < enNodes.length; j++) {
      enNodes[j].setAttribute("data-il-variant", enrollVar);
      if (enrollVar === "B" && enNodes[j].childElementCount === 0) {
        enNodes[j].textContent = enNodes[j].getAttribute("data-il-exp-b") || "Join the cohort";
      }
    }
  }

  function bindAuto() {
    global.document.addEventListener("click", function (e) {
      var t = e.target;
      if (!t || !t.closest) return;
      var el = t.closest("[data-il-track], a[href]");
      if (!el) return;
      var href = el.getAttribute("href") || "";
      var explicit = el.getAttribute("data-il-track");
      var name = explicit;
      if (!name) {
        if (/\/enroll\/?/.test(href)) name = "enroll_click";
        else if (/\/paths\//.test(href) || href === "/paths/" || href === "/paths") name = "path_open";
        else if (el.classList.contains("il-cta") || el.hasAttribute("data-il-exp")) name = "cta_click";
        else if (/\/(prep|learn|play|founders|about)\//.test(href) && el.closest("main")) name = "cta_click";
        else return;
      }
      track(name, {
        href: href,
        id: el.id || null,
        exp: el.getAttribute("data-il-exp") || null,
        variant: el.getAttribute("data-il-variant") || null,
        text: (el.textContent || "").trim().slice(0, 80)
      });
    }, true);

    global.document.addEventListener("change", function (e) {
      var el = e.target;
      if (!el || el.type !== "checkbox") return;
      if (el.hasAttribute("data-il-progress") || el.closest(".check-row") || el.closest("[data-il-checklist]")) {
        track("checklist_tick", {
          id: el.id || el.getAttribute("data-il-progress") || null,
          checked: !!el.checked
        });
      }
    }, true);

    global.document.addEventListener("il:game", function (ev) {
      var d = (ev && ev.detail) || {};
      if (d.type === "quest_claim" || d.event === "quest_claim") track("quest_claim", d);
      if (d.type === "level_up" || d.event === "hud_level_up") track("hud_level_up", d);
    });

    // Bridge lang picker
    global.document.addEventListener("il:lang", function (ev) {
      var d = (ev && ev.detail) || {};
      track("lang_select", { lang: d.lang || currentLang() });
    });
  }

  function detectFriction() {
    try {
      var k = "il.analytics.reload";
      var arr = JSON.parse(global.sessionStorage.getItem(k) || "[]");
      var t = Date.now();
      arr = arr.filter(function (x) { return t - x < 60000; });
      arr.push(t);
      global.sessionStorage.setItem(k, JSON.stringify(arr));
      if (arr.length >= 4) track("friction_reload", { count: arr.length, windowMs: 60000 });
    } catch (e) {}
  }

  function maybeCloudflareBeacon() {
    var token = cfg.cloudflareBeaconToken;
    if (!token || /PASTE|PLACEHOLDER|null/i.test(String(token))) return;
    if (global.document.getElementById("il-cf-wa")) return;
    var s = global.document.createElement("script");
    s.id = "il-cf-wa";
    s.defer = true;
    s.src = "https://static.cloudflareinsights.com/beacon.min.js";
    s.setAttribute("data-cf-beacon", JSON.stringify({ token: token }));
    (global.document.head || global.document.documentElement).appendChild(s);
  }

  function boot() {
    track("page_view", {
      title: global.document.title || "",
      ref: (global.document.referrer || "").slice(0, 200)
    });
    bindAuto();
    applyCTAExperiments();
    detectFriction();
    maybeCloudflareBeacon();
  }

  global.ILAnalytics = {
    track: track,
    getBuffer: getBuffer,
    clearBuffer: clearBuffer,
    assignVariant: assignVariant,
    getExperiments: getExperiments
  };

  if (global.document.readyState === "loading") {
    global.document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})(typeof window !== "undefined" ? window : this);
