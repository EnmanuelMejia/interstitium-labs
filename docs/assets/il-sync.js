/**
 * Interstitium Labs — cross-device sync for signed-in learners.
 *
 * Local-first: every store keeps working offline in localStorage. When a
 * session exists (ILAccount), each store is reconciled with the server
 * copy at /api/user/sync using per-store updated_at timestamps:
 *   - server newer  -> server data is written into the local keys
 *   - local newer   -> local data is PUT to the server
 *   - tie / none    -> nothing moves
 * Local edit tracking: a meta record (il.sync.meta.v1) holds the newest
 * updated_at seen per store; the raw local values are fingerprinted so
 * edits made by other components (notes vault, Noah, interview UI) are
 * detected on the next tick without those components knowing sync exists.
 *
 * Stores (server whitelist mirrors _worker.js SYNC_STORES):
 *   notes      -> il-notes-v1
 *   interviews -> il-mock-interviews-v1
 *   noah       -> noah-ai-history-v1, noah-session-v2
 *   prefs      -> il-noah-profile, il-mock-interview-settings-v1
 *   goals      -> il-goals-v1 (Noah/Genesis goal summaries cache; the
 *                 goals engine also mirrors server-side into this store)
 * (CBT/course progress syncs through /api/progress + ILAccount's
 *  local_mirror; skills profiles live in the bootcamp shell and join
 *  this registry when present under il.skills.v1.)
 *
 * Public API: window.ILSync { syncNow, stores }
 */
(function (global) {
  "use strict";

  var META_KEY = "il.sync.meta.v1";
  var STORES = {
    notes: ["il-notes-v1"],
    interviews: ["il-mock-interviews-v1"],
    noah: ["noah-ai-history-v1", "noah-session-v2"],
    prefs: ["il-noah-profile", "il-mock-interview-settings-v1"],
    skills: ["il.skills.v1"],
    goals: ["il-goals-v1"],
  };
  var TICK_MS = 45000;
  var syncing = false;

  function ls() {
    try {
      return global.localStorage;
    } catch (e) {
      return null;
    }
  }

  function readMeta() {
    var s = ls();
    if (!s) return {};
    try {
      return JSON.parse(s.getItem(META_KEY) || "{}") || {};
    } catch (e) {
      return {};
    }
  }

  function writeMeta(meta) {
    var s = ls();
    if (!s) return;
    try {
      s.setItem(META_KEY, JSON.stringify(meta));
    } catch (e) {}
  }

  /** Current local payload for a store: { <localKey>: <parsed value> }. */
  function readLocal(store) {
    var s = ls();
    if (!s) return null;
    var keys = STORES[store] || [];
    var out = {};
    var any = false;
    for (var i = 0; i < keys.length; i++) {
      var raw = null;
      try {
        raw = s.getItem(keys[i]);
      } catch (e) {}
      if (raw != null) {
        any = true;
        try {
          out[keys[i]] = JSON.parse(raw);
        } catch (e) {
          out[keys[i]] = raw;
        }
      }
    }
    return any ? out : null;
  }

  function writeLocal(store, data) {
    var s = ls();
    if (!s || !data || typeof data !== "object") return;
    var keys = STORES[store] || [];
    for (var i = 0; i < keys.length; i++) {
      if (Object.prototype.hasOwnProperty.call(data, keys[i])) {
        try {
          var v = data[keys[i]];
          s.setItem(keys[i], typeof v === "string" ? v : JSON.stringify(v));
        } catch (e) {}
      }
    }
  }

  function fingerprint(data) {
    var str;
    try {
      str = JSON.stringify(data) || "";
    } catch (e) {
      str = "";
    }
    var h = 5381;
    for (var i = 0; i < str.length; i++) {
      h = ((h << 5) + h + str.charCodeAt(i)) | 0;
    }
    return str.length + ":" + (h >>> 0).toString(36);
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
          return { ok: false };
        });
      });
  }

  function nowIso() {
    return new Date().toISOString();
  }

  function syncStore(store, meta) {
    var local = readLocal(store);
    var localFp = local ? fingerprint(local) : null;
    var seen = meta[store] || {};
    var localChanged = localFp !== (seen.fp || null);
    return api("/api/user/sync?store=" + encodeURIComponent(store)).then(function (r) {
      if (!r || !r.ok) return;
      var entry = r.entry || null;
      var serverTs = entry ? entry.updated_at || "" : "";
      var localTs = seen.ts || "";
      if (entry && entry.data && serverTs > localTs) {
        // Server is newer: adopt it wholesale.
        writeLocal(store, entry.data);
        meta[store] = { ts: serverTs, fp: fingerprint(entry.data) };
        return;
      }
      if (local && (localChanged || localTs > serverTs)) {
        var ts = localChanged ? nowIso() : localTs;
        return api("/api/user/sync", {
          method: "PUT",
          body: { store: store, data: local, updated_at: ts },
        }).then(function (pr) {
          if (pr && pr.ok && !pr.conflict) {
            meta[store] = { ts: pr.updated_at || ts, fp: localFp };
          } else if (pr && pr.ok && pr.conflict && pr.entry) {
            writeLocal(store, pr.entry.data);
            meta[store] = { ts: pr.entry.updated_at || "", fp: fingerprint(pr.entry.data) };
          }
        });
      }
      if (!seen.ts && serverTs) meta[store] = { ts: serverTs, fp: seen.fp || null };
    });
  }

  function syncNow() {
    if (syncing) return Promise.resolve(false);
    if (!global.ILAccount || !global.ILAccount.me) return Promise.resolve(false);
    syncing = true;
    return global.ILAccount.me()
      .then(function (email) {
        if (!email) return false;
        var meta = readMeta();
        var chain = Promise.resolve();
        Object.keys(STORES).forEach(function (store) {
          chain = chain.then(function () {
            return syncStore(store, meta).catch(function () {});
          });
        });
        return chain.then(function () {
          writeMeta(meta);
          return true;
        });
      })
      .catch(function () {
        return false;
      })
      .then(function (done) {
        syncing = false;
        return done;
      });
  }

  function boot() {
    syncNow();
    global.setInterval(syncNow, TICK_MS);
    document.addEventListener("visibilitychange", function () {
      if (document.visibilityState === "hidden") syncNow();
    });
    document.addEventListener("il:signedin", function () {
      syncNow();
    });
  }

  global.ILSync = { syncNow: syncNow, stores: STORES };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})(typeof window !== "undefined" ? window : this);
