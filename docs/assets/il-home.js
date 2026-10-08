/* Editorial homepage. External so the page CSP can stay script-src 'self'. */
(function () {
  try {
    var y = document.getElementById("il-year");
    if (y) y.textContent = String(new Date().getFullYear());
    document.querySelectorAll(".il-menu__sheet a").forEach(function (a) {
      a.addEventListener("click", function () {
        var d = a.closest("details");
        if (d) d.removeAttribute("open");
      });
    });
  } catch (e) {}
})();
