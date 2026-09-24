/**
 * Brilliant-style interactive drill cards with instant feedback.
 * Mount: <div data-il-drills data-il-drills-set="cidr|git|k8s|mixed"></div>
 * Never dumps full answer first — Socratic feedback on wrong picks.
 */
(function (g) {
  'use strict';

  function t(key, fb) {
    try {
      if (g.ILi18n && typeof g.ILi18n.t === 'function') return g.ILi18n.t(key, fb);
    } catch (e) {}
    return fb;
  }

  var SETS = {
    cidr: [
      {
        id: 'cidr-hosts',
        prompt: 'How many usable host addresses in a /24 IPv4 subnet (classic RFC 950)?',
        choices: [
          { key: 'A', text: '256', correct: false, tip: 'That counts network + broadcast. Subtract two for usable hosts.' },
          { key: 'B', text: '254', correct: true, tip: 'Correct — 2^8 − 2 = 254 usable hosts.' },
          { key: 'C', text: '255', correct: false, tip: 'Off by one. Network vs broadcast vs hosts.' },
          { key: 'D', text: '24', correct: false, tip: '24 is the prefix length, not the host count.' }
        ]
      },
      {
        id: 'cidr-mask',
        prompt: 'Which CIDR matches netmask 255.255.255.0?',
        choices: [
          { key: 'A', text: '/16', correct: false, tip: ' /16 is 255.255.0.0. Count the 1-bits.' },
          { key: 'B', text: '/24', correct: true, tip: 'Yes — twenty-four 1-bits → /24.' },
          { key: 'C', text: '/32', correct: false, tip: '/32 is a single host route.' },
          { key: 'D', text: '/8', correct: false, tip: '/8 is 255.0.0.0.' }
        ]
      },
      {
        id: 'cidr-overlap',
        prompt: 'Can 10.0.0.0/24 and 10.0.0.128/25 overlap?',
        choices: [
          { key: 'A', text: 'No — different prefixes never overlap', correct: false, tip: 'Prefix length alone does not guarantee disjointness.' },
          { key: 'B', text: 'Yes — 10.0.0.128/25 sits inside 10.0.0.0/24', correct: true, tip: 'Correct. Nested prefixes overlap; routing must choose longest match.' },
          { key: 'C', text: 'Only if both are public IPs', correct: false, tip: 'RFC1918 does not change set overlap.' },
          { key: 'D', text: 'Only on IPv6', correct: false, tip: 'Same set logic on IPv4.' }
        ]
      }
    ],
    git: [
      {
        id: 'git-detached',
        prompt: 'You are in a detached HEAD after checking out a commit. Safest next move to keep new work?',
        choices: [
          { key: 'A', text: 'git push -f origin main', correct: false, tip: 'Force-pushing main from detached HEAD is destructive. Branch first.' },
          { key: 'B', text: 'git switch -c fix/keep-work', correct: true, tip: 'Create a branch at the current commit so work has a name.' },
          { key: 'C', text: 'git reset --hard HEAD~20', correct: false, tip: 'That discards history — opposite of keeping work.' },
          { key: 'D', text: 'Delete .git and re-clone', correct: false, tip: 'Nuclear option; you lose unpushed work.' }
        ]
      },
      {
        id: 'git-rebase',
        prompt: 'When is interactive rebase usually the wrong tool?',
        choices: [
          { key: 'A', text: 'Cleaning local commits not yet pushed', correct: false, tip: 'That is a common good use.' },
          { key: 'B', text: 'Rewriting commits already on a shared main branch', correct: true, tip: 'Rewriting published shared history breaks collaborators.' },
          { key: 'C', text: 'Squashing before opening a PR', correct: false, tip: 'Often fine if the branch is still private.' },
          { key: 'D', text: 'Editing a commit message on a feature branch', correct: false, tip: 'Fine while the branch is yours alone.' }
        ]
      },
      {
        id: 'git-ff',
        prompt: 'Fast-forward merge means…',
        choices: [
          { key: 'A', text: 'Git invents a merge commit always', correct: false, tip: 'That describes a true merge, not FF.' },
          { key: 'B', text: 'Branch pointer moves forward with no merge commit', correct: true, tip: 'Exactly — linear history when target has no divergent commits.' },
          { key: 'C', text: 'All conflicts auto-resolve to theirs', correct: false, tip: 'FF requires no divergence; conflicts are unrelated.' },
          { key: 'D', text: 'Hooks are skipped', correct: false, tip: 'Hooks still run.' }
        ]
      }
    ],
    k8s: [
      {
        id: 'k8s-pod',
        prompt: 'A Pod is CrashLoopBackOff. First signal to inspect?',
        choices: [
          { key: 'A', text: 'kubectl delete ns kube-system', correct: false, tip: 'Never start by deleting control-plane namespaces.' },
          { key: 'B', text: 'kubectl describe pod / kubectl logs --previous', correct: true, tip: 'Events + previous logs usually reveal probe/config/image errors.' },
          { key: 'C', text: 'Raise replicas to 100', correct: false, tip: 'Amplifies the failure mode.' },
          { key: 'D', text: 'Disable the scheduler', correct: false, tip: 'Unrelated and dangerous.' }
        ]
      },
      {
        id: 'k8s-svc',
        prompt: 'ClusterIP Service selects Pods by…',
        choices: [
          { key: 'A', text: 'Pod UID only', correct: false, tip: 'UIDs change every recreate; labels are the contract.' },
          { key: 'B', text: 'Label selectors matching Pod labels', correct: true, tip: 'Yes — Service.spec.selector ↔ Pod.metadata.labels.' },
          { key: 'C', text: 'Node hostname', correct: false, tip: 'That is not how ClusterIP selects endpoints.' },
          { key: 'D', text: 'Image digest', correct: false, tip: 'Images are not the Service selector.' }
        ]
      },
      {
        id: 'k8s-probe',
        prompt: 'Liveness probe failing repeatedly typically causes…',
        choices: [
          { key: 'A', text: 'Pod stays Ready forever', correct: false, tip: 'Liveness ≠ readiness; failure restarts the container.' },
          { key: 'B', text: 'kubelet restarts the container', correct: true, tip: 'Correct — liveness failure → restart.' },
          { key: 'C', text: 'etcd wipe', correct: false, tip: 'Probes never touch etcd.' },
          { key: 'D', text: 'Automatic HorizontalPodAutoscaler scale to zero', correct: false, tip: 'HPA uses metrics, not liveness.' }
        ]
      }
    ]
  };

  SETS.mixed = SETS.cidr.concat(SETS.git, SETS.k8s);

  function pickSet(name) {
    return SETS[name] || SETS.mixed;
  }

  function mount(el) {
    if (el.getAttribute('data-il-drills-ready')) return;
    var setName = el.getAttribute('data-il-drills-set') || 'mixed';
    var items = pickSet(setName).slice();
    var idx = 0;
    var answered = {};

    var root = document.createElement('div');
    root.className = 'il-drills';

    var progress = document.createElement('p');
    progress.className = 'il-kicker';
    root.appendChild(progress);

    var cardHost = document.createElement('div');
    root.appendChild(cardHost);

    var nav = document.createElement('div');
    nav.style.display = 'flex';
    nav.style.gap = '0.5rem';
    nav.style.marginTop = '1rem';
    nav.style.flexWrap = 'wrap';
    var prev = document.createElement('button');
    prev.type = 'button';
    prev.className = 'il-coach-topic';
    prev.textContent = t('drill.prev', 'Previous');
    var next = document.createElement('button');
    next.type = 'button';
    next.className = 'il-coach-topic';
    next.textContent = t('drill.next', 'Next drill');
    nav.appendChild(prev);
    nav.appendChild(next);
    root.appendChild(nav);

    function render() {
      var item = items[idx];
      progress.textContent = t('drill.kicker', 'Drill') + ' ' + (idx + 1) + ' / ' + items.length + ' · ' + setName + ' · ' + t('drill.feedback_note', 'instant feedback, no answer dumps');
      cardHost.innerHTML = '';
      var card = document.createElement('div');
      card.className = 'il-drill';
      card.setAttribute('role', 'group');
      card.setAttribute('aria-label', t('drill.aria', 'Practice drill'));
      var prompt = document.createElement('p');
      prompt.className = 'il-drill__prompt';
      prompt.textContent = item.prompt;
      card.appendChild(prompt);
      var choices = document.createElement('div');
      choices.className = 'il-drill__choices';
      var fb = document.createElement('div');
      fb.className = 'il-feedback';
      fb.setAttribute('aria-live', 'polite');

      var locked = !!answered[item.id];

      item.choices.forEach(function (c) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'il-drill__choice';
        btn.innerHTML = '<span class="il-drill__key"></span><span></span>';
        btn.querySelector('.il-drill__key').textContent = c.key;
        btn.querySelectorAll('span')[1].textContent = c.text;
        if (locked) {
          btn.disabled = true;
          if (c.correct) btn.classList.add('is-correct');
          if (answered[item.id] === c.key && !c.correct) btn.classList.add('is-wrong');
        }
        btn.addEventListener('click', function () {
          if (answered[item.id]) return;
          answered[item.id] = c.key;
          try {
            if (g.ILGame && typeof g.ILGame.award === 'function') {
              g.ILGame.award(c.correct ? 'drill_ok' : 'drill_try', c.correct ? 15 : 3, { id: 'drill:' + item.id });
            }
          } catch (e) {}
          // re-render for classes
          render();
          var feedback = cardHost.querySelector('.il-feedback');
          if (feedback) {
            feedback.classList.add('is-on', c.correct ? 'il-feedback--ok' : 'il-feedback--bad');
            feedback.textContent = c.correct
              ? '✓ ' + c.tip
              : t('drill.not_yet', 'Not yet —') + ' ' + c.tip + ' ' + t('drill.another_angle', 'Try another angle; do not memorize the letter.');
          }
        });
        choices.appendChild(btn);
      });
      card.appendChild(choices);
      if (locked) {
        var chosen = item.choices.filter(function (c) { return c.key === answered[item.id]; })[0];
        var correct = item.choices.filter(function (c) { return c.correct; })[0];
        fb.classList.add('is-on', chosen && chosen.correct ? 'il-feedback--ok' : 'il-feedback--bad');
        fb.textContent = (chosen && chosen.correct)
          ? '✓ ' + correct.tip
          : t('drill.not_yet', 'Not yet —') + ' ' + (chosen ? chosen.tip : '') + (correct ? ' (' + t('adapt.path', 'Path') + ': ' + correct.key + ')' : '');
      }
      card.appendChild(fb);
      cardHost.appendChild(card);
    }

    prev.addEventListener('click', function () {
      idx = (idx - 1 + items.length) % items.length;
      render();
    });
    next.addEventListener('click', function () {
      idx = (idx + 1) % items.length;
      render();
    });

    render();
    el.innerHTML = '';
    el.appendChild(root);
    el.setAttribute('data-il-drills-ready', '1');
    document.addEventListener('il:i18n', function () {
      prev.textContent = t('drill.prev', 'Previous');
      next.textContent = t('drill.next', 'Next drill');
      render();
    });
  }

  function boot() {
    var nodes = document.querySelectorAll('[data-il-drills]');
    for (var i = 0; i < nodes.length; i++) mount(nodes[i]);
  }

  g.ILDrills = { mount: mount, boot: boot, sets: SETS };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})(typeof window !== 'undefined' ? window : this);
