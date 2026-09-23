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
    var cx = size / 2, cy = size / 2, scale = size * 0.36;
    var cos = Math.cos(yaw), sin = Math.sin(yaw);
    function proj(x, y, z) {
      var x1 = x * cos - z * sin;
      var z1 = x * sin + z * cos;
      var f = 3.2 / (3.2 + z1);
      return [cx + x1 * f * scale, cy - y * f * scale];
    }
    ctx.beginPath();
    for (var i = 0; i <= 96; i++) {
      var a = (i / 96) * Math.PI * 2;
      var q = proj(Math.cos(a) * 1.15, Math.sin(a) * 1.15, 0);
      if (i === 0) ctx.moveTo(q[0], q[1]);
      else ctx.lineTo(q[0], q[1]);
    }
    ctx.strokeStyle = "#f4f1ea";
    ctx.lineWidth = 1.6;
    ctx.stroke();
    var nodes = [[0, 1.15], [1.15, 0], [0, -1.15], [-1.15, 0]];
    for (var n = 0; n < nodes.length; n++) {
      var qn = proj(nodes[n][0], nodes[n][1], 0);
      ctx.beginPath();
      ctx.arc(qn[0], qn[1], 2.3, 0, Math.PI * 2);
      ctx.fillStyle = "#f4f1ea";
      ctx.fill();
    }
    var tri = [[0, 0.74, 0.02], [0.62, -0.4, 0.02], [-0.62, -0.4, 0.02]];
    ctx.beginPath();
    for (var t = 0; t < tri.length; t++) {
      var qt = proj(tri[t][0], tri[t][1], tri[t][2]);
      if (t === 0) ctx.moveTo(qt[0], qt[1]);
      else ctx.lineTo(qt[0], qt[1]);
    }
    ctx.closePath();
    ctx.strokeStyle = "#c6a36a";
    ctx.lineWidth = 1.4;
    ctx.stroke();
    function quad(x, y, w0, h) {
      var pts = [[x, y, 0.06], [x + w0, y, 0.06], [x + w0, y - h, 0.06], [x, y - h, 0.06]];
      ctx.beginPath();
      for (var i = 0; i < pts.length; i++) {
        var q = proj(pts[i][0], pts[i][1], pts[i][2]);
        if (i === 0) ctx.moveTo(q[0], q[1]);
        else ctx.lineTo(q[0], q[1]);
      }
      ctx.closePath();
      var shade = 0.72 + 0.28 * Math.abs(cos);
      ctx.fillStyle = "rgb(" + Math.round(198 * shade) + "," + Math.round(163 * shade) + "," + Math.round(106 * shade) + ")";
      ctx.fill();
    }
    quad(-0.42, 0.48, 0.16, 0.92);
    quad(0.08, 0.48, 0.16, 0.68);
    quad(0.08, -0.2, 0.46, 0.16);
    function orbit(tilt, radius) {
      ctx.beginPath();
      for (var i = 0; i <= 80; i++) {
        var a = (i / 80) * Math.PI * 2 + yaw * 1.4;
        var x = Math.cos(a) * radius;
        var y = Math.sin(a) * radius * 0.36;
        var q = proj(x, y * Math.cos(tilt), y * Math.sin(tilt));
        if (i === 0) ctx.moveTo(q[0], q[1]);
        else ctx.lineTo(q[0], q[1]);
      }
      ctx.strokeStyle = "#7ed4e0";
      ctx.lineWidth = 1.25;
      ctx.stroke();
    }
    orbit(0.9, 0.84);
    orbit(1.7, 0.74);
    orbit(2.45, 0.64);
    var c = proj(0, 0, 0.18);
    ctx.beginPath();
    ctx.arc(c[0], c[1], 4.6, 0, Math.PI * 2);
    ctx.fillStyle = "#c6a36a";
    ctx.fill();
    ctx.beginPath();
    ctx.arc(c[0], c[1], 1.8, 0, Math.PI * 2);
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

  function mountHero(node) {
    if (node.getAttribute("data-il-mark") === "1") return;
    node.setAttribute("data-il-mark", "1");
    while (node.firstChild) node.removeChild(node.firstChild);
    var canvas = d.createElement("canvas");
    canvas.className = "il-spin-mark il-spin-mark--hero";
    canvas.setAttribute("aria-label", "Interstitium Labs");
    canvas.setAttribute("role", "img");
    canvas.width = 160;
    canvas.height = 160;
    node.appendChild(canvas);
    hosts.push(canvas);
  }

  function scan() {
    var pictures = d.querySelectorAll("picture.il-lockup");
    var headerMark = null;
    for (var i = 0; i < pictures.length; i++) {
      var picture = pictures[i];
      if (!headerMark && picture.closest && picture.closest("header")) headerMark = picture;
      else picture.remove();
    }
    if (headerMark) mount(headerMark);
    var heroes = d.querySelectorAll(".il-hero-sigil");
    for (var h = 0; h < heroes.length; h++) mountHero(heroes[h]);
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
