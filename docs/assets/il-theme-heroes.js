/* il-theme-heroes.js — generative canvas hero engine for the 8 category themes.
   API: ILThemeHeroes.mount(canvasEl, themeId, opts) / ILThemeHeroes.unmount(canvasEl).
   - One rAF loop per mounted canvas, IntersectionObserver pauses offscreen canvases.
   - Auto devicePixelRatio scaling, resize handling, particle counts scale down on mobile.
   - prefers-reduced-motion renders a single static frame.
   - All visuals are original generative vector animation (no assets, no fonts beyond the
     system monospace stack, no copyrighted material — Mr. Robot / Tron are style homages only).
   ES5 style (var, function), no modules. Attaches to window.ILThemeHeroes. */
(function(){
'use strict';

var TAU = Math.PI * 2;
var MONO = '"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace';

/* ---------- deterministic utils ---------- */
function mulberry(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
function hashStr(s){var h=2166136261;for(var i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619);}return h>>>0;}
function clamp(v,a,b){return v<a?a:(v>b?b:v);}
function lerp(a,b,k){return a+(b-a)*k;}
function smooth(k){k=clamp(k,0,1);return k*k*(3-2*k);}
function easeIO(k){k=clamp(k,0,1);return k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;}
function pick(r,arr){return arr[Math.floor(r()*arr.length)];}

/* ---------- shared draw helpers ---------- */
function bg(S,c){var x=S.ctx;x.fillStyle=c;x.fillRect(0,0,S.w,S.h);}
function txt(S,str,x,y,color,size,align,alpha){
  var c=S.ctx;c.save();
  c.globalAlpha=(alpha==null?1:alpha);
  c.font=size+'px '+MONO;
  c.textAlign=align||'left';c.textBaseline='alphabetic';
  c.fillStyle=color;c.fillText(str,x,y);
  c.restore();
}
function vig(S,a){
  var c=S.ctx,w=S.w,h=S.h;
  var g=c.createRadialGradient(w/2,h/2,Math.min(w,h)*0.32,w/2,h/2,Math.max(w,h)*0.72);
  g.addColorStop(0,'rgba(0,0,0,0)');
  g.addColorStop(1,'rgba(0,0,0,'+a+')');
  c.fillStyle=g;c.fillRect(0,0,w,h);
}
function scan(S,step,a){
  var c=S.ctx;c.fillStyle='rgba(0,0,0,'+a+')';
  for(var y=0;y<S.h;y+=step){c.fillRect(0,y,S.w,1);}
}
function glowLine(S,x1,y1,x2,y2,color,wdt,alpha){
  var c=S.ctx;c.save();
  c.globalAlpha=alpha==null?1:alpha;
  c.strokeStyle=color;c.lineWidth=wdt*2.6;c.lineCap='round';c.globalAlpha=(alpha==null?1:alpha)*0.25;
  c.beginPath();c.moveTo(x1,y1);c.lineTo(x2,y2);c.stroke();
  c.globalAlpha=(alpha==null?1:alpha);
  c.lineWidth=wdt;
  c.beginPath();c.moveTo(x1,y1);c.lineTo(x2,y2);c.stroke();
  c.restore();
}
function dot(S,x,y,r,color,alpha){
  var c=S.ctx;c.save();c.globalAlpha=alpha==null?1:alpha;
  c.fillStyle=color;c.beginPath();c.arc(x,y,r,0,TAU);c.fill();c.restore();
}
/* expanding ring pulse; local 0..1 progress */
function ring(S,x,y,r0,r1,k,color,wdt,alpha){
  var c=S.ctx;c.save();
  c.globalAlpha=(alpha==null?1:alpha)*(1-k);
  c.strokeStyle=color;c.lineWidth=wdt;
  c.beginPath();c.arc(x,y,lerp(r0,r1,k),0,TAU);c.stroke();
  c.restore();
}

/* ---------- engine core ---------- */
var THEMES = {};
var records = [];

function fit(rec){
  var el=rec.el;
  var w=el.clientWidth||600, h=el.clientHeight||340;
  var dpr=Math.min(window.devicePixelRatio||1,2);
  rec.w=w;rec.h=h;rec.dpr=dpr;
  el.width=Math.round(w*dpr);el.height=Math.round(h*dpr);
  rec.ctx.setTransform(dpr,0,0,dpr,0,0);
  var S=rec.S;
  S.w=w;S.h=h;S.dpr=dpr;
  S.q=(w<768?0.4:1);
}

function reinit(rec){
  fit(rec);
  rec.S.rand=mulberry(hashStr(rec.id));
  rec.S.cols=null;
  if(rec.theme.init)rec.theme.init(rec.S);
  if(rec.reduced){draw(rec,rec.theme.period*0.32);}
}

function draw(rec,t){
  var S=rec.S,P=rec.theme.period;
  var p=(((t%P)+P)%P)/P;
  S.t=t;S.p=p;
  rec.theme.frame(S);
}

function tick(now,rec){
  if(!rec.live)return;
  draw(rec,(now-rec.t0)/1000);
  if(rec.reduced){rec.live=false;return;}
  rec.raf=requestAnimationFrame(function(n){tick(n,rec);});
}

function play(rec){
  if(rec.live||!rec.inview)return;
  rec.live=true;
  var off=rec.reduced?rec.theme.period*0.32:0;
  rec.t0=performance.now()-off*1000;
  rec.raf=requestAnimationFrame(function(n){tick(n,rec);});
}

function stop(rec){
  rec.live=false;
  if(rec.raf){cancelAnimationFrame(rec.raf);rec.raf=0;}
}

function mount(el,themeId,opts){
  if(!el||!el.getContext)return null;
  var theme=THEMES[themeId];
  if(!theme)return null;
  unmount(el);
  opts=opts||{};
  var ctx=el.getContext('2d');
  var rec={
    el:el,ctx:ctx,theme:theme,id:themeId,opts:opts,
    w:0,h:0,dpr:1,raf:0,live:false,inview:true,t0:0,
    reduced:(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches)||!!opts.reduced,
    S:{ctx:ctx,w:0,h:0,dpr:1,rand:mulberry(hashStr(themeId)),q:1,t:0,p:0,period:theme.period},
    io:null,ro:null
  };
  fit(rec);
  if(theme.init)theme.init(rec.S);
  el.__ilHero=rec;
  records.push(rec);
  if('IntersectionObserver' in window){
    rec.io=new IntersectionObserver(function(es){
      for(var i=0;i<es.length;i++){
        if(es[i].target!==el)continue;
        rec.inview=!!es[i].isIntersecting;
        if(rec.inview)play(rec);else stop(rec);
      }
    },{threshold:0.04,rootMargin:'60px'});
    rec.io.observe(el);
  }
  if('ResizeObserver' in window){
    rec.ro=new ResizeObserver(function(){reinit(rec);});
    rec.ro.observe(el);
  }
  play(rec);
  return rec;
}

function unmount(el){
  if(!el||!el.__ilHero)return;
  var rec=el.__ilHero;
  stop(rec);
  if(rec.io)rec.io.disconnect();
  if(rec.ro)rec.ro.disconnect();
  for(var i=0;i<records.length;i++){
    if(records[i]===rec){records.splice(i,1);break;}
  }
  try{delete el.__ilHero;}catch(e){el.__ilHero=null;}
}

document.addEventListener('visibilitychange',function(){
  if(document.hidden){
    for(var i=0;i<records.length;i++)stop(records[i]);
  }else{
    for(var j=0;j<records.length;j++)play(records[j]);
  }
});

/* =====================================================================
   THEME 1 — security: "MR. ROBOT" aesthetic (style homage only).
   Dark gritty terminal: green phosphor code rain, RGB glitch slices,
   CRT scanlines + vignette, looping boot-sequence terminal typing,
   original angular hooded-mask vector silhouette, red accent flashes.
   ===================================================================== */
THEMES['security']={
period:20,
init:function(S){
  var r=mulberry(hashStr('security-cols'));
  var n=Math.max(14,Math.round(S.w/24*S.q));
  var cols=[],i;
  var glyphs='01<>#$%&*+=;:/?!|{}[]abcdef0123456789@';
  for(i=0;i<n;i++){
    cols.push({
      x:(i+0.5)/n*S.w,
      spd:0.25+r()*0.55,          /* loop-fractions of screen height per cycle */
      off:r(),
      len:6+Math.floor(r()*14),
      bright:0.55+r()*0.45
    });
  }
  S.secCols=cols;S.secGlyphs=glyphs;
  /* boot sequence script (original text) */
  S.secLines=[
    '$ veil-init --stealth',
    '> handshake: 4096-bit channel ......... OK',
    '> routing through 7 relays ............ OK',
    '> daemon listening on 127.0.0.1:31337',
    '> packet sniffer armed :: passive mode',
    '> status: UNDETECTED'
  ];
  S.secChars=S.secLines.join('\n').length;
},
frame:function(S){
  var c=S.ctx,w=S.w,h=S.h,p=S.p,t=S.t;
  bg(S,'#040805');

  /* ---- phosphor code rain ---- */
  var rowH=19,rows=Math.ceil(h/rowH)+2,i,j,k;
  var head='#baffc9',body='#39ff6a',dim='#0d5c26';
  c.textBaseline='top';
  for(i=0;i<S.secCols.length;i++){
    var col=S.secCols[i];
    var headRow=((p*col.spd+col.off)%1)*rows;
    var r2=mulberry(hashStr('g'+i));
    for(j=0;j<col.len;j++){
      var rr=headRow-j;
      if(rr<0||rr>=rows)continue;
      var gl=S.secGlyphs[Math.floor(r2()*(j*0.13+p*7+i)%1*S.secGlyphs.length)%S.secGlyphs.length];
      var a=col.bright*(1-j/col.len);
      c.globalAlpha=Math.max(0,a)*(j===0?1:0.85);
      c.font='15px '+MONO;
      c.fillStyle=(j===0?head:(j<col.len*0.4?body:dim));
      c.fillText(gl,col.x,rr*rowH-6);
    }
  }
  c.globalAlpha=1;

  /* dark gradient wash so the mask + terminal read on top */
  var wash=c.createLinearGradient(0,0,0,h);
  wash.addColorStop(0,'rgba(4,8,5,0.25)');
  wash.addColorStop(1,'rgba(4,8,5,0.88)');
  c.fillStyle=wash;c.fillRect(0,0,w,h);

  /* ---- angular hooded-mask silhouette (original vector shape) ---- */
  var cx=w*0.68,cy=h*0.44,s=Math.min(w,h)*0.30;
  var jit=(mulberry(Math.floor(t*24))()-0.5)*1.6;
  var flick=0.55+0.28*Math.sin(t*13.7)+0.17*Math.sin(t*41.3);
  c.save();
  c.translate(cx,cy+jit);
  c.strokeStyle='rgba(57,255,106,'+(0.42+0.30*flick)+')';
  c.lineWidth=2;
  /* hood: angular cowl */
  c.beginPath();
  c.moveTo(0,-s*1.25);
  c.lineTo(s*0.72,-s*0.55);c.lineTo(s*1.05,s*0.35);c.lineTo(s*1.25,s*1.25);
  c.lineTo(-s*1.25,s*1.25);c.lineTo(-s*1.05,s*0.35);c.lineTo(-s*0.72,-s*0.55);
  c.closePath();c.stroke();
  /* mask plate: faceted hexagon */
  c.beginPath();
  c.moveTo(0,-s*0.62);c.lineTo(s*0.52,-s*0.30);c.lineTo(s*0.44,s*0.42);
  c.lineTo(0,s*0.78);c.lineTo(-s*0.44,s*0.42);c.lineTo(-s*0.52,-s*0.30);
  c.closePath();c.stroke();
  /* angular eye slits */
  c.lineWidth=3;
  c.beginPath();
  c.moveTo(-s*0.38,-s*0.10);c.lineTo(-s*0.12,-s*0.16);c.lineTo(-s*0.10,-s*0.02);c.lineTo(-s*0.36,-s*0.02);
  c.closePath();c.stroke();
  c.beginPath();
  c.moveTo(s*0.38,-s*0.10);c.lineTo(s*0.12,-s*0.16);c.lineTo(s*0.10,-s*0.02);c.lineTo(s*0.36,-s*0.02);
  c.closePath();c.stroke();
  /* nose bridge + jaw facets */
  c.lineWidth=1.5;
  c.beginPath();c.moveTo(0,-s*0.02);c.lineTo(0,s*0.30);c.stroke();
  c.beginPath();c.moveTo(-s*0.20,s*0.52);c.lineTo(0,s*0.62);c.lineTo(s*0.20,s*0.52);c.stroke();
  c.restore();
  /* mask under-glow */
  var mg=c.createRadialGradient(cx,cy,0,cx,cy,s*1.6);
  mg.addColorStop(0,'rgba(57,255,106,'+(0.10+0.08*flick)+')');
  mg.addColorStop(1,'rgba(57,255,106,0)');
  c.fillStyle=mg;c.fillRect(cx-s*1.7,cy-s*1.7,s*3.4,s*3.4);

  /* ---- terminal boot sequence (loops inside the cycle) ---- */
  var tw=Math.min(w*0.46,430),th=168,tx=24,ty=h-th-24;
  c.fillStyle='rgba(2,10,5,0.82)';c.fillRect(tx,ty,tw,th);
  c.strokeStyle='rgba(57,255,106,0.35)';c.lineWidth=1;c.strokeRect(tx+0.5,ty+0.5,tw-1,th-1);
  txt(S,'root@veil:~',tx+12,ty+20,'#39ff6a',11,'left',0.9);
  var typeT=p*20; /* seconds into the 20s loop */
  var total=S.secChars,nch;
  if(typeT<11){nch=Math.floor(typeT/11*total);}
  else if(typeT<16.5){nch=total;}
  else{nch=total;} /* hold, then wipe at loop end */
  var wipeA=typeT>17.5?(20-typeT)/2.5:1;
  c.save();c.globalAlpha=Math.max(0,wipeA);
  /* map nch -> (line index, column) */
  var li=0,rem=nch;
  while(li<S.secLines.length&&rem>S.secLines[li].length){rem-=S.secLines[li].length+1;li++;}
  c.font='12px '+MONO;c.textBaseline='alphabetic';
  for(i=0;i<li&&i<S.secLines.length;i++){
    c.fillStyle=(i===0)?'#baffc9':'#39ff6a';
    c.fillText(S.secLines[i],tx+12,ty+42+i*19);
  }
  if(li<S.secLines.length){
    var pline=S.secLines[li].substring(0,Math.max(0,rem));
    var colr2=(li===0)?'#baffc9':(S.secLines[li].indexOf('UNDETECTED')>=0?'#ff3b3b':'#39ff6a');
    c.fillStyle=colr2;
    c.fillText(pline,tx+12,ty+42+li*19);
    if(typeT<11&&(Math.floor(t*2.4)%2===0)){
      c.fillStyle='#baffc9';
      c.fillRect(tx+12+c.measureText(pline).width,ty+42+li*19-12,8,14);
    }
  }
  c.restore();

  /* ---- RGB glitch slices ---- */
  var gT=t%4.7;
  if(gT<0.30){
    var gr=mulberry(Math.floor(t/4.7)*7919+11);
    var slices=3+Math.floor(gr()*3);
    for(k=0;k<slices;k++){
      var sy=gr()*h,sh=6+gr()*26,dx=(gr()-0.5)*70;
      /* self-copy: source rect in raw pixels, dest in CSS px (transform is active) */
      var dpr=S.dpr;
      c.drawImage(c.canvas,0,sy*dpr,c.canvas.width,sh*dpr,dx,sy,w,sh);
      c.save();c.globalAlpha=0.5;
      c.fillStyle=k%2?'rgba(255,59,59,0.16)':'rgba(0,229,255,0.14)';
      c.fillRect(0,sy,w,sh);
      c.restore();
    }
  }

  /* ---- red accent flashes ---- */
  var rT=t%7.3;
  if(rT<0.16){
    c.save();c.globalAlpha=(0.16-rT)/0.16*0.5;
    c.strokeStyle='#ff3b3b';c.lineWidth=6;c.strokeRect(3,3,w-6,h-6);
    c.restore();
    txt(S,'!! INTRUSION COUNTERMEASURE ARMED !!',w/2,30,'#ff3b3b',12,'center',0.9);
  }

  scan(S,4,0.16);
  vig(S,0.62);
  txt(S,'SEC.07 // PHOSPHOR GRID',w-16,h-14,'rgba(57,255,106,0.55)',10,'right',1);
}
};
/* =====================================================================
   THEME 2 — ai: "TRON" aesthetic (style homage only).
   Perspective neon grid floor, light-trail streaks racing along lanes,
   lens-flare horizon glow, rotating wireframe icosahedron.
   ===================================================================== */
THEMES['ai']={
period:16,
init:function(S){
  var r=mulberry(hashStr('ai-trails'));
  var lanes=[],i;
  for(i=0;i<7;i++){
    lanes.push({
      lane:-8+Math.floor(r()*17),   /* which vertical lane */
      spd:0.55+r()*0.5,
      off:r(),
      col:r()<0.62?'#00e5ff':'#ff9a00',
      wdt:1.5+r()*1.5
    });
  }
  S.aiTrails=lanes;
  /* icosahedron verts + edges */
  var t=(1+Math.sqrt(5))/2;
  var v=[[1,t,0],[-1,t,0],[1,-t,0],[-1,-t,0],[0,1,t],[0,1,-t],[0,-1,t],[0,-1,-t],[t,0,1],[-t,0,1],[t,0,-1],[-t,0,-1]];
  var n=v.length,edges=[],a,b2,dx,dy,dz,d;
  for(a=0;a<n;a++)for(b2=a+1;b2<n;b2++){
    dx=v[a][0]-v[b2][0];dy=v[a][1]-v[b2][1];dz=v[a][2]-v[b2][2];
    d=Math.sqrt(dx*dx+dy*dy+dz*dz);
    if(Math.abs(d-2)<0.01)edges.push([a,b2]);
  }
  var nl=0;
  for(a=0;a<n;a++){var m=Math.sqrt(v[a][0]*v[a][0]+v[a][1]*v[a][1]+v[a][2]*v[a][2]);v[a]=[v[a][0]/m,v[a][1]/m,v[a][2]/m];}
  S.aiIco={v:v,e:edges};
},
frame:function(S){
  var c=S.ctx,w=S.w,h=S.h,p=S.p,t=S.t,i;
  var gg=c.createLinearGradient(0,0,0,h);
  gg.addColorStop(0,'#020610');gg.addColorStop(0.42,'#04101f');gg.addColorStop(1,'#01030a');
  c.fillStyle=gg;c.fillRect(0,0,w,h);
  var cx=w/2,hy=h*0.40;

  /* faint stars above horizon */
  var sr=mulberry(42);
  c.fillStyle='rgba(180,220,255,0.5)';
  for(i=0;i<40*S.q;i++){
    var sx=sr()*w,sy=sr()*hy*0.92;
    c.globalAlpha=0.15+sr()*0.35;
    c.fillRect(sx,sy,1.4,1.4);
  }
  c.globalAlpha=1;

  /* ---- perspective grid ---- */
  c.lineWidth=1;
  var laneX=function(l){return cx+l*w*0.008;};      /* at horizon */
  var laneXB=function(l){return cx+l*w*0.085;};     /* at bottom */
  c.strokeStyle='rgba(0,229,255,0.28)';
  c.beginPath();
  for(i=-9;i<=9;i++){c.moveTo(laneX(i),hy);c.lineTo(laneXB(i),h);}
  c.stroke();
  var HN=13;
  c.strokeStyle='rgba(0,229,255,0.22)';
  c.beginPath();
  for(i=0;i<HN;i++){
    var kk=(i+p)/HN,yy=hy+(h-hy)*Math.pow(kk,2.3);
    c.moveTo(0,yy);c.lineTo(w,yy);
  }
  c.stroke();
  /* horizon line */
  glowLine(S,0,hy,w,hy,'#00e5ff',1.5,0.8);

  /* ---- light trails ---- */
  for(i=0;i<S.aiTrails.length;i++){
    var tr=S.aiTrails[i];
    var s=((p*tr.spd+tr.off)%1+1)%1;
    var k1=Math.pow(s,2.3),k0=Math.pow(Math.max(0,s-0.09),2.3);
    var y1=hy+(h-hy)*k1,y0=hy+(h-hy)*k0;
    var x1=lerp(laneX(tr.lane),laneXB(tr.lane),k1);
    var x0=lerp(laneX(tr.lane),laneXB(tr.lane),k0);
    var fade=Math.sin(s*Math.PI);
    glowLine(S,x0,y0,x1,y1,tr.col,tr.wdt,0.25+0.75*fade);
    dot(S,x1,y1,tr.wdt*1.4,'#ffffff',0.9*fade);
  }

  /* ---- lens-flare horizon glow ---- */
  var fg=c.createRadialGradient(cx,hy,0,cx,hy,w*0.35);
  fg.addColorStop(0,'rgba(0,229,255,0.30)');
  fg.addColorStop(0.4,'rgba(0,150,255,0.10)');
  fg.addColorStop(1,'rgba(0,150,255,0)');
  c.fillStyle=fg;c.fillRect(0,0,w,h);
  dot(S,cx,hy,26,'rgba(140,240,255,0.35)',0.5);
  dot(S,cx,hy,9,'rgba(220,250,255,0.8)',0.8);

  /* ---- rotating wireframe icosahedron ---- */
  var ico=S.aiIco,ir=Math.min(w,h)*0.115;
  var icx=w*0.5,icy=hy*0.52;
  var ay=p*TAU*0.6,ax=p*TAU*0.35;
  var ca=Math.cos(ay),sa=Math.sin(ay),cb=Math.cos(ax),sb=Math.sin(ax);
  var P2=[];
  for(i=0;i<ico.v.length;i++){
    var vx=ico.v[i][0],vy=ico.v[i][1],vz=ico.v[i][2];
    var x1r=vx*ca+vz*sa,z1=-vx*sa+vz*ca;
    var y1r=vy*cb-z1*sb,z2=vy*sb+z1*cb;
    var persp=1/(1.6+z2*0.9);
    P2.push([icx+x1r*ir*2.2*persp,icy+y1r*ir*2.2*persp]);
  }
  c.strokeStyle='rgba(0,229,255,0.85)';c.lineWidth=1.2;
  c.beginPath();
  for(i=0;i<ico.e.length;i++){
    var e=ico.e[i];
    c.moveTo(P2[e[0]][0],P2[e[0]][1]);c.lineTo(P2[e[1]][0],P2[e[1]][1]);
  }
  c.stroke();
  for(i=0;i<P2.length;i++)dot(S,P2[i][0],P2[i][1],1.8,'#9df3ff',0.9);
  /* small orange satellite icosahedron */
  dot(S,w*0.82,hy*0.28,2,'#ff9a00',0.9);
  c.strokeStyle='rgba(255,154,0,0.6)';
  c.beginPath();c.arc(w*0.82,hy*0.28,10+4*Math.sin(p*TAU*2),0,TAU);c.stroke();

  vig(S,0.55);
  txt(S,'AI.02 // LIGHT CYCLE GRID',w-16,h-14,'rgba(0,229,255,0.6)',10,'right',1);
}
};

/* =====================================================================
   THEME 3 — cloud: orbital infrastructure.
   Thin orbital rings with satellite nodes, pulsing constellation
   link-lines, data packets traveling between nodes, deploy ripples.
   ===================================================================== */
THEMES['cloud']={
period:18,
init:function(S){
  var r=mulberry(hashStr('cloud-nodes'));
  var rings=[
    {rx:0.34,ry:0.40,tilt:-0.12,n:4,spd:1,dir:1},
    {rx:0.25,ry:0.30,tilt:0.18,n:3,spd:2,dir:-1},
    {rx:0.16,ry:0.19,tilt:-0.05,n:3,spd:3,dir:1}
  ];
  var nodes=[],i,j,k=0;
  for(i=0;i<rings.length;i++){
    var rg=rings[i];
    for(j=0;j<rg.n;j++){
      nodes.push({ring:i,off:(j/rg.n)+r()*0.05,spd:rg.spd,dir:rg.dir,rx:rg.rx,ry:rg.ry,tilt:rg.tilt,id:k++});
    }
  }
  /* link pairs: connect each node to the next ring's nearest + a few cross links */
  var links=[];
  for(i=0;i<nodes.length;i++){
    links.push([i,(i+3)%nodes.length]);
    if(i%2===0)links.push([i,(i+5)%nodes.length]);
  }
  S.clRings=rings;S.clNodes=nodes;S.clLinks=links;
  var stars=[],ns=Math.round(90*S.q);
  for(i=0;i<ns;i++)stars.push([r(),r(),0.2+r()*0.8]);
  S.clStars=stars;
},
nodePos:function(S,nd,p){
  var cx=S.w/2,cy=S.h/2;
  var a=p*TAU*nd.spd*nd.dir+nd.off*TAU;
  var ex=Math.cos(a)*nd.rx*S.w,ey=Math.sin(a)*nd.ry*S.h;
  /* apply ring tilt */
  var x=ex*Math.cos(nd.tilt)-ey*Math.sin(nd.tilt);
  var y=ex*Math.sin(nd.tilt)+ey*Math.cos(nd.tilt);
  return [cx+x,cy+y*0.9];
},
frame:function(S){
  var c=S.ctx,w=S.w,h=S.h,p=S.p,t=S.t,i;
  bg(S,'#030509');
  var cx=w/2,cy=h/2;

  /* star specks */
  for(i=0;i<S.clStars.length;i++){
    var st=S.clStars[i];
    c.globalAlpha=0.12+0.30*st[2]*(0.6+0.4*Math.sin(t*1.3+i));
    c.fillStyle='#bcd2ff';
    c.fillRect(st[0]*w,st[1]*h,1.3,1.3);
  }
  c.globalAlpha=1;

  var th=this;
  var pos=[];
  for(i=0;i<S.clNodes.length;i++)pos.push(th.nodePos(S,S.clNodes[i],p));

  /* orbital rings */
  c.lineWidth=1;
  for(i=0;i<S.clRings.length;i++){
    var rg=S.clRings[i];
    c.save();c.translate(cx,cy);c.rotate(rg.tilt);
    c.strokeStyle='rgba(140,180,255,0.20)';
    c.beginPath();c.ellipse(0,0,rg.rx*w,rg.ry*h*0.9,0,0,TAU);c.stroke();
    c.restore();
  }

  /* constellation links + packets */
  for(i=0;i<S.clLinks.length;i++){
    var A=pos[S.clLinks[i][0]],B=pos[S.clLinks[i][1]];
    var pulse=0.5+0.5*Math.sin(p*TAU*2+i*1.7);
    c.strokeStyle='rgba(120,170,255,'+(0.10+0.22*pulse)+')';
    c.lineWidth=1;
    c.beginPath();c.moveTo(A[0],A[1]);c.lineTo(B[0],B[1]);c.stroke();
    /* data packets */
    var pk;
    for(pk=0;pk<2;pk++){
      var q=((p*(1+S.clLinks[i][0]%3*0.5)+(i*0.37+pk*0.5))%1+1)%1;
      var px=lerp(A[0],B[0],q),py=lerp(A[1],B[1],q);
      dot(S,px,py,2.2,'#cfe4ff',0.35+0.55*Math.sin(q*Math.PI));
    }
  }

  /* satellite nodes */
  for(i=0;i<pos.length;i++){
    var hub=(i%4===0);
    var pr=hub?5:3.2;
    var halo=c.createRadialGradient(pos[i][0],pos[i][1],0,pos[i][0],pos[i][1],pr*4);
    halo.addColorStop(0,'rgba(160,200,255,0.5)');
    halo.addColorStop(1,'rgba(160,200,255,0)');
    c.fillStyle=halo;
    c.fillRect(pos[i][0]-pr*4,pos[i][1]-pr*4,pr*8,pr*8);
    dot(S,pos[i][0],pos[i][1],pr,hub?'#ffffff':'#9db9ff',0.95);
    if(hub){ /* hub node: small cross */
      c.strokeStyle='rgba(220,235,255,0.7)';c.lineWidth=1;
      c.beginPath();
      c.moveTo(pos[i][0]-8,pos[i][1]);c.lineTo(pos[i][0]+8,pos[i][1]);
      c.moveTo(pos[i][0],pos[i][1]-8);c.lineTo(pos[i][0],pos[i][1]+8);
      c.stroke();
    }
  }

  /* deploy pulse ripples: two per loop from the primary hub */
  var rip=[[0.18,0.38],[0.60,0.80]];
  for(i=0;i<rip.length;i++){
    if(p>=rip[i][0]&&p<=rip[i][1]){
      var rk=(p-rip[i][0])/(rip[i][1]-rip[i][0]);
      ring(S,pos[0][0],pos[0][1],8,Math.min(w,h)*0.45,rk,'#7fb2ff',1.5,0.7);
      if(rk<0.25)txt(S,'DEPLOY',pos[0][0],pos[0][1]-16,'#bcd6ff',10,'center',1-rk*4);
    }
  }

  /* central core */
  var core=c.createRadialGradient(cx,cy,0,cx,cy,44);
  core.addColorStop(0,'rgba(150,190,255,0.28)');
  core.addColorStop(1,'rgba(150,190,255,0)');
  c.fillStyle=core;c.fillRect(cx-44,cy-44,88,88);
  dot(S,cx,cy,3,'#e8f1ff',0.9);
  txt(S,'MESH // 99.99%',cx,cy+22,'rgba(160,190,255,0.7)',10,'center',1);

  vig(S,0.55);
  txt(S,'CLOUD.03 // ORBITAL MESH',w-16,h-14,'rgba(140,180,255,0.6)',10,'right',1);
}
};

/* =====================================================================
   THEME 4 — data: data stream.
   Flowing particle streams converging into live-updating bar charts,
   a scrolling line chart, and ticking monospace readouts.
   ===================================================================== */
THEMES['data']={
period:14,
init:function(S){
  var r=mulberry(hashStr('data-parts'));
  var n=Math.round(110*S.q),parts=[],i;
  for(i=0;i<n;i++){
    parts.push({
      y0:r()*S.h, x0:-20-r()*S.w*0.25,
      spd:0.35+r()*0.6, off:r(),
      curve:(r()-0.5)*S.h*0.5,
      sz:1+r()*1.8, hue:r()
    });
  }
  S.daParts=parts;
  S.daBars=12;
  S.daLines=['INGEST','PARSE','INDEX','SERVE'];
},
frame:function(S){
  var c=S.ctx,w=S.w,h=S.h,p=S.p,t=S.t,i;
  bg(S,'#03110c');
  var ex=w*0.80,ey=h*0.46; /* convergence point */

  /* ---- particle streams ---- */
  for(i=0;i<S.daParts.length;i++){
    var pt=S.daParts[i];
    var s=((p*pt.spd+pt.off)%1+1)%1;
    var x=lerp(pt.x0,ex,easeIO(s));
    var y=lerp(pt.y0,ey,s)+Math.sin(s*Math.PI)*pt.curve*0.4;
    var a=Math.sin(s*Math.PI);
    var col=pt.hue<0.7?'#2dd4a7':'#5eead4';
    dot(S,x,y,pt.sz,col,0.15+0.75*a);
  }
  /* convergence glow */
  var cg=c.createRadialGradient(ex,ey,0,ex,ey,70);
  cg.addColorStop(0,'rgba(45,212,167,0.35)');
  cg.addColorStop(1,'rgba(45,212,167,0)');
  c.fillStyle=cg;c.fillRect(ex-70,ey-70,140,140);

  /* ---- live bar chart ---- */
  var bw=14,gap=8,bx=ex-((S.daBars*(bw+gap))/2),by=h*0.82,bmax=h*0.30;
  for(i=0;i<S.daBars;i++){
    var v=0.35+0.30*Math.sin(p*TAU*2+i*0.75)+0.20*Math.sin(p*TAU*3.3+i*1.9+1);
    v=clamp(v,0.06,1);
    var bh=v*bmax;
    var grd=c.createLinearGradient(0,by-bh,0,by);
    grd.addColorStop(0,'#5eead4');grd.addColorStop(1,'rgba(45,212,167,0.25)');
    c.fillStyle=grd;
    c.fillRect(bx+i*(bw+gap),by-bh,bw,bh);
  }
  c.strokeStyle='rgba(94,234,212,0.4)';c.lineWidth=1;
  c.beginPath();c.moveTo(bx-8,by+0.5);c.lineTo(bx+S.daBars*(bw+gap),by+0.5);c.stroke();
  txt(S,'THROUGHPUT',bx,by+18,'rgba(94,234,212,0.7)',10,'left',1);

  /* ---- scrolling line chart ---- */
  var lx=24,lw=w*0.34,lh=h*0.24,ly0=h*0.60;
  c.fillStyle='rgba(3,20,15,0.75)';c.fillRect(lx-8,ly0-lh-24,lw+16,lh+40);
  c.strokeStyle='rgba(94,234,212,0.25)';c.strokeRect(lx-7.5,ly0-lh-23.5,lw+15,lh+39);
  var val=function(ph){
    return 0.5+0.28*Math.sin(ph*TAU*3)+0.14*Math.sin(ph*TAU*7+1.2)+0.06*Math.sin(ph*TAU*13);
  };
  var N=60;
  c.strokeStyle='#5eead4';c.lineWidth=1.6;c.beginPath();
  for(i=0;i<=N;i++){
    var ph=p-0.45+0.45*i/N; /* trailing window, loops because val is periodic in ph */
    var px=lx+lw*i/N,py=ly0-val(ph)*lh;
    if(i===0)c.moveTo(px,py);else c.lineTo(px,py);
  }
  c.stroke();
  /* area fill */
  c.lineTo(lx+lw,ly0);c.lineTo(lx,ly0);c.closePath();
  c.fillStyle='rgba(94,234,212,0.08)';c.fill();
  /* head dot */
  var hv=val(p);
  dot(S,lx+lw,ly0-hv*lh,3,'#a7f3d0',1);
  txt(S,'SIGNAL',lx,ly0-lh-8,'rgba(94,234,212,0.7)',10,'left',1);

  /* ---- ticking readouts ---- */
  var rows=[
    ['PKT/S',Math.floor(12000+3200*Math.sin(p*TAU*3)+900*Math.sin(p*TAU*9)).toLocaleString('en-US')],
    ['LAT MS',(4.2+1.8*Math.sin(p*TAU*2+1)).toFixed(2)],
    ['ERR %',(0.03+0.02*Math.abs(Math.sin(p*TAU*5))).toFixed(3)],
    ['SHARD','0x'+Math.floor(4096+2048*Math.sin(p*TAU*4)).toString(16).toUpperCase()]
  ];
  for(i=0;i<rows.length;i++){
    txt(S,rows[i][0],24,34+i*22,'rgba(45,212,167,0.65)',11,'left',1);
    txt(S,rows[i][1],110,34+i*22,'#a7f3d0',12,'left',1);
  }
  txt(S,'STREAM // LIVE',24,20,'#5eead4',10,'left',0.85);

  vig(S,0.5);
  txt(S,'DATA.04 // STREAMS',w-16,h-14,'rgba(94,234,212,0.6)',10,'right',1);
}
};

/* =====================================================================
   THEME 5 — code: circuit.
   PCB traces lighting up in sequence toward a central chip, a typing
   code panel, compile-success pulses.
   ===================================================================== */
THEMES['code']={
period:16,
init:function(S){
  var r=mulberry(hashStr('code-traces'));
  var traces=[],i;
  var chipX=S.w*0.52,chipY=S.h*0.52,cw=110,ch=76;
  /* pads on left edge and bottom edge */
  for(i=0;i<7;i++){
    var py=40+i*((S.h-80)/6);
    var pts=[[14,py]];
    var mx=chipX-cw/2-30-r()*60;
    pts.push([mx,py]);
    pts.push([mx,chipY-ch/2-14-i*2]);
    pts.push([chipX-cw/2,chipY-ch/2-14-i*2]);
    traces.push({pts:pts,st:i*0.055,pad:[14,py]});
  }
  for(i=0;i<5;i++){
    var px=S.w*0.15+i*((S.w*0.6)/4);
    var pts2=[[px,S.h-14]];
    var my=chipY+ch/2+24+r()*40;
    pts2.push([px,my]);
    pts2.push([chipX-cw/2+20+i*16,my]);
    pts2.push([chipX-cw/2+20+i*16,chipY+ch/2]);
    traces.push({pts:pts2,st:0.42+i*0.05,pad:[px,S.h-14]});
  }
  S.coTraces=traces;
  S.coChip={x:chipX,y:chipY,w:cw,h:ch};
  S.coCode=[
    'fn route(pkt: &Packet) -> Status {',
    '  let sig = verify(&pkt.sig);',
    '  match sig.trust() {',
    '    Trust::Full  => forward(pkt),',
    '    Trust::None  => quarantine(pkt),',
    '  }',
    '}'
  ];
},
traceLen:function(pts){
  var L=0;
  for(var i=1;i<pts.length;i++)L+=Math.abs(pts[i][0]-pts[i-1][0])+Math.abs(pts[i][1]-pts[i-1][1]);
  return L;
},
drawTrace:function(S,pts,k,color){
  /* draw the first k fraction of the orthogonal path */
  var c=S.ctx;
  var total=this.traceLen(pts),target=total*k,done=0;
  c.strokeStyle=color;c.lineWidth=2;c.lineCap='round';c.lineJoin='round';
  c.beginPath();c.moveTo(pts[0][0],pts[0][1]);
  for(var i=1;i<pts.length&&done<target;i++){
    var seg=Math.abs(pts[i][0]-pts[i-1][0])+Math.abs(pts[i][1]-pts[i-1][1]);
    if(done+seg<=target){c.lineTo(pts[i][0],pts[i][1]);done+=seg;}
    else{
      var f=(target-done)/seg;
      c.lineTo(lerp(pts[i-1][0],pts[i][0],f),lerp(pts[i-1][1],pts[i][1],f));
      done=target;
    }
  }
  c.stroke();
},
frame:function(S){
  var c=S.ctx,w=S.w,h=S.h,p=S.p,t=S.t,i;
  bg(S,'#0a0f04');
  var th=this;

  /* faint PCB grid dots */
  c.fillStyle='rgba(163,230,53,0.10)';
  var gs=34;
  for(var gx=gs/2;gx<w;gx+=gs)for(var gy=gs/2;gy<h;gy+=gs)c.fillRect(gx,gy,1.6,1.6);

  /* ---- traces lighting in sequence ---- */
  for(i=0;i<S.coTraces.length;i++){
    var tr=S.coTraces[i];
    var local=(p-tr.st)/0.34;
    /* pad */
    dot(S,tr.pad[0],tr.pad[1],3,'#a3e635',0.5);
    if(local<=0||local>=1.6)continue;
    var a=local<1?local:(1.6-local)/0.6;
    var col='rgba(163,230,53,'+(0.25+0.65*a)+')';
    if(local<1){
      th.drawTrace(S,tr.pts,smooth(local),col);
      /* signal head dot */
      var total=th.traceLen(tr.pts),target=total*smooth(local),done=0,hx=tr.pts[0][0],hy=tr.pts[0][1];
      for(var sgi=1;sgi<tr.pts.length;sgi++){
        var seg=Math.abs(tr.pts[sgi][0]-tr.pts[sgi-1][0])+Math.abs(tr.pts[sgi][1]-tr.pts[sgi-1][1]);
        if(done+seg<=target){hx=tr.pts[sgi][0];hy=tr.pts[sgi][1];done+=seg;}
        else{var f=(target-done)/seg;hx=lerp(tr.pts[sgi-1][0],tr.pts[sgi][0],f);hy=lerp(tr.pts[sgi-1][1],tr.pts[sgi][1],f);break;}
      }
      dot(S,hx,hy,3,'#d9f99d',0.95);
    }else{
      th.drawTrace(S,tr.pts,1,col);
    }
  }

  /* ---- central chip ---- */
  var chp=S.coChip;
  c.fillStyle='#111a08';
  c.fillRect(chp.x-chp.w/2,chp.y-chp.h/2,chp.w,chp.h);
  c.strokeStyle='rgba(163,230,53,0.8)';c.lineWidth=1.5;
  c.strokeRect(chp.x-chp.w/2+0.5,chp.y-chp.h/2+0.5,chp.w-1,chp.h-1);
  /* pins */
  c.fillStyle='rgba(163,230,53,0.7)';
  for(i=0;i<8;i++){
    c.fillRect(chp.x-chp.w/2-6,chp.y-chp.h/2+6+i*((chp.h-12)/7),6,2.4);
    c.fillRect(chp.x+chp.w/2,chp.y-chp.h/2+6+i*((chp.h-12)/7),6,2.4);
  }
  txt(S,'IL-CORE',chp.x,chp.y+4,'#d9f99d',11,'center',0.9);

  /* compile-success pulses */
  var cT=p*16;
  if(cT>9.5&&cT<12.5){
    var ck=(cT-9.5)/3;
    ring(S,chp.x,chp.y,20,120,ck,'#a3e635',2,0.8);
  }
  if(cT>10&&cT<14){
    txt(S,'BUILD OK',chp.x,chp.y-chp.h/2-16,'#a3e635',12,'center',
      Math.min(1,(cT-10))*Math.min(1,(14-cT)));
  }

  /* ---- typing code panel ---- */
  var pw=Math.min(w*0.36,330),ph2=150,px2=w-pw-20,py2=20;
  c.fillStyle='rgba(5,10,2,0.85)';c.fillRect(px2,py2,pw,ph2);
  c.strokeStyle='rgba(163,230,53,0.35)';c.lineWidth=1;
  c.strokeRect(px2+0.5,py2+0.5,pw-1,ph2-1);
  txt(S,'router.rs',px2+10,py2+18,'rgba(163,230,53,0.7)',10,'left',1);
  var total=S.coCode.join('\n').length;
  var typeT=p*16,nch=typeT<8?Math.floor(typeT/8*total):total;
  var wipe=typeT>13.5?(16-typeT)/2.5:1;
  c.save();c.globalAlpha=Math.max(0,wipe);
  var li2=0,rem2=nch;
  while(li2<S.coCode.length&&rem2>S.coCode[li2].length){rem2-=S.coCode[li2].length+1;li2++;}
  c.font='11px '+MONO;
  for(i=0;i<li2&&i<S.coCode.length;i++){
    c.fillStyle='#bef264';c.fillText(S.coCode[i],px2+10,py2+40+i*15);
  }
  if(li2<S.coCode.length){
    var pl2=S.coCode[li2].substring(0,Math.max(0,rem2));
    c.fillStyle='#bef264';c.fillText(pl2,px2+10,py2+40+li2*15);
  }
  c.restore();

  vig(S,0.5);
  txt(S,'CODE.05 // PCB',w-16,h-14,'rgba(163,230,53,0.6)',10,'right',1);
}
};

/* =====================================================================
   THEME 6 — math: sacred geometry.
   Compass-and-straightedge constructions drawing themselves, a golden
   spiral, a rotating geometric lattice, formula glyphs fading in/out.
   ===================================================================== */
THEMES['math']={
period:18,
init:function(S){
  var r=mulberry(hashStr('math-glyphs'));
  var glyphs=['π','∑','∫','√','φ','∞','∂','λ','θ','Δ'],g=[],i;
  for(i=0;i<glyphs.length;i++){
    g.push({ch:glyphs[i],x:0.08+r()*0.84,y:0.12+r()*0.76,off:r(),sz:20+r()*26});
  }
  S.maGlyphs=g;
},
frame:function(S){
  var c=S.ctx,w=S.w,h=S.h,p=S.p,t=S.t,i;
  bg(S,'#0d0902');
  var cx=w*0.5,cy=h*0.52,R=Math.min(w,h)*0.30;

  /* ---- rotating geometric lattice (behind) ---- */
  c.save();c.translate(cx,cy);c.rotate(p*TAU*0.25);
  c.strokeStyle='rgba(251,191,36,0.10)';c.lineWidth=1;
  var lr=R*2.2;
  for(i=-6;i<=6;i++){
    c.beginPath();c.moveTo(i*lr/6,-lr);c.lineTo(i*lr/6,lr);c.stroke();
    c.beginPath();c.moveTo(-lr,i*lr/6);c.lineTo(lr,i*lr/6);c.stroke();
  }
  c.strokeStyle='rgba(251,191,36,0.16)';
  c.beginPath();c.arc(0,0,R*1.35,0,TAU);c.stroke();
  c.beginPath();
  for(i=0;i<6;i++){
    var a2=i/6*TAU;
    c.moveTo(Math.cos(a2)*R*1.35,Math.sin(a2)*R*1.35);
    c.lineTo(Math.cos(a2+TAU/3)*R*1.35,Math.sin(a2+TAU/3)*R*1.35);
  }
  c.stroke();
  c.restore();

  /* ---- compass constructions drawing themselves ---- */
  var cons=[
    {x:cx-R*0.85,y:cy+R*0.15,r:R*0.55,a:0.02,b:0.30,col:'#fbbf24'},
    {x:cx+R*0.85,y:cy+R*0.15,r:R*0.55,a:0.10,b:0.38,col:'#f59e0b'},
    {x:cx,y:cy-R*0.55,r:R*0.62,a:0.20,b:0.48,col:'#fcd34d'}
  ];
  for(i=0;i<cons.length;i++){
    var cn=cons[i];
    var k=smooth((p-cn.a)/(cn.b-cn.a));
    if(k<=0)continue;
    var al=k<1?0.95:0.55+0.25*Math.sin(t*2+i);
    c.save();c.globalAlpha=al;
    c.strokeStyle=cn.col;c.lineWidth=1.4;
    /* center cross */
    c.beginPath();
    c.moveTo(cn.x-5,cn.y);c.lineTo(cn.x+5,cn.y);
    c.moveTo(cn.x,cn.y-5);c.lineTo(cn.x,cn.y+5);
    c.stroke();
    /* sweeping arc */
    c.beginPath();c.arc(cn.x,cn.y,cn.r,-Math.PI/2,-Math.PI/2+k*TAU);c.stroke();
    /* compass needle: center to arc head */
    var ha=-Math.PI/2+k*TAU;
    var hx=cn.x+Math.cos(ha)*cn.r,hy2=cn.y+Math.sin(ha)*cn.r;
    c.strokeStyle='rgba(253,224,71,0.5)';
    c.beginPath();c.moveTo(cn.x,cn.y);c.lineTo(hx,hy2);c.stroke();
    dot(S,hx,hy2,2.5,cn.col,0.95);
    /* when complete: straightedge chord + intersection ticks */
    if(k>=1){
      c.strokeStyle='rgba(251,191,36,0.45)';c.lineWidth=1;
      c.beginPath();
      c.moveTo(cn.x-cn.r*0.8,cn.y+cn.r*0.5);
      c.lineTo(cn.x+cn.r*0.8,cn.y-cn.r*0.3);
      c.stroke();
    }
    c.restore();
  }

  /* ---- golden-ratio spiral (logarithmic, grows by φ per quarter turn) ---- */
  var phi=(1+Math.sqrt(5))/2;
  var sp=smooth((p-0.45)/0.4);
  if(sp>0){
    c.save();c.globalAlpha=0.9;
    c.strokeStyle='#fde68a';c.lineWidth=1.6;
    var scx=cx+R*1.02,scy=cy-R*0.95;
    var r0=R*0.035,turns=3.1,thMax=sp*turns*TAU,rot=-Math.PI/2;
    c.beginPath();
    var steps2=Math.max(8,Math.floor(thMax*24));
    for(i=0;i<=steps2;i++){
      var th2=i/steps2*thMax;
      var rr=r0*Math.pow(phi,th2/(Math.PI/2));
      var px2=scx+Math.cos(th2+rot)*rr,py2=scy+Math.sin(th2+rot)*rr;
      if(i===0)c.moveTo(px2,py2);else c.lineTo(px2,py2);
    }
    c.stroke();
    c.restore();
    txt(S,'φ = 1.618…',scx+8,scy+10,'rgba(253,230,138,0.75)',11,'left',sp);
  }

  /* ---- formula glyphs fading in/out ---- */
  c.textBaseline='middle';
  for(i=0;i<S.maGlyphs.length;i++){
    var gl2=S.maGlyphs[i];
    var ga=Math.pow(Math.max(0,Math.sin(p*TAU+gl2.off*TAU)),1.6);
    if(ga<0.02)continue;
    c.save();c.globalAlpha=ga*0.8;
    c.font=gl2.sz+'px '+MONO;
    c.fillStyle='#fcd34d';
    c.fillText(gl2.ch,gl2.x*w,gl2.y*h);
    c.restore();
  }
  c.textBaseline='alphabetic';

  vig(S,0.55);
  txt(S,'MATH.06 // SACRED GEOMETRY',w-16,h-14,'rgba(251,191,36,0.6)',10,'right',1);
}
};

/* =====================================================================
   THEME 7 — career: spotlight.
   Dark stage, sweeping spotlight cone, looping rising bar "level up"
   chart, clean gold motes (no confetti).
   ===================================================================== */
THEMES['career']={
period:12,
init:function(S){
  var r=mulberry(hashStr('career-motes'));
  var n=Math.round(45*S.q),motes=[],i;
  for(i=0;i<n;i++)motes.push({x:r(),spd:0.25+r()*0.5,off:r(),sz:1+r()*2.2,sw:r()*TAU});
  S.caMotes=motes;
  S.caBars=7;
},
frame:function(S){
  var c=S.ctx,w=S.h?S.w:0,h=S.h,p=S.p,t=S.t,i;
  bg(S,'#0b0803');

  /* stage floor */
  var fl=c.createLinearGradient(0,h*0.55,0,h);
  fl.addColorStop(0,'rgba(20,14,4,0)');
  fl.addColorStop(1,'rgba(60,42,8,0.55)');
  c.fillStyle=fl;c.fillRect(0,h*0.55,w,h*0.45);

  /* ---- sweeping spotlight cone ---- */
  var sx=w*0.5,sy=-20;
  var sweep=Math.sin(p*TAU)*0.38;
  var px=sx+Math.tan(sweep)*h*1.1,py=h;
  var cone=c.createLinearGradient(sx,sy,px,py);
  cone.addColorStop(0,'rgba(251,191,36,0.34)');
  cone.addColorStop(1,'rgba(251,191,36,0.03)');
  c.fillStyle=cone;
  c.beginPath();
  c.moveTo(sx-26,sy);c.lineTo(sx+26,sy);
  c.lineTo(px+150,py);c.lineTo(px-150,py);
  c.closePath();c.fill();
  /* light pool on the floor */
  var pool=c.createRadialGradient(px,py-8,0,px,py-8,150);
  pool.addColorStop(0,'rgba(251,191,36,0.30)');
  pool.addColorStop(1,'rgba(251,191,36,0)');
  c.save();c.translate(px,py-8);c.scale(1,0.22);c.translate(-px,-(py-8));
  c.fillStyle=pool;
  c.beginPath();c.arc(px,py-8,150,0,TAU);c.fill();
  c.restore();
  /* fixture */
  c.fillStyle='#1a1206';
  c.fillRect(sx-30,sy,60,26);
  c.strokeStyle='rgba(251,191,36,0.6)';c.lineWidth=1.5;
  c.strokeRect(sx-30.5,sy+0.5,60,26);

  /* ---- rising level-up bars ---- */
  var n=S.caBars,bw=Math.min(46,w*0.075),gap=14;
  var bwTot=n*(bw+gap)-gap,bx0=w/2-bwTot/2,base=h*0.86,maxH=h*0.52;
  var rise=smooth(p/0.55),holdA=p>0.82?(1-p)/0.18:1;
  for(i=0;i<n;i++){
    var local=clamp((p*1.35-i*0.11)/0.55,0,1);
    var bh=easeIO(local)*maxH*(0.45+0.55*(i/(n-1)));
    var bx=bx0+i*(bw+gap);
    var grd=c.createLinearGradient(0,base-bh,0,base);
    grd.addColorStop(0,'#fde68a');grd.addColorStop(1,'rgba(180,120,20,0.35)');
    c.save();c.globalAlpha=Math.max(0,holdA);
    c.fillStyle=grd;
    c.fillRect(bx,base-bh,bw,bh);
    c.fillStyle='rgba(251,191,36,0.9)';
    c.fillRect(bx,base-bh,bw,3);
    c.restore();
  }
  c.save();c.globalAlpha=Math.max(0,holdA)*0.5;
  c.strokeStyle='#fbbf24';c.lineWidth=1;
  c.beginPath();c.moveTo(bx0-16,base+0.5);c.lineTo(bx0+bwTot+16,base+0.5);c.stroke();
  c.restore();

  /* LEVEL UP text at the peak */
  var peakA=smooth((p-0.5)/0.08)*(p>0.82?(1-p)/0.18:1);
  if(peakA>0){
    c.save();c.globalAlpha=peakA;
    c.font='600 30px '+MONO;c.textAlign='center';
    c.fillStyle='#fde68a';
    c.shadowColor='rgba(251,191,36,0.8)';c.shadowBlur=24;
    c.fillText('L E V E L  U P',w/2,h*0.20);
    c.restore();
    txt(S,'+2,400 XP',w/2,h*0.20+26,'rgba(253,230,138,0.9)',13,'center',peakA);
  }

  /* ---- gold motes rising ---- */
  for(i=0;i<S.caMotes.length;i++){
    var mt=S.caMotes[i];
    var s2=((p*mt.spd+mt.off)%1+1)%1;
    var mx=mt.x*w+Math.sin(s2*6+mt.sw)*14;
    var my=h-(s2*(h*0.95));
    dot(S,mx,my,mt.sz,'#fcd34d',(1-s2)*0.7);
  }

  vig(S,0.6);
  txt(S,'CAREER.07 // SPOTLIGHT',w-16,h-14,'rgba(251,191,36,0.6)',10,'right',1);
}
};

/* =====================================================================
   THEME 8 — frontier: cosmic/quantum.
   Parallax starfield, drifting nebula wisps, a shimmering quantum
   double-slit interference pattern, occasional warp streaks.
   ===================================================================== */
THEMES['frontier']={
period:20,
init:function(S){
  var r=mulberry(hashStr('frontier-stars'));
  var layers=[],i,L;
  var counts=[70,45,25];
  for(L=0;L<3;L++){
    var arr=[];
    for(i=0;i<Math.round(counts[L]*S.q);i++){
      arr.push({x:r(),y:r(),sz:0.6+L*0.7+r()*1.2,tw:r()*TAU,drift:0.02+L*0.035});
    }
    layers.push(arr);
  }
  S.frLayers=layers;
  var streaks=[];
  for(i=0;i<6;i++)streaks.push({y:r(),spd:0.5+r()*0.7,off:r(),len:0.10+r()*0.12,hue:r()});
  S.frStreaks=streaks;
},
frame:function(S){
  var c=S.ctx,w=S.w,h=S.h,p=S.p,t=S.t,i,L;
  bg(S,'#05030d');

  /* ---- nebula wisps (behind stars) ---- */
  var nebs=[
    {x:0.28+0.05*Math.sin(p*TAU),y:0.35+0.04*Math.cos(p*TAU*0.8),r:0.30,col:'124,58,237'},
    {x:0.72+0.04*Math.cos(p*TAU*0.7),y:0.62+0.05*Math.sin(p*TAU),r:0.34,col:'192,38,211'},
    {x:0.55+0.03*Math.sin(p*TAU*1.3),y:0.20+0.03*Math.cos(p*TAU),r:0.24,col:'59,130,246'}
  ];
  for(i=0;i<nebs.length;i++){
    var nb=nebs[i];
    var ng=c.createRadialGradient(nb.x*w,nb.y*h,0,nb.x*w,nb.y*h,nb.r*Math.max(w,h));
    ng.addColorStop(0,'rgba('+nb.col+',0.20)');
    ng.addColorStop(1,'rgba('+nb.col+',0)');
    c.fillStyle=ng;c.fillRect(0,0,w,h);
  }

  /* ---- parallax starfield ---- */
  for(L=0;L<S.frLayers.length;L++){
    var lay=S.frLayers[L];
    for(i=0;i<lay.length;i++){
      var s2=lay[i];
      var sx=(((s2.x-p*s2.drift)%1)+1)%1*w;
      var twk=0.55+0.45*Math.sin(t*2.2+s2.tw);
      c.globalAlpha=twk*(0.35+L*0.25);
      c.fillStyle=L===2?'#e9d5ff':'#c4b5fd';
      c.fillRect(sx,s2.y*h,s2.sz,s2.sz);
    }
  }
  c.globalAlpha=1;

  /* ---- quantum double-slit interference ---- */
  var slitY=h*0.52,bandH=h*0.30;
  var x0=w*0.12,x1=w*0.88;
  var steps=Math.floor((x1-x0)/3);
  c.save();
  for(i=0;i<=steps;i++){
    var fx=i/steps,px=x0+fx*(x1-x0);
    var u=(fx-0.5)*2; /* -1..1 */
    var env=Math.exp(-u*u*4.5);
    var interf=Math.pow(Math.cos(u*22),2);
    var shimmer=0.82+0.18*Math.sin(p*TAU*3+fx*14);
    var inten=env*interf*shimmer;
    if(inten<0.015)continue;
    var grad=c.createLinearGradient(0,slitY-bandH/2,0,slitY+bandH/2);
    grad.addColorStop(0,'rgba(167,139,250,0)');
    grad.addColorStop(0.5,'rgba(196,181,253,'+(0.75*inten)+')');
    grad.addColorStop(1,'rgba(167,139,250,0)');
    c.fillStyle=grad;
    c.fillRect(px,slitY-bandH/2,3,bandH);
  }
  c.restore();
  /* slit barrier hint */
  c.fillStyle='rgba(10,6,24,0.9)';
  c.fillRect(w/2-3,slitY-bandH/2-26,2,20);
  c.fillRect(w/2+1,slitY-bandH/2-26,2,20);
  txt(S,'DOUBLE-SLIT // ψ',w/2,slitY+bandH/2+30,'rgba(196,181,253,0.75)',11,'center',1);

  /* ---- warp streaks ---- */
  for(i=0;i<S.frStreaks.length;i++){
    var ws=S.frStreaks[i];
    var q=((p*ws.spd+ws.off)%1+1)%1;
    var wx0=q*w,wy=ws.y*h;
    var wl=ws.len*w*(0.4+0.6*q);
    var wg=c.createLinearGradient(wx0,0,wx0-wl,0);
    var wc=ws.hue<0.5?'196,181,253':'125,211,252';
    wg.addColorStop(0,'rgba('+wc+','+(0.75*Math.sin(q*Math.PI))+')');
    wg.addColorStop(1,'rgba('+wc+',0)');
    c.fillStyle=wg;
    c.fillRect(wx0-wl,wy-1,wl,2);
  }

  vig(S,0.6);
  txt(S,'FRONTIER.08 // DEEP FIELD',w-16,h-14,'rgba(196,181,253,0.6)',10,'right',1);
}
};

/* ---------- public API ---------- */
window.ILThemeHeroes={
  mount:mount,
  unmount:unmount,
  themes:function(){var k,out=[];for(k in THEMES)out.push(k);return out;}
};

})();
