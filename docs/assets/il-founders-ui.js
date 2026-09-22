document.addEventListener("DOMContentLoaded", function () {
  var btn = document.getElementById("il-reset-founders");
  if (btn && window.ILProgress) {
    btn.addEventListener("click", function () {
      if (!confirm("Clear founders weekly checklist + streak on this browser?")) return;
      ILProgress.clearScope("founders");
      location.reload();
    });
  }
});
