(function () {
  var root = document.getElementById("account-root");
  if (!root) return;

  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"]/g, function (ch) {
      return "&#" + ch.charCodeAt(0) + ";";
    });
  }

  function draw(session, providers) {
    var user = session && session.user;
    var social = ["google", "github", "x"]
      .map(function (name) {
        var label = name === "x" ? "X" : name.charAt(0).toUpperCase() + name.slice(1);
        var ready = providers && providers[name];
        return (
          '<a class="inline-flex h-11 items-center justify-center rounded-lg border border-paper/15 px-4 font-display text-xs uppercase tracking-[0.14em]" href="/api/auth/' +
          name +
          '/start">' +
          (ready ? "Continue with " + label : label + " — not connected") +
          "</a>"
        );
      })
      .join("");
    var who = user
      ? "<p class=\"mt-4 text-paper\">Signed in with " +
        esc(user.provider) +
        (user.email ? " · " + esc(user.email) : "") +
        (user.address ? " · " + esc(user.address) : "") +
        "</p>" +
        '<form id="profile" class="mt-4 flex flex-col gap-2 max-w-md">' +
        '<label class="text-sm text-muted" for="display-name">Display name</label>' +
        '<input id="display-name" class="h-11 rounded-lg border border-paper/15 bg-void px-3 text-paper" maxlength="80" value="' +
        esc(user.name || "") +
        '"/>' +
        '<button class="h-11 rounded-lg bg-paper px-4 font-display text-xs uppercase tracking-[0.14em] text-void" type="submit">Save registration</button>' +
        "</form>" +
        '<button id="logout" class="mt-3 text-sm text-cyan" type="button">Sign out</button>'
      : "";
    root.innerHTML =
      '<div class="flex flex-col gap-3 sm:flex-row sm:flex-wrap">' +
      social +
      '<button id="eth" class="inline-flex h-11 items-center justify-center rounded-lg bg-paper px-4 font-display text-xs uppercase tracking-[0.14em] text-void" type="button">Sign in with Ethereum</button>' +
      "</div>" +
      who +
      '<p id="account-note" class="mt-4 text-sm text-muted"></p>';
    var note = document.getElementById("account-note");
    if (!session.secret) note.textContent = "Sign-in is waiting for the SESSION_SECRET worker secret.";
    var eth = document.getElementById("eth");
    if (eth) {
      eth.addEventListener("click", function () {
        if (!window.ethereum) {
          note.textContent = "This browser has no Ethereum wallet.";
          return;
        }
        window.ethereum
          .request({ method: "eth_requestAccounts" })
          .then(function (accounts) {
            return fetch("/api/auth/siwe/nonce", { method: "POST" }).then(function (res) {
              return res.json().then(function (data) {
                return { accounts: accounts, data: data, ok: res.ok };
              });
            });
          })
          .then(function (out) {
            if (!out.ok) throw new Error(out.data.error || "nonce");
            var message = [
              location.host + " wants you to sign in with your Ethereum account:",
              out.accounts[0],
              "",
              "Sign in to Interstitium Labs",
              "",
              "URI: " + location.origin + "/account/",
              "Version: 1",
              "Chain ID: 1",
              "Nonce: " + out.data.nonce,
              "Issued At: " + out.data.issuedAt,
            ].join("\n");
            return window.ethereum
              .request({ method: "personal_sign", params: [message, out.accounts[0]] })
              .then(function (signature) {
                return fetch("/api/auth/siwe/verify", {
                  method: "POST",
                  headers: { "content-type": "application/json" },
                  body: JSON.stringify({ address: out.accounts[0], signature: signature }),
                });
              });
          })
          .then(function (res) {
            if (!res.ok) return res.json().then(function (data) { throw new Error(data.error || "rejected"); });
            location.reload();
          })
          .catch(function (err) {
            note.textContent = err && err.message ? err.message : "Wallet sign-in failed.";
          });
      });
    }
    var form = document.getElementById("profile");
    if (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        fetch("/api/account", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ displayName: document.getElementById("display-name").value }),
        })
          .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
          .then(function (out) {
            note.textContent = out.ok ? "Registration saved." : (out.data.error || "Could not save.");
          });
      });
    }
    var logout = document.getElementById("logout");
    if (logout) {
      logout.addEventListener("click", function () {
        fetch("/api/auth/logout", { method: "POST" }).then(function () { location.reload(); });
      });
    }
  }

  Promise.all([
    fetch("/api/session").then(function (res) { return res.json(); }),
    fetch("/api/auth/providers").then(function (res) { return res.json(); }),
  ])
    .then(function (pair) { draw(pair[0], pair[1]); })
    .catch(function () {
      root.textContent = "Account service is unavailable.";
    });
})();
