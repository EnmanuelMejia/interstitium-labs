/**
 * Interstitium Labs — first-party i18n (privacy-first, Musk-practical)
 *
 * Detection priority:
 * 1) localStorage `il.lang` (picker override)
 * 2) navigator.languages / Accept-Language
 * 3) Geo hint: CF-IPCountry (optional inject) + Intl timezone → region default
 * 4) Fallback `en`
 *
 * Never forces geo over a strong browser language preference.
 */
(function (global) {
  "use strict";

  var STORAGE_KEY = "il.lang";
  var BASE = "/i18n/";
  var CACHE_V = "20260924";
  var RTL = { ar: 1, he: 1, fa: 1, ur: 1 };

  var LOCALES = [
    { code: "en", name: "English", completeness: "full" },
    { code: "es", name: "Español", completeness: "full" },
    { code: "pt-BR", name: "Português (BR)", completeness: "chrome" },
    { code: "fr", name: "Français", completeness: "chrome" },
    { code: "de", name: "Deutsch", completeness: "chrome" },
    { code: "zh-CN", name: "简体中文", completeness: "chrome" },
    { code: "ja", name: "日本語", completeness: "chrome" },
    { code: "ko", name: "한국어", completeness: "chrome" },
    { code: "hi", name: "हिन्दी", completeness: "chrome" },
    { code: "ar", name: "العربية", completeness: "chrome" }
  ];

  var TZ_DEFAULT = {
    "America/Santo_Domingo": "es",
    "America/Mexico_City": "es",
    "America/Bogota": "es",
    "America/Lima": "es",
    "America/Santiago": "es",
    "America/Buenos_Aires": "es",
    "America/Argentina/Buenos_Aires": "es",
    "America/Caracas": "es",
    "America/Guayaquil": "es",
    "America/La_Paz": "es",
    "America/Asuncion": "es",
    "America/Montevideo": "es",
    "America/Havana": "es",
    "America/Puerto_Rico": "es",
    "America/Panama": "es",
    "America/Costa_Rica": "es",
    "America/Guatemala": "es",
    "America/Sao_Paulo": "pt-BR",
    "America/Fortaleza": "pt-BR",
    "America/Recife": "pt-BR",
    "America/Manaus": "pt-BR",
    "America/Belem": "pt-BR",
    "Europe/Madrid": "es",
    "Europe/Paris": "fr",
    "Europe/Berlin": "de",
    "Europe/Rome": "it",
    "Europe/Lisbon": "pt-BR",
    "Asia/Shanghai": "zh-CN",
    "Asia/Chongqing": "zh-CN",
    "Asia/Hong_Kong": "zh-CN",
    "Asia/Taipei": "zh-CN",
    "Asia/Tokyo": "ja",
    "Asia/Seoul": "ko",
    "Asia/Kolkata": "hi",
    "Asia/Calcutta": "hi",
    "Asia/Dubai": "ar",
    "Asia/Riyadh": "ar",
    "Africa/Cairo": "ar",
    "Africa/Casablanca": "ar"
  };

  var CF_COUNTRY_LANG = {
    MX: "es", ES: "es", AR: "es", CO: "es", CL: "es", PE: "es", VE: "es",
    DO: "es", PR: "es", EC: "es", GT: "es", CR: "es", PA: "es", UY: "es",
    PY: "es", BO: "es", HN: "es", SV: "es", NI: "es", CU: "es",
    BR: "pt-BR", PT: "pt-BR",
    FR: "fr", BE: "fr",
    DE: "de", AT: "de", CH: "de",
    CN: "zh-CN", TW: "zh-CN", HK: "zh-CN", SG: "zh-CN",
    JP: "ja", KR: "ko", IN: "hi",
    SA: "ar", AE: "ar", EG: "ar", MA: "ar", QA: "ar", KW: "ar"
  };

  var catalog = {};
  var bodyMap = {};
  var bodyApplying = false;
  var current = "en";
  var completeness = "full";
  var ready = false;

  var INLINE_OK = {
    CODE: 1, EM: 1, STRONG: 1, B: 1, I: 1, SPAN: 1, A: 1, BR: 1,
    SMALL: 1, KBD: 1, ABBR: 1, MARK: 1, SUB: 1, SUP: 1, WBR: 1
  };
  var SKIP_TAGS = { SCRIPT: 1, STYLE: 1, NOSCRIPT: 1, SVG: 1, CODE: 1, PRE: 1, KBD: 1, SAMP: 1, TEXTAREA: 1 };

  function supportedCodes() {
    return LOCALES.map(function (l) { return l.code; });
  }

  function normalize(tag) {
    if (!tag) return null;
    var t = String(tag).replace(/_/g, "-").trim();
    if (!t) return null;
    var lower = t.toLowerCase();
    var codes = supportedCodes();
    for (var i = 0; i < codes.length; i++) {
      if (codes[i].toLowerCase() === lower) return codes[i];
    }
    var base = lower.split("-")[0];
    if (base === "pt") return "pt-BR";
    if (base === "zh") return "zh-CN";
    for (var j = 0; j < codes.length; j++) {
      if (codes[j].toLowerCase().split("-")[0] === base) return codes[j];
    }
    return null;
  }

  function browserLangs() {
    var list = [];
    try {
      if (global.navigator && global.navigator.languages) {
        list = Array.prototype.slice.call(global.navigator.languages);
      } else if (global.navigator && global.navigator.language) {
        list = [global.navigator.language];
      }
    } catch (e) {}
    return list;
  }

  function strongBrowserPref() {
    var langs = browserLangs();
    for (var i = 0; i < langs.length; i++) {
      var n = normalize(langs[i]);
      if (n) return n;
    }
    return null;
  }

  function timezoneHint() {
    try {
      var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      if (tz && TZ_DEFAULT[tz]) return TZ_DEFAULT[tz];
      if (tz && tz.indexOf("America/") === 0) {
        // Generic Americas without explicit mapping: do not force Spanish over EN
        return null;
      }
    } catch (e) {}
    return null;
  }

  function cfCountryHint() {
    var c = null;
    try {
      if (global.IL_CF_COUNTRY) c = String(global.IL_CF_COUNTRY).toUpperCase();
      if (!c && global.document) {
        var meta = global.document.querySelector('meta[name="cf-ipcountry"]');
        if (meta) c = String(meta.getAttribute("content") || "").toUpperCase();
      }
    } catch (e) {}
    if (c && CF_COUNTRY_LANG[c]) return CF_COUNTRY_LANG[c];
    return null;
  }

  /**
   * Resolve locale. Geo never overrides a strong browser language when they conflict.
   * Example: en-US browser in Mexico → en.
   */
  function detect() {
    try {
      var stored = global.localStorage && global.localStorage.getItem(STORAGE_KEY);
      var fromStore = normalize(stored);
      if (fromStore) return { lang: fromStore, source: "storage" };
    } catch (e) {}

    var browser = strongBrowserPref();
    var geo = cfCountryHint() || timezoneHint();

    if (browser) {
      // Soft geo: only fill when browser is English AND geo suggests a local tongue?
      // Spec: never force geo over explicit browser preference when they conflict strongly.
      // So if browser resolved to anything, keep it.
      return { lang: browser, source: "browser", geoHint: geo || null };
    }

    if (geo) return { lang: geo, source: "geo" };
    return { lang: "en", source: "fallback" };
  }

  function t(key, fallback) {
    if (!key) return fallback || "";
    if (catalog && Object.prototype.hasOwnProperty.call(catalog, key) && catalog[key] != null) {
      return String(catalog[key]);
    }
    return fallback != null ? String(fallback) : key;
  }

  function setDir(lang) {
    var html = global.document.documentElement;
    var dir = RTL[lang] || RTL[lang.split("-")[0]] ? "rtl" : "ltr";
    html.setAttribute("lang", lang);
    html.setAttribute("dir", dir);
  }

  function sanitizeInline(html) {
    var tpl = global.document.createElement("template");
    tpl.innerHTML = String(html);
    function walk(node) {
      var kids = Array.prototype.slice.call(node.childNodes);
      for (var i = 0; i < kids.length; i++) {
        var ch = kids[i];
        if (ch.nodeType !== 1) continue;
        if (!INLINE_OK[ch.tagName]) {
          node.replaceChild(global.document.createTextNode(ch.textContent || ""), ch);
          continue;
        }
        var attrs = Array.prototype.slice.call(ch.attributes);
        for (var a = 0; a < attrs.length; a++) {
          var n = attrs[a].name.toLowerCase();
          var v = attrs[a].value || "";
          if (n.indexOf("on") === 0 || n === "srcdoc" || n === "style") {
            ch.removeAttribute(attrs[a].name);
            continue;
          }
          if ((n === "href" || n === "src") && !/^(\/|https?:|#|mailto:)/i.test(v)) {
            ch.removeAttribute(attrs[a].name);
          }
        }
        walk(ch);
      }
    }
    walk(tpl.content);
    return tpl.innerHTML;
  }

  function writeTranslation(el, val) {
    var slot = el.querySelector("[data-i18n-text]");
    if (el.childElementCount && slot) {
      slot.textContent = val;
      return;
    }
    if (/<[a-z]/i.test(val)) {
      el.innerHTML = sanitizeInline(val);
      return;
    }
    el.textContent = val;
  }

  function lookupBody(text) {
    if (!text || current === "en") return null;
    var key = String(text).replace(/\s+/g, " ").trim();
    if (!key || !Object.prototype.hasOwnProperty.call(bodyMap, key)) return null;
    var v = bodyMap[key];
    if (v == null || v === key) return null;
    return String(v);
  }

  function inSkipped(el) {
    while (el) {
      if (el.nodeType === 1) {
        if (SKIP_TAGS[el.tagName]) return true;
        if (el.getAttribute && (el.getAttribute("translate") === "no" || el.hasAttribute("data-i18n") || el.hasAttribute("data-il-no-body"))) return true;
      }
      el = el.parentElement || el.parentNode;
    }
    return false;
  }

  function applyBodyText(node) {
    if (!node || node.nodeType !== 3 || inSkipped(node.parentElement)) return;
    if (node.__ilOrig == null) node.__ilOrig = node.nodeValue;
    var orig = node.__ilOrig;
    var match = orig.match(/^(\s*)([\s\S]*?)(\s*)$/);
    if (!match) return;
    var core = match[2].replace(/\s+/g, " ").trim();
    var translated = lookupBody(core);
    var next = translated ? (match[1] + translated + match[3]) : orig;
    if (node.nodeValue !== next) node.nodeValue = next;
  }

  function applyBodyAttrs(el) {
    if (!el || el.nodeType !== 1 || SKIP_TAGS[el.tagName]) return;
    if (el.getAttribute("translate") === "no" || el.hasAttribute("data-il-no-body")) return;
    var names = ["aria-label", "title", "placeholder", "alt"];
    for (var i = 0; i < names.length; i++) {
      var name = names[i];
      if (!el.hasAttribute(name)) continue;
      var store = "data-il-orig-" + name;
      if (!el.hasAttribute(store)) el.setAttribute(store, el.getAttribute(name) || "");
      var orig = el.getAttribute(store) || "";
      var translated = lookupBody(orig);
      var next = translated || orig;
      if (el.getAttribute(name) !== next) el.setAttribute(name, next);
    }
    if (el.tagName === "META") {
      var prop = (el.getAttribute("property") || el.getAttribute("name") || "").toLowerCase();
      if (prop === "description" || prop === "og:description" || prop === "og:title" || prop === "twitter:title" || prop === "twitter:description") {
        if (!el.hasAttribute("data-il-orig-content")) el.setAttribute("data-il-orig-content", el.getAttribute("content") || "");
        var oc = el.getAttribute("data-il-orig-content") || "";
        var tv = lookupBody(oc);
        var nc = tv || oc;
        if (el.getAttribute("content") !== nc) el.setAttribute("content", nc);
      }
    }
  }

  function applyBody(root) {
    if (!global.document || !global.document.documentElement) return;
    bodyApplying = true;
    try {
      var scope = root || global.document.documentElement;
      if (scope.nodeType === 1) applyBodyAttrs(scope);
      var walker = global.document.createTreeWalker(scope, 5 /* SHOW_ELEMENT | SHOW_TEXT */, null);
      var n = walker.nextNode();
      while (n) {
        if (n.nodeType === 3) applyBodyText(n);
        else applyBodyAttrs(n);
        n = walker.nextNode();
      }
    } finally {
      bodyApplying = false;
    }
  }

  function loadBody(lang) {
    if (!lang || lang === "en") {
      bodyMap = {};
      return Promise.resolve(bodyMap);
    }
    return fetch(BASE + lang + ".body.json?v=" + CACHE_V, { credentials: "same-origin", cache: "no-cache" })
      .then(function (res) {
        if (!res.ok) throw new Error("i18n body " + lang);
        return res.json();
      })
      .then(function (json) {
        bodyMap = json && typeof json === "object" ? json : {};
        return bodyMap;
      })
      .catch(function () {
        bodyMap = {};
        return bodyMap;
      });
  }

  function applyAttrs(root) {
    var scope = root || global.document;
    var nodes = scope.querySelectorAll("[data-i18n]");
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var key = el.getAttribute("data-i18n");
      if (!key) continue;
      var val = t(key, el.getAttribute("data-i18n-fallback") || el.textContent);
      writeTranslation(el, val);
    }
    var attrs = scope.querySelectorAll("[data-i18n-attr]");
    for (var j = 0; j < attrs.length; j++) {
      var ael = attrs[j];
      var spec = ael.getAttribute("data-i18n-attr") || "";
      // format: "placeholder:nav.search|aria-label:nav.aria"
      var parts = spec.split("|");
      for (var k = 0; k < parts.length; k++) {
        var pair = parts[k].split(":");
        if (pair.length < 2) continue;
        var attr = pair[0].trim();
        var akey = pair.slice(1).join(":").trim();
        ael.setAttribute(attr, t(akey, ael.getAttribute(attr) || ""));
      }
    }
  }

  function injectHreflang() {
    if (!global.document || !global.document.head) return;
    var canonical = global.document.querySelector('link[rel="canonical"]');
    var href = canonical ? canonical.getAttribute("href") : global.location.href.split("?")[0];
    if (!href) return;
    // Remove prior IL hreflang
    var old = global.document.querySelectorAll('link[data-il-hreflang]');
    for (var i = 0; i < old.length; i++) old[i].parentNode.removeChild(old[i]);
    var codes = supportedCodes();
    for (var j = 0; j < codes.length; j++) {
      var link = global.document.createElement("link");
      link.rel = "alternate";
      link.hreflang = codes[j];
      link.href = href + (href.indexOf("?") >= 0 ? "&" : "?") + "lang=" + encodeURIComponent(codes[j]);
      link.setAttribute("data-il-hreflang", "1");
      global.document.head.appendChild(link);
    }
    var xdef = global.document.createElement("link");
    xdef.rel = "alternate";
    xdef.hreflang = "x-default";
    xdef.href = href;
    xdef.setAttribute("data-il-hreflang", "1");
    global.document.head.appendChild(xdef);
  }

  function showScaffoldNote() {
    if (completeness === "full") {
      var existing = global.document.getElementById("il-i18n-scaffold-note");
      if (existing) existing.parentNode.removeChild(existing);
      return;
    }
    var main = global.document.querySelector("main") || global.document.body;
    if (!main) return;
    var note = global.document.getElementById("il-i18n-scaffold-note");
    if (!note) {
      note = global.document.createElement("div");
      note.id = "il-i18n-scaffold-note";
      note.className = "il-i18n-note no-print";
      note.setAttribute("role", "status");
      if (main.firstChild) main.insertBefore(note, main.firstChild);
      else main.appendChild(note);
    }
    note.innerHTML = "";
    var span = global.document.createElement("span");
    span.textContent = t("i18n.scaffold_note", "Original EN · translating… chrome is localized; long-form may still be English.");
    note.appendChild(span);
    var btn = global.document.createElement("button");
    btn.type = "button";
    btn.textContent = t("i18n.browser_translate", "Use browser translate");
    btn.addEventListener("click", function () {
      try {
        global.alert(t("i18n.browser_translate_help", "Use your browser menu: Translate page. Chrome/Edge: right-click → Translate."));
      } catch (e) {}
    });
    note.appendChild(btn);
  }

  function closeMenus() {
    var menus = global.document.querySelectorAll(".il-lang-menu.is-open");
    for (var i = 0; i < menus.length; i++) menus[i].classList.remove("is-open");
  }

  function mountSwitcher(host) {
    if (!host || host.getAttribute("data-il-lang-mounted")) return;
    host.setAttribute("data-il-lang-mounted", "1");
    host.classList.add("il-lang");

    var btn = global.document.createElement("button");
    btn.type = "button";
    btn.className = "il-lang-btn";
    btn.setAttribute("aria-haspopup", "listbox");
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-label", t("nav.language", "Language"));
    btn.innerHTML =
      '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 3 2.5 15 0 18M12 3c-2.5 3-2.5 15 0 18"/></svg>' +
      '<span data-il-lang-code>' + current + "</span>";

    var menu = global.document.createElement("div");
    menu.className = "il-lang-menu";
    menu.setAttribute("role", "listbox");

    LOCALES.forEach(function (loc) {
      var opt = global.document.createElement("button");
      opt.type = "button";
      opt.setAttribute("role", "option");
      if (loc.code === current) opt.setAttribute("aria-current", "true");
      opt.innerHTML =
        "<span>" + loc.name + '</span><span class="il-lang-meta">' +
        (loc.completeness === "full" ? "full" : "chrome") + "</span>";
      opt.addEventListener("click", function () {
        setLang(loc.code, true);
        closeMenus();
        btn.setAttribute("aria-expanded", "false");
      });
      menu.appendChild(opt);
    });

    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = !menu.classList.contains("is-open");
      closeMenus();
      if (open) {
        menu.classList.add("is-open");
        btn.setAttribute("aria-expanded", "true");
      } else {
        btn.setAttribute("aria-expanded", "false");
      }
    });

    host.appendChild(btn);
    host.appendChild(menu);
  }

  function ensureSwitcherHosts() {
    var hosts = global.document.querySelectorAll("[data-il-lang-switcher]");
    if (hosts.length) {
      for (var i = 0; i < hosts.length; i++) mountSwitcher(hosts[i]);
      return;
    }
    // Auto-inject into header / footer when missing
    var headerRow = global.document.querySelector("header .mx-auto.flex");
    if (headerRow && !headerRow.querySelector("[data-il-lang-switcher]")) {
      var slot = global.document.createElement("div");
      slot.setAttribute("data-il-lang-switcher", "");
      slot.className = "no-print";
      // Prefer placing before the mobile CTA (last child often)
      headerRow.appendChild(slot);
      mountSwitcher(slot);
    }
    var footer = global.document.querySelector("footer .mx-auto");
    if (footer && !footer.querySelector("[data-il-lang-switcher]")) {
      var fslot = global.document.createElement("div");
      fslot.setAttribute("data-il-lang-switcher", "");
      fslot.className = "no-print";
      footer.appendChild(fslot);
      mountSwitcher(fslot);
    }
  }

  function refreshSwitcherLabels() {
    var codes = global.document.querySelectorAll("[data-il-lang-code]");
    for (var i = 0; i < codes.length; i++) codes[i].textContent = current;
    var opts = global.document.querySelectorAll(".il-lang-menu [role=\"option\"]");
    for (var j = 0; j < opts.length; j++) {
      var meta = opts[j].querySelector(".il-lang-meta");
      var codeGuess = null;
      // Match by LOCALES order
      if (LOCALES[j]) {
        if (LOCALES[j].code === current) opts[j].setAttribute("aria-current", "true");
        else opts[j].removeAttribute("aria-current");
      }
    }
    // Sync any native <select aria-label=Language> leftovers
    var selects = global.document.querySelectorAll('select[aria-label="Language"], select[data-il-lang-select]');
    for (var s = 0; s < selects.length; s++) {
      try { selects[s].value = current; } catch (e) {}
    }
  }

  function wireNativeSelects() {
    var selects = global.document.querySelectorAll('select[aria-label="Language"], select[data-il-lang-select]');
    for (var i = 0; i < selects.length; i++) {
      var sel = selects[i];
      if (sel.getAttribute("data-il-lang-wired")) continue;
      sel.setAttribute("data-il-lang-wired", "1");
      sel.setAttribute("data-il-lang-select", "");
      // Replace dead SPA option values (zh, pt, …) with supported codes where possible
      sel.addEventListener("change", function (ev) {
        var v = ev.target.value;
        var map = { zh: "zh-CN", pt: "pt-BR", "pt-br": "pt-BR", "zh-cn": "zh-CN" };
        var mapped = map[String(v).toLowerCase()] || v;
        setLang(mapped, true);
      });
    }
  }

  function loadCatalog(lang) {
    return fetch(BASE + lang + ".json?v=" + CACHE_V, { credentials: "same-origin", cache: "no-cache" })
      .then(function (res) {
        if (!res.ok) throw new Error("i18n " + lang);
        return res.json();
      })
      .then(function (json) {
        catalog = json || {};
        completeness = catalog._meta && catalog._meta.completeness
          ? catalog._meta.completeness
          : (lang === "en" || lang === "es" ? "full" : "chrome");
        return catalog;
      });
  }

  function setLang(lang, persist) {
    var n = normalize(lang) || "en";
    current = n;
    if (persist) {
      try {
        global.localStorage.setItem(STORAGE_KEY, n);
      } catch (e) {}
      try {
        if (global.ILAnalytics && typeof global.ILAnalytics.track === "function") {
          global.ILAnalytics.track("lang_select", { lang: n });
        }
      } catch (e2) {}
    }
    setDir(n);
    return loadCatalog(n)
      .catch(function () {
        if (n !== "en") return loadCatalog("en").then(function () {
          current = "en";
          setDir("en");
        });
        catalog = {};
        completeness = "full";
      })
      .then(function () { return loadBody(current); })
      .then(function () {
        applyAttrs(global.document);
        applyBody(global.document);
        showScaffoldNote();
        ensureSwitcherHosts();
        wireNativeSelects();
        refreshSwitcherLabels();
        injectHreflang();
        ready = true;
        try {
          global.document.dispatchEvent(new CustomEvent("il:i18n", { detail: { lang: current, completeness: completeness } }));
          global.document.dispatchEvent(new CustomEvent("il:lang", { detail: { lang: current } }));
        } catch (e) {}
        return current;
      });
  }

  function queryLang() {
    try {
      var q = new URLSearchParams(global.location.search).get("lang");
      return normalize(q);
    } catch (e) {
      return null;
    }
  }

  function boot() {
    // Optional one-line CF country: window.IL_CF_COUNTRY from Worker
    var q = queryLang();
    var detected = detect();
    var lang = q || detected.lang;
    if (q) {
      try { global.localStorage.setItem(STORAGE_KEY, q); } catch (e) {}
    }
    global.document.addEventListener("click", function () { closeMenus(); });
    setLang(lang, false).then(function () {
      // Expose detection for admin insights
      try {
        global.sessionStorage.setItem("il.lang.detect", JSON.stringify(detected));
      } catch (e) {}
    });
    if (global.MutationObserver && global.document.documentElement) {
      var pending = 0;
      var obs = new global.MutationObserver(function () {
        if (bodyApplying || current === "en") return;
        if (pending) return;
        pending = global.setTimeout(function () {
          pending = 0;
          if (!bodyApplying && current !== "en") applyBody(global.document);
        }, 30);
      });
      var target = global.document.documentElement;
      var startObs = function () {
        try {
          obs.observe(target, {
            subtree: true,
            childList: true,
            characterData: true,
            attributes: true,
            attributeFilter: ["aria-label", "title", "placeholder", "alt", "content"]
          });
        } catch (e) {}
      };
      if (global.document.body) startObs();
      else global.document.addEventListener("DOMContentLoaded", startObs);
    }
  }

  var api = {
    t: t,
    setLang: setLang,
    getLang: function () { return current; },
    detect: detect,
    apply: applyAttrs,
    applyBody: applyBody,
    locales: LOCALES.slice(),
    ready: function () { return ready; },
    completeness: function () { return completeness; }
  };

  global.ILi18n = api;

  if (global.document.readyState === "loading") {
    global.document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})(typeof window !== "undefined" ? window : this);
