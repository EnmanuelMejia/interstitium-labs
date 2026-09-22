(function(g){'use strict';
var ROWS=[
{dim:'Hosted lab / playground fleet',il:'LOSE',note:'One SuperLab + CotD — not 800 VMs',kk:'WIN',br:'TIE',al:'LOSE',aws:'WIN'},
{dim:'Adaptive placement + fringe',il:'WIN',note:'Local CAT + ALEKS-style fringe',kk:'TIE',br:'TIE',al:'WIN',aws:'TIE'},
{dim:'Interaction / lesson craft',il:'TIE',note:'Brilliant still denser',kk:'TIE',br:'WIN',al:'TIE',aws:'TIE'},
{dim:'In-lab live AI / Muse',il:'TIE',note:'Lab Muse + router shipped; no fake keys',kk:'WIN',br:'TIE',al:'LOSE',aws:'TIE'},
{dim:'Official certs / proctoring',il:'LOSE',note:'Vendor-map orchestrates',kk:'TIE',br:'LOSE',al:'TIE',aws:'WIN'},
{dim:'Portfolio honesty / proof',il:'WIN',note:'Labeled portfolio; no fake employment',kk:'TIE',br:'LOSE',al:'LOSE',aws:'LOSE'},
{dim:'Offline / inspectable static OS',il:'WIN',note:'Browser-local; CSP-first',kk:'LOSE',br:'LOSE',al:'LOSE',aws:'LOSE'},
{dim:'Career-changer JD → STAR path',il:'WIN',note:'Founders + Prep + exceed paths',kk:'TIE',br:'LOSE',al:'LOSE',aws:'TIE'},
{dim:'Commerce / enroll polish',il:'LOSE',note:'Placeholder payments by design',kk:'WIN',br:'WIN',al:'WIN',aws:'WIN'},
{dim:'Community / forums',il:'LOSE',note:'Not productized — do not fake',kk:'WIN',br:'TIE',al:'LOSE',aws:'TIE'}
];
function badge(v){var c=v==='WIN'?'is-win':v==='LOSE'?'is-lose':'is-tie';return '<span class="il-mx-badge '+c+'">'+v+'</span>';}
function paint(root){var h='<p class="il-kicker">Honest matrix · peers</p><h2 class="mt-2 font-display text-2xl tracking-[-0.02em]">Where we win. Where we lose. No wallpaper.</h2><p class="mt-3 max-w-2xl text-sm text-muted">vs KodeKloud (KK), Brilliant (BR), ALEKS (AL), AWS Skill Builder (AWS).</p><div class="il-mx-scroll mt-6"><table class="il-mx-table"><thead><tr><th>Dimension</th><th>IL</th><th>KK</th><th>BR</th><th>AL</th><th>AWS</th><th>Note</th></tr></thead><tbody>';
ROWS.forEach(function(r){h+='<tr><td class="il-mx-dim">'+r.dim+'</td><td>'+badge(r.il)+'</td><td>'+badge(r.kk)+'</td><td>'+badge(r.br)+'</td><td>'+badge(r.al)+'</td><td>'+badge(r.aws)+'</td><td class="il-mx-note">'+r.note+'</td></tr>';});
h+='</tbody></table></div><p class="mt-4 text-sm text-muted"><a class="text-cyan" href="/paths/">Paths</a> · <a class="text-cyan" href="/ops/MUSK-BAR-RECURSIVE.md">Musk bar</a> · <a class="text-cyan" href="/trending/">Trending</a></p>';root.className='il-peer-matrix';root.innerHTML=h;}
function boot(){document.querySelectorAll('[data-il-peer-matrix]').forEach(paint);}
g.ILPeerMatrix={boot:boot};if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})(typeof window!=='undefined'?window:this);