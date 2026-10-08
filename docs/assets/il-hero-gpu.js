/* Pick a hero master the GPU can actually decode well.
   RTX 30-series (Legion 7, WQXGA): 2560x1440 from the 5K mezzanine.
   Quadro P1000 (Pascal, 4 GB): 1080p H.264, Level 4.0. No AV1, no 5K HDR. */
(function () {
  var video = document.querySelector(".il-hero__video");
  if (!video || video.getAttribute("data-il-gpu")) return;
  var renderer = "";
  try {
    var canvas = document.createElement("canvas");
    var gl = canvas.getContext("webgl");
    if (gl) {
      var info = gl.getExtension("WEBGL_debug_renderer_info");
      if (info) renderer = String(gl.getParameter(info.UNMASKED_RENDERER_WEBGL) || "");
      var lose = gl.getExtension("WEBGL_lose_context");
      if (lose) lose.loseContext();
    }
  } catch (err) {
    return;
  }
  var name = renderer.toLowerCase();
  var src = "";
  if (/rtx|geforce/.test(name)) src = "/assets/chrome/hero-rtx.mp4";
  else if (/p1000|quadro/.test(name)) src = "/assets/chrome/hero-p1000.mp4";
  if (!src) return;
  var nodes = video.querySelectorAll("source");
  for (var i = 0; i < nodes.length; i++) nodes[i].remove();
  var source = document.createElement("source");
  source.src = src;
  source.type = "video/mp4";
  video.insertBefore(source, video.firstChild);
  video.setAttribute("data-il-gpu", src);
  video.load();
})();
