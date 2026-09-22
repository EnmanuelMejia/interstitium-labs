/**
 * Khan-grade Learn → Practice → Checkpoint next-action queue.
 * Mount: <div data-il-mastery data-il-mastery-track="prep"></div>
 * Optional data-il-mastery-learn / -practice / -checkpoint href overrides.
 */
(function (g) {
  'use strict';
  var TRACKS = {
    learn: {
      title: 'Curriculum mastery loop',
      steps: [
        { id: 'learn', title: 'Learn', hint: 'Open an outcome card & skills map', href: '/learn/skills/' },
        { id: 'practice', title: 'Practice', hint: 'Ship a path block or SuperLab task', href: '/labs/superlab/' },
        { id: 'checkpoint', title: 'Checkpoint', hint: 'Self-rate radar + drills', href: '/prep/drills/' }
      ]
    },
    prep: {
      title: 'Interview mastery loop',
      steps: [
        { id: 'learn', title: 'Learn', hint: 'Phase notes: Math → Programming → DevOps', href: '/prep/math/' },
        { id: 'practice', title: 'Practice', hint: 'KatAs, labs, daily routine block', href: '/prep/programming/' },
        { id: 'checkpoint', title: 'Checkpoint', hint: 'STAR drills + explain-back', href: '/prep/drills/' }
      ]
    },
    founders: {
      title: 'Student Zero mastery loop',
      steps: [
        { id: 'learn', title: 'Learn', hint: 'Weekly OS + journey map', href: '/founders/#weekly-os' },
        { id: 'practice', title: 'Practice', hint: 'Quest board + Prep block', href: '/founders/#quest-board' },
        { id: 'checkpoint', title: 'Checkpoint', hint: 'Update skills radar', href: '/founders/#radar' }
      ]
    }
  };

  function key(track) { return 'il.mastery.' + track; }

  function loadState(track) {
    try {
      var raw = g.localStorage.getItem(key(track));
      if (raw) return JSON.parse(raw);
    } catch (e) {}
    return { done: {}, active: 'learn' };
  }

  function saveState(track, state) {
    try { g.localStorage.setItem(key(track), JSON.stringify(state)); } catch (e) {}
  }

  function nextStep(steps, state) {
    for (var i = 0; i < steps.length; i++) {
      if (!state.done[steps[i].id]) return steps[i];
    }
    return steps[steps.length - 1];
  }

  function mount(el) {
    if (el.getAttribute('data-il-mastery-ready')) return;
    var track = el.getAttribute('data-il-mastery-track') || 'learn';
    var cfg = TRACKS[track] || TRACKS.learn;
    var steps = cfg.steps.map(function (s) {
      var o = { id: s.id, title: s.title, hint: s.hint, href: s.href };
      var ov = el.getAttribute('data-il-mastery-' + s.id);
      if (ov) o.href = ov;
      return o;
    });
    var state = loadState(track);
    if (!state.active) state.active = nextStep(steps, state).id;

    var root = document.createElement('div');
    root.className = 'il-mastery';
    var head = document.createElement('p');
    head.className = 'il-kicker';
    head.textContent = cfg.title + ' · Learn → Practice → Checkpoint';
    root.appendChild(head);

    var trackEl = document.createElement('div');
    trackEl.className = 'il-mastery__track';
    trackEl.setAttribute('role', 'list');

    function paint() {
      trackEl.innerHTML = '';
      steps.forEach(function (s, idx) {
        var a = document.createElement('a');
        a.className = 'il-mastery-step';
        a.href = s.href;
        a.setAttribute('role', 'listitem');
        if (state.done[s.id]) a.classList.add('is-done');
        if (state.active === s.id) a.classList.add('is-active');
        a.innerHTML =
          '<div class="il-mastery-step__n">0' + (idx + 1) + (state.done[s.id] ? ' · Done' : '') + '</div>' +
          '<div class="il-mastery-step__title"></div>' +
          '<div class="il-mastery-step__hint"></div>';
        a.querySelector('.il-mastery-step__title').textContent = s.title;
        a.querySelector('.il-mastery-step__hint').textContent = s.hint;
        a.addEventListener('click', function () {
          state.active = s.id;
          saveState(track, state);
        });
        // mark done via button
        var mark = document.createElement('button');
        mark.type = 'button';
        mark.className = 'il-coach-topic';
        mark.style.marginTop = '0.65rem';
        mark.textContent = state.done[s.id] ? 'Reopen' : 'Mark done';
        mark.addEventListener('click', function (ev) {
          ev.preventDefault();
          ev.stopPropagation();
          state.done[s.id] = !state.done[s.id];
          state.active = nextStep(steps, state).id;
          saveState(track, state);
          paint();
          paintNext();
        });
        a.appendChild(mark);
        trackEl.appendChild(a);
      });
    }

    var nextBox = document.createElement('div');
    nextBox.className = 'il-mastery__next';
    nextBox.setAttribute('aria-live', 'polite');
    function paintNext() {
      var n = nextStep(steps, state);
      var allDone = steps.every(function (s) { return state.done[s.id]; });
      nextBox.innerHTML =
        '<div><div class="il-mastery__next-label">' + (allDone ? 'Loop complete · restart or deepen' : 'Your next action') + '</div>' +
        '<div class="il-mastery__next-action"></div></div>' +
        '<a class="il-mastery__cta" href=""></a>';
      nextBox.querySelector('.il-mastery__next-action').textContent = allDone
        ? 'All three stages checked — bump radar ratings or open Coach.'
        : n.title + ' — ' + n.hint;
      var cta = nextBox.querySelector('.il-mastery__cta');
      cta.href = allDone ? '/coach/' : n.href;
      cta.textContent = allDone ? 'Open Coach' : 'Go · ' + n.title;
    }

    paint();
    paintNext();
    root.appendChild(trackEl);
    root.appendChild(nextBox);
    el.innerHTML = '';
    el.appendChild(root);
    el.setAttribute('data-il-mastery-ready', '1');
  }

  function boot() {
    var nodes = document.querySelectorAll('[data-il-mastery]');
    for (var i = 0; i < nodes.length; i++) mount(nodes[i]);
  }

  g.ILMastery = { mount: mount, boot: boot, tracks: TRACKS };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})(typeof window !== 'undefined' ? window : this);
