/**
 * Interstitium Labs — client account session library (vanilla, no build).
 * Mounts: [data-il-auth] sign-in form · [data-il-auth-required] page gate ·
 *          [data-il-account-email] label · [data-il-signout] button.
 * Public API: window.ILAccount
 *
 * Conventions (server, docs/_worker.js):
 *   GET  /api/me                 -> { ok, email } or 401
 *   POST /api/auth/request       { email } -> { ok } (magic link emailed)
 *   POST /api/auth/signout       -> { ok }
 *   GET  /api/progress           -> { ok, progress, updated_at } (session)
 *   PUT  /api/progress           { progress } -> merged (session)
 *
 * First-sign-in local merge: every il.* localStorage key is mirrored to the
 * server once per account, under the top-level key "local_mirror"
 * ({ "<key>": <value> }), then flagged with il.account.merged.v1.<email>.
 */
(function (global) {
  "use strict";
  var doc = global.document;

  var MERGE_FLAG_PREFIX = "il.account.merged.v1.";
  var meCache = null; // null = not signed in, string = email, false = unknown
  var mePromise = null;

  function emailOk(email) {
    return (
      typeof email === "string" &&
      email.length <= 254 &&
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())
    );
  }

  function api(path, opts) {
    opts = opts || {};
    var headers = { accept: "application/json" };
    if (opts.body != null) headers["content-type"] = "application/json";
    return global
      .fetch(path, {
        method: opts.method || "GET",
        credentials: "same-origin",
        headers: headers,
        body: opts.body != null ? JSON.stringify(opts.body) : undefined,
      })
      .then(function (res) {
        return res.json().catch(function () {
          return { ok: false, error: "bad_response" };
        });
      });
  }

  /** Resolved session email, or null. Cached after first call. */
  function me(refresh) {
    if (mePromise && !refresh) return mePromise;
    mePromise = api("/api/me")
      .then(function (r) {
        meCache = r && r.ok && r.email ? String(r.email) : null;
        return meCache;
      })
      .catch(function () {
        meCache = null;
        return null;
      });
    return mePromise;
  }

  function signOut() {
    return api("/api/auth/signout", { method: "POST" }).then(function () {
      meCache = null;
      mePromise = null;
      return true;
    });
  }

  function getProgress() {
    return api("/api/progress").then(function (r) {
      if (r && r.ok && r.progress) return r.progress;
      throw new Error((r && r.error) || "progress_unavailable");
    });
  }

  function putProgress(progress) {
    return api("/api/progress", {
      method: "PUT",
      body: { progress: progress },
    }).then(function (r) {
      if (r && r.ok) return r.progress;
      throw new Error((r && r.error) || "progress_unavailable");
    });
  }

  /** Read every il.* localStorage entry into a plain object. */
  function readLocalMirror() {
    var out = {};
    try {
      for (var i = 0; i < global.localStorage.length; i++) {
        var k = global.localStorage.key(i);
        if (!k || k.indexOf("il.") !== 0) continue;
        var raw = global.localStorage.getItem(k);
        var v;
        try {
          v = JSON.parse(raw);
        } catch (e) {
          v = raw;
        }
        out[k] = v;
      }
    } catch (e) {
      /* private mode — nothing to mirror */
    }
    return out;
  }

  /** One-time: push local il.* state into the server account. */
  function syncLocalOnce(email) {
    var flag = MERGE_FLAG_PREFIX + email;
    try {
      if (global.localStorage.getItem(flag) === "1") return Promise.resolve(false);
    } catch (e) {}
    var mirror = readLocalMirror();
    return putProgress({ local_mirror: mirror })
      .then(function () {
        try {
          global.localStorage.setItem(flag, "1");
        } catch (e) {}
        return true;
      })
      .catch(function () {
        return false;
      });
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  var ERROR_COPY = {
    email_invalid: "Enter a valid email address.",
    too_many_requests: "A link was just sent — check your inbox, then try again in a minute.",
    email_send_failed: "We couldn't send the email. Try again, or contact us.",
    store_unavailable: "Sign-in is temporarily unavailable. Try again shortly.",
    accounts_unavailable: "Sign-in is temporarily unavailable. Try again shortly.",
  };

  function paintForm(root, state) {
    // state: idle | sending | sent | signedin
    if (state === "signedin") {
      root.innerHTML =
        '<div class="il-auth-box"><p class="il-kicker">Signed in</p>' +
        '<p class="il-auth-email" data-il-account-email>' + esc(root.getAttribute("data-il-auth-email") || "") + "</p>" +
        '<div class="il-auth-actions"><a class="il-btn" href="/progress/">My dashboard</a> ' +
        '<button type="button" class="il-btn il-btn-ghost" data-il-signout>Sign out</button></div></div>';
      wireSignedIn(root);
      return;
    }
    if (state === "sent") {
      root.innerHTML =
        '<div class="il-auth-box"><p class="il-kicker">Check your email</p>' +
        '<p>We sent a sign-in link to <strong>' + esc(root.getAttribute("data-il-auth-sent-to") || "") + '</strong>. ' +
        "It expires in 15 minutes.</p>" +
        '<p class="il-auth-hint">Didn\'t arrive? Check spam, then <button type="button" class="il-link" data-il-auth-retry>send a new link</button>.</p></div>';
      var retry = root.querySelector("[data-il-auth-retry]");
      if (retry) {
        retry.addEventListener("click", function () {
          paintForm(root, "idle");
        });
      }
      return;
    }
    root.innerHTML =
      '<div class="il-auth-box"><p class="il-kicker">Sign in</p>' +
      '<h3 class="il-auth-title">Continue with</h3>' +
      '<div data-il-oauth-buttons style="display:flex;flex-direction:column;gap:.6rem;margin:.8rem 0 1.2rem"></div>' +
      '<p class="il-auth-hint" style="text-align:center;margin:.4rem 0">— or —</p>' +
      '<h3 class="il-auth-title" style="font-size:1.1rem">Continue with email</h3>' +
      '<p class="il-auth-hint">No password — we email you a one-time sign-in link.</p>' +
      '<form data-il-auth-form novalidate><label class="il-field"><span>Email</span>' +
      '<input type="email" name="email" autocomplete="email" required placeholder="you@example.com"/></label>' +
      '<p class="il-auth-error" data-il-auth-error hidden></p>' +
      '<button type="submit" class="il-btn" data-il-auth-submit>Send sign-in link</button></form></div>';
    /* 2026-10-09: OAuth social login buttons. */
    (function renderOAuth() {
      var wrap = root.querySelector("[data-il-oauth-buttons]");
      if (!wrap) return;
      api("/api/auth/oauth/providers", { method: "GET" }).then(function (r) {
        if (!r || !r.ok || !Array.isArray(r.providers)) return;
        var names = { github: "GitHub", google: "Google", microsoft: "Microsoft", apple: "Apple", linkedin: "LinkedIn", twitter: "X (Twitter)", facebook: "Facebook" };
        var configuredCount = 0;
        r.providers.forEach(function (p) {
          var b = document.createElement("a");
          b.className = "il-btn il-btn-ghost";
          b.style.cssText = "width:100%;text-decoration:none";
          if (p.configured) {
            configuredCount++;
            b.textContent = "Continue with " + (names[p.provider] || p.provider);
            b.href = "/auth/oauth/" + p.provider;
          } else {
            /* Provider activates when the owner adds its keys — show the
               roadmap honestly instead of a dead button. */
            b.textContent = "Continue with " + (names[p.provider] || p.provider) + " — coming soon";
            b.href = "#";
            b.style.opacity = ".45";
            b.setAttribute("aria-disabled", "true");
            b.title = "This sign-in option is being configured";
            b.addEventListener("click", function (e) { e.preventDefault(); });
          }
          wrap.appendChild(b);
        });
        if (!wrap.children.length) { wrap.style.display = "none"; return; }
        /* 2026-10-09: clear "setup required" state when no providers configured */
        if (configuredCount === 0) {
          var note = document.createElement("p");
          note.className = "il-auth-hint";
          note.style.cssText = "text-align:center;font-size:.78rem;margin:.2rem 0 0";
          note.textContent = "Social sign-in is unavailable — use email for now.";
          wrap.appendChild(note);
        }
      }, function () {});
    })();
    var form = root.querySelector("[data-il-auth-form]");
    var errEl = root.querySelector("[data-il-auth-error]");
    var submitBtn = root.querySelector("[data-il-auth-submit]");
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var email = form.email.value.trim().toLowerCase();
      errEl.hidden = true;
      errEl.textContent = "";
      if (!emailOk(email)) {
        errEl.textContent = ERROR_COPY.email_invalid;
        errEl.hidden = false;
        return;
      }
      submitBtn.disabled = true;
      submitBtn.textContent = "Sending…";
      api("/api/auth/request", { method: "POST", body: { email: email } }).then(
        function (r) {
          if (r && r.ok) {
            root.setAttribute("data-il-auth-sent-to", email);
            paintForm(root, "sent");
          } else {
            var msg = ERROR_COPY[(r && r.error) || ""] || "Something went wrong. Try again.";
            errEl.textContent = msg;
            errEl.hidden = false;
            submitBtn.disabled = false;
            submitBtn.textContent = "Send sign-in link";
          }
        },
        function () {
          errEl.textContent = "Network error. Try again.";
          errEl.hidden = false;
          submitBtn.disabled = false;
          submitBtn.textContent = "Send sign-in link";
        }
      );
    });
  }

  function wireSignedIn(root) {
    var btn = root.querySelector("[data-il-signout]");
    if (btn) {
      btn.addEventListener("click", function () {
        btn.disabled = true;
        signOut().then(function () {
          global.location.reload();
        });
      });
    }
    // Also bind any free-standing [data-il-signout] buttons on the page.
    var extra = doc.querySelectorAll("button[data-il-signout]");
    for (var i = 0; i < extra.length; i++) {
      if (extra[i] === btn) continue;
      extra[i].addEventListener("click", function () {
        signOut().then(function () {
          global.location.reload();
        });
      });
    }
  }

  function mountAuth(root) {
    paintForm(root, "idle");
    me().then(function (email) {
      if (email) {
        root.setAttribute("data-il-auth-email", email);
        paintForm(root, "signedin");
        // First sign-in: merge localStorage il.* state into the server.
        syncLocalOnce(email);
      }
    });
  }

  /** Pages that require sign-in carry [data-il-auth-required]; gate them. */
  function gate() {
    var gated = doc.querySelectorAll("[data-il-auth-required]");
    if (!gated.length) return;
    me().then(function (email) {
      if (email) {
        var labels = doc.querySelectorAll("[data-il-account-email]");
        for (var i = 0; i < labels.length; i++) labels[i].textContent = email;
        doc.body.classList.add("il-signed-in");
        // First sign-in: merge localStorage il.* state into the server.
        syncLocalOnce(email);
        var ev = new CustomEvent("il:signedin", { detail: { email: email } });
        doc.dispatchEvent(ev);
      } else {
        var next = global.location.pathname + global.location.search;
        global.location.replace("/account/?next=" + encodeURIComponent(next));
      }
    });
  }

  function boot() {
    var nodes = doc.querySelectorAll("[data-il-auth]");
    for (var i = 0; i < nodes.length; i++) mountAuth(nodes[i]);
    gate();
  }

  global.ILAccount = {
    me: me,
    signOut: signOut,
    getProgress: getProgress,
    putProgress: putProgress,
    syncLocalOnce: syncLocalOnce,
    readLocalMirror: readLocalMirror,
    boot: boot,
  };

  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", boot);
  else boot();
})(typeof window !== "undefined" ? window : this);
