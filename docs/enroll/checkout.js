/**
 * Interstitium Labs — checkout UI (Phase 4b + paywall 2026-10-08).
 *
 * Flow: pick tier (?tier=) or course (?course=<slug>) -> email -> provider
 * -> (coin/rail for crypto) -> POST /api/pay/create -> redirect to
 * Stripe/PayPal/NOWPayments hosted checkout, or render the direct-wallet
 * panel (address + QR + tag/memo) with a transaction-hash submission form.
 *
 * Prices are display-only here; the Worker is the price authority.
 * Course prices shown are researched 2026-10-08 ($249/course, $999 bundle;
 * see payment-routes.js PAYWALL_CONFIG); the server decides the real amount
 * at /api/pay/create.
 * No secrets, no keys, no wallet addresses are hardcoded in this file —
 * direct addresses come from GET /api/pay/ud at runtime.
 */
(function () {
  "use strict";

  var TIERS = {
    "prep-sprint": {
      name: "Prep Sprint",
      price: "$149",
      blurb: "The complete interview-prep track: a structured 3-phase study plan plus timed drill packs.",
    },
    "devsecops-mastery": {
      name: "DevSecOps Mastery",
      price: "$499",
      blurb: "The 52-week DevSecOps path with weekly build artifacts, SuperLab hardening loops, and Noah side-quests.",
    },
    "full-academy": {
      name: "Full Academy",
      price: "$799",
      blurb: "Prep Sprint plus DevSecOps Mastery, with orientation across the whole knowledge OS.",
    },
  };

  /* Paywalled courses (display prices — researched 2026-10-08: $249/course,
     $999 bundle; server is the price authority, see payment-routes.js).
     Item ids match server ITEMS keys exactly (the course JSON slugs). */
  var COURSES = {
    "il-01-esoteric-foundations": { name: "IL-01 · Esoteric Foundations", price: "$249" },
    "il-02-mathematical-maturity-engine": { name: "IL-02 · Mathematical Maturity Engine", price: "$249" },
    "il-03-programming-language-forge": { name: "IL-03 · Programming Language Forge", price: "$249" },
    "il-04-systems-linux-windows-networks": { name: "IL-04 · Systems, Linux, Windows & Networks", price: "$249" },
    "il-05-cloud-devsecops-platform-sre": { name: "IL-05 · Cloud, DevSecOps, Platform & SRE", price: "$249" },
    "il-06-cybersecurity-secure-engineering": { name: "IL-06 · Cybersecurity & Secure Engineering", price: "$249" },
    "il-07-data-engineering-analytics-ai": { name: "IL-07 · SQL, Data Engineering, Analytics & AI", price: "$249" },
    "il-08-algorithms-compilers-distributed-formal": { name: "IL-08 · Algorithms, Compilers, Distributed & Formal", price: "$249" },
    "il-09-adaptive-certification-command": { name: "IL-09 · Adaptive Certification Command", price: "$249" },
    "il-10-portfolio-career-professional-practice": { name: "IL-10 · Portfolio, Career & Professional Practice", price: "$249" },
    "il-11-zero-trust-endpoint-defense": { name: "IL-11 · Zero Trust & Endpoint Defense", price: "$249" },
    "il-12-ai-engineering": { name: "IL-12 · AI Engineering", price: "$249" },
    "il-13-software-engineering-interview-prep": { name: "IL-13 · Software Engineering Interview Prep", price: "$249" },
    "il-14-sre-devops-cloud-security-interview-prep": { name: "IL-14 · SRE, DevOps, Cloud & Security Interview Prep", price: "$249" },
    "il-15-data-engineering-analytics-interview-prep": { name: "IL-15 · Data Engineering & Analytics Interview Prep", price: "$249" },
    "il-16-machine-learning-ai-engineering": { name: "IL-16 · Machine Learning & AI Engineering", price: "$249" },
    "il-17-agentic-ai-engineering": { name: "IL-17 · Agentic AI Engineering", price: "$249" },
    "il-18-technical-leadership-interview-prep": { name: "IL-18 · Technical Leadership Interview Prep", price: "$249" },
    "il-19-multicloud-devops-ai-bootcamp": { name: "IL-19 · MultiCloud, DevOps & AI Bootcamp", price: "$249" },
    "il-20-mathematics": { name: "IL-20 · Mathematics for Engineers & Scientists", price: "$249" },
    "il-21-humanities": { name: "IL-21 · Humanities for Technologists", price: "$249" },
    "il-22-esoteric-secret-knowledge": { name: "IL-22 · The Deep Library — Esoteric & Secret Knowledge", price: "$249" },
    "il-23-frontier-knowledge": { name: "IL-23 · The Frontier — Cutting-Edge Research Distilled", price: "$249" },
    "il-24-threatlocker-assessment-prep-cbt": { name: "IL-24 · ThreatLocker Assessment Prep CBT", price: "$249" },
    "il-25-cybersecurity-professional-certificate": { name: "IL-25 · Professional Certificate in Cybersecurity", price: "$249" },
    "il-26-data-analyst-certification-senior-mastery": { name: "IL-26 · Data Analyst Certification & Senior Mastery Bootcamp", price: "$249" },
    "all-courses": { name: "All Courses Bundle (IL-01–IL-26)", price: "$999" },
  };

  var COINS = [
    { code: "XRP", name: "XRP (Ripple)" },
    { code: "XLM", name: "Stellar Lumens" },
    { code: "ADA", name: "Cardano" },
    { code: "ALGO", name: "Algorand" },
    { code: "QNT", name: "Quant" },
    { code: "HBAR", name: "Hedera" },
    { code: "IOTA", name: "IOTA" },
    { code: "XDC", name: "XDC Network" },
    { code: "XMR", name: "Monero" },
    { code: "BTC", name: "Bitcoin" },
  ];

  var PROVIDERS = [
    {
      id: "stripe",
      title: "Card",
      sub: "Visa, Mastercard, Amex — plus Apple Pay and Google Pay, handled securely by Stripe.",
    },
    {
      id: "paypal",
      title: "PayPal",
      sub: "Pay with your PayPal balance or linked accounts. Venmo is available inside PayPal Checkout.",
    },
    {
      id: "nowpayments",
      title: "Crypto — hosted checkout",
      sub: "Pay with any of the 10 supported coins through a secure hosted crypto checkout.",
    },
    {
      id: "direct",
      title: "Crypto — direct wallet",
      sub: "Send straight to our crypto receiving name. Address + QR shown here; no middleman.",
    },
  ];

  var root = document.getElementById("il-root");
  var params = new URLSearchParams(window.location.search);
  /* ?course=<slug> for paywalled courses (paywall page links here);
     ?tier= retained for the legacy prep tiers. */
  var itemId = params.get("course") || params.get("tier") || "prep-sprint";
  var tier = null;
  var isCourseItem = false;
  /* Own-property lookups only, and copy the catalog entry before use:
     a query value such as "__proto__" or "constructor" must never
     resolve through the prototype chain — COURSES["__proto__"] IS
     Object.prototype, and the tier.blurb assignment below would then
     write onto every object on the page (prototype pollution). The
     copy also keeps display edits off the shared catalog objects. */
  if (Object.prototype.hasOwnProperty.call(COURSES, itemId)) {
    tier = Object.assign({}, COURSES[itemId]);
    isCourseItem = true;
  } else if (Object.prototype.hasOwnProperty.call(TIERS, itemId)) {
    tier = Object.assign({}, TIERS[itemId]);
  } else {
    itemId = "prep-sprint";
    tier = Object.assign({}, TIERS[itemId]);
  }
  if (isCourseItem) tier.blurb = "A full Interstitium Labs course: the complete interactive CBT with all modules, labs, and the Noah AI tutor.";

  var state = {
    provider: "stripe",
    coin: "BTC",
    rail: "hosted", // hosted (NOWPayments) | direct
    email: "",
    ud: null,
    busy: false,
  };

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function showLoading(msg) {
    root.innerHTML =
      '<div class="il-state" role="status"><div class="il-spinner" aria-hidden="true"></div>' +
      "<p>" + esc(msg || "Working…") + "</p></div>";
  }

  function friendlyError(code, detail) {
    var map = {
      provider_unavailable:
        "NOT_LIVE:This payment method isn't switched on yet. Checkout opens soon — join the waitlist and we'll email you the moment it goes live.",
      payments_not_configured:
        "NOT_LIVE:Checkout isn't live yet. Join the waitlist and we'll email you the moment seats open.",
      store_unavailable:
        "Our order store is temporarily unreachable. Please wait a minute and try again.",
      provider_error:
        "The payment provider returned an error. Please try again, or choose a different method.",
      coin_address_missing:
        "No receiving address is configured for that coin yet. Please pick another coin or method.",
      email_invalid: "Please enter a valid email address so we can send your receipt.",
      bad_json: "Something went wrong preparing your order. Please reload and try again.",
    };
    var v = map[code] || "Something went wrong. Please try again.";
    if (detail && code !== "provider_unavailable") v += " (" + detail + ")";
    return v;
  }

  function showError(code, detail, retry) {
    var f = friendlyError(code, detail);
    var notLive = f.indexOf("NOT_LIVE:") === 0;
    var msg = notLive ? f.slice("NOT_LIVE:".length) : f;
    var html =
      '<div class="' + (notLive ? "il-notlive" : "il-error") + '" role="alert">' +
      (notLive ? "" : '<p class="il-error__title">Payment couldn\u2019t start</p>') +
      '<p class="' + (notLive ? "" : "il-error__msg") + '">' + esc(msg) + "</p>" +
      (notLive
        ? '<a class="il-btn" href="/enroll/">Join the waitlist</a>'
        : '<button class="il-error__retry" id="il-retry" type="button">Try again</button>') +
      "</div>";
    root.innerHTML = html;
    if (!notLive) {
      var b = document.getElementById("il-retry");
      if (b) b.addEventListener("click", retry || renderForm);
    }
  }

  function providerCards() {
    return PROVIDERS.map(function (p) {
      var on = state.provider === p.id;
      return (
        '<button type="button" class="il-provider" data-provider="' + p.id + '" aria-pressed="' + on + '">' +
        '<span class="il-provider__radio" aria-hidden="true"></span>' +
        '<span><span class="il-provider__title">' + esc(p.title) + "</span>" +
        '<span class="il-provider__sub" style="display:block">' + esc(p.sub) + "</span></span>" +
        "</button>"
      );
    }).join("");
  }

  function coinGrid() {
    return COINS.map(function (c) {
      var on = state.coin === c.code;
      return (
        '<button type="button" class="il-coin" data-coin="' + c.code + '" aria-pressed="' + on + '">' +
        '<span class="il-coin__code">' + esc(c.code) + "</span>" +
        '<span class="il-coin__name">' + esc(c.name) + "</span>" +
        "</button>"
      );
    }).join("");
  }

  function cryptoSection() {
    var isCrypto = state.provider === "nowpayments" || state.provider === "direct";
    if (!isCrypto) return "";
    var railToggle =
      '<div class="il-field"><span class="il-label">Crypto rail</span>' +
      '<div class="il-rail-toggle" role="group" aria-label="Crypto rail">' +
      '<button type="button" class="il-rail" data-rail="hosted" aria-pressed="' + (state.rail === "hosted") + '">Hosted checkout</button>' +
      '<button type="button" class="il-rail" data-rail="direct" aria-pressed="' + (state.rail === "direct") + '">Direct wallet</button>' +
      "</div>" +
      '<p class="il-hint">' +
      (state.rail === "hosted"
        ? "A secure hosted page handles the transfer — it shows the exact coin amount and a QR code."
        : "Pay straight to our receiving name (revealed with the address below). We show the address and QR here; include the destination tag / memo where shown.") +
      "</p></div>";
    return (
      railToggle +
      '<div class="il-field"><span class="il-label">Coin</span>' +
      '<div class="il-coins" role="group" aria-label="Coin">' + coinGrid() + "</div></div>"
    );
  }

  function renderForm() {
    var html =
      '<section class="il-card" aria-label="Order summary"><div class="il-order">' +
      "<div><h2 class='il-order__tier'>" + esc(tier.name) + "</h2>" +
      '<p class="il-order__blurb">' + esc(tier.blurb) + "</p></div>" +
      '<div><span class="il-order__price">' + esc(tier.price) + '</span><span class="il-order__per">one-time · USD</span></div>' +
      "</div></section>" +
      '<form id="il-form" novalidate>' +
      '<div class="il-field"><label class="il-label" for="il-email">Email for your receipt</label>' +
      '<input class="il-input" id="il-email" name="email" type="email" autocomplete="email" inputmode="email" placeholder="you@example.com" value="' + esc(state.email) + '"/>' +
      '<p class="il-hint">Your receipt and course access go here. We never share it.</p></div>' +
      '<div class="il-field"><span class="il-label" id="il-paywith">Pay with</span>' +
      '<div class="il-providers" role="group" aria-labelledby="il-paywith">' + providerCards() + "</div></div>" +
      '<div id="il-crypto">' + cryptoSection() + "</div>" +
      '<button class="il-pay" id="il-paybtn" type="submit">Pay ' + esc(tier.price) + "</button>" +
      '<p class="il-secure">Secured by Stripe, PayPal, or on-chain transfer. Interstitium Labs never sees your card number.</p>' +
      "</form>";
    root.innerHTML = html;

    var form = document.getElementById("il-form");
    form.addEventListener("submit", onSubmit);

    root.querySelectorAll("[data-provider]").forEach(function (b) {
      b.addEventListener("click", function () {
        state.provider = b.getAttribute("data-provider");
        if (state.provider === "nowpayments") state.rail = "hosted";
        if (state.provider === "direct") state.rail = "direct";
        renderForm();
      });
    });
    root.querySelectorAll("[data-coin]").forEach(function (b) {
      b.addEventListener("click", function () {
        state.coin = b.getAttribute("data-coin");
        renderForm();
      });
    });
    root.querySelectorAll("[data-rail]").forEach(function (b) {
      b.addEventListener("click", function () {
        state.rail = b.getAttribute("data-rail");
        state.provider = state.rail === "direct" ? "direct" : "nowpayments";
        renderForm();
      });
    });
  }

  function effectiveProvider() {
    if (state.provider === "nowpayments" || state.provider === "direct") {
      return state.rail === "direct" ? "direct" : "nowpayments";
    }
    return state.provider;
  }

  async function onSubmit(ev) {
    ev.preventDefault();
    if (state.busy) return;
    var emailInput = document.getElementById("il-email");
    state.email = (emailInput.value || "").trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(state.email)) {
      showError("email_invalid", "", renderForm);
      return;
    }
    state.busy = true;
    showLoading("Creating your secure order…");
    var provider = effectiveProvider();
    var payload = { provider: provider, item: itemId, email: state.email };
    if (provider === "nowpayments" || provider === "direct") payload.coin = state.coin;
    var res, data;
    try {
      res = await fetch("/api/pay/create", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(payload),
      });
      data = await res.json().catch(function () { return null; });
    } catch (e) {
      state.busy = false;
      showError("network", "network_unreachable", renderForm);
      return;
    }
    state.busy = false;
    if (!res.ok || !data || !data.ok) {
      var code = (data && data.error) || "provider_error";
      var hint = (data && data.hint) || "";
      if (hint === "payments_not_configured") code = "provider_unavailable";
      showError(code, (data && data.detail) || "", renderForm);
      return;
    }
    if (data.redirect_url) {
      window.location.href = data.redirect_url;
      return;
    }
    if (provider === "direct" && data.direct) {
      renderDirect(data);
      return;
    }
    showError("provider_error", "unexpected_response", renderForm);
  }

  function copyText(text, btn) {
    function done() {
      var old = btn.textContent;
      btn.textContent = "Copied ✓";
      setTimeout(function () { btn.textContent = old; }, 1600);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallback(); });
    } else {
      fallback();
    }
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta);
      done();
    }
  }

  function renderQr(el, text) {
    el.innerHTML = "";
    try {
      // vendored qrcode-generator (MIT, Kazuhiko Arase), loaded in <head> via vendor/qrcode.js
      var qr = qrcode(0, "M");
      qr.addData(text);
      qr.make();
      el.innerHTML = qr.createImgTag(6, 8);
    } catch (e) {
      el.innerHTML = '<p class="il-hint">QR unavailable — copy the address above.</p>';
    }
  }

  function renderDirect(data) {
    var d = data.direct;
    var coinName = data.coin_name || data.coin;
    var extraRow = "";
    if (d.destination_tag || d.memo) {
      var label = d.extra_label || (d.destination_tag ? "Destination tag" : "Memo");
      var val = d.destination_tag || d.memo;
      extraRow =
        '<div class="il-tag" role="note"><strong>' + esc(label) + " (required):</strong> " +
        '<span style="font-family:monospace">' + esc(val) + "</span><br/>" +
        '<button class="il-copy" type="button" data-copy="' + esc(val) + '">Copy ' + esc(label.toLowerCase()) + "</button></div>";
    }
    var html =
      '<section class="il-card il-direct" aria-label="Direct wallet payment">' +
      "<h2 class='il-order__tier'>Pay with " + esc(coinName) + "</h2>" +
      '<p class="il-ud">Pay to <span data-il-ud-reveal></span></p>' +
      '<div class="il-qr" id="il-qr" role="img" aria-label="QR code for the receiving address"></div>' +
      '<p class="il-hint">Receiving address' + (d.source ? " · via " + esc(d.source === "ud" ? "resolved receiving name" : "configured wallet") : "") + "</p>" +
      '<p class="il-addr">' + esc(d.address) + "</p>" +
      '<button class="il-copy" type="button" data-copy="' + esc(d.address) + '">Copy address</button>' +
      extraRow +
      '<p class="il-order__price" style="margin:0.6rem 0 0">' + esc(tier.price) + ' <span style="font-size:0.75rem;color:var(--il-muted)">USD-equivalent in ' + esc(data.coin) + "</span></p>" +
      '<p class="il-wait">Send the USD-equivalent of <strong>' + esc(tier.price) + "</strong> in " + esc(data.coin) +
      " to the address above" +
      (d.destination_tag ? " with the destination tag" : d.memo ? " with the memo" : "") +
      ". Direct payments are verified by our team — your receipt and course access follow by email at <strong>" + esc(state.email) + "</strong>.</p>" +
      '<p class="il-hint">Order <span style="font-family:monospace">' + esc(data.order_id) + "</span> · status: awaiting payment</p>" +
      '<form id="il-txform">' +
      '<div class="il-field"><label class="il-label" for="il-txhash">Transaction hash — after you send</label>' +
      '<input class="il-input" id="il-txhash" name="txhash" type="text" inputmode="text" autocomplete="off" spellcheck="false" placeholder="Paste the on-chain transaction hash" style="font-family:monospace"/>' +
      '<p class="il-hint">Direct crypto has no automatic confirmation. Paste the hash and we verify the transfer on-chain manually — your receipt and course access follow by email.</p></div>' +
      '<button class="il-pay" id="il-txbtn" type="submit">I sent it — record transaction</button>' +
      '<p class="il-hint" id="il-txstatus" role="status"></p>' +
      "</form>" +
      "</section>";
    root.innerHTML = html;
    if (window.ILUdReveal) window.ILUdReveal.scan();
    renderQr(document.getElementById("il-qr"), d.qr_payload || d.address);
    root.querySelectorAll("[data-copy]").forEach(function (b) {
      b.addEventListener("click", function () { copyText(b.getAttribute("data-copy"), b); });
    });
    var txform = document.getElementById("il-txform");
    if (txform) {
      txform.addEventListener("submit", function (ev) { submitTx(ev, data.order_id); });
    }
  }

  function friendlyTxError(code) {
    var map = {
      tx_hash_invalid:
        "That doesn't look like a transaction hash — paste the full hash from your wallet.",
      tx_already_submitted:
        "A transaction hash was already recorded for this order. If you sent a replacement, email us with your order id.",
      already_paid: "This order is already paid.",
      not_found: "Order not found — please reload the checkout page and start again.",
    };
    return map[code] || "Couldn't record the transaction. Please try again.";
  }

  async function submitTx(ev, orderId) {
    ev.preventDefault();
    var input = document.getElementById("il-txhash");
    var status = document.getElementById("il-txstatus");
    var btn = document.getElementById("il-txbtn");
    if (!input || !status || !btn) return;
    var tx = (input.value || "").trim();
    if (!/^[A-Za-z0-9]{16,160}$/.test(tx)) {
      status.textContent = friendlyTxError("tx_hash_invalid");
      return;
    }
    btn.disabled = true;
    status.textContent = "Recording…";
    try {
      var res = await fetch("/api/pay/tx/submit", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ order: orderId, tx_hash: tx }),
      });
      var data = await res.json().catch(function () { return null; });
      if (!res.ok || !data || !data.ok) {
        status.textContent = friendlyTxError((data && data.error) || "provider_error");
        btn.disabled = false;
        return;
      }
      status.textContent =
        "Recorded. Our team verifies the transfer on-chain manually — your receipt and course access follow by email at " +
        state.email + ".";
      input.disabled = true;
      btn.disabled = true;
    } catch (e) {
      status.textContent = "Network error — please try again.";
      btn.disabled = false;
    }
  }

  // Boot: prefetch UD-resolved addresses so the direct panel is instant.
  fetch("/api/pay/ud").then(function (r) { return r.ok ? r.json() : null; })
    .then(function (j) { if (j && j.ok) state.ud = j; })
    .catch(function () {});
  renderForm();
})();
