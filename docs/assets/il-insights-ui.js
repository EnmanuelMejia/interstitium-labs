document.addEventListener("DOMContentLoaded", function () {
  function paint() {
    if (window.ILIterate) {
      ILIterate.run();
      ILIterate.render(document.getElementById("il-insights-root"));
    }
    var raw = document.getElementById("il-insights-raw");
    if (raw && window.ILAnalytics) {
      var buf = ILAnalytics.getBuffer().slice(-25).reverse();
      raw.textContent = buf.length ? JSON.stringify(buf, null, 2) : "(empty — browse the site on this device)";
    }
  }
  setTimeout(paint, 50);
  var r = document.getElementById("il-insights-refresh");
  if (r) r.addEventListener("click", paint);
  var c = document.getElementById("il-insights-clear");
  if (c) c.addEventListener("click", function () {
    if (!confirm("Clear local analytics buffer on this browser?")) return;
    if (window.ILAnalytics) ILAnalytics.clearBuffer();
    paint();
  });
});
