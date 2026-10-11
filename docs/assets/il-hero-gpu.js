/* RTX 3080 on the Legion: 2560x1440, the WQXGA panel width.
   Quadro P1000: skip 5K HEVC. Wide screens keep the 5K H.264 file,
   because the dual Xeon can decode it. Smaller screens get 1080p Level 4.0. */
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
  var wide = Math.max(screen.width || 0, window.innerWidth || 0) >= 2400;
  var src = "";
  if (/rtx|geforce/.test(name)) src = "/assets/chrome/hero-rtx.mp4";
  else if (/p1000|quadro/.test(name)) src = wide ? "/assets/chrome/hero-5k.mp4" : "/assets/chrome/hero-p1000.mp4";
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
