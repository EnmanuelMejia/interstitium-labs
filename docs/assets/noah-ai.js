/* =====================================================================
 * Interstitium Labs — Noah AI (js/noah.js)
 *
 * The resident intelligence of Interstitium Labs. Named Noah AI.
 *
 * Two engines, one voice:
 *  1. LOCAL (always available): the Socratic engine — ask(text, ctx)
 *     -> {reply, nudges[]}. Keyword-topic detection, one guiding
 *     question, a two-rung hint ladder. Never an answer dump first.
 *  2. REMOTE (when reachable): POST {messages} to the Noah AI endpoint
 *     (same-origin /api/noah by default; absolute on sibling domains),
 *     which answers with the full distilled knowledge of Enmanuel's
 *     work: the Learning University curriculum, every repo, the brand.
 *     If the endpoint is unreachable or reports fallback, the widget
 *     degrades gracefully to the local engine with a plain notice.
 *
 * The chat widget (window.IL.noahAI) renders a floating launcher with
 * an orbiting avatar, a chat panel, typing indicator, suggestion
 * chips, and conversation memory in localStorage.
 *
 * Public surface:
 *   window.IL.noah   = { ask, configureLLM }            (legacy, kept)
 *   window.IL.noahAI = { open, close, toggle, ask, endpoint }
 * ===================================================================== */
(function (g) {
  'use strict';

  /* ================= Local Socratic engine (unchanged doctrine) ====== */

  var TOPICS = [
    { name: 'algebra', keys: ['equation', 'solve for', 'quadratic', 'polynomial', 'variable', 'factor', 'algebra', 'linear', 'inequality', 'fraction', 'exponent'] },
    { name: 'trigonometry', keys: ['trigonometry', 'triangle', 'hypotenuse', 'unit circle', ' sin', ' cos', ' tan', 'sine', 'cosine', 'tangent', 'angle'] },
    { name: 'calculus', keys: ['derivative', 'integral', 'calculus', 'differentiate', 'integrate', 'limit'] },
    { name: 'networking', keys: ['subnet', 'cidr', 'tcp', 'ip address', 'dns', 'router', 'switch', 'osi', 'packet', 'vlan', 'nat', 'network'] },
    { name: 'linux', keys: ['linux', 'bash', 'terminal', 'chmod', 'ssh', 'kernel', 'systemd', 'grep', 'cron', 'shell', 'command line'] },
    { name: 'security', keys: ['vulnerability', 'exploit', 'encryption', 'malware', 'phishing', 'firewall', 'penetration', 'ransomware', 'cve', 'security'] },
    { name: 'python', keys: ['python', 'list comprehension', 'pandas', 'def '] },
    { name: 'sql', keys: ['sql', 'select', 'join', 'where clause', 'database', 'query'] },
    { name: 'git', keys: ['git', 'commit', 'branch', 'merge', 'rebase', 'repository'] },
    { name: 'kubernetes', keys: ['kubernetes', 'k8s', 'kubectl', 'helm', 'argocd', 'gitops'] },
    { name: 'containers', keys: ['docker', 'container', 'pod', 'deployment'] },
    { name: 'cloud', keys: ['aws', 'azure', 'gcp', 'cloud', 'ec2'] },
    { name: 'blockchain', keys: ['blockchain', 'bitcoin', 'ethereum', 'solidity', 'smart contract', 'wallet', 'ledger', 'consensus', 'monero', 'stellar', 'xrpl', 'defi', 'utxo'] },
    { name: 'quantum', keys: ['quantum', 'qubit', 'superposition', 'entanglement', 'shor', 'grover'] },
    { name: 'devops', keys: ['devops', 'sre', 'terraform', 'jenkins', 'github actions', 'cicd', 'ci/cd', 'pipeline'] },
    { name: 'web', keys: ['javascript', 'typescript', 'react', 'html', 'css', 'node.js', 'nodejs', 'frontend', 'fullstack', 'full-stack'] },
    { name: 'study', keys: ['study', 'studying', 'focus', 'procrastinat', 'deep work', 'time block', 'exam', 'certification'] },
    { name: 'career', keys: ['interview', 'resume', 'cv', 'job', 'career', 'salary', 'hiring', 'offer letter'] }
  ];

  var GUIDE = {
    'algebra': { question: 'What is the smallest piece of this equation you can isolate with certainty?', nudge1: 'Move the constant term across the equals sign. What must change about its sign as it crosses?', nudge2: 'With the term in the unknown standing alone, which single operation undoes its coefficient?' },
    'trigonometry': { question: 'Before naming a ratio, which side of the triangle do you actually know, and which side are you asked to find?', nudge1: 'Label the sides relative to the given angle: opposite, adjacent, hypotenuse. Which two appear in your problem?', nudge2: 'Write the ratio that binds exactly those two sides. The function name follows the ratio, not the other way around.' },
    'calculus': { question: 'Are you being asked about a rate of change, or about accumulation? The two questions wear different tools.', nudge1: 'State in plain words what the symbol is asking for, before you reach for any rule.', nudge2: 'Apply one rule only — the outermost structure first. What does the outer form resemble?' },
    'networking': { question: 'Which layer of the problem are you actually on — addressing, routing, or naming? Name it before you touch anything.', nudge1: 'Write down what the address and the mask, together, actually claim about the network.', nudge2: 'Follow one packet in your mind from source to destination. Where does your current explanation first break?' },
    'linux': { question: 'What did you expect the command to do, stated as plainly as you can, before we look at what it did?', nudge1: 'Read the manual entry for the single flag you are least sure about. What does it promise?', nudge2: 'Reproduce the behavior with the smallest possible input. What changes when the input shrinks?' },
    'security': { question: 'Who is the actor, what is the asset, and where is the boundary between them? State all three.', nudge1: 'Describe the attack in one sentence with no jargon. If you cannot, the model is not yet clear.', nudge2: 'Which single control, if removed, would make the attack trivial? That is where the real weakness lives.' },
    'python': { question: 'What type is the object at the exact point where your reasoning gets uncertain?', nudge1: 'Print the object and its type at that point. What does the interpreter report, versus what you assumed?', nudge2: 'Reduce the code to the smallest fragment that still shows the behavior. What remains?' },
    'sql': { question: 'Which rows must survive, and which must be excluded? State the filter as a sentence before writing it.', nudge1: 'Name the grain of the result: one row per what? Every join and grouping must serve that grain.', nudge2: 'Run the query without the final filter. Do the intermediate rows match what you expected?' },
    'git': { question: 'Draw the branch graph as it is right now, from memory. Where does your drawing go vague?', nudge1: 'Which commit is each branch actually pointing at? Name them; do not trust the labels alone.', nudge2: 'What would the graph look like after the operation succeeds? Describe the desired end state first.' },
    'containers': { question: 'Is the failure in the image, the container, or the orchestration around it? Place it before fixing it.', nudge1: 'Read the exact error line, not the summary. Which component speaks first in the log?', nudge2: 'What is the smallest change that would prove your theory wrong? Try that before trying to prove it right.' },
    'cloud': { question: 'Which service owns the resource, and which identity is acting on it? Confusion between the two causes most cloud errors.', nudge1: 'Check the effective permissions of the acting identity, not the ones you believe it has.', nudge2: 'Trace one request through the console or the logs. Where does the observed path diverge from your mental model?' },
    'kubernetes': { question: 'Is the trouble in the workload definition, the cluster state, or the traffic path into the pod? Place it before you touch anything.', nudge1: 'Name the failing object — Deployment, Service, or Pod — and read its events first. What does the newest event actually claim?', nudge2: 'What is the smallest change that would prove your theory wrong? Try that before trying to prove it right.' },
    'blockchain': { question: 'Are you reasoning about the ledger, the cryptography, or the application on top? Name the layer before the question.', nudge1: 'State what the chain guarantees — ordering, finality — and what it does not. Which guarantee does your question depend on?', nudge2: 'Which module\u2019s lab would settle your question empirically: UTXO, EVM, or consensus?' },
    'quantum': { question: 'Is your question about the physics, the algorithms, or the engineering of qubits? Each wears different math.', nudge1: 'Write the smallest quantum state involved — one qubit, two amplitudes. What operation are you actually asking about?', nudge2: 'Apply one idea only: superposition, interference, or entanglement. Which one carries your question?' },
    'devops': { question: 'Is the failure in code, pipeline, or platform? The fix lives wherever the handoff breaks.', nudge1: 'Name the stage that went red first — lint, test, build, push, or deploy — and quote its first error line.', nudge2: 'Separate \u201ctest red\u201d from \u201csecrets or registry auth\u201d. Which one is it?' },
    'web': { question: 'Is the behavior in markup, style, or script? Isolate the layer before debugging the framework.', nudge1: 'Reproduce with the smallest page that still shows it. Does it survive with the framework removed?', nudge2: 'What type is the object at the exact point where your reasoning gets uncertain?' },
    'study': { question: 'Are you stuck on attention, retention, or pacing? Each has a different fix.', nudge1: 'What does one 90-minute distraction-free session on this topic actually look like for you — same time, same place, phone in another room?', nudge2: 'Which are you skipping: the shutdown ritual, the weekly review, or measuring depth instead of hours?' },
    'career': { question: 'Are you optimizing the application, the interview, or the offer conversation? Each is a different game.', nudge1: 'Name the single strongest proof of work you can show — a shipped project beats a claimed skill. What is yours?', nudge2: 'State the role\u2019s actual problem in one sentence. How does your proof map onto it?' },
    'general': { question: 'What is the single claim you are least sure of in your own reasoning? Begin there.', nudge1: 'Restate the problem in your own words, with no terms you could not define to a beginner.', nudge2: 'What would you need to observe to know your hypothesis is wrong? Seek that observation first. Festina lente.' }
  };

  var llmConfig = null;
  function configureLLM(opts) {
    if (!opts || !opts.endpoint) { llmConfig = null; return null; }
    llmConfig = { endpoint: String(opts.endpoint), apiKey: opts.apiKey ? String(opts.apiKey) : null, model: opts.model ? String(opts.model) : null };
    return { endpoint: llmConfig.endpoint, model: llmConfig.model, local: true };
  }

  /* ============ On-device knowledge bundle ==========================
     Built by scripts/build-noah-knowledge.mjs from the site's real curriculum
     pages. The engine searches it and answers with cited on-site links.
     Nothing is invented: no bundle entry, no claim. */
  var KB = null, kbInflight = null;
  var KB_STOP = { what: 1, why: 1, how: 1, when: 1, where: 1, which: 1, who: 1,
    does: 1, doing: 1, done: 1, about: 1, tell: 1, show: 1, explain: 1, give: 1,
    with: 1, from: 1, that: 1, this: 1, these: 1, those: 1, them: 1, then: 1,
    than: 1, into: 1, over: 1, under: 1, your: 1, you: 1, the: 1, and: 1,
    for: 1, are: 1, was: 1, were: 1, has: 1, have: 1, had: 1, will: 1,
    would: 1, should: 1, could: 1, can: 1, any: 1, all: 1, more: 1, most: 1,
    some: 1, such: 1, like: 1, just: 1, very: 1, much: 1, many: 1, get: 1,
    got: 1, one: 1, two: 1, new: 1, best: 1, top: 1 };

  function ensureKB() {
    if (KB) return Promise.resolve(KB);
    if (kbInflight) return kbInflight;
    kbInflight = fetch('/assets/noah-knowledge.json', { credentials: 'same-origin' })
      .then(function (r) { if (!r.ok) throw new Error('kb-missing'); return r.json(); })
      .then(function (b) {
        KB = (b && b.entries && b.entries.length) ? b : null;
        return KB;
      })
      .catch(function () { KB = null; return null; });
    return kbInflight;
  }

  function kbTokens(text) {
    var out = [], words = String(text).toLowerCase().replace(/[^a-z0-9+#/ ]/g, ' ').split(/\s+/), i, w;
    for (i = 0; i < words.length; i++) {
      w = words[i];
      if (w.length > 2 && !KB_STOP[w]) out.push(w);
    }
    return out;
  }

  function kbScore(entry, tokens) {
    var score = 0, kws = String(entry.k || '').split(' '), i, j, tok, kw;
    var title = String(entry.t || '').toLowerCase(), desc = String(entry.d || '').toLowerCase();
    for (i = 0; i < tokens.length; i++) {
      tok = tokens[i];
      for (j = 0; j < kws.length; j++) {
        kw = kws[j];
        if (!kw) continue;
        if (kw === tok) { score += 3; break; }
        if (kw.indexOf(tok) === 0 || tok.indexOf(kw) === 0) { score += 1; break; }
      }
      if (title.indexOf(tok) !== -1) score += 2;
      else if (desc.indexOf(tok) !== -1) score += 1;
    }
    return score;
  }

  function shortTitle(t) {
    return String(t).split(/\s+[—–|\-]\s+/)[0].trim() || String(t);
  }

  function answerFromKB(text) {
    if (!KB || !KB.entries) return null;
    var tokens = kbTokens(text);
    if (!tokens.length) return null;
    var scored = [], i, s;
    for (i = 0; i < KB.entries.length; i++) {
      s = kbScore(KB.entries[i], tokens);
      if (s >= 3) scored.push({ e: KB.entries[i], s: s });
    }
    if (!scored.length) return null;
    scored.sort(function (a, b) { return b.s - a.s; });
    var top = scored[0], links = [], j;
    for (j = 0; j < scored.length && j < 3; j++) {
      if (scored[j].s >= top.s * 0.45) links.push('[' + shortTitle(scored[j].e.t) + '](' + scored[j].e.u + ')');
    }
    var reply = '**' + top.e.t + '** — ' + top.e.d;
    if (links.length) reply += '\n\nOn this site: ' + links.join(' · ');
    return { reply: reply, entry: top.e };
  }

  /* Direct answers for questions the site cannot answer from a page. All facts
     below are verified against the published site — no invented content. */
  var GREET_RE = /^(hi|hey|hello|yo|sup|good\s(morning|afternoon|evening))\b/;
  var BUILDER_RE = /who (built|made|created|founded|is behind)|about the founder|who runs this/;
  var START_RE = /what should i learn first|where (do|should) i start|how do i (get started|begin)|learning path/;
  var IL11_RE = /\bil-?11\b/;

  var A_GREET = 'Hey — I\u2019m **Noah**, answering on-device from this site\u2019s curriculum. ' +
    'Ask me about any track — blockchain, quantum, DevOps, Kubernetes, deep work — or tap a suggestion below.';
  var A_BUILDER = 'Interstitium Labs was built by **Enmanuel Mejia** — Founder and DevSecOps/Full Stack Developer. ' +
    'This site is his knowledge operating system: curriculum tracks, labs, and study guides distilled from his work ' +
    'across IT operations, DevOps, security, and systems engineering. Everything I tell you comes from these on-site ' +
    'pages, answered on-device. What do you want to learn first?';
  var A_START = '**Where to start** depends on your target:\n\n' +
    '- **DevOps / SRE roles:** [DevOps Zero to Hire](/paths/devops-zero-to-hire/) — Linux, networking, Git, containers, CI/CD.\n' +
    '- **Security:** [CISSP](/learn/sequences/cissp/) and [Security+ / CySA+](/learn/sequences/security-plus-cysa/) study guides.\n' +
    '- **Study method itself:** [Deep Work](/learn/deep-work/) and the [Study Protocol](/learn/study-protocol/).\n\n' +
    'Tell me the role or the topic and I\u2019ll narrow it to one next step.';
  var A_IL11 = 'Honest answer: **there is no IL-11 Zero Trust track on this site** — the name doesn\u2019t match ' +
    'a published academy or path. The site\u2019s real Zero Trust material lives inside two labs:\n\n' +
    '- **[K8s CKA](/learn/sequences/k8s-cka/)** — zero-trust network policies: default-deny-all, then explicit allow rules.\n' +
    '- **[Security+ / CySA+](/learn/sequences/security-plus-cysa/)** — microsegmentation plus a half-page zero-trust plan for a flat home LAN.\n\n' +
    'Want the network-policy lab or the segmentation plan first?';
  var A_ZT = 'Zero Trust on this site is taught as practice rather than a dedicated track: ' +
    '**[K8s CKA](/learn/sequences/k8s-cka/)** covers zero-trust network policies (default-deny-all with explicit allow rules), ' +
    'and **[Security+ / CySA+](/learn/sequences/security-plus-cysa/)** covers microsegmentation with a hands-on zero-trust plan lab. ' +
    'Which one do you want?';
  var A_UNKNOWN = 'I don\u2019t have on-site material on that yet — I answer from this site\u2019s curriculum, and it doesn\u2019t cover it. ' +
    'Try rephrasing, or start from [DevOps Zero to Hire](/paths/devops-zero-to-hire/), [Deep Work](/learn/deep-work/), or the [Study Protocol](/learn/study-protocol/).';

  function detectTopic(lower) {
    for (var i = 0; i < TOPICS.length; i++) {
      var keys = TOPICS[i].keys;
      for (var j = 0; j < keys.length; j++) {
        if (lower.indexOf(keys[j]) !== -1) return TOPICS[i].name;
      }
    }
    return 'general';
  }

  function ask(text, ctx) {
    var input = String(text == null ? '' : text);
    var lower = input.toLowerCase();
    /* 1 · direct special cases (verified facts only) */
    if (GREET_RE.test(lower) && input.trim().length < 32) return { reply: A_GREET, nudges: [] };
    if (BUILDER_RE.test(lower)) return { reply: A_BUILDER, nudges: [] };
    if (START_RE.test(lower)) return { reply: A_START, nudges: [] };
    if (IL11_RE.test(lower)) return { reply: A_IL11, nudges: [] };
    if (/zero.?trust/.test(lower)) return { reply: A_ZT, nudges: [] };
    /* 2 · the knowledge bundle: direct answers with cited on-site links */
    var hit = answerFromKB(input);
    if (hit) {
      var topic = detectTopic(lower);
      var guide = GUIDE[topic];
      var nudges = (guide && topic && topic !== 'general') ? [guide.question] : [];
      return { reply: hit.reply, nudges: nudges };
    }
    /* 3 · Socratic topic guides (bundle unreachable or genuinely uncovered) */
    var topic2 = detectTopic(lower);
    if (topic2 && topic2 !== 'general' && GUIDE[topic2]) {
      var g2 = GUIDE[topic2];
      return { reply: g2.question + ' ' + g2.nudge1, nudges: [g2.nudge2] };
    }
    return { reply: A_UNKNOWN, nudges: [], unknown: true };
  }

  /* Honesty screen for REMOTE replies (2026-10-01, noah-recovery-2). The remote
     endpoint once fabricated a confirmation of a nonexistent "IL-11 Zero Trust"
     track, so every remote answer is screened before display:
     - IL-11 claims that are not explicit denials are replaced with the verified
       local answer (there is no such track on this site).
     Remote answers are always labeled as remote; they never carry the on-device
     notice. Returns { reply, replaced }. */
  var REMOTE_NOTICE = 'Answered by the remote Noah endpoint — track names verified against this site\u2019s published pages; treat uncited claims as unverified.';
  function screenRemote(reply, text) {
    var r = String(reply == null ? '' : reply);
    if (/\bil-?11\b/i.test(r) && !/no\s+(such|il-?11)|doesn[’']t exist|not\s+a\s+(real|published)/i.test(r)) {
      return { reply: A_IL11, replaced: true };
    }
    return { reply: r, replaced: false };
  }

  /* ================= Remote endpoint =============================== */

  var DEFAULT_ENDPOINT = (function () {
    try {
      var h = window.location.host || '';
      if (h === 'learn.interstitiumlabs.dev') return '/api/noah';
      if (/interstitiumlabs\.dev$/.test(h)) return 'https://learn.interstitiumlabs.dev/api/noah';
    } catch (e) {}
    return '/api/noah';
  })();

  function getEndpoint() {
    try {
      if (window.IL_NOAH_ENDPOINT) return String(window.IL_NOAH_ENDPOINT);
    } catch (e) {}
    return llmConfig && llmConfig.endpoint ? llmConfig.endpoint : DEFAULT_ENDPOINT;
  }

  var LOCAL_NOTICE = 'Answered on-device from this site\u2019s distilled curriculum — no cloud.';

  function askLocal(text) {
    var out = ask(text);
    out.answered = !out.unknown; /* false only for the honest "not on this site" fallthrough */
    out.notice = LOCAL_NOTICE;
    return out;
  }

  function askRemote(text, history) {
    var endpoint = getEndpoint();
    var msgs = (history || []).concat([{ role: 'user', content: String(text) }]);
    return fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: msgs.slice(-12) })
    }).then(function (res) { return res.json().then(function (data) { return { res: res, data: data }; }); })
      .then(function (out) {
        if (out.res.ok && out.data && out.data.reply) {
          var screened = screenRemote(out.data.reply, text);
          return { reply: screened.reply, remote: true, remoteScreened: screened.replaced, notice: REMOTE_NOTICE };
        }
        return ensureKB().then(function () {
          var local = askLocal(text);
          return { reply: local.reply, nudges: local.nudges, remote: false, notice: local.notice };
        });
      })
      .catch(function () {
        return ensureKB().then(function () {
          var local = askLocal(text);
          return { reply: local.reply, nudges: local.nudges, remote: false, notice: local.notice };
        });
      });
  }

  /* ================= Chat widget =================================== */

  var WIDGET_CSS = [
    '#noah-launcher{position:fixed;right:22px;bottom:22px;width:64px;height:64px;border-radius:50%;',
    'cursor:pointer;z-index:2147483000;border:none;background:transparent;padding:0;}',
    '#noah-launcher .noah-orb{position:absolute;inset:6px;border-radius:50%;overflow:hidden;',
    'background:radial-gradient(circle at 35% 30%,#1c2b3a,#0a0f16 70%);',
    'box-shadow:0 0 0 1px rgba(212,175,55,.45),0 0 22px rgba(34,211,238,.25),0 8px 28px rgba(0,0,0,.55);}',
    '#noah-launcher .noah-orb canvas{width:100%;height:100%;display:block;border-radius:50%;}',
    '#noah-launcher:hover .noah-orb{box-shadow:0 0 0 1px rgba(212,175,55,.8),0 0 30px rgba(34,211,238,.45),0 8px 28px rgba(0,0,0,.55);}',
    '#noah-launcher .noah-ping{position:absolute;inset:0;border-radius:50%;border:2px solid rgba(34,211,238,.7);',
    'opacity:0;pointer-events:none;}',
    '#noah-launcher.attn .noah-ping{animation:noah-ping 1.6s ease-out 3;}',
    '@keyframes noah-ping{0%{transform:scale(1);opacity:.8;}100%{transform:scale(1.7);opacity:0;}}',
    '#noah-panel{position:fixed;right:22px;bottom:100px;width:min(392px,calc(100vw - 32px));height:min(600px,calc(100dvh - 140px));',
    'z-index:2147483001;display:flex;flex-direction:column;border-radius:18px;overflow:hidden;',
    'background:linear-gradient(165deg,#0d141d 0%,#0a0f16 60%,#0c1219 100%);',
    'border:1px solid rgba(212,175,55,.28);box-shadow:0 24px 70px rgba(0,0,0,.65),0 0 40px rgba(34,211,238,.08);',
    'opacity:0;transform:translateY(16px) scale(.98);pointer-events:none;transition:opacity .28s ease,transform .28s ease;}',
    '#noah-panel.open{opacity:1;transform:none;pointer-events:auto;}',
    '#noah-head{display:flex;align-items:center;gap:12px;padding:14px 16px;',
    'background:linear-gradient(120deg,rgba(212,175,55,.12),rgba(34,211,238,.08));border-bottom:1px solid rgba(212,175,55,.2);}',
    '#noah-head .noah-avatar{width:40px;height:40px;border-radius:50%;overflow:hidden;flex:none;',
    'box-shadow:0 0 0 1px rgba(212,175,55,.5),0 0 14px rgba(34,211,238,.3);background:#0a0f16;}',
    '#noah-head .noah-avatar canvas{width:100%;height:100%;display:block;border-radius:50%;}',
    '#noah-head .noah-title{flex:1;min-width:0;}',
    '#noah-head .noah-name{color:#f2e8c9;font-weight:650;font-size:15px;letter-spacing:.02em;}',
    '#noah-head .noah-status{color:#7d8ea3;font-size:12px;display:flex;align-items:center;gap:6px;}',
    '#noah-head .noah-dot{width:8px;height:8px;border-radius:50%;background:#34d399;box-shadow:0 0 8px #34d399;animation:noah-blink 2.4s ease-in-out infinite;}',
    '@keyframes noah-blink{0%,100%{opacity:1;}50%{opacity:.45;}}',
    '#noah-close{background:none;border:none;color:#7d8ea3;font-size:20px;cursor:pointer;line-height:1;padding:4px;}',
    '#noah-close:hover{color:#f2e8c9;}',
    '#noah-msgs{flex:1;overflow-y:auto;padding:16px 14px;display:flex;flex-direction:column;gap:12px;scrollbar-width:thin;}',
    '.noah-msg{max-width:88%;padding:10px 13px;border-radius:14px;font-size:14px;line-height:1.55;',
    'animation:noah-in .3s ease;word-wrap:break-word;}',
    '@keyframes noah-in{from{opacity:0;transform:translateY(8px);}to{opacity:1;transform:none;}}',
    '.noah-msg.user{align-self:flex-end;background:linear-gradient(135deg,#1d4ed8,#1e40af);color:#fff;border-bottom-right-radius:4px;}',
    '.noah-msg.noah{align-self:flex-start;background:rgba(255,255,255,.05);color:#dbe4ee;border:1px solid rgba(255,255,255,.08);border-bottom-left-radius:4px;}',
    '.noah-msg.noah b,.noah-msg.noah strong{color:#f2e8c9;}',
    '.noah-msg.noah code{background:rgba(0,0,0,.45);padding:1px 6px;border-radius:6px;font-size:12.5px;color:#7dd3fc;}',
    '.noah-msg.noah pre{background:rgba(0,0,0,.5);padding:10px;border-radius:8px;overflow-x:auto;font-size:12.5px;}',
    '.noah-msg.noah pre code{background:none;padding:0;}',
    '.noah-msg.noah ul{margin:6px 0;padding-left:18px;}',
    '.noah-msg .noah-notice{display:block;margin-top:8px;font-size:11.5px;color:#7d8ea3;font-style:italic;}',
    '.noah-nudges{display:flex;flex-direction:column;gap:6px;margin-top:8px;}',
    '.noah-nudge{background:rgba(212,175,55,.08);border:1px solid rgba(212,175,55,.25);border-radius:10px;',
    'padding:8px 10px;font-size:12.5px;color:#e8dcc0;cursor:pointer;}',
    '.noah-nudge:hover{background:rgba(212,175,55,.16);}',
    '.noah-nudge::before{content:"Hint \\2014  ";color:#d4af37;font-weight:600;}',
    '#noah-typing{align-self:flex-start;display:flex;gap:5px;padding:12px 14px;background:rgba(255,255,255,.05);border-radius:14px;}',
    '#noah-typing span{width:7px;height:7px;border-radius:50%;background:#7d8ea3;animation:noah-bounce 1.2s infinite;}',
    '#noah-typing span:nth-child(2){animation-delay:.15s;}',
    '#noah-typing span:nth-child(3){animation-delay:.3s;}',
    '@keyframes noah-bounce{0%,60%,100%{transform:none;opacity:.5;}30%{transform:translateY(-5px);opacity:1;}}',
    '#noah-chips{display:flex;gap:8px;padding:0 14px 10px;overflow-x:auto;scrollbar-width:none;}',
    '.noah-chip{flex:none;background:rgba(34,211,238,.08);border:1px solid rgba(34,211,238,.3);color:#a5e8fc;',
    'border-radius:999px;padding:7px 13px;font-size:12.5px;cursor:pointer;white-space:nowrap;}',
    '.noah-chip:hover{background:rgba(34,211,238,.18);}',
    '#noah-form{display:flex;gap:8px;padding:12px 14px;border-top:1px solid rgba(255,255,255,.08);}',
    '#noah-input{flex:1;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:12px;',
    'color:#eef3f8;padding:10px 13px;font-size:14px;outline:none;resize:none;font-family:inherit;max-height:96px;}',
    '#noah-input:focus{border-color:rgba(34,211,238,.5);}',
    '#noah-send{background:linear-gradient(135deg,#d4af37,#a67c1a);border:none;border-radius:12px;color:#0a0f16;',
    'font-weight:700;padding:0 16px;cursor:pointer;font-size:14px;}',
    '#noah-send:disabled{opacity:.45;cursor:default;}',
    '#noah-foot{padding:8px 14px 10px;color:#5b6b7f;font-size:11px;text-align:center;}',
    '@media (max-width:480px){#noah-panel{right:12px;bottom:92px;}#noah-launcher{right:14px;bottom:14px;}}'
  ].join('\n');

  var AVATAR_SRC = '/assets/noah-avatar.png'; // apex-local avatar
  var LS_KEY = 'noah-ai-history-v1';
  var CHIPS = ['What should I learn first?', 'How do I study with deep work?', 'Who built this site?', 'Explain a DevOps concept'];

  var els = {};
  var history = [];
  var busy = false;

  function el(tag, cls, html) {
    var d = document.createElement(tag);
    if (cls) d.className = cls;
    if (html != null) d.innerHTML = html;
    return d;
  }

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function mdLite(src) {
    var h = esc(src);
    h = h.replace(/```([\s\S]*?)```/g, function (m, code) { return '<pre><code>' + code.replace(/^\n/, '') + '</code></pre>'; });
    h = h.replace(/`([^`\n]+)`/g, '<code>$1</code>');
    h = h.replace(/\[([^\]\n]{1,80})\]\((\/[A-Za-z0-9\-._~:/?#@!$&'()*+,;=%]*)\)/g, '<a href="$2">$1</a>');
    h = h.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    var lines = h.split('\n'), out = [], inList = false;
    lines.forEach(function (ln) {
      var m = ln.match(/^\s*[-*]\s+(.*)/);
      if (m) { if (!inList) { out.push('<ul>'); inList = true; } out.push('<li>' + m[1] + '</li>'); }
      else { if (inList) { out.push('</ul>'); inList = false; } out.push(ln); }
    });
    if (inList) out.push('</ul>');
    return out.join('<br>');
  }

  function loadHistory() {
    try {
      var raw = localStorage.getItem(LS_KEY);
      if (raw) history = JSON.parse(raw).slice(-20) || [];
    } catch (e) { history = []; }
  }
  function saveHistory() {
    try { localStorage.setItem(LS_KEY, JSON.stringify(history.slice(-20))); } catch (e) {}
  }

  function addMsg(role, html, notice) {
    var m = el('div', 'noah-msg ' + (role === 'user' ? 'user' : 'noah'), html);
    if (notice) {
      var n = el('span', 'noah-notice', esc(notice));
      m.appendChild(n);
    }
    els.msgs.appendChild(m);
    els.msgs.scrollTop = els.msgs.scrollHeight;
    return m;
  }

  function showTyping() {
    var t = el('div', '', '<span></span><span></span><span></span>');
    t.id = 'noah-typing';
    els.msgs.appendChild(t);
    els.msgs.scrollTop = els.msgs.scrollHeight;
  }
  function hideTyping() {
    var t = document.getElementById('noah-typing');
    if (t) t.remove();
  }

  function renderNudges(nudges) {
    if (!nudges || !nudges.length) return;
    var box = el('div', 'noah-nudges');
    nudges.forEach(function (n) {
      var b = el('button', 'noah-nudge', esc(n));
      b.type = 'button';
      b.addEventListener('click', function () { NoahStats.track('nudge'); sendText(n); });
      box.appendChild(b);
    });
    els.msgs.appendChild(box);
    els.msgs.scrollTop = els.msgs.scrollHeight;
  }

  function sendText(text) {
    text = String(text || '').trim();
    if (!text || busy) return;
    busy = true;
    els.send.disabled = true;
    setAvatarState('thinking');
    NoahStats.track('ask', detectTopic(text.toLowerCase()));
    addMsg('user', esc(text));
    history.push({ role: 'user', content: text });
    saveHistory();
    showTyping();
    /* Local-first (2026-10-01, noah-recovery-2): the on-device knowledge bundle
       answers first, so the honesty guardrails can never be bypassed by trying the
       remote endpoint first. Remote is only a fallback for questions the site's
       curriculum genuinely doesn't cover, and its replies pass screenRemote(). */
    ensureKB().then(function () {
      var local = askLocal(text);
      if (local.answered) {
        deliver({ reply: local.reply, nudges: local.nudges, remote: false, local: true, notice: local.notice });
        return;
      }
      askRemote(text, history.slice(0, -1)).then(deliver);
    });
  }

  function deliver(out) {
    hideTyping();
    NoahStats.track(out.local ? 'local' : (out.remote ? 'remote' : 'fallback'));
    setAvatarState('speaking');
    setTimeout(function () { if (!busy) setAvatarState('idle'); }, 2800);
    var notice = out.notice;
    if (!out.remote && !out.local && !fallbackNoted && NoahStats.fallbackStreak() >= 3) {
      fallbackNoted = true;
      notice = (notice ? notice + ' ' : '') + 'Heads up: the remote Noah endpoint is unreachable — I\u2019m answering on-device from the site\u2019s curriculum.';
    }
    addMsg('noah', mdLite(out.reply), notice);
    if (out.nudges) renderNudges(out.nudges);
    history.push({ role: 'assistant', content: out.reply });
    saveHistory();
    busy = false;
    els.send.disabled = false;
    els.input.focus();
  }

  /* ================= NoahStats: privacy-respecting analytics ==========
     Event counters only — never message text, never PII. Aggregates live
     in localStorage; per-session deltas are beaconed to /api/noah-stats
     (fire-and-forget, throttled to one beacon per 5 minutes). This powers
     the in-widget autonomous iteration (adaptive chips, returning-user
     greeting, fallback awareness) and the weekly fleet review. */
  var NoahStats = (function () {
    var KEY = 'noah-ai-stats-v1';
    var agg = null, lastSent = null, lastBeacon = 0, fallbackStreak = 0;
    function fresh() {
      return { v: 1, opens: 0, asks: 0, remotes: 0, fallbacks: 0, nudges: 0,
        chips: 0, errors: 0, sessions: 0, byTopic: {}, firstSeen: Date.now() };
    }
    function load() {
      try {
        var raw = localStorage.getItem(KEY);
        agg = raw ? JSON.parse(raw) : fresh();
        if (!agg || agg.v !== 1 || !agg.byTopic) agg = fresh();
      } catch (e) { agg = fresh(); }
      agg.sessions++;
      save();
      try {
        lastSent = JSON.parse(JSON.stringify(agg));
      } catch (e) { lastSent = fresh(); }
    }
    function save() {
      try { localStorage.setItem(KEY, JSON.stringify(agg)); } catch (e) {}
    }
    function statsEndpoint() {
      try {
        var m = getEndpoint().match(/^(https:\/\/[^/]+)/);
        return (m ? m[1] : '') + '/api/noah-stats';
      } catch (e) { return null; }
    }
    function delta() {
      var d = { opens: agg.opens - lastSent.opens, asks: agg.asks - lastSent.asks,
        remotes: agg.remotes - lastSent.remotes, fallbacks: agg.fallbacks - lastSent.fallbacks,
        nudges: agg.nudges - lastSent.nudges, chips: agg.chips - lastSent.chips,
        errors: agg.errors - lastSent.errors, byTopic: {} };
      for (var k in agg.byTopic) {
        var dd = agg.byTopic[k] - (lastSent.byTopic[k] || 0);
        if (dd > 0) d.byTopic[k] = dd;
      }
      return d;
    }
    function maybeBeacon() {
      var now = Date.now();
      if (now - lastBeacon < 5 * 60 * 1000) return;
      var url = statsEndpoint();
      if (!url) return;
      var d = delta();
      var total = d.opens + d.asks + d.remotes + d.fallbacks + d.nudges + d.chips + d.errors;
      if (!total) return;
      lastBeacon = now;
      try { lastSent = JSON.parse(JSON.stringify(agg)); } catch (e) {}
      try {
        var payload = JSON.stringify({
          v: 1,
          sid: Math.random().toString(36).slice(2, 12),
          platform: /Capacitor/i.test(navigator.userAgent || '') ? 'mobile' : 'web',
          agg: d
        });
        if (navigator.sendBeacon) { navigator.sendBeacon(url, payload); }
        else { fetch(url, { method: 'POST', body: payload, keepalive: true }).catch(function () {}); }
      } catch (e) {}
    }
    function track(ev, topic) {
      if (!agg) load();
      if (ev === 'open') agg.opens++;
      else if (ev === 'ask') { agg.asks++; if (topic && topic !== 'general') agg.byTopic[topic] = (agg.byTopic[topic] || 0) + 1; }
      else if (ev === 'remote') { agg.remotes++; fallbackStreak = 0; }
      else if (ev === 'fallback') { agg.fallbacks++; fallbackStreak++; }
      else if (ev === 'nudge') agg.nudges++;
      else if (ev === 'chip') agg.chips++;
      else if (ev === 'error') agg.errors++;
      save();
      maybeBeacon();
    }
    function topTopic() {
      if (!agg) load();
      var best = null, n = 0;
      for (var k in agg.byTopic) { if (agg.byTopic[k] > n) { n = agg.byTopic[k]; best = k; } }
      return n >= 2 ? { topic: best, count: n } : null;
    }
    function getFallbackStreak() { return fallbackStreak; }
    function getSessions() { if (!agg) load(); return agg.sessions; }
    return { load: load, track: track, topTopic: topTopic,
      fallbackStreak: getFallbackStreak, sessions: getSessions };
  })();

  /* ============ Autonomous in-widget iteration =====================
     Noah adapts to the learner from their own usage — no server needed:
     - adaptive chips: the learner's most-asked topic becomes the first chip
     - returning greeting: sessions 2+ with a top topic get a welcome-back
       that names the topic and offers to continue
     - fallback awareness: 3+ consecutive local fallbacks surface one
       gentle connectivity note (once per session) */
  var TOPIC_LABEL = {
    algebra: 'algebra', trigonometry: 'trigonometry', calculus: 'calculus',
    networking: 'subnetting & networking', linux: 'Linux', security: 'security',
    python: 'Python', sql: 'SQL', git: 'Git', kubernetes: 'Kubernetes',
    containers: 'containers', cloud: 'cloud', blockchain: 'blockchain',
    quantum: 'quantum computing', devops: 'DevOps', web: 'web development',
    study: 'study method', career: 'career prep'
  };
  var fallbackNoted = false;
  function adaptiveChips() {
    var chips = CHIPS.slice();
    var top = NoahStats.topTopic();
    if (top && TOPIC_LABEL[top.topic]) {
      var label = 'Keep going with ' + TOPIC_LABEL[top.topic];
      chips = [label].concat(chips.filter(function (c) { return c !== label; }));
    }
    return chips;
  }
  function returningGreeting() {
    var top = NoahStats.topTopic();
    if (NoahStats.sessions() >= 2 && top && TOPIC_LABEL[top.topic] && !history.length) {
      return 'Welcome back. Last time you were working through <b>' +
        TOPIC_LABEL[top.topic] + '</b> — shall we continue where you left off, ' +
        'or start something new?';
    }
    return null;
  }

  /* ============ NoahAvatar: living-portrait canvas engine ============
     Layered render per frame: deep-space ground + drifting nebulae,
     breathing portrait, three orbit rings (one with a satellite),
     Hermetic glyphs riding the gold ring (Dee's planetary septet),
     twinkling particle motes, speaking ripples, state glow rim.
     States idle / thinking / speaking change tempo and glow.
     One shared rAF drives every mounted instance; pauses when the
     tab is hidden; renders a single static frame under
     prefers-reduced-motion. Falls back to a static <img>. */
  var NoahAvatar = (function () {
    var GLYPHS = ['\u2609', '\u263D', '\u263F', '\u2640', '\u2641', '\u2642', '\u2643'];
    var instances = [], rafId = 0, lastT = 0;
    var img = null, imgOk = false;
    var reduced = false;
    try { reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches); } catch (e) {}

    function ensureImg() {
      if (img || typeof Image === 'undefined') return;
      img = new Image();
      img.onload = function () { imgOk = true; };
      img.onerror = function () { img = null; };
      img.src = AVATAR_SRC;
    }

    function frame(now) {
      rafId = 0;
      var dt = Math.min(0.05, (now - lastT) / 1000 || 0.016);
      lastT = now;
      var any = false;
      for (var i = 0; i < instances.length; i++) {
        if (!instances[i].dead) { any = true; draw(instances[i], dt); }
      }
      if (any && !document.hidden) rafId = requestAnimationFrame(frame);
    }
    function kick() {
      if (!rafId && !reduced && typeof requestAnimationFrame !== 'undefined') {
        lastT = performance.now();
        rafId = requestAnimationFrame(frame);
      }
    }
    if (typeof document !== 'undefined' && document.addEventListener) {
      document.addEventListener('visibilitychange', function () { if (!document.hidden) kick(); });
    }

    function neb(ctx, x, y, r, rgb, a) {
      var g = ctx.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, 'rgba(' + rgb + ',' + a + ')');
      g.addColorStop(1, 'rgba(' + rgb + ',0)');
      ctx.fillStyle = g;
      ctx.fillRect(x - r, y - r, r * 2, r * 2);
    }

    function orbitRing(ctx, R, rx, ry, rot, color, w, satellite, st) {
      ctx.save();
      ctx.translate(R, R);
      ctx.rotate(rot * 0.35);
      ctx.strokeStyle = color;
      ctx.lineWidth = w;
      ctx.beginPath();
      if (ctx.ellipse) ctx.ellipse(0, 0, rx, ry, 0, 0, 6.2832);
      else ctx.arc(0, 0, (rx + ry) / 2, 0, 6.2832);
      ctx.stroke();
      if (satellite && st) {
        var sa = rot * 2, sx = Math.cos(sa) * rx, sy = Math.sin(sa) * ry;
        var sg = ctx.createRadialGradient(sx, sy, 0, sx, sy, 5);
        sg.addColorStop(0, 'rgba(170,242,255,1)');
        sg.addColorStop(1, 'rgba(34,211,238,0)');
        ctx.fillStyle = sg;
        ctx.beginPath(); ctx.arc(sx, sy, 5, 0, 6.2832); ctx.fill();
        ctx.fillStyle = '#e2fbff';
        ctx.beginPath(); ctx.arc(sx, sy, 1.7, 0, 6.2832); ctx.fill();
      }
      ctx.restore();
    }

    function draw(st, dt) {
      var speed = st.state === 'thinking' ? 2.8 : st.state === 'speaking' ? 1.7 : 1;
      st.t += dt * speed;
      if (st.state === 'speaking' && st.t - st.lastRipple > 0.55) {
        st.lastRipple = st.t;
        st.ripples.push({ r: 0.34, a: 0.5 });
      }
      st.px += (st.tx - st.px) * Math.min(1, dt * 6);
      st.py += (st.ty - st.py) * Math.min(1, dt * 6);

      var ctx = st.ctx, S = st.size, dpr = st.dpr, R = S / 2, i;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, S, S);
      ctx.save();
      ctx.beginPath(); ctx.arc(R, R, R - 1, 0, 6.2832); ctx.clip();

      var g = ctx.createRadialGradient(R * 0.85, R * 0.75, R * 0.1, R, R, R);
      g.addColorStop(0, '#16242f'); g.addColorStop(0.55, '#0a1119'); g.addColorStop(1, '#04070b');
      ctx.fillStyle = g; ctx.fillRect(0, 0, S, S);
      neb(ctx, R + Math.sin(st.t * 0.21) * R * 0.18, R * 0.72 + Math.cos(st.t * 0.17) * R * 0.12, R * 0.55, '212,175,55', 0.07);
      neb(ctx, R + Math.cos(st.t * 0.13) * R * 0.2, R * 0.4 + Math.sin(st.t * 0.19) * R * 0.14, R * 0.6, '34,211,238', 0.08);

      var br = 1 + 0.028 * Math.sin(st.t * 1.1);
      var pr = R * 0.62 * br;
      var ox = st.px * 2.2, oy = st.py * 2.2;
      if (imgOk) {
        ctx.save();
        ctx.beginPath(); ctx.arc(R + ox, R + oy, pr, 0, 6.2832); ctx.clip();
        var iw = img.width, ih = img.height, sc = Math.max(pr * 2 / iw, pr * 2 / ih);
        ctx.drawImage(img, R + ox - iw * sc / 2, R + oy - ih * sc / 2, iw * sc, ih * sc);
        ctx.restore();
        ctx.strokeStyle = 'rgba(212,175,55,.5)'; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.arc(R + ox, R + oy, pr, 0, 6.2832); ctx.stroke();
      } else {
        ctx.fillStyle = '#0d1620';
        ctx.beginPath(); ctx.arc(R, R, pr, 0, 6.2832); ctx.fill();
        ctx.fillStyle = '#d4af37';
        ctx.font = '700 ' + Math.round(pr * 1.1) + 'px Georgia,serif';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText('N', R, R + pr * 0.06);
      }
      var vg = ctx.createRadialGradient(R, R, R * 0.45, R, R, R);
      vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,.5)');
      ctx.fillStyle = vg; ctx.fillRect(0, 0, S, S);

      orbitRing(ctx, R, R * 0.80, R * 0.34, st.t * 0.5, 'rgba(34,211,238,.6)', 1.1, true, st);
      orbitRing(ctx, R, R * 0.70, R * 0.70, -st.t * 0.32, 'rgba(212,175,55,.45)', 1, false, null);
      orbitRing(ctx, R, R * 0.88, R * 0.30, st.t * 0.22 + 1.3, 'rgba(255,255,255,.22)', 0.8, false, null);

      ctx.fillStyle = 'rgba(212,175,55,.55)';
      ctx.font = Math.max(5, Math.round(R * 0.2)) + 'px serif';
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      for (i = 0; i < st.glyphs.length; i++) {
        var ga = st.glyphs[i].a + st.t * 0.32;
        ctx.fillText(st.glyphs[i].ch, R + Math.cos(ga) * R * 0.7, R + Math.sin(ga) * R * 0.7);
      }

      for (i = 0; i < st.parts.length; i++) {
        var p = st.parts[i];
        p.y -= p.s * dt * speed;
        if (p.y < -0.05) { p.y = 1.05; p.x = Math.random(); }
        var tw = 0.22 + 0.5 * Math.abs(Math.sin(st.t * 2 + p.tw));
        ctx.fillStyle = p.gold ? 'rgba(212,175,55,' + tw.toFixed(2) + ')' : 'rgba(165,232,252,' + tw.toFixed(2) + ')';
        ctx.beginPath(); ctx.arc(p.x * S, p.y * S, p.r, 0, 6.2832); ctx.fill();
      }

      for (i = st.ripples.length - 1; i >= 0; i--) {
        var rp = st.ripples[i];
        rp.r += dt * 0.9; rp.a -= dt * 0.8;
        if (rp.a <= 0 || rp.r > 1.15) { st.ripples.splice(i, 1); continue; }
        ctx.strokeStyle = 'rgba(212,175,55,' + rp.a.toFixed(2) + ')';
        ctx.lineWidth = 1.4;
        ctx.beginPath(); ctx.arc(R, R, rp.r * R, 0, 6.2832); ctx.stroke();
      }

      ctx.restore();

      var glowA = st.state === 'thinking' ? 0.5 + 0.3 * Math.sin(st.t * 6)
        : st.state === 'speaking' ? 0.45 + 0.25 * Math.sin(st.t * 4) : 0.28;
      var glowC = st.state === 'thinking' ? '34,211,238' : '212,175,55';
      ctx.strokeStyle = 'rgba(' + glowC + ',' + glowA.toFixed(2) + ')';
      ctx.lineWidth = 1.6;
      ctx.beginPath(); ctx.arc(R, R, R - 1.5, 0, 6.2832); ctx.stroke();
    }

    function mount(host, size) {
      ensureImg();
      var api = { setState: function () {}, parallax: function () {}, destroy: function () {} };
      try {
        var cv = document.createElement('canvas');
        var ctx = cv.getContext('2d');
        if (!ctx) throw new Error('no2d');
        var dpr = Math.min(2, window.devicePixelRatio || 1);
        cv.width = Math.round(size * dpr); cv.height = Math.round(size * dpr);
        cv.style.width = '100%'; cv.style.height = '100%';
        cv.style.display = 'block'; cv.style.borderRadius = '50%';
        host.appendChild(cv);
        var st = {
          ctx: ctx, size: size, dpr: dpr, t: Math.random() * 40,
          state: 'idle', tx: 0, ty: 0, px: 0, py: 0,
          ripples: [], parts: [], glyphs: [], lastRipple: 0, dead: false
        };
        for (var k = 0; k < 44; k++) st.parts.push({
          x: Math.random(), y: Math.random(), r: 0.7 + Math.random() * 1.5,
          s: 0.02 + Math.random() * 0.05, tw: Math.random() * 6.28, gold: Math.random() < 0.32
        });
        for (var q = 0; q < GLYPHS.length; q++) st.glyphs.push({ ch: GLYPHS[q], a: q / GLYPHS.length * 6.2832 });
        instances.push(st);
        if (reduced) draw(st, 0.016); else kick();
        api.setState = function (s) { st.state = s; if (reduced) draw(st, 0.016); else kick(); };
        api.parallax = function (x, y) {
          st.tx = Math.max(-1, Math.min(1, x));
          st.ty = Math.max(-1, Math.min(1, y));
        };
        api.destroy = function () {
          st.dead = true;
          var ix = instances.indexOf(st);
          if (ix >= 0) instances.splice(ix, 1);
        };
      } catch (e) {
        var im = document.createElement('img');
        im.alt = 'Noah AI'; im.src = AVATAR_SRC;
        im.style.width = '100%'; im.style.height = '100%';
        im.style.objectFit = 'cover'; im.style.display = 'block'; im.style.borderRadius = '50%';
        host.appendChild(im);
      }
      return api;
    }

    return { mount: mount };
  })();

  var avatarCtl = { launcher: null, head: null };
  function setAvatarState(s) {
    try {
      if (avatarCtl.launcher) avatarCtl.launcher.setState(s);
      if (avatarCtl.head) avatarCtl.head.setState(s);
    } catch (e) {}
  }

  function buildWidget() {
    if (document.getElementById('noah-launcher')) return;
    /* One canonical Noah per page: the full coach chat owns pages that mount it
       (coach, cinema). The floating widget would be a competing second chat UI. */
    try { if (document.querySelector('[data-il-muse]')) return; } catch (e) {}
    var style = document.createElement('style');
    style.textContent = WIDGET_CSS;
    document.head.appendChild(style);

    var launcher = el('button', '', '<span class="noah-orb" aria-hidden="true"></span><span class="noah-ping"></span>');
    launcher.id = 'noah-launcher';
    launcher.setAttribute('aria-label', 'Chat with Noah AI');
    launcher.addEventListener('click', toggle);
    avatarCtl.launcher = NoahAvatar.mount(launcher.querySelector('.noah-orb'), 52);
    launcher.addEventListener('pointermove', function (e) {
      var r = launcher.getBoundingClientRect();
      avatarCtl.launcher.parallax(((e.clientX - r.left) / r.width - 0.5) * 2, ((e.clientY - r.top) / r.height - 0.5) * 2);
    });
    launcher.addEventListener('pointerleave', function () { avatarCtl.launcher.parallax(0, 0); });

    var panel = el('div', '');
    panel.id = 'noah-panel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Noah AI chat');
    panel.innerHTML =
      '<div id="noah-head"><span class="noah-avatar" aria-hidden="true"></span>' +
      '<span class="noah-title"><span class="noah-name">Noah AI</span><br>' +
      '<span class="noah-status"><span class="noah-dot"></span><span id="noah-status-text">On-device · site curriculum</span></span></span>' +
      '<button id="noah-close" aria-label="Close chat">×</button></div>' +
      '<div id="noah-msgs"></div>' +
      '<div id="noah-chips"></div>' +
      '<form id="noah-form"><textarea id="noah-input" rows="1" placeholder="Ask Noah AI anything…" aria-label="Message Noah AI"></textarea>' +
      '<button id="noah-send" type="submit">Send</button></form>' +
      '<div id="noah-foot">Noah AI · Interstitium Labs · answers from Enmanuel\'s distilled work</div>';
    avatarCtl.head = NoahAvatar.mount(panel.querySelector('.noah-avatar'), 40);

    document.body.appendChild(launcher);
    document.body.appendChild(panel);

    els = {
      launcher: launcher, panel: panel,
      msgs: panel.querySelector('#noah-msgs'),
      chips: panel.querySelector('#noah-chips'),
      form: panel.querySelector('#noah-form'),
      input: panel.querySelector('#noah-input'),
      send: panel.querySelector('#noah-send')
    };

    panel.querySelector('#noah-close').addEventListener('click', close);
    els.form.addEventListener('submit', function (e) { e.preventDefault(); sendText(els.input.value); els.input.value = ''; });
    els.input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); els.form.dispatchEvent(new Event('submit', { cancelable: true })); }
    });

    adaptiveChips().forEach(function (c) {
      var b = el('button', 'noah-chip', esc(c));
      b.type = 'button';
      b.addEventListener('click', function () { NoahStats.track('chip'); sendText(c); });
      els.chips.appendChild(b);
    });

    loadHistory();
    NoahStats.load();
    NoahStats.track('open');
    var greeted = false;
    try { greeted = sessionStorage.getItem('noah-ai-greeted') === '1'; } catch (e) {}
    history.forEach(function (m) {
      addMsg(m.role, m.role === 'user' ? esc(m.content) : mdLite(m.content));
    });
    if (!history.length && !greeted) {
      var rg = returningGreeting();
      addMsg('noah', rg || ('I am <b>Noah AI</b> — the resident intelligence of Interstitium Labs. ' +
        'Ask me about the curriculum, the projects, the code — or bring me a hypothesis and we will reason it through, Socratic-style.'));
      try { sessionStorage.setItem('noah-ai-greeted', '1'); } catch (e) {}
    }
    if (!greeted) {
      setTimeout(function () {
        if (!panel.classList.contains('open')) launcher.classList.add('attn');
      }, 6000);
    }
  }

  function open() {
    buildWidget();
    if (!els.panel) return; /* main coach chat owns this page — no floating widget */
    els.panel.classList.add('open');
    els.launcher.classList.remove('attn');
    setTimeout(function () { els.input.focus(); }, 320);
  }
  function close() {
    if (els.panel) els.panel.classList.remove('open');
  }
  function toggle() {
    buildWidget();
    if (!els.panel) return; /* main coach chat owns this page */
    if (els.panel.classList.contains('open')) close(); else open();
  }

  /* ================= Boot ========================================== */
  function boot() {
    if (!document.body) return;
    try { ensureKB(); } catch (e) {} /* preload the answer bundle */
    buildWidget();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  g.IL = g.IL || {};
  g.IL.noah = { ask: ask, configureLLM: configureLLM };
  g.IL.noahAI = {
    open: open, close: close, toggle: toggle,
    /* Local-first (2026-10-01, noah-recovery-2): on-device bundle answers first;
       remote only as a screened fallback. Same result shape as before. */
    ask: function (text, hist) {
      return ensureKB().then(function () {
        var local = askLocal(text);
        if (local.answered) {
          return { reply: local.reply, nudges: local.nudges, remote: false, local: true, notice: local.notice };
        }
        return askRemote(text, hist || []);
      });
    },
    endpoint: getEndpoint
  };
  /* Shared on-device knowledge API for the coach page (il-coach.js). */
  g.__ilNoahKB = {
    ensure: ensureKB,
    get: function () { return KB; },
    answer: answerFromKB
  };
})(typeof window !== 'undefined' ? window : this);
