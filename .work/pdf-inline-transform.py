#!/usr/bin/env python3
"""PDF library ANIMATED inline-preview buildout (2026-10-09, rev 2).
Per user correction: previews must be ANIMATED and DYNAMIC, not static.

Transforms every .pdf-card in docs/pdf-library/index.html:
  - adds a .pdf-preview block: ONE iframe per card showing the PDF,
    auto-cycling pages 1-4 on a 2.5s timer with a fade transition
    (the "step-through animation" feel the guides were designed for)
  - only ONE card animates at a time: the most-visible preview in the
    viewport (IntersectionObserver + ratio map); others hold their page
  - iframes lazy-load src via a second IntersectionObserver (data-src)
  - Expand button opens the full PDF in an inline modal (no new tab)
  - secondary Download link per card; live search box; TOC untouched
Run: python3 this_file.py
"""
import re
import shutil
import html as htmlmod

SRC = '/home/hatch/workspace/apex-audit/docs/pdf-library/index.html'
BAK = '/home/hatch/workspace/apex-audit/.work/pdf-library-index.html.bak-20261009'

t = open(SRC, encoding='utf-8').read()

card_re = re.compile(
    r'<div class="pdf-card"><span class="pdf-cat">(.*?)</span><h3>(.*?)</h3><p>(.*?)</p>'
    r'<a class="btn" href="(/assets/pdfs/[^"]+\.pdf)">Read the guide</a>'
    r'<div class="pdf-meta">(.*?)</div></div>'
)


def repl(m):
    cat, title, desc, url, meta = m.groups()
    title_attr = htmlmod.escape(htmlmod.unescape(title), quote=True)
    preview = (
        '<div class="pdf-preview" data-pdf="' + url + '">'
        '<iframe class="pdf-frame" data-src="' + url + '#page=1&amp;toolbar=0&amp;navpanes=0" '
        'loading="lazy" title="Animated preview: ' + title_attr + '"></iframe>'
        '<button class="pdf-expand" type="button">&#x2922; Expand</button>'
        '<span class="pdf-live" aria-hidden="true"></span>'
        '<div class="pdf-pager"><span class="on">1</span><span>2</span><span>3</span><span>4</span></div>'
        '</div>'
    )
    actions = (
        '<div class="pdf-actions">'
        '<a class="btn" href="' + url + '">Read the guide</a>'
        '<a class="pdf-dl" href="' + url + '" download>Download</a>'
        '</div>'
    )
    return (
        '<div class="pdf-card"><span class="pdf-cat">' + cat + '</span><h3>' + title + '</h3><p>' + desc + '</p>'
        + preview + actions
        + '<div class="pdf-meta">' + meta + '</div></div>'
    )


t2, n = card_re.subn(repl, t)
print('cards transformed:', n)
assert n == 241, 'expected 241 cards, got %d' % n

# --- search box + lede update after the lede paragraph ---
lede_old = '241 guides, free to read, no sign-in.</p>'
lede_new = ('241 guides, free to read, no sign-in. Every card auto-plays an animated preview of the guide '
            'inline — scroll to load, or hit Expand to read the full PDF without leaving the page.</p>\n'
            '<input id="pdf-search" type="search" placeholder="Search the guides — e.g. consensus, B-trees, OAuth">')
assert lede_old in t2
t2 = t2.replace(lede_old, lede_new)

# --- CSS additions ---
css_add = """
.pdf-preview{position:relative;margin:.75rem 0;border:1px solid rgba(255,255,255,.12);border-radius:10px;overflow:hidden;background:#fff}
.pdf-frame{display:block;width:100%;height:280px;border:0;background:#fff;transition:opacity .28s ease}
.pdf-frame.fading{opacity:0}
.pdf-expand{position:absolute;top:.5rem;right:.5rem;padding:.35rem .7rem;border-radius:8px;border:1px solid rgba(255,255,255,.25);background:rgba(13,16,32,.88);color:#fff;font-size:.8rem;font-weight:600;cursor:pointer}
.pdf-expand:hover{background:#4361ee}
.pdf-live{position:absolute;top:.65rem;left:.65rem;width:.6rem;height:.6rem;border-radius:50%;background:#22c55e;display:none}
.pdf-preview.cycling .pdf-live{display:block;animation:pdfpulse 2s infinite}
@keyframes pdfpulse{0%{box-shadow:0 0 0 0 rgba(34,197,94,.55)}70%{box-shadow:0 0 0 8px rgba(34,197,94,0)}100%{box-shadow:0 0 0 0 rgba(34,197,94,0)}}
.pdf-pager{position:absolute;bottom:.5rem;left:.6rem;display:flex;gap:.35rem}
.pdf-pager span{width:1.35rem;height:1.35rem;border-radius:50%;background:rgba(13,16,32,.75);color:#cfd6ff;font-size:.68rem;font-weight:700;display:flex;align-items:center;justify-content:center;cursor:pointer;border:1px solid rgba(255,255,255,.2)}
.pdf-pager span.on{background:#4361ee;color:#fff}
.pdf-actions{display:flex;gap:.75rem;align-items:center;flex-wrap:wrap;margin:.5rem 0 .25rem}
.pdf-card a.pdf-dl{font-size:.85rem;color:#8b9cf0;text-decoration:none}
.pdf-card a.pdf-dl:hover{text-decoration:underline}
#pdf-search{width:100%;max-width:520px;padding:.7rem 1rem;border-radius:10px;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.04);color:#fff;font-size:1rem;margin:1.25rem 0 0}
#pdf-search::placeholder{color:#6b7280}
#pdf-modal{position:fixed;inset:0;z-index:1000}
#pdf-modal[hidden]{display:none}
.pdf-modal-backdrop{position:absolute;inset:0;background:rgba(0,0,0,.78)}
.pdf-modal-inner{position:relative;width:94%;max-width:1024px;height:92vh;margin:4vh auto;background:#10132a;border:1px solid rgba(255,255,255,.15);border-radius:12px;overflow:hidden;display:flex;flex-direction:column}
.pdf-modal-bar{display:flex;align-items:center;gap:.6rem;padding:.55rem .8rem;border-bottom:1px solid rgba(255,255,255,.1)}
#pdf-modal-title{flex:1;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pdf-modal-btn{padding:.4rem .8rem;border-radius:8px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.06);color:#fff;font-size:.85rem;cursor:pointer;text-decoration:none}
.pdf-modal-btn:hover{background:#4361ee}
#pdf-modal-frame{flex:1;width:100%;border:0;background:#fff}
@media(max-width:640px){.pdf-modal-inner{width:97%;height:96vh;margin:2vh auto}.pdf-frame{height:240px}}
"""
assert '</style>' in t2
t2 = t2.replace('</style>', css_add + '</style>')

# --- modal + JS before </body> ---
modal_js = """
<div id="pdf-modal" role="dialog" aria-modal="true" aria-labelledby="pdf-modal-title" hidden>
<div class="pdf-modal-backdrop" data-close="1"></div>
<div class="pdf-modal-inner">
<div class="pdf-modal-bar">
<span id="pdf-modal-title"></span>
<a id="pdf-modal-dl" class="pdf-modal-btn" href="#" download>Download</a>
<button id="pdf-modal-close" class="pdf-modal-btn" type="button">&#x2715; Close</button>
</div>
<iframe id="pdf-modal-frame" title="Full guide viewer" loading="lazy"></iframe>
</div>
</div>
<script>
(function(){
"use strict";
var CYCLE_PAGES=4, CYCLE_MS=2500;
var previews=Array.prototype.slice.call(document.querySelectorAll(".pdf-preview"));
var frames=previews.map(function(p){return p.querySelector("iframe.pdf-frame");});
function loadFrame(f){var u=f.getAttribute("data-src");if(u){f.setAttribute("src",u);f.removeAttribute("data-src");}}
/* 1. lazy first-page load: src only set near the viewport */
if("IntersectionObserver" in window){
var lazyIO=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){loadFrame(e.target);lazyIO.unobserve(e.target);}});},{rootMargin:"400px 0px"});
frames.forEach(function(f){lazyIO.observe(f);});
}else{frames.forEach(loadFrame);}
/* 2. animated page-cycling: only the most-visible card animates */
var pageIdx={}, active=null, timer=null, ratios=new Map();
function swapTo(p,n){
var key=p.getAttribute("data-pdf");
var f=p.querySelector("iframe.pdf-frame");
var dots=p.querySelectorAll(".pdf-pager span");
pageIdx[key]=n;
f.classList.add("fading");
var done=false;
function show(){if(done){return;}done=true;f.classList.remove("fading");}
f.addEventListener("load",show,{once:true});
setTimeout(show,2000);
setTimeout(function(){
f.setAttribute("src",key+"#page="+n+"&toolbar=0&navpanes=0");
dots.forEach(function(d,i){d.className=(i===n-1)?"on":"";});
},280);
}
function makeActive(p){
if(active===p){return;}
if(active){active.classList.remove("cycling");}
active=p;
if(timer){clearInterval(timer);timer=null;}
if(!p){return;}
p.classList.add("cycling");
var key=p.getAttribute("data-pdf");
loadFrame(p.querySelector("iframe.pdf-frame"));
if(!(pageIdx[key]>=1)){pageIdx[key]=1;}
timer=setInterval(function(){
if(document.hidden){return;}
var n=(pageIdx[key]%CYCLE_PAGES)+1;
swapTo(p,n);
},CYCLE_MS);
}
if("IntersectionObserver" in window){
var visIO=new IntersectionObserver(function(es){
es.forEach(function(e){ratios.set(e.target,e.isIntersecting?e.intersectionRatio:0);});
var best=null,bestR=0.3;
ratios.forEach(function(r,pl){if(r>bestR){best=pl;bestR=r;}});
makeActive(best);
},{threshold:[0,0.3,0.6,1]});
previews.forEach(function(p){visIO.observe(p);});
}
document.addEventListener("visibilitychange",function(){
if(document.hidden){if(timer){clearInterval(timer);timer=null;}}
else if(active){var p=active;active=null;makeActive(p);}
});
/* 3. expand modal: full PDF inline, no new tab */
var modal=document.getElementById("pdf-modal"),
mframe=document.getElementById("pdf-modal-frame"),
mtitle=document.getElementById("pdf-modal-title"),
mdl=document.getElementById("pdf-modal-dl");
function openModal(url,name){mtitle.textContent=name;mdl.href=url;mframe.setAttribute("src",url+"#page=1");modal.hidden=false;document.body.style.overflow="hidden";}
function closeModal(){mframe.setAttribute("src","about:blank");modal.hidden=true;document.body.style.overflow="";}
document.addEventListener("click",function(e){
var t=e.target;
if(!(t&&t.closest)){return;}
var pg=t.closest(".pdf-pager span");
if(pg){
var pv=pg.closest(".pdf-preview");
var idx=Array.prototype.indexOf.call(pv.querySelectorAll(".pdf-pager span"),pg);
swapTo(pv,idx+1);
if(active===pv){var key=pv.getAttribute("data-pdf");pageIdx[key]=idx+1;}
return;
}
var b=t.closest(".pdf-expand");
if(b){
var pv2=b.closest(".pdf-preview");
var card=b.closest(".pdf-card");
var h=card?card.querySelector("h3"):null;
openModal(pv2.getAttribute("data-pdf"),h?h.textContent:"Guide");
return;
}
if(t.closest("#pdf-modal-close")||t.closest("[data-close]")){closeModal();}
});
document.addEventListener("keydown",function(e){if(e.key==="Escape"&&!modal.hidden){closeModal();}});
/* 4. live search across cards, categories, descriptions */
var q=document.getElementById("pdf-search");
if(q){q.addEventListener("input",function(){
var s=q.value.trim().toLowerCase();
document.querySelectorAll(".pdf-grid").forEach(function(g){
var any=false;
g.querySelectorAll(".pdf-card").forEach(function(c){
var show=!s||c.textContent.toLowerCase().indexOf(s)>-1;
c.style.display=show?"":"none";if(show){any=true;}
});
g.style.display=any?"":"none";
var h=g.previousElementSibling;
if(h&&h.tagName==="H2"){h.style.display=any?"":"none";}
});
});}
})();
</script>
"""
assert '</body>' in t2
t2 = t2.replace('</body>', modal_js + '\n</body>')

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(t2)

# --- validate ---
out = open(SRC, encoding='utf-8').read()
checks = {
    'pdf-card count': out.count('class="pdf-card"'),
    'data-src iframes': out.count('data-src="'),
    'pdf-preview blocks': out.count('class="pdf-preview"'),
    'expand buttons': out.count('class="pdf-expand"'),
    'pager dot groups': out.count('class="pdf-pager"'),
    'download links': out.count('class="pdf-dl"'),
}
for k, v in checks.items():
    print('%-18s: %d' % (k, v))
print('modal present     :', 'id="pdf-modal"' in out)
print('cycle JS present  :', 'CYCLE_PAGES' in out and 'makeActive' in out)
print('search present    :', 'id="pdf-search"' in out)
print('ends with </html> :', out.rstrip().endswith('</html>'))
assert checks['pdf-card count'] == 241
assert checks['data-src iframes'] == 241
assert checks['pdf-preview blocks'] == 241
assert checks['expand buttons'] == 241
assert checks['pager dot groups'] == 241
assert checks['download links'] == 241
assert '_t.pdf' not in out
print('OK')
