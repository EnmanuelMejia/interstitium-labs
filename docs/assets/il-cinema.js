/* Interstitium Labs — Cinema player logic. External file so the page CSP (script-src 'self', no unsafe-inline) allows it. */
(function(){
  var video = document.getElementById('cinema-video');
  var stage = document.getElementById('cinema-stage');
  var fsBtn = document.getElementById('cinema-fs');
  var soundBtn = document.getElementById('cinema-sound');
  var titleEl = document.getElementById('cinema-title');
  var descEl = document.getElementById('cinema-desc');
  if(!video || !stage) return;
  /* TikTok-style muted autoplay preview (2026-10-09 standard):
     plays when scrolled into view, pauses when out; tap unmutes + controls.
     prefers-reduced-motion => poster + native controls, no autoplay. */
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function setSoundLabel(){
    if(!soundBtn) return;
    soundBtn.textContent = video.muted ? 'Sound: off' : 'Sound: on';
    soundBtn.setAttribute('aria-pressed', video.muted ? 'false' : 'true');
  }
  function unmuteCinema(){
    if(video.muted){
      video.muted = false;
      video.setAttribute('controls','');
      if(video.paused) video.play().catch(function(){});
      setSoundLabel();
    }
  }
  function toggleSound(){
    video.muted = !video.muted;
    if(!video.muted){
      video.setAttribute('controls','');
      if(video.paused) video.play().catch(function(){});
    }
    setSoundLabel();
  }
  if(soundBtn){
    soundBtn.addEventListener('click', toggleSound);
    setSoundLabel();
  }
  if(reduced){
    video.setAttribute('controls','');
    video.muted = false;
    video.removeAttribute('autoplay');
  } else {
    video.addEventListener('click', unmuteCinema);
    if('IntersectionObserver' in window){
      new IntersectionObserver(function(entries){
        entries.forEach(function(en){
          if(en.isIntersecting){ if(video.paused) video.play().catch(function(){}); }
          else video.pause();
        });
      }, {rootMargin: '200px 0px', threshold: 0.1}).observe(stage);
    } else if(video.paused){
      video.play().catch(function(){});
    }
  }
  function setFsLabel(){
    var fs = document.fullscreenElement === stage;
    fsBtn.textContent = fs ? 'Exit fullscreen' : 'Enter fullscreen';
    fsBtn.setAttribute('aria-pressed', fs ? 'true' : 'false');
  }
  function toggleFs(){
    if(document.fullscreenElement === stage){
      if(document.exitFullscreen) document.exitFullscreen();
    } else if(stage.requestFullscreen){
      stage.requestFullscreen();
    } else if(video.webkitEnterFullscreen){
      video.webkitEnterFullscreen();
    }
  }
  if(fsBtn){
    fsBtn.addEventListener('click', toggleFs);
  }
  video.addEventListener('dblclick', toggleFs);
  document.addEventListener('fullscreenchange', setFsLabel);
  var items = document.querySelectorAll('.il-cinema-item');
  items.forEach(function(btn){
    btn.addEventListener('click', function(){
      items.forEach(function(b){ b.setAttribute('aria-current','false'); });
      btn.setAttribute('aria-current','true');
      video.pause();
      var src = video.querySelector('source');
      src.setAttribute('src', btn.getAttribute('data-src'));
      video.setAttribute('poster', btn.getAttribute('data-poster'));
      if(titleEl) titleEl.textContent = btn.getAttribute('data-title');
      if(descEl) descEl.innerHTML = btn.getAttribute('data-desc');
      if(!reduced){ video.muted = true; video.removeAttribute('controls'); }
      setSoundLabel();
      video.load();
      if(!reduced){ video.play().catch(function(){}); }
    });
  });
})();
