/*!
 * il-cine-cards.js — TikTok-style cinematic preview cards for Interstitium Labs programs.
 * ES5, no external deps. Exposes window.ILCineCards.
 *
 * API:
 *   ILCineCards.render(container, programCode)   -> HTMLElement | null
 *   ILCineCards.renderAll(container, codes)      -> renders a grid (codes optional, defaults to all 31)
 *   ILCineCards.PROGRAMS                          -> config array (31 entries)
 *
 * Card: vertical 9:16 dark container, theme-accented, ~15s animation loop,
 * 4 numbered step pills highlighting 1->4, live stat count-up, price badge,
 * Noah-tutored badge, CTA, Noah TTS voiceover button w/ captions.
 * Cards animate only when visible (IntersectionObserver); prefers-reduced-motion
 * renders one static frame. Independent-prep framing wherever certs are mentioned.
 */
(function(){
'use strict';

var LOOP = 15; /* seconds per social loop */
var ACCENT_DEFAULT = '#6ba8ff';

/* ---------------- data: all 31 programs (source of truth from user order) ---------------- */
/* fields: code, title, take, steps[4], viz, vlabels[4], accent, hrs, mods, free */
var PROGRAMS = [
 {code:'IL-01',title:'Esoteric Foundations',take:'Western esotericism decoded — from Hermeticism to the Golden Dawn.',steps:['Core esoteric map','Key texts & lineages','Symbol systems','Noah check-in'],viz:'radar',vlabels:['Hermeticism','Kabbalah','Alchemy','Tarot'],accent:'#c084fc',hrs:29,mods:5},
 {code:'IL-02',title:'Mathematical Maturity Engine',take:'Proof-first math that makes every technical field readable.',steps:['Logic & proof','Core structures','Problem drills','Noah check-in'],viz:'line',vlabels:['Logic','Sets','Proof','Limits'],accent:'#fbbf24',hrs:34,mods:7},
 {code:'IL-03',title:'Programming Language Forge',take:'Build languages, not just apps — syntax to interpreter.',steps:['Language theory','Grammar & parsing','Interpreter build','Noah check-in'],viz:'bars',vlabels:['Lexer','Parser','AST','Runtime'],accent:'#a3e635',hrs:34,mods:8},
 {code:'IL-04',title:'Systems, Linux, Windows & Networks',take:'The machine under the code: OS, shell, and packets.',steps:['OS internals','Linux & Windows labs','Networking','Noah check-in'],viz:'flow',vlabels:['Kernel','Shell','TCP/IP','DNS'],accent:'#a3e635',hrs:34,mods:7},
 {code:'IL-05',title:'Cloud, DevSecOps, Platform & SRE',take:'Ship like a platform team: cloud, CI/CD, reliability.',steps:['Cloud core','CI/CD pipelines','Observability','SRE practice'],viz:'flow',vlabels:['Build','Deploy','Monitor','Scale'],accent:'#6ba8ff',hrs:92,mods:17},
 {code:'IL-06',title:'Cybersecurity & Secure Engineering',take:'Think like an attacker, build like a defender.',steps:['Security mindset','Attack surface','Secure coding','Noah check-in'],viz:'grid',vlabels:['Recon','Exploit','Harden','Monitor'],accent:'#ff6b6b',vizAccent:'#22ff88',hrs:46,mods:9},
 {code:'IL-07',title:'SQL, Data Engineering, Analytics & AI',take:'From raw tables to AI-ready pipelines.',steps:['SQL mastery','Data pipelines','Analytics','AI workflows'],viz:'bars',vlabels:['Query','Model','Pipe','Predict'],accent:'#4ade80',hrs:63,mods:12},
 {code:'IL-08',title:'Algorithms, Compilers, Distributed & Formal',take:'The deep machinery: algorithms, compilers, proofs.',steps:['Core algorithms','Compiler pipeline','Distributed systems','Formal methods'],viz:'line',vlabels:['Sort','Parse','Consensus','Verify'],accent:'#a3e635',hrs:29,mods:5},
 {code:'IL-09',title:'Adaptive Certification Command',take:'A study command center that adapts to your gaps.',steps:['Skills diagnostic','Study plan','Practice exams','Noah check-in'],viz:'steps',vlabels:['Assess','Plan','Drill','Pass'],accent:'#f0c040',hrs:52,mods:9},
 {code:'IL-10',title:'Portfolio, Career & Professional Practice',take:'Proof of work that hiring managers actually read.',steps:['Portfolio build','Resume & LinkedIn','Interview reps','Noah check-in'],viz:'steps',vlabels:['Build','Brand','Pitch','Land'],accent:'#f0c040',hrs:29,mods:6},
 {code:'IL-11',title:'Zero Trust & Endpoint Defense',take:'Trust nothing, verify everything — endpoint to network.',steps:['Zero-trust model','Endpoint hardening','Detection & response','Noah check-in'],viz:'radar',vlabels:['Identity','Device','Network','Data'],accent:'#ff6b6b',hrs:155,mods:28},
 {code:'IL-12',title:'AI Engineering',take:'Production AI systems: RAG, agents, evals, deployment.',steps:['LLM systems','RAG pipelines','Agent design','Ship & eval'],viz:'flow',vlabels:['Retrieve','Reason','Act','Eval'],accent:'#7fd4e8',hrs:414,mods:73},
 {code:'IL-13',title:'Software Engineering Interview Prep',take:'Code, design, and behavior — interview-ready in weeks.',steps:['DSA drills','System design','Behavioral reps','Mock interviews'],viz:'bars',vlabels:['Arrays','Graphs','Design','Mock'],accent:'#f0c040',hrs:334,mods:58},
 {code:'IL-14',title:'SRE, DevOps, Cloud & Security Interview Prep',take:'Talk reliability, security, and scale with confidence.',steps:['Infra drills','Incident scenarios','Security rounds','Mock interviews'],viz:'flow',vlabels:['CI/CD','K8s','Incidents','Sec'],accent:'#f0c040',hrs:178,mods:31},
 {code:'IL-15',title:'Data Engineering & Analytics Interview Prep',take:'SQL, pipelines, and stats — on the spot, on the record.',steps:['SQL drills','Pipeline design','Analytics cases','Mock interviews'],viz:'line',vlabels:['SQL','ETL','Metrics','Case'],accent:'#4ade80',hrs:184,mods:32},
 {code:'IL-16',title:'Machine Learning & AI Engineering',take:'From loss curves to deployed models.',steps:['ML foundations','Deep learning','Training loops','Deploy & eval'],viz:'line',vlabels:['Loss','Gradient','Epoch','Serve'],accent:'#7fd4e8',hrs:449,mods:48},
 {code:'IL-17',title:'Agentic AI Engineering',take:'Agents that plan, tool-use, and ship real work.',steps:['Agent patterns','Tool use','Multi-agent systems','Evals & guardrails'],viz:'flow',vlabels:['Plan','Tool','Coordinate','Guard'],accent:'#7fd4e8',hrs:329,mods:46},
 {code:'IL-18',title:'Technical Leadership Interview Prep',take:'Leadership stories, system judgment, exec presence.',steps:['Leadership stories','Architecture judgment','People scenarios','Mock panels'],viz:'steps',vlabels:['Story','Design','People','Panel'],accent:'#f0c040',hrs:250,mods:32},
 {code:'IL-19',title:'MultiCloud, DevOps & AI Bootcamp',take:'One engineer, three clouds, AI everywhere.',steps:['Cloud trio','DevOps toolchain','AI integration','Capstone build'],viz:'flow',vlabels:['AWS','Azure','GCP','AI'],accent:'#6ba8ff',hrs:343,mods:67},
 {code:'IL-20',title:'Mathematics for Engineers & Scientists',take:'The math stack behind every simulation and model.',steps:['Linear algebra','Calculus','Probability','Applied projects'],viz:'line',vlabels:['Vectors','Calculus','Prob','ODE'],accent:'#fbbf24',hrs:77,mods:18},
 {code:'IL-21',title:'Humanities for Technologists',take:'Philosophy, history, and ethics for builders of the future.',steps:['Core readings','Argument drills','Ethics cases','Noah check-in'],viz:'grid',vlabels:['Philo','History','Ethics','Logic'],accent:'#c084fc',hrs:62,mods:17},
 {code:'IL-22',title:'The Deep Library — Esoteric & Secret Knowledge',take:"Sixty-eight hours inside humanity's hidden canon.",steps:['Canon map','Secret societies','Symbol systems','Noah check-in'],viz:'grid',vlabels:['Texts','Orders','Symbols','Rites'],accent:'#c084fc',hrs:68,mods:18},
 {code:'IL-23',title:'The Frontier — Cutting-Edge Research Distilled',take:'Breakthrough research, distilled to what matters.',steps:['Research radar','Key papers','Lab-grade explainers','Noah check-in'],viz:'radar',vlabels:['Papers','Labs','Breakthroughs','Signals'],accent:'#c084fc',hrs:67,mods:17},
 {code:'IL-24',title:'ThreatLocker Assessment Prep CBT',take:'ThreatLocker-ready: zero-trust endpoints, assessment drills.',steps:['Zero-trust model','ThreatLocker stack','Assessment drills','Noah check-in'],viz:'steps',vlabels:['Deny','Allow','Ringfence','Drill'],accent:'#ff6b6b',hrs:70,mods:16},
 {code:'IL-25',title:'Professional Cybersecurity Certificate Prep',take:'Independent cert prep that teaches the job, not just the test.',steps:['Domain review','Lab drills','Practice exams','Independent prep plan'],viz:'bars',vlabels:['Network','Crypto','Ops','Exam'],accent:'#ff6b6b',hrs:111,mods:27},
 {code:'IL-26',title:'Data Analyst Certification & Senior Mastery',take:'Analyst to senior: SQL, stats, and business judgment.',steps:['SQL & data','Statistics','Dashboards & story','Senior capstone'],viz:'bars',vlabels:['SQL','Stats','Viz','Story'],accent:'#4ade80',hrs:414,mods:54},
 {code:'IL-27',title:'IT Infrastructure Specialist — Zero Trust Infrastructure',take:'Zero-trust infrastructure, end to end — free and open.',steps:['Infra core','Zero-trust design','Hardening labs','Noah check-in'],viz:'flow',vlabels:['Identity','Segment','Harden','Monitor'],accent:'#ff6b6b',hrs:252,mods:56,free:true},
 {code:'IL-28',title:'DevSecOps & Cloud Infrastructure — Production Mastery',take:'Production-grade DevSecOps at cloud scale — free.',steps:['Pipeline mastery','Cloud infra','Security gates','Capstone ship'],viz:'steps',vlabels:['Build','Secure','Deploy','Run'],accent:'#6ba8ff',hrs:473,mods:52,free:true},
 {code:'IL-29',title:'ThreatLocker Zero-Trust CBT with AI — Cybersecurity Mastery',take:'ThreatLocker mastery with AI tutor — free and open.',steps:['Zero-trust core','AI-guided labs','Assessment drills','Noah check-in'],viz:'grid',vlabels:['Deny','Ringfence','Audit','Drill'],accent:'#ff6b6b',vizAccent:'#22ff88',hrs:431,mods:48,free:true},
 {code:'IL-30',title:'Post-Quantum Cryptography & Quantum-Safe Engineering',take:'Crypto that survives the quantum era.',steps:['Quantum threat','PQC algorithms','Migration plans','Noah check-in'],viz:'line',vlabels:['RSA','Lattice','Migrate','Verify'],accent:'#ff6b6b',hrs:165,mods:16},
 {code:'IL-31',title:'AI Red-Teaming & Safety Evals Engineering',take:'Break AI systems safely — then make them safer.',steps:['Threat models','Attack playbooks','Eval harnesses','Safety reports'],viz:'bars',vlabels:['Prompt','Jailbreak','Eval','Report'],accent:'#7fd4e8',hrs:100,mods:16}
];
var byCode = {};
PROGRAMS.forEach(function(p){ byCode[p.code] = p; });

var reduceMotion = (typeof window.matchMedia === 'function') &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------------- small helpers ---------------- */
function E(tag, attrs, parent){
  var el = document.createElement(tag);
  if(attrs) for(var k in attrs){
    if(k==='class') el.className = attrs[k];
    else if(k==='text') el.textContent = attrs[k];
    else el.setAttribute(k, attrs[k]);
  }
  if(parent) parent.appendChild(el);
  return el;
}
function mulberry(seed){
  var a = seed >>> 0;
  return function(){
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    var t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function hashStr(s){
  var h = 2166136261;
  for(var i=0;i<s.length;i++){ h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}
function hexA(hex, a){
  var r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
  return 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
}

/* ---------------- injected CSS (ilcc-* namespace only) ---------------- */
var CSS_ONCE = false;
function injectCSS(){
  if(CSS_ONCE) return; CSS_ONCE = true;
  var st = document.createElement('style');
  st.setAttribute('data-ilcc-css','1');
  st.textContent =
  '.ilcc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px;align-items:start;}' +
  '.ilcc-card{--ilcc-accent:' + ACCENT_DEFAULT + ';position:relative;display:flex;flex-direction:column;' +
    'width:100%;max-width:430px;margin:0 auto;aspect-ratio:9/16;overflow:hidden;border-radius:18px;' +
    'background:linear-gradient(180deg,#0b1220 0%,#070b14 60%,#05080f 100%);' +
    'border:1px solid rgba(148,163,184,.16);box-shadow:0 18px 50px rgba(0,0,0,.5);' +
    'color:#e8eef7;font-family:"Space Grotesk",Inter,system-ui,-apple-system,"Segoe UI",sans-serif;}' +
  '.ilcc-card::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:5;' +
    'background:radial-gradient(120% 60% at 50% 0%,var(--ilcc-accent) 0%,transparent 55%);opacity:.10;}' +
  '.ilcc-head{padding:14px 16px 6px;z-index:2;}' +
  '.ilcc-eyebrow{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:10.5px;' +
    'letter-spacing:.14em;color:var(--ilcc-accent);text-transform:uppercase;}' +
  '.ilcc-title{margin:6px 0 4px;font-size:24px;line-height:1.12;font-weight:800;letter-spacing:-.01em;color:#fff;}' +
  '.ilcc-take{margin:0 0 4px;font-size:12.5px;line-height:1.45;color:#aeb9cc;}' +
  '.ilcc-canvas-wrap{position:relative;flex:1 1 auto;min-height:0;margin:4px 12px 0;border-radius:12px;' +
    'background:rgba(2,6,14,.55);border:1px solid rgba(148,163,184,.12);overflow:hidden;z-index:2;}' +
  '.ilcc-canvas-wrap canvas{position:absolute;inset:0;width:100%;height:100%;display:block;}' +
  '.ilcc-live{position:absolute;top:8px;left:10px;z-index:3;display:flex;align-items:center;gap:6px;' +
    'font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:9.5px;letter-spacing:.12em;color:#9fb0c8;}' +
  '.ilcc-live i{width:7px;height:7px;border-radius:50%;background:#22ff88;box-shadow:0 0 8px #22ff88;animation:ilcc-blink 1.4s infinite;}' +
  '@keyframes ilcc-blink{0%,100%{opacity:1;}50%{opacity:.25;}}' +
  '.ilcc-steps{list-style:none;margin:8px 12px 0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:6px;z-index:2;}' +
  '.ilcc-pill{display:flex;align-items:center;gap:7px;padding:6px 8px;border-radius:9px;' +
    'font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:10.5px;line-height:1.3;color:#8b98ad;' +
    'background:rgba(148,163,184,.06);border:1px solid rgba(148,163,184,.14);' +
    'transition:color .25s,border-color .25s,background-color .25s,box-shadow .25s;}' +
  '.ilcc-pill b{flex:none;display:inline-flex;align-items:center;justify-content:center;width:17px;height:17px;' +
    'border-radius:50%;background:rgba(148,163,184,.15);color:#8b98ad;font-size:10px;font-weight:700;}' +
  '.ilcc-pill.on{color:#fff;border-color:var(--ilcc-accent);background:rgba(255,255,255,.05);' +
    'box-shadow:0 0 14px var(--ilcc-accent);}' +
  '.ilcc-pill.on b{background:var(--ilcc-accent);color:#04070d;}' +
  '.ilcc-ticker{display:flex;align-items:center;justify-content:center;gap:8px;margin:8px 12px 0;' +
    'font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;letter-spacing:.08em;color:#9fb0c8;z-index:2;}' +
  '.ilcc-ticker b{color:#fff;font-size:14px;min-width:3ch;display:inline-block;text-align:right;}' +
  '.ilcc-foot{display:flex;align-items:center;gap:8px;margin:8px 12px 0;z-index:2;}' +
  '.ilcc-price{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;font-weight:700;' +
    'padding:5px 10px;border-radius:999px;background:rgba(148,163,184,.1);border:1px solid rgba(148,163,184,.25);color:#dbe4f2;}' +
  '.ilcc-price.free{background:rgba(34,255,136,.12);border-color:rgba(34,255,136,.5);color:#4dff9d;}' +
  '.ilcc-noah{font-size:10px;padding:5px 10px;border-radius:999px;background:var(--ilcc-accent);color:#04070d;font-weight:800;}' +
  '.ilcc-cta{margin-left:auto;font-size:11.5px;font-weight:700;color:var(--ilcc-accent);text-decoration:none;white-space:nowrap;}' +
  '.ilcc-cta:hover{text-decoration:underline;}' +
  '.ilcc-vo{margin:10px 12px 0;padding:9px 12px;border-radius:10px;cursor:pointer;' +
    'border:1px solid var(--ilcc-accent);background:rgba(255,255,255,.04);color:#fff;' +
    'font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;font-weight:700;z-index:2;' +
    'transition:box-shadow .2s,background .2s;}' +
  '.ilcc-vo:hover{background:rgba(255,255,255,.08);}' +
  '.ilcc-vo.playing{box-shadow:0 0 16px var(--ilcc-accent);}' +
  '.ilcc-vo:focus-visible{outline:2px solid var(--ilcc-accent);outline-offset:2px;}' +
  '.ilcc-cap{margin:6px 14px 14px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;' +
    'font-size:10px;line-height:1.5;color:#6f7d94;z-index:2;}' +
  '.ilcc-cap strong{color:#9fb0c8;}';
  (document.head || document.documentElement).appendChild(st);
}

/* ---------------- viz implementations (canvas 2D motion graphics) ---------------- */
/* Each viz: init(p, W, H, rand) -> state; draw(ctx, W, H, lt, step, p, state). */
var VIZ = {
  bars: {
    init: function(p, W, H, rand){
      var s = [];
      for(var i=0;i<12;i++) s.push({base:.35+rand()*.3, amp:.12+rand()*.18, ph:rand()*6.28, sp:.8+rand()*1.4});
      return s;
    },
    draw: function(ctx, W, H, lt, step, p, s){
      var acc = p.accent, pad = 34, bw = (W - pad*2) / 12;
      ctx.strokeStyle = 'rgba(148,163,184,.12)'; ctx.lineWidth = 1;
      for(var g=0; g<4; g++){ var gy = pad + (H-pad*2)*g/3;
        ctx.beginPath(); ctx.moveTo(pad, gy); ctx.lineTo(W-pad, gy); ctx.stroke(); }
      for(var i=0;i<12;i++){
        var v = s[i].base + s[i].amp * Math.sin(lt*s[i].sp + s[i].ph) + s[i].amp*0.35*Math.sin(lt*2.7 + s[i].ph*2);
        v = Math.max(.04, Math.min(1, v));
        var bh = v * (H - pad*2);
        var x = pad + i*bw + bw*0.18, w = bw*0.64, y = H - pad - bh;
        var grd = ctx.createLinearGradient(0, y, 0, H-pad);
        grd.addColorStop(0, hexA(acc,.95)); grd.addColorStop(1, hexA(acc,.25));
        ctx.fillStyle = grd;
        ctx.fillRect(x, y, w, bh);
      }
      ctx.fillStyle = '#8b98ad'; ctx.font = '9px ui-monospace,monospace'; ctx.textAlign = 'center';
      for(var l=0;l<4;l++){ ctx.fillText(p.vlabels[l], pad + (W-pad*2)*(l+0.5)/4, H-8); }
      var live = Math.round(40 + 45*(0.5+0.5*Math.sin(lt*1.7)));
      ctx.textAlign = 'right'; ctx.fillStyle = hexA(acc,.95); ctx.font = 'bold 12px ui-monospace,monospace';
      ctx.fillText('LIVE ' + live + '%', W-10, 18);
    }
  },
  line: {
    init: function(p, W, H, rand){
      return [ {ph:rand()*6.28, sp:.5+rand()*.4, amp:.20+rand()*.15, off:0},
               {ph:rand()*6.28, sp:.6+rand()*.4, amp:.14+rand()*.12, off:.28},
               {ph:rand()*6.28, sp:.4+rand()*.4, amp:.10+rand()*.10, off:-.28} ];
    },
    draw: function(ctx, W, H, lt, step, p, s){
      var acc = p.accent, pad = 34, mid = pad + (H-pad*2)*0.55;
      ctx.strokeStyle = 'rgba(148,163,184,.12)'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(pad, pad); ctx.lineTo(pad, H-pad); ctx.lineTo(W-pad, H-pad); ctx.stroke();
      for(var i=0;i<3;i++){
        ctx.beginPath();
        for(var x=0;x<=W-pad*2;x+=4){
          var xx = pad + x;
          var y = mid + (H-pad*2)*s[i].off*0.4 - (H-pad*2)*s[i].amp*Math.sin(x*0.028 - lt*2*s[i].sp + s[i].ph)
                  - (H-pad*2)*0.05*Math.sin(x*0.09 - lt*4 + s[i].ph);
          if(x===0) ctx.moveTo(xx,y); else ctx.lineTo(xx,y);
        }
        ctx.strokeStyle = i===0 ? hexA(acc,.95) : hexA(acc,.35); ctx.lineWidth = i===0 ? 2 : 1.25;
        ctx.stroke();
      }
      /* scrolling cursor */
      var cx = pad + ((lt*40) % (W-pad*2));
      ctx.strokeStyle = hexA(acc,.5); ctx.setLineDash([3,4]);
      ctx.beginPath(); ctx.moveTo(cx,pad); ctx.lineTo(cx,H-pad); ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle = '#8b98ad'; ctx.font = '9px ui-monospace,monospace'; ctx.textAlign = 'center';
      for(var l=0;l<4;l++){ ctx.fillText(p.vlabels[l], pad + (W-pad*2)*(l+0.5)/4, pad-8); }
      var live = Math.round(1000 + 240*lt + 60*Math.sin(lt*2.2));
      ctx.textAlign = 'right'; ctx.fillStyle = hexA(acc,.95); ctx.font = 'bold 12px ui-monospace,monospace';
      ctx.fillText('SAMPLES ' + live, W-10, 18);
    }
  },
  flow: {
    init: function(p, W, H, rand){
      var parts = [];
      for(var i=0;i<26;i++) parts.push({e:Math.floor(rand()*3), u:rand(), sp:.12+rand()*.12});
      return parts;
    },
    draw: function(ctx, W, H, lt, step, p, parts){
      var acc = p.vizAccent || p.accent;
      var xs = [W*0.12, W*0.37, W*0.63, W*0.88], cy = H*0.46, R = 20;
      ctx.strokeStyle = 'rgba(148,163,184,.25)'; ctx.lineWidth = 2;
      for(var e=0;e<3;e++){
        ctx.beginPath(); ctx.moveTo(xs[e]+R, cy); ctx.lineTo(xs[e+1]-R, cy); ctx.stroke();
        ctx.fillStyle = 'rgba(148,163,184,.5)';
        ctx.beginPath(); ctx.moveTo(xs[e+1]-R-6, cy-4); ctx.lineTo(xs[e+1]-R, cy); ctx.lineTo(xs[e+1]-R-6, cy+4); ctx.closePath(); ctx.fill();
      }
      for(var i=0;i<parts.length;i++){
        var pt = parts[i], u = (pt.u + lt*pt.sp) % 1;
        var x = xs[pt.e] + (xs[pt.e+1]-xs[pt.e])*u, y = cy + 7*Math.sin(u*6.28 + lt*3);
        ctx.fillStyle = hexA(acc, .55+.45*Math.sin(u*6.28));
        ctx.beginPath(); ctx.arc(x, y, 2.6, 0, 6.29); ctx.fill();
      }
      for(var n=0;n<4;n++){
        var on = (n === step);
        var r = R + (on ? 4*Math.sin(lt*6) : 0);
        ctx.beginPath(); ctx.arc(xs[n], cy, r, 0, 6.29);
        ctx.fillStyle = on ? hexA(acc,.28) : 'rgba(10,17,32,.9)'; ctx.fill();
        ctx.strokeStyle = hexA(acc, on?1:.45); ctx.lineWidth = on?2.5:1.5; ctx.stroke();
        ctx.fillStyle = on ? '#fff' : '#8b98ad';
        ctx.font = 'bold 11px ui-monospace,monospace'; ctx.textAlign = 'center';
        ctx.fillText('N'+(n+1), xs[n], cy+4);
        ctx.fillStyle = '#8b98ad'; ctx.font = '9px ui-monospace,monospace';
        ctx.fillText(p.vlabels[n], xs[n], cy + R + 22);
      }
      var pkts = Math.round(12400 + lt*860 + 120*Math.sin(lt*3));
      ctx.textAlign = 'right'; ctx.fillStyle = hexA(acc,.95); ctx.font = 'bold 12px ui-monospace,monospace';
      ctx.fillText('PKTS ' + pkts.toLocaleString(), W-10, 18);
    }
  },
  steps: {
    init: function(){ return null; },
    draw: function(ctx, W, H, lt, step, p){
      var acc = p.accent, n = 4, pad = 20;
      var bw = (W - pad*2 - (n-1)*10) / n, bh = H*0.52, y0 = H*0.18;
      for(var i=0;i<n;i++){
        var x = pad + i*(bw+10);
        var on = (i === step), done = (i < step);
        ctx.fillStyle = on ? hexA(acc,.22) : done ? hexA(acc,.08) : 'rgba(10,17,32,.85)';
        ctx.strokeStyle = hexA(acc, on?1:(done?.6:.25)); ctx.lineWidth = on?2:1.25;
        ctx.beginPath();
        if(ctx.roundRect) ctx.roundRect(x, y0, bw, bh, 8); else ctx.rect(x, y0, bw, bh);
        ctx.fill(); ctx.stroke();
        ctx.fillStyle = on ? '#fff' : (done ? hexA(acc,.9) : '#5b6678');
        ctx.font = 'bold 13px ui-monospace,monospace'; ctx.textAlign = 'center';
        ctx.fillText((i+1), x + bw/2, y0 + 26);
        ctx.fillStyle = '#aeb9cc'; ctx.font = '9px ui-monospace,monospace';
        var words = p.vlabels[i].split(' ');
        for(var wl=0; wl<Math.min(2,words.length); wl++)
          ctx.fillText(words[wl], x + bw/2, y0 + 44 + wl*12);
        /* progress bar in active stage */
        if(on){
          var frac = (lt % (LOOP/4)) / (LOOP/4);
          ctx.fillStyle = 'rgba(148,163,184,.2)';
          ctx.fillRect(x+8, y0+bh-16, bw-16, 5);
          ctx.fillStyle = acc;
          ctx.fillRect(x+8, y0+bh-16, (bw-16)*frac, 5);
        } else if(done){
          ctx.fillStyle = hexA(acc,.8);
          ctx.fillRect(x+8, y0+bh-16, bw-16, 5);
        }
        if(i < n-1){
          ctx.strokeStyle = hexA(acc,.35); ctx.lineWidth = 2;
          var ax = x + bw, bx = x + bw + 10;
          ctx.beginPath(); ctx.moveTo(ax, y0+bh/2); ctx.lineTo(bx, y0+bh/2); ctx.stroke();
          ctx.fillStyle = hexA(acc,.6);
          ctx.beginPath(); ctx.moveTo(bx-5, y0+bh/2-4); ctx.lineTo(bx, y0+bh/2); ctx.lineTo(bx-5, y0+bh/2+4); ctx.closePath(); ctx.fill();
        }
      }
      ctx.textAlign = 'right'; ctx.fillStyle = hexA(acc,.95); ctx.font = 'bold 12px ui-monospace,monospace';
      ctx.fillText('STAGE ' + (step+1) + '/4', W-10, 18);
    }
  },
  radar: {
    init: function(p, W, H, rand){
      var blips = [];
      for(var i=0;i<14;i++) blips.push({a:rand()*6.28, r:.18+rand()*.68, sz:2+rand()*3, tw:rand()*6.28});
      return blips;
    },
    draw: function(ctx, W, H, lt, step, p, blips){
      var acc = p.accent, cx = W/2, cy = H*0.52, R = Math.min(W,H)*0.36;
      ctx.strokeStyle = 'rgba(148,163,184,.16)'; ctx.lineWidth = 1;
      for(var r=1;r<=4;r++){ ctx.beginPath(); ctx.arc(cx, cy, R*r/4, 0, 6.29); ctx.stroke(); }
      ctx.beginPath(); ctx.moveTo(cx-R, cy); ctx.lineTo(cx+R, cy);
      ctx.moveTo(cx, cy-R); ctx.lineTo(cx, cy+R); ctx.stroke();
      var sweep = (lt/LOOP)*6.2832 - 1.5708;
      /* trail */
      for(var k=40;k>0;k--){
        var a0 = sweep - k*0.02;
        ctx.strokeStyle = hexA(acc, 0.35*(1-k/40));
        ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.moveTo(cx, cy);
        ctx.lineTo(cx + Math.cos(a0)*R, cy + Math.sin(a0)*R); ctx.stroke();
      }
      ctx.strokeStyle = hexA(acc,.95); ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + Math.cos(sweep)*R, cy + Math.sin(sweep)*R); ctx.stroke();
      /* blips */
      for(var i=0;i<blips.length;i++){
        var b = blips[i], bx = cx + Math.cos(b.a)*R*b.r, by = cy + Math.sin(b.a)*R*b.r;
        var d = Math.abs(((sweep - b.a) % 6.2832 + 6.2832) % 6.2832);
        var glow = Math.max(0, 1 - d/1.2);
        var tw = 0.5 + 0.5*Math.sin(lt*3 + b.tw);
        ctx.fillStyle = hexA(acc, 0.25 + 0.75*Math.max(glow, tw*0.4));
        ctx.beginPath(); ctx.arc(bx, by, b.sz + glow*2, 0, 6.29); ctx.fill();
      }
      ctx.fillStyle = '#8b98ad'; ctx.font = '9px ui-monospace,monospace'; ctx.textAlign = 'center';
      ctx.fillText(p.vlabels[0], cx, cy - R - 8);
      ctx.fillText(p.vlabels[1], cx + R + 6, cy + 3);
      ctx.fillText(p.vlabels[2], cx, cy + R + 14);
      ctx.fillText(p.vlabels[3], cx - R - 6, cy + 3);
      var hits = Math.round(3 + 9*(0.5+0.5*Math.sin(lt*1.3)));
      ctx.textAlign = 'right'; ctx.fillStyle = hexA(acc,.95); ctx.font = 'bold 12px ui-monospace,monospace';
      ctx.fillText('HITS ' + hits, W-10, 18);
    }
  },
  grid: {
    init: function(p, W, H, rand){
      var hot = [];
      for(var i=0;i<9;i++) hot.push({x:Math.floor(rand()*10), y:Math.floor(rand()*6)});
      return hot;
    },
    draw: function(ctx, W, H, lt, step, p, hot){
      var acc = p.vizAccent || p.accent;
      var cols = 10, rows = 6, pad = 26;
      var cw = (W - pad*2)/cols, ch = (H - pad*2 - 18)/rows;
      var isHot = {};
      for(var h=0;h<hot.length;h++) isHot[hot[h].x+','+hot[h].y] = 1;
      for(var x=0;x<cols;x++) for(var y=0;y<rows;y++){
        var wave = Math.sin(lt*2.1 - (x+y)*0.72);
        var base = wave > 0.35 ? 0.75 : (wave > -0.2 ? 0.28 : 0.08);
        var a = isHot[x+','+y] ? Math.max(base, 0.55 + 0.4*Math.sin(lt*4 + x)) : base;
        ctx.fillStyle = hexA(acc, a);
        ctx.fillRect(pad + x*cw + 1.5, pad + y*ch + 1.5, cw - 3, ch - 3);
      }
      ctx.fillStyle = '#8b98ad'; ctx.font = '9px ui-monospace,monospace'; ctx.textAlign = 'center';
      for(var l=0;l<4;l++){ ctx.fillText(p.vlabels[l], pad + (W-pad*2)*(l+0.5)/4, H-6); }
      var ops = Math.round(900 + 320*(0.5+0.5*Math.sin(lt*1.9)));
      ctx.textAlign = 'right'; ctx.fillStyle = hexA(acc,.95); ctx.font = 'bold 12px ui-monospace,monospace';
      ctx.fillText('OPS ' + ops, W-10, 18);
    }
  }
};

/* ---------------- Noah TTS (same /api/noah/tts pattern as il-algo-viz.js) ---------------- */
function voScript(p){
  var s = p.take;
  for(var i=0;i<4;i++) s += ' Step ' + (i+1) + ': ' + p.steps[i] + '.';
  return s;
}
var TTS_GLYPH = '▶';
function wireTTS(btn, m){
  btn.addEventListener('click', function(){
    if(m.audio){ try{ m.audio.pause(); }catch(e){} m.audio = null; btn.classList.remove('playing'); btn.textContent = TTS_GLYPH + ' Noah voiceover'; return; }
    btn.classList.add('playing'); btn.textContent = '■ Stop voiceover';
    fetch('/api/noah/tts', {method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({text: voScript(m.p), voice:'narrator'})})
    .then(function(r){
      if(!r.ok) throw new Error('tts http ' + r.status);
      var ct = (r.headers.get('content-type') || '').toLowerCase();
      if(ct.indexOf('audio') === 0) return r.blob().then(function(b){ return URL.createObjectURL(b); });
      return r.json().then(function(j){ if(j && j.url) return j.url; throw new Error('tts: no audio url'); });
    })
    .then(function(url){
      var a = new Audio(url); m.audio = a;
      var done = function(){ try{ URL.revokeObjectURL(url); }catch(e){} m.audio = null;
        btn.classList.remove('playing'); btn.textContent = TTS_GLYPH + ' Noah voiceover'; };
      a.onended = done;
      a.onerror = done;
      var pr = a.play();
      if(pr && pr.catch) pr.catch(function(){ done(); });
    })
    .catch(function(){ m.audio = null; btn.classList.remove('playing'); btn.textContent = TTS_GLYPH + ' Noah voiceover'; });
  });
}

/* ---------------- mount lifecycle ---------------- */
var mounts = [];
var io = null;

function activeStep(t){
  return Math.min(3, Math.floor(((t % LOOP) + LOOP) % LOOP / LOOP * 4));
}
function paintSteps(m){
  if(!m.pills || !m.pills.length) return;
  var si = activeStep(m.t);
  if(si === m.stepIdx) return;
  m.stepIdx = si;
  for(var i=0;i<m.pills.length;i++) m.pills[i].classList.toggle('on', i === si);
}
function fitCanvas(m){
  var w = m.wrap.clientWidth, h = m.wrap.clientHeight;
  if(!w || !h) return false;
  var dpr = Math.min(2, window.devicePixelRatio || 1);
  var bw = Math.round(w*dpr), bh = Math.round(h*dpr);
  if(m.cv.width !== bw || m.cv.height !== bh){ m.cv.width = bw; m.cv.height = bh; }
  m.W = w; m.H = h; m.dpr = dpr;
  return true;
}
function drawFrame(m){
  if(!fitCanvas(m)) return;
  var ctx = m.cv.getContext('2d');
  ctx.setTransform(m.dpr, 0, 0, m.dpr, 0, 0);
  ctx.clearRect(0, 0, m.W, m.H);
  try{
    m.viz.draw(ctx, m.W, m.H, m.t % LOOP, m.stepIdx < 0 ? activeStep(m.t) : m.stepIdx, m.p, m.vstate);
  }catch(e){}
}

function buildCard(p){
  var card = E('article', {'class':'ilcc-card', 'aria-label': p.code + ' ' + p.title});
  card.style.setProperty('--ilcc-accent', p.accent);

  var head = E('div', {'class':'ilcc-head'}, card);
  E('div', {'class':'ilcc-eyebrow', 'text':'Interstitium Labs · ' + p.code}, head);
  E('h3', {'class':'ilcc-title', 'text': p.title}, head);
  E('p', {'class':'ilcc-take', 'text': p.take}, head);

  var wrap = E('div', {'class':'ilcc-canvas-wrap'}, card);
  E('div', {'class':'ilcc-live', 'text':''}, wrap).innerHTML = '<i></i>LIVE SIM';
  var cv = E('canvas', {'class':'ilcc-canvas', 'aria-hidden':'true'}, wrap);

  var ol = E('ol', {'class':'ilcc-steps'}, card);
  var pills = p.steps.map(function(s, i){
    var li = E('li', {'class':'ilcc-pill'}, ol);
    E('b', {'text': String(i+1)}, li);
    E('span', {'text': s}, li);
    return li;
  });

  var ticker = E('div', {'class':'ilcc-ticker'}, card);
  var hNum = E('b', {'text':'0'}, ticker);
  ticker.appendChild(document.createTextNode(' HRS · '));
  var mNum = E('b', {'text':'0'}, ticker);
  ticker.appendChild(document.createTextNode(' MODULES'));

  var foot = E('div', {'class':'ilcc-foot'}, card);
  var price = E('span', {'class':'ilcc-price' + (p.free ? ' free' : ''), 'text': p.free ? 'FREE' : '$249'}, foot);
  price.title = p.free ? 'Free and open' : '$249 · $999 all-access bundle';
  E('span', {'class':'ilcc-noah', 'text':'Noah-tutored'}, foot);
  E('a', {'class':'ilcc-cta', 'href':'/university/academy?id=' + p.code, 'text':'Open course →'}, foot);

  var btn = E('button', {'class':'ilcc-vo', 'type':'button', 'text': TTS_GLYPH + ' Noah voiceover'}, card);
  btn.setAttribute('aria-label', 'Play Noah voiceover for ' + p.code);
  var cap = E('p', {'class':'ilcc-cap'}, card);
  E('strong', {'text':'VO script: '}, cap);
  cap.appendChild(document.createTextNode(voScript(p)));

  var vizDef = VIZ[p.viz];
  var rand = mulberry(hashStr(p.code));
  var m = { card:card, p:p, cv:cv, wrap:wrap, pills:pills, viz:vizDef,
            vstate: vizDef.init(p, 300, 220, rand), t: (hashStr(p.code) % 1500) / 100,
            stepIdx:-1, visible:false, audio:null, hNum:hNum, mNum:mNum, W:0, H:0, dpr:1 };
  wireTTS(btn, m);
  mounts.push(m);
  return { card:card, m:m };
}

function paintTicker(m){
  var lt = ((m.t % LOOP) + LOOP) % LOOP;
  var f = Math.min(1, lt / 2.5);
  /* ease-out */
  f = 1 - (1-f)*(1-f);
  m.hNum.textContent = String(Math.round(m.p.hrs * f));
  m.mNum.textContent = String(Math.round(m.p.mods * f));
}

function render(container, code){
  var el = (typeof container === 'string') ? document.querySelector(container) : container;
  if(!el) return null;
  var p = byCode[code];
  if(!p) return null;
  injectCSS();
  var built = buildCard(p);
  el.appendChild(built.card);
  var m = built.m;
  if(reduceMotion){
    m.t = 3.2; m.stepIdx = -1;
    drawFrame(m); paintTicker(m);
  } else if(io){
    io.observe(built.card);
  } else {
    m.visible = true;
  }
  paintSteps(m);
  return built.card;
}

function renderAll(container, codes){
  var el = (typeof container === 'string') ? document.querySelector(container) : container;
  if(!el) return null;
  injectCSS();
  el.classList.add('ilcc-grid');
  var list = codes && codes.length ? codes : PROGRAMS.map(function(p){ return p.code; });
  var out = [];
  for(var i=0;i<list.length;i++){
    var c = render(el, list[i]);
    if(c) out.push(c);
  }
  return out;
}

/* ---------------- visibility + global tick ---------------- */
function boot(){
  if('IntersectionObserver' in window){
    io = new IntersectionObserver(function(es){
      es.forEach(function(e){
        for(var i=0;i<mounts.length;i++){
          if(mounts[i].card === e.target){ mounts[i].visible = e.isIntersecting; break; }
        }
      });
    }, {threshold: 0.2, rootMargin: '60px'});
    /* observe any cards already in DOM */
    for(var i=0;i<mounts.length;i++) io.observe(mounts[i].card);
  } else {
    for(var j=0;j<mounts.length;j++) mounts[j].visible = true;
  }
  if(reduceMotion) return;
  var last = 0;
  (function tick(now){
    var t = now / 1000;
    var dt = Math.min(0.06, last ? t - last : 0.016);
    last = t;
    for(var k=0;k<mounts.length;k++){
      var m = mounts[k];
      if(m.visible && m.viz){
        m.t += dt;
        drawFrame(m); paintSteps(m); paintTicker(m);
      }
    }
    requestAnimationFrame(tick);
  })(0);
}

window.ILCineCards = {
  render: render,
  renderAll: renderAll,
  PROGRAMS: PROGRAMS,
  LOOP: LOOP
};

if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
else boot();
})();
