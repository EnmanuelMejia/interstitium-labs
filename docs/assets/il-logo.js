/**
 * One spinning mark for every lockup.
 * Canvas only. No innerHTML. No remote script. Pauses when the tab is hidden.
 */
(function (w, d) {
  "use strict";
  if (w.__IL_LOGO__) return;
  w.__IL_LOGO__ = true;

  var hosts = [];
  var frame = 0;
  var reduced = false;
  try {
    reduced = w.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch (e) {
    reduced = false;
  }

  function draw(canvas, yaw) {
    var ctx = canvas.getContext("2d");
    if (!ctx) return;
    var dpr = Math.min(2, w.devicePixelRatio || 1);
    var size = 160;
    if (canvas.width !== size * dpr) {
      canvas.width = size * dpr;
      canvas.height = size * dpr;
    }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, size, size);
    var cx = size / 2;
    var cy = size / 2;
    var s = size * 0.36;
    function proj(x, y, z) {
      var x1 = x * Math.cos(yaw) - z * Math.sin(yaw);
      var z1 = x * Math.sin(yaw) + z * Math.cos(yaw);
      var f = 3.2 / (3.2 + z1);
      return [cx + x1 * f * s, cy - y * f * s];
    }
    ctx.beginPath();
    var i;
    for (i = 0; i <= 80; i++) {
      var a = (i / 80) * Math.PI * 2;
      var q = proj(Math.cos(a) * 1.15, Math.sin(a) * 1.15, 0);
      if (i === 0) ctx.moveTo(q[0], q[1]);
      else ctx.lineTo(q[0], q[1]);
    }
    ctx.strokeStyle = "#eceae4";
    ctx.lineWidth = 1.7;
    ctx.stroke();
    var nodes = [[0, 1.15], [1.15, 0], [0, -1.15], [-1.15, 0]];
    for (i = 0; i < nodes.length; i++) {
      var nq = proj(nodes[i][0], nodes[i][1], 0);
      ctx.beginPath();
      ctx.arc(nq[0], nq[1], 2.4, 0, Math.PI * 2);
      ctx.fillStyle = "#eceae4";
      ctx.fill();
    }
    var tri = [[0, 0.74, 0.04], [0.62, -0.4, 0.04], [-0.62, -0.4, 0.04]];
    ctx.beginPath();
    for (i = 0; i < tri.length; i++) {
      var tq = proj(tri[i][0], tri[i][1], tri[i][2]);
      if (i === 0) ctx.moveTo(tq[0], tq[1]);
      else ctx.lineTo(tq[0], tq[1]);
    }
    ctx.closePath();
    ctx.strokeStyle = "#c6a36a";
    ctx.lineWidth = 1.5;
    ctx.stroke();
    function quad(x, y, wdt, h) {
      var pts = [[x, y, 0.1], [x + wdt, y, 0.1], [x + wdt, y - h, 0.1], [x, y - h, 0.1]];
      ctx.beginPath();
      for (var k = 0; k < pts.length; k++) {
        var pq = proj(pts[k][0], pts[k][1], pts[k][2]);
        if (k === 0) ctx.moveTo(pq[0], pq[1]);
        else ctx.lineTo(pq[0], pq[1]);
      }
      ctx.closePath();
      ctx.fillStyle = "#c6a36a";
      ctx.fill();
    }
    quad(-0.44, 0.5, 0.18, 0.96);
    quad(0.06, 0.5, 0.18, 0.72);
    quad(0.06, -0.22, 0.5, 0.18);
    function orbit(tilt, radius) {
      ctx.beginPath();
      for (var j = 0; j <= 72; j++) {
        var ang = (j / 72) * Math.PI * 2 + yaw * 1.7;
        var x = Math.cos(ang) * radius;
        var y = Math.sin(ang) * radius * 0.38;
        var y1 = y * Math.cos(tilt);
        var z1 = y * Math.sin(tilt);
        var oq = proj(x, y1, z1);
        if (j === 0) ctx.moveTo(oq[0], oq[1]);
        else ctx.lineTo(oq[0], oq[1]);
      }
      ctx.strokeStyle = "#3c9fbe";
      ctx.lineWidth = 1.35;
      ctx.stroke();
    }
    orbit(0.85, 0.86);
    orbit(1.65, 0.76);
    orbit(2.35, 0.66);
    var nucleus = proj(0, 0, 0.22);
    ctx.beginPath();
    ctx.arc(nucleus[0], nucleus[1], 5.2, 0, Math.PI * 2);
    ctx.fillStyle = "#c6a36a";
    ctx.fill();
    ctx.beginPath();
    ctx.arc(nucleus[0], nucleus[1], 2.2, 0, Math.PI * 2);
    ctx.fillStyle = "#102028";
    ctx.fill();
  }

  function mount(picture) {
    if (picture.getAttribute("data-il-mark") === "1") return;
    picture.setAttribute("data-il-mark", "1");
    var link = picture.closest ? picture.closest("a") : null;
    if (link && !link.getAttribute("aria-label")) link.setAttribute("aria-label", "Interstitium Labs");
    var canvas = d.createElement("canvas");
    canvas.className = "il-spin-mark";
    canvas.setAttribute("aria-hidden", "true");
    canvas.width = 160;
    canvas.height = 160;
    var word = d.createElement("span");
    word.className = "il-word";
    word.textContent = "Interstitium";
    var labs = d.createElement("span");
    labs.className = "il-labs";
    labs.textContent = "LABS";
    var row = d.createElement("span");
    row.className = "il-lockup-row";
    row.appendChild(canvas);
    row.appendChild(word);
    row.appendChild(labs);
    picture.replaceWith(row);
    hosts.push(canvas);
  }

  function paint(t) {
    var yaw = reduced ? 0.55 : t * 0.00045;
    for (var i = 0; i < hosts.length; i++) draw(hosts[i], yaw);
    if (!reduced && d.visibilityState === "visible") frame = w.requestAnimationFrame(paint);
  }

  function scan() {
    var nodes = d.querySelectorAll(".il-lockup");
    for (var i = 0; i < nodes.length; i++) mount(nodes[i]);
    if (!hosts.length) return;
    if (reduced) paint(0);
    else if (!frame) frame = w.requestAnimationFrame(paint);
  }

  function start() {
    scan();
    d.addEventListener("visibilitychange", function () {
      if (d.visibilityState === "visible" && !reduced) frame = w.requestAnimationFrame(paint);
    });
  }

  if (d.readyState === "loading") d.addEventListener("DOMContentLoaded", start);
  else start();
})(window, document);
