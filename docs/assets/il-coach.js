/**
 * Noah Live Assist — local Socratic in-lab coach. NO fake API keys.
 * Exceeds KodeKloud AI Tutor Live Assist on honesty: lab-context prompts, no spoiler dumps,
 * demand-tier OSS router (Ollama) when present, 3D curriculum stages stay separate.
 * Optional: window.IL_COACH / IL_MUSE / IL_MODEL_ROUTER (never commit secrets).
 * Topics: CIDR, Git, K8s pods (+ Terraform, CI, Linux) + lab-paste triage.
 */
(function (g) {
  'use strict';

  var TOPICS = [
    { id: 'cidr', label: 'CIDR' },
    { id: 'git', label: 'Git' },
    { id: 'k8s', label: 'K8s pods' },
    { id: 'terraform', label: 'Terraform' },
    { id: 'ci', label: 'CI/CD' },
    { id: 'linux', label: 'Linux' }
  ];

  function labContext(el) {
    var ctx = {
      surface: '',
      challenge: '',
      scene: '',
      mode: 'coach'
    };
    try {
      var path = (g.location && g.location.pathname) || '';
      if (path.indexOf('/labs/challenge') === 0) ctx.surface = 'challenge';
      else if (path.indexOf('/labs') === 0) ctx.surface = 'labs';
      else if (path.indexOf('/coach') === 0) ctx.surface = 'coach';
      else if (path.indexOf('/prep') === 0) ctx.surface = 'prep';
      var host = el || (g.document && g.document.querySelector('[data-il-live-assist], [data-il-coach]'));
      if (host) {
        ctx.challenge = host.getAttribute('data-il-lab-challenge') || '';
        ctx.scene = host.getAttribute('data-il-lab-scene') || '';
        if (host.getAttribute('data-il-live-assist') != null) ctx.mode = 'live-assist';
      }
      var ch = g.document && g.document.querySelector('[data-il-challenge-id], [data-challenge]');
      if (ch && !ctx.challenge) {
        ctx.challenge = ch.getAttribute('data-il-challenge-id') || ch.getAttribute('data-challenge') || '';
      }
    } catch (e) {}
    return ctx;
  }

  function liveAssistPreface(ctx) {
    var bits = ['Noah Live Assist'];
    if (ctx.surface) bits.push(ctx.surface);
    if (ctx.challenge) bits.push('challenge ' + ctx.challenge);
    if (ctx.scene) bits.push('scene ' + ctx.scene);
    return bits.join(' · ') + ' — Socratic, lab-context, no spoiler dump. Paste an error or hypothesis.';
  }

  var RULES = [
    // meta
    { re: /(answer|just tell me|give me the (answer|solution)|solve it for me)/i, topic: null,
      reply: 'I will not dump the answer. What have you already tried? Name one observation (error text, command output, or hypothesis).' },
    // Live Assist — lab paste / terminal triage (still Socratic)
    { re: /(error:|Traceback|E\d{4}|ImagePullBackOff|CrashLoopBackOff|ErrImagePull|CreateContainerConfigError)/i, topic: null,
      reply: 'Live Assist triage: quote the *first* failing line only. What command or apply produced it? Do not paste secrets. What did you expect to happen instead?' },
    { re: /(kubectl\s+(apply|get|describe|logs)|helm\s+|argocd\s+|terraform\s+)/i, topic: 'k8s',
      reply: 'Live Assist: name the resource kind + namespace (no cluster credentials). Is the failure at apply-time validation, schedule, or runtime? One hypothesis before I nudge the next check.' },
    { re: /(micro-?lesson|on-?demand|explain this lab|what should I do next)/i, topic: null,
      reply: 'Micro-lesson mode: I will not narrate the whole lab. Pick one concept (CIDR, probes, selectors, state lock, pipeline stage). What have you already verified?' },

    { re: /^(hi|hello|hey)\b/i, topic: null,
      reply: 'Welcome. Ask about CIDR, Git, K8s, blockchain, quantum, deep work, or Linux. I stay Socratic for coaching — factual questions get direct answers from the site\u2019s curriculum.' },
    // CIDR
    { re: /(cidr|subnet|\/2[0-9]|netmask|usable hosts?)/i, topic: 'cidr',
      reply: 'CIDR check: (1) How many host bits remain? (2) What are network vs broadcast? (3) Are you designing for hosts or for routes? Reply with your prefix and intended host count.' },
    { re: /(overlap|supernet|longest\s*prefix)/i, topic: 'cidr',
      reply: 'Overlap thinking: draw both ranges as bit prefixes. Does one contain the other? Routers pick longest prefix match — which prefix is more specific?' },
    // Git
    { re: /(detached|head|rebase|merge conflict|force.?push)/i, topic: 'git',
      reply: 'Git: Is the commit published to a shared branch? If yes, avoid history rewrites. If no, what named branch should hold this work? Paste the status line you care about (redact secrets).' },
    { re: /(cherry-?pick|revert|reset)/i, topic: 'git',
      reply: 'Choose the tool by intent: undo on a public branch → usually revert. Discard local only → reset. Replay a commit elsewhere → cherry-pick. Which intent is yours?' },
    // K8s
    { re: /(crashloop|pending|imagepull|readiness|liveness|pod)/i, topic: 'k8s',
      reply: 'Pod triage order: describe events → logs (--previous if restarting) → probes/resources/image. Which phase is the Pod in right now, and what does the last event say?' },
    { re: /(service|clusterip|endpoint|selector)/i, topic: 'k8s',
      reply: 'Service path: do labels on the Pod match spec.selector? Do Endpoints populate? From inside the cluster, can you curl the ClusterIP? Where does the chain break?' },
    // Terraform
    { re: /(terraform|state|plan|apply|drift)/i, topic: 'terraform',
      reply: 'Terraform: Is state remote and locked? Did plan show destroy you did not expect? Never apply a surprise destroy in shared state — quote the resource address that worries you.' },
    // CI
    { re: /(jenkins|github actions|pipeline|ci\/?cd|workflow)/i, topic: 'ci',
      reply: 'CI: Is the failure at lint, unit, build, push, or deploy? Separate “test red” from “secrets/registry auth”. Which stage failed first?' },
    // Blockchain (site carries a full ledger-engineering track)
    { re: /(blockchain|bitcoin|ethereum|solidity|smart contract|utxo|monero|stellar|xrpl|ledger)/i, topic: 'blockchain',
      reply: 'Ledger first: which layer is your question on — the protocol (consensus, UTXO/account model), the cryptography (hashes, signatures), or the application (contracts, wallets)? Name the layer, then state your hypothesis.' },
    // Quantum
    { re: /(quantum|qubit|superposition|entanglement)/i, topic: 'quantum',
      reply: 'Quantum: are you asking about the physics, an algorithm (Shor, Grover), or the engineering of qubits? Write the smallest state involved — what operation are you uncertain about?' },
    // Study method (Cal Newport content now on site)
    { re: /(deep work|procrastinat|study plan|time block|focus)/i, topic: 'study',
      reply: 'Study method: are you stuck on attention, retention, or pacing? Name one 90-minute distraction-free session you could run this week — same time, same place, phone elsewhere. What would it cover?' },
    // Zero Trust / IL-11 (honest: no such track exists on the site)
    { re: /(il-?11|zero.?trust)/i, topic: null,
      reply: 'Honest correction: there is no IL-11 Zero Trust track on this site — the name matches no published academy or path. The real Zero Trust material lives in two labs: the K8s CKA network-policies lab (default-deny-all, explicit allow rules) and the Security+/CySA+ microsegmentation lab. Which one do you want to work through, and what is your first hypothesis about it?' },
    // Career
    { re: /(interview|resume|job application|career|salary|hiring)/i, topic: 'career',
      reply: 'Career: are you optimizing the application, the interview, or the offer? Name your single strongest proof of work — a shipped project beats a claimed skill. What is yours?' },
    // Linux
    { re: /(linux|systemd|journalctl|chmod|ssh|disk|oom)/i, topic: 'linux',
      reply: 'Linux: What is the symptom — exit code, service status, or resource pressure? Check unit status / journal / df / free before changing configs. What command output do you have?' }
  ];

  var FALLBACK = 'I only have local rule-based coaching right now (AI model hookup pending). Ask about CIDR, Git, K8s pods, Terraform, CI/CD, Linux, blockchain, quantum, or study method — or ask any factual question and I will answer it from the site\u2019s curriculum on-device.';

  function config() {
    return g.IL_COACH || {};
  }

  function socratic(text, topic) {
    var cfg = config();
    var router = g.IL_MODEL_ROUTER || g.ILModelRouter;
    // Prefer analytics-driven OSS router when present (local Ollama / OpenAI-compat).
    if (router && typeof router.chat === 'function') {
      var messages = [{ role: 'user', content: text }];
      return router.chat(messages, { topic: topic || '', task: 'chat' }).then(function (res) {
        var lr = asReply(localReply(text, topic));
        return {
          text: res.text || lr.text,
          source: res.text ? (res.source || res.backendId || 'model-router') : lr.source,
          modelId: res.modelId,
          demand_tier: res.demand_tier
        };
      }, function () {
        return asReply(localReply(text, topic));
      });
    }
    // Legacy: endpoint set without router — honesty stub (CSP + key safety).
    if (cfg.endpoint) {
      var lr2 = asReply(localReply(text, topic));
      return Promise.resolve({
        text: 'IL_COACH.endpoint is set, but load il-model-router.js (or a same-origin Worker proxy) before enabling remote chat. Meanwhile: ' + lr2.text,
        source: 'stub-remote'
      });
    }
    return Promise.resolve(asReply(localReply(text, topic)));
  }

  /* localReply returns a string for Socratic rules, or {text, source} for the
     knowledge-bundle branch. Normalize before handing to the chat shell. */
  function asReply(r) {
    if (r && typeof r === 'object' && typeof r.text === 'string') {
      return { text: r.text, source: r.source || 'local-rules' };
    }
    return { text: String(r), source: 'local-rules' };
  }

  function localReply(text, topic) {
    for (var i = 0; i < RULES.length; i++) {
      var r = RULES[i];
      if (r.re.test(text) && (!r.topic || !topic || r.topic === topic || topic === r.topic)) {
        return r.reply;
      }
    }
    if (topic) {
      var topical = RULES.filter(function (r) { return r.topic === topic; });
      if (topical.length) return topical[0].reply + ' Your question: “' + String(text).slice(0, 120) + '”';
    }
    /* On-device knowledge bundle: direct grounded answers when no Socratic rule
       fires. Socratic stays the coach doctrine; the bundle answers factual
       "tell me about X" questions from the site's real curriculum. Plain text
       only — the coach chat renders escaped bubbles, no markdown. */
    try {
      var kbApi = g.__ilNoahKB;
      if (kbApi && kbApi.get && kbApi.answer && kbApi.get()) {
        var hit = kbApi.answer(text);
        if (hit && hit.entry) {
          var plain = String(hit.reply)
            .replace(/\[([^\]]+)\]\((\/[^)]+)\)/g, '$1 ($2)')
            .replace(/\*\*/g, '');
          return { text: plain + '\n\nWant to go Socratic on it? State your first hypothesis and we will reason from there.', source: 'kb-local' };
        }
      }
    } catch (e) { /* bundle unreachable — Socratic fallback below */ }
    return FALLBACK;
  }

  function mount(el) {
    if (el.getAttribute('data-il-coach-ready')) return;
    var topic = el.getAttribute('data-il-coach-topic') || '';
    var ctx = labContext(el);
    var live = ctx.mode === 'live-assist' || el.getAttribute('data-il-live-assist') != null;

    var shell = document.createElement('div');
    shell.className = 'il-coach-shell' + (live ? ' il-coach-shell--live-assist' : '');

    var left = document.createElement('div');
    left.className = 'il-ux-card il-ux-card--quiet';
    left.innerHTML =
      '<span class="il-coach-status"><span class="il-coach-status__dot" aria-hidden="true"></span> ' + (live ? 'Noah Live Assist · online (local)' : 'Noah · Socratic coach') + '</span>' +
      '<h2 class="mt-4 font-display text-2xl tracking-[-0.02em]" style="margin-top:1rem;font-family:Space Grotesk,system-ui,sans-serif;font-size:1.5rem;color:#e8eef5">' + (live ? 'Live Assist in the lab' : 'Local Socratic hints') + '</h2>' +
      '<p style="margin-top:0.75rem;font-size:0.875rem;color:#8b9bb4;line-height:1.55">' + (live
        ? 'Real-time <em>in-lab</em> help without KodeKloud\'s hosted fleet claim. Paste an error or hypothesis. On-demand micro-lessons stay Socratic — no spoiler dump. Demand-tier OSS router when Ollama is present. No fake keys.'
        : 'No API keys in this repo. Optional <code style="color:#5eead4">window.IL_COACH</code> stub for a future same-origin proxy. I ask questions; I do not dump final answers.') + '</p>' +
      '<p class="il-kicker" style="margin-top:1.25rem">Topics</p>';
    var topics = document.createElement('div');
    topics.className = 'il-coach-topics';
    topics.style.marginTop = '0.75rem';
    TOPICS.forEach(function (t) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'il-coach-topic' + (topic === t.id ? ' is-on' : '');
      b.textContent = t.label;
      b.addEventListener('click', function () {
        topic = t.id;
        Array.prototype.forEach.call(topics.children, function (c) { c.classList.remove('is-on'); });
        b.classList.add('is-on');
        push('bot', 'Topic set to ' + t.label + '. What are you stuck on? One sentence on what you already tried.');
      });
      topics.appendChild(b);
    });
    left.appendChild(topics);
    left.insertAdjacentHTML('beforeend',
      '<p class="il-honest-note" style="margin-top:1.25rem"><strong>Honesty vs KodeKloud Live Assist:</strong> We ship Socratic lab-context coaching + optional local Ollama router. We do <em>not</em> claim a hosted multi-cloud playground fleet or terminal keylogger. SuperLab is cloneable proof; paste your own lab state.</p>');

    var right = document.createElement('div');
    right.className = 'il-ux-card';
    var log = document.createElement('div');
    log.className = 'il-coach-log';
    log.setAttribute('role', 'log');
    log.setAttribute('aria-live', 'polite');
    var form = document.createElement('form');
    form.className = 'il-coach-form';
    form.setAttribute('autocomplete', 'off');
    var input = document.createElement('input');
    input.type = 'text';
    input.name = 'q';
    input.placeholder = 'Ask a stuck question (not “just give the answer”)…';
    input.setAttribute('aria-label', 'Coach question');
    var send = document.createElement('button');
    send.type = 'submit';
    send.textContent = 'Ask';
    form.appendChild(input);
    form.appendChild(send);
    right.appendChild(log);
    right.appendChild(form);

    function push(who, text) {
      var m = document.createElement('div');
      m.className = 'il-coach-msg il-coach-msg--' + who;
      m.textContent = text;
      log.appendChild(m);
      log.scrollTop = log.scrollHeight;
    }

    push('bot', live ? liveAssistPreface(ctx) : 'Interstitium Coach (local rules). Topics: CIDR, Git, K8s, Terraform, CI/CD, Linux. I will not answer-dump — show your work.');

    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var q = (input.value || '').trim();
      if (!q) return;
      push('user', q);
      input.value = '';
      send.disabled = true;
      socratic(q, topic).then(function (res) {
        push('bot', res.text);
        send.disabled = false;
        input.focus();
        try {
          if (g.ILGame && g.ILGame.award) g.ILGame.award('coach_ask', 5, { id: 'coach:' + Date.now() });
        } catch (e) {}
      });
    });

    shell.appendChild(left);
    shell.appendChild(right);
    el.innerHTML = '';
    el.appendChild(shell);
    el.setAttribute('data-il-coach-ready', '1');
  }

  function boot() {
    var nodes = document.querySelectorAll('[data-il-coach], [data-il-live-assist]');
    for (var i = 0; i < nodes.length; i++) mount(nodes[i]);
  }

  g.ILCoach = { mount: mount, boot: boot, ask: socratic, topics: TOPICS,
    labContext: labContext, liveAssistPreface: liveAssistPreface,
    usesRouter: function () { return !!(g.IL_MODEL_ROUTER || g.ILModelRouter); } };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})(typeof window !== 'undefined' ? window : this);
