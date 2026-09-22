/**
 * SuperLab hub helpers — informational XP claim for "Clone SuperLab".
 * Depends on window.ILGame when present.
 */
(function (global) {
  "use strict";
  function ready(fn) {
    if (global.document.readyState === "loading") {
      global.document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }
  ready(function () {
    var btn = global.document.getElementById("il-superlab-claim");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var G = global.ILGame;
      if (!G || typeof G.award !== "function") {
        btn.textContent = "ILGame not loaded";
        return;
      }
      var r = G.award("quest_claim", 40, {
        id: "clone_superlab",
        once: true,
        flag: "superlab_clone",
        label: "Clone SuperLab",
      });
      if (r && r.gained === 0) {
        btn.textContent = "Already claimed";
        btn.disabled = true;
      } else {
        btn.textContent = "Claimed · +" + ((r && r.gained) || 40) + " XP";
        btn.disabled = true;
      }
    });
  });
})(typeof window !== "undefined" ? window : this);
