/**
 * IL Immersive CLI v1.1.0 (2026-10-19; v1.0.0 2026-10-16) — type real kubectl / etcdctl / crictl / aws CLI syntax and the authored
 * glTF scene changes. Killercoda-style tasks (goal → ordered steps → verify) over the SAME in-browser rules
 * engine (il-immersive-sims.js) that drives the predict→reveal drills.
 *
 * Honest scope: this is a SIMULATED shell. Commands are parsed in the browser and mapped onto sim state; output
 * is computed from that state (kubectl-/etcdctl-/aws-shaped, not byte-identical to the real tools). There is no
 * real shell, no container, no cluster, no AWS account and no hosted lab fleet. Unmodelled commands say so
 * instead of inventing output. `fault …` is a lab-only fault-injection verb and is labelled as such.
 *
 * v1.1.0 (2026-10-19) — Lab Muse task coach (answer to Killercoda Brain): `check` verifies the active task like a
 * CHECK button and explains WHY the next step is not verified (out-of-order, right command / wrong cluster state,
 * live state not true, last command failed); a second failed check on the same step auto-offers a hint (tip only,
 * never the command); `solution` prints the exact command. Every step names the authored glTF nodes to look at
 * (focus regex, unit-tested against the .glb files), so the player can light up WHERE in the 3D scene to look.
 * Honest scope: the coach is deterministic rules over the same in-browser sim state — not an LLM, not reading a
 * real terminal; it knows only what the drill models.
 *
 * Pure + UMD so `node --test` exercises exactly what the browser runs.
 *   run(simId, state, line, ctx) → { out:[lines], exit, set:{statePatch}|null, events:[…], action, verb }
 *   taskStatus(simId, taskId, state, ctx) → { done, next, steps:[{ label, done, hint }] }
 * ctx is a per-terminal session object from newCtx(taskId): { seq, events:{name:[seq…]}, vars:{}, task, latched:{} }.
 */
(function (root, factory) {
  var api = factory(root);
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.ILImmersiveCLI = api;
})(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this), function (root) {
  'use strict';

  var HONESTY = 'Simulated shell over the in-browser rules engine — real CLI syntax, computed output. Not a real shell, not a cluster, no AWS account, no hosted lab fleet.';

  function Sims() {
    if (root && root.ILImmersiveSims) return root.ILImmersiveSims;
    try { if (typeof require === 'function') return require('./il-immersive-sims.js'); } catch (e) { /* browser */ }
    return null;
  }

  /* ── tokenizer + flag helpers ─────────────────────────────────────────── */
  function tokenize(line) {
    var s = String(line == null ? '' : line).replace(/^\s*\$\s+/, ''), out = [], cur = '', q = null, has = false;
    for (var i = 0; i < s.length; i++) {
      var c = s[i];
      if (q) { if (c === q) q = null; else cur += c; continue; }
      if (c === '"' || c === "'") { q = c; has = true; continue; }
      if (c === '\\' && i + 1 < s.length) { cur += s[++i]; has = true; continue; }
      if (/\s/.test(c)) { if (has || cur) { out.push(cur); cur = ''; has = false; } continue; }
      cur += c; has = true;
    }
    if (has || cur) out.push(cur);
    return out;
  }
  /** --name=v | --name v | -x v (aliases). Returns string, true (bare boolean flag) or null. */
  function flag(t, names) {
    names = [].concat(names);
    for (var i = 0; i < t.length; i++) {
      for (var j = 0; j < names.length; j++) {
        var n = names[j];
        if (t[i] === n) return (i + 1 < t.length && t[i + 1].charAt(0) !== '-') ? t[i + 1] : true;
        if (t[i].indexOf(n + '=') === 0) return t[i].slice(n.length + 1);
      }
    }
    return null;
  }
  function hasFlag(t, names) { return flag(t, names) !== null; }
  /** Positional args (drops flags and their values for the flags listed as taking a value). */
  function positional(t, valued) {
    valued = valued || [];
    var out = [];
    for (var i = 0; i < t.length; i++) {
      var a = t[i];
      if (a.charAt(0) === '-') { if (a.indexOf('=') < 0 && valued.indexOf(a) >= 0) i++; continue; }
      out.push(a);
    }
    return out;
  }
  var KUBECTL_VALUED = ['-n', '--namespace', '-o', '--output', '-p', '--patch', '--replicas', '--image', '-f', '--filename', '-l', '--selector', '--requests', '--type', '--context'];
  function pad(s, n) { s = String(s); while (s.length < n) s += ' '; return s; }
  function table(rows) {
    var w = [];
    rows.forEach(function (r) { r.forEach(function (c, i) { w[i] = Math.max(w[i] || 0, String(c).length); }); });
    return rows.map(function (r) { return r.map(function (c, i) { return i === r.length - 1 ? String(c) : pad(c, w[i] + 3); }).join('').replace(/\s+$/, ''); });
  }
  function res(out, exit, set, events, extra) {
    var r = { out: [].concat(out || []), exit: exit || 0, set: set || null, events: events || [] };
    for (var k in (extra || {})) r[k] = extra[k];
    return r;
  }
  function unmodelled(cmd, examples) {
    return res(['sim: `' + cmd + '` is not modelled in this drill (simulated shell — no output is invented).',
      'Try: ' + examples.slice(0, 4).join('  ·  ')], 2);
  }
  function refused() { return res(['The connection to the server 10.0.0.10:6443 was refused - did you specify the right host or port?'], 1, null, ['kubectl-refused']); }

  /** Strip env-assignments, `sudo`, and an `ssh HOST [cmd…]` prefix. Returns { host, t }. */
  function unwrap(t) {
    var host = null;
    t = t.slice();
    while (t.length && /^[A-Z_][A-Z0-9_]*=/.test(t[0])) t.shift();
    if (t[0] === 'ssh' && t.length >= 2) {
      host = t[1];
      t = t.slice(2);
      if (t.length === 1 && /\s/.test(t[0])) t = tokenize(t[0]);
      while (t.length && /^[A-Z_][A-Z0-9_]*=/.test(t[0])) t.shift();
    }
    if (t[0] === 'sudo') t = t.slice(1);
    if (t[0] === 'k') t[0] = 'kubectl';
    return { host: host, t: t };
  }
  var MANIFESTS = '/etc/kubernetes/manifests';
  /** `mv /etc/kubernetes/manifests/X.yaml /tmp/` → { component:X, up:false }; reverse → up:true. */
  function manifestMove(t) {
    if (t[0] !== 'mv' || t.length < 3) return null;
    var src = t[t.length - 2], dst = t[t.length - 1];
    var m = /([a-z0-9-]+)\.yaml$/.exec(src);
    if (!m) return null;
    var fromManifests = src.indexOf(MANIFESTS + '/') === 0;
    var toManifests = dst.replace(/\/$/, '') === MANIFESTS || dst.indexOf(MANIFESTS + '/') === 0;
    if (fromManifests && !toManifests) return { component: m[1], up: false };
    if (!fromManifests && toManifests) return { component: m[1], up: true };
    return null;
  }
  function faultArgs(t) { return t[0] === 'fault' ? t.slice(1) : null; }

  /* ── pack: etcd quorum (CKA cluster architecture) ─────────────────────── */
  var ETCD_IP = ['10.0.0.11', '10.0.0.12', '10.0.0.13'];
  var ETCD_ID = ['8e9e05c52164694d', '91bc3c398fb3c146', 'fd422379fda50e48'];
  function etcdUp(s) { return [!!s.m0, !!s.m1, !!s.m2]; }
  function etcdMemberIdx(name) {
    var m = /^(?:etcd|cp|controlplane)-?([0-2])$/.exec(name || '');
    return m ? +m[1] : -1;
  }
  var etcdPack = {
    sim: 'etcd-quorum',
    prompt: 'student@cp-0:~$',
    examples: ['etcdctl endpoint health --cluster', 'etcdctl member list', 'etcdctl endpoint status --cluster -w table',
      'kubectl create deployment web --image=nginx', 'fault stop etcd-1', 'ssh cp-1 sudo mv /etc/kubernetes/manifests/etcd.yaml /tmp/'],
    run: function (u, s, d, ctx) {
      var t = u.t, ups = etcdUp(s), q = d.metrics, upN = q.up;
      var f = faultArgs(t);
      if (f) {
        var i = etcdMemberIdx(f[1]);
        if ((f[0] === 'stop' || f[0] === 'start') && i >= 0) {
          var p = {}; p['m' + i] = f[0] === 'start';
          return res(['[lab fault injection] etcd-' + i + ' ' + (f[0] === 'start' ? 'started' : 'stopped') + ' (simulated)'], 0, p, [f[0] === 'start' ? 'member-start' : 'member-stop']);
        }
        return res(['usage: fault stop|start etcd-0|etcd-1|etcd-2   (lab-only fault injection)'], 2);
      }
      var mv = manifestMove(t);
      if (mv) {
        if (mv.component !== 'etcd') return unmodelled(t.join(' '), etcdPack.examples);
        var idx = etcdMemberIdx(u.host || 'cp-0');
        if (idx < 0) return res(['ssh: Could not resolve hostname ' + u.host + ' (this lab has cp-0, cp-1, cp-2)'], 255);
        var pp = {}; pp['m' + idx] = mv.up;
        return res([], 0, pp, [mv.up ? 'member-start' : 'member-stop']);
      }
      if (t[0] === 'etcdctl') {
        var sub = positional(t.slice(1), ['--endpoints', '-w', '--write-out', '--cacert', '--cert', '--key']);
        if (sub[0] === 'endpoint' && sub[1] === 'health') {
          var lines = [], bad = 0;
          for (var m = 0; m < 3; m++) {
            var ep = 'https://' + ETCD_IP[m] + ':2379';
            if (!ups[m]) { bad++; lines.push(ep + ' is unhealthy: failed to connect: dial tcp ' + ETCD_IP[m] + ':2379: connect: connection refused'); }
            else if (!q.writable) { bad++; lines.push(ep + ' is unhealthy: failed to commit proposal: context deadline exceeded'); }
            else lines.push(ep + ' is healthy: successfully committed proposal: took = ' + (2 + m * 0.7).toFixed(1) + 'ms');
          }
          if (bad) lines.push('Error: unhealthy cluster');
          var ev = ['health'];
          if (upN === 3) ev.push('health-all-ok');
          if (upN === 2) ev.push('health-degraded');
          if (!q.writable) ev.push('health-noquorum');
          return res(lines, bad ? 1 : 0, null, ev);
        }
        if (sub[0] === 'member' && sub[1] === 'list') {
          if (!q.writable) return res(['{"level":"warn","msg":"retrying of unary invoker failed","error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded"}', 'Error: context deadline exceeded'], 1, null, ['member-list-fail']);
          return res([0, 1, 2].map(function (k) {
            return ETCD_ID[k] + ', started, cp-' + k + ', https://' + ETCD_IP[k] + ':2380, https://' + ETCD_IP[k] + ':2379, false';
          }), 0, null, ['member-list']);
        }
        if (sub[0] === 'endpoint' && sub[1] === 'status') {
          var rows = [['ENDPOINT', 'ID', 'VERSION', 'DB SIZE', 'IS LEADER', 'RAFT TERM']], errs = [];
          for (var k = 0; k < 3; k++) {
            if (!ups[k]) { errs.push('Failed to get the status of endpoint https://' + ETCD_IP[k] + ':2379 (context deadline exceeded)'); continue; }
            rows.push(['https://' + ETCD_IP[k] + ':2379', ETCD_ID[k], '3.5.21', '24 MB', q.leader === k ? 'true' : 'false', String(q.writable ? 7 : 7 + upN)]);
          }
          return res(errs.concat(table(rows)), errs.length ? 1 : 0, null, ['endpoint-status' + (q.leader >= 0 ? '' : '-noleader')]);
        }
        return unmodelled(t.join(' '), etcdPack.examples);
      }
      if (t[0] === 'kubectl') {
        var verb = t[1];
        if (verb === 'create' || verb === 'apply' || verb === 'scale' || verb === 'delete' || verb === 'run' || verb === 'label') {
          if (!q.writable) return res(['Error from server: etcdserver: request timed out'], 1, null, ['write-fail']);
          var what = verb === 'create' && t[2] === 'deployment' && t[3] ? 'deployment.apps/' + t[3] + ' created'
            : (verb === 'run' && t[2] ? 'pod/' + t[2] + ' created' : 'write committed (' + verb + ')');
          return res([what], 0, null, ['write-ok', upN < 3 ? 'write-ok-degraded' : 'write-ok-healthy']);
        }
        return unmodelled(t.join(' '), etcdPack.examples);
      }
      return null;
    },
    tasks: [
      { id: 'tolerate-one', title: 'Prove 3 members tolerate one failure',
        goal: 'Stop one etcd member, show the cluster is still writable, then bring it back.',
        setup: { m0: true, m1: true, m2: true },
        steps: [
          { label: 'Stop one member (fault stop etcd-1, or move its static-pod manifest out on cp-1)', event: 'member-stop', hint: 'fault stop etcd-1' },
          { label: 'Check health while one member is down', event: 'health-degraded', hint: 'etcdctl endpoint health --cluster' },
          { label: 'Commit a write with 2/3 members up', event: 'write-ok-degraded', hint: 'kubectl create deployment web --image=nginx' },
          { label: 'Restore the member — 3/3 healthy', state: function (s) { return s.m0 && s.m1 && s.m2; }, hint: 'fault start etcd-1' }
        ] },
      { id: 'lose-quorum', title: 'Lose quorum, watch writes fail, recover',
        goal: 'Take two members down, observe that writes time out, then restore quorum and write again.',
        setup: { m0: true, m1: true, m2: true },
        steps: [
          { label: 'Bring the cluster below quorum (2 of 3 down)', state: function (s, d) { return !d.metrics.writable; }, hint: 'fault stop etcd-1  then  fault stop etcd-2' },
          { label: 'Attempt a write and see it time out', event: 'write-fail', hint: 'kubectl create deployment api --image=nginx' },
          { label: 'Restore quorum (at least 2 members up)', state: function (s, d) { return d.metrics.writable; }, hint: 'fault start etcd-1' },
          { label: 'Write succeeds again', event: 'write-ok', hint: 'kubectl create deployment api --image=nginx' }
        ] }
    ]
  };

  /* ── pack: control-plane component failures (CKA troubleshooting) ─────── */
  var CP_COMPONENT = { 'kube-apiserver': 'apiUp', 'kube-scheduler': 'schedUp', 'kube-controller-manager': 'cmUp' };
  var cpPack = {
    sim: 'control-plane-failure',
    prompt: 'student@controlplane:~$',
    examples: ['kubectl get nodes', 'kubectl get pods -n kube-system', 'kubectl scale deployment web --replicas=5', 'kubectl get pods',
      'sudo mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/', 'sudo crictl ps', 'ls /etc/kubernetes/manifests', 'ssh worker-2 sudo systemctl stop kubelet'],
    run: function (u, s, d, ctx) {
      var t = u.t, m = d.metrics, host = u.host || 'controlplane';
      var mv = manifestMove(t);
      if (mv) {
        if (host !== 'controlplane') return res(['mv: cannot stat \'' + t[t.length - 2] + '\': No such file or directory (static pods live on controlplane)'], 1);
        var key = CP_COMPONENT[mv.component];
        if (!key) return unmodelled(t.join(' '), cpPack.examples);
        var p = {}; p[key] = mv.up;
        return res([], 0, p, [mv.component.replace('kube-', '') + (mv.up ? '-started' : '-stopped')]);
      }
      if (t[0] === 'systemctl' || t[0] === 'service') {
        var act = t[0] === 'service' ? t[2] : t[1], unit = t[0] === 'service' ? t[1] : t[2];
        if (unit !== 'kubelet') return unmodelled(t.join(' '), cpPack.examples);
        var onW2 = host === 'worker-2';
        if (act === 'status') {
          var running = onW2 ? s.kubelet2Up : true;
          return res(['● kubelet.service - kubelet: The Kubernetes Node Agent', '     Active: ' + (running ? 'active (running)' : 'inactive (dead)')], running ? 0 : 3);
        }
        if (!onW2) return res(['sim: only the kubelet on worker-2 is modelled — try: ssh worker-2 sudo systemctl ' + act + ' kubelet'], 2);
        if (act === 'stop') return res([], 0, { kubelet2Up: false }, ['kubelet-stopped']);
        if (act === 'start' || act === 'restart') return res([], 0, { kubelet2Up: true }, ['kubelet-started']);
        return unmodelled(t.join(' '), cpPack.examples);
      }
      if (t[0] === 'ls' && /^\/etc\/kubernetes\/manifests\/?$/.test(t[t.length - 1] || '')) {
        if (host !== 'controlplane') return res(["ls: cannot access '" + MANIFESTS + "': No such file or directory"], 2);
        var files = ['etcd.yaml'];
        if (s.apiUp) files.push('kube-apiserver.yaml');
        if (s.cmUp) files.push('kube-controller-manager.yaml');
        if (s.schedUp) files.push('kube-scheduler.yaml');
        return res([files.join('  ')], 0, null, ['ls-manifests']);
      }
      if (t[0] === 'crictl' && t[1] === 'ps') {
        if (host !== 'controlplane') return res(['CONTAINER   IMAGE   STATE   NAME', '(sim: worker containers are not modelled; web pods keep running)'], 0, null, ['crictl']);
        var rows = [['CONTAINER', 'STATE', 'NAME', 'POD']];
        rows.push(['3f1c9a2b7e10', 'Running', 'etcd', 'etcd-controlplane']);
        if (s.apiUp) rows.push(['a81d02c4f5e3', 'Running', 'kube-apiserver', 'kube-apiserver-controlplane']);
        if (s.cmUp) rows.push(['c0ffee12ab34', 'Running', 'kube-controller-manager', 'kube-controller-manager-controlplane']);
        if (s.schedUp) rows.push(['5ced01e9d7aa', 'Running', 'kube-scheduler', 'kube-scheduler-controlplane']);
        return res(table(rows), 0, null, ['crictl', s.apiUp ? 'crictl-api-up' : 'crictl-api-down']);
      }
      if (t[0] !== 'kubectl') return null;
      if (!s.apiUp) return refused();
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED);
      var ns = flag(t, ['-n', '--namespace']) || 'default';
      var want = ctx.vars.webReplicas || 3;
      if (verb === 'get' && /^(nodes?|no)$/.test(args[0] || '')) {
        var rows2 = [['NAME', 'STATUS', 'ROLES', 'AGE', 'VERSION'], ['controlplane', 'Ready', 'control-plane', '41d', 'v1.36.1']];
        for (var w = 0; w < 5; w++) rows2.push(['worker-' + w, w === 2 && m.worker2NotReady ? 'NotReady' : 'Ready', '<none>', '41d', 'v1.36.1']);
        return res(table(rows2), 0, null, ['get-nodes', m.worker2NotReady ? 'get-nodes-notready' : 'get-nodes-ready']);
      }
      if (verb === 'get' && /^(pods?|po)$/.test(args[0] || '')) {
        if (ns === 'kube-system') {
          var r3 = [['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE'], ['etcd-controlplane', '1/1', 'Running', '0', '41d'], ['kube-apiserver-controlplane', '1/1', 'Running', '0', '41d']];
          if (s.cmUp) r3.push(['kube-controller-manager-controlplane', '1/1', 'Running', '0', '41d']);
          if (s.schedUp) r3.push(['kube-scheduler-controlplane', '1/1', 'Running', '0', '41d']);
          return res(table(r3), 0, null, ['get-kube-system']);
        }
        var have = ctx.vars.webCreated == null ? 3 : ctx.vars.webCreated;
        var rows4 = [['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE', 'NODE']], names = ['web-7c5d8-2xkqp', 'web-7c5d8-9hj4w', 'web-7c5d8-tm6rb', 'web-7c5d8-v8wcz', 'web-7c5d8-zq7ln', 'web-7c5d8-b4nfx'];
        var pending = 0;
        for (var i = 0; i < Math.min(have, 6); i++) {
          var isNew = i >= 3, bound = !isNew || ctx.vars.webBound > i - 3;
          if (!bound) pending++;
          rows4.push([names[i], bound ? '1/1' : '0/1', bound ? 'Running' : 'Pending', '0', isNew ? '8s' : '3d', bound ? 'worker-' + (i % 5 === 2 && m.worker2NotReady ? 3 : i % 5) : '<none>']);
        }
        return res(table(rows4), 0, null, ['get-pods', pending ? 'get-pods-pending' : 'get-pods-all-running']);
      }
      if (verb === 'scale') {
        var target = (args[0] === 'deployment' || args[0] === 'deploy') ? args[1] : String(args[0] || '').replace(/^(deployment|deploy)(\.apps)?\//, '');
        var n = parseInt(flag(t, '--replicas'), 10);
        if (target !== 'web' || !(n >= 0)) return res(['sim: this drill models `kubectl scale deployment web --replicas=N` (N 0–6)'], 2);
        n = Math.min(n, 6);
        ctx.vars.webReplicas = n;
        var ev = ['scale'];
        if (n > 3) ev.push(m.controllerPods === 'pending' ? 'scale-pending' : (m.controllerPods === 'not-created' ? 'scale-not-created' : 'scale-scheduled'));
        return res(['deployment.apps/web scaled'], 0, null, ev);
      }
      if (verb === 'get' && /^(deploy|deployments?)$/.test(args[0] || '')) {
        var created = ctx.vars.webCreated == null ? 3 : ctx.vars.webCreated, ready = Math.min(created, 3 + (ctx.vars.webBound || 0));
        return res(table([['NAME', 'READY', 'UP-TO-DATE', 'AVAILABLE', 'AGE'], ['web', ready + '/' + want, String(created), String(ready), '3d']]), 0, null, ['get-deploy']);
      }
      return unmodelled(t.join(' '), cpPack.examples);
    },
    /** Reconcile CLI-only vars (desired replicas) against component health after every state change. */
    reconcile: function (s, d, ctx) {
      var want = ctx.vars.webReplicas || 3, m = d.metrics;
      if (s.apiUp && s.cmUp) ctx.vars.webCreated = want; /* ReplicaSet controller creates pod objects */
      var created = ctx.vars.webCreated == null ? 3 : ctx.vars.webCreated;
      if (s.apiUp && s.schedUp) ctx.vars.webBound = Math.max(0, created - 3);
      else ctx.vars.webBound = Math.min(ctx.vars.webBound || 0, Math.max(0, created - 3));
      return m;
    },
    tasks: [
      { id: 'pending-scale', title: 'Diagnose a scale-up stuck in Pending',
        goal: 'Break the scheduler, scale web to 5, find the Pending pods, then fix the scheduler so they bind.',
        setup: { apiUp: true, schedUp: true, cmUp: true, kubelet2Up: true },
        steps: [
          { label: 'Stop kube-scheduler (move its static-pod manifest out of /etc/kubernetes/manifests)', event: 'scheduler-stopped', hint: 'sudo mv /etc/kubernetes/manifests/kube-scheduler.yaml /tmp/' },
          { label: 'Scale web from 3 to 5 replicas', event: 'scale-pending', hint: 'kubectl scale deployment web --replicas=5' },
          { label: 'Find the Pending pods (no NODE assigned)', event: 'get-pods-pending', hint: 'kubectl get pods' },
          { label: 'Restore the scheduler manifest', event: 'scheduler-started', hint: 'sudo mv /tmp/kube-scheduler.yaml /etc/kubernetes/manifests/' },
          { label: 'Confirm every web pod is Running', event: 'get-pods-all-running', hint: 'kubectl get pods' }
        ] },
      { id: 'api-blind', title: 'API server down: kubectl is blind, crictl is not',
        goal: 'Take kube-apiserver down, see kubectl fail, inspect the node with crictl, then restore it.',
        setup: { apiUp: true, schedUp: true, cmUp: true, kubelet2Up: true },
        steps: [
          { label: 'Stop kube-apiserver (move its manifest out)', event: 'apiserver-stopped', hint: 'sudo mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/' },
          { label: 'Watch kubectl lose the API', event: 'kubectl-refused', hint: 'kubectl get nodes' },
          { label: 'Inspect control-plane containers without the API', event: 'crictl-api-down', hint: 'sudo crictl ps' },
          { label: 'Restore kube-apiserver; kubectl works again', event: 'get-nodes', hint: 'sudo mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/  then  kubectl get nodes' }
        ] },
      { id: 'notready', title: 'NotReady node: whose job is it to notice?',
        goal: 'Stop the kubelet on worker-2 and watch the node go NotReady; then start it again.',
        setup: { apiUp: true, schedUp: true, cmUp: true, kubelet2Up: true },
        steps: [
          { label: 'Stop the kubelet on worker-2', event: 'kubelet-stopped', hint: 'ssh worker-2 sudo systemctl stop kubelet' },
          { label: 'See worker-2 NotReady', event: 'get-nodes-notready', hint: 'kubectl get nodes' },
          { label: 'Start the kubelet and confirm all nodes Ready', event: 'get-nodes-ready', hint: 'ssh worker-2 sudo systemctl start kubelet  then  kubectl get nodes' }
        ] }
    ]
  };

  /* ── pack: scheduling — cordon · taints · labels (CKA workloads) ──────── */
  function dbReasons(s) {
    /* Default-scheduler filter order: NodeUnschedulable → TaintToleration → NodeAffinity; first failure per node. */
    var tally = {}, order = [];
    function add(r) { if (!tally[r]) { tally[r] = 0; order.push(r); } tally[r]++; }
    if (s.aCordoned) add("node(s) were unschedulable"); else add("node(s) didn't match Pod's node affinity/selector");
    add('node(s) had untolerated taint {gpu: true}');
    if (s.cTaint) add('node(s) had untolerated taint {maintenance: true}');
    else if (!s.cNvme) add("node(s) didn't match Pod's node affinity/selector");
    return order.map(function (r) { return tally[r] + ' ' + r; });
  }
  var schedPack = {
    sim: 'sched-taints',
    prompt: 'student@controlplane:~$',
    examples: ['kubectl get pods -o wide', 'kubectl describe pod db', 'kubectl get nodes', 'kubectl label nodes node-c disktype=nvme --overwrite',
      'kubectl taint nodes node-c maintenance=true:NoExecute-', 'kubectl cordon node-a'],
    run: function (u, s, d, ctx) {
      var t = u.t;
      if (t[0] !== 'kubectl') return null;
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED), m = d.metrics;
      function where(n) { return n ? 'node-' + n : '<none>'; }
      if (verb === 'cordon' || verb === 'uncordon') {
        if (args[0] !== 'node-a') return res(['sim: this drill models cordon/uncordon on node-a only'], 2);
        var on = verb === 'cordon';
        return res(['node/node-a ' + (on === !!s.aCordoned ? 'already ' : '') + verb + 'ed'], 0, { aCordoned: on }, [verb]);
      }
      if (verb === 'drain') return res(['sim: drain = cordon + evict. This drill models cordon only — try: kubectl cordon node-a'], 2);
      if (verb === 'taint') {
        var a = args[0] === 'nodes' || args[0] === 'node' || args[0] === 'no' ? args.slice(1) : args;
        var node = (a[0] || '').replace(/^nodes?\//, ''), spec = a[1] || '';
        if (node !== 'node-c' || !/^maintenance/.test(spec)) return res(['sim: this drill models the maintenance taint on node-c only (e.g. kubectl taint nodes node-c maintenance=true:NoExecute-)'], 2);
        var remove = /-$/.test(spec);
        if (remove && !s.cTaint) return res(['error: taint "maintenance:NoExecute" not found'], 1);
        if (!remove && s.cTaint && !hasFlag(t, '--overwrite')) return res(["error: node node-c already has maintenance taint(s) with same effect(s) and --overwrite is false"], 1);
        if (!remove && !/:NoExecute$/.test(spec)) return res(['sim: this drill models effect NoExecute only (maintenance=true:NoExecute)'], 2);
        return res(['node/node-c ' + (remove ? 'untainted' : 'tainted')], 0, { cTaint: !remove }, [remove ? 'untaint' : 'taint']);
      }
      if (verb === 'label') {
        var b = args[0] === 'nodes' || args[0] === 'node' || args[0] === 'no' ? args.slice(1) : args;
        var nd = (b[0] || '').replace(/^nodes?\//, ''), kv = /^disktype=(nvme|hdd)$/.exec(b[1] || '');
        if (nd !== 'node-c' || !kv) return res(['sim: this drill models `kubectl label nodes node-c disktype=nvme|hdd --overwrite`'], 2);
        var cur = s.cNvme ? 'nvme' : 'hdd';
        if (!hasFlag(t, '--overwrite')) return res(["error: 'disktype' already has a value (" + cur + "), and --overwrite is false"], 1, null, ['label-no-overwrite']);
        return res([kv[1] === cur ? 'node/node-c not labeled' : 'node/node-c labeled'], 0, { cNvme: kv[1] === 'nvme' }, ['label']);
      }
      if (verb === 'get' && /^(nodes?|no)$/.test(args[0] || '')) {
        var showLabels = hasFlag(t, '--show-labels');
        var rows = [['NAME', 'STATUS', 'ROLES', 'AGE', 'VERSION'].concat(showLabels ? ['LABELS'] : [])];
        rows.push(['node-a', s.aCordoned ? 'Ready,SchedulingDisabled' : 'Ready', '<none>', '9d', 'v1.36.1'].concat(showLabels ? ['disktype=ssd'] : []));
        rows.push(['node-b', 'Ready', '<none>', '9d', 'v1.36.1'].concat(showLabels ? ['zone=us-east-1b'] : []));
        rows.push(['node-c', 'Ready', '<none>', '9d', 'v1.36.1'].concat(showLabels ? ['disktype=' + (s.cNvme ? 'nvme' : 'hdd')] : []));
        return res(table(rows), 0, null, ['get-nodes']);
      }
      if (verb === 'get' && /^(pods?|po)$/.test(args[0] || '')) {
        var rows2 = [['NAME', 'READY', 'STATUS', 'NODE']];
        rows2.push(['web-5d9c7-a1', '1/1', 'Running', 'node-a']);
        rows2.push(['web-5d9c7-a2', m.webNewReplica ? '1/1' : '0/1', m.webNewReplica ? 'Running' : 'Pending', where(m.webNewReplica)]);
        rows2.push(['trainer', m.trainer ? '1/1' : '0/1', m.trainer ? 'Running' : 'Pending', where(m.trainer)]);
        rows2.push(['db', m.db ? '1/1' : '0/1', m.db ? 'Running' : 'Pending', where(m.db)]);
        var ev = ['get-pods', m.db ? 'get-pods-db-running' : 'get-pods-db-pending'];
        if (!m.webNewReplica) ev.push('get-pods-web-pending');
        return res(table(rows2), 0, null, ev);
      }
      if (verb === 'describe' && /^(pods?|po)$/.test(args[0] || '') && args[1] === 'db' || (verb === 'describe' && args[0] === 'pod/db')) {
        var lines = ['Name:         db', 'Node:         ' + (m.db ? 'node-' + m.db : '<none>'), 'Status:       ' + (m.db ? 'Running' : 'Pending'),
          'Node-Selectors / affinity: requiredDuringScheduling disktype In [nvme]', 'Tolerations:  node.kubernetes.io/not-ready:NoExecute op=Exists for 300s', 'Events:'];
        if (m.db) lines.push('  Normal   Scheduled  default-scheduler  Successfully assigned default/db to node-' + m.db);
        else lines.push('  Warning  FailedScheduling  default-scheduler  0/3 nodes are available: ' + dbReasons(s).join(', ') + '. preemption: 0/3 nodes are available: 3 Preemption is not helpful for scheduling.');
        return res(lines, 0, null, [m.db ? 'describe-db-scheduled' : 'describe-db-pending']);
      }
      return unmodelled(t.join(' '), schedPack.examples);
    },
    tasks: [
      { id: 'schedule-db', title: 'Get the Pending db pod scheduled',
        goal: 'db needs disktype=nvme and tolerates nothing. Read the scheduler’s reason, then fix node-c so db binds there.',
        setup: { aCordoned: false, trainerTol: true, cNvme: false, cTaint: true },
        steps: [
          { label: 'Read why db is Pending (FailedScheduling event)', event: 'describe-db-pending', hint: 'kubectl describe pod db' },
          { label: 'Label node-c disktype=nvme (it already has a value)', state: function (s) { return !!s.cNvme; }, hint: 'kubectl label nodes node-c disktype=nvme --overwrite' },
          { label: 'Remove node-c’s maintenance:NoExecute taint', state: function (s) { return !s.cTaint; }, hint: 'kubectl taint nodes node-c maintenance=true:NoExecute-' },
          { label: 'Confirm db is Running on node-c', event: 'get-pods-db-running', hint: 'kubectl get pods -o wide' }
        ] },
      { id: 'cordon', title: 'Cordon vs drain',
        goal: 'Cordon node-a and show the running web pod survives while a new replica goes Pending; then uncordon.',
        setup: { aCordoned: false, trainerTol: true, cNvme: false, cTaint: true },
        steps: [
          { label: 'Cordon node-a', event: 'cordon', hint: 'kubectl cordon node-a' },
          { label: 'See node-a SchedulingDisabled, web-…-a1 still Running, the new replica Pending', event: 'get-pods-web-pending', hint: 'kubectl get pods -o wide' },
          { label: 'Uncordon node-a', state: function (s) { return !s.aCordoned; }, hint: 'kubectl uncordon node-a' }
        ] }
    ]
  };

  /* ── pack: HPA (autoscaling/v2) ───────────────────────────────────────── */
  var hpaPack = {
    sim: 'hpa-scale',
    prompt: 'student@controlplane:~$',
    examples: ['kubectl get hpa', 'kubectl describe hpa web', 'kubectl top pods', 'kubectl set resources deployment web --requests=cpu=200m',
      "kubectl patch hpa web -p '{\"spec\":{\"maxReplicas\":5}}'", 'kubectl run load-generator --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://web; done"'],
    run: function (u, s, d, ctx) {
      var t = u.t, m = d.metrics;
      var f = faultArgs(t);
      if (f) {
        if (f[0] === 'load' && (f[1] === 'spike' || f[1] === 'normal')) return res(['[lab fault injection] load → ' + f[1] + ' (simulated)'], 0, { spike: f[1] === 'spike' }, [f[1] === 'spike' ? 'load-started' : 'load-stopped']);
        return res(['usage: fault load spike|normal   (lab-only fault injection)'], 2);
      }
      if (t[0] !== 'kubectl') return null;
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED), ns = flag(t, ['-n', '--namespace']) || 'default';
      if (verb === 'run' && /^load/.test(args[0] || '')) {
        if (s.spike) return res(['Error from server (AlreadyExists): pods "' + args[0] + '" already exists'], 1);
        return res(['pod/' + args[0] + ' created'], 0, { spike: true }, ['load-started']);
      }
      if (verb === 'delete' && (/^(pods?|po)$/.test(args[0] || '') && /^load/.test(args[1] || '') || /^pod\/load/.test(args[0] || ''))) {
        if (!s.spike) return res(['Error from server (NotFound): pods "load-generator" not found'], 1);
        return res(['pod "load-generator" deleted'], 0, { spike: false }, ['load-stopped']);
      }
      if (verb === 'scale' && ns === 'kube-system' && /metrics-server/.test(args.join(' '))) {
        var n = parseInt(flag(t, '--replicas'), 10);
        if (!(n >= 0)) return res(['error: --replicas is required'], 1);
        return res(['deployment.apps/metrics-server scaled'], 0, { metricsUp: n > 0 }, [n > 0 ? 'metrics-up' : 'metrics-down']);
      }
      if (verb === 'set' && args[0] === 'resources') {
        var req = flag(t, '--requests') || '';
        var cpu = /cpu=([0-9]+m?)/.exec(req);
        if (!cpu) return res(['sim: this drill models `kubectl set resources deployment web --requests=cpu=200m`'], 2);
        var ok = cpu[1] !== '0' && cpu[1] !== '0m';
        return res(['deployment.apps/web resource requirements updated'], 0, { requestsSet: ok }, ['requests-set']);
      }
      if (verb === 'patch' && /^(hpa|horizontalpodautoscalers?)/.test(args[0] || '')) {
        var raw = flag(t, ['-p', '--patch']), mx = null;
        try { mx = JSON.parse(raw).spec.maxReplicas; } catch (e) { return res(['error: unable to parse "' + raw + '": invalid JSON patch'], 1); }
        if (mx !== 3 && mx !== 5) return res(['sim: this drill models maxReplicas 3 or 5'], 2);
        return res(['horizontalpodautoscaler.autoscaling/web patched'], 0, { max5: mx === 5 }, ['patched-max-' + mx]);
      }
      if (verb === 'top' && /^(pods?|po)$/.test(args[0] || '')) {
        if (!s.metricsUp) return res(['error: Metrics API not available'], 1, null, ['top-fail']);
        var mc = s.spike ? 240 : 80, rows = [['NAME', 'CPU(cores)', 'MEMORY(bytes)']];
        for (var i = 0; i < m.desired; i++) rows.push(['web-6b9f-' + 'abcde'[i], (i < 2 ? mc : Math.round(mc * 2 / m.desired)) + 'm', '21Mi']);
        return res(table(rows), 0, null, ['top']);
      }
      if (verb === 'get' && /^(hpa|horizontalpodautoscalers?)$/.test(args[0] || '')) {
        var tgt = m.canCompute ? m.util + '%/50%' : '<unknown>/50%';
        var ev = ['get-hpa', m.canCompute ? 'get-hpa-ok' : 'get-hpa-unknown'];
        if (m.canCompute && m.desired >= 5) ev.push('get-hpa-5');
        if (m.limited) ev.push('get-hpa-limited');
        return res(table([['NAME', 'REFERENCE', 'TARGETS', 'MINPODS', 'MAXPODS', 'REPLICAS', 'AGE'], ['web', 'Deployment/web', 'cpu: ' + tgt, '2', String(m.max), String(m.desired), '12m']]), 0, null, ev);
      }
      if (verb === 'describe' && /^(hpa|horizontalpodautoscalers?)/.test(args[0] || '')) {
        var lines = ['Name:                     web', 'Reference:                Deployment/web',
          'Metrics:                  ( current / target )', '  resource cpu on pods  (as a percentage of request):  ' + (m.canCompute ? m.util + '% (' + (s.spike ? 240 : 80) + 'm)' : '<unknown>') + ' / 50%',
          'Min replicas:             2', 'Max replicas:             ' + m.max, 'Conditions:', '  Type            Status  Reason'];
        lines.push('  AbleToScale     True    ' + (m.canCompute && m.desired !== 2 ? 'SucceededRescale' : 'ReadyForNewScale'));
        if (m.canCompute) lines.push('  ScalingActive   True    ValidMetricFound');
        else lines.push('  ScalingActive   False   FailedGetResourceMetric  ' + (!s.metricsUp ? 'unable to get metrics for resource cpu: unable to fetch metrics from resource metrics API' : 'failed to get cpu utilization: missing request for cpu in container web'));
        lines.push('  ScalingLimited  ' + (m.limited ? 'True    TooManyReplicas  the desired replica count is more than the maximum replica count' : 'False   DesiredWithinRange'));
        return res(lines, 0, null, ['describe-hpa', m.limited ? 'describe-limited' : 'describe-in-range', m.canCompute ? 'describe-active' : 'describe-inactive']);
      }
      return unmodelled(t.join(' '), hpaPack.examples);
    },
    tasks: [
      { id: 'unknown-target', title: 'Fix TARGETS <unknown>',
        goal: 'Traffic is spiking but the HPA will not scale. Find out why, fix the Deployment, and watch it scale to 5.',
        setup: { spike: true, metricsUp: true, requestsSet: false, max5: true },
        steps: [
          { label: 'See TARGETS <unknown>/50%', event: 'get-hpa-unknown', hint: 'kubectl get hpa' },
          { label: 'Read the FailedGetResourceMetric condition', event: 'describe-inactive', hint: 'kubectl describe hpa web' },
          { label: 'Give the container a CPU request', state: function (s) { return !!s.requestsSet; }, hint: 'kubectl set resources deployment web --requests=cpu=200m' },
          { label: 'Confirm the HPA computes 5 replicas', event: 'get-hpa-5', hint: 'kubectl get hpa' }
        ] },
      { id: 'ceiling', title: 'Hit the maxReplicas ceiling, then lift it',
        goal: 'Start load with maxReplicas 3, find ScalingLimited, raise the ceiling to 5.',
        setup: { spike: false, metricsUp: true, requestsSet: true, max5: false },
        steps: [
          { label: 'Start a load generator', event: 'load-started', hint: 'kubectl run load-generator --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://web; done"' },
          { label: 'Find ScalingLimited=True (TooManyReplicas)', event: 'describe-limited', hint: 'kubectl describe hpa web' },
          { label: 'Raise maxReplicas to 5', state: function (s) { return !!s.max5; }, hint: "kubectl patch hpa web -p '{\"spec\":{\"maxReplicas\":5}}'" },
          { label: 'Confirm 5 replicas', event: 'get-hpa-5', hint: 'kubectl get hpa' }
        ] }
    ]
  };

  /* ── pack: AWS Multi-AZ (SAA-C03) ─────────────────────────────────────── */
  function azKey(name) { return name === 'us-east-1a' || name === 'a' ? 'azA' : (name === 'us-east-1b' || name === 'b' ? 'azB' : null); }
  var awsPack = {
    sim: 'aws-az-failure',
    prompt: 'student@il-sim:~$',
    examples: ['aws rds describe-db-instances --db-instance-identifier shop-db', 'aws rds modify-db-instance --db-instance-identifier shop-db --multi-az --apply-immediately',
      'aws elbv2 describe-target-health --target-group-arn shop-web-tg', 'curl -sI https://shop.example.com', 'fault az us-east-1a down'],
    run: function (u, s, d, ctx) {
      var t = u.t, h = d.metrics;
      var f = faultArgs(t);
      if (f) {
        var k = f[0] === 'az' ? azKey(f[1]) : null;
        if (k && (f[2] === 'down' || f[2] === 'up')) {
          var p = {}; p[k] = f[2] === 'up';
          return res(['[lab fault injection] ' + f[1] + ' ' + (f[2] === 'up' ? 'restored' : 'outage') + ' (simulated — no AWS account is touched)'], 0, p, ['az-' + f[2]]);
        }
        return res(['usage: fault az us-east-1a|us-east-1b down|up   (lab-only fault injection)'], 2);
      }
      if (t[0] === 'curl') {
        var both = h.azUp.a && h.azUp.b;
        if (h.serving) return res(['HTTP/2 200', 'server: awselb/2.0', 'x-sim-note: computed by the rules engine'], 0, null, ['curl-200', both ? 'curl-200-healthy' : 'curl-200-degraded']);
        /* curl exits 0 on an HTTP 503 unless -f/--fail is given (then 22). */
        var failFlag = t.some(function (a) { return a === '--fail' || /^-[a-zA-Z]*f[a-zA-Z]*$/.test(a); });
        return res(['HTTP/2 503', 'server: awselb/2.0', 'x-sim-note: ' + (h.app ? 'web tier up, no database writer' : 'no healthy targets')], failFlag ? 22 : 0, null, ['curl-503']);
      }
      if (t[0] !== 'aws') return null;
      var svc = t[1], op = t[2];
      if (svc === 'rds' && op === 'describe-db-instances') {
        var status = h.dbWriter ? 'available' : 'unreachable (sim: its only AZ is down)';
        var o = { DBInstances: [{ DBInstanceIdentifier: 'shop-db', Engine: 'postgres', DBInstanceStatus: status, MultiAZ: !!s.multiAz,
          AvailabilityZone: h.dbWriter ? 'us-east-1' + h.dbWriter : 'us-east-1a', Endpoint: { Address: 'shop-db.c9xyz.us-east-1.rds.amazonaws.com', Port: 5432 } }] };
        if (s.multiAz) o.DBInstances[0].SecondaryAvailabilityZone = h.dbWriter === 'b' ? 'us-east-1a' : 'us-east-1b';
        return res(JSON.stringify(o, null, 2).split('\n'), 0, null, ['describe-db', s.multiAz ? 'describe-db-multiaz' : 'describe-db-single']);
      }
      if (svc === 'rds' && op === 'modify-db-instance') {
        var on = hasFlag(t, '--multi-az'), off = hasFlag(t, '--no-multi-az');
        if (flag(t, '--db-instance-identifier') !== 'shop-db' || on === off) return res(['sim: this drill models `aws rds modify-db-instance --db-instance-identifier shop-db --multi-az|--no-multi-az --apply-immediately`'], 2);
        var lines = JSON.stringify({ DBInstance: { DBInstanceIdentifier: 'shop-db', DBInstanceStatus: 'modifying', MultiAZ: !!s.multiAz, PendingModifiedValues: { MultiAZ: on } } }, null, 2).split('\n');
        lines.push('# sim: applied instantly' + (hasFlag(t, '--apply-immediately') ? '' : ' (without --apply-immediately AWS waits for the maintenance window)') + '; a real conversion takes minutes');
        return res(lines, 0, { multiAz: on }, [on ? 'multiaz-on' : 'multiaz-off']);
      }
      if (svc === 'elbv2' && op === 'describe-target-health') {
        var td = [];
        [['a', 'i-0a1f00d5e7c1'], ['b', 'i-0b2c4e6a8d03']].forEach(function (x) {
          td.push({ Target: { Id: x[1], Port: 80, AvailabilityZone: 'us-east-1' + x[0] }, TargetHealth: h.azUp[x[0]] ? { State: 'healthy' } : { State: 'unhealthy', Reason: 'Target.Timeout' } });
        });
        if (h.surge) td.push({ Target: { Id: 'i-0c3d5f7b9e15', Port: 80, AvailabilityZone: 'us-east-1' + h.surge }, TargetHealth: { State: 'initial', Reason: 'Elb.RegistrationInProgress' } });
        return res(JSON.stringify({ TargetHealthDescriptions: td }, null, 2).split('\n'), 0, null, ['target-health']);
      }
      return unmodelled(t.join(' '), awsPack.examples);
    },
    tasks: [
      { id: 'survive-az', title: 'Make shop survive an AZ outage',
        goal: 'shop-db is Single-AZ. Confirm it, convert it to Multi-AZ, then fail us-east-1a and prove the site still answers 200.',
        setup: { azA: true, azB: true, multiAz: false },
        steps: [
          { label: 'Confirm shop-db is Single-AZ', event: 'describe-db-single', hint: 'aws rds describe-db-instances --db-instance-identifier shop-db' },
          { label: 'Convert shop-db to Multi-AZ', state: function (s) { return !!s.multiAz; }, hint: 'aws rds modify-db-instance --db-instance-identifier shop-db --multi-az --apply-immediately' },
          { label: 'Fail us-east-1a', state: function (s) { return !s.azA; }, hint: 'fault az us-east-1a down' },
          { label: 'Prove the site still serves (200) during the outage', event: 'curl-200-degraded', hint: 'curl -sI https://shop.example.com' }
        ] },
      { id: 'spof', title: 'Prove Single-AZ RDS is a single point of failure',
        goal: 'With Single-AZ RDS, fail us-east-1a and watch the site go 503 even though the web tier survives.',
        setup: { azA: true, azB: true, multiAz: false },
        steps: [
          { label: 'Fail us-east-1a', state: function (s) { return !s.azA; }, hint: 'fault az us-east-1a down' },
          { label: 'See the site answer 503', event: 'curl-503', hint: 'curl -sI https://shop.example.com' },
          { label: 'Find the cause: the ALB still has a healthy target in 1b — the Single-AZ database is the SPOF', event: 'target-health', hint: 'aws elbv2 describe-target-health --target-group-arn shop-web-tg' }
        ] }
    ]
  };

  var PACKS = {};
  [etcdPack, cpPack, schedPack, hpaPack, awsPack].forEach(function (p) { PACKS[p.sim] = p; });

  /* ── Lab Muse coach content (v1.1.0): per step [nudge (tip, never the command), focus (authored glTF node regex)] ── */
  var COACH = {
    'etcd-quorum': {
      'tolerate-one': [
        ['Take exactly one member offline. The lab has a fault verb, or do it the CKA way: a static pod disappears when its manifest leaves /etc/kubernetes/manifests on that node.', '^etcd-(member|heart)-1$'],
        ['Ask etcd itself, across the whole cluster, which endpoints are healthy.', '^etcd-heart-[0-2]$'],
        ['Any kubectl write goes through the API server into etcd. With 2 of 3 up, does Raft still commit it?', '^(apiserver-front|raft-link-.*)$'],
        ['Undo the failure you injected and confirm all three members are back.', '^etcd-(member|heart)-1$']
      ],
      'lose-quorum': [
        ['Quorum for 3 members is 2. Take members down until fewer than 2 are left.', '^etcd-(member|heart)-[12]$'],
        ['Try any kubectl write now and read the error carefully.', '^apiserver-front$'],
        ['One member back is enough: 2 of 3 is a majority again.', '^etcd-(member|heart)-1$'],
        ['Repeat the write that failed.', '^(apiserver-front|raft-link-.*)$']
      ]
    },
    'control-plane-failure': {
      'pending-scale': [
        ['The scheduler is a static pod on controlplane: the kubelet stops it when its manifest leaves /etc/kubernetes/manifests.', '^scheduler$'],
        ['Ask for more replicas of the web Deployment than it has now (more than 3).', '^(controller-manager|api-server)$'],
        ['List the pods and look at the NODE and STATUS columns of the new ones.', '^worker-[0-4]$'],
        ['Put the scheduler manifest back where the kubelet watches.', '^scheduler$'],
        ['List the pods again — every replica should now have a node.', '^(worker|kubelet-led)-[0-4]$']
      ],
      'api-blind': [
        ['kube-apiserver is also a static pod on controlplane — same manifest trick.', '^api-server$'],
        ['Run any kubectl read and watch what happens without an API server.', '^(api-server|cp-halo)$'],
        ['The container runtime still knows what is running; use its CLI on controlplane (it needs root).', '^control-plane$'],
        ['Restore the manifest, then prove kubectl can talk to the API again.', '^api-server$']
      ],
      'notready': [
        ['The kubelet is a systemd unit on each node — you have to be ON worker-2 to stop it.', '^(worker-2|kubelet-led-2)$'],
        ['List nodes; the node controller marks a node NotReady when its kubelet stops posting status.', '^(worker-2|kubelet-led-2)$'],
        ['Start the unit again on worker-2, then list nodes.', '^kubelet-led-[0-4]$']
      ]
    },
    'sched-taints': {
      'schedule-db': [
        ['The scheduler writes its reasons into the pod’s Events — describe the db pod.', '^(pod-pending|event-failed-scheduling)$'],
        ['db needs disktype=nvme. node-c already has a disktype label, so changing it needs one extra flag.', '^node-c(-label-badge)?$'],
        ['A taint is removed with the same key/effect plus a trailing minus.', '^node-c-taint(-mark)?$'],
        ['List pods wide and check which node db landed on.', '^(node-c|pod-pending|edge-reject-node-c)$']
      ],
      'cordon': [
        ['Cordon marks a node unschedulable without evicting anything.', '^node-a$'],
        ['List pods wide: the old web pod and the new replica tell different stories.', '^(node-a|pod-pending)$'],
        ['Make node-a schedulable again — the opposite verb of the one you used first.', '^node-a$']
      ]
    },
    'hpa-scale': {
      'unknown-target': [
        ['Look at the HPA’s TARGETS column first.', '^(hpa-controller|hpa-halo)$'],
        ['Describe the HPA and read its Conditions — ScalingActive tells you why it cannot compute.', '^(hpa-controller|metric-hop-[0-5])$'],
        ['Utilization is a percentage OF the CPU request. No request → nothing to divide by. Set one on the Deployment.', '^(deployment|cpu-bar-[0-2])$'],
        ['Check the HPA again — REPLICAS should reach the ceiling.', '^(desired-replicas|replica-[0-4])$']
      ],
      'ceiling': [
        ['Create load: a busybox pod looping wget against the web Service is the classic CKA way.', '^cpu-bar-[0-2]$'],
        ['Describe the HPA and look for ScalingLimited.', '^hpa-controller$'],
        ['maxReplicas lives in the HPA spec — patch it with a JSON merge patch.', '^(hpa-controller|desired-replicas)$'],
        ['Check the HPA one more time.', '^replica-[0-4]$']
      ]
    },
    'aws-az-failure': {
      'survive-az': [
        ['Describe the RDS instance and read the MultiAZ field.', '^az-a-rds$'],
        ['Modify the DB instance to Multi-AZ — and do not wait for the maintenance window.', '^(az-b-rds|edge-rds-sync-replication)$'],
        ['Use the lab’s fault verb to take us-east-1a down.', '^az-a-pad$'],
        ['Hit the site’s public URL and read the status line.', '^(alb|internet-users)$']
      ],
      'spof': [
        ['Use the lab’s fault verb to take us-east-1a down.', '^az-a-pad$'],
        ['Hit the site’s public URL and read the status line.', '^alb$'],
        ['Ask the load balancer which targets are healthy — is the web tier really the problem?', '^(az-a-rds|az-b-ec2-[01])$']
      ]
    }
  };
  Object.keys(COACH).forEach(function (simId) {
    var p = PACKS[simId];
    p.tasks.forEach(function (tk) {
      var rows = COACH[simId][tk.id] || [];
      tk.steps.forEach(function (st, i) { if (rows[i]) { st.nudge = rows[i][0]; st.focus = rows[i][1]; } });
    });
  });

  /** taskId (optional) = the active task; state steps of that task are latched as they become true, in order. */
  function newCtx(taskId) { return { seq: 0, events: {}, vars: {}, history: [], task: taskId || null, latched: {}, coach: { fails: {}, checks: 0 }, last: null }; }
  function has(simId) { return !!PACKS[simId]; }
  function pack(simId) { return PACKS[simId] || null; }
  function list() { return Object.keys(PACKS); }
  function task(simId, taskId) {
    var p = PACKS[simId]; if (!p) return null;
    for (var i = 0; i < p.tasks.length; i++) if (p.tasks[i].id === taskId) return p.tasks[i];
    return null;
  }
  function record(ctx, names) {
    (names || []).forEach(function (n) { ctx.seq += 1; (ctx.events[n] || (ctx.events[n] = [])).push(ctx.seq); });
  }
  function derive(simId, state) { var S = Sims(), sim = S && S.get(simId); return sim ? sim.derive(state) : null; }

  /** Run one command line. Pure w.r.t. state (returns a patch); mutates only ctx (events, vars, history). */
  function run(simId, state, line, ctx) {
    ctx = ctx || newCtx();
    var p = PACKS[simId];
    var raw = String(line == null ? '' : line).trim();
    if (!p) return res(['sim: no CLI lab for ' + simId], 2);
    if (!raw) return res([], 0);
    ctx.history.push(raw);
    if (ctx.history.length > 200) ctx.history.shift();
    var tok = tokenize(raw);
    var u = unwrap(tok), t = u.t;
    var head = t[0] || '';
    if (head === 'help' || head === '?') {
      return res(['IL sim shell — ' + HONESTY, 'Commands modelled in this drill:'].concat(p.examples.map(function (e) { return '  ' + e; }))
        .concat(['Lab verbs: help · check · hint · solution · task · history · clear · reset' + (/fault/.test(p.examples.join(' ')) || p.sim === 'hpa-scale' ? ' · fault … (lab-only fault injection)' : '')]), 0, null, ['help'], { verb: 'help' });
    }
    if (head === 'clear') return res([], 0, null, [], { action: 'clear', verb: 'clear' });
    if (head === 'reset') return res(['sim reset to the drill’s initial state'], 0, null, ['reset'], { action: 'reset', verb: 'reset' });
    if (head === 'hint' || head === 'task' || head === 'solution') return res([], 0, null, [], { action: head, verb: head });
    if (head === 'check' || head === 'verify') return res([], 0, null, [], { action: 'check', verb: 'check' });
    if (head === 'history') return res(ctx.history.map(function (h, i) { return pad(i + 1, 5) + h; }), 0, null, [], { verb: 'history' });
    if (head === 'alias' && /^k=/.test(t[1] || '')) return res([], 0, null, [], { verb: 'alias' });
    var d = derive(simId, state);
    if (!d) return res(['sim: rules engine (il-immersive-sims.js) not loaded'], 2);
    var r = p.run(u, state, d, ctx);
    if (!r) {
      if (/^(kubectl|etcdctl|crictl|aws|curl|systemctl|mv|ls|fault)$/.test(head)) r = unmodelled(raw, p.examples);
      else r = res(['bash: ' + head + ': command not found  (simulated shell — type help)'], 127);
    }
    r.verb = r.verb || (head === 'kubectl' || head === 'aws' || head === 'etcdctl' ? head + ' ' + (t[1] || '') : head).trim();
    var merged = state, k;
    if (r.set) {
      merged = {};
      for (k in state) merged[k] = state[k];
      for (k in r.set) merged[k] = r.set[k];
    }
    if (p.reconcile) p.reconcile(merged, r.set ? derive(simId, merged) : d, ctx);
    record(ctx, r.events);
    ctx.seq += 1; /* every command gets a sequence slot, so "your last command" is always after the previous step */
    ctx.last = { exit: r.exit, first: r.out[0] || '', verb: r.verb, seq: ctx.seq };
    observe(simId, merged, ctx);
    return r;
  }

  /** Re-run a pack's reconcile after a non-CLI state change (toggle button, scenario, XR select). */
  function reconcile(simId, state, ctx) {
    var p = PACKS[simId]; if (!p || !ctx) return;
    var d = derive(simId, state);
    if (d && p.reconcile) p.reconcile(state, d, ctx);
    observe(simId, state, ctx);
  }

  /** Walk a task's steps in order. Event steps need an occurrence after the previous step; state steps are
   *  satisfied by a latch recorded after the previous step, or (when latch=true) are latched now if true now.
   *  So "lose quorum → write fails → restore quorum" still counts step 1 after quorum returns. */
  function walk(tk, state, d, ctx, latch) {
    var last = 0, blocked = false, steps = [];
    tk.steps.forEach(function (st, i) {
      var ok = false;
      if (!blocked) {
        if (st.event) {
          var seqs = ctx.events[st.event] || [];
          for (var k = 0; k < seqs.length; k++) if (seqs[k] > last) { ok = true; last = seqs[k]; break; }
        } else if (st.state) {
          var key = tk.id + ':' + i, at = ctx.latched[key];
          if (at && at > last) { ok = true; last = at; }
          else if (d && st.state(state, d, ctx)) {
            ok = true;
            if (latch) { ctx.seq += 1; ctx.latched[key] = ctx.seq; last = ctx.seq; }
          }
        }
      }
      if (!ok) blocked = true;
      steps.push({ label: st.label, done: ok, hint: st.hint, nudge: st.nudge || null, focus: st.focus || null, at: ok ? last : 0 });
    });
    return steps;
  }
  /** Latch the active task's state steps against the current state (called after every state change). */
  function observe(simId, state, ctx) {
    if (!ctx || !ctx.task) return;
    var tk = task(simId, ctx.task); if (!tk) return;
    walk(tk, state, derive(simId, state), ctx, true);
  }

  function taskStatus(simId, taskId, state, ctx) {
    var tk = task(simId, taskId); if (!tk) return null;
    ctx = ctx || newCtx(taskId);
    if (!ctx.latched) ctx.latched = {};
    var steps = walk(tk, state, derive(simId, state), ctx, false);
    var next = null;
    for (var j = 0; j < steps.length; j++) if (!steps[j].done) { next = steps[j]; break; }
    return { id: tk.id, title: tk.title, goal: tk.goal, done: !next, next: next, steps: steps, total: steps.length, completed: steps.filter(function (x) { return x.done; }).length };
  }

  /* ── Lab Muse coach (v1.1.0) ─────────────────────────────────────────── */
  /** Event names seen after `after` that share a prefix family with `want` (e.g. get-pods for get-pods-pending). */
  function relatedEvents(ctx, want, after) {
    var parts = String(want).split('-'), seen = [];
    for (var n = parts.length - 1; n >= 1 && !seen.length; n--) {
      var pre = parts.slice(0, n).join('-');
      Object.keys(ctx.events).forEach(function (name) {
        if (name === want || (name !== pre && name.indexOf(pre + '-') !== 0)) return;
        var seqs = ctx.events[name];
        if (seqs.length && seqs[seqs.length - 1] > after && seen.indexOf(name) < 0) seen.push(name);
      });
    }
    return seen;
  }

  /** Why is step `idx` not verified? Deterministic: reads only ctx (events / latches / last result) and live sim state. */
  function diagnose(simId, tk, state, ctx, st, idx) {
    var step = tk.steps[idx], after = idx > 0 ? st.steps[idx - 1].at : 0, lines = [], short = '';
    var d = derive(simId, state);
    if (step.event) {
      var seqs = ctx.events[step.event] || [];
      var rel = relatedEvents(ctx, step.event, after), relEver = rel.length ? rel : relatedEvents(ctx, step.event, 0);
      if (seqs.length && seqs[seqs.length - 1] <= after) {
        short = 'you did this before the previous step was verified — steps count in order, so do it again now.';
        lines.push('Seen earlier, but before step ' + idx + ' was verified — steps count in order. Run it again now.');
      } else if (rel.length) {
        short = 'right kind of command, but the cluster was not in the state this step needs yet.';
        lines.push('You ran the right kind of command, but the lab saw `' + rel.join('`, `') + '` — not `' + step.event + '`. The cluster was not in the state this step needs yet.');
      } else if (relEver.length && idx > 0) {
        short = 'you ran a related command before step ' + idx + ' was verified — order matters, run it again now.';
        lines.push('You ran a related command (`' + relEver.join('`, `') + '`) before step ' + idx + ' was verified — steps count in order. Run it again now.');
      } else {
        short = 'the lab has not seen this command yet.';
        lines.push('The lab has not seen this yet (it verifies what you run, in order, ' + (idx ? 'after step ' + idx : 'since the task started') + ').');
      }
    } else {
      short = 'the live state is not true right now.';
      lines.push('This step checks live state, and it is not true right now.');
    }
    if (d && d.caption) lines.push('Scene now: ' + d.caption + ' [' + d.verdict + ']');
    var last = ctx.last;
    if (last && last.exit !== 0 && last.seq > after) {
      lines.push('Your last command exited ' + last.exit + (last.exit === 2 ? ' (not modelled in this drill — nothing was invented)' : (last.exit === 127 ? ' (command not found)' : '')) + ': ' + last.first);
    }
    return { lines: lines, short: short };
  }

  /** Human label for a focus regex, for stages without a 3D render: '^(worker|kubelet-led)-[0-4]$' → 'worker / kubelet-led-*'. */
  function focusLabel(src) {
    if (!src) return '';
    return String(src).replace(/^\^|\$$/g, '').replace(/\([^()]*\)\?/g, '').replace(/\[[^\]]+\]/g, '*')
      .replace(/\.\*/g, '*').replace(/[()]/g, '').replace(/\|/g, ' / ');
  }

  /** Killercoda-style CHECK with an escalation ladder: 1st failed check on a step → diagnosis; 2nd+ → diagnosis +
   *  auto-offered hint (tip, never the command); level 'solution' (the `solution` verb) → the exact command.
   *  opts.count=false inspects without counting a failed attempt (used by `hint` / `solution`). */
  function coach(simId, taskId, state, ctx, opts) {
    opts = opts || {};
    var tk = task(simId, taskId);
    if (!tk) return { ok: false, done: false, level: 'none', lines: ['No task selected — pick one above, then type `check`.'], speak: 'Pick a task first, then ask me to check it.', focus: null, step: -1 };
    if (!ctx.coach) ctx.coach = { fails: {}, checks: 0 };
    var st = taskStatus(simId, taskId, state, ctx);
    if (st.done) {
      return { ok: true, done: true, level: 'done', step: -1, focus: null, fails: 0,
        lines: ['✓ check: all ' + st.total + ' steps verified — ' + st.title + ' complete.'],
        speak: 'Lab Muse: every step of ' + st.title + ' is verified. Nice work.' };
    }
    var idx = st.steps.indexOf(st.next), step = tk.steps[idx];
    var counted = opts.count !== false;
    if (counted) { ctx.coach.checks += 1; ctx.coach.fails[idx] = (ctx.coach.fails[idx] || 0) + 1; }
    var fails = ctx.coach.fails[idx] || 0;
    var level = opts.level || (fails >= 2 ? 'hint' : 'diagnose');
    var dg = diagnose(simId, tk, state, ctx, st, idx);
    var lines = ['✗ check: step ' + (idx + 1) + '/' + st.total + ' not verified — ' + step.label];
    dg.lines.forEach(function (l) { lines.push('  · ' + l); });
    if (level === 'hint' || level === 'solution') lines.push('  hint → ' + (step.nudge || step.label));
    if (level === 'solution') lines.push('  solution → $ ' + step.hint);
    else if (level === 'hint') lines.push('  Still stuck? `solution` prints the exact command.');
    else lines.push('  Check again after another try and I will offer a hint (or type `hint` now).');
    if (step.focus) lines.push('  Look in the scene: the pulsing gold nodes.');
    var speak = 'Lab Muse: step ' + (idx + 1) + ' of ' + st.total + ' is not verified yet — ' + dg.short +
      (level === 'hint' || level === 'solution' ? ' Hint: ' + (step.nudge || step.label) : '');
    return { ok: true, done: false, level: level, step: idx, label: step.label, fails: fails, focus: step.focus || null, focusLabel: focusLabel(step.focus),
      lines: lines, speak: speak, diagnosis: dg.lines, nudge: step.nudge || null, solution: level === 'solution' ? step.hint : null };
  }

  /** Tab completion over the pack's example commands + lab verbs. */
  function complete(simId, prefix) {
    var p = PACKS[simId]; if (!p) return [];
    var pool = p.examples.concat(['help', 'check', 'hint', 'solution', 'task', 'history', 'clear', 'reset']);
    var pre = String(prefix || '');
    return pool.filter(function (c) { return c.indexOf(pre) === 0 && c !== pre; });
  }

  return {
    VERSION: '1.1.0',
    honesty: HONESTY,
    tokenize: tokenize,
    flag: flag,
    manifestMove: manifestMove,
    has: has,
    list: list,
    pack: pack,
    task: task,
    newCtx: newCtx,
    run: run,
    reconcile: reconcile,
    observe: observe,
    taskStatus: taskStatus,
    coach: coach,
    focusLabel: focusLabel,
    relatedEvents: relatedEvents,
    complete: complete
  };
});
