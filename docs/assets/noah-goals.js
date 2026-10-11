/* Noah/Genesis Goals — Phase 1 client (2026-10-11).
 *
 * The mandate: give Noah or Genesis a goal and it handles the rest.
 * This module is the Goals surface inside /noah/:
 *   - a "🎯 Goals" entry in the sidebar (with an active-goal count badge)
 *   - a slide-over panel: add-goal box, goal cards (domain icon, progress
 *     bar, next action, due date), expandable step checklists, pause /
 *     resume / complete, milestone display, and the goal timeline
 *   - a morning-brief check-in nudge on chat open when steps are due
 *     (one concise card, dismissible per day — never spam)
 * Data lives server-side per account via /api/goals; a summaries cache
 * mirrors to localStorage "il-goals-v1" (registered as the "goals" store
 * in il-sync.js) so goals follow the user through the sync layer too.
 * Signed-out visitors get an honest sign-in prompt — goals need an
 * account to follow you. */
(function () {
  'use strict';
  if (window.ILGoals) return;
  if (!document.getElementById('newChatBtn')) return; /* /noah/ only */

  var API = '/api/goals';
  var CACHE_KEY = 'il-goals-v1';
  var DISMISS_KEY = 'il-goals-checkin-dismissed';
  var state = { goals: [], signedIn: null, open: false, expanded: {} };

  var DOMAIN_META = {
    learn: { icon: '🎓', label: 'Learning' },
    money: { icon: '💰', label: 'Money' },
    health: { icon: '💪', label: 'Health' },
    shopping: { icon: '🛒', label: 'Shopping' },
    relationships: { icon: '💛', label: 'Relationships' },
    general: { icon: '🎯', label: 'Life goals' },
  };

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function $(id) { return document.getElementById(id); }
  function todayStr() { return new Date().toISOString().slice(0, 10); }

  var css = [
    '#goalsBtn{position:relative}',
    '#goalsBtn .g-badge{position:absolute;top:6px;right:8px;background:#c9a227;color:#0a0e1a;',
    'border-radius:999px;font-size:.65rem;font-weight:700;padding:1px 6px}',
    '.ilg-overlay{position:fixed;inset:0;background:rgba(4,6,12,.55);z-index:60;opacity:0;pointer-events:none;transition:opacity .2s}',
    '.ilg-overlay.on{opacity:1;pointer-events:auto}',
    '.ilg-panel{position:fixed;top:0;right:0;height:100dvh;width:min(430px,94vw);z-index:61;',
    'background:var(--panel,#10141d);color:var(--text,#e8e4da);border-left:1px solid rgba(201,162,39,.25);',
    'transform:translateX(105%);transition:transform .25s ease;display:flex;flex-direction:column;',
    'box-shadow:-18px 0 50px rgba(0,0,0,.5)}',
    '.ilg-panel.on{transform:none}',
    '.ilg-head{display:flex;align-items:center;gap:.6rem;padding:1rem 1.1rem;border-bottom:1px solid rgba(255,255,255,.08)}',
    '.ilg-head h2{font-size:1.05rem;margin:0;flex:1}',
    '.ilg-head button{background:none;border:1px solid rgba(255,255,255,.15);color:inherit;border-radius:8px;padding:.3rem .6rem;cursor:pointer}',
    '.ilg-body{overflow-y:auto;padding:1rem 1.1rem;flex:1}',
    '.ilg-add{display:flex;flex-direction:column;gap:.5rem;margin-bottom:1.1rem}',
    '.ilg-add textarea{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);border-radius:10px;',
    'color:inherit;padding:.6rem .7rem;font:inherit;resize:vertical;min-height:52px}',
    '.ilg-add .row{display:flex;gap:.5rem}',
    '.ilg-add select{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);border-radius:8px;color:inherit;padding:.45rem;font:inherit}',
    '.ilg-add select option{color:#111}',
    '.ilg-add button{background:#c9a227;color:#0a0e1a;border:none;border-radius:8px;padding:.5rem .9rem;font-weight:700;cursor:pointer;flex:1}',
    '.ilg-add button:disabled{opacity:.55;cursor:wait}',
    '.ilg-hint{font-size:.78rem;color:var(--muted2,#9a958a);margin:0}',
    '.ilg-card{border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:.8rem .9rem;margin-bottom:.8rem;background:rgba(255,255,255,.03)}',
    '.ilg-card.paused{opacity:.65}',
    '.ilg-card h3{margin:0 0 .25rem;font-size:.98rem;display:flex;gap:.5rem;align-items:baseline}',
    '.ilg-card .meta{font-size:.75rem;color:var(--muted2,#9a958a);margin-bottom:.45rem}',
    '.ilg-bar{height:8px;border-radius:99px;background:rgba(255,255,255,.1);overflow:hidden;margin:.35rem 0 .5rem}',
    '.ilg-bar i{display:block;height:100%;background:linear-gradient(90deg,#c9a227,#e6c95c)}',
    '.ilg-next{font-size:.85rem;margin:.3rem 0}',
    '.ilg-next b{color:#e6c95c}',
    '.ilg-due{font-size:.75rem;color:#e08a8a}',
    '.ilg-due.soon{color:#e6c95c}',
    '.ilg-actions{display:flex;gap:.4rem;flex-wrap:wrap;margin-top:.55rem}',
    '.ilg-actions button{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);color:inherit;',
    'border-radius:8px;padding:.35rem .6rem;font-size:.8rem;cursor:pointer}',
    '.ilg-actions button.primary{background:#c9a227;color:#0a0e1a;border-color:#c9a227;font-weight:700}',
    '.ilg-steps{margin:.6rem 0 0;padding:0;list-style:none}',
    '.ilg-steps li{display:flex;gap:.5rem;align-items:flex-start;padding:.35rem 0;border-top:1px dashed rgba(255,255,255,.08);font-size:.85rem}',
    '.ilg-steps li.done{opacity:.6;text-decoration:line-through}',
    '.ilg-steps li button{margin-left:auto;background:none;border:1px solid rgba(255,255,255,.2);color:inherit;border-radius:6px;padding:.1rem .45rem;cursor:pointer;font-size:.75rem;flex:none}',
    '.ilg-steps .due{font-size:.7rem;color:var(--muted2,#9a958a);display:block;text-decoration:none}',
    '.ilg-timeline{margin-top:.5rem;font-size:.75rem;color:var(--muted2,#9a958a)}',
    '.ilg-timeline div{padding:.15rem 0;border-top:1px dotted rgba(255,255,255,.06)}',
    '.ilg-empty{color:var(--muted2,#9a958a);font-size:.9rem;line-height:1.5}',
    '.ilg-signin a{color:#e6c95c}',
    '.ilg-checkin{margin:0 auto .8rem;max-width:820px;border:1px solid rgba(201,162,39,.4);',
    'background:rgba(201,162,39,.08);border-radius:12px;padding:.7rem .9rem;font-size:.9rem;',
    'display:flex;gap:.7rem;align-items:flex-start}',
    '.ilg-checkin p{margin:0;flex:1;line-height:1.45}',
    '.ilg-checkin button{background:#c9a227;color:#0a0e1a;border:none;border-radius:8px;padding:.35rem .7rem;font-weight:700;cursor:pointer;flex:none}',
    '.ilg-checkin .x{background:none;color:inherit;border:1px solid rgba(255,255,255,.2);font-weight:400}',
  ].join('\n');
  var style = document.createElement('style');
  style.id = 'il-goals-style';
  style.textContent = css;
  document.head.appendChild(style);

  /* ---------- DOM ---------- */
  var newBtn = $('newChatBtn');
  var goalsBtn = document.createElement('button');
  goalsBtn.className = 'new-chat';
  goalsBtn.id = 'goalsBtn';
  goalsBtn.type = 'button';
  goalsBtn.innerHTML = '🎯 Goals';
  newBtn.parentNode.insertBefore(goalsBtn, newBtn.nextSibling);

  var overlay = document.createElement('div');
  overlay.className = 'ilg-overlay';
  var panel = document.createElement('aside');
  panel.className = 'ilg-panel';
  panel.setAttribute('aria-label', 'Your goals');
  panel.innerHTML =
    '<div class="ilg-head"><h2>🎯 Your goals</h2>' +
    '<button type="button" id="ilgRefresh">Refresh</button>' +
    '<button type="button" id="ilgClose" aria-label="Close goals">✕</button></div>' +
    '<div class="ilg-body" id="ilgBody"></div>';
  document.body.appendChild(overlay);
  document.body.appendChild(panel);
  var body = panel.querySelector('#ilgBody');

  function setBadge() {
    var n = state.goals.filter(function (g) { return g.status === 'active'; }).length;
    var b = goalsBtn.querySelector('.g-badge');
    if (n) {
      if (!b) { b = document.createElement('span'); b.className = 'g-badge'; goalsBtn.appendChild(b); }
      b.textContent = n;
    } else if (b) b.remove();
  }

  function cacheGoals() {
    try { localStorage.setItem(CACHE_KEY, JSON.stringify({ goals: state.goals })); } catch (e) {}
  }

  function api(path, opts) {
    return fetch(path, Object.assign({ headers: { 'Content-Type': 'application/json' } }, opts || {}))
      .then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (data) {
          return { status: res.status, data: data };
        });
      });
  }

  function refresh() {
    return api(API).then(function (out) {
      if (out.status === 401) { state.signedIn = false; state.goals = []; }
      else if (out.data && out.data.ok) { state.signedIn = true; state.goals = out.data.goals || []; }
      state.loaded = true;
      cacheGoals(); setBadge(); render();
      return out;
    }).catch(function () { state.loaded = true; render(); });
  }

  function dueClass(g) {
    if (!g.next_due || g.status !== 'active') return '';
    var t = todayStr();
    if (g.next_due < t) return ' overdue';
    if (g.next_due === t) return ' soon';
    return '';
  }
  function dueText(g) {
    if (!g.next_due || g.status !== 'active') return '';
    var t = todayStr();
    if (g.next_due < t) return 'Next step overdue (was due ' + g.next_due + ')';
    if (g.next_due === t) return 'Next step due today';
    return 'Next step due ' + g.next_due;
  }

  function cardHtml(g) {
    var meta = DOMAIN_META[g.domain] || DOMAIN_META.general;
    var h = '<article class="ilg-card' + (g.status === 'paused' ? ' paused' : '') + '" data-id="' + esc(g.id) + '">';
    h += '<h3><span aria-hidden="true">' + meta.icon + '</span><span>' + esc(g.title) + '</span></h3>';
    h += '<div class="meta">' + meta.label + ' · ' + esc(g.status) + ' · check-ins ' + esc(g.cadence) +
      ' · ' + g.steps_done + '/' + g.steps_total + ' steps</div>';
    h += '<div class="ilg-bar"><i style="width:' + (g.pct || 0) + '%"></i></div>';
    if (g.status === 'completed') h += '<p class="ilg-next">🎉 <b>Complete</b></p>';
    else h += '<p class="ilg-next">Next: <b>' + esc(g.next_action || '—') + '</b></p>';
    var dt = dueText(g);
    if (dt) h += '<p class="ilg-due' + dueClass(g) + '">' + esc(dt) + '</p>';
    h += '<div class="ilg-actions">';
    if (g.status === 'active') {
      h += '<button type="button" class="primary" data-act="next">✓ Step done</button>';
      h += '<button type="button" data-act="steps">' + (state.expanded[g.id] ? 'Hide steps' : 'Steps') + '</button>';
      h += '<button type="button" data-act="pause">Pause</button>';
      h += '<button type="button" data-act="complete">Complete</button>';
    } else if (g.status === 'paused') {
      h += '<button type="button" class="primary" data-act="resume">Resume</button>';
      h += '<button type="button" data-act="steps">' + (state.expanded[g.id] ? 'Hide steps' : 'Steps') + '</button>';
      h += '<button type="button" data-act="complete">Complete</button>';
    } else {
      h += '<button type="button" data-act="steps">' + (state.expanded[g.id] ? 'Hide steps' : 'Steps') + '</button>';
    }
    h += '</div>';
    if (state.expanded[g.id] && g._full) {
      var f = g._full;
      if (f.milestones && f.milestones.length) {
        h += '<ul class="ilg-steps">' + f.milestones.map(function (m, i) {
          return '<li class="' + (m.done ? 'done' : '') + '"><span>◆</span><span>' + esc(m.title) + '</span>' +
            '<button type="button" data-mile="' + i + '" data-done="' + (m.done ? '0' : '1') + '">' + (m.done ? 'Reopen' : 'Reached') + '</button></li>';
        }).join('') + '</ul>';
      }
      h += '<ul class="ilg-steps">' + f.steps.map(function (s) {
        return '<li class="' + (s.state === 'done' || s.state === 'skipped' ? 'done' : '') + '">' +
          '<span>' + (s.state === 'done' ? '✅' : s.state === 'skipped' ? '⏭' : '⬜') + '</span>' +
          '<span>' + esc(s.title) + (s.due ? '<span class="due">due ' + esc(s.due) + '</span>' : '') + '</span>' +
          (s.state !== 'done' && s.state !== 'skipped'
            ? '<button type="button" data-step="' + esc(s.id) + '">Done</button>' : '') +
          '</li>';
      }).join('') + '</ul>';
      if (f.timeline && f.timeline.length) {
        h += '<div class="ilg-timeline">' + f.timeline.slice(-6).reverse().map(function (t) {
          return '<div>' + esc(String(t.ts || '').slice(0, 10)) + ' — ' + esc(t.text) + '</div>';
        }).join('') + '</div>';
      }
    }
    h += '</article>';
    return h;
  }

  function render() {
    if (state.signedIn === false) {
      body.innerHTML = '<p class="ilg-empty ilg-signin">Goals live in your account so Noah and Genesis ' +
        'can carry them across every device. <a href="/account/">Sign in</a> to hand them a goal.</p>';
      return;
    }
    var h = '<form class="ilg-add" id="ilgAdd">' +
      '<textarea id="ilgText" maxlength="1000" placeholder="Hand Noah a goal — “Save $200 a month”, “Get fit by December”, “Find me a laptop under $800”, “Stay close to my brother”…" aria-label="New goal"></textarea>' +
      '<div class="row"><select id="ilgDomain" aria-label="Goal area">' +
      '<option value="">Auto-detect area</option>' +
      Object.keys(DOMAIN_META).map(function (k) {
        return '<option value="' + k + '">' + DOMAIN_META[k].icon + ' ' + DOMAIN_META[k].label + '</option>';
      }).join('') +
      '</select><button type="submit" id="ilgSubmit">Give it to Noah</button></div>' +
      '<p class="ilg-hint">Noah/Genesis builds the plan, works the steps, and checks in. ' +
      'It never buys, sends, or books anything without your approval.</p></form>';
    if (!state.goals.length) {
      h += '<p class="ilg-empty">No goals yet. State one above — or just tell Noah in chat: ' +
        '“I want to save $200 a month” becomes a tracked goal with a plan on the spot.</p>';
    } else {
      h += state.goals.map(cardHtml).join('');
    }
    body.innerHTML = h;
    var form = $('ilgAdd');
    if (form) form.addEventListener('submit', onAdd);
    body.querySelectorAll('.ilg-card').forEach(function (card) {
      var id = card.getAttribute('data-id');
      card.querySelectorAll('button[data-act]').forEach(function (b) {
        b.addEventListener('click', function () { onAction(id, b.getAttribute('data-act'), b); });
      });
      card.querySelectorAll('button[data-step]').forEach(function (b) {
        b.addEventListener('click', function () {
          post(id + '/progress', { step_id: b.getAttribute('data-step'), state: 'done' }).then(function () { loadFull(id); });
        });
      });
      card.querySelectorAll('button[data-mile]').forEach(function (b) {
        b.addEventListener('click', function () {
          post(id + '/progress', { milestone_index: parseInt(b.getAttribute('data-mile'), 10), milestone_done: b.getAttribute('data-done') === '1' })
            .then(function () { loadFull(id); });
        });
      });
    });
  }

  function post(pathSuffix, payload) {
    return api(API + '/' + pathSuffix, { method: 'POST', body: JSON.stringify(payload || {}) })
      .then(function (out) {
        if (out.data && out.data.goal) {
          var pub = out.data.goal;
          state.goals = state.goals.map(function (g) {
            return g.id === pub.id ? Object.assign({}, g, summaryOf(pub), { _full: pub }) : g;
          });
          cacheGoals(); setBadge(); render();
        }
        return out;
      });
  }
  function summaryOf(g) {
    return { id: g.id, title: g.title, domain: g.domain, agent: g.agent, status: g.status, cadence: g.cadence,
      pct: g.pct, next_action: g.next_action, next_step_id: g.next_step_id, next_due: g.next_due,
      steps_total: g.steps_total, steps_done: g.steps_done, created_at: g.created_at, updated_at: g.updated_at };
  }

  function loadFull(id) {
    return api(API + '/' + id).then(function (out) {
      if (out.data && out.data.goal) {
        var pub = out.data.goal;
        state.goals = state.goals.map(function (g) {
          return g.id === id ? Object.assign({}, summaryOf(pub), { _full: pub }) : g;
        });
        cacheGoals(); setBadge(); render();
      }
    });
  }

  function onAction(id, act, btn) {
    if (act === 'steps') {
      state.expanded[id] = !state.expanded[id];
      if (state.expanded[id]) loadFull(id); else render();
      return;
    }
    btn.disabled = true;
    if (act === 'next') post(id + '/progress', { complete_next: true }).then(function () { refresh(); });
    else post(id + '/' + act, {}).then(function () { refresh(); });
  }

  function onAdd(ev) {
    ev.preventDefault();
    var text = $('ilgText').value.trim();
    var domain = $('ilgDomain').value || undefined;
    if (text.length < 3) return;
    var btn = $('ilgSubmit');
    btn.disabled = true; btn.textContent = 'Noah is planning…';
    api(API, { method: 'POST', body: JSON.stringify({ text: text, domain: domain }) }).then(function (out) {
      if (out.status === 401) { state.signedIn = false; render(); return; }
      if (out.data && out.data.goal) {
        var pub = out.data.goal;
        state.goals.unshift(Object.assign({}, summaryOf(pub), { _full: pub }));
        state.expanded[pub.id] = true;
        cacheGoals(); setBadge(); render();
      } else {
        btn.disabled = false; btn.textContent = 'Give it to Noah';
      }
    }).catch(function () { btn.disabled = false; btn.textContent = 'Give it to Noah'; });
  }

  function openPanel() {
    state.open = true;
    overlay.classList.add('on'); panel.classList.add('on');
    if (!state.loaded) refresh(); else render();
  }
  function closePanel() {
    state.open = false;
    overlay.classList.remove('on'); panel.classList.remove('on');
  }
  goalsBtn.addEventListener('click', function () { state.open ? closePanel() : openPanel(); });
  overlay.addEventListener('click', closePanel);
  panel.querySelector('#ilgClose').addEventListener('click', closePanel);
  panel.querySelector('#ilgRefresh').addEventListener('click', refresh);
  document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && state.open) closePanel(); });

  /* Morning-brief check-in: on chat open, surface due steps once a day. */
  function checkin() {
    try { if (localStorage.getItem(DISMISS_KEY) === todayStr()) return; } catch (e) {}
    api(API + '/checkin').then(function (out) {
      if (!out.data || !out.data.ok || !out.data.due || !out.data.due.length) return;
      var main = document.querySelector('main') || document.body;
      var card = document.createElement('div');
      card.className = 'ilg-checkin';
      card.innerHTML = '<p>' + esc(out.data.brief) + '</p>' +
        '<button type="button" class="go">View goals</button><button type="button" class="x" aria-label="Dismiss">✕</button>';
      var composer = document.querySelector('.composer');
      if (composer && composer.parentNode) composer.parentNode.insertBefore(card, composer);
      else main.appendChild(card);
      card.querySelector('.go').addEventListener('click', openPanel);
      card.querySelector('.x').addEventListener('click', function () {
        card.remove();
        try { localStorage.setItem(DISMISS_KEY, todayStr()); } catch (e) {}
      });
    }).catch(function () {});
  }

  window.ILGoals = { refresh: refresh, open: openPanel, close: closePanel };
  refresh().then(checkin);
})();
