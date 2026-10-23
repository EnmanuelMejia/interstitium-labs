(function () {
  var cfg = window.IL_ENROLL || { tiers: [], disclaimer: "Config missing." };
  var status = document.getElementById("enroll-status");
  var grid = document.getElementById("tier-grid");
  if (!status || !grid) return;

  var live = !!cfg.paymentsLive;

  function escAttr(v) {
    return String(v == null ? "" : v)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;");
  }

  function bindWaitlistForm(root) {
    var form = root.querySelector("#waitlist-form");
    if (!form) return;
    var err = root.querySelector("#wl-error");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = form.elements.name.value.trim();
      var email = form.elements.email.value.trim();
      var tier = "prep-sprint";
      try {
        var tierEl = form.querySelector('input[name="tier"]:checked');
        if (tierEl && tierEl.value) tier = tierEl.value;
      } catch (e) {}
      err.hidden = true;
      err.textContent = "";
      if (!name || !email) {
        err.textContent = "Enter your name and email so we can reach you.";
        err.hidden = false;
        return;
      }
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      fetch("/api/waitlist", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ name: name, email: email, tier: tier }),
      })
        .then(function (res) {
          return res.json().then(function (data) {
            return { status: res.status, data: data };
          });
        })
        .then(function (r) {
          if (r.status === 200 && r.data && r.data.ok) {
            window.location.href = "/enroll/success.html";
            return;
          }
          var msg = "Could not join the waitlist. Check your email and try again.";
          if (r.data && r.data.error === "email_invalid") msg = "That email does not look valid — check it and try again.";
          err.textContent = msg;
          err.hidden = false;
          btn.disabled = false;
        })
        .catch(function () {
          err.textContent = "Network error — try again in a moment.";
          err.hidden = false;
          btn.disabled = false;
        });
    });
  }

  if (!live) {
    // Waitlist form is static HTML (works without JS); just bind + disclaimer.
    var disc = document.getElementById("enroll-disclaimer");
    if (disc && cfg.disclaimer) disc.textContent = cfg.disclaimer;
    bindWaitlistForm(status);

    grid.innerHTML =
      '<article class="rounded-xl border border-paper/10 bg-panel p-6 sm:p-8 lg:col-span-3">' +
      '<p class="font-mono text-[0.62rem] uppercase tracking-[0.22em] text-cyan">Enrollment opens soon</p>' +
      '<h2 class="mt-3 font-display text-2xl tracking-[-0.02em]">Seats not for sale yet</h2>' +
      '<p class="mt-4 max-w-2xl text-sm leading-relaxed text-muted">Pricing is shown for planning — checkout opens when enrollment goes live. Join the waitlist and we will email you first.</p>' +
      '<ul class="mt-6 grid gap-3 sm:grid-cols-3">' +
      (cfg.tiers || [])
        .map(function (t) {
          var feats = (t.features || [])
            .map(function (f) {
              return "<li>" + f + "</li>";
            })
            .join("");
          return (
            '<li class="rounded-lg bg-void/60 p-4 shadow-[0_0_0_1px_rgba(232,238,245,0.08)]">' +
            '<p class="font-mono text-[0.58rem] uppercase tracking-[0.18em] text-gold">' +
            (t.badge || "") +
            "</p>" +
            '<p class="mt-2 font-display text-lg text-paper">' +
            (t.name || "") +
            "</p>" +
            '<p class="mt-1 font-display text-xl text-muted">' +
            (t.publishablePrice || "") +
            "</p>" +
            '<p class="mt-2 text-sm leading-relaxed text-muted">' +
            (t.blurb || "") +
            "</p>" +
            '<ul class="mt-3 space-y-1 text-sm text-muted">' +
            feats +
            "</ul>" +
            "</li>"
          );
        })
        .join("") +
      "</ul></article>";
    return;
  }

  status.innerHTML =
    '<p class="font-mono text-[0.58rem] uppercase tracking-[0.18em] text-cyan">Payments</p><p class="mt-2 text-paper">Live checkout enabled for flagged tiers.</p>';

  (cfg.tiers || []).forEach(function (t) {
    var feats = (t.features || [])
      .map(function (f) {
        return "<li>" + f + "</li>";
      })
      .join("");
    var stripeOk =
      t.stripeEnabled &&
      t.stripePaymentLink &&
      t.stripePaymentLink.indexOf("PLACEHOLDER") === -1;
    var paypalOk =
      t.paypalEnabled &&
      t.paypalLink &&
      t.paypalLink.indexOf("PLACEHOLDER") === -1;
    var stripeBtn = stripeOk
      ? '<a href="' +
        t.stripePaymentLink +
        '" class="inline-flex h-11 w-full items-center justify-center rounded-lg bg-paper px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-void hover:bg-paper/90">Pay with card / Stripe</a>'
      : '<button type="button" disabled class="inline-flex h-11 w-full cursor-not-allowed items-center justify-center rounded-lg bg-paper/20 px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-muted">Stripe inactive</button>';
    var paypalBtn = paypalOk
      ? '<a href="' +
        t.paypalLink +
        '" class="inline-flex h-11 w-full items-center justify-center rounded-lg border border-paper/15 px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-paper hover:border-paper/30">PayPal</a>'
      : '<button type="button" disabled class="inline-flex h-11 w-full cursor-not-allowed items-center justify-center rounded-lg border border-paper/10 px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-muted">PayPal inactive</button>';
    var art = document.createElement("article");
    art.className =
      "flex flex-col rounded-xl bg-panel p-6 shadow-[0_0_0_1px_rgba(232,238,245,0.08)] sm:p-7";
    art.innerHTML =
      '<p class="font-mono text-[0.62rem] uppercase tracking-[0.22em] text-gold">' +
      (t.badge || "") +
      "</p>" +
      '<h2 class="mt-3 font-display text-2xl tracking-[-0.02em]">' +
      t.name +
      "</h2>" +
      '<p class="mt-2 font-display text-3xl text-paper">' +
      (t.publishablePrice || "") +
      ' <span class="font-mono text-[0.62rem] uppercase tracking-[0.14em] text-muted">' +
      (t.period || "") +
      "</span></p>" +
      '<p class="mt-4 flex-1 text-sm leading-relaxed text-muted">' +
      (t.blurb || "") +
      "</p>" +
      '<ul class="mt-4 space-y-1 text-sm text-muted prose-il">' +
      feats +
      "</ul>" +
      '<div class="mt-6 flex flex-col gap-2">' +
      stripeBtn +
      paypalBtn +
      "</div>";
    grid.appendChild(art);
  });
})();
