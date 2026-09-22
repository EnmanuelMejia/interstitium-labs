(function () {
  var cfg = window.IL_ENROLL || { tiers: [], disclaimer: "Config missing." };
  var status = document.getElementById("enroll-status");
  var live = !!cfg.paymentsLive;
  status.innerHTML = live
    ? '<p class="font-mono text-[0.58rem] uppercase tracking-[0.18em] text-cyan">Payments</p><p class="mt-2 text-paper">Live checkout enabled for flagged tiers.</p>'
    : '<p class="font-mono text-[0.58rem] uppercase tracking-[0.18em] text-gold">Payments inactive</p><p class="mt-2">' + (cfg.disclaimer || "") + "</p>";
  var grid = document.getElementById("tier-grid");
  (cfg.tiers || []).forEach(function (t) {
    var feats = (t.features || []).map(function (f) { return "<li>" + f + "</li>"; }).join("");
    var stripeOk = live && t.stripeEnabled && t.stripePaymentLink && t.stripePaymentLink.indexOf("PLACEHOLDER") === -1;
    var paypalOk = live && t.paypalEnabled && t.paypalLink && t.paypalLink.indexOf("PLACEHOLDER") === -1;
    var stripeBtn = stripeOk
      ? '<a href="' + t.stripePaymentLink + '" class="inline-flex h-11 w-full items-center justify-center rounded-lg bg-paper px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-void hover:bg-paper/90">Pay with card / Stripe</a>'
      : '<button type="button" disabled class="inline-flex h-11 w-full cursor-not-allowed items-center justify-center rounded-lg bg-paper/20 px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-muted" title="Paste live Stripe Payment Link in config.js">Stripe inactive</button>';
    var paypalBtn = paypalOk
      ? '<a href="' + t.paypalLink + '" class="inline-flex h-11 w-full items-center justify-center rounded-lg border border-paper/15 px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-paper hover:border-paper/30">PayPal</a>'
      : '<button type="button" disabled class="inline-flex h-11 w-full cursor-not-allowed items-center justify-center rounded-lg border border-paper/10 px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-muted" title="Paste live PayPal URL in config.js">PayPal inactive</button>';
    var art = document.createElement("article");
    art.className = "flex flex-col rounded-xl bg-panel p-6 shadow-[0_0_0_1px_rgba(232,238,245,0.08)] sm:p-7";
    art.innerHTML =
      '<p class="font-mono text-[0.62rem] uppercase tracking-[0.22em] text-gold">' + (t.badge || "") + "</p>" +
      '<h2 class="mt-3 font-display text-2xl tracking-[-0.02em]">' + t.name + "</h2>" +
      '<p class="mt-2 font-display text-3xl text-paper">' + (t.publishablePrice || "") +
      ' <span class="font-mono text-[0.62rem] uppercase tracking-[0.14em] text-muted">' + (t.period || "") + "</span></p>" +
      '<p class="mt-4 flex-1 text-sm leading-relaxed text-muted">' + (t.blurb || "") + "</p>" +
      '<ul class="mt-4 space-y-1 text-sm text-muted prose-il">' + feats + "</ul>" +
      '<div class="mt-6 flex flex-col gap-2">' + stripeBtn + paypalBtn + "</div>";
    grid.appendChild(art);
  });
})();
