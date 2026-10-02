/* Original spatial neural scene. Native WebGL; no CDN, trackers, or synthetic activity. */
(function (g) {
  'use strict';
  var canvas = document.getElementById('noah-neural'), button = document.getElementById('motion-toggle');
  if (!canvas || !button) return;
  var media = g.matchMedia('(prefers-reduced-motion: reduce)'), reduced = media.matches;
  var paused = reduced, inView = true, frame = 0, elapsed = 0, previous = 0, state = 'idle', graph = null, gl = null, program = null, points = null, lines = null;
  var vertex = 'precision mediump float;attribute vec3 position;uniform float angle;uniform float aspect;uniform float pulse;uniform float dpr;varying float depth;void main(){float c=cos(angle),s=sin(angle);vec3 p=vec3(position.x*c+position.z*s,position.y,-position.x*s+position.z*c);float tilt=.16;p=vec3(p.x,p.y*cos(tilt)-p.z*sin(tilt),p.y*sin(tilt)+p.z*cos(tilt));float z=3.8-p.z;depth=1.0/z;gl_Position=vec4(p.x*2.15/aspect,p.y*2.15,0.1,z);gl_PointSize=(4.0+pulse*2.0)*dpr*(3.0/z);}';
  var fragment = 'precision mediump float;uniform vec3 color;uniform float dots;uniform float pulse;varying float depth;void main(){float a=1.0;if(dots>0.5){float r=length(gl_PointCoord-vec2(.5));if(r>.5)discard;a=1.0-smoothstep(.15,.5,r);}gl_FragColor=vec4(color*(.55+depth*1.7+pulse*.2),a*(dots>.5?.95:.28));}';
  function compile(type, source) { var shader = gl.createShader(type); gl.shaderSource(shader, source); gl.compileShader(shader); if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) throw Error('shader'); return shader; }
  function init() {
    try {
      gl = canvas.getContext('webgl', { alpha: true, antialias: true, powerPreference: 'low-power' }); if (!gl) throw Error('webgl');
      program = gl.createProgram(); gl.attachShader(program, compile(gl.VERTEX_SHADER, vertex)); gl.attachShader(program, compile(gl.FRAGMENT_SHADER, fragment)); gl.linkProgram(program);
      if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw Error('program');
      points = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, points); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(graph.nodes.flat()), gl.STATIC_DRAW);
      lines = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, lines); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(graph.edges.flatMap(function (e) { return graph.nodes[e[0]].concat(graph.nodes[e[1]]); })), gl.STATIC_DRAW);
      canvas.parentElement.dataset.rendered = 'true'; draw(); kick();
    } catch (_) { canvas.parentElement.dataset.rendered = 'false'; button.disabled = true; button.textContent = 'Static visual'; }
  }
  function draw() {
    if (!gl || gl.isContextLost()) return;
    var rect = canvas.getBoundingClientRect(), dpr = Math.min(g.devicePixelRatio || 1, 1.5), w = Math.round(rect.width*dpr), h = Math.round(rect.height*dpr);
    if (!w || !h) return;
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
    gl.viewport(0,0,w,h); gl.clearColor(0,0,0,0); gl.clear(gl.COLOR_BUFFER_BIT); gl.useProgram(program); gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA,gl.ONE);
    var pulse = state === 'executing' || state === 'researching' ? .65 + .25*Math.sin(elapsed*4) : state === 'approval' ? .25 : .1;
    gl.uniform1f(gl.getUniformLocation(program,'angle'),elapsed*Math.PI/10); gl.uniform1f(gl.getUniformLocation(program,'aspect'),w/h); gl.uniform1f(gl.getUniformLocation(program,'pulse'),pulse); gl.uniform1f(gl.getUniformLocation(program,'dpr'),dpr);
    var color = state === 'error' ? [1,.38,.2] : state === 'approval' ? [.84,.69,.38] : [.25,.68,1];
    gl.uniform3fv(gl.getUniformLocation(program,'color'),color);
    var position = gl.getAttribLocation(program,'position'); gl.enableVertexAttribArray(position);
    gl.bindBuffer(gl.ARRAY_BUFFER,lines); gl.vertexAttribPointer(position,3,gl.FLOAT,false,0,0); gl.uniform1f(gl.getUniformLocation(program,'dots'),0); gl.drawArrays(gl.LINES,0,graph.edges.length*2);
    gl.bindBuffer(gl.ARRAY_BUFFER,points); gl.vertexAttribPointer(position,3,gl.FLOAT,false,0,0); gl.uniform1f(gl.getUniformLocation(program,'dots'),1); gl.drawArrays(gl.POINTS,0,graph.nodes.length);
  }
  function tick(now) { frame=0; if (paused || reduced || document.hidden || !inView) { previous=0; return; } if (previous) elapsed=(elapsed+Math.min((now-previous)/1000,.05))%20; previous=now; draw(); kick(); }
  function kick() { if (!frame && !paused && !reduced && !document.hidden && inView && gl && !gl.isContextLost()) frame=g.requestAnimationFrame(tick); }
  function stop() { g.cancelAnimationFrame(frame); frame=0; previous=0; }
  function label() { button.setAttribute('aria-pressed',String(paused || reduced)); button.textContent=paused || reduced ? 'Resume motion' : 'Pause motion'; }
  button.addEventListener('click',function () { if (reduced) { reduced=false; paused=false; } else paused=!paused; label(); if (paused) stop(); else kick(); });
  media.addEventListener('change',function (event) { reduced=event.matches; paused=reduced; label(); if (reduced) { stop(); draw(); } else kick(); });
  document.addEventListener('visibilitychange',function () { if (document.hidden) stop(); else kick(); });
  if ('IntersectionObserver' in g) new IntersectionObserver(function (entries) { inView=entries[0].isIntersecting; if (inView) kick(); else stop(); }).observe(canvas);
  g.addEventListener('resize',draw); g.addEventListener('noah:activity',function (event) { state=event.detail && event.detail.state || 'idle'; draw(); kick(); });
  canvas.addEventListener('webglcontextlost',function (event) { event.preventDefault(); stop(); canvas.parentElement.dataset.rendered='false'; });
  canvas.addEventListener('webglcontextrestored',init);
  label();
  fetch('/assets/noah/noah-neural.json',{credentials:'omit'}).then(function (r) { if(!r.ok) throw Error('geometry'); return r.json(); }).then(function (data) {
    if (!data || !Array.isArray(data.nodes) || !Array.isArray(data.edges) || data.nodes.length>160 || data.edges.length>600 || !data.nodes.every(function (n) { return Array.isArray(n) && n.length===3 && n.every(function (v) { return Number.isFinite(v) && Math.abs(v)<10; }); }) || !data.edges.every(function (e) { return Array.isArray(e) && e.length===2 && e.every(function (v) { return Number.isInteger(v) && v>=0 && v<data.nodes.length; }); })) throw Error('geometry');
    graph=data; init();
  }).catch(function () { button.disabled=true; button.textContent='Static visual'; });
})(window);
