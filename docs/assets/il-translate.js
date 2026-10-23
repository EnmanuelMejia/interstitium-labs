/* Interstitium Labs — translation dropdown (2026-10-09).
   The footer 🌐 button opens a minimal language picker that routes
   through Google's translate proxy. No widget injection, no layout shift. */
(function () {
  "use strict";
  var LANGS = [
    ["es", "Español"], ["fr", "Français"], ["de", "Deutsch"],
    ["pt", "Português"], ["it", "Italiano"], ["nl", "Nederlands"],
    ["ru", "Русский"], ["zh-CN", "中文"], ["ja", "日本語"],
    ["ko", "한국어"], ["ar", "العربية"], ["hi", "हिन्दी"],
  ];
  function host() {
    return location.hostname.replace(/^www\./, "");
  }
  function go(code) {
    var h = host();
    var path = location.pathname + location.search + location.hash;
    location.href = "https://" + h.replace(/\./g, "-") + ".translate.goog" +
      path + (path.indexOf("?") > -1 ? "&" : "?") +
      "_x_tr_sl=en&_x_tr_tl=" + encodeURIComponent(code) + "&_x_tr_hl=en";
  }
  function closeAll() {
    document.querySelectorAll(".il-lang-menu.is-open").forEach(function (m) {
      m.classList.remove("is-open");
    });
  }
  document.addEventListener("click", function (e) {
    var btn = e.target.closest ? e.target.closest(".il-fc-lang") : null;
    if (!btn) { closeAll(); return; }
    e.preventDefault();
    // wrap button in positioned container on first use
    var wrap = btn.parentElement;
    if (!wrap.classList.contains("il-fc-lang-wrap")) {
      wrap = document.createElement("div");
      wrap.className = "il-fc-lang-wrap";
      btn.parentNode.insertBefore(wrap, btn);
      wrap.appendChild(btn);
    }
    var menu = wrap.querySelector(".il-lang-menu");
    if (!menu) {
      menu = document.createElement("div");
      menu.className = "il-lang-menu";
      menu.setAttribute("role", "menu");
      var html = LANGS.map(function (l) {
        return '<button role="menuitem" data-lang="' + l[0] + '">' + l[1] + "</button>";
      }).join("");
      // "English (original)" resets by going to the canonical host
      html = '<button role="menuitem" data-lang="">English (original)</button>' + html;
      menu.innerHTML = html;
      wrap.appendChild(menu);
      menu.addEventListener("click", function (ev) {
        var b = ev.target.closest("button[data-lang]");
        if (!b) return;
        var code = b.getAttribute("data-lang");
        if (!code) {
          // back to original: strip translate.goog proxy
          var h = location.hostname;
          if (h.indexOf(".translate.goog") > -1) {
            var orig = h.replace(/\.translate\.goog$/, "").replace(/-/g, ".");
            location.href = "https://" + orig + location.pathname + location.search + location.hash;
          }
        } else {
          go(code);
        }
      });
    }
    var wasOpen = menu.classList.contains("is-open");
    closeAll();
    if (!wasOpen) menu.classList.add("is-open");
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeAll();
  });
})();
