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
    var scale = size * 0.36;
    var cos = Math.cos(yaw);
    var sin = Math.sin(yaw);
    function proj(x, y, z) {
      var x1 = x * cos - z * sin;
      var z1 = x * sin + z * cos;
      var f = 3.4 / (3.4 + z1);
      return [cx + x1 * f * scale, cy - y * f * scale, z1];
    }
    function viewN(nx, ny, nz) {
      var nx1 = nx * cos - nz * sin;
      var nz1 = nx * sin + nz * cos;
      var d = nx1 * 0.42 + ny * 0.78 + nz1 * 0.46;
      return { facing: nz1, shade: Math.max(0.16, Math.min(1, 0.3 + d)) };
    }
    var faces = [];
    function pushFace(pts, nx, ny, nz, gold) {
      var lit = viewN(nx, ny, nz);
      if (lit.facing < -0.02) return;
      var z = 0;
      var xy = [];
      for (var i = 0; i < pts.length; i++) {
        var q = proj(pts[i][0], pts[i][1], pts[i][2]);
        xy.push(q);
        z += q[2];
      }
      var sh = lit.shade;
      var color = gold
        ? "rgb(" + Math.round(72 + sh * 150) + "," + Math.round(48 + sh * 112) + "," + Math.round(18 + sh * 62) + ")"
        : "rgb(" + Math.round(150 + sh * 90) + "," + Math.round(146 + sh * 88) + "," + Math.round(136 + sh * 80) + ")";
      faces.push({ z: z / pts.length, xy: xy, color: color });
    }
    function box(x, y, z, w0, h, d) {
      var x0 = x, x1 = x + w0, y0 = y - h, y1 = y, z0 = z, z1 = z + d;
      pushFace([[x0,y1,z1],[x1,y1,z1],[x1,y0,z1],[x0,y0,z1]], 0, 0, 1, true);
      pushFace([[x1,y1,z0],[x0,y1,z0],[x0,y0,z0],[x1,y0,z0]], 0, 0, -1, true);
      pushFace([[x1,y1,z1],[x1,y1,z0],[x1,y0,z0],[x1,y0,z1]], 1, 0, 0, true);
      pushFace([[x0,y1,z0],[x0,y1,z1],[x0,y0,z1],[x0,y0,z0]], -1, 0, 0, true);
      pushFace([[x0,y1,z0],[x1,y1,z0],[x1,y1,z1],[x0,y1,z1]], 0, 1, 0, true);
      pushFace([[x0,y0,z1],[x1,y0,z1],[x1,y0,z0],[x0,y0,z0]], 0, -1, 0, true);
    }
    for (var i = 0; i < 48; i++) {
      var a0 = (i / 48) * Math.PI * 2;
      var a1 = ((i + 1) / 48) * Math.PI * 2;
      var nx = Math.cos((a0 + a1) / 2);
      var ny = Math.sin((a0 + a1) / 2);
      var outer = 1.2, inner = 1.06;
      pushFace([
        [Math.cos(a0) * outer, Math.sin(a0) * outer, 0.03],
        [Math.cos(a1) * outer, Math.sin(a1) * outer, 0.03],
        [Math.cos(a1) * inner, Math.sin(a1) * inner, -0.03],
        [Math.cos(a0) * inner, Math.sin(a0) * inner, -0.03]
      ], nx, ny, 0.15, false);
    }
    box(-0.46, 0.52, 0.02, 0.2, 1.02, 0.16);
    box(0.08, 0.58, 0.04, 0.18, 0.78, 0.16);
    box(0.08, -0.18, 0.04, 0.52, 0.18, 0.16);
    faces.sort(function (a, b) { return a.z - b.z; });
    for (var f = 0; f < faces.length; f++) {
      var face = faces[f];
      ctx.beginPath();
      for (var k = 0; k < face.xy.length; k++) {
        if (k === 0) ctx.moveTo(face.xy[k][0], face.xy[k][1]);
        else ctx.lineTo(face.xy[k][0], face.xy[k][1]);
      }
      ctx.closePath();
      ctx.fillStyle = face.color;
      ctx.fill();
    }
    var nodes = [[0, 1.13], [1.13, 0], [0, -1.13], [-1.13, 0]];
    for (var n = 0; n < nodes.length; n++) {
      var q = proj(nodes[n][0], nodes[n][1], 0);
      ctx.beginPath();
      ctx.arc(q[0], q[1], 2.6, 0, Math.PI * 2);
      ctx.fillStyle = "#f4f1ea";
      ctx.fill();
    }
    function orbit(tilt, radius) {
      var pts = [];
      for (var i = 0; i <= 72; i++) {
        var a = (i / 72) * Math.PI * 2 + yaw * 1.7;
        var x = Math.cos(a) * radius;
        var y = Math.sin(a) * radius * 0.38;
        var q = proj(x, y * Math.cos(tilt), y * Math.sin(tilt));
        pts.push(q);
      }
      function stroke(dx, color) {
        ctx.beginPath();
        for (var i = 0; i < pts.length; i++) {
          if (i === 0) ctx.moveTo(pts[i][0] + dx, pts[i][1]);
          else ctx.lineTo(pts[i][0] + dx, pts[i][1]);
        }
        ctx.strokeStyle = color;
        ctx.lineWidth = 1.35;
        ctx.stroke();
      }
      stroke(0.8, "rgba(180,40,55,0.45)");
      stroke(-0.8, "rgba(40,90,220,0.4)");
      stroke(0, "#7ed4e0");
    }
    orbit(0.85, 0.86);
    orbit(1.65, 0.76);
    orbit(2.35, 0.66);
    var c = proj(0, 0, 0.28);
    var glow = ctx.createRadialGradient(c[0] - 1.5, c[1] - 1.5, 0.4, c[0], c[1], 6.5);
    glow.addColorStop(0, "#fff6df");
    glow.addColorStop(0.45, "#c6a36a");
    glow.addColorStop(1, "#6a4e28");
    ctx.beginPath();
    ctx.arc(c[0], c[1], 5.4, 0, Math.PI * 2);
    ctx.fillStyle = glow;
    ctx.fill();
    ctx.beginPath();
    ctx.arc(c[0], c[1], 2.1, 0, Math.PI * 2);
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
