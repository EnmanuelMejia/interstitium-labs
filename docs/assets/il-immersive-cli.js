/**
 * IL Immersive CLI v1.2.0 (2026-10-20; v1.1.0 2026-10-19; v1.0.0 2026-10-16) — type real kubectl / etcdctl / crictl / aws CLI syntax and the authored
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
 * v1.2.0 (2026-10-20) — four more packs (9 total): NetworkPolicy (lab YAML files + `kubectl apply -f`, in-pod curl /
 * nslookup probes, `fault cni flannel|calico`), RBAC (`kubectl auth can-i --as`, role / rolebinding /
 * clusterrolebinding), storage (reclaim Retain, pvc-protection, default StorageClass) and the Ingress API (curl status
 * from ingressMatch, pathType, EndpointSlices, TLS secret; ingress-nginx retired 2026-03-24 — said in help). Lab files
 * (`ls` / `cat`) stand in for editing YAML. `fromSpeech(transcript, simId)` normalises a spoken utterance into a lab
 * verb or a command line (snapped to the drill's own vocabulary) — the player never auto-runs spoken commands.
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
        var rows2 = [['NAME', 'STATUS', 'ROLES', 'AGE', 'VERSION'], ['controlplane', 'Ready', 'control-plane', '41d', 'v1.37.1']];
        for (var w = 0; w < 5; w++) rows2.push(['worker-' + w, w === 2 && m.worker2NotReady ? 'NotReady' : 'Ready', '<none>', '41d', 'v1.37.1']);
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
        rows.push(['node-a', s.aCordoned ? 'Ready,SchedulingDisabled' : 'Ready', '<none>', '9d', 'v1.37.1'].concat(showLabels ? ['disktype=ssd'] : []));
        rows.push(['node-b', 'Ready', '<none>', '9d', 'v1.37.1'].concat(showLabels ? ['zone=us-east-1b'] : []));
        rows.push(['node-c', 'Ready', '<none>', '9d', 'v1.37.1'].concat(showLabels ? ['disktype=' + (s.cNvme ? 'nvme' : 'hdd')] : []));
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

  /* ── v1.2.0 (2026-10-20) shared helpers for the networking / security / storage packs ─────────── */
  /** `kubectl exec [-n NS] TARGET -- CMD…` → { ns, target, cmd:[…] } or null. */
  function execArgs(t) {
    if (t[0] !== 'kubectl' || t[1] !== 'exec') return null;
    var dd = t.indexOf('--');
    var head = dd < 0 ? t.slice(2) : t.slice(2, dd);
    var tgt = positional(head, KUBECTL_VALUED.concat(['-c', '--container']));
    return { ns: flag(head, ['-n', '--namespace']) || 'default', target: (tgt[0] || '').replace(/^(deploy|deployment|deployments)(\.apps)?\//, '').replace(/^pods?\//, ''), cmd: dd < 0 ? [] : t.slice(dd + 1), hasDd: dd >= 0 };
  }
  /** Lab files the learner can `ls` / `cat` / `kubectl apply -f`. */
  function fileRun(p, t) {
    if (!p.files) return null;
    if (t[0] === 'ls' && (t.length === 1 || /^(\.|~|\.\/|~\/|-l|-la|-al)$/.test(t[1] || ''))) return res([Object.keys(p.files).join('  ')], 0, null, ['ls']);
    if (t[0] === 'cat' && t[1]) {
      var f = p.files[t[1].replace(/^(\.\/|~\/)/, '')];
      return f ? res(f.yaml, 0, null, ['cat', 'cat-' + t[1].replace(/^(\.\/|~\/)/, '').replace(/\.ya?ml$/, '')]) : res(['cat: ' + t[1] + ': No such file or directory'], 1);
    }
    return null;
  }
  function applyFile(p, t) {
    var fname = String(flag(t, ['-f', '--filename']) || '').replace(/^(\.\/|~\/)/, '');
    if (!fname || fname === 'true') return { err: res(['error: must specify one of -f and -k'], 1) };
    var f = p.files && p.files[fname];
    if (!f) return { err: res(['error: the path "' + fname + '" does not exist'], 1) };
    return { f: f, name: fname };
  }
  function nsOf(t) { return flag(t, ['-n', '--namespace']) || (hasFlag(t, ['-A', '--all-namespaces']) ? '*' : 'default'); }
  function notFound(kind, name) { return res(['Error from server (NotFound): ' + kind + ' "' + name + '" not found'], 1, null, ['not-found']); }

  /* ── pack: NetworkPolicy isolation (CKA services & networking) ─────────── */
  var NP_BASE = ['apiVersion: networking.k8s.io/v1', 'kind: NetworkPolicy', 'metadata:', '  name: api-netpol', '  namespace: backend', 'spec:', '  podSelector:', '    matchLabels:', '      app: api'];
  var NP_FROM_FRONTEND = ['  ingress:', '  - from:', '    - namespaceSelector:', '        matchLabels:', '          kubernetes.io/metadata.name: frontend', '    ports:', '    - protocol: TCP', '      port: 8080'];
  var NP_EGRESS_DB = ['  egress:', '  - to:', '    - podSelector:', '        matchLabels:', '          app: db', '    ports:', '    - protocol: TCP', '      port: 5432'];
  var NP_EGRESS_DNS = ['  - to:', '    - namespaceSelector:', '        matchLabels:', '          kubernetes.io/metadata.name: kube-system', '      podSelector:', '        matchLabels:', '          k8s-app: kube-dns', '    ports:', '    - protocol: UDP', '      port: 53', '    - protocol: TCP', '      port: 53'];
  var netpolPack = {
    sim: 'netpol-isolation',
    prompt: 'student@controlplane:~$',
    files: {
      'api-deny-all.yaml': { set: { policy: true, ruleFrontend: false, ruleUntrusted: false, egressIsolated: false }, yaml: NP_BASE.concat(['  policyTypes:', '  - Ingress', '  # no ingress rules: every pod selected by podSelector is isolated for ingress']) },
      'api-allow-frontend.yaml': { set: { policy: true, ruleFrontend: true, ruleUntrusted: false, egressIsolated: false }, yaml: NP_BASE.concat(['  policyTypes:', '  - Ingress']).concat(NP_FROM_FRONTEND) },
      'api-egress-lockdown.yaml': { set: { policy: true, ruleFrontend: true, ruleUntrusted: false, egressIsolated: true, ruleDns: false }, yaml: NP_BASE.concat(['  policyTypes:', '  - Ingress', '  - Egress']).concat(NP_FROM_FRONTEND).concat(NP_EGRESS_DB) },
      'api-egress-dns.yaml': { set: { policy: true, ruleFrontend: true, ruleUntrusted: false, egressIsolated: true, ruleDns: true }, yaml: NP_BASE.concat(['  policyTypes:', '  - Ingress', '  - Egress']).concat(NP_FROM_FRONTEND).concat(NP_EGRESS_DB).concat(NP_EGRESS_DNS) }
    },
    examples: ['kubectl get networkpolicy -n backend', 'kubectl describe networkpolicy api-netpol -n backend', 'cat api-allow-frontend.yaml', 'kubectl apply -f api-deny-all.yaml',
      'kubectl exec -n frontend deploy/web -- curl -s -m 3 http://api.backend:8080', 'kubectl exec -n untrusted deploy/scanner -- curl -s -m 3 http://api.backend:8080',
      'kubectl exec -n backend deploy/api -- nslookup db.backend.svc.cluster.local', 'kubectl get daemonsets -A', 'fault cni flannel'],
    run: function (u, s, d, ctx) {
      var t = u.t, m = d.metrics;
      var f = faultArgs(t);
      if (f) {
        if (f[0] === 'cni' && (f[1] === 'flannel' || f[1] === 'calico' || f[1] === 'cilium')) {
          var on = f[1] !== 'flannel';
          return res(['[lab fault injection] pod network → ' + f[1] + (on ? ' (enforces NetworkPolicy)' : ' (no NetworkPolicy support)') + ' — stands in for a CNI migration (simulated)'], 0, { cniEnforces: on }, [on ? 'cni-enforcing' : 'cni-flannel']);
        }
        return res(['usage: fault cni calico|cilium|flannel   (lab-only: stands in for a CNI migration)'], 2);
      }
      var fr = fileRun(netpolPack, t); if (fr) return fr;
      if (t[0] !== 'kubectl') return null;
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED), ns = nsOf(t);
      var isNp = /^(netpol|networkpolic(y|ies)(\.networking\.k8s\.io)?)$/;
      if (verb === 'apply' || (verb === 'create' && hasFlag(t, ['-f', '--filename']))) {
        var a = applyFile(netpolPack, t); if (a.err) return a.err;
        var same = true;
        for (var k in a.f.set) if (!!s[k] !== a.f.set[k]) same = false;
        var word = !s.policy ? 'created' : (same ? 'unchanged' : 'configured');
        if (verb === 'create' && s.policy) return res(['Error from server (AlreadyExists): error when creating "' + a.name + '": networkpolicies.networking.k8s.io "api-netpol" already exists'], 1);
        return res(['networkpolicy.networking.k8s.io/api-netpol ' + word], 0, a.f.set, ['apply-netpol', 'apply-' + a.name.replace(/\.yaml$/, '')]);
      }
      if (verb === 'delete' && (isNp.test(args[0] || '') || /^networkpolic(y|ies)\//.test(args[0] || '') || hasFlag(t, ['-f', '--filename']))) {
        var nm = hasFlag(t, ['-f', '--filename']) ? 'api-netpol' : (args[1] || String(args[0]).split('/')[1] || '');
        if (!hasFlag(t, ['-f', '--filename']) && ns !== 'backend') return notFound('networkpolicies.networking.k8s.io', nm);
        if (nm !== 'api-netpol' || !s.policy) return notFound('networkpolicies.networking.k8s.io', nm);
        return res(['networkpolicy.networking.k8s.io "api-netpol" deleted'], 0, { policy: false }, ['delete-netpol']);
      }
      if (verb === 'get' && isNp.test(args[0] || '')) {
        if (ns !== 'backend' && ns !== '*' || !s.policy) return res(['No resources found in ' + (ns === '*' ? 'any' : ns) + ' namespace.'], 0, null, ['get-netpol-none']);
        var hdr = (ns === '*' ? ['NAMESPACE'] : []).concat(['NAME', 'POD-SELECTOR', 'AGE']);
        return res(table([hdr, (ns === '*' ? ['backend'] : []).concat(['api-netpol', 'app=api', '6m'])]), 0, null, ['get-netpol']);
      }
      if (verb === 'describe' && (isNp.test(args[0] || '') || /^networkpolic(y|ies)\//.test(args[0] || ''))) {
        if (ns !== 'backend' || !s.policy) return notFound('networkpolicies.networking.k8s.io', args[1] || 'api-netpol');
        var L = ['Name:         api-netpol', 'Namespace:    backend', 'Labels:       <none>', 'Annotations:  <none>', 'Spec:', '  PodSelector:     app=api', '  Allowing ingress traffic:'];
        var from = [];
        if (s.ruleFrontend) from.push('      NamespaceSelector: kubernetes.io/metadata.name=frontend');
        if (s.ruleUntrusted) from.push('      NamespaceSelector: kubernetes.io/metadata.name=untrusted');
        if (from.length) L = L.concat(['    To Port: 8080/TCP', '    From:']).concat(from);
        else L.push('    <none> (Selected pods are isolated for ingress connectivity)');
        if (s.egressIsolated) {
          L = L.concat(['  Allowing egress traffic:', '    To Port: 5432/TCP', '    To:', '      PodSelector: app=db']);
          if (s.ruleDns) L = L.concat(['    ----------', '    To Port: 53/UDP', '    To Port: 53/TCP', '    To:', '      NamespaceSelector: kubernetes.io/metadata.name=kube-system', '      PodSelector: k8s-app=kube-dns']);
          L.push('  Policy Types: Ingress, Egress');
        } else L = L.concat(['  Not affecting egress traffic', '  Policy Types: Ingress']);
        var ev = ['describe-netpol', s.egressIsolated ? (s.ruleDns ? 'describe-netpol-egress-dns' : 'describe-netpol-egress') : 'describe-netpol-ingress'];
        return res(L, 0, null, ev);
      }
      if (verb === 'get' && /^(ds|daemonsets?(\.apps)?)$/.test(args[0] || '')) {
        if (ns !== '*' && ns !== 'kube-system' && ns !== 'kube-flannel') return res(['No resources found in ' + ns + ' namespace.'], 0, null, ['get-ds-none']);
        var rows = [['NAMESPACE', 'NAME', 'DESIRED', 'CURRENT', 'READY', 'UP-TO-DATE', 'AVAILABLE', 'NODE SELECTOR', 'AGE']];
        if (s.cniEnforces) rows.push(['kube-system', 'calico-node', '4', '4', '4', '4', '4', 'kubernetes.io/os=linux', '30d']);
        else rows.push(['kube-flannel', 'kube-flannel-ds', '4', '4', '4', '4', '4', '<none>', '30d']);
        rows.push(['kube-system', 'kube-proxy', '4', '4', '4', '4', '4', 'kubernetes.io/os=linux', '30d']);
        if (ns !== '*') rows = rows.filter(function (r, i) { return i === 0 || r[0] === ns; }).map(function (r) { return r.slice(1); });
        return res(table(rows), 0, null, ['get-ds', s.cniEnforces ? 'get-ds-enforcing' : 'get-ds-flannel']);
      }
      var ex = execArgs(t);
      if (ex) {
        var SRC = { frontend: 'web', untrusted: 'scanner', backend: 'api' };
        if (!ex.hasDd || !ex.cmd.length) return res(['error: you must specify at least one command for the container (kubectl exec … -- CMD)'], 1);
        if (!SRC[ex.ns] || ex.target.indexOf(SRC[ex.ns]) !== 0) return res(['Error from server (NotFound): deployments.apps "' + ex.target + '" not found' + (SRC[ex.ns] ? '' : ' (this lab has frontend/web, untrusted/scanner, backend/api)')], 1, null, ['not-found']);
        var bin = ex.cmd[0], url = ex.cmd.filter(function (x) { return /api|db|:\/\//.test(x) && x.charAt(0) !== '-'; })[0] || '';
        if ((bin === 'nslookup' || bin === 'dig' || bin === 'host' || (bin === 'getent' && ex.cmd[1] === 'hosts'))) {
          var name = ex.cmd[ex.cmd.length - 1];
          var dnsOk = ex.ns === 'backend' ? m.dns : true;
          if (!dnsOk) return res([';; connection timed out; no servers could be reached', '', 'command terminated with exit code 1'], 1, null, ['dns', 'dns-fail']);
          return res(['Server:\t\t10.96.0.10', 'Address:\t10.96.0.10:53', '', 'Name:\t' + (/\./.test(name) ? name : name + '.backend.svc.cluster.local'), 'Address: 10.96.142.7'], 0, null, ['dns', ex.ns === 'backend' ? 'dns-ok' : 'dns-ok-other']);
        }
        if (bin === 'curl' || bin === 'wget') {
          if (!/(^|\/\/)api(\.backend)?(\.svc(\.cluster\.local)?)?(:8080)?(\/|$)/.test(url)) return res(['sim: this drill models probes to the api Service (http://api.backend:8080) and DNS lookups from backend/api'], 2);
          if (ex.ns === 'backend') {
            if (!m.dns) return res(['curl: (6) Could not resolve host: api.backend', 'command terminated with exit code 6'], 6, null, ['probe', 'dns-fail']);
            return res(['{"service":"api","ok":true}'], 0, null, ['probe', 'probe-self']);
          }
          var ok = ex.ns === 'frontend' ? m.frontend : m.untrusted, who = ex.ns === 'frontend' ? 'frontend' : 'untrusted';
          var timeoutNote = (bin === 'curl' && !hasFlag(ex.cmd, ['-m', '--max-time', '--connect-timeout'])) || (bin === 'wget' && !hasFlag(ex.cmd, ['-T', '--timeout']));
          if (ok) return res(['{"service":"api","pod":"api-7f9c-x2k4q","ok":true}'], 0, null, ['probe', 'probe-' + who + '-ok', who === 'untrusted' ? 'probe-untrusted-open' : 'probe-frontend-ok']);
          var lines = bin === 'curl' ? ['curl: (28) Connection timed out after 3002 milliseconds', 'command terminated with exit code 28'] : ['wget: download timed out', 'command terminated with exit code 1'];
          if (timeoutNote) lines.unshift('# sim: without a timeout flag a real probe hangs until the TCP connect gives up (~2 min); the sim stops at 3 s');
          return res(lines, bin === 'curl' ? 28 : 1, null, ['probe', 'probe-' + who + '-blocked']);
        }
        return res(['sim: inside the pods this drill models curl / wget (to api.backend:8080) and nslookup / dig'], 2);
      }
      return unmodelled(t.join(' '), netpolPack.examples);
    },
    tasks: [
      { id: 'lock-api', title: 'Lock api down, then let only frontend in',
        goal: 'No policy selects app=api, so every namespace reaches it. Prove it, apply a default-deny, then allow ns frontend only.',
        setup: { cniEnforces: true, policy: false, ruleFrontend: false, ruleUntrusted: false, egressIsolated: false, ruleDns: true },
        steps: [
          { label: 'Prove the problem: ns untrusted reaches api:8080', event: 'probe-untrusted-open', hint: 'kubectl exec -n untrusted deploy/scanner -- curl -s -m 3 http://api.backend:8080' },
          { label: 'Apply a default-deny ingress policy to app=api', state: function (s) { return s.policy && !s.ruleFrontend && !s.ruleUntrusted; }, hint: 'kubectl apply -f api-deny-all.yaml' },
          { label: 'See that frontend is dropped too (default deny)', event: 'probe-frontend-blocked', hint: 'kubectl exec -n frontend deploy/web -- curl -s -m 3 http://api.backend:8080' },
          { label: 'Allow ingress from ns frontend on 8080 only', state: function (s) { return s.policy && s.ruleFrontend && !s.ruleUntrusted; }, hint: 'kubectl apply -f api-allow-frontend.yaml' },
          { label: 'frontend gets in again', event: 'probe-frontend-ok', hint: 'kubectl exec -n frontend deploy/web -- curl -s -m 3 http://api.backend:8080' },
          { label: 'untrusted is still dropped', event: 'probe-untrusted-blocked', hint: 'kubectl exec -n untrusted deploy/scanner -- curl -s -m 3 http://api.backend:8080' }
        ] },
      { id: 'egress-dns', title: 'Egress lock-down breaks DNS — fix it',
        goal: 'Restrict api egress to db:5432, watch name resolution die, read the policy, then allow kube-dns on 53.',
        setup: { cniEnforces: true, policy: true, ruleFrontend: true, ruleUntrusted: false, egressIsolated: false, ruleDns: true },
        steps: [
          { label: 'Lock api egress down to db:5432 only', state: function (s) { return s.policy && s.egressIsolated && !s.ruleDns; }, hint: 'kubectl apply -f api-egress-lockdown.yaml' },
          { label: 'Watch api fail to resolve db.backend', event: 'dns-fail', hint: 'kubectl exec -n backend deploy/api -- nslookup db.backend.svc.cluster.local' },
          { label: 'Read which egress the policy allows', event: 'describe-netpol-egress', hint: 'kubectl describe networkpolicy api-netpol -n backend' },
          { label: 'Allow egress to kube-dns on 53 (UDP and TCP)', state: function (s) { return s.policy && s.egressIsolated && s.ruleDns; }, hint: 'kubectl apply -f api-egress-dns.yaml' },
          { label: 'Resolve db.backend again', event: 'dns-ok', hint: 'kubectl exec -n backend deploy/api -- nslookup db.backend.svc.cluster.local' }
        ] },
      { id: 'flannel', title: 'Policy applied, nothing enforced',
        goal: 'The policy exists, yet untrusted still gets in. Find out which CNI runs the pod network and fix the root cause.',
        setup: { cniEnforces: false, policy: true, ruleFrontend: true, ruleUntrusted: false, egressIsolated: false, ruleDns: true },
        steps: [
          { label: 'Confirm the policy exists in ns backend', event: 'get-netpol', hint: 'kubectl get networkpolicy -n backend' },
          { label: 'Yet untrusted still reaches api', event: 'probe-untrusted-open', hint: 'kubectl exec -n untrusted deploy/scanner -- curl -s -m 3 http://api.backend:8080' },
          { label: 'Find which CNI DaemonSet runs the pod network', event: 'get-ds-flannel', hint: 'kubectl get daemonsets -A' },
          { label: 'Move to a NetworkPolicy-enforcing CNI (lab verb stands in for the migration)', state: function (s) { return !!s.cniEnforces; }, hint: 'fault cni calico' },
          { label: 'untrusted is dropped now', event: 'probe-untrusted-blocked', hint: 'kubectl exec -n untrusted deploy/scanner -- curl -s -m 3 http://api.backend:8080' }
        ] }
    ]
  };

  /* ── pack: RBAC (CKA cluster architecture) ─────────────────────────────── */
  var RB_DEFAULT = { b0: 'alice-pod-reader', b1: 'bob-secret-reader', b2: 'ci-bot-deployer' };
  var CI_SA = 'system:serviceaccount:dev:ci-bot';
  function rbacRes(r) {
    r = String(r || '').toLowerCase().replace(/\.(apps|rbac\.authorization\.k8s\.io)$/, '');
    if (/^(pods?|po)$/.test(r)) return 'pods';
    if (/^secrets?$/.test(r)) return 'secrets';
    if (/^(deploy|deployments?)$/.test(r)) return 'deployments';
    if (/^(nodes?|no)$/.test(r)) return 'nodes';
    return null;
  }
  /** Can WHO do VERB on RES in NS, given binding state? (alice/bob are Users; ci-bot is a ServiceAccount in dev.) */
  function rbacCan(s, who, verb, rsc, ns) {
    if (!who) return true; /* kubernetes-admin */
    var read = /^(get|list|watch)$/.test(verb);
    if (who === 'alice') return rsc === 'pods' && read && !!s.b0 && ns === 'dev';
    if (who === 'bob') return rsc === 'secrets' && (verb === 'get' || verb === 'list') && !!s.b1 && ns === 'dev';
    if (who === CI_SA) {
      if (!s.b2) return false;
      if (rsc === 'deployments') return /^(get|list|watch|create|update|patch)$/.test(verb) && (!!s.b2Cluster || ns === 'dev');
      if (rsc === 'nodes') return read && !!s.b2Cluster;
      return false;
    }
    return false;
  }
  function whoKey(who) { return !who ? 'admin' : (who === CI_SA ? 'ci-bot' : (who === 'ci-bot' ? 'ci-bot-user' : (who === 'alice' || who === 'bob' ? who : 'other'))); }
  var RB_ROWS = { pods: [['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE'], ['web-6f7d9-k2x8q', '1/1', 'Running', '0', '4d']],
    secrets: [['NAME', 'TYPE', 'DATA', 'AGE'], ['db-creds', 'Opaque', '2', '4d']],
    deployments: [['NAME', 'READY', 'UP-TO-DATE', 'AVAILABLE', 'AGE'], ['web', '1/1', '1', '1', '4d']],
    nodes: [['NAME', 'STATUS', 'ROLES', 'AGE', 'VERSION'], ['controlplane', 'Ready', 'control-plane', '30d', 'v1.37.1'], ['node01', 'Ready', '<none>', '30d', 'v1.37.1']] };
  var rbacPack = {
    sim: 'rbac-authz',
    prompt: 'student@controlplane:~$',
    examples: ['kubectl auth can-i list pods -n dev --as alice', 'kubectl auth can-i get nodes --as system:serviceaccount:dev:ci-bot', 'kubectl get rolebindings -n dev -o wide',
      'kubectl create rolebinding alice-pod-reader --role=pod-reader --user=alice -n dev', 'kubectl delete rolebinding bob-secret-reader -n dev',
      'kubectl create clusterrolebinding ci-bot-deployer --clusterrole=deployer --serviceaccount=dev:ci-bot', 'kubectl get secrets -n dev --as bob', 'kubectl describe rolebinding alice-pod-reader -n dev'],
    run: function (u, s, d, ctx) {
      var t = u.t;
      if (t[0] !== 'kubectl') return null;
      var names = ctx.vars.rbNames || (ctx.vars.rbNames = { b0: RB_DEFAULT.b0, b1: RB_DEFAULT.b1, b2: RB_DEFAULT.b2 });
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED.concat(['--as', '--as-group', '--role', '--clusterrole', '--user', '--serviceaccount', '--group'])), ns = nsOf(t);
      var as = flag(t, '--as'); if (as === true) as = null;
      var nsPatch = function (n) { return (n === 'dev' || n === 'prod') && !!s.sameNs !== (n === 'dev') ? { sameNs: n === 'dev' } : null; };
      if (verb === 'auth' && t[2] === 'can-i') {
        var cargs = positional(t.slice(3), KUBECTL_VALUED.concat(['--as', '--as-group']));
        if (hasFlag(t, '--list')) return res(['sim: `can-i --list` is not modelled — ask one verb + resource at a time (kubectl auth can-i list pods -n dev --as alice)'], 2);
        var v = cargs[0], rsc = rbacRes(cargs[1]);
        if (!v || !rsc) return res(['sim: this drill models can-i on pods, secrets, deployments and nodes (e.g. kubectl auth can-i list pods -n dev --as alice)'], 2);
        var clusterScoped = rsc === 'nodes';
        var nsk = clusterScoped ? 'cluster' : (ns === '*' ? 'all' : ns);
        var ok = rbacCan(s, as, v, rsc, clusterScoped ? null : (ns === '*' ? '*' : ns));
        var yn = ok ? 'yes' : 'no', wk = whoKey(as);
        var out = [];
        if (clusterScoped && flag(t, ['-n', '--namespace'])) out.push("Warning: resource 'nodes' is not namespace scoped");
        out.push(yn);
        if (as === 'ci-bot') out.push('# sim: "ci-bot" here is a User with no bindings — the ServiceAccount is impersonated as ' + CI_SA);
        return res(out, ok ? 0 : 1, clusterScoped ? null : nsPatch(ns), ['cani', 'cani-' + yn, 'cani-' + wk + '-' + rsc + '-' + yn, 'cani-' + wk + '-' + rsc + '-' + nsk + '-' + yn]);
      }
      if (verb === 'get' && rbacRes(args[0]) && !/^(rolebindings?|clusterrolebindings?)$/.test(args[0])) {
        var r2 = rbacRes(args[0]), cs = r2 === 'nodes';
        if (!rbacCan(s, as, 'list', r2, cs ? null : ns)) {
          var grp = r2 === 'deployments' ? 'apps' : '';
          var subj = 'User "' + as + '"';
          return res(['Error from server (Forbidden): ' + r2 + ' is forbidden: ' + subj + ' cannot list resource "' + r2 + '" in API group "' + grp + '" ' + (cs ? 'at the cluster scope' : 'in the namespace "' + ns + '"')], 1, cs ? null : nsPatch(ns), ['forbidden', 'get-' + r2 + '-forbidden']);
        }
        return res(table(RB_ROWS[r2]), 0, cs ? null : nsPatch(ns), ['get-' + r2 + '-ok']);
      }
      if (verb === 'get' && /^(rolebindings?|rb)$/.test(args[0] || '')) {
        if (ns !== 'dev') return res(['No resources found in ' + ns + ' namespace.'], 0, null, ['get-rolebindings-none']);
        var wide = flag(t, ['-o', '--output']) === 'wide';
        var rows = [['NAME', 'ROLE', 'AGE'].concat(wide ? ['USERS', 'GROUPS', 'SERVICEACCOUNTS'] : [])];
        if (s.b0) rows.push([names.b0, 'Role/pod-reader', '4d'].concat(wide ? ['alice', '', ''] : []));
        if (s.b1) rows.push([names.b1, 'Role/secret-reader', '4d'].concat(wide ? ['bob', '', ''] : []));
        if (s.b2 && !s.b2Cluster) rows.push([names.b2, 'ClusterRole/deployer', '4d'].concat(wide ? ['', '', 'dev/ci-bot'] : []));
        if (rows.length === 1) return res(['No resources found in dev namespace.'], 0, null, ['get-rolebindings', 'get-rolebindings-none']);
        return res(table(rows), 0, null, ['get-rolebindings']);
      }
      if (verb === 'get' && /^(clusterrolebindings?|crb)$/.test(args[0] || '')) {
        if (!(s.b2 && s.b2Cluster)) return res(['sim: only the drill’s own bindings are modelled — no ClusterRoleBinding for ci-bot exists (system:* bindings omitted)'], 0, null, ['get-crb-none']);
        return res(table([['NAME', 'ROLE', 'AGE'], [names.b2, 'ClusterRole/deployer', '1m']]).concat(['# sim: system:* ClusterRoleBindings omitted']), 0, null, ['get-crb']);
      }
      if (verb === 'describe' && /^(rolebindings?|rb)$/.test(args[0] || '')) {
        var nm = args[1], which = nm === names.b0 && s.b0 ? 0 : (nm === names.b1 && s.b1 ? 1 : (nm === names.b2 && s.b2 && !s.b2Cluster ? 2 : -1));
        if (ns !== 'dev' || which < 0) return notFound('rolebindings.rbac.authorization.k8s.io', nm || '');
        var role = ['Role pod-reader', 'Role secret-reader', 'ClusterRole deployer'][which].split(' ');
        var sub = [['User', 'alice', ''], ['User', 'bob', ''], ['ServiceAccount', 'ci-bot', 'dev']][which];
        return res(['Name:         ' + nm, 'Labels:       <none>', 'Annotations:  <none>', 'Role:', '  Kind:  ' + role[0], '  Name:  ' + role[1], 'Subjects:'].concat(table([['  Kind', 'Name', 'Namespace'], ['  ----', '----', '---------'], ['  ' + sub[0], sub[1], sub[2]]])), 0, null, ['describe-rolebinding']);
      }
      if (verb === 'create' && (args[0] === 'role' || args[0] === 'clusterrole')) {
        var rn = args[1] || '';
        if (/^(pod-reader|secret-reader|deployer)$/.test(rn)) return res(['error: failed to create ' + args[0] + ': ' + args[0] + 's.rbac.authorization.k8s.io "' + rn + '" already exists'], 1);
        return res(['sim: Roles in this drill are pre-created (Role pod-reader, Role secret-reader in dev; ClusterRole deployer) — bind them with create rolebinding / clusterrolebinding'], 2);
      }
      if (verb === 'create' && args[0] === 'rolebinding') {
        var bn = args[1], role2 = flag(t, '--role'), cr = flag(t, '--clusterrole'), usr = flag(t, '--user'), sa = flag(t, '--serviceaccount');
        if (!bn || (!role2 && !cr)) return res(['error: exactly one NAME is required, and one of --role or --clusterrole'], 1);
        if (ns !== 'dev') return res(['rolebinding.rbac.authorization.k8s.io/' + bn + ' created', '# sim: created in namespace ' + ns + ' — it grants nothing in dev (add -n dev). Not reflected in the scene.'], 0, null, ['rolebinding-wrong-ns']);
        var slot = role2 === 'pod-reader' && usr === 'alice' ? 'b0' : (role2 === 'secret-reader' && usr === 'bob' ? 'b1' : (cr === 'deployer' && sa === 'dev:ci-bot' ? 'b2' : null));
        if (!slot) {
          if (cr === 'deployer' && usr === 'ci-bot') return res(['sim: ci-bot is a ServiceAccount in dev — bind it with --serviceaccount=dev:ci-bot (a --user=ci-bot binding grants the ServiceAccount nothing)'], 2);
          return res(['sim: this drill models pod-reader→alice, secret-reader→bob (--role, --user) and ClusterRole deployer→dev:ci-bot (--clusterrole, --serviceaccount)'], 2);
        }
        if (s[slot] && !(slot === 'b2' && s.b2Cluster)) return res(['error: failed to create rolebinding: rolebindings.rbac.authorization.k8s.io "' + (names[slot] === bn ? bn : names[slot]) + '" already exists' + (names[slot] === bn ? '' : ' (sim: one binding per subject in this drill)')], 1);
        if (slot === 'b2' && s.b2Cluster) return res(['sim: ci-bot already has a ClusterRoleBinding (a superset). Delete it first to model the namespaced RoleBinding.'], 2);
        names[slot] = bn;
        var p = {}; p[slot] = true; if (slot === 'b2') p.b2Cluster = false;
        return res(['rolebinding.rbac.authorization.k8s.io/' + bn + ' created'], 0, p, ['create-rolebinding', 'bind-' + slot]);
      }
      if (verb === 'create' && args[0] === 'clusterrolebinding') {
        var cn = args[1];
        if (flag(t, '--clusterrole') !== 'deployer' || flag(t, '--serviceaccount') !== 'dev:ci-bot' || !cn) return res(['sim: this drill models `kubectl create clusterrolebinding NAME --clusterrole=deployer --serviceaccount=dev:ci-bot`'], 2);
        if (s.b2 && s.b2Cluster) return res(['error: failed to create clusterrolebinding: clusterrolebindings.rbac.authorization.k8s.io "' + names.b2 + '" already exists'], 1);
        var note = s.b2 ? ['# sim: the dev RoleBinding is now redundant — this drill shows ci-bot’s effective (cluster-wide) grant'] : [];
        names.b2 = cn;
        return res(['clusterrolebinding.rbac.authorization.k8s.io/' + cn + ' created'].concat(note), 0, { b2: true, b2Cluster: true }, ['create-crb', 'bind-b2-cluster']);
      }
      if (verb === 'delete' && /^(rolebindings?|rb)$/.test(args[0] || '')) {
        var dn = args[1];
        if (ns !== 'dev') return notFound('rolebindings.rbac.authorization.k8s.io', dn || '');
        var dslot = dn === names.b0 && s.b0 ? 'b0' : (dn === names.b1 && s.b1 ? 'b1' : (dn === names.b2 && s.b2 && !s.b2Cluster ? 'b2' : null));
        if (!dslot) return notFound('rolebindings.rbac.authorization.k8s.io', dn || '');
        var dp = {}; dp[dslot] = false;
        return res(['rolebinding.rbac.authorization.k8s.io "' + dn + '" deleted'], 0, dp, ['delete-rolebinding', 'unbind-' + dslot]);
      }
      if (verb === 'delete' && /^(clusterrolebindings?|crb)$/.test(args[0] || '')) {
        if (args[1] !== names.b2 || !(s.b2 && s.b2Cluster)) return notFound('clusterrolebindings.rbac.authorization.k8s.io', args[1] || '');
        return res(['clusterrolebinding.rbac.authorization.k8s.io "' + args[1] + '" deleted'], 0, { b2: false, b2Cluster: false }, ['delete-crb']);
      }
      return unmodelled(t.join(' '), rbacPack.examples);
    },
    tasks: [
      { id: 'least-privilege', title: 'Grant alice read on pods in dev — and nothing more',
        goal: 'alice has no binding. Prove she is denied, bind her to the existing pod-reader Role in dev, then prove the grant stops at the namespace.',
        setup: { b0: false, b1: true, b2: true, b2Cluster: false, sameNs: true },
        steps: [
          { label: 'Prove alice cannot list pods in dev today', event: 'cani-alice-pods-dev-no', hint: 'kubectl auth can-i list pods -n dev --as alice' },
          { label: 'Bind alice to Role pod-reader in ns dev', state: function (s) { return !!s.b0; }, hint: 'kubectl create rolebinding alice-pod-reader --role=pod-reader --user=alice -n dev' },
          { label: 'alice can list pods in dev', event: 'cani-alice-pods-dev-yes', hint: 'kubectl auth can-i list pods -n dev --as alice' },
          { label: '…but not in prod (a RoleBinding is namespaced)', event: 'cani-alice-pods-prod-no', hint: 'kubectl auth can-i list pods -n prod --as alice' }
        ] },
      { id: 'cluster-scope', title: 'ClusterRole via RoleBinding vs ClusterRoleBinding',
        goal: 'ci-bot’s ClusterRole deployer is bound with a RoleBinding in dev. Show what that grants, then make it cluster-wide.',
        setup: { b0: true, b1: true, b2: true, b2Cluster: false, sameNs: true },
        steps: [
          { label: 'ci-bot can create deployments in dev', event: 'cani-ci-bot-deployments-dev-yes', hint: 'kubectl auth can-i create deployments -n dev --as system:serviceaccount:dev:ci-bot' },
          { label: '…but cannot get nodes (the RoleBinding scopes it)', event: 'cani-ci-bot-nodes-no', hint: 'kubectl auth can-i get nodes --as system:serviceaccount:dev:ci-bot' },
          { label: 'Bind deployer to ci-bot with a ClusterRoleBinding', state: function (s) { return s.b2 && s.b2Cluster; }, hint: 'kubectl create clusterrolebinding ci-bot-deployer --clusterrole=deployer --serviceaccount=dev:ci-bot' },
          { label: 'ci-bot can get nodes now', event: 'cani-ci-bot-nodes-yes', hint: 'kubectl auth can-i get nodes --as system:serviceaccount:dev:ci-bot' },
          { label: '…and create deployments in prod', event: 'cani-ci-bot-deployments-prod-yes', hint: 'kubectl auth can-i create deployments -n prod --as system:serviceaccount:dev:ci-bot' }
        ] },
      { id: 'revoke', title: 'Revoke bob’s secret access',
        goal: 'bob can read Secrets in dev. Find the binding that grants it, remove it, and prove the API now answers Forbidden.',
        setup: { b0: true, b1: true, b2: true, b2Cluster: false, sameNs: true },
        steps: [
          { label: 'Confirm bob can get secrets in dev', event: 'cani-bob-secrets-dev-yes', hint: 'kubectl auth can-i get secrets -n dev --as bob' },
          { label: 'Find the RoleBinding that grants it', event: 'get-rolebindings', hint: 'kubectl get rolebindings -n dev -o wide' },
          { label: 'Delete that RoleBinding', state: function (s) { return !s.b1; }, hint: 'kubectl delete rolebinding bob-secret-reader -n dev' },
          { label: 'bob is Forbidden now', event: 'get-secrets-forbidden', hint: 'kubectl get secrets -n dev --as bob' }
        ] }
    ]
  };

  /* ── pack: storage — StorageClass · PV/PVC · reclaim (CKA storage) ─────── */
  function jsonArg(t) {
    var raw = flag(t, ['-p', '--patch']);
    if (raw == null || raw === true) return { err: res(['error: must specify -p (--patch)'], 1) };
    try { return { v: JSON.parse(raw) }; } catch (e) { return { err: res(['error: unable to parse "' + raw + '": invalid JSON patch'], 1) }; }
  }
  var storagePack = {
    sim: 'storage-csi',
    prompt: 'student@controlplane:~$',
    files: {
      'consumer-pod.yaml': { yaml: ['apiVersion: v1', 'kind: Pod', 'metadata:', '  name: consumer', 'spec:', '  containers:', '  - name: app', '    image: busybox:1.37', '    command: ["sh", "-c", "while true; do date >> /data/log; sleep 5; done"]', '    volumeMounts:', '    - name: data', '      mountPath: /data', '  volumes:', '  - name: data', '    persistentVolumeClaim:', '      claimName: pvc-1'] },
      'pvc-1.yaml': { yaml: ['apiVersion: v1', 'kind: PersistentVolumeClaim', 'metadata:', '  name: pvc-1', 'spec:', '  # no storageClassName → the default StorageClass (if one is marked)', '  accessModes: ["ReadWriteOnce"]', '  resources:', '    requests:', '      storage: 10Gi'] }
    },
    examples: ['kubectl get pvc', 'kubectl get pv', 'kubectl get storageclass', 'kubectl describe pvc pvc-1',
      "kubectl patch pv pv-1 -p '{\"spec\":{\"persistentVolumeReclaimPolicy\":\"Retain\"}}'",
      "kubectl patch storageclass csi-gp3 -p '{\"metadata\":{\"annotations\":{\"storageclass.kubernetes.io/is-default-class\":\"true\"}}}'",
      'kubectl delete pod consumer', 'kubectl delete pvc pvc-1', 'kubectl get pods', 'cat consumer-pod.yaml'],
    run: function (u, s, d, ctx) {
      var t = u.t, m = d.metrics;
      var fr = fileRun(storagePack, t); if (fr) return fr;
      if (t[0] !== 'kubectl') return null;
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED), ns = nsOf(t);
      var kind = (args[0] || '').toLowerCase(), name = args[1] || '';
      if (/\//.test(kind)) { name = kind.split('/')[1]; kind = kind.split('/')[0]; }
      var isPvc = /^(pvc|persistentvolumeclaims?)$/.test(kind), isPv = /^(pv|persistentvolumes?)$/.test(kind), isSc = /^(sc|storageclass(es)?(\.storage\.k8s\.io)?)$/.test(kind), isPod = /^(pods?|po)$/.test(kind);
      if ((isPvc || isPod) && ns !== 'default' && ns !== '*') return res(['No resources found in ' + ns + ' namespace.'], 0);
      var pvc1Class = s.scDefault ? 'csi-gp3' : '<unset>';
      if (verb === 'get' && isPvc) {
        var rows = [['NAME', 'STATUS', 'VOLUME', 'CAPACITY', 'ACCESS MODES', 'STORAGECLASS', 'VOLUMEATTRIBUTESCLASS', 'AGE']];
        var b0 = m.pvc0 === 'Bound';
        rows.push(['pvc-0', m.pvc0, b0 ? 'pv-0' : '', b0 ? m.pv0Capacity : '', b0 ? 'RWO' : '', 'manual', '<unset>', '9d']);
        if (m.pvc1 !== 'deleted') rows.push(['pvc-1', m.pvc1, m.pvc1 === 'Pending' ? '' : 'pv-1', m.pvc1 === 'Pending' ? '' : '10Gi', m.pvc1 === 'Pending' ? '' : 'RWO', pvc1Class, '<unset>', '3d']);
        var ev = ['get-pvc', 'get-pvc-' + (m.pvc1 === 'deleted' ? 'gone' : m.pvc1.toLowerCase())];
        return res(table(rows), 0, null, ev);
      }
      if (verb === 'get' && isPv) {
        var r2 = [['NAME', 'CAPACITY', 'ACCESS MODES', 'RECLAIM POLICY', 'STATUS', 'CLAIM', 'STORAGECLASS', 'VOLUMEATTRIBUTESCLASS', 'REASON', 'AGE']];
        r2.push(['pv-0', m.pv0Capacity, 'RWO', 'Retain', m.pvc0 === 'Bound' ? 'Bound' : 'Available', m.pvc0 === 'Bound' ? 'default/pvc-0' : '', 'manual', '<unset>', '', '9d']);
        if (m.pv1 === 'Bound' || m.pv1 === 'Released') r2.push(['pv-1', '10Gi', 'RWO', s.retain ? 'Retain' : 'Delete', m.pv1, 'default/pvc-1', 'csi-gp3', '<unset>', '', '3d']);
        r2.push(['pv-2', '100Gi', 'RWO', 'Retain', 'Available', '', 'fast-ssd', '<unset>', '', '9d']);
        var e2 = ['get-pv', m.pv1 === 'Bound' ? (s.retain ? 'get-pv-retain' : 'get-pv-delete') : (m.pv1 === 'Released' ? 'get-pv-released' : (m.pv1 === 'deleted' ? 'get-pv-deleted' : 'get-pv-none'))];
        return res(table(r2), 0, null, e2);
      }
      if (verb === 'get' && isSc) {
        return res(table([['NAME', 'PROVISIONER', 'RECLAIMPOLICY', 'VOLUMEBINDINGMODE', 'ALLOWVOLUMEEXPANSION', 'AGE'],
          ['csi-gp3' + (s.scDefault ? ' (default)' : ''), 'ebs.csi.aws.com', 'Delete', s.wffc ? 'WaitForFirstConsumer' : 'Immediate', 'true', '30d'],
          ['fast-ssd', 'ebs.csi.aws.com', 'Retain', 'Immediate', 'true', '30d']]), 0, null, ['get-sc', s.scDefault ? 'get-sc-default' : 'get-sc-nodefault']);
      }
      if (verb === 'get' && isPod) {
        var r3 = [['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE']];
        if (m.pod === 'Running' || m.pod === 'multi-attach') r3.push(['consumer', '1/1', 'Running', '0', '3d']);
        if (m.pod === 'Pending') r3.push(['consumer', '0/1', 'Pending', '0', '3d']);
        if (m.pod === 'multi-attach') r3.push(['consumer-2', '0/1', 'ContainerCreating', '0', '2m']);
        if (r3.length === 1) return res(['No resources found in default namespace.'], 0, null, ['get-pods-none']);
        return res(table(r3), 0, null, ['get-pods', 'get-pods-' + m.pod.toLowerCase()]);
      }
      if (verb === 'describe' && isPvc) {
        if (name === 'pvc-0') return res(['Name:          pvc-0', 'StorageClass:  manual', 'Status:        ' + m.pvc0, 'Access Modes:  ' + (s.pvc0Rwx ? 'RWX' : 'RWO'), 'Events:        ' + (m.pvc0 === 'Bound' ? '<none>' : 'Normal  FailedBinding  persistentvolume-controller  no persistent volumes available for this claim and no storage class is set')], 0, null, ['describe-pvc0']);
        if (name !== 'pvc-1' || m.pvc1 === 'deleted') return notFound('persistentvolumeclaims', name);
        var L = ['Name:          pvc-1', 'Namespace:     default', 'StorageClass:  ' + (s.scDefault ? 'csi-gp3' : ''), 'Status:        ' + m.pvc1, 'Volume:        ' + (m.pvc1 === 'Pending' ? '' : 'pv-1'),
          'Finalizers:    [kubernetes.io/pvc-protection]', 'Capacity:      ' + (m.pvc1 === 'Pending' ? '' : '10Gi'), 'Access Modes:  ' + (m.pvc1 === 'Pending' ? '' : 'RWO'), 'VolumeMode:    Filesystem',
          'Used By:       ' + (m.pod === 'none' || m.pod === 'deleted' ? '<none>' : 'consumer'), 'Events:'];
        var e3 = ['describe-pvc'];
        if (m.pvc1 === 'Pending' && m.pendingWhy === 'no-default-class') { L.push('  Normal  FailedBinding  12s (x14 over 3m)  persistentvolume-controller  no persistent volumes available for this claim and no storage class is set'); e3.push('describe-pvc-nodefault'); }
        else if (m.pvc1 === 'Pending') { L.push('  Normal  WaitForFirstConsumer  9s (x6 over 1m)  persistentvolume-controller  waiting for first consumer to be created before binding'); e3.push('describe-pvc-wffc'); }
        else if (m.pvc1 === 'Terminating') { L.push('  (sim) deletionTimestamp set; the pvc-protection finalizer waits until no pod uses the claim'); e3.push('describe-pvc-terminating'); }
        else { L.push('  Normal  ProvisioningSucceeded  3d  ebs.csi.aws.com  Successfully provisioned volume pv-1'); e3.push('describe-pvc-bound'); }
        return res(L, 0, null, e3);
      }
      if (verb === 'patch' && isPv) {
        if (name !== 'pv-1' || !(m.pv1 === 'Bound' || m.pv1 === 'Released')) return notFound('persistentvolumes', name);
        var j = jsonArg(t); if (j.err) return j.err;
        var pol = j.v && j.v.spec && j.v.spec.persistentVolumeReclaimPolicy;
        if (pol !== 'Retain' && pol !== 'Delete') return res(['sim: this drill models spec.persistentVolumeReclaimPolicy Retain | Delete'], 2);
        return res(['persistentvolume/pv-1 patched' + ((pol === 'Retain') === !!s.retain ? ' (no change)' : '')], 0, { retain: pol === 'Retain' }, ['patch-pv', 'reclaim-' + pol.toLowerCase()]);
      }
      if ((verb === 'patch' || verb === 'annotate') && isSc) {
        if (name !== 'csi-gp3') return res([name === 'fast-ssd' ? 'sim: this drill models the default-class annotation on csi-gp3 (fast-ssd is a static class)' : 'Error from server (NotFound): storageclasses.storage.k8s.io "' + name + '" not found'], name === 'fast-ssd' ? 2 : 1);
        var val;
        if (verb === 'annotate') {
          var kv = /^storageclass\.kubernetes\.io\/is-default-class=(true|false)$/.exec(args[2] || '');
          if (!kv) return res(['sim: this drill models storageclass.kubernetes.io/is-default-class=true|false'], 2);
          if (s.scDefault && !hasFlag(t, '--overwrite') && kv[1] === 'true') return res(["error: --overwrite is false but found the following declared annotation(s): 'storageclass.kubernetes.io/is-default-class' already has a value (true)"], 1);
          val = kv[1] === 'true';
        } else {
          var jp = jsonArg(t); if (jp.err) return jp.err;
          var an = jp.v && jp.v.metadata && jp.v.metadata.annotations && jp.v.metadata.annotations['storageclass.kubernetes.io/is-default-class'];
          if (an !== 'true' && an !== 'false') return res(['sim: this drill models metadata.annotations["storageclass.kubernetes.io/is-default-class"] = "true" | "false" (a string)'], 2);
          val = an === 'true';
        }
        return res(['storageclass.storage.k8s.io/csi-gp3 ' + (verb === 'patch' ? 'patched' : 'annotated')], 0, { scDefault: val }, [val ? 'sc-default-on' : 'sc-default-off']);
      }
      if (verb === 'delete' && isPod) {
        if (name !== 'consumer' || m.pod === 'none' || m.pod === 'deleted') return notFound('pods', name);
        return res(['pod "consumer" deleted'], 0, { podDeleted: true }, ['delete-pod', s.pvcDeleted ? 'pod-released-claim' : 'delete-pod-only']);
      }
      if (verb === 'delete' && isPvc) {
        if (name !== 'pvc-1' || m.pvc1 === 'deleted' || m.pvc1 === 'Terminating') return name === 'pvc-1' && m.pvc1 === 'Terminating'
          ? res(['persistentvolumeclaim "pvc-1" deleted', '# sim: already Terminating — still held by the pvc-protection finalizer'], 0, null, ['delete-pvc'])
          : notFound('persistentvolumeclaims', name);
        var inUse = m.pod === 'Running' || m.pod === 'Pending' || m.pod === 'multi-attach';
        var lines = ['persistentvolumeclaim "pvc-1" deleted'];
        if (inUse) lines.push('# sim: a real kubectl now waits (--wait=true): kubernetes.io/pvc-protection holds the claim while pod consumer mounts it — Ctrl-C leaves it Terminating');
        return res(lines, 0, { pvcDeleted: true }, ['delete-pvc', inUse ? 'pvc-terminating' : 'pvc-deleted']);
      }
      if ((verb === 'apply' || verb === 'create') && hasFlag(t, ['-f', '--filename'])) {
        var a = applyFile(storagePack, t); if (a.err) return a.err;
        if (a.name === 'pvc-1.yaml') return res([m.pvc1 === 'deleted' ? 'sim: re-creating pvc-1 after deletion is not modelled — type `reset`' : 'persistentvolumeclaim/pvc-1 unchanged'], m.pvc1 === 'deleted' ? 2 : 0);
        if (m.pvc1 === 'deleted') return res(['sim: pvc-1 is gone — a new consumer would sit Pending; not modelled, type `reset`'], 2);
        if (m.pod === 'Running' || m.pod === 'Pending' || m.pod === 'multi-attach') return res(['pod/consumer unchanged'], 0);
        return res(['pod/consumer created'], 0, { podCreated: true, podDeleted: false }, ['create-pod']);
      }
      return unmodelled(t.join(' '), storagePack.examples);
    },
    tasks: [
      { id: 'retain-data', title: 'Keep the data when the claim is deleted',
        goal: 'pv-1 was dynamically provisioned with reclaimPolicy Delete. Make it Retain, remove the consumer and the claim, and prove the volume survived as Released.',
        setup: { scDefault: true, wffc: true, podCreated: true, podDeleted: false, secondNode: false, retain: false, pvcDeleted: false, pv0Big: true, pvc0Rwx: false },
        steps: [
          { label: 'Read pv-1’s current reclaim policy', event: 'get-pv-delete', hint: 'kubectl get pv' },
          { label: 'Patch pv-1 to reclaimPolicy Retain', state: function (s) { return !!s.retain; }, hint: "kubectl patch pv pv-1 -p '{\"spec\":{\"persistentVolumeReclaimPolicy\":\"Retain\"}}'" },
          { label: 'Delete the pod that mounts pvc-1', state: function (s) { return !!s.podDeleted; }, hint: 'kubectl delete pod consumer' },
          { label: 'Delete pvc-1', state: function (s) { return !!s.pvcDeleted; }, hint: 'kubectl delete pvc pvc-1' },
          { label: 'Confirm pv-1 is Released and its disk is kept', event: 'get-pv-released', hint: 'kubectl get pv' }
        ] },
      { id: 'pvc-protection', title: 'Delete a PVC that is still in use',
        goal: 'Delete pvc-1 while consumer still mounts it, see why it hangs in Terminating, then let it go and watch the Delete policy run.',
        setup: { scDefault: true, wffc: true, podCreated: true, podDeleted: false, secondNode: false, retain: false, pvcDeleted: false, pv0Big: true, pvc0Rwx: false },
        steps: [
          { label: 'Delete pvc-1 while the pod still uses it', event: 'pvc-terminating', hint: 'kubectl delete pvc pvc-1' },
          { label: 'See it stuck in Terminating', event: 'get-pvc-terminating', hint: 'kubectl get pvc' },
          { label: 'Find what holds it (Used By + finalizer)', event: 'describe-pvc-terminating', hint: 'kubectl describe pvc pvc-1' },
          { label: 'Delete the pod — the claim is released', event: 'pod-released-claim', hint: 'kubectl delete pod consumer' },
          { label: 'pv-1 and its disk followed reclaimPolicy Delete', event: 'get-pv-deleted', hint: 'kubectl get pv' }
        ] },
      { id: 'no-default-sc', title: 'Pending PVC: no default StorageClass',
        goal: 'pvc-1 omits storageClassName and nothing provisions it. Find out why and fix the class, not the claim.',
        setup: { scDefault: false, wffc: false, podCreated: true, podDeleted: false, secondNode: false, retain: false, pvcDeleted: false, pv0Big: true, pvc0Rwx: false },
        steps: [
          { label: 'See pvc-1 Pending', event: 'get-pvc-pending', hint: 'kubectl get pvc' },
          { label: 'Read the claim’s events', event: 'describe-pvc-nodefault', hint: 'kubectl describe pvc pvc-1' },
          { label: 'List StorageClasses — none is marked (default)', event: 'get-sc-nodefault', hint: 'kubectl get storageclass' },
          { label: 'Mark csi-gp3 as the default class', state: function (s) { return !!s.scDefault; }, hint: "kubectl patch storageclass csi-gp3 -p '{\"metadata\":{\"annotations\":{\"storageclass.kubernetes.io/is-default-class\":\"true\"}}}'" },
          { label: 'pvc-1 is Bound (the default class is applied retroactively)', event: 'get-pvc-bound', hint: 'kubectl get pvc' }
        ] }
    ]
  };

  /* ── pack: Ingress — controller · pathType · endpoints · TLS (CKA services & networking) ─────── */
  var INGRESS_NOTE = 'Note: the Kubernetes project retired ingress-nginx on 2026-03-24 (no further releases or security fixes). The Ingress API itself stays GA; Gateway API is the recommended successor; this drill covers the Ingress API only.';
  function curlArgs(t) {
    var url = null, o = { insecure: false, head: false, include: false, fail: false, w: null };
    for (var i = 1; i < t.length; i++) {
      var a = t[i];
      if (a === '-w' || a === '--write-out') { o.w = t[++i] || ''; continue; }
      if (a === '-o' || a === '--output' || a === '-H' || a === '-m' || a === '--max-time' || a === '--resolve' || a === '-X') { i++; continue; }
      if (a === '--insecure') { o.insecure = true; continue; }
      if (a === '--head') { o.head = true; continue; }
      if (a === '--include') { o.include = true; continue; }
      if (a === '--fail') { o.fail = true; continue; }
      if (/^-[a-zA-Z]+$/.test(a)) { if (/k/.test(a)) o.insecure = true; if (/I/.test(a)) o.head = true; if (/i/.test(a)) o.include = true; if (/f/.test(a)) o.fail = true; continue; }
      if (a.charAt(0) !== '-') url = a;
    }
    var m = /^(https?):\/\/([^\/:]+)(?::\d+)?(\/[^?#]*)?/.exec(url || '');
    o.url = url; o.scheme = m ? m[1] : null; o.host = m ? m[2] : null; o.path = m ? (m[3] || '/') : null;
    return o;
  }
  var ingressPack = {
    sim: 'ingress-routing',
    prompt: 'student@controlplane:~$',
    note: INGRESS_NOTE,
    files: {
      'ingress-controller.yaml': { yaml: ['# Ingress controller for class "nginx" (Deployment + Service type LoadBalancer + IngressClass).', '# sim: applying this file stands in for installing a controller. ' + INGRESS_NOTE] },
      'shop-ingress.yaml': { yaml: ['apiVersion: networking.k8s.io/v1', 'kind: Ingress', 'metadata:', '  name: shop', 'spec:', '  ingressClassName: nginx', '  tls:', '  - hosts: [shop.example.com]', '    secretName: shop-tls', '  rules:', '  - host: shop.example.com', '    http:', '      paths:', '      - path: /api', '        pathType: Prefix', '        backend: { service: { name: service-0, port: { number: 80 } } }', '      - path: /web', '        pathType: Prefix', '        backend: { service: { name: service-1, port: { number: 80 } } }'] }
    },
    examples: ['kubectl get ingress', 'kubectl describe ingress shop', 'kubectl get ingress shop -o yaml', 'curl -sI https://shop.example.com/api/v1/orders',
      'kubectl get endpointslices -l kubernetes.io/service-name=service-0', 'kubectl get svc service-0 -o wide', 'kubectl get pods --show-labels',
      "kubectl patch service service-0 -p '{\"spec\":{\"selector\":{\"app\":\"api\"}}}'",
      'kubectl patch ingress shop --type=json -p \'[{"op":"replace","path":"/spec/rules/0/http/paths/0/pathType","value":"Prefix"}]\'',
      'kubectl create secret tls shop-tls --cert=shop.crt --key=shop.key', 'kubectl get secret shop-tls', 'kubectl get ingressclass',
      'kubectl get pods -A -l app.kubernetes.io/name=ingress-nginx'],
    run: function (u, s, d, ctx) {
      var t = u.t;
      var fr = fileRun(ingressPack, t); if (fr) return fr;
      if (t[0] === 'curl') {
        var c = curlArgs(t);
        if (!c.host) return res(['curl: (3) URL rejected: No host part in the URL'], 3);
        if (c.host !== 'shop.example.com') return res(['curl: (6) Could not resolve host: ' + c.host], 6);
        if (!s.controller) return res(['curl: (7) Failed to connect to shop.example.com port ' + (c.scheme === 'https' ? 443 : 80) + ' after 2 ms: Couldn\'t connect to server'], 7, null, ['curl', 'curl-noconnect']);
        if (c.scheme === 'http') return res(['HTTP/1.1 308 Permanent Redirect', 'Location: https://shop.example.com' + c.path], 0, null, ['curl', 'curl-308']);
        if (!s.tlsSecret && !c.insecure) return res(['curl: (60) SSL certificate problem: self-signed certificate', 'More details here: https://curl.se/docs/sslcerts.html'], 60, null, ['curl', 'curl-cert-error']);
        var r = S_ingressMatch(c.path, [{ path: '/api', type: s.apiExact ? 'Exact' : 'Prefix', svc: 0 }, { path: '/web', type: 'Prefix', svc: 1 }]);
        var code = !r ? 404 : (r.svc === 0 && !s.apiReady ? 503 : 200);
        var reason = { 200: 'OK', 404: 'Not Found', 503: 'Service Temporarily Unavailable' }[code];
        var ev = ['curl', 'curl-' + code];
        if (code === 200) ev.push(s.tlsSecret && !c.insecure ? 'curl-200-verified' : 'curl-200-insecure');
        var out;
        if (c.w && /http_code/.test(c.w)) out = [String(code)];
        else if (c.head || c.include) {
          out = ['HTTP/2 ' + code, 'content-type: ' + (code === 200 ? 'application/json' : 'text/html'), 'x-sim-note: computed by the rules engine' + (r ? ' (rule ' + r.path + ' ' + r.type + ' → service-' + r.svc + ')' : ' (no rule matched → default backend)')];
          if (c.include && !c.head) out.push('', code === 200 ? '{"service":"service-' + r.svc + '","path":"' + c.path + '"}' : '<html><head><title>' + code + ' ' + reason + '</title></head></html>');
        } else out = [code === 200 ? '{"service":"service-' + r.svc + '","path":"' + c.path + '"}' : '<html><head><title>' + code + ' ' + reason + '</title></head></html>'];
        return res(out, c.fail && code >= 400 ? 22 : 0, null, ev);
      }
      if (t[0] !== 'kubectl') return null;
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED), ns = nsOf(t), out2 = flag(t, ['-o', '--output']);
      var kind = (args[0] || '').toLowerCase(), name = args[1] || '';
      if (/\//.test(kind)) { name = kind.split('/')[1]; kind = kind.split('/')[0]; }
      var isIng = /^(ing|ingress(es)?(\.networking\.k8s\.io)?)$/.test(kind);
      var addr = s.controller ? '203.0.113.10' : '';
      var ep0 = s.apiReady ? '10.244.1.5:8080,10.244.2.7:8080' : '';
      if (verb === 'get' && isIng && ns !== '*' && ns !== 'default') return res(['No resources found in ' + ns + ' namespace.'], 0);
      if (verb === 'get' && isIng && out2 && /yaml|jsonpath/.test(out2)) {
        var pt = s.apiExact ? 'Exact' : 'Prefix';
        if (/jsonpath/.test(out2)) {
          if (!/pathType/.test(out2)) return res(['sim: this drill models jsonpath on .spec.rules[0].http.paths[*].pathType'], 2);
          return res([/\[\*\]/.test(out2) ? pt + ' Prefix' : pt], 0, null, ['ingress-pathtype', 'ingress-pathtype-' + pt.toLowerCase()]);
        }
        var y = ingressPack.files['shop-ingress.yaml'].yaml.slice();
        y[14] = '        pathType: ' + pt;
        y = y.concat(['status:', '  loadBalancer:', s.controller ? '    ingress:\n    - ip: 203.0.113.10' : '    {}']);
        return res(y.join('\n').split('\n'), 0, null, ['ingress-yaml', 'ingress-pathtype-' + pt.toLowerCase()]);
      }
      if (verb === 'get' && isIng) {
        return res(table([['NAME', 'CLASS', 'HOSTS', 'ADDRESS', 'PORTS', 'AGE'], ['shop', 'nginx', 'shop.example.com', addr || ' ', '80, 443', '5d']]), 0, null, ['get-ingress', s.controller ? 'get-ingress-address' : 'get-ingress-noaddress']);
      }
      if (verb === 'describe' && isIng) {
        if (name !== 'shop') return notFound('ingresses.networking.k8s.io', name);
        var L = ['Name:             shop', 'Labels:           <none>', 'Namespace:        default', 'Address:          ' + addr, 'Ingress Class:    nginx', 'Default backend:  <default>',
          'TLS:', '  shop-tls terminates shop.example.com', 'Rules:', '  Host              Path  Backends', '  ----              ----  --------', '  shop.example.com',
          '                    /api   service-0:80 (' + ep0 + ')', '                    /web   service-1:80 (10.244.1.9:8080,10.244.3.4:8080)', 'Annotations:        <none>', 'Events:             <none>'];
        return res(L, 0, null, ['describe-ingress', s.apiReady ? 'describe-ingress-endpoints' : 'describe-ingress-noendpoints']);
      }
      if (verb === 'get' && /^(endpointslices?(\.discovery\.k8s\.io)?|eps)$/.test(kind)) {
        var sel = flag(t, ['-l', '--selector']) || '';
        var rows = [['NAME', 'ADDRESSTYPE', 'PORTS', 'ENDPOINTS', 'AGE']];
        if (!sel || /service-0/.test(sel)) rows.push(['service-0-x7k2p', 'IPv4', s.apiReady ? '8080' : '<unset>', s.apiReady ? '10.244.1.5,10.244.2.7' : '<unset>', '5d']);
        if (!sel || /service-1/.test(sel)) rows.push(['service-1-m3q9d', 'IPv4', '8080', '10.244.1.9,10.244.3.4', '5d']);
        return res(table(rows), 0, null, ['endpoints', s.apiReady || (sel && !/service-0/.test(sel)) ? 'endpoints-ok' : 'endpoints-empty']);
      }
      if (verb === 'get' && /^(ep|endpoints)$/.test(kind)) {
        return res(['Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice'].concat(table([['NAME', 'ENDPOINTS', 'AGE'], ['service-0', s.apiReady ? '10.244.1.5:8080,10.244.2.7:8080' : '<none>', '5d'], ['service-1', '10.244.1.9:8080,10.244.3.4:8080', '5d']])), 0, null, ['endpoints', s.apiReady ? 'endpoints-ok' : 'endpoints-empty']);
      }
      if (verb === 'get' && /^(svc|services?)$/.test(kind)) {
        var wide = out2 === 'wide';
        var rr = [['NAME', 'TYPE', 'CLUSTER-IP', 'EXTERNAL-IP', 'PORT(S)', 'AGE'].concat(wide ? ['SELECTOR'] : [])];
        if (!name || name === 'service-0') rr.push(['service-0', 'ClusterIP', '10.96.20.11', '<none>', '80/TCP', '5d'].concat(wide ? [s.apiReady ? 'app=api' : 'app=api-v2'] : []));
        if (!name || name === 'service-1') rr.push(['service-1', 'ClusterIP', '10.96.20.12', '<none>', '80/TCP', '5d'].concat(wide ? ['app=web'] : []));
        if (rr.length === 1) return notFound('services', name);
        return res(table(rr), 0, null, ['get-svc', wide ? 'get-svc-selector' : 'get-svc-plain']);
      }
      if (verb === 'get' && /^(pods?|po)$/.test(kind)) {
        var lsel = flag(t, ['-l', '--selector']) || '';
        if (/ingress-nginx/.test(lsel)) {
          if (!s.controller) return res(['No resources found'], 0, null, ['get-controller', 'get-controller-none']);
          return res(table([['NAMESPACE', 'NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE'], ['ingress-nginx', 'ingress-nginx-controller-5f8c9-qk2wd', '1/1', 'Running', '0', '30d']]).concat(['# sim: ' + INGRESS_NOTE]), 0, null, ['get-controller', 'get-controller-running']);
        }
        var labels = hasFlag(t, '--show-labels');
        var pr = [['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE'].concat(labels ? ['LABELS'] : [])];
        [['api-6d4b8-2kq9x', 'app=api,pod-template-hash=6d4b8'], ['api-6d4b8-7zv4m', 'app=api,pod-template-hash=6d4b8'], ['web-58c7f-h2n8p', 'app=web,pod-template-hash=58c7f'], ['web-58c7f-t9w3c', 'app=web,pod-template-hash=58c7f']].forEach(function (p) {
          pr.push([p[0], '1/1', 'Running', '0', '5d'].concat(labels ? [p[1]] : []));
        });
        return res(table(pr), 0, null, ['get-pods', labels ? 'pods-labels' : 'get-pods-plain']);
      }
      if (verb === 'get' && /^(ingressclass(es)?)$/.test(kind)) {
        if (!s.controller) return res(['No resources found'], 0, null, ['get-ingressclass-none']);
        return res(table([['NAME', 'CONTROLLER', 'PARAMETERS', 'AGE'], ['nginx', 'k8s.io/ingress-nginx', '<none>', '30d']]), 0, null, ['get-ingressclass']);
      }
      if (verb === 'get' && /^secrets?$/.test(kind)) {
        if (name && name !== 'shop-tls') return notFound('secrets', name);
        if (!s.tlsSecret) return name ? res(['Error from server (NotFound): secrets "shop-tls" not found'], 1, null, ['get-secret-missing']) : res(['No resources found in default namespace.'], 0, null, ['get-secret-missing']);
        return res(table([['NAME', 'TYPE', 'DATA', 'AGE'], ['shop-tls', 'kubernetes.io/tls', '2', '5d']]), 0, null, ['get-secret', 'get-secret-ok']);
      }
      if (verb === 'create' && args[0] === 'secret' && args[1] === 'tls') {
        if (args[2] !== 'shop-tls' || !flag(t, '--cert') || !flag(t, '--key')) return res(['sim: this drill models `kubectl create secret tls shop-tls --cert=shop.crt --key=shop.key`'], 2);
        if (s.tlsSecret) return res(['error: failed to create secret secrets "shop-tls" already exists'], 1);
        return res(['secret/shop-tls created'], 0, { tlsSecret: true }, ['create-secret-tls']);
      }
      if (verb === 'delete' && /^secrets?$/.test(kind)) {
        if (name !== 'shop-tls' || !s.tlsSecret) return notFound('secrets', name);
        return res(['secret "shop-tls" deleted'], 0, { tlsSecret: false }, ['delete-secret-tls']);
      }
      if (verb === 'patch' && /^(svc|services?)$/.test(kind)) {
        if (name !== 'service-0') return res(['sim: this drill models the selector of service-0'], 2);
        var j = jsonArg(t); if (j.err) return j.err;
        var app = j.v && j.v.spec && j.v.spec.selector && j.v.spec.selector.app;
        if (!app) return res(['sim: this drill models spec.selector.app on service-0'], 2);
        return res(['service/service-0 patched'], 0, { apiReady: app === 'api' }, ['patch-svc', app === 'api' ? 'selector-fixed' : 'selector-broken']);
      }
      if (verb === 'set' && args[0] === 'selector') {
        var sv = (args[1] || '').replace(/^(svc|service)\//, ''), kvs = args[args[1] && /^(svc|service|services)$/.test(args[1]) ? 3 : 2] || '';
        if (args[1] && /^(svc|service|services)$/.test(args[1])) sv = args[2];
        var mm = /^app=([a-z0-9-]+)$/.exec(kvs);
        if (sv !== 'service-0' || !mm) return res(['sim: this drill models `kubectl set selector service service-0 app=api`'], 2);
        return res(['service/service-0 selector updated'], 0, { apiReady: mm[1] === 'api' }, ['patch-svc', mm[1] === 'api' ? 'selector-fixed' : 'selector-broken']);
      }
      if (verb === 'patch' && isIng) {
        if (name !== 'shop') return notFound('ingresses.networking.k8s.io', name);
        var jj = jsonArg(t); if (jj.err) return jj.err;
        var ops = Array.isArray(jj.v) ? jj.v : null;
        var op = ops && ops.filter(function (o) { return /^\/spec\/rules\/0\/http\/paths\/0\/pathType$/.test(o.path || ''); })[0];
        if (flag(t, '--type') !== 'json' || !op || (op.value !== 'Exact' && op.value !== 'Prefix')) return res(['sim: this drill models a JSON patch: --type=json -p \'[{"op":"replace","path":"/spec/rules/0/http/paths/0/pathType","value":"Prefix"}]\''], 2);
        return res(['ingress.networking.k8s.io/shop patched'], 0, { apiExact: op.value === 'Exact' }, ['patch-ingress', 'pathtype-' + op.value.toLowerCase()]);
      }
      if ((verb === 'apply' || verb === 'delete') && hasFlag(t, ['-f', '--filename'])) {
        var a = applyFile(ingressPack, t); if (a.err) return a.err;
        if (a.name === 'ingress-controller.yaml') {
          if (verb === 'delete') return s.controller ? res(['(sim) ingress controller removed'], 0, { controller: false }, ['controller-removed']) : res(['Error from server (NotFound): deployments.apps "ingress-nginx-controller" not found'], 1);
          return res(s.controller ? ['ingressclass.networking.k8s.io/nginx unchanged', 'deployment.apps/ingress-nginx-controller unchanged'] : ['ingressclass.networking.k8s.io/nginx created', 'deployment.apps/ingress-nginx-controller created', 'service/ingress-nginx-controller created'], 0, s.controller ? null : { controller: true }, ['controller-installed']);
        }
        if (verb === 'delete') return res(['sim: deleting the shop Ingress is not modelled in this drill'], 2);
        return res(['ingress.networking.k8s.io/shop ' + (s.apiExact ? 'configured' : 'unchanged')], 0, { apiExact: false }, ['apply-ingress']);
      }
      if (verb === 'edit') return res(['sim: interactive editors are not modelled — use kubectl patch (see `help`)'], 2);
      return unmodelled(t.join(' '), ingressPack.examples);
    },
    tasks: [
      { id: 'exact-404', title: 'Fix a 404 on /api/v1/orders',
        goal: 'Orders started returning 404 after a change to the shop Ingress. Reproduce it, find the rule’s pathType, and fix the rule.',
        setup: { controller: true, apiExact: true, apiReady: true, tlsSecret: true },
        steps: [
          { label: 'Reproduce the 404', event: 'curl-404', hint: 'curl -sI https://shop.example.com/api/v1/orders' },
          { label: 'Read the /api rule’s pathType', event: 'ingress-pathtype-exact', hint: 'kubectl get ingress shop -o yaml' },
          { label: 'Switch /api to pathType Prefix', state: function (s) { return !s.apiExact; }, hint: 'kubectl patch ingress shop --type=json -p \'[{"op":"replace","path":"/spec/rules/0/http/paths/0/pathType","value":"Prefix"}]\'' },
          { label: 'GET /api/v1/orders reaches service-0', event: 'curl-200', hint: 'curl -sI https://shop.example.com/api/v1/orders' }
        ] },
      { id: 'no-endpoints', title: '503: a Service with no endpoints',
        goal: 'The route exists but /api answers 503. Follow Ingress → Service → EndpointSlice → pod labels to the cause.',
        setup: { controller: true, apiExact: false, apiReady: false, tlsSecret: true },
        steps: [
          { label: 'Reproduce the 503', event: 'curl-503', hint: 'curl -sI https://shop.example.com/api/v1/orders' },
          { label: 'Find that service-0 has no endpoints', event: 'endpoints-empty', hint: 'kubectl get endpointslices -l kubernetes.io/service-name=service-0' },
          { label: 'Compare the Service selector with the pod labels', event: 'pods-labels', hint: 'kubectl get svc service-0 -o wide  then  kubectl get pods --show-labels' },
          { label: 'Fix service-0’s selector', state: function (s) { return !!s.apiReady; }, hint: "kubectl patch service service-0 -p '{\"spec\":{\"selector\":{\"app\":\"api\"}}}'" },
          { label: 'Get a 200 from /api/v1/orders', event: 'curl-200', hint: 'curl -sI https://shop.example.com/api/v1/orders' }
        ] },
      { id: 'tls', title: 'Certificate warning: the TLS Secret is missing',
        goal: 'Browsers warn on shop.example.com. Prove curl rejects the certificate, find the missing Secret, create it, and verify HTTPS without -k.',
        setup: { controller: true, apiExact: false, apiReady: true, tlsSecret: false },
        steps: [
          { label: 'See curl reject the certificate', event: 'curl-cert-error', hint: 'curl -sI https://shop.example.com/api' },
          { label: 'Find that Secret shop-tls does not exist', event: 'get-secret-missing', hint: 'kubectl get secret shop-tls' },
          { label: 'Create the kubernetes.io/tls Secret', state: function (s) { return !!s.tlsSecret; }, hint: 'kubectl create secret tls shop-tls --cert=shop.crt --key=shop.key' },
          { label: 'HTTPS verifies (no -k) and answers 200', event: 'curl-200-verified', hint: 'curl -sI https://shop.example.com/api' }
        ] }
    ]
  };
  function S_ingressMatch(path, rules) { var S = Sims(); return S && S.ingressMatch ? S.ingressMatch(path, rules) : null; }

  var PACKS = {};
  [etcdPack, cpPack, schedPack, hpaPack, awsPack, netpolPack, rbacPack, storagePack, ingressPack].forEach(function (p) { PACKS[p.sim] = p; });

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
    },
    /* v1.2.0 (2026-10-20) */
    'netpol-isolation': {
      'lock-api': [
        ['Probe api from inside a pod in the untrusted namespace — exec into its Deployment and hit the Service on 8080.', '^(pod-untrusted-[01]|edge-deny-[01])$'],
        ['There is a ready-made manifest in your home directory that selects app=api for Ingress with no rules. Read it, then apply it.', '^(netpol-manifest|netpol-shield-ring)$'],
        ['Now probe from the frontend namespace. Isolation is not selective until you add a rule.', '^(pod-frontend-[01]|edge-allow-[01])$'],
        ['Apply the manifest whose ingress rule uses a namespaceSelector for frontend.', '^(netpol-manifest|edge-allow-[01])$'],
        ['Probe from frontend again.', '^edge-allow-[01]$'],
        ['And from untrusted: no rule admits it, so the allow-list drops it.', '^deny-block-[01]$']
      ],
      'egress-dns': [
        ['The lock-down manifest adds policyTypes Egress with a single rule to the db pods on 5432. Apply it.', '^(netpol-manifest|netpol-shield-ring)$'],
        ['Exec into the api Deployment in backend and resolve the db Service name.', '^(kube-dns|edge-egress-dns)$'],
        ['Describe the policy and read the “Allowing egress traffic” block.', '^netpol-manifest$'],
        ['Egress isolation blocks port 53 too. Apply the manifest that adds kube-dns in kube-system on UDP and TCP 53.', '^edge-egress-dns$'],
        ['Run the same lookup again.', '^(kube-dns|pod-backend-[01])$']
      ],
      'flannel': [
        ['List NetworkPolicies in the namespace where api lives.', '^netpol-manifest$'],
        ['Probe api from the untrusted namespace anyway.', '^(pod-untrusted-[01]|edge-deny-[01])$'],
        ['The pod network is a DaemonSet. List DaemonSets across all namespaces and read the names.', '^cni-enforcer$'],
        ['flannel does not implement NetworkPolicy. Use the lab’s CNI verb to stand in for migrating to Calico or Cilium.', '^cni-enforcer$'],
        ['Probe from untrusted one more time.', '^deny-block-[01]$']
      ]
    },
    'rbac-authz': {
      'least-privilege': [
        ['Ask the API server on alice’s behalf: auth can-i with impersonation, in namespace dev.', '^(user-0|api-pods)$'],
        ['The Role already exists in dev. Create the namespaced binding that ties user alice to it.', '^(rolebinding-0|edge-u0-b0|edge-b0-r0)$'],
        ['Ask the same can-i question again.', '^(edge-r0-pods|verbs-pods)$'],
        ['Ask the same question for another namespace — prod.', '^(user-0|rolebinding-0)$']
      ],
      'cluster-scope': [
        ['ci-bot is a ServiceAccount: impersonate it as system:serviceaccount:<namespace>:<name> and ask about creating deployments in dev.', '^(user-2|edge-r2-deploys)$'],
        ['Nodes are cluster-scoped. Ask whether ci-bot can get them (no namespace flag needed).', '^(edge-r2-nodes|api-nodes)$'],
        ['Only a cluster-wide binding grants a ClusterRole on cluster-scoped resources. Create one for the same ServiceAccount.', '^(rolebinding-2|edge-u2-b2)$'],
        ['Ask about nodes again.', '^(edge-r2-nodes|verbs-nodes)$'],
        ['Ask about creating deployments in prod.', '^(edge-r2-deploys|api-deployments)$']
      ],
      'revoke': [
        ['Impersonate bob and ask about getting secrets in dev.', '^(user-1|api-secrets)$'],
        ['List the RoleBindings in dev with the wide output — it shows the subjects.', '^(rolebinding-1|edge-u1-b1)$'],
        ['RBAC has no deny rules: remove the grant by deleting bob’s binding.', '^(rolebinding-1|edge-b1-r1)$'],
        ['Try to read the secrets as bob and read the API’s answer.', '^(edge-r1-secrets|verbs-secrets)$']
      ]
    },
    'storage-csi': {
      'retain-data': [
        ['List the PersistentVolumes and read the RECLAIM POLICY column for pv-1.', '^(pv-1|backend-disk-1)$'],
        ['The reclaim policy lives on the PV spec (persistentVolumeReclaimPolicy). Patch the volume, not the claim.', '^pv-1$'],
        ['A claim in use cannot go away. Remove the pod that mounts it first.', '^(consumer-pod|volume-mount)$'],
        ['Now delete the claim itself.', '^(pvc-1|edge-pv1-pvc1)$'],
        ['List the volumes again: STATUS and whether pv-1 is still there tell the story.', '^(pv-1|backend-disk-1|platter-1)$']
      ],
      'pvc-protection': [
        ['Delete the claim while the pod is still running.', '^(pvc-1|consumer-pod)$'],
        ['List the claims and read pvc-1’s STATUS.', '^pvc-1$'],
        ['Describe the claim: look at Finalizers and Used By.', '^(pvc-1|edge-pvc-pod)$'],
        ['The finalizer lets go once no pod uses the claim. Remove that pod.', '^(consumer-pod|volume-mount)$'],
        ['List the volumes: what did the StorageClass’s default reclaim policy do to pv-1?', '^(pv-1|edge-csi-pv1)$']
      ],
      'no-default-sc': [
        ['List the claims in the default namespace.', '^pvc-1$'],
        ['Describe pvc-1 and read the persistentvolume-controller event.', '^(pvc-1|csi-controller)$'],
        ['List the StorageClasses and look for the (default) marker.', '^(storage-class|sc-provisioner)$'],
        ['A class becomes the default through the storageclass.kubernetes.io/is-default-class annotation, set to the string "true".', '^(storage-class|edge-sc-csi)$'],
        ['List the claims again — a claim with no class gets the new default retroactively.', '^(pvc-1|pv-1)$']
      ]
    },
    'ingress-routing': {
      'exact-404': [
        ['Request the orders URL over HTTPS and read only the status line.', '^(client-0|req-0-[0-3])$'],
        ['describe does not print pathType — read the Ingress back as YAML.', '^rule-0$'],
        ['pathType sits inside a list, so use a JSON patch that replaces paths/0/pathType.', '^rule-0$'],
        ['Request the orders URL again.', '^(client-0|route-0-[0-4]|service-0)$']
      ],
      'no-endpoints': [
        ['Request the orders URL and read the status line.', '^(client-0|service-0)$'],
        ['A Service’s backends are EndpointSlices labelled with kubernetes.io/service-name.', '^(service-0|endpoint-pod-[01])$'],
        ['Show the Service’s selector (wide output), then the pods’ labels, and compare.', '^(service-0|endpoint-pod-[01])$'],
        ['Point the Service selector at the label the api pods actually carry.', '^service-0$'],
        ['Request the orders URL once more.', '^(ep-[01]-[0-2]|endpoint-pod-[01])$']
      ],
      'tls': [
        ['Request the /api URL over HTTPS without skipping certificate checks.', '^(tls-terminate|client-1)$'],
        ['spec.tls names a Secret. Ask for that Secret by name.', '^(rule-2|tls-terminate)$'],
        ['kubectl has a dedicated generator for kubernetes.io/tls Secrets; the cert and key files are in your home directory.', '^(rule-2|tls-terminate)$'],
        ['Repeat the HTTPS request — still without the insecure flag.', '^(tls-terminate|client-1|req-1-[0-3])$']
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
        .concat(['Lab verbs: help · check · hint · solution · task · history · clear · reset' + (/fault/.test(p.examples.join(' ')) || p.sim === 'hpa-scale' ? ' · fault … (lab-only fault injection)' : '')])
        .concat(p.files ? ['Lab files (ls / cat / kubectl apply -f): ' + Object.keys(p.files).join('  ')] : []).concat(p.note ? [p.note] : []), 0, null, ['help'], { verb: 'help' });
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
      if (/^(kubectl|etcdctl|crictl|aws|curl|systemctl|mv|ls|cat|fault|helm)$/.test(head)) r = unmodelled(raw, p.examples);
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


  /* ── v1.2.0 voice-to-command (pure): one spoken utterance → a lab verb, or command text for the input ──
   * Deterministic word rules + snapping to this drill's own vocabulary (example + solution tokens). The player
   * runs lab verbs directly but only TYPES a spoken command into the prompt — the learner confirms with Enter. */
  var SPOKEN_VERBS = [
    [/^(lab muse,? )?(check|verify|check (it|this|again|my (work|task|step|solution|answer)))$/, 'check'],
    [/^(lab muse,? )?(hint|a hint|give me a hint|(i need|show me) a hint|help me)$/, 'hint'],
    [/^(lab muse,? )?(solution|show (me )?(the )?solution|give me the (answer|solution|command))$/, 'solution'],
    [/^(task|progress|show (my )?progress|status)$/, 'task'],
    [/^(reset|start over|restart( the task)?)$/, 'reset'],
    [/^(clear|clear (the )?screen)$/, 'clear'],
    [/^(help|what can i (type|say))$/, 'help']
  ];
  var NUMBER_WORDS = { zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10 };
  var SPOKEN_RULES = [
    [/\b(cube|kube|queue|cue|coupe) ?(control|ctl|cuttle|cuddle|cattle|c t l)\b/g, 'kubectl'],
    [/\bk u b e c t l\b/g, 'kubectl'],
    [/\b(etcd|et cd|e t c d) ?(control|ctl|c t l)\b/g, 'etcdctl'],
    [/\b(cri|cry|c r i) ?(control|ctl|c t l)\b/g, 'crictl'],
    [/\bm v\b/g, 'mv'], [/\bl s\b/g, 'ls'], [/\bp v c\b/g, 'pvc'], [/\bp v\b/g, 'pv'], [/\bh p a\b/g, 'hpa'], [/\bt l s\b/g, 'tls'], [/\br d s\b/g, 'rds'], [/\bd n s\b/g, 'dns'],
    [/\bnet pol\b|\bnetwork ?polic(y|ies)\b/g, 'networkpolicy'],
    [/\bname ?space\b/g, 'namespace'], [/\brole ?binding(s?)\b/g, 'rolebinding$1'], [/\bcluster ?role ?binding(s?)\b/g, 'clusterrolebinding$1'], [/\bcluster ?role\b/g, 'clusterrole'], [/\bservice ?account\b/g, 'serviceaccount'],
    [/\bstorage ?class(es)?\b/g, 'storageclass$1'], [/\bendpoint ?slices?\b/g, 'endpointslices'], [/\bdaemon ?sets?\b/g, 'daemonsets'],
    [/\bcan i\b/g, 'can-i'], [/\bsudo\b/g, 'sudo'],
    [/\b(dash dash|double dash|minus minus)\s+(?=(curl|wget|nslookup|dig|host|getent|sh|bash|cat|ls|env)\b)/g, '-- '],
    [/\b(dash dash|double dash|minus minus)\s+/g, '--'], [/\b(dash|minus|hyphen)\s+/g, '-'],
    [/\s*\b(slash|forward slash)\b\s*/g, '/'], [/\s*\b(dot|period)\b\s*/g, '.'],
    [/\s*\b(equals|equal|equal sign)\b\s*/g, '='], [/\s*\bcolon\b\s*/g, ':']
  ];
  function vocab(p) {
    var v = {};
    p.examples.concat(p.tasks.reduce(function (a, tk) { return a.concat(tk.steps.map(function (st) { return st.hint; })); }, []))
      .forEach(function (line) { String(line).split(/\s{2}then\s{2}/).forEach(function (l) { tokenize(l).forEach(function (w) {
        v[w] = 1;
        if (/=/.test(w)) v[w.slice(w.indexOf('=') + 1)] = 1;
        w.split('/').forEach(function (seg) { if (seg) v[seg] = 1; });
      }); }); });
    Object.keys(p.files || {}).forEach(function (f) { v[f] = 1; });
    return Object.keys(v);
  }
  function inVocab(words, w) {
    for (var i = 0; i < words.length; i++) {
      var x = words[i];
      if (x === w || x.indexOf(w + '-') === 0 || x.indexOf(w + '.') === 0 || x.indexOf(w + '/') === 0) return true;
    }
    return false;
  }
  function fromSpeech(transcript, simId) {
    var txt = String(transcript == null ? '' : transcript).toLowerCase().replace(/[“”"]/g, '').replace(/[.!?,]+$/, '').replace(/\s+/g, ' ').trim();
    if (!txt) return null;
    var vt = txt.replace(/^(hey |ok |okay )?(lab )?muse[,.]? /, '').replace(/^please /, '').replace(/[,.]? please$/, '');
    for (var i = 0; i < SPOKEN_VERBS.length; i++) if (SPOKEN_VERBS[i][0].test(vt)) return { line: SPOKEN_VERBS[i][1], verb: true };
    var line = ' ' + txt + ' ';
    SPOKEN_RULES.forEach(function (r) { line = line.replace(r[0], r[1]); });
    line = line.replace(/\b(zero|one|two|three|four|five|six|seven|eight|nine|ten)\b/g, function (w) { return String(NUMBER_WORDS[w]); }).replace(/(\.ya?ml)\//g, '$1 /').trim();
    var p = PACKS[simId], toks = line.split(/\s+/).filter(Boolean);
    if (p) {
      var words = vocab(p), changed = true;
      /* "mv/etc/…" → "mv /etc/…" when the part before the first slash is a whole command word of this drill. */
      toks = toks.join(' ').split(' ').reduce(function (acc, w) {
        var i2 = w.indexOf('/'), head = w.slice(0, i2);
        if (i2 > 0 && /^[a-z]+$/.test(head) && /^(mv|cp|ls|cat|sudo)$/.test(head)) return acc.concat([head, w.slice(i2)]);
        return acc.concat([w]);
      }, []);
      while (changed) {
        changed = false;
        for (var k = 0; k + 1 < toks.length; k++) {
          var a = toks[k], b = toks[k + 1];
          var cand = b.charAt(0) === '-' && b.charAt(1) !== '-' ? a + b : (/^[0-9a-z]/.test(b) ? a + '-' + b : null);
          var tail = cand ? (/=/.test(a) ? cand.slice(cand.indexOf('=') + 1) : cand.split('/').pop()) : '';
          if (cand && (a.charAt(0) !== '-' || /=/.test(a)) && tail.length > 1 && inVocab(words, tail) && !(words.indexOf(a) >= 0 && words.indexOf(b) >= 0 && b.charAt(0) !== '-')) {
            toks.splice(k, 2, cand); changed = true; break;
          }
        }
      }
    }
    line = toks.join(' ');
    return line ? { line: line, verb: false } : null;
  }

  /** Tab completion over the pack's example commands + lab verbs. */
  function complete(simId, prefix) {
    var p = PACKS[simId]; if (!p) return [];
    var pool = p.examples.concat(['help', 'check', 'hint', 'solution', 'task', 'history', 'clear', 'reset']);
    var pre = String(prefix || '');
    return pool.filter(function (c) { return c.indexOf(pre) === 0 && c !== pre; });
  }

  return {
    VERSION: '1.2.0',
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
    complete: complete,
    fromSpeech: fromSpeech
  };
});
