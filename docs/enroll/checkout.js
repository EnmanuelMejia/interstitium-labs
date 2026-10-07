/**
 * Interstitium Labs — checkout UI (Phase 4b).
 *
 * Flow: pick tier (via ?tier=) -> email -> provider -> (coin/rail for crypto)
 * -> POST /api/pay/create -> redirect to Stripe/PayPal/NOWPayments hosted
 * checkout, or render the direct-wallet panel (address + QR + tag/memo).
 *
 * Prices are display-only here; the Worker is the price authority.
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
      sub: "Send straight to enmanuelmejia.crypto. Address + QR shown here; no middleman.",
    },
  ];

  var root = document.getElementById("il-root");
  var params = new URLSearchParams(window.location.search);
  var tierId = params.get("tier") || "prep-sprint";
  if (!TIERS[tierId]) tierId = "prep-sprint";
  var tier = TIERS[tierId];

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
        : "Pay straight to <strong>enmanuelmejia.crypto</strong>. We show the address and QR here; include the destination tag / memo where shown.") +
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
    var payload = { provider: provider, item: tierId, email: state.email };
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
      '<p class="il-ud">Pay to enmanuelmejia.crypto</p>' +
      '<div class="il-qr" id="il-qr" role="img" aria-label="QR code for the receiving address"></div>' +
      '<p class="il-hint">Receiving address' + (d.source ? " · via " + esc(d.source === "ud" ? "enmanuelmejia.crypto" : "configured wallet") : "") + "</p>" +
      '<p class="il-addr">' + esc(d.address) + "</p>" +
      '<button class="il-copy" type="button" data-copy="' + esc(d.address) + '">Copy address</button>' +
      extraRow +
      '<p class="il-order__price" style="margin:0.6rem 0 0">' + esc(tier.price) + ' <span style="font-size:0.75rem;color:var(--il-muted)">USD-equivalent in ' + esc(data.coin) + "</span></p>" +
      '<p class="il-wait">Send the USD-equivalent of <strong>' + esc(tier.price) + "</strong> in " + esc(data.coin) +
      " to the address above" +
      (d.destination_tag ? " with the destination tag" : d.memo ? " with the memo" : "") +
      ". Direct payments are verified by our team — your receipt and course access follow by email at <strong>" + esc(state.email) + "</strong>.</p>" +
      '<p class="il-hint">Order <span style="font-family:monospace">' + esc(data.order_id) + "</span> · status: awaiting payment</p>" +
      "</section>";
    root.innerHTML = html;
    renderQr(document.getElementById("il-qr"), d.qr_payload || d.address);
    root.querySelectorAll("[data-copy]").forEach(function (b) {
      b.addEventListener("click", function () { copyText(b.getAttribute("data-copy"), b); });
    });
  }

  // Boot: prefetch UD-resolved addresses so the direct panel is instant.
  fetch("/api/pay/ud").then(function (r) { return r.ok ? r.json() : null; })
    .then(function (j) { if (j && j.ok) state.ud = j; })
    .catch(function () {});
  renderForm();
})();
