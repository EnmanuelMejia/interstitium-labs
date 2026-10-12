/**
 * Interstitium Labs — crypto receiving-name reveal widget (privacy).
 *
 * The owner's .crypto receiving name NEVER appears as a plain string in
 * page source or API responses (scrapers harvest both). Any element with
 * [data-il-ud-reveal] becomes a "Reveal receiving name" button; only on
 * an explicit click does the client fetch split fragments from
 * POST /api/pay/ud/reveal and assemble the name in the DOM, with a
 * copy-to-clipboard button. No click = nothing to harvest.
 *
 * Public API: window.ILUdReveal { scan, enhance }
 */
(function (global) {
  "use strict";
  var doc = global.document;

  function enhance(el) {
    if (!el || el.getAttribute("data-il-ud-done") === "1") return;
    el.setAttribute("data-il-ud-done", "1");
    var btn = doc.createElement("button");
    btn.type = "button";
    btn.className = "il-ud-reveal-btn";
    btn.textContent = "Reveal receiving name";
    btn.addEventListener("click", function () {
      btn.disabled = true;
      btn.textContent = "Revealing…";
      global
        .fetch("/api/pay/ud/reveal", {
          method: "POST",
          headers: { accept: "application/json" },
          credentials: "same-origin",
        })
        .then(function (r) {
          return r.json();
        })
        .then(function (d) {
          if (!d || !d.ok || !Array.isArray(d.parts) || !d.tld) {
            btn.disabled = false;
            btn.textContent = "Reveal failed — try again";
            return;
          }
          var name = d.parts.join("") + "." + d.tld;
          el.textContent = "";
          var span = doc.createElement("span");
          span.className = "il-ud-name";
          span.style.fontFamily = "monospace";
          span.textContent = name;
          el.appendChild(span);
          el.appendChild(doc.createTextNode(" "));
          var copy = doc.createElement("button");
          copy.type = "button";
          copy.className = "il-copy il-ud-copy";
          copy.textContent = "Copy";
          copy.addEventListener("click", function () {
            function done() {
              copy.textContent = "Copied";
              setTimeout(function () {
                copy.textContent = "Copy";
              }, 1600);
            }
            if (global.navigator && global.navigator.clipboard) {
              global.navigator.clipboard.writeText(name).then(done, done);
            } else {
              done();
            }
          });
          el.appendChild(copy);
        })
        .catch(function () {
          btn.disabled = false;
          btn.textContent = "Reveal failed — try again";
        });
    });
    el.textContent = "";
    el.appendChild(btn);
  }

  function scan() {
    var nodes = doc.querySelectorAll("[data-il-ud-reveal]");
    for (var i = 0; i < nodes.length; i++) enhance(nodes[i]);
  }

  global.ILUdReveal = { scan: scan, enhance: enhance };

  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", scan);
  else scan();
})(typeof window !== "undefined" ? window : this);
