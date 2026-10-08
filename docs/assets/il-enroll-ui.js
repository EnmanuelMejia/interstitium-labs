(function () {
  var status = document.getElementById("enroll-status");
  var grid = document.getElementById("tier-grid");
  var cfg = window.IL_ENROLL || { tiers: [] };
  if (!status || !grid) return;

  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"]/g, function (ch) {
      return "&#" + ch.charCodeAt(0) + ";";
    });
  }

  function say(html) {
    status.innerHTML = html;
  }

  function units(amount, decimals) {
    var raw = BigInt(amount).toString().padStart(decimals + 1, "0");
    var whole = raw.slice(0, raw.length - decimals);
    var frac = raw.slice(raw.length - decimals).replace(/0+$/, "");
    return frac ? whole + "." + frac.slice(0, 6) : whole;
  }

  function transferData(to, amount) {
    return (
      "0xa9059cbb" +
      to.slice(2).toLowerCase().padStart(64, "0") +
      BigInt(amount).toString(16).padStart(64, "0")
    );
  }

  async function pay(payTo, tierId, asset, amount, token, quote) {
    try {
    if (!window.ethereum) {
      say("<p>No wallet was found in this browser. Install a wallet that speaks Ethereum, then pay " + esc(payTo.domain) + ".</p>");
      return;
    }
    try {
      await window.ethereum.request({
        method: "wallet_switchEthereumChain",
        params: [{ chainId: "0x1" }],
      });
    } catch (err) {
      if (!err || err.code !== 4902) {
        say("<p>Switch the wallet to Ethereum mainnet before paying.</p>");
        return;
      }
    }
    var accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
    var tx;
    if (asset === "eth") {
      tx = await window.ethereum.request({
        method: "eth_sendTransaction",
        params: [{ from: accounts[0], to: payTo.address, value: "0x" + BigInt(amount).toString(16) }],
      });
    } else {
      tx = await window.ethereum.request({
        method: "eth_sendTransaction",
        params: [{ from: accounts[0], to: token, data: transferData(payTo.address, amount) }],
      });
    }
    var verified = await fetch("/api/pay/verify", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ tier: tierId, asset: asset, txHash: tx, quote: quote || "" }),
    });
    var result = await verified.json();
    say(
      "<p>Transaction " +
        esc(tx) +
        " is " +
        esc(result.status || result.error || "submitted") +
        ". Funds go only to " +
        esc(payTo.domain) +
        " (" +
        esc(payTo.address) +
        ").</p>"
    );
    } catch (err) {
      say("<p>" + esc(err && err.message ? err.message : "The wallet did not send the payment.") + "</p>");
    }
  }

  fetch("/api/pay/config")
    .then(function (res) {
      return res.json();
    })
    .then(function (payTo) {
      var tiers = cfg.tiers || [];
      var byId = {};
      (payTo.tiers || []).forEach(function (tier) {
        byId[tier.id] = tier;
      });
      say(
        '<p class="font-mono text-[0.58rem] uppercase tracking-[0.18em] text-cyan">Payments</p>' +
          '<p class="mt-2 text-paper">Card checkout uses Stripe when the worker secret is set. Crypto is paid on Ethereum mainnet to <a class="text-cyan" href="/account/">' +
          esc(payTo.domain) +
          "</a>, record crypto.ETH.address.</p>" +
          '<p class="mt-2 text-sm text-muted">' +
          esc(payTo.iso20022) +
          "</p>" +
          '<p class="mt-2 font-mono text-xs text-gold">' +
          esc(payTo.address) +
          "</p>"
      );
      grid.innerHTML = "";
      tiers.forEach(function (tier) {
        var remote = byId[tier.id];
        if (!remote) return;
        var art = document.createElement("article");
        art.className = "flex flex-col rounded-xl bg-panel p-6 shadow-[0_0_0_1px_rgba(232,238,245,0.08)] sm:p-7";
        var buttons =
          '<button type="button" data-card="1" class="inline-flex h-11 w-full items-center justify-center rounded-lg bg-paper px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-void">Card via Stripe</button>' +
          '<button type="button" data-asset="usdc" class="inline-flex h-11 w-full items-center justify-center rounded-lg border border-paper/15 px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-paper">Pay ' +
          esc(units(remote.stable.usdc, 6)) +
          " USDC</button>" +
          '<button type="button" data-asset="usdt" class="inline-flex h-11 w-full items-center justify-center rounded-lg border border-paper/15 px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-paper">Pay ' +
          esc(units(remote.stable.usdt, 6)) +
          " USDT</button>" +
          '<button type="button" data-asset="dai" class="inline-flex h-11 w-full items-center justify-center rounded-lg border border-paper/15 px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-paper">Pay ' +
          esc(units(remote.stable.dai, 18)) +
          " DAI</button>" +
          '<button type="button" data-asset="eth" class="inline-flex h-11 w-full items-center justify-center rounded-lg border border-paper/15 px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-paper">Pay with ETH</button>' +
          '<button type="button" data-asset="qnt" class="inline-flex h-11 w-full items-center justify-center rounded-lg border border-paper/15 px-4 font-display text-xs font-medium uppercase tracking-[0.14em] text-paper">Pay with QNT</button>';
        art.innerHTML =
          '<p class="font-mono text-[0.62rem] uppercase tracking-[0.22em] text-gold">' +
          esc(tier.badge || "") +
          "</p><h2 class=\"mt-3 font-display text-2xl tracking-[-0.02em]\">" +
          esc(tier.name) +
          '</h2><p class="mt-2 font-display text-3xl text-paper">' +
          esc(tier.publishablePrice || "") +
          '</p><p class="mt-4 flex-1 text-sm leading-relaxed text-muted">' +
          esc(tier.blurb || "") +
          '</p><div class="mt-6 flex flex-col gap-2">' +
          buttons +
          "</div>";
        art.addEventListener("click", function (event) {
          var button = event.target.closest("button");
          if (!button) return;
          if (button.getAttribute("data-card")) {
            fetch("/api/checkout", {
              method: "POST",
              headers: { "content-type": "application/json" },
              body: JSON.stringify({ tier: tier.id }),
            })
              .then(function (res) {
                return res.json().then(function (data) {
                  return { ok: res.ok, data: data };
                });
              })
              .then(function (out) {
                if (out.ok && out.data.url) {
                  location.href = out.data.url;
                  return;
                }
                say("<p>Stripe is not connected yet. Set the STRIPE_SECRET_KEY worker secret. Crypto buttons on this page already pay " + esc(payTo.domain) + ".</p>");
              });
            return;
          }
          var asset = button.getAttribute("data-asset");
          var amount = remote.stable[asset];
          var token = payTo.assets[asset] && payTo.assets[asset].token;
          if (amount) {
            pay(payTo, tier.id, asset, amount, token, "");
            return;
          }
          fetch("/api/pay/quote?tier=" + encodeURIComponent(tier.id) + "&asset=" + asset)
            .then(function (res) {
              return res.json().then(function (data) {
                return { ok: res.ok, data: data };
              });
            })
            .then(function (out) {
              if (!out.ok) {
                say("<p>No live " + esc(asset.toUpperCase()) + " price, so that button will not invent an amount.</p>");
                return;
              }
              pay(payTo, tier.id, asset, out.data.amount, token, out.data.quote);
            });
        });
        grid.appendChild(art);
      });
    })
    .catch(function () {
      say("<p>Payment configuration could not be loaded.</p>");
    });
})();
