/**
 * IL Immersive CLI v1.7.0 (2026-10-29; v1.6.0 2026-10-27; v1.5.0 2026-10-23; v1.4.0 2026-10-22; v1.3.0 2026-10-21; v1.2.0 2026-10-20; v1.1.0 2026-10-19; v1.0.0 2026-10-16) — type real kubectl / etcdctl / crictl / aws CLI syntax and the authored
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
 * v1.3.0 (2026-10-21) — two more packs (11 total): Gateway API (`gateway-api` on the same authored ingress-gateway.glb:
 * GatewayClass / Gateway / HTTPRoute / ReferenceGrant get · describe · patch, api-resources, listener conditions,
 * RefNotPermitted → HTTP 500, InvalidCertificateRef → TLS handshake failure; GatewayClass lab-gw is a lab
 * implementation, not a vendor) and ConfigMaps & Secrets (`config-propagation`: data patch vs immutable, kubelet sync
 * via a simulated `sleep`, env vs volume freshness, rollout restart, secretKeyRef missing key, etcdctl get at rest).
 *
 * v1.4.0 (2026-10-22) — worker-node troubleshooting pack (12 total) on the NEW authored node-troubleshoot.glb:
 * `ssh node-01` sessions (host-aware prompt via promptFor; kubectl on the worker has no kubeconfig → localhost:8080
 * refused), systemctl status / restart / daemon-reload / enable --now for kubelet + containerd (203/EXEC from a bad
 * ExecStart, the real "changed on disk" warning until daemon-reload), journalctl -u kubelet (labelled representative
 * lines), sed -i on the kubeadm drop-in, crictl socket failure / rmi --prune, df, /etc/cni/net.d, describe node
 * conditions + taints, kubelet eviction of BestEffort pods. Tasks: kubelet-203 · runtime-down · cni-missing ·
 * disk-pressure. Voice: "system control" → systemctl, "journal control" → journalctl.
 *
 * v1.5.0 (2026-10-23) — Service + DNS troubleshooting pack (13 total) on the NEW authored service-dns.glb: Service →
 * EndpointSlice → containerPort (describe svc TargetPort vs describe deployment Port, strategic-merge patch on
 * ports[].targetPort), a dnsutils debug pod (nslookup / dig [+short] [+search] / cat /etc/resolv.conf through the rules
 * engine's search-list + ndots:5 resolver; refused vs timed out vs NXDOMAIN), CoreDNS CrashLoopBackOff from a Corefile
 * parse error (logs by label, `get cm -o yaml > FILE`, sed -i, apply -f), namespace default-deny egress without a
 * kube-dns:53 rule, `kubectl set env` for a cross-namespace FQDN. Tasks: target-port · coredns-corefile · dns-egress ·
 * cross-ns-fqdn. Voice: "n s lookup" → nslookup, "core dns" → coredns, "config map" → configmap.
 *
 * v1.6.0 (2026-10-27) — the last two drills without a typed task get packs (15 total). CNI on the authored
 * cni-pod-network.glb: NotReady nodes + Pending CoreDNS before any CNI (describe node NetworkPluginNotReady, empty
 * /etc/cni/net.d, apply a trimmed calico.yaml stand-in), a pod CIDR that overlaps the VPC (same-node ping answers,
 * cross-node does not; Calico's documented pool migration: new IPPool, disable the old one, recreate pods), and no
 * kube-proxy (pod IPs answer, ClusterIP times out, names fail because DNS rides the kube-dns VIP; `kubeadm init phase
 * addon kube-proxy`). Service mesh mTLS on service-mesh-sidecar.glb: STRICT resets a sidecar-less client, injection
 * needs the namespace label AND new pods, X-Forwarded-Client-Cert proves the hop was mTLS, PERMISSIVE → STRICT
 * migration in a safe order, istiod at zero keeps traffic flowing but the injection webhook (failurePolicy Fail) blocks
 * new pods; `istioctl proxy-status`. Tasks: no-cni · cidr-overlap · no-kube-proxy · strict-reset ·
 * permissive-to-strict · istiod-down. Voice: "istio control" → istioctl, "peer authentication", "ip pool", "kube adm".
 *
 * v1.7.0 (2026-10-29) — the first CKS pack (16 total) on the NEW authored cks-pod-security.glb: Pod Security Admission
 * (`kubectl label --dry-run=server --overwrite ns … pod-security.kubernetes.io/enforce=restricted` with the real
 * existing-pods warning, Forbidden on a privileged pod, ReplicaSet FailedCreate listing every restricted check),
 * securityContext + seccomp proof from inside the container (`id`, `grep Seccomp /proc/1/status`), default-deny ingress
 * then allow frontend, ServiceAccount least privilege (`auth can-i --as system:serviceaccount:…`, ClusterRoleBinding
 * removal, `create role` / `create rolebinding --serviceaccount`), and the API audit log backend (`sed -i` on the
 * kube-apiserver static-pod manifest, a Metadata-level audit.k8s.io/v1 event without the secret value). Tasks:
 * psa-enforce · harden-pod · default-deny · sa-least-privilege · audit-log. Voice: "sec comp" → seccomp, "dry run" → dry-run.
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

  /* ── v1.3.0 (2026-10-21) pack: Gateway API — GatewayClass · Gateway · HTTPRoute · ReferenceGrant (CKA services & networking) ──
   * Drives the gateway-api sim on the SAME authored ingress-gateway.glb. Resource names: GatewayClass lab-gw
   * (controllerName example.net/lab-gateway-controller — a lab implementation, not a vendor), Gateway shop-gw and
   * HTTPRoute shop-route in default, service-0 in namespace shop-api (cross-namespace backendRef), service-1 in default. */
  var GW_API = 'gateway.networking.k8s.io';
  var GW_NOTE = 'Gateway API (' + GW_API + '/v1; ReferenceGrant v1beta1) is the Kubernetes successor to Ingress and a CKA Services & Networking competency. sim: GatewayClass lab-gw is a lab implementation computed by the rules engine — not Envoy Gateway, Istio, Cilium or NGINX Gateway Fabric.';
  var GW_ROUTE_YAML = ['apiVersion: ' + GW_API + '/v1', 'kind: HTTPRoute', 'metadata:', '  name: shop-route', '  namespace: default', 'spec:', '  parentRefs:', '  - name: shop-gw', '    sectionName: https',
    '  hostnames:', '  - shop.example.com', '  rules:', '  - matches:', '    - path:', '        type: PathPrefix', '        value: /api', '    backendRefs:', '    - name: service-0', '      namespace: shop-api', '      port: 80',
    '  - matches:', '    - path:', '        type: PathPrefix', '        value: /web', '    backendRefs:', '    - name: service-1', '      port: 80'];
  function gwKind(k) {
    k = String(k || '').toLowerCase().replace(/\.gateway\.networking\.k8s\.io$/, '');
    if (/^(gc|gatewayclass(es)?)$/.test(k)) return 'gatewayclass';
    if (/^(gtw|gateways?)$/.test(k)) return 'gateway';
    if (/^httproutes?$/.test(k)) return 'httproute';
    if (/^(refgrant|referencegrants?)$/.test(k)) return 'referencegrant';
    return null;
  }
  function S_gatewayDecide(s) { var S = Sims(); return S && S.gatewayDecide ? S.gatewayDecide(s) : null; }
  var gatewayPack = {
    sim: 'gateway-api',
    prompt: 'student@controlplane:~$',
    note: GW_NOTE,
    files: {
      'gateway-controller.yaml': { yaml: ['# Lab stand-in for installing a Gateway API implementation that watches GatewayClass lab-gw', '# (controllerName: example.net/lab-gateway-controller). Real clusters install one first: CRDs + controller + data plane.', '# sim: applying this file flips the class to Accepted in the rules engine. ' + GW_NOTE] },
      'shop-route.yaml': { yaml: GW_ROUTE_YAML },
      'shop-api-refgrant.yaml': { yaml: ['apiVersion: ' + GW_API + '/v1beta1', 'kind: ReferenceGrant', 'metadata:', '  name: allow-default-routes', '  namespace: shop-api   # lives in the namespace that owns the TARGET', 'spec:', '  from:', '  - group: ' + GW_API, '    kind: HTTPRoute', '    namespace: default', '  to:', '  - group: ""', '    kind: Service'] }
    },
    examples: ['kubectl get gatewayclass', 'kubectl get gateway', 'kubectl describe gateway shop-gw', 'kubectl get httproute', 'kubectl describe httproute shop-route',
      'kubectl get httproute shop-route -o yaml', 'kubectl get referencegrant -n shop-api', 'curl -sI https://shop.example.com/api/v1/orders',
      'kubectl api-resources --api-group=gateway.networking.k8s.io', 'cat shop-api-refgrant.yaml', 'kubectl apply -f gateway-controller.yaml',
      'kubectl patch httproute shop-route --type=json -p \'[{"op":"replace","path":"/spec/rules/0/matches/0/path/type","value":"PathPrefix"}]\'',
      'kubectl patch httproute shop-route --type=json -p \'[{"op":"replace","path":"/spec/hostnames/0","value":"shop.example.com"}]\'',
      'kubectl get secret shop-tls', 'kubectl create secret tls shop-tls --cert=shop.crt --key=shop.key'],
    run: function (u, s, d, ctx) {
      var t = u.t, g = d.metrics;
      var fr = fileRun(gatewayPack, t); if (fr) return fr;
      if (t[0] === 'curl') {
        var c = curlArgs(t);
        if (!c.host) return res(['curl: (3) URL rejected: No host part in the URL'], 3);
        if (c.host !== 'shop.example.com') return res(['curl: (6) Could not resolve host: ' + c.host], 6);
        if (!s.gwcAccepted) return res(['curl: (7) Failed to connect to shop.example.com port ' + (c.scheme === 'https' ? 443 : 80) + ' after 2 ms: Couldn\'t connect to server', '# sim: shop-gw has no ADDRESS yet — nothing has programmed a data plane for it'], 7, null, ['curl', 'curl-noconnect']);
        if (c.scheme === 'http') return res(['curl: (7) Failed to connect to shop.example.com port 80 after 1 ms: Couldn\'t connect to server', '# sim: shop-gw has a single HTTPS listener (port 443)'], 7, null, ['curl', 'curl-http-nolistener']);
        if (!s.certRef) return res(['curl: (35) OpenSSL/3.0.13: error:0A000410:SSL routines::ssl/tls alert handshake failure', '# sim: listener https is not programmed (certificateRefs unresolved) — -k does not help; there is no fallback certificate'], 35, null, ['curl', 'curl-tls-fail']);
        var r = s.routeAttached ? S_ingressMatch(c.path, [{ path: '/api', type: s.routeExact ? 'Exact' : 'Prefix', svc: 0 }, { path: '/web', type: 'Prefix', svc: 1 }]) : null;
        var code = !r ? 404 : (r.svc === 0 && !s.refGrant ? 500 : 200);
        var ev = ['curl', 'curl-' + code];
        if (code === 200) ev.push(c.insecure ? 'curl-200-insecure' : 'curl-200-verified');
        var why = !s.routeAttached ? 'no HTTPRoute is attached for this host (NoMatchingListenerHostname)' : (!r ? 'no rule matched → 404' : (code === 500 ? 'backendRef ' + 'shop-api/service-0 not permitted (RefNotPermitted) → 500' : 'rule ' + r.path + ' → service-' + r.svc));
        var body = code === 200 ? '{"service":"service-' + r.svc + '","path":"' + c.path + '"}' : (code === 404 ? 'fault filter abort' : 'no healthy upstream');
        var out;
        if (c.w && /http_code/.test(c.w)) out = [String(code)];
        else if (c.head || c.include) {
          out = ['HTTP/2 ' + code, 'content-type: ' + (code === 200 ? 'application/json' : 'text/plain'), 'x-sim-note: computed by the rules engine (' + why + ')'];
          if (c.include && !c.head) out.push('', body);
        } else out = [body];
        return res(out, c.fail && code >= 400 ? 22 : 0, null, ev);
      }
      if (t[0] !== 'kubectl') return null;
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED), ns = nsOf(t), out2 = flag(t, ['-o', '--output']);
      var rawKind = args[0] || '', name = args[1] || '';
      if (/\//.test(rawKind)) { name = rawKind.split('/')[1]; rawKind = rawKind.split('/')[0]; }
      var kind = gwKind(rawKind);
      if (verb === 'api-resources') {
        var grp = flag(t, '--api-group');
        if (grp && grp !== GW_API) return res(['sim: this drill models `kubectl api-resources --api-group=' + GW_API + '`'], 2);
        return res(table([['NAME', 'SHORTNAMES', 'APIVERSION', 'NAMESPACED', 'KIND'], ['gatewayclasses', 'gc', GW_API + '/v1', 'false', 'GatewayClass'], ['gateways', 'gtw', GW_API + '/v1', 'true', 'Gateway'],
          ['grpcroutes', '', GW_API + '/v1', 'true', 'GRPCRoute'], ['httproutes', '', GW_API + '/v1', 'true', 'HTTPRoute'], ['referencegrants', 'refgrant', GW_API + '/v1beta1', 'true', 'ReferenceGrant']]), 0, null, ['api-resources']);
      }
      if (kind === 'gatewayclass' && (verb === 'get' || verb === 'describe')) {
        if (name && name !== 'lab-gw') return notFound('gatewayclasses.' + GW_API, name);
        var acc = s.gwcAccepted ? 'True' : 'Unknown';
        if (verb === 'get') return res(table([['NAME', 'CONTROLLER', 'ACCEPTED', 'AGE'], ['lab-gw', 'example.net/lab-gateway-controller', acc, '12d']]), 0, null, ['get-gc', s.gwcAccepted ? 'get-gc-accepted' : 'get-gc-unknown']);
        return res(['Name:         lab-gw', 'API Version:  ' + GW_API + '/v1', 'Kind:         GatewayClass', 'Spec:', '  Controller Name:  example.net/lab-gateway-controller', 'Status:', '  Conditions:',
          '    Type:     Accepted', '    Status:   ' + acc, '    Reason:   ' + (s.gwcAccepted ? 'Accepted' : 'Pending'), '    Message:  ' + (s.gwcAccepted ? 'Handled by example.net/lab-gateway-controller' : 'Waiting for controller')], 0, null, ['describe-gc', s.gwcAccepted ? 'get-gc-accepted' : 'get-gc-unknown']);
      }
      if (kind && verb === 'get' && ns !== 'default' && ns !== '*' && !(kind === 'referencegrant' && ns === 'shop-api')) {
        return res(['No resources found in ' + ns + ' namespace.'], 0, null, kind === 'referencegrant' ? ['get-refgrant-wrongns'] : []);
      }
      if (kind === 'gateway' && verb === 'get') {
        if (name && name !== 'shop-gw') return notFound('gateways.' + GW_API, name);
        if (out2 && /yaml/.test(out2)) {
          return res(['apiVersion: ' + GW_API + '/v1', 'kind: Gateway', 'metadata:', '  name: shop-gw', '  namespace: default', 'spec:', '  gatewayClassName: lab-gw', '  listeners:', '  - name: https', '    protocol: HTTPS', '    port: 443', '    hostname: shop.example.com',
            '    tls:', '      mode: Terminate', '      certificateRefs:', '      - name: shop-tls', '    allowedRoutes:', '      namespaces:', '        from: Same', 'status:', '  # read conditions with: kubectl describe gateway shop-gw'], 0, null, ['gw-yaml']);
        }
        var row = ['shop-gw', 'lab-gw', g.address || '', g.gatewayProgrammed, '12d'];
        return res(table([(ns === '*' ? ['NAMESPACE'] : []).concat(['NAME', 'CLASS', 'ADDRESS', 'PROGRAMMED', 'AGE']), (ns === '*' ? ['default'] : []).concat(row)]), 0, null,
          ['get-gw', g.gatewayProgrammed === 'Unknown' ? 'get-gw-pending' : (g.gatewayProgrammed === 'True' ? 'get-gw-programmed' : 'get-gw-notprogrammed')]);
      }
      if (kind === 'gateway' && verb === 'describe') {
        if (name !== 'shop-gw') return notFound('gateways.' + GW_API, name || '');
        var pend = !s.gwcAccepted;
        var L = ['Name:         shop-gw', 'Namespace:    default', 'API Version:  ' + GW_API + '/v1', 'Kind:         Gateway', 'Spec:', '  Gateway Class Name:  lab-gw', '  Listeners:', '    Name:      https', '    Hostname:  shop.example.com', '    Port:      443', '    Protocol:  HTTPS',
          '    Tls:', '      Mode:  Terminate', '      Certificate Refs:', '        Kind:  Secret', '        Name:  shop-tls', 'Status:', '  Addresses:' + (g.address ? '' : '  <none>')];
        if (g.address) L.push('    Type:   IPAddress', '    Value:  ' + g.address);
        L.push('  Conditions:', '    Type:    Accepted', '    Status:  ' + (pend ? 'Unknown' : 'True'), '    Reason:  ' + (pend ? 'Pending' : 'Accepted'),
          '    Type:    Programmed', '    Status:  ' + g.gatewayProgrammed, '    Reason:  ' + (pend ? 'Pending' : (s.certRef ? 'Programmed' : 'Invalid')));
        if (pend) L.push('  Listeners:  <none — no controller has reconciled this Gateway>');
        else {
          L.push('  Listeners:', '    Name:             https', '    Attached Routes:  ' + (s.routeAttached ? 1 : 0), '    Conditions:',
            '      Type:     ResolvedRefs', '      Status:   ' + (s.certRef ? 'True' : 'False'), '      Reason:   ' + (s.certRef ? 'ResolvedRefs' : 'InvalidCertificateRef'));
          if (!s.certRef) L.push('      Message:  Secret default/shop-tls does not exist');
          L.push('      Type:     Programmed', '      Status:   ' + (s.certRef ? 'True' : 'False'), '      Reason:   ' + (s.certRef ? 'Programmed' : 'Invalid'));
        }
        L.push('Events:       <none>');
        return res(L, 0, null, ['describe-gw', pend ? 'describe-gw-pending' : (s.certRef ? 'describe-gw-ok' : 'describe-gw-certref')]);
      }
      if (kind === 'httproute' && verb === 'get') {
        if (name && name !== 'shop-route') return notFound('httproutes.' + GW_API, name);
        var host = s.routeAttached ? 'shop.example.com' : 'shop.example.org';
        if (out2 && /yaml|jsonpath/.test(out2)) {
          var mt = s.routeExact ? 'Exact' : 'PathPrefix';
          if (/jsonpath/.test(out2)) {
            if (/hostnames/.test(out2)) return res([host], 0, null, ['route-hostnames']);
            if (!/path\.type/.test(out2)) return res(['sim: this drill models jsonpath on .spec.hostnames and .spec.rules[*].matches[*].path.type'], 2);
            return res([/\[\*\]/.test(out2) ? mt + ' PathPrefix' : mt], 0, null, ['route-yaml', 'route-match-' + mt.toLowerCase()]);
          }
          var y = GW_ROUTE_YAML.slice();
          y[10] = '  - ' + host;
          y[14] = '        type: ' + mt;
          y = y.concat(['status:', '  parents:', '  - parentRef: { name: shop-gw, sectionName: https }', '    controllerName: example.net/lab-gateway-controller', '    # conditions: kubectl describe httproute shop-route']);
          return res(y, 0, null, ['route-yaml', 'route-match-' + mt.toLowerCase(), s.routeAttached ? 'route-hostnames' : 'route-hostnames-mismatch']);
        }
        return res(table([(ns === '*' ? ['NAMESPACE'] : []).concat(['NAME', 'HOSTNAMES', 'AGE']), (ns === '*' ? ['default'] : []).concat(['shop-route', '["' + host + '"]', '12d'])]), 0, null, ['get-route']);
      }
      if (kind === 'httproute' && verb === 'describe') {
        if (name !== 'shop-route') return notFound('httproutes.' + GW_API, name || '');
        var R = ['Name:         shop-route', 'Namespace:    default', 'API Version:  ' + GW_API + '/v1', 'Kind:         HTTPRoute', 'Spec:', '  Hostnames:', '    ' + (s.routeAttached ? 'shop.example.com' : 'shop.example.org'),
          '  Parent Refs:', '    Name:          shop-gw', '    Section Name:  https', '  Rules:', '    Matches:  Path ' + (s.routeExact ? 'Exact' : 'PathPrefix') + ' /api   Backend Refs:  shop-api/service-0:80',
          '    Matches:  Path PathPrefix /web   Backend Refs:  service-1:80', 'Status:', '  Parents:'];
        var evs = ['describe-route'];
        if (!s.gwcAccepted) { R.push('    <none — no controller has processed this route yet>'); evs.push('describe-route-pending'); }
        else {
          R.push('    Controller Name:  example.net/lab-gateway-controller', '    Parent Ref:       shop-gw (sectionName https)', '    Conditions:',
            '      Type:     Accepted', '      Status:   ' + (s.routeAttached ? 'True' : 'False'), '      Reason:   ' + (s.routeAttached ? 'Accepted' : 'NoMatchingListenerHostname'));
          if (!s.routeAttached) R.push('      Message:  no listener hostname intersects the route hostnames (listener https: shop.example.com)');
          R.push('      Type:     ResolvedRefs', '      Status:   ' + (s.refGrant ? 'True' : 'False'), '      Reason:   ' + (s.refGrant ? 'ResolvedRefs' : 'RefNotPermitted'));
          if (!s.refGrant) R.push('      Message:  backendRef shop-api/service-0 is in another namespace and no ReferenceGrant allows it');
          if (!s.routeAttached) evs.push('describe-route-hostname');
          if (!s.refGrant) evs.push('describe-route-refnotpermitted');
          if (s.routeAttached && s.refGrant) evs.push('describe-route-ok');
        }
        R.push('Events:       <none>');
        return res(R, 0, null, evs);
      }
      if (kind === 'referencegrant' && verb === 'get') {
        if (ns !== 'shop-api' && ns !== '*') return res(['No resources found in ' + ns + ' namespace.', '# sim: a ReferenceGrant lives in the namespace that owns the target'], 0, null, ['get-refgrant-wrongns']);
        if (!s.refGrant) return res(['No resources found in ' + (ns === '*' ? 'any' : 'shop-api') + ' namespace.'], 0, null, ['get-refgrant', 'get-refgrant-none']);
        return res(table([(ns === '*' ? ['NAMESPACE'] : []).concat(['NAME', 'AGE']), (ns === '*' ? ['shop-api'] : []).concat(['allow-default-routes', '3m'])]), 0, null, ['get-refgrant', 'get-refgrant-ok']);
      }
      if (kind === 'referencegrant' && verb === 'delete') {
        if (ns !== 'shop-api' || name !== 'allow-default-routes' || !s.refGrant) return notFound('referencegrants.' + GW_API, name);
        return res(['referencegrant.' + GW_API + ' "allow-default-routes" deleted'], 0, { refGrant: false }, ['delete-refgrant']);
      }
      if (kind === 'httproute' && verb === 'patch') {
        if (name !== 'shop-route') return notFound('httproutes.' + GW_API, name);
        var jj = jsonArg(t); if (jj.err) return jj.err;
        var type = flag(t, '--type');
        if (type === 'merge' && jj.v && jj.v.spec && Array.isArray(jj.v.spec.hostnames)) {
          var okm = jj.v.spec.hostnames.indexOf('shop.example.com') >= 0;
          return res(['httproute.' + GW_API + '/shop-route patched'], 0, { routeAttached: okm }, ['patch-route', okm ? 'route-hostname-fixed' : 'route-hostname-broken']);
        }
        var ops = Array.isArray(jj.v) ? jj.v : null;
        if (type !== 'json' || !ops) return res(['sim: this drill models JSON patches on /spec/hostnames/0 and /spec/rules/0/matches/0/path/type (or --type=merge on spec.hostnames)'], 2);
        var set = {}, evp = ['patch-route'];
        ops.forEach(function (o) {
          if (o.op !== 'replace' && o.op !== 'add') return;
          if (o.path === '/spec/hostnames/0' || o.path === '/spec/hostnames') { var hv = Array.isArray(o.value) ? o.value : [o.value]; set.routeAttached = hv.indexOf('shop.example.com') >= 0; evp.push(set.routeAttached ? 'route-hostname-fixed' : 'route-hostname-broken'); }
          if (o.path === '/spec/rules/0/matches/0/path/type' && (o.value === 'Exact' || o.value === 'PathPrefix')) { set.routeExact = o.value === 'Exact'; evp.push('route-match-set-' + o.value.toLowerCase()); }
        });
        if (evp.length === 1) {
          if (ops.some(function (o) { return o.path === '/spec/rules/0/matches/0/path/type'; })) return res(['The HTTPRoute "shop-route" is invalid: spec.rules[0].matches[0].path.type: Unsupported value: ' + JSON.stringify(ops[0].value) + ': supported values: "Exact", "PathPrefix", "RegularExpression"'], 1);
          return res(['sim: this drill models JSON patches on /spec/hostnames/0 and /spec/rules/0/matches/0/path/type'], 2);
        }
        return res(['httproute.' + GW_API + '/shop-route patched'], 0, set, evp);
      }
      if ((verb === 'apply' || verb === 'delete' || verb === 'create') && hasFlag(t, ['-f', '--filename'])) {
        var a = applyFile(gatewayPack, t); if (a.err) return a.err;
        if (a.name === 'gateway-controller.yaml') {
          if (verb === 'delete') return s.gwcAccepted ? res(['(sim) lab gateway controller removed — lab-gw goes back to Pending'], 0, { gwcAccepted: false }, ['controller-removed']) : res(['Error from server (NotFound): deployments.apps "lab-gateway-controller" not found'], 1);
          return res(s.gwcAccepted ? ['deployment.apps/lab-gateway-controller unchanged'] : ['namespace/lab-gateway-system created', 'deployment.apps/lab-gateway-controller created', '(sim) lab-gw Accepted · shop-gw Programmed at 203.0.113.20'], 0, s.gwcAccepted ? null : { gwcAccepted: true }, ['controller-installed']);
        }
        if (a.name === 'shop-api-refgrant.yaml') {
          if (verb === 'delete') return s.refGrant ? res(['referencegrant.' + GW_API + ' "allow-default-routes" deleted'], 0, { refGrant: false }, ['delete-refgrant']) : notFound('referencegrants.' + GW_API, 'allow-default-routes');
          return res(['referencegrant.' + GW_API + '/allow-default-routes ' + (s.refGrant ? 'unchanged' : 'created')], 0, { refGrant: true }, ['apply-refgrant']);
        }
        if (verb === 'delete') return res(['sim: deleting shop-route is not modelled in this drill'], 2);
        var same = s.routeAttached && !s.routeExact;
        return res(['httproute.' + GW_API + '/shop-route ' + (same ? 'unchanged' : 'configured')], 0, { routeAttached: true, routeExact: false }, ['apply-route']);
      }
      if (verb === 'get' && /^secrets?$/.test(rawKind)) {
        if (name && name !== 'shop-tls') return notFound('secrets', name);
        if (!s.certRef) return name ? res(['Error from server (NotFound): secrets "shop-tls" not found'], 1, null, ['get-secret-missing']) : res(['No resources found in default namespace.'], 0, null, ['get-secret-missing']);
        return res(table([['NAME', 'TYPE', 'DATA', 'AGE'], ['shop-tls', 'kubernetes.io/tls', '2', '5d']]), 0, null, ['get-secret', 'get-secret-ok']);
      }
      if (verb === 'create' && args[0] === 'secret' && args[1] === 'tls') {
        if (args[2] !== 'shop-tls' || !flag(t, '--cert') || !flag(t, '--key')) return res(['sim: this drill models `kubectl create secret tls shop-tls --cert=shop.crt --key=shop.key`'], 2);
        if (s.certRef) return res(['error: failed to create secret secrets "shop-tls" already exists'], 1);
        return res(['secret/shop-tls created'], 0, { certRef: true }, ['create-secret-tls']);
      }
      if (verb === 'delete' && /^secrets?$/.test(rawKind)) {
        if (name !== 'shop-tls' || !s.certRef) return notFound('secrets', name);
        return res(['secret "shop-tls" deleted'], 0, { certRef: false }, ['delete-secret-tls']);
      }
      if (verb === 'get' && /^(ing|ingress(es)?)$/.test(rawKind)) return res(['No resources found in default namespace.', '# sim: this drill routes with Gateway API (Gateway + HTTPRoute), not an Ingress — see the Ingress drill for the Ingress API'], 0);
      if (verb === 'edit') return res(['sim: interactive editors are not modelled — use kubectl patch (see `help`)'], 2);
      return unmodelled(t.join(' '), gatewayPack.examples);
    },
    tasks: [
      { id: 'gw-pending', title: 'Gateway with no ADDRESS',
        goal: 'shop.example.com does not answer. Follow Gateway → GatewayClass to the missing controller, install it, and get a 200.',
        setup: { gwcAccepted: false, routeAttached: true, routeExact: false, refGrant: true, certRef: true },
        steps: [
          { label: 'Reproduce: nothing answers on shop.example.com', event: 'curl-noconnect', hint: 'curl -sI https://shop.example.com/api/v1/orders' },
          { label: 'See shop-gw with no ADDRESS and PROGRAMMED Unknown', event: 'get-gw-pending', hint: 'kubectl get gateway' },
          { label: 'Find that GatewayClass lab-gw was never Accepted', event: 'get-gc-unknown', hint: 'kubectl get gatewayclass' },
          { label: 'Install the implementation for lab-gw (lab file stands in for the install)', state: function (s) { return !!s.gwcAccepted; }, hint: 'kubectl apply -f gateway-controller.yaml' },
          { label: 'GET /api/v1/orders answers 200', event: 'curl-200', hint: 'curl -sI https://shop.example.com/api/v1/orders' }
        ] },
      { id: 'gw-hostname', title: '404: the route never attached',
        goal: 'The Gateway is Programmed, yet every path 404s. Read the HTTPRoute’s parent status and fix its hostname.',
        setup: { gwcAccepted: true, routeAttached: false, routeExact: false, refGrant: true, certRef: true },
        steps: [
          { label: 'Reproduce the 404', event: 'curl-404', hint: 'curl -sI https://shop.example.com/api/v1/orders' },
          { label: 'Read the parent status: Accepted False, NoMatchingListenerHostname', event: 'describe-route-hostname', hint: 'kubectl describe httproute shop-route' },
          { label: 'Make the route hostname match the listener (shop.example.com)', state: function (s) { return !!s.routeAttached; }, hint: 'kubectl patch httproute shop-route --type=json -p \'[{"op":"replace","path":"/spec/hostnames/0","value":"shop.example.com"}]\'' },
          { label: 'GET /api/v1/orders answers 200', event: 'curl-200', hint: 'curl -sI https://shop.example.com/api/v1/orders' }
        ] },
      { id: 'gw-refgrant', title: '500: cross-namespace backendRef not permitted',
        goal: '/api answers 500 while /web works. Find the ResolvedRefs reason, find what is missing in shop-api, and grant it.',
        setup: { gwcAccepted: true, routeAttached: true, routeExact: false, refGrant: false, certRef: true },
        steps: [
          { label: 'Reproduce the 500', event: 'curl-500', hint: 'curl -sI https://shop.example.com/api/v1/orders' },
          { label: 'Read ResolvedRefs False, RefNotPermitted', event: 'describe-route-refnotpermitted', hint: 'kubectl describe httproute shop-route' },
          { label: 'Find that ns shop-api has no ReferenceGrant', event: 'get-refgrant-none', hint: 'kubectl get referencegrant -n shop-api' },
          { label: 'Grant HTTPRoutes in default access to Services in shop-api', state: function (s) { return !!s.refGrant; }, hint: 'kubectl apply -f shop-api-refgrant.yaml' },
          { label: 'GET /api/v1/orders answers 200', event: 'curl-200', hint: 'curl -sI https://shop.example.com/api/v1/orders' }
        ] },
      { id: 'gw-cert', title: 'TLS handshake fails: listener certificateRefs',
        goal: 'HTTPS to shop.example.com fails before any HTTP. Read the listener conditions, find the missing Secret, create it, verify without -k.',
        setup: { gwcAccepted: true, routeAttached: true, routeExact: false, refGrant: true, certRef: false },
        steps: [
          { label: 'See the TLS handshake fail', event: 'curl-tls-fail', hint: 'curl -sI https://shop.example.com/api' },
          { label: 'Read listener https: ResolvedRefs False, InvalidCertificateRef', event: 'describe-gw-certref', hint: 'kubectl describe gateway shop-gw' },
          { label: 'Find that Secret shop-tls does not exist', event: 'get-secret-missing', hint: 'kubectl get secret shop-tls' },
          { label: 'Create the kubernetes.io/tls Secret', state: function (s) { return !!s.certRef; }, hint: 'kubectl create secret tls shop-tls --cert=shop.crt --key=shop.key' },
          { label: 'HTTPS verifies (no -k) and answers 200', event: 'curl-200-verified', hint: 'curl -sI https://shop.example.com/api' }
        ] }
    ]
  };

  /* ── v1.3.0 (2026-10-21) pack: ConfigMaps & Secrets — propagation · immutable · missing key (CKA workloads & scheduling) ──
   * Drives config-propagation on secrets-configmaps.glb. Deployment api (pod api-7c9d8-x2k4q) mounts ConfigMap app-config
   * as a volume at /etc/config AND reads LOG_LEVEL via configMapKeyRef; DB_PASS comes from secretKeyRef db-creds/password.
   * `sleep N` (N ≥ 60) stands in for waiting out the kubelet sync period — the sim skips time, it does not wait. */
  var CFG_POD = ['api-7c9d8-x2k4q', 'api-5f6b7-q8w2n'];
  function cfgPodName(s) { return s.restarted ? CFG_POD[1] : CFG_POD[0]; }
  function cfgVal(on) { return on ? 'debug' : 'info'; }
  var configPack = {
    sim: 'config-propagation',
    prompt: 'student@controlplane:~$',
    examples: ['kubectl get configmap', 'kubectl get configmap app-config -o yaml', 'kubectl exec deploy/api -- cat /etc/config/LOG_LEVEL', 'kubectl exec deploy/api -- printenv LOG_LEVEL',
      'kubectl patch configmap app-config -p \'{"data":{"LOG_LEVEL":"debug"}}\'', 'sleep 90', 'kubectl rollout restart deployment/api', 'kubectl rollout status deployment/api',
      'kubectl get pods', 'kubectl describe pods -l app=api', 'kubectl get secret db-creds', 'kubectl describe secret db-creds',
      'kubectl patch secret db-creds -p \'{"stringData":{"password":"s3cr3t-lab"}}\'', 'ETCDCTL_API=3 etcdctl get /registry/secrets/default/db-creds'],
    run: function (u, s, d, ctx) {
      var t = u.t, m = d.metrics;
      if (t[0] === 'sleep') {
        var n = parseInt(t[1], 10);
        if (!(n >= 0)) return res(['sleep: missing operand'], 1);
        if (n < 60) return res(['# sim: ' + n + ' s passed — the kubelet has probably not re-synced projected volumes yet (sync period + cache TTL, often 60–90 s)'], 0, null, ['sleep', 'sleep-short']);
        return res(['# sim: skipped ' + n + ' s — kubelet sync period + ConfigMap cache TTL elapsed (time is simulated, nothing waited)'], 0, { synced: true }, ['sleep', 'sleep-synced']);
      }
      if (t[0] === 'etcdctl') {
        var keyArg = positional(t.slice(1), ['--endpoints', '-w', '--write-out', '--cacert', '--cert', '--key']);
        if (keyArg[0] !== 'get' || !/^\/registry\/secrets\/default\/db-creds$/.test(keyArg[1] || '')) return res(['sim: this drill models `etcdctl get /registry/secrets/default/db-creds`'], 2);
        if (s.encryptAtRest) return res(['/registry/secrets/default/db-creds', 'k8s:enc:aescbc:v1:key1:\u00b7\u00b7\u00b7(ciphertext)\u00b7\u00b7\u00b7'], 0, null, ['etcd-get', 'etcd-encrypted']);
        return res(['/registry/secrets/default/db-creds', 'k8s\u0000\n\u0010\n\u0002v1\u0012\u0006Secret\u0012\u2026 db-creds \u2026 username\u0012\u0005admin' + (s.keyMissing ? '' : ' \u2026 password\u0012\ns3cr3t-lab') + ' \u2026 Opaque',
          '# sim: no EncryptionConfiguration — Secret data sits in etcd unencrypted (base64 in the API is encoding, not encryption)'], 0, null, ['etcd-get', 'etcd-plaintext']);
      }
      if (t[0] !== 'kubectl') return null;
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED.concat(['--from-literal'])), out2 = flag(t, ['-o', '--output']);
      var rawKind = (args[0] || '').toLowerCase(), name = args[1] || '';
      if (/\//.test(rawKind)) { name = rawKind.split('/')[1]; rawKind = rawKind.split('/')[0]; }
      var isCm = /^(cm|configmaps?)$/.test(rawKind), isSecret = /^secrets?$/.test(rawKind);
      var deleted = !!ctx.vars.cmDeleted;
      if (isCm && verb === 'get') {
        if (name && name !== 'app-config') return notFound('configmaps', name);
        if (deleted) return name ? notFound('configmaps', 'app-config') : res(table([['NAME', 'DATA', 'AGE'], ['kube-root-ca.crt', '1', '41d']]), 0, null, ['get-cm-list']);
        if (out2 && /yaml/.test(out2)) {
          var y = ['apiVersion: v1', 'data:', '  LOG_LEVEL: ' + cfgVal(m.editApplied)];
          if (s.immutable) y.push('immutable: true');
          y = y.concat(['kind: ConfigMap', 'metadata:', '  name: app-config', '  namespace: default']);
          return res(y, 0, null, ['get-cm', s.immutable ? 'get-cm-immutable' : 'get-cm-mutable']);
        }
        if (out2 && /jsonpath/.test(out2)) return res([/immutable/.test(out2) ? String(!!s.immutable) : cfgVal(m.editApplied)], 0, null, ['get-cm', s.immutable ? 'get-cm-immutable' : 'get-cm-mutable']);
        return res(table([['NAME', 'DATA', 'AGE'], ['app-config', '1', '4d'], ['kube-root-ca.crt', '1', '41d']].filter(function (r) { return !name || r[0] === 'NAME' || r[0] === name; })), 0, null, ['get-cm-list']);
      }
      if (isCm && verb === 'patch') {
        if (name !== 'app-config') return notFound('configmaps', name);
        if (deleted) return notFound('configmaps', 'app-config');
        var j = jsonArg(t); if (j.err) return j.err;
        var lv = j.v && j.v.data && j.v.data.LOG_LEVEL;
        if (lv !== 'debug' && lv !== 'info') return res(['sim: this drill models data.LOG_LEVEL = "debug" | "info" on app-config'], 2);
        if (s.immutable) return res(['The ConfigMap "app-config" is invalid: data: Forbidden: field is immutable when `immutable` is set'], 1, { cmEdited: true }, ['cm-patch-rejected']);
        return res(['configmap/app-config patched'], 0, { cmEdited: lv === 'debug', synced: false, restarted: false }, ['cm-patched']);
      }
      if (isCm && verb === 'delete') {
        if (name !== 'app-config' || deleted) return notFound('configmaps', name);
        ctx.vars.cmDeleted = true;
        return res(['configmap "app-config" deleted', '# sim: running pods keep the last projected copy; new pods would fail to start until it exists again'], 0, null, ['cm-deleted']);
      }
      if (verb === 'create' && (rawKind === 'configmap' || rawKind === 'cm')) {
        if (name !== 'app-config') return res(['sim: this drill models `kubectl create configmap app-config --from-literal=LOG_LEVEL=debug`'], 2);
        if (!deleted) return res(['error: failed to create configmap: configmaps "app-config" already exists'], 1);
        var lit = /^LOG_LEVEL=(debug|info)$/.exec(String(flag(t, '--from-literal') || ''));
        if (!lit) return res(['sim: this drill models --from-literal=LOG_LEVEL=debug'], 2);
        ctx.vars.cmDeleted = false;
        return res(['configmap/app-config created'], 0, { immutable: false, cmEdited: lit[1] === 'debug', synced: false, restarted: false }, ['cm-created']);
      }
      if (verb === 'edit') return res(['sim: interactive editors are not modelled — use kubectl patch (see `help`)'], 2);
      if (verb === 'rollout') {
        var target = (args[1] || '').replace(/^(deploy|deployments?)(\.apps)?\//, ''), sub = args[0];
        if (/^(deploy|deployments?)(\.apps)?$/.test(args[1] || '')) target = args[2] || '';
        if (target !== 'api') return res(['sim: this drill models `kubectl rollout restart|status deployment/api`'], 2);
        if (sub === 'restart') return res(['deployment.apps/api restarted'], 0, { restarted: true }, ['rollout-restart']);
        if (sub === 'status') return s.keyMissing ? res(['Waiting for deployment "api" rollout to finish: 0 of 1 updated replicas are available...', '# sim: the new pod cannot start (CreateContainerConfigError)'], 1, null, ['rollout-status', 'rollout-stuck'])
          : res(['deployment "api" successfully rolled out'], 0, null, ['rollout-status', 'rollout-ok']);
        return res(['sim: this drill models `kubectl rollout restart|status deployment/api`'], 2);
      }
      if (verb === 'get' && /^(pods?|po)$/.test(rawKind)) {
        var st = s.keyMissing ? ['0/1', 'CreateContainerConfigError'] : ['1/1', 'Running'];
        return res(table([['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE'], [cfgPodName(s), st[0], st[1], '0', s.restarted ? '20s' : '2m']]), 0, null, ['get-pods', s.keyMissing ? 'get-pods-configerror' : 'get-pods-running']);
      }
      if (verb === 'describe' && /^(pods?|po)$/.test(rawKind)) {
        var sel = flag(t, ['-l', '--selector']);
        if (!(sel === 'app=api' || (name && name.indexOf('api') === 0))) return notFound('pods', name || String(sel || ''));
        var L = ['Name:         ' + cfgPodName(s), 'Namespace:    default', 'Labels:       app=api', 'Status:       ' + (s.keyMissing ? 'Pending' : 'Running'), 'Containers:', '  api:',
          '    State:      ' + (s.keyMissing ? 'Waiting' : 'Running'), s.keyMissing ? '      Reason:   CreateContainerConfigError' : '      Started:  ' + (s.restarted ? '20s ago' : '2m ago'),
          '    Environment:', '      LOG_LEVEL:  <set to the key \'LOG_LEVEL\' of config map \'app-config\'>', '      DB_PASS:    <set to the key \'password\' in secret \'db-creds\'>',
          '    Mounts:', '      /etc/config from config (ro)', 'Volumes:', '  config:', '    Type:  ConfigMap (a volume populated by a ConfigMap)', '    Name:  app-config', 'Events:'];
        if (s.keyMissing) L.push('  Warning  Failed  12s (x6 over 1m)  kubelet  Error: couldn\'t find key password in Secret default/db-creds');
        else L.push('  Normal   Started  ' + (s.restarted ? '20s' : '2m') + '  kubelet  Started container api');
        return res(L, 0, null, ['describe-pod', s.keyMissing ? 'describe-pod-missingkey' : 'describe-pod-ok']);
      }
      if (isSecret && (verb === 'get' || verb === 'describe')) {
        if (name && name !== 'db-creds') return notFound('secrets', name);
        if (verb === 'get') return res(table([['NAME', 'TYPE', 'DATA', 'AGE'], ['db-creds', 'Opaque', s.keyMissing ? '1' : '2', '4d']]), 0, null, ['get-secret', s.keyMissing ? 'get-secret-nokey' : 'get-secret-ok']);
        var D = ['Name:         db-creds', 'Namespace:    default', 'Type:  Opaque', '', 'Data', '====', 'username:  5 bytes'];
        if (!s.keyMissing) D.push('password:  10 bytes');
        return res(D, 0, null, ['describe-secret', s.keyMissing ? 'describe-secret-nokey' : 'describe-secret-ok']);
      }
      if (isSecret && verb === 'patch') {
        if (name !== 'db-creds') return notFound('secrets', name);
        var js = jsonArg(t); if (js.err) return js.err;
        var pw = js.v && ((js.v.stringData && js.v.stringData.password) || (js.v.data && js.v.data.password));
        if (!pw) return res(['sim: this drill models adding stringData.password (or base64 data.password) to db-creds'], 2);
        return res(['secret/db-creds patched'], 0, { keyMissing: false }, ['secret-patched']);
      }
      var ex = execArgs(t);
      if (ex) {
        if (!ex.hasDd || !ex.cmd.length) return res(['error: you must specify at least one command for the container (kubectl exec … -- CMD)'], 1);
        if (ex.ns !== 'default' || ex.target.indexOf('api') !== 0) return res(['Error from server (NotFound): deployments.apps "' + ex.target + '" not found (this lab has deployment api in default)'], 1, null, ['not-found']);
        if (s.keyMissing) return res(['error: unable to upgrade connection: container not found ("api")'], 1, null, ['exec-nocontainer']);
        var bin = ex.cmd[0];
        if (bin === 'cat' && /^\/etc\/config\/LOG_LEVEL$/.test(ex.cmd[1] || '')) {
          var fresh = m.editApplied && m.volumeFresh;
          return res([cfgVal(fresh)], 0, null, ['exec-file', m.editApplied ? (fresh ? 'file-debug' : 'file-stale') : 'file-info']);
        }
        if ((bin === 'printenv' && ex.cmd[1] === 'LOG_LEVEL') || (bin === 'sh' && /\$LOG_LEVEL/.test(ex.cmd.join(' ')))) {
          var efresh = m.editApplied && m.envFresh;
          return res([cfgVal(efresh)], 0, null, ['exec-env', m.editApplied ? (efresh ? 'env-debug' : 'env-stale') : 'env-info']);
        }
        if (bin === 'ls' && /^\/etc\/config\/?$/.test(ex.cmd[1] || '')) return res(['LOG_LEVEL'], 0, null, ['exec-ls']);
        return res(['sim: inside the api container this drill models cat /etc/config/LOG_LEVEL, ls /etc/config and printenv LOG_LEVEL'], 2);
      }
      return unmodelled(t.join(' '), configPack.examples);
    },
    tasks: [
      { id: 'volume-vs-env', title: 'Edit a ConfigMap: the file updates, the env var does not',
        goal: 'Set LOG_LEVEL=debug in app-config, watch the mounted file pick it up after the kubelet sync while the env var stays stale, then roll the pods.',
        setup: { cmEdited: false, synced: false, subPath: false, immutable: false, restarted: false, keyMissing: false },
        steps: [
          { label: 'Set LOG_LEVEL=debug in ConfigMap app-config', state: function (s, d) { return d.metrics.editApplied; }, hint: 'kubectl patch configmap app-config -p \'{"data":{"LOG_LEVEL":"debug"}}\'' },
          { label: 'Read the mounted file at once — still info', event: 'file-stale', hint: 'kubectl exec deploy/api -- cat /etc/config/LOG_LEVEL' },
          { label: 'Let the kubelet sync period pass (simulated)', state: function (s) { return !!s.synced; }, hint: 'sleep 90' },
          { label: 'The mounted file now says debug', event: 'file-debug', hint: 'kubectl exec deploy/api -- cat /etc/config/LOG_LEVEL' },
          { label: 'The env var still says info', event: 'env-stale', hint: 'kubectl exec deploy/api -- printenv LOG_LEVEL' },
          { label: 'Roll the Deployment so new pods start', state: function (s, d) { return !!s.restarted && d.metrics.editApplied; }, hint: 'kubectl rollout restart deployment/api' },
          { label: 'The new pod’s env says debug', event: 'env-debug', hint: 'kubectl exec deploy/api -- printenv LOG_LEVEL' }
        ] },
      { id: 'immutable', title: 'Immutable ConfigMap: delete, recreate, roll',
        goal: 'app-config is immutable. See the API reject the edit, confirm why, then replace it and roll the pods so they read debug.',
        setup: { cmEdited: false, synced: false, subPath: false, immutable: true, restarted: false, keyMissing: false },
        steps: [
          { label: 'Try to set LOG_LEVEL=debug and see it rejected', event: 'cm-patch-rejected', hint: 'kubectl patch configmap app-config -p \'{"data":{"LOG_LEVEL":"debug"}}\'' },
          { label: 'Confirm immutable: true on the object', event: 'get-cm-immutable', hint: 'kubectl get configmap app-config -o yaml' },
          { label: 'Delete the immutable ConfigMap', event: 'cm-deleted', hint: 'kubectl delete configmap app-config' },
          { label: 'Recreate it with LOG_LEVEL=debug', state: function (s, d) { return d.metrics.editApplied; }, hint: 'kubectl create configmap app-config --from-literal=LOG_LEVEL=debug' },
          { label: 'Roll the Deployment', state: function (s, d) { return !!s.restarted && d.metrics.editApplied; }, hint: 'kubectl rollout restart deployment/api' },
          { label: 'The new pod’s env says debug', event: 'env-debug', hint: 'kubectl exec deploy/api -- printenv LOG_LEVEL' }
        ] },
      { id: 'missing-key', title: 'CreateContainerConfigError: a Secret key is missing',
        goal: 'The api pod never starts. Read the kubelet’s reason, find the missing key in db-creds, add it, and watch the pod start.',
        setup: { cmEdited: false, synced: false, subPath: false, immutable: false, restarted: false, keyMissing: true },
        steps: [
          { label: 'See the pod stuck in CreateContainerConfigError', event: 'get-pods-configerror', hint: 'kubectl get pods' },
          { label: 'Read the kubelet event: couldn’t find key password', event: 'describe-pod-missingkey', hint: 'kubectl describe pods -l app=api' },
          { label: 'Confirm db-creds has no password key', event: 'describe-secret-nokey', hint: 'kubectl describe secret db-creds' },
          { label: 'Add the password key to db-creds', state: function (s) { return !s.keyMissing; }, hint: 'kubectl patch secret db-creds -p \'{"stringData":{"password":"s3cr3t-lab"}}\'' },
          { label: 'The pod is Running (the kubelet retried on its own)', event: 'get-pods-running', hint: 'kubectl get pods' }
        ] }
    ]
  };

  /* ── pack: worker-node troubleshooting (v1.4.0, 2026-10-22 — CKA Troubleshooting, 30%) ──────────────────
   * Drives node-troubleshoot on the NEW authored node-troubleshoot.glb. Cluster: controlplane, node-01 (the patient),
   * node-02. `ssh node-01` opens a session on the node (prompt changes; `exit` returns); `ssh node-01 CMD` runs one
   * command there. kubectl has no kubeconfig on node-01 (localhost:8080 refused), as on a kubeadm worker.
   * systemd / journald / crictl / df / sed are modelled only for the fields this drill teaches. */
  var DROPIN = '/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf';
  var DROPIN_RE = /^\/(usr\/lib|etc)\/systemd\/system\/kubelet\.service\.d\/10-kubeadm\.conf$/;
  var GOOD_KUBELET = '/usr/bin/kubelet';
  var SOCK_ERR = 'E1022 09:14:07.512301    5120 remote_runtime.go] "Status from runtime service failed" err="rpc error: code = Unavailable desc = connection error: desc = \\"transport: Error while dialing: dial unix /run/containerd/containerd.sock: connect: no such file or directory\\""';
  var RELOAD_WARN = "Warning: The unit file, source configuration file or drop-ins of kubelet.service changed on disk. Run 'systemctl daemon-reload' to reload units.";
  function nodeExecPath(s, ctx) { return s.execOnDisk ? GOOD_KUBELET : (ctx.vars.execPath || '/usr/local/bin/kubelet'); }
  function nodeHost(u, ctx) { return u.host || ctx.vars.host || 'controlplane'; }
  /** Split a sed s-command on its (unescaped) delimiter: s|a|b|g → { a, b }. */
  function sedSubst(expr) {
    if (!expr || expr.charAt(0) !== 's' || expr.length < 4) return null;
    var dl = expr.charAt(1), parts = [], cur = '';
    for (var i = 2; i < expr.length; i++) {
      var c = expr.charAt(i);
      if (c === '\\' && i + 1 < expr.length && expr.charAt(i + 1) === dl) { cur += dl; i++; continue; }
      if (c === dl) { parts.push(cur); cur = ''; continue; }
      cur += c;
    }
    parts.push(cur);
    return parts.length >= 3 ? { a: parts[0], b: parts[1] } : null;
  }
  var NODE_PODS = [['web-6f7d9-gq2xk', 'Guaranteed'], ['api-58b4c-brs4n', 'Burstable'], ['batch-7c5d8-k9w2t', 'BestEffort'], ['batch-7c5d8-p4m6z', 'BestEffort']];
  var nodePack = {
    sim: 'node-troubleshoot',
    prompt: 'student@controlplane:~$',
    examples: ['kubectl get nodes', 'kubectl describe node node-01', 'ssh node-01', 'systemctl status kubelet', 'journalctl -u kubelet -n 20 --no-pager',
      'cat ' + DROPIN, 'which kubelet', 'systemctl daemon-reload', 'systemctl restart kubelet', 'systemctl status containerd', 'crictl ps',
      'crictl rmi --prune', 'df -h /', 'ls /etc/cni/net.d', 'kubectl get pods -o wide', 'kubectl rollout restart daemonset calico-node -n kube-system', 'exit'],
    note: 'Hosts: controlplane (kubectl) · node-01 (the patient: systemd, journald, crictl, df) · node-02. `ssh node-01` opens a session, `exit` leaves it. Editing is done with sed -i (no editor in a simulated shell). Lab-only: fault kubelet|containerd stop|start · fault cni delete · fault disk fill.',
    run: function (u, s, d, ctx) {
      var t = u.t, m = d.metrics, host = nodeHost(u, ctx), onNode = host === 'node-01';
      if (u.host && !/^(node-0[12]|controlplane)$/.test(u.host)) return res(['ssh: Could not resolve hostname ' + u.host + ': Name or service not known (this lab has controlplane, node-01, node-02)'], 255);
      if (u.host && !t.length) {
        ctx.vars.host = u.host;
        return res(['(sim) logged in to ' + u.host + ' — `exit` returns to controlplane'], 0, null, ['ssh-' + u.host], { prompt: 'student@' + u.host + ':~$' });
      }
      if ((t[0] === 'exit' || t[0] === 'logout') && ctx.vars.host) {
        var was = ctx.vars.host; ctx.vars.host = null;
        return res(['logout', 'Connection to ' + was + ' closed.'], 0, null, ['ssh-exit'], { prompt: 'student@controlplane:~$' });
      }
      if (t[0] === 'exit' || t[0] === 'logout') return res(['sim: already on controlplane (the lab keeps this terminal open)'], 0);
      var f = faultArgs(t);
      if (f) {
        var fm = { 'kubelet stop': { kubeletOn: false }, 'kubelet start': { kubeletOn: true }, 'containerd stop': { runtimeUp: false }, 'containerd start': { runtimeUp: true },
          'cni delete': { cniOk: false }, 'cni restore': { cniOk: true }, 'disk fill': { diskPressure: true }, 'disk free': { diskPressure: false } }[f.join(' ')];
        if (!fm) return res(['usage: fault kubelet|containerd stop|start · fault cni delete|restore · fault disk fill|free   (lab-only fault injection)'], 2);
        return res(['[lab fault injection] ' + f.join(' ') + ' on node-01 (simulated)'], 0, fm, ['fault']);
      }
      var nodeOnly = /^(systemctl|journalctl|crictl|df|which|sed|vi|vim|nano)$/.test(t[0] || '') || (/^(cat|ls)$/.test(t[0] || '') && /^\/(etc|usr|var|run)\//.test(t[t.length - 1] || ''));
      if (nodeOnly && !onNode) {
        if (host === 'node-02') return res(['sim: node-02 is healthy and not modelled in depth — the patient is node-01'], 2);
        return res(['sim: you are on controlplane — node-01’s units, logs and files live on node-01 (ssh node-01 first, or ssh node-01 CMD)'], 2, null, ['wrong-host']);
      }
      if (t[0] === 'which' && t[1] === 'kubelet') return res([GOOD_KUBELET], 0, null, ['which-kubelet']);
      if (t[0] === 'vi' || t[0] === 'vim' || t[0] === 'nano') return res(['sim: no interactive editor in a simulated shell — edit with sed -i \'s|OLD|NEW|\' FILE (and read it back with cat)'], 2);
      if (t[0] === 'ls' && /^\/etc\/cni\/net\.d\/?$/.test(t[t.length - 1])) {
        return res(s.cniOk ? ['10-calico.conflist  calico-kubeconfig'] : [], 0, null, ['ls-cni', s.cniOk ? 'ls-cni-present' : 'ls-cni-empty']);
      }
      if (t[0] === 'ls' && /kubelet$/.test(t[t.length - 1])) {
        var lp = t[t.length - 1];
        if (lp === GOOD_KUBELET) return res(['-rwxr-xr-x 1 root root 77819992 Oct  1 12:00 /usr/bin/kubelet'], 0, null, ['ls-kubelet']);
        return res(["ls: cannot access '" + lp + "': No such file or directory"], 2, null, ['ls-kubelet-missing']);
      }
      if (t[0] === 'cat' && DROPIN_RE.test(t[1] || '')) {
        var ep = nodeExecPath(s, ctx);
        return res(['# Note: This dropin only works with kubeadm and kubelet v1.11+', '[Service]',
          'Environment="KUBELET_KUBECONFIG_ARGS=--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf"',
          'Environment="KUBELET_CONFIG_ARGS=--config=/var/lib/kubelet/config.yaml"', 'EnvironmentFile=-/var/lib/kubelet/kubeadm-flags.env', 'EnvironmentFile=-/etc/default/kubelet',
          'ExecStart=', 'ExecStart=' + ep + ' $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS'], 0, null, ['cat-dropin', ep === GOOD_KUBELET ? 'cat-dropin-ok' : 'cat-dropin-bad']);
      }
      if (t[0] === 'cat') return unmodelled(t.join(' '), nodePack.examples);
      if (t[0] === 'sed') {
        var inPlace = t.some(function (a) { return /^-[a-zA-Z]*i/.test(a) || a === '--in-place'; });
        var file = t[t.length - 1], expr = t.filter(function (a) { return a.charAt(0) === 's' && a.length > 3 && !/[a-z]/i.test(a.charAt(1)); })[0];
        if (!DROPIN_RE.test(file || '')) return res(['sim: this drill models sed on ' + DROPIN + ' only'], 2);
        var sub = sedSubst(expr);
        if (!sub) return res(["sed: -e expression #1, char 1: unknown command: `" + String(expr || '').charAt(0) + "'"], 1);
        var cur = nodeExecPath(s, ctx);
        var line = 'ExecStart=' + cur;
        var next = line.indexOf(sub.a) >= 0 ? line.replace(sub.a, sub.b) : line;
        var np = next.replace(/^ExecStart=/, '');
        if (!inPlace) return res(['(sim) without -i sed prints the edited file to stdout — nothing was written', 'ExecStart=' + np + ' …'], 0);
        if (np === cur) return res([], 0, null, ['sed-nochange']);
        ctx.vars.execPath = np === GOOD_KUBELET ? null : np;
        return res([], 0, { execOnDisk: np === GOOD_KUBELET }, ['dropin-edited', np === GOOD_KUBELET ? 'dropin-fixed' : 'dropin-still-bad']);
      }
      if (t[0] === 'systemctl') {
        var act = t[1], unit = (t.filter(function (a, i) { return i > 1 && a.charAt(0) !== '-'; })[0] || '').replace(/\.service$/, '');
        if (act === 'daemon-reload') return res([], 0, { execLoaded: !!s.execOnDisk }, ['daemon-reload']);
        if (unit !== 'kubelet' && unit !== 'containerd') return unmodelled(t.join(' '), nodePack.examples);
        var now = hasFlag(t, '--now');
        if (unit === 'kubelet') {
          if (act === 'status') {
            var lines = ['● kubelet.service - kubelet: The Kubernetes Node Agent',
              '     Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; preset: enabled)',
              '    Drop-In: /usr/lib/systemd/system/kubelet.service.d', '             └─10-kubeadm.conf'];
            if (m.daemonReloadNeeded) lines.unshift(RELOAD_WARN);
            var loadedPath = s.execLoaded ? GOOD_KUBELET : (s.execOnDisk ? '/usr/local/bin/kubelet' : nodeExecPath(s, ctx));
            if (m.kubeletUnit === 'active') lines.push('     Active: active (running) since Thu 2026-10-22 09:20:11 EDT; 3s ago', '   Main PID: 6411 (kubelet)');
            else if (m.kubeletUnit === 'inactive') lines.push('     Active: inactive (dead) since Thu 2026-10-22 09:02:40 EDT');
            else lines.push('     Active: activating (auto-restart) (Result: exit-code) since Thu 2026-10-22 09:14:31 EDT; 4s ago',
              '    Process: 5873 ExecStart=' + loadedPath + ' $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS (code=exited, status=203/EXEC)',
              '   Main PID: 5873 (code=exited, status=203/EXEC)');
            return res(lines, m.kubeletUnit === 'active' ? 0 : 3, null, ['kubelet-status', 'kubelet-status-' + (m.kubeletUnit === 'auto-restart-203' ? '203' : m.kubeletUnit)]);
          }
          if (act === 'stop' || act === 'disable' && now) return res([], 0, { kubeletOn: false }, ['kubelet-stopped']);
          if (act === 'start' || act === 'restart' || (act === 'enable' && now)) {
            var w = m.daemonReloadNeeded ? [RELOAD_WARN] : [];
            if (!s.execLoaded) w.push('(sim) the unit starts, then exits 203/EXEC — read it with systemctl status kubelet');
            return res(w, 0, { kubeletOn: true }, ['kubelet-restarted', s.execLoaded ? 'kubelet-restarted-ok' : 'kubelet-restarted-203']);
          }
          if (act === 'enable') return res([], 0, null, ['kubelet-enabled']);
          return unmodelled(t.join(' '), nodePack.examples);
        }
        if (act === 'status') {
          var up = !!s.runtimeUp;
          return res(['● containerd.service - containerd container runtime', '     Loaded: loaded (/usr/lib/systemd/system/containerd.service; enabled; preset: enabled)',
            up ? '     Active: active (running) since Thu 2026-10-22 08:01:12 EDT; 1h 19min ago' : '     Active: inactive (dead) since Thu 2026-10-22 09:11:58 EDT; 3min ago',
            up ? '   Main PID: 812 (containerd)' : '(sim) running containers are still held by their containerd-shim processes'], up ? 0 : 3, null, ['containerd-status', up ? 'containerd-active' : 'containerd-inactive']);
        }
        if (act === 'stop') return res([], 0, { runtimeUp: false }, ['containerd-stopped']);
        if (act === 'start' || act === 'restart' || (act === 'enable' && now)) return res([], 0, { runtimeUp: true }, ['containerd-started']);
        if (act === 'enable') return res([], 0, null, ['containerd-enabled']);
        return unmodelled(t.join(' '), nodePack.examples);
      }
      if (t[0] === 'journalctl') {
        var ju = flag(t, ['-u', '--unit']);
        if (String(ju).replace(/\.service$/, '') !== 'kubelet') return res(['sim: this drill models journalctl -u kubelet'], 2);
        var jl = ['-- (sim) representative kubelet / systemd journal lines for node-01 --'], ev = ['journal-kubelet'];
        if (m.kubeletUnit === 'auto-restart-203') {
          var bad = s.execLoaded ? GOOD_KUBELET : (s.execOnDisk ? '/usr/local/bin/kubelet' : nodeExecPath(s, ctx));
          jl.push('Oct 22 09:14:31 node-01 systemd[1]: kubelet.service: Failed to locate executable ' + bad + ': No such file or directory',
            'Oct 22 09:14:31 node-01 systemd[1]: kubelet.service: Failed at step EXEC spawning ' + bad + ': No such file or directory',
            'Oct 22 09:14:31 node-01 systemd[1]: kubelet.service: Main process exited, code=exited, status=203/EXEC',
            'Oct 22 09:14:31 node-01 systemd[1]: kubelet.service: Failed with result \'exit-code\'.');
          ev.push('journal-203');
        } else if (m.kubeletUnit === 'inactive') {
          jl.push('Oct 22 09:02:40 node-01 systemd[1]: Stopped kubelet.service - kubelet: The Kubernetes Node Agent.');
          ev.push('journal-stopped');
        } else {
          if (!s.runtimeUp) { jl.push('Oct 22 09:14:07 node-01 kubelet[6411]: ' + SOCK_ERR, 'Oct 22 09:14:07 node-01 kubelet[6411]: E1022 09:14:07.512388    6411 kubelet.go] "Skipping pod synchronization" err="container runtime is down"'); ev.push('journal-runtime'); }
          if (!s.cniOk) { jl.push('Oct 22 09:14:12 node-01 kubelet[6411]: E1022 09:14:12.104227    6411 kubelet.go] "Container runtime network not ready" networkReady="NetworkReady=false reason:NetworkPluginNotReady message:Network plugin returns error: cni plugin not initialized"'); ev.push('journal-cni'); }
          if (m.diskPressure === true) { jl.push('Oct 22 09:14:20 node-01 kubelet[6411]: W1022 09:14:20.330918    6411 eviction_manager.go] "Eviction manager: attempting to reclaim" resourceName="ephemeral-storage"',
            'Oct 22 09:14:20 node-01 kubelet[6411]: I1022 09:14:20.331120    6411 eviction_manager.go] "Eviction manager: pods ranked for eviction" pods=["default/' + NODE_PODS[2][0] + '","default/' + NODE_PODS[3][0] + '","default/' + NODE_PODS[1][0] + '","default/' + NODE_PODS[0][0] + '"]');
            ev.push('journal-eviction'); }
          if (ev.length === 1) jl.push('(sim) no errors in the modelled window — kubelet is posting Ready');
        }
        return res(jl, 0, null, ev);
      }
      if (t[0] === 'crictl') {
        if (!s.runtimeUp) return res(['E1022 09:14:40.118034    7020 remote_runtime.go] validate service connection: validate CRI v1 runtime API for endpoint "unix:///run/containerd/containerd.sock": rpc error: code = Unavailable desc = connection error: desc = "transport: Error while dialing: dial unix /run/containerd/containerd.sock: connect: no such file or directory"'], 1, null, ['crictl-sock-refused']);
        if (t[1] === 'rmi' && hasFlag(t, '--prune')) {
          if (!s.diskPressure) return res(['(sim) no unused images to prune'], 0, null, ['images-pruned-none']);
          return res(['Deleted: registry.example.com/batch/report-builder:2024.11', 'Deleted: registry.example.com/batch/report-builder:2025.03', 'Deleted: docker.io/library/golang:1.22', '(sim) nodefs.available back above the 10% threshold'], 0, { diskPressure: false }, ['images-pruned']);
        }
        if (t[1] === 'ps') {
          var rows = [['CONTAINER', 'IMAGE', 'STATE', 'NAME', 'POD']];
          rows.push(['4c1a9e2f0b77', 'calico/node:v3.30.3', 'Running', 'calico-node', 'calico-node-4tq8z']);
          rows.push(['9b3d70c1e5a2', 'registry.k8s.io/kube-proxy:v1.37.1', 'Running', 'kube-proxy', 'kube-proxy-7m2kd']);
          NODE_PODS.forEach(function (p, i) { if (!(i >= 2 && (m.evictBestEffort || ctx.vars.evicted))) rows.push([(i + 1) + 'e7f0d2a91c' + i, p[0].split('-')[0], 'Running', p[0].split('-')[0], p[0]]); });
          return res(table(rows), 0, null, ['crictl', 'crictl-ps']);
        }
        if (t[1] === 'images') return res(table([['IMAGE', 'TAG', 'SIZE'], ['registry.example.com/batch/report-builder', '2024.11', '3.1GB'], ['registry.example.com/batch/report-builder', '2025.03', '3.3GB'], ['docker.io/library/golang', '1.22', '842MB']].slice(0, s.diskPressure ? 4 : 1).concat(s.diskPressure ? [] : [['(sim) unused images already pruned', '', '']])), 0, null, ['crictl-images']);
        return unmodelled(t.join(' '), nodePack.examples);
      }
      if (t[0] === 'df') {
        var full = !!s.diskPressure;
        return res(['Filesystem      Size  Used Avail Use% Mounted on', '/dev/sda1        50G  ' + (full ? '46G  2.6G  95%' : '29G   19G  61%') + ' /'], 0, null, ['df', full ? 'df-full' : 'df-ok']);
      }
      if (t[0] !== 'kubectl') return null;
      if (onNode) return res(['The connection to the server localhost:8080 was refused - did you specify the right host or port?', '(sim) node-01 has no admin kubeconfig — run kubectl from controlplane (`exit`)'], 1, null, ['kubectl-on-node']);
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED), ns = flag(t, ['-n', '--namespace']) || 'default';
      var kind = (args[0] || '').toLowerCase(), nm = args[1] || '';
      if (/\//.test(kind)) { nm = kind.split('/')[1]; kind = kind.split('/')[0]; }
      var node1 = m.ready === 'True' ? 'Ready' : 'NotReady';
      if (verb === 'get' && /^(nodes?|no)$/.test(kind)) {
        var wide = /wide/.test(String(flag(t, ['-o', '--output']) || ''));
        var nrows = [['NAME', 'STATUS', 'ROLES', 'AGE', 'VERSION'].concat(wide ? ['INTERNAL-IP', 'CONTAINER-RUNTIME'] : [])];
        nrows.push(['controlplane', 'Ready', 'control-plane', '41d', 'v1.37.1'].concat(wide ? ['10.0.0.10', 'containerd://2.1.4'] : []));
        nrows.push(['node-01', node1, '<none>', '41d', 'v1.37.1'].concat(wide ? ['10.0.0.21', 'containerd://2.1.4'] : []));
        nrows.push(['node-02', 'Ready', '<none>', '41d', 'v1.37.1'].concat(wide ? ['10.0.0.22', 'containerd://2.1.4'] : []));
        return res(table(nrows), 0, null, ['get-nodes', node1 === 'Ready' ? 'get-nodes-ready' : 'get-nodes-notready']);
      }
      if (verb === 'describe' && /^(nodes?|no)$/.test(kind)) {
        if (nm && nm !== 'node-01') return res(['(sim) ' + nm + ' is healthy: Ready=True, no pressure conditions — the patient is node-01'], 0, null, ['describe-node-other']);
        var unk = m.ready === 'Unknown', cond = function (type, st, reason, msg) { return '  ' + pad(type, 16) + pad(st, 9) + pad(reason, 30) + msg; };
        var tl = m.taint ? m.taintEffects.map(function (e, i) { return (i ? '                    ' : 'Taints:             ') + m.taint + ':' + e; }) : ['Taints:             <none>'];
        var dl = ['Name:               node-01', 'Roles:              <none>'].concat(tl).concat(['Unschedulable:      false', 'Conditions:', '  Type            Status   Reason                        Message', '  ----            ------   ------                        -------']);
        if (unk) {
          ['MemoryPressure', 'DiskPressure', 'PIDPressure', 'Ready'].forEach(function (c) { dl.push(cond(c, 'Unknown', 'NodeStatusUnknown', 'Kubelet stopped posting node status.')); });
        } else {
          dl.push(cond('MemoryPressure', 'False', 'KubeletHasSufficientMemory', 'kubelet has sufficient memory available'));
          dl.push(m.diskPressure === true ? cond('DiskPressure', 'True', 'KubeletHasDiskPressure', 'kubelet has disk pressure') : cond('DiskPressure', 'False', 'KubeletHasNoDiskPressure', 'kubelet has no disk pressure'));
          dl.push(cond('PIDPressure', 'False', 'KubeletHasSufficientPID', 'kubelet has sufficient PID available'));
          dl.push(m.ready === 'True' ? cond('Ready', 'True', 'KubeletReady', 'kubelet is posting ready status') : cond('Ready', 'False', 'KubeletNotReady', m.reason.replace(/^KubeletNotReady: /, '')));
        }
        dl.push('System Info:', '  Container Runtime Version:  containerd://2.1.4', '  Kubelet Version:            v1.37.1');
        if (m.diskPressure === true) dl.push('Events:', '  Warning  EvictionThresholdMet  kubelet  Attempting to reclaim ephemeral-storage');
        var tag = unk ? 'unknown' : (m.ready === 'False-runtime' ? 'runtime-down' : (m.ready === 'False-cni' ? 'cni' : (m.diskPressure === true ? 'diskpressure' : 'ok')));
        return res(dl, 0, null, ['describe-node', 'describe-node-' + tag]);
      }
      if (verb === 'get' && /^(pods?|po)$/.test(kind)) {
        var sys = ns === 'kube-system';
        var wide2 = /wide/.test(String(flag(t, ['-o', '--output']) || ''));
        var prow = [['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE'].concat(wide2 ? ['NODE'] : [])];
        if (sys) {
          prow.push(['calico-node-4tq8z', s.cniOk ? '1/1' : '0/1', 'Running', '0', '41d'].concat(wide2 ? ['node-01'] : []));
          prow.push(['calico-node-m2c7d', '1/1', 'Running', '0', '41d'].concat(wide2 ? ['node-02'] : []));
          prow.push(['coredns-7c65d6cfc9-x8rwd', '1/1', 'Running', '0', '41d'].concat(wide2 ? ['node-02'] : []));
          return res(table(prow), 0, null, ['get-pods-system']);
        }
        if (m.evictBestEffort) ctx.vars.evicted = true;
        var ev2 = !!ctx.vars.evicted;
        NODE_PODS.forEach(function (p, i) {
          var gone = i >= 2 && ev2;
          prow.push([p[0], gone ? '0/1' : '1/1', gone ? 'Evicted' : 'Running', '0', '6d'].concat(wide2 ? ['node-01'] : []));
        });
        if (ev2) { prow.push(['batch-7c5d8-r7v1c', '1/1', 'Running', '0', '40s'].concat(wide2 ? ['node-02'] : [])); prow.push(['batch-7c5d8-z3h8q', '1/1', 'Running', '0', '40s'].concat(wide2 ? ['node-02'] : [])); }
        return res(table(prow), 0, null, ['get-pods', ev2 ? 'get-pods-evicted' : 'get-pods-running']);
      }
      if (verb === 'rollout' && args[0] === 'restart' && /^(daemonsets?|ds)(\/calico-node)?$/.test(String(args[1] || '')) && (args[2] === 'calico-node' || /\/calico-node$/.test(args[1]))) {
        if (ns !== 'kube-system') return notFound('daemonsets.apps', 'calico-node');
        var canRun = m.kubeletActive && s.runtimeUp;
        return res(['daemonset.apps/calico-node restarted'].concat(canRun ? [] : ['(sim) the new calico-node pod cannot start on node-01 until its kubelet and runtime are up']), 0, canRun ? { cniOk: true } : null, ['cni-ds-restarted']);
      }
      if (verb === 'delete' && /^(pods?|po)$/.test(kind) && /^calico-node-4tq8z$/.test(nm) && ns === 'kube-system') {
        var canRun2 = m.kubeletActive && s.runtimeUp;
        return res(['pod "calico-node-4tq8z" deleted'], 0, canRun2 ? { cniOk: true } : null, ['cni-ds-restarted']);
      }
      return unmodelled(t.join(' '), nodePack.examples);
    },
    tasks: [
      { id: 'kubelet-203', title: 'NotReady after an upgrade: kubelet exits 203/EXEC',
        goal: 'node-01 went NotReady after an in-place upgrade. Find why its kubelet will not stay up, fix the unit, and bring the node back to Ready.',
        setup: { kubeletOn: true, execLoaded: false, execOnDisk: false, runtimeUp: true, cniOk: true, diskPressure: false },
        steps: [
          { label: 'See node-01 NotReady', event: 'get-nodes-notready', hint: 'kubectl get nodes' },
          { label: 'Read node-01’s conditions: Kubelet stopped posting node status', event: 'describe-node-unknown', hint: 'kubectl describe node node-01' },
          { label: 'On node-01, read the kubelet unit status (203/EXEC)', event: 'kubelet-status-203', hint: 'ssh node-01 systemctl status kubelet' },
          { label: 'Find the bad ExecStart in the kubeadm drop-in', event: 'cat-dropin-bad', hint: 'ssh node-01 cat ' + DROPIN },
          { label: 'Point ExecStart at the real kubelet binary', state: function (s) { return !!s.execOnDisk; }, hint: "ssh node-01 sudo sed -i 's|/usr/local/bin/kubelet|/usr/bin/kubelet|' " + DROPIN },
          { label: 'Make systemd load the edited unit', state: function (s) { return !!s.execLoaded; }, hint: 'ssh node-01 sudo systemctl daemon-reload' },
          { label: 'Restart the kubelet and see it active (running)', event: 'kubelet-status-active', hint: 'ssh node-01 sudo systemctl restart kubelet  then  ssh node-01 systemctl status kubelet' },
          { label: 'node-01 is Ready again', event: 'get-nodes-ready', hint: 'kubectl get nodes' }
        ] },
      { id: 'runtime-down', title: 'Container runtime is down',
        goal: 'node-01 reports “container runtime is down”. Prove it from the node, start the runtime, and confirm Ready.',
        setup: { kubeletOn: true, execLoaded: true, execOnDisk: true, runtimeUp: false, cniOk: true, diskPressure: false },
        steps: [
          { label: 'Read the Ready condition: container runtime is down', event: 'describe-node-runtime-down', hint: 'kubectl describe node node-01' },
          { label: 'On node-01, watch crictl fail at the containerd socket', event: 'crictl-sock-refused', hint: 'ssh node-01 sudo crictl ps' },
          { label: 'See containerd inactive (dead)', event: 'containerd-inactive', hint: 'ssh node-01 systemctl status containerd' },
          { label: 'Start containerd (and keep it enabled)', state: function (s) { return !!s.runtimeUp; }, hint: 'ssh node-01 sudo systemctl enable --now containerd' },
          { label: 'node-01 is Ready again', event: 'get-nodes-ready', hint: 'kubectl get nodes' }
        ] },
      { id: 'cni-missing', title: 'NotReady: cni plugin not initialized',
        goal: 'node-01 is NotReady and new pods will not land there. Trace it to the CNI config, get the CNI DaemonSet to rewrite it, and confirm Ready.',
        setup: { kubeletOn: true, execLoaded: true, execOnDisk: true, runtimeUp: true, cniOk: false, diskPressure: false },
        steps: [
          { label: 'See node-01 NotReady', event: 'get-nodes-notready', hint: 'kubectl get nodes' },
          { label: 'Read the Ready message: NetworkPluginNotReady', event: 'describe-node-cni', hint: 'kubectl describe node node-01' },
          { label: 'Find the same error in the kubelet journal on node-01', event: 'journal-cni', hint: 'ssh node-01 sudo journalctl -u kubelet -n 20 --no-pager' },
          { label: 'Confirm /etc/cni/net.d is empty', event: 'ls-cni-empty', hint: 'ssh node-01 ls /etc/cni/net.d' },
          { label: 'Restart the CNI DaemonSet so its install step rewrites the conflist', state: function (s) { return !!s.cniOk; }, hint: 'kubectl rollout restart daemonset calico-node -n kube-system' },
          { label: 'node-01 is Ready again', event: 'get-nodes-ready', hint: 'kubectl get nodes' }
        ] },
      { id: 'disk-pressure', title: 'DiskPressure: who gets evicted first?',
        goal: 'node-01’s root disk crossed the kubelet’s hard eviction threshold. Read the condition and the evictions, find the space, reclaim it, and confirm the pressure clears.',
        setup: { kubeletOn: true, execLoaded: true, execOnDisk: true, runtimeUp: true, cniOk: true, diskPressure: true },
        steps: [
          { label: 'Read DiskPressure=True and the disk-pressure taint', event: 'describe-node-diskpressure', hint: 'kubectl describe node node-01' },
          { label: 'See which pods were evicted (and where their replacements went)', event: 'get-pods-evicted', hint: 'kubectl get pods -o wide' },
          { label: 'On node-01, see the root filesystem at 95%', event: 'df-full', hint: 'ssh node-01 df -h /' },
          { label: 'Reclaim space by pruning unused images', state: function (s) { return !s.diskPressure; }, hint: 'ssh node-01 sudo crictl rmi --prune' },
          { label: 'DiskPressure is False again', event: 'describe-node-ok', hint: 'kubectl describe node node-01' }
        ] }
    ]
  };

  /* ── pack: Service + DNS troubleshooting (v1.5.0, 2026-10-23 — CKA Troubleshooting 30% / Services & Networking 20%) ──
   * Drives service-dns on the NEW authored service-dns.glb. Namespaces: shop (deploy/web = the client, pod dnsutils =
   * the debug pod from the Kubernetes DNS-debugging docs, deploy/api behind Service api), kube-system (CoreDNS behind
   * Service kube-dns), data (Service db). Lookups go through ILImmersiveSims.svcDnsResolve (resolv.conf search list,
   * ndots:5). `kubectl get … -o yaml > FILE`, `sed -i` and `kubectl apply -f FILE` are modelled for the CoreDNS
   * ConfigMap only; files live in this terminal session. nslookup output is shaped like bind's (dnsutils image). */
  var SD_NOTE = 'Namespaces: shop (deploy/web is the client, pod dnsutils is a debug pod, deploy/api sits behind Service api) · kube-system (CoreDNS behind Service kube-dns) · data (Service db). Edit with `kubectl get … -o yaml > FILE`, `sed -i`, `kubectl apply -f FILE` (no interactive editor in a simulated shell). Lookups and probes are computed by the rules engine. Lab-only: fault selector|targetport|corefile|netpol|fqdn break|fix.';
  var SD_PODS = { web: 'web-5d8f7c9b4-q2x9m', dnsutils: 'dnsutils', api0: 'api-6c9f8d7b5-4kx2p', api1: 'api-6c9f8d7b5-r8m3t' };
  var SD_COREFILE = function (ok) {
    return ['.:53 {', '    errors', '    health {', '       lameduck 5s', '    }', '    ready', '    kubernetes cluster.local in-addr.arpa ip6.arpa {', '       pods insecure', '       fallthrough in-addr.arpa ip6.arpa', '       ttl 30', '    }', '    prometheus :9153',
      '    ' + (ok ? 'forward' : 'forwrd') + ' . /etc/resolv.conf {', '       max_concurrent 1000', '    }', '    cache 30', '    loop', '    reload', '    loadbalance', '}'];
  };
  function sdCorefileYaml(ok) {
    return ['apiVersion: v1', 'kind: ConfigMap', 'metadata:', '  name: coredns', '  namespace: kube-system', 'data:', '  Corefile: |'].concat(SD_COREFILE(ok).map(function (l) { return '    ' + l; }));
  }
  var SD_ALLOW_DNS = ['apiVersion: networking.k8s.io/v1', 'kind: NetworkPolicy', 'metadata:', '  name: allow-dns-egress', '  namespace: shop', 'spec:', '  podSelector: {}', '  policyTypes:', '  - Egress', '  egress:', '  - to:', '    - namespaceSelector:', '        matchLabels:', '          kubernetes.io/metadata.name: kube-system', '      podSelector:', '        matchLabels:', '          k8s-app: kube-dns', '    ports:', '    - protocol: UDP', '      port: 53', '    - protocol: TCP', '      port: 53'];
  function sdFiles(ctx) { return ctx.vars.sdFiles || (ctx.vars.sdFiles = {}); }
  function sdFqdnOk(h) { return /^db\.data(\.svc(\.cluster\.local)?)?\.?$/.test(String(h || '')); }
  function sdDbHost(s, ctx) { var h = ctx.vars.dbHost; return h && sdFqdnOk(h) === !!s.fqdnOk ? h : (s.fqdnOk ? 'db.data.svc.cluster.local' : 'db'); }
  function sdResolve(s, name, opts) { var S = Sims(); return S && S.svcDnsResolve ? S.svcDnsResolve(s, name, opts) : { status: 'refused', tried: [] }; }
  /** nslookup / dig / curl / cat inside a shop pod. */
  function sdInPod(s, d, ctx, cmd) {
    var bin = cmd[0], args = cmd.slice(1).filter(function (a) { return a.charAt(0) !== '-' && a.charAt(0) !== '+'; });
    if (bin === 'cat' && cmd[1] === '/etc/resolv.conf') {
      return res(['search shop.svc.cluster.local svc.cluster.local cluster.local', 'nameserver 10.96.0.10', 'options ndots:5'], 0, null, ['resolv-conf']);
    }
    if (bin === 'nslookup' || bin === 'dig' || bin === 'host') {
      var name = args[0] || '';
      if (!name) return res(['sim: give a name, e.g. nslookup api'], 2);
      var isIp = /^\d+\.\d+\.\d+\.\d+$/.test(name);
      if (isIp || !/^[a-z0-9.-]+$/i.test(name)) return res(['sim: this lab models forward lookups of cluster names (api, db.data, kubernetes.default, …)'], 2);
      var dig = bin === 'dig', short = dig && cmd.indexOf('+short') >= 0, search = !dig || cmd.indexOf('+search') >= 0;
      var r = sdResolve(s, name, { noSearch: !search });
      if (r.status !== 'ok' && r.status !== 'nxdomain') {
        var lines = r.status === 'timeout' ? [';; connection timed out; no servers could be reached'] : [';; communications error to 10.96.0.10#53: connection refused', ';; no servers could be reached'];
        if (r.status === 'timeout') lines.push('(sim) the resolver retried and gave up — no clock is simulated');
        return res(lines.concat(['', 'command terminated with exit code ' + (dig ? 9 : 1)]), dig ? 9 : 1, null, ['dns', 'dns-' + r.status]);
      }
      var outName = r.fqdn || name;
      if (!/(^|\.)(cluster\.local|svc)\.?$/.test(r.fqdn || '') && r.status === 'nxdomain' && !/^(api|db|kubernetes|kube-dns)(\.|$)/.test(name.toLowerCase())) {
        return res(['sim: this lab models cluster names only (api, db.data, kubernetes.default, kube-dns.kube-system); there is no internet upstream'], 2);
      }
      if (dig) {
        if (short) return res(r.status === 'ok' ? [r.ip] : [], 0, null, ['dns', 'dns-' + r.status]);
        return res(['; <<>> DiG 9.18 <<>> ' + cmd.slice(1).join(' '), ';; ->>HEADER<<- opcode: QUERY, status: ' + (r.status === 'ok' ? 'NOERROR' : 'NXDOMAIN')].concat(
          r.status === 'ok' ? [';; ANSWER SECTION:', outName + '.\t30\tIN\tA\t' + r.ip] : (search ? [] : ['(sim) dig does not use the search list unless you pass +search'])).concat([';; SERVER: 10.96.0.10#53(10.96.0.10) (UDP)']), 0, null, ['dns', 'dns-' + r.status]);
      }
      if (r.status === 'nxdomain') return res(['Server:\t\t10.96.0.10', 'Address:\t10.96.0.10#53', '', '** server can\'t find ' + name + ': NXDOMAIN', '', 'command terminated with exit code 1'], 1, null, ['dns', 'dns-nxdomain']);
      return res(['Server:\t\t10.96.0.10', 'Address:\t10.96.0.10#53', '', 'Name:\t' + outName, 'Address: ' + r.ip], 0, null, ['dns', 'dns-ok']);
    }
    if (bin === 'curl' || bin === 'wget') {
      var url = '';
      for (var ci = 1; ci < cmd.length; ci++) {
        if (/^(-m|--max-time|--connect-timeout|-o|--output|-H|--header|-w|--write-out|-X|-T|--timeout|-O)$/.test(cmd[ci])) { ci++; continue; }
        if (cmd[ci].charAt(0) !== '-') { url = cmd[ci]; break; }
      }
      var m = /^(?:https?:\/\/)?([^\/:]+)(?::(\d+))?/.exec(url);
      if (!m) return res(['curl: (3) URL rejected: No host part in the URL'], 3);
      var host = m[1].toLowerCase(), port = m[2] || '80', ip = host;
      if (!/^\d+\.\d+\.\d+\.\d+$/.test(host)) {
        var rr = sdResolve(s, host);
        if (rr.status !== 'ok') return res(['curl: (6) Could not resolve host: ' + host, 'command terminated with exit code 6'], 6, null, ['probe', 'curl-api-dns-fail']);
        ip = rr.ip;
      }
      if (ip !== '10.96.88.20' || port !== '80') return res(['sim: this drill probes Service api (http://api, http://api.shop.svc.cluster.local or http://10.96.88.20 on port 80)'], 2);
      var viaIp = host === ip;
      if (d.metrics.apiByIp !== 'ok') return res(['curl: (7) Failed to connect to ' + host + ' port 80 after 1 ms: Couldn\'t connect to server', 'command terminated with exit code 7'], 7, null, ['probe', 'curl-api-refused']);
      return res(['{"service":"api","pod":"' + SD_PODS.api0 + '","port":8080,"ok":true}'], 0, null, ['probe', 'curl-api-ok'].concat(viaIp ? ['curl-api-ip-ok'] : ['curl-api-name-ok']));
    }
    return res(['sim: inside the shop pods this drill models nslookup / dig (dnsutils), curl (web) and cat /etc/resolv.conf'], 2);
  }
  var svcDnsPack = {
    sim: 'service-dns',
    prompt: 'student@controlplane:~$',
    note: SD_NOTE,
    files: { 'allow-dns-egress.yaml': { yaml: SD_ALLOW_DNS } },
    examples: ['kubectl get svc -A', 'kubectl get svc api -n shop -o wide', 'kubectl describe svc api -n shop', 'kubectl get endpointslices -n shop -l kubernetes.io/service-name=api',
      'kubectl get pods -n shop --show-labels', 'kubectl describe deployment api -n shop', 'kubectl exec -n shop deploy/web -- curl -s -m 3 http://api',
      'kubectl exec -n shop dnsutils -- nslookup api', 'kubectl exec -n shop dnsutils -- nslookup db.data', 'kubectl exec -n shop dnsutils -- cat /etc/resolv.conf',
      'kubectl get pods -n kube-system -l k8s-app=kube-dns', 'kubectl logs -n kube-system -l k8s-app=kube-dns', 'kubectl get configmap coredns -n kube-system -o yaml',
      'kubectl get networkpolicy -n shop', 'kubectl describe networkpolicy default-deny-egress -n shop', 'cat allow-dns-egress.yaml', 'kubectl logs -n shop deploy/web',
      'kubectl set env deployment/web -n shop --list'],
    run: function (u, s, d, ctx) {
      var t = u.t, m = d.metrics, files = sdFiles(ctx);
      var f = faultArgs(t);
      if (f) {
        var key = { selector: 'selectorOk', targetport: 'targetPortOk', corefile: 'corefileOk', netpol: 'dnsEgress', fqdn: 'fqdnOk' }[f[0]];
        if (!key || (f[1] !== 'break' && f[1] !== 'fix')) return res(['usage: fault selector|targetport|corefile|netpol|fqdn break|fix   (lab-only fault injection)'], 2);
        var fs = {}; fs[key] = f[1] === 'fix';
        if (key === 'fqdnOk') ctx.vars.dbHost = null;
        return res(['[lab fault injection] ' + f.join(' ') + ' (simulated)'], 0, fs, ['fault']);
      }
      /* output redirection: modelled for saving the CoreDNS ConfigMap only */
      var ri = -1;
      for (var i = 0; i < t.length; i++) if (t[i] === '>' || /^>[^>]/.test(t[i])) { ri = i; break; }
      var redirect = null;
      if (ri >= 0) {
        redirect = t[ri] === '>' ? t[ri + 1] : t[ri].slice(1);
        t = t.slice(0, ri).concat(t[ri] === '>' ? t.slice(ri + 2) : t.slice(ri + 1));
        if (!redirect) return res(['bash: syntax error near unexpected token `newline\''], 2);
        redirect = redirect.replace(/^(\.\/|~\/)/, '');
      }
      if (t[0] === 'ls' && (t.length === 1 || /^(\.|~|\.\/|~\/|-l|-la|-al)$/.test(t[1] || ''))) return res([['allow-dns-egress.yaml'].concat(Object.keys(files)).join('  ')], 0, null, ['ls']);
      if (t[0] === 'cat' && t[1] && files[t[1].replace(/^(\.\/|~\/)/, '')]) {
        return res(sdCorefileYaml(files[t[1].replace(/^(\.\/|~\/)/, '')].ok), 0, null, ['cat', 'cat-corefile-file']);
      }
      var fr = fileRun(svcDnsPack, t); if (fr) return fr;
      if (t[0] === 'sed') {
        var inPlace = t.some(function (a) { return /^-[a-zA-Z]*i/.test(a) || a === '--in-place'; });
        var file = (t[t.length - 1] || '').replace(/^(\.\/|~\/)/, ''), expr = t.filter(function (a) { return a.charAt(0) === 's' && a.length > 3 && !/[a-z]/i.test(a.charAt(1)); })[0];
        if (!files[file]) return res(['sed: can\'t read ' + file + ': No such file or directory'], 2);
        var sub = sedSubst(expr);
        if (!sub) return res(["sed: -e expression #1, char 1: unknown command: `" + String(expr || '').charAt(0) + "'"], 1);
        var fixes = sub.a.length >= 4 && 'forwrd'.indexOf(sub.a) >= 0 && /^forward\b/.test(sub.b) && !files[file].ok;
        if (!inPlace) return res(['(sim) without -i sed prints the edited file to stdout — nothing was written'].concat(sdCorefileYaml(files[file].ok || fixes).slice(-10)), 0);
        if (!fixes) return res([], 0, null, ['sed-nochange']);
        files[file].ok = true;
        return res([], 0, null, ['corefile-file-fixed']);
      }
      if (t[0] === 'vi' || t[0] === 'vim' || t[0] === 'nano') return res(['sim: no interactive editor in a simulated shell — save with `kubectl get … -o yaml > FILE`, edit with sed -i, then kubectl apply -f FILE'], 2);
      if (t[0] === 'nslookup' || t[0] === 'dig') return res(['sim: controlplane does not use cluster DNS — run the lookup from a pod: kubectl exec -n shop dnsutils -- ' + t[0] + ' …'], 2, null, ['dns-wrong-place']);
      if (t[0] !== 'kubectl') return null;
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED.concat(['-c', '--container', '--tail'])), ns = nsOf(t), out = flag(t, ['-o', '--output']);
      var kind = (args[0] || '').toLowerCase(), name = args[1] || '';
      if (/\//.test(kind)) { name = kind.split('/')[1]; kind = kind.split('/')[0]; }
      if (redirect && !(verb === 'get' && /^(cm|configmaps?)$/.test(kind) && out === 'yaml')) return res(['sim: output redirection is modelled only for saving the CoreDNS ConfigMap (kubectl get configmap coredns -n kube-system -o yaml > coredns.yaml)'], 2);
      if (verb === 'edit') return res(['sim: interactive editors are not modelled — use kubectl patch, kubectl set, or get -o yaml > FILE + sed -i + apply -f (see `help`)'], 2);
      if (verb === 'get' && /^(svc|services?)$/.test(kind)) {
        var wide = out === 'wide', all = ns === '*';
        var SV = [['shop', 'api', 'ClusterIP', '10.96.88.20', '80/TCP', m.selector], ['data', 'db', 'ClusterIP', '10.96.140.5', '5432/TCP', 'app=db'],
          ['kube-system', 'kube-dns', 'ClusterIP', '10.96.0.10', '53/UDP,53/TCP,9153/TCP', 'k8s-app=kube-dns'], ['default', 'kubernetes', 'ClusterIP', '10.96.0.1', '443/TCP', '<none>']];
        var rows = SV.filter(function (r) { return (all || r[0] === ns) && (!name || r[1] === name); });
        if (!rows.length) return name ? notFound('services', name) : res(['No resources found in ' + ns + ' namespace.'], 0);
        var hdr = (all ? ['NAMESPACE'] : []).concat(['NAME', 'TYPE', 'CLUSTER-IP', 'EXTERNAL-IP', 'PORT(S)', 'AGE']).concat(wide ? ['SELECTOR'] : []);
        var tb = [hdr].concat(rows.map(function (r) { return (all ? [r[0]] : []).concat([r[1], r[2], r[3], '<none>', r[4], '12d']).concat(wide ? [r[5]] : []); }));
        var evs = ['get-svc'];
        if (rows.some(function (r) { return r[1] === 'db'; })) evs.push('svc-db-found');
        if (wide && rows.some(function (r) { return r[1] === 'api'; })) evs.push(s.selectorOk ? 'svc-api-selector-ok' : 'svc-api-selector-bad');
        return res(table(tb), 0, null, evs);
      }
      if (verb === 'describe' && /^(svc|services?)$/.test(kind)) {
        if (name === 'api' && ns === 'shop') {
          var ep = m.endpoints ? '10.244.1.21:' + m.endpointPort + ',10.244.2.17:' + m.endpointPort : '<none>';
          return res(['Name:                     api', 'Namespace:                shop', 'Labels:                   app=api', 'Selector:                 ' + m.selector, 'Type:                     ClusterIP',
            'IP Family Policy:         SingleStack', 'IP:                       10.96.88.20', 'Port:                     http  80/TCP', 'TargetPort:               ' + m.targetPort + '/TCP',
            'Endpoints:                ' + ep, 'Session Affinity:         None', 'Internal Traffic Policy:  Cluster', 'Events:                   <none>'], 0, null,
            ['describe-svc-api', m.endpoints ? 'describe-svc-api-tp' + m.targetPort : 'describe-svc-api-noendpoints']);
        }
        if (name === 'kube-dns' && ns === 'kube-system') {
          return res(['Name:              kube-dns', 'Namespace:         kube-system', 'Selector:          k8s-app=kube-dns', 'IP:                10.96.0.10', 'Port:              dns  53/UDP', 'TargetPort:        53/UDP',
            'Endpoints:         ' + (s.corefileOk ? '10.244.0.5:53,10.244.0.6:53' : '<none>  (sim: the CoreDNS pods are not Ready)'), 'Port:              dns-tcp  53/TCP', 'Port:              metrics  9153/TCP'], 0, null, ['describe-svc-kube-dns']);
        }
        return notFound('services', name || '');
      }
      if (verb === 'get' && /^(endpointslices?(\.discovery\.k8s\.io)?|eps|ep|endpoints)$/.test(kind)) {
        var legacy = /^(ep|endpoints)$/.test(kind), sel = flag(t, ['-l', '--selector']) || '';
        if (ns !== 'shop' || (sel && !/service-name=api$/.test(sel)) || (name && !/^api/.test(name))) return res(['sim: this drill models the EndpointSlice of Service api in ns shop (-l kubernetes.io/service-name=api)'], 2);
        if (legacy) return res(['Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice'].concat(table([['NAME', 'ENDPOINTS', 'AGE'], ['api', m.endpoints ? '10.244.1.21:' + m.endpointPort + ',10.244.2.17:' + m.endpointPort : '<none>', '12d']])), 0, null,
          ['eps-api', m.endpoints ? 'eps-api-port' + m.endpointPort : 'eps-api-empty']);
        return res(table([['NAME', 'ADDRESSTYPE', 'PORTS', 'ENDPOINTS', 'AGE'], ['api-7xk2q', 'IPv4', m.endpoints ? String(m.endpointPort) : '<unset>', m.endpoints ? '10.244.1.21,10.244.2.17' : '<unset>', '12d']]), 0, null,
          ['eps-api', m.endpoints ? 'eps-api-port' + m.endpointPort : 'eps-api-empty']);
      }
      if (verb === 'get' && /^(pods?|po)$/.test(kind)) {
        var lsel = flag(t, ['-l', '--selector']) || '', labels = hasFlag(t, '--show-labels');
        if (ns === 'kube-system') {
          var crash = !s.corefileOk;
          var cp = [['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE'], ['coredns-7c65d6cfc9-5qz8n', crash ? '0/1' : '1/1', crash ? 'CrashLoopBackOff' : 'Running', crash ? '6 (41s ago)' : '0', '12d'], ['coredns-7c65d6cfc9-x8rwd', crash ? '0/1' : '1/1', crash ? 'CrashLoopBackOff' : 'Running', crash ? '6 (38s ago)' : '0', '12d']];
          if (!/kube-dns/.test(lsel)) cp.push(['kube-proxy-7m2kd', '1/1', 'Running', '0', '12d'], ['calico-node-4tq8z', '1/1', 'Running', '0', '12d']);
          return res(table(cp), 0, null, ['get-pods-dns', crash ? 'coredns-pods-crash' : 'coredns-pods-running']);
        }
        if (ns !== 'shop') return res(['No resources found in ' + (ns === '*' ? 'the cluster (sim: pass -n shop or -n kube-system)' : ns + ' namespace.')], 0);
        var pr = [['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE'].concat(labels ? ['LABELS'] : [])];
        [[SD_PODS.api0, 'app=api,pod-template-hash=6c9f8d7b5'], [SD_PODS.api1, 'app=api,pod-template-hash=6c9f8d7b5'], [SD_PODS.web, 'app=web,pod-template-hash=5d8f7c9b4'], [SD_PODS.dnsutils, 'run=dnsutils']]
          .filter(function (p) { return !lsel || p[1].split(',').indexOf(lsel) >= 0; })
          .forEach(function (p) { pr.push([p[0], '1/1', 'Running', '0', '12d'].concat(labels ? [p[1]] : [])); });
        return res(table(pr), 0, null, ['get-pods', labels ? 'pods-labels' : 'get-pods-plain']);
      }
      if (verb === 'describe' && /^(deploy|deployments?(\.apps)?)$/.test(kind)) {
        if (ns !== 'shop' || name !== 'api') return name === 'web' && ns === 'shop' ? res(['Name: web', 'Namespace: shop', 'Containers:', '  web:', '    Image: registry.example.com/shop/web:3.4.0', '    Environment:', '      DB_HOST:  ' + sdDbHost(s, ctx)], 0, null, ['describe-deploy-web']) : notFound('deployments.apps', name);
        return res(['Name:                   api', 'Namespace:              shop', 'Selector:               app=api', 'Replicas:               2 desired | 2 updated | 2 total | 2 available | 0 unavailable',
          'Pod Template:', '  Labels:  app=api', '  Containers:', '   api:', '    Image:         registry.example.com/shop/api:1.8.2', '    Port:          8080/TCP', '    Host Port:     0/TCP',
          '    Readiness:     http-get http://:8080/healthz delay=0s timeout=1s period=10s', 'Conditions:', '  Available      True    MinimumReplicasAvailable'], 0, null, ['describe-deploy-api']);
      }
      if (verb === 'patch' && /^(svc|services?)$/.test(kind)) {
        if (name !== 'api' || ns !== 'shop') return name === 'api' ? notFound('services', 'api') : res(['sim: this drill models patches to Service api in ns shop'], 2);
        var j = jsonArg(t); if (j.err) return j.err;
        var spec = j.v && j.v.spec || {}, patch = {}, ev = ['patch-svc'];
        if (spec.selector && spec.selector.app) { patch.selectorOk = spec.selector.app === 'api'; ev.push(patch.selectorOk ? 'selector-fixed' : 'selector-broken'); }
        if (Array.isArray(spec.ports)) {
          var p80 = spec.ports.filter(function (p) { return p && Number(p.port) === 80; })[0];
          if (!p80 || p80.targetPort == null) return res(['sim: ports is a list merged on its `port` key — send {"spec":{"ports":[{"port":80,"targetPort":8080}]}}'], 2);
          patch.targetPortOk = String(p80.targetPort) === '8080';
          ev.push(patch.targetPortOk ? 'targetport-fixed' : 'targetport-broken');
        }
        if (!Object.keys(patch).length) return res(['sim: this drill models spec.selector.app and spec.ports[].targetPort on Service api'], 2);
        return res(['service/api patched'], 0, patch, ev);
      }
      if (verb === 'logs') {
        var lns = flag(t, ['-l', '--selector']) || '';
        if (ns === 'kube-system' && (/kube-dns/.test(lns) || /^(deploy|deployment)$/.test(kind) && name === 'coredns' || /^coredns-/.test(kind))) {
          if (!s.corefileOk) return res(['-- (sim) representative CoreDNS output --', '/etc/coredns/Corefile:13 - Error during parsing: Unknown directive \'forwrd\''], 0, null, ['coredns-logs', 'coredns-logs-parse-error']);
          return res(['-- (sim) representative CoreDNS output --', '.:53', '[INFO] plugin/reload: Running configuration SHA512 = 1b226df79860026c6a52e67daa10d7f0d57ec5b023288ec00c5e05f93523c894564e15b91770d3a07ae1cfbe861d15b37d4a0027e69c546ab112970993a3b03b', 'CoreDNS-1.12.1', 'linux/amd64, go1.24.1, 707c7c1'], 0, null, ['coredns-logs', 'coredns-logs-ok']);
        }
        if (ns === 'shop' && ((/^(deploy|deployment)$/.test(kind) && name === 'web') || kind === SD_PODS.web || /app=web/.test(lns))) {
          var host = sdDbHost(s, ctx), r = sdResolve(s, host);
          var tag = r.status === 'ok' ? 'ok' : (r.status === 'nxdomain' ? 'nxdomain' : 'timeout');
          var L = ['-- (sim) representative application log --'];
          if (tag === 'ok') L.push('2026/10/23 09:14:02 db: connected to ' + host + ':5432');
          else if (tag === 'nxdomain') L.push('2026/10/23 09:14:02 db: dial tcp: lookup ' + host + ' on 10.96.0.10:53: no such host', '2026/10/23 09:14:07 db: dial tcp: lookup ' + host + ' on 10.96.0.10:53: no such host');
          else L.push('2026/10/23 09:14:02 db: dial tcp: lookup ' + host + ' on 10.96.0.10:53: ' + (r.status === 'refused' ? 'read udp 10.244.1.30:41622->10.96.0.10:53: read: connection refused' : 'read udp 10.244.1.30:41622->10.96.0.10:53: i/o timeout'));
          return res(L, 0, null, ['web-logs', 'web-logs-' + tag]);
        }
        return res(['sim: this drill models logs for CoreDNS (-n kube-system -l k8s-app=kube-dns) and deploy/web in ns shop'], 2);
      }
      if (verb === 'get' && /^(cm|configmaps?)$/.test(kind)) {
        if (ns !== 'kube-system' || name !== 'coredns') return name ? notFound('configmaps', name) : res(['sim: this drill models ConfigMap coredns in ns kube-system'], 2);
        if (out !== 'yaml') return res(table([['NAME', 'DATA', 'AGE'], ['coredns', '1', '12d']]), 0, null, ['get-cm-coredns']);
        if (redirect) {
          files[redirect] = { ok: !!s.corefileOk };
          return res([], 0, null, ['corefile-exported']);
        }
        return res(sdCorefileYaml(!!s.corefileOk), 0, null, ['corefile-yaml', s.corefileOk ? 'corefile-ok' : 'corefile-bad']);
      }
      if (verb === 'apply' || (verb === 'create' && hasFlag(t, ['-f', '--filename']))) {
        var fname = String(flag(t, ['-f', '--filename']) || '').replace(/^(\.\/|~\/)/, '');
        if (files[fname]) {
          if (!files[fname].ok) return res(['configmap/coredns unchanged'], 0, null, ['apply-corefile-unchanged']);
          if (s.corefileOk) return res(['configmap/coredns unchanged'], 0, null, ['apply-corefile']);
          return res(['configmap/coredns configured', '(sim) the crash-looping CoreDNS pods load the fixed Corefile on their next restart (after the kubelet syncs the ConfigMap volume); the sim skips the back-off wait'], 0, { corefileOk: true }, ['apply-corefile', 'corefile-applied']);
        }
        var a = applyFile(svcDnsPack, t); if (a.err) return a.err;
        if (!s.dnsEgress) ctx.vars.sdAllowApplied = true;
        return res(['networkpolicy.networking.k8s.io/allow-dns-egress ' + (s.dnsEgress ? 'unchanged' : 'created')], 0, s.dnsEgress ? null : { dnsEgress: true }, ['apply-allow-dns']);
      }
      if (verb === 'rollout' && args[0] === 'restart' && ns === 'kube-system' && (/coredns$/.test(args[1] || '') || args[2] === 'coredns')) {
        return res(['deployment.apps/coredns restarted'].concat(s.corefileOk ? [] : ['(sim) the new pods parse the same Corefile and crash too — fix the ConfigMap first']), 0, null, ['coredns-restarted']);
      }
      if (/^(netpol|networkpolic(y|ies)(\.networking\.k8s\.io)?)$/.test(kind)) {
        if (verb === 'get') {
          if (ns !== 'shop') return res(['No resources found in ' + ns + ' namespace.'], 0);
          var np = [['NAME', 'POD-SELECTOR', 'AGE'], ['default-deny-egress', '<none>', '2h']];
          if (s.dnsEgress) np.push(['allow-dns-egress', '<none>', ctx.vars.sdAllowApplied ? '5s' : '2h']);
          return res(table(np), 0, null, ['get-netpol', s.dnsEgress ? 'get-netpol-dns' : 'get-netpol-nodns']);
        }
        if (verb === 'describe') {
          if (ns !== 'shop' || (name && !/^(default-deny-egress|allow-dns-egress)$/.test(name))) return notFound('networkpolicies.networking.k8s.io', name);
          var D = ['Name:         default-deny-egress', 'Namespace:    shop', 'Spec:', '  PodSelector:     <none> (Allowing the specific traffic to all pods in this namespace)', '  Not affecting ingress traffic',
            '  Allowing egress traffic:', '    To Port: <any> (traffic allowed to all ports)', '    To:', '      PodSelector: <none>', '  Policy Types: Egress'];
          if (name === 'allow-dns-egress') {
            if (!s.dnsEgress) return notFound('networkpolicies.networking.k8s.io', name);
            return res(['Name:         allow-dns-egress', 'Namespace:    shop', 'Spec:', '  PodSelector:     <none> (Allowing the specific traffic to all pods in this namespace)', '  Allowing egress traffic:', '    To Port: 53/UDP', '    To Port: 53/TCP', '    To:', '      NamespaceSelector: kubernetes.io/metadata.name=kube-system', '      PodSelector: k8s-app=kube-dns', '  Policy Types: Egress'], 0, null, ['describe-netpol-allow-dns']);
          }
          return res(D.concat(['(sim) egress is allowed only to pods in ns shop — nothing reaches kube-system']), 0, null, ['describe-netpol', 'describe-netpol-deny-egress']);
        }
      }
      if (verb === 'set' && args[0] === 'env') {
        var tgt = (args[1] || '').replace(/^(deploy|deployment|deployments)(\.apps)?\//, '');
        if (args[1] && /^(deploy|deployment|deployments)$/.test(args[1])) tgt = args[2];
        if (tgt !== 'web' || ns !== 'shop') return tgt === 'web' ? notFound('deployments.apps', 'web') : res(['sim: this drill models env on deployment/web in ns shop'], 2);
        if (hasFlag(t, '--list')) return res(['# Deployment web, container web', 'DB_HOST=' + sdDbHost(s, ctx)], 0, null, ['env-list']);
        var kv = args.filter(function (a) { return /^DB_HOST=/.test(a); })[0];
        if (!kv) return res(['sim: this drill models DB_HOST on deployment/web (kubectl set env deployment/web -n shop DB_HOST=…)'], 2);
        var val = kv.slice(8);
        ctx.vars.dbHost = val;
        return res(['deployment.apps/web env updated', '(sim) the Deployment rolls out new web pods with DB_HOST=' + val], 0, { fqdnOk: sdFqdnOk(val) }, ['set-env', sdFqdnOk(val) ? 'fqdn-fixed' : 'fqdn-still-bad']);
      }
      if (verb === 'set' && args[0] === 'selector') {
        var sv = (args[1] || '').replace(/^(svc|service)\//, ''), kvs = args[args[1] && /^(svc|service|services)$/.test(args[1]) ? 3 : 2] || '';
        if (args[1] && /^(svc|service|services)$/.test(args[1])) sv = args[2];
        var mm = /^app=([a-z0-9-]+)$/.exec(kvs);
        if (sv !== 'api' || ns !== 'shop' || !mm) return res(['sim: this drill models `kubectl set selector service api app=api -n shop`'], 2);
        return res(['service/api selector updated'], 0, { selectorOk: mm[1] === 'api' }, ['patch-svc', mm[1] === 'api' ? 'selector-fixed' : 'selector-broken']);
      }
      var ex = execArgs(t);
      if (ex) {
        if (!ex.hasDd || !ex.cmd.length) return res(['error: you must specify at least one command for the container (kubectl exec … -- CMD)'], 1);
        var okTarget = ex.ns === 'shop' && (ex.target === 'dnsutils' || ex.target === 'web' || ex.target === SD_PODS.web);
        if (!okTarget) return res(['Error from server (NotFound): pods "' + ex.target + '" not found' + (ex.ns === 'shop' ? '' : ' (this lab’s client pods are in ns shop: dnsutils, deploy/web)')], 1, null, ['not-found']);
        if (ex.target !== 'dnsutils' && /^(nslookup|dig|host)$/.test(ex.cmd[0])) return res(['OCI runtime exec failed: exec failed: unable to start container process: exec: "' + ex.cmd[0] + '": executable file not found in $PATH: unknown', '(sim) the web image has no DNS tools — use the dnsutils debug pod', 'command terminated with exit code 126'], 126);
        if (ex.target === 'dnsutils' && /^(curl|wget)$/.test(ex.cmd[0])) return res(['OCI runtime exec failed: exec failed: unable to start container process: exec: "' + ex.cmd[0] + '": executable file not found in $PATH: unknown', '(sim) probe from deploy/web instead', 'command terminated with exit code 126'], 126);
        return sdInPod(s, d, ctx, ex.cmd);
      }
      if (verb === 'run') {
        var dd = t.indexOf('--');
        if (dd < 0 || ns !== 'shop') return res(['sim: this drill models a one-shot debug pod in ns shop: kubectl run tmp -n shop --rm -it --restart=Never --image=registry.k8s.io/e2e-test-images/agnhost:2.39 -- nslookup api'], 2);
        var rr2 = sdInPod(s, d, ctx, t.slice(dd + 1));
        rr2.out = rr2.out.concat(rr2.exit === 0 || rr2.exit === 1 ? ['pod "' + (args[0] || 'tmp') + '" deleted'] : []);
        return rr2;
      }
      return unmodelled(t.join(' '), svcDnsPack.examples);
    },
    tasks: [
      { id: 'target-port', title: 'Endpoints are there, connections are refused',
        goal: 'web cannot reach api, yet both api pods are Running and Ready. Follow Service → EndpointSlice → container to the port that does not line up, fix it, and get a 200.',
        setup: { selectorOk: true, targetPortOk: false, corefileOk: true, dnsEgress: true, fqdnOk: true },
        steps: [
          { label: 'Reproduce it: web → api is refused', event: 'curl-api-refused', hint: 'kubectl exec -n shop deploy/web -- curl -s -m 3 http://api' },
          { label: 'The EndpointSlice lists both pods — on port 80', event: 'eps-api-port80', hint: 'kubectl get endpointslices -n shop -l kubernetes.io/service-name=api' },
          { label: 'Read the Service: TargetPort 80/TCP', event: 'describe-svc-api-tp80', hint: 'kubectl describe svc api -n shop' },
          { label: 'Find the port the api container really listens on', event: 'describe-deploy-api', hint: 'kubectl describe deployment api -n shop' },
          { label: 'Point targetPort at the container port', state: function (s) { return !!s.targetPortOk; }, hint: 'kubectl patch svc api -n shop -p \'{"spec":{"ports":[{"port":80,"targetPort":8080}]}}\'' },
          { label: 'web → api answers', event: 'curl-api-ok', hint: 'kubectl exec -n shop deploy/web -- curl -s -m 3 http://api' }
        ] },
      { id: 'coredns-corefile', title: 'Every lookup fails: CoreDNS is crash-looping',
        goal: 'Name resolution fails in every namespace. Find out why CoreDNS will not stay up, fix its ConfigMap, and resolve api again.',
        setup: { selectorOk: true, targetPortOk: true, corefileOk: false, dnsEgress: true, fqdnOk: true },
        steps: [
          { label: 'From the debug pod, see lookups refused', event: 'dns-refused', hint: 'kubectl exec -n shop dnsutils -- nslookup api' },
          { label: 'See the CoreDNS pods in CrashLoopBackOff', event: 'coredns-pods-crash', hint: 'kubectl get pods -n kube-system -l k8s-app=kube-dns' },
          { label: 'Read why CoreDNS exits: a Corefile parse error', event: 'coredns-logs-parse-error', hint: 'kubectl logs -n kube-system -l k8s-app=kube-dns' },
          { label: 'Save the coredns ConfigMap to a file', event: 'corefile-exported', hint: 'kubectl get configmap coredns -n kube-system -o yaml > coredns.yaml' },
          { label: 'Fix the misspelt directive in the file', event: 'corefile-file-fixed', hint: "sed -i 's/forwrd/forward/' coredns.yaml" },
          { label: 'Apply the fixed ConfigMap', state: function (s) { return !!s.corefileOk; }, hint: 'kubectl apply -f coredns.yaml' },
          { label: 'api resolves again', event: 'dns-ok', hint: 'kubectl exec -n shop dnsutils -- nslookup api' }
        ] },
      { id: 'dns-egress', title: 'Lookups time out in one namespace only',
        goal: 'Pods in ns shop cannot resolve anything, while other namespaces can. Show that the network path works by IP, find the policy, and allow DNS.',
        setup: { selectorOk: true, targetPortOk: true, corefileOk: true, dnsEgress: false, fqdnOk: true },
        steps: [
          { label: 'From the debug pod, see the lookup time out', event: 'dns-timeout', hint: 'kubectl exec -n shop dnsutils -- nslookup api' },
          { label: 'Prove api answers by its ClusterIP (routing is fine)', event: 'curl-api-ip-ok', hint: 'kubectl exec -n shop deploy/web -- curl -s -m 3 http://10.96.88.20' },
          { label: 'Find the egress policy in ns shop and read what it allows', event: 'describe-netpol-deny-egress', hint: 'kubectl get networkpolicy -n shop  then  kubectl describe networkpolicy default-deny-egress -n shop' },
          { label: 'Allow egress to kube-dns on 53 (UDP and TCP)', state: function (s) { return !!s.dnsEgress; }, hint: 'kubectl apply -f allow-dns-egress.yaml' },
          { label: 'api resolves again', event: 'dns-ok', hint: 'kubectl exec -n shop dnsutils -- nslookup api' }
        ] },
      { id: 'cross-ns-fqdn', title: 'no such host: a short name across namespaces',
        goal: 'web logs “no such host” for its database, but CoreDNS is healthy. Work out what name the pod really asks for, find where db lives, and fix web’s DB_HOST.',
        setup: { selectorOk: true, targetPortOk: true, corefileOk: true, dnsEgress: true, fqdnOk: false },
        steps: [
          { label: 'Read web’s log: lookup db … no such host', event: 'web-logs-nxdomain', hint: 'kubectl logs -n shop deploy/web' },
          { label: 'Reproduce the NXDOMAIN from the debug pod', event: 'dns-nxdomain', hint: 'kubectl exec -n shop dnsutils -- nslookup db' },
          { label: 'Read the pod’s search list', event: 'resolv-conf', hint: 'kubectl exec -n shop dnsutils -- cat /etc/resolv.conf' },
          { label: 'Find which namespace Service db lives in', event: 'svc-db-found', hint: 'kubectl get svc -A' },
          { label: 'Give web a name that leaves its namespace', state: function (s) { return !!s.fqdnOk; }, hint: 'kubectl set env deployment/web -n shop DB_HOST=db.data.svc.cluster.local' },
          { label: 'web connects to the database', event: 'web-logs-ok', hint: 'kubectl logs -n shop deploy/web' }
        ] }
    ]
  };

  /* ── pack: CNI / pod networking (v1.6.0, 2026-10-27 — CKA Services & Networking 20% · Cluster Architecture 25%) ──
   * Drives cni-network on the authored cni-pod-network.glb: node-0 (control plane) and node-1 (worker); in ns default
   * deploy/client and web pod 0 on node-0, web pod 1 and both CoreDNS replicas on node-1; Service web = 10.96.45.12:80.
   * The CNI is Calico. ping / curl / nslookup run from deploy/client and are computed from ILImmersiveSims cniDecide.
   * Lab files stand in for the (much longer) real manifests and say so. kubectl get/patch ippool stands in for calicoctl
   * or the Calico API server (projectcalico.org/v3). */
  var CN_NOTE = 'Nodes: node-0 (control plane, 10.0.1.10) and node-1 (worker, 10.0.2.11) in VPC 10.0.0.0/16. ns default: deploy/client + one web pod on node-0, the other web pod + both CoreDNS pods on node-1; Service web = 10.96.45.12:80. Probe from the client: kubectl exec deploy/client -- ping|curl|nslookup. CNI = Calico; kubectl get/patch ippool stands in for calicoctl or the Calico API server (projectcalico.org/v3) — Calico\'s docs say not to edit crd.projectcalico.org objects directly. Lab files are trimmed stand-ins for the real manifests. Lab-only: fault cni none|calico · fault cidr overlap|distinct · fault kube-proxy off|on · fault coredns 0|2.';
  var CN_POD = { client: 'client-6b7f9d8c4-x2lq7', web0: 'web-5c8d7f6b9-k4m2p', web1: 'web-5c8d7f6b9-r7t9w', dns0: 'coredns-7c65d6cfc9-5qz8n', dns1: 'coredns-7c65d6cfc9-x8rwd' };
  var CN_CLUSTER_IP = '10.96.45.12';
  function cnIps(s) {
    var o = !!s.cidrOverlap, p = o ? '10.0.' : '192.168.';
    return { client: p + '10.4', web0: p + '10.5', web1: p + '77.3', dns0: p + '77.2', dns1: p + '77.4' };
  }
  function cnVars(ctx) { return ctx.vars.cn || (ctx.vars.cn = { newPool: false, oldDisabled: false, re: {} }); }
  var CN_CALICO = ['# lab excerpt (sim) — the real calico.yaml is several thousand lines; applying it here sets the drill\'s CNI state',
    'apiVersion: apps/v1', 'kind: DaemonSet', 'metadata:', '  name: calico-node', '  namespace: kube-system', 'spec:', '  template:', '    spec:', '      hostNetwork: true',
    '      initContainers:', '      - name: install-cni        # writes /etc/cni/net.d/10-calico.conflist on every node', '      containers:', '      - name: calico-node',
    '        env:', '        - name: CALICO_IPV4POOL_CIDR', '          value: "192.168.0.0/16"', '---', 'apiVersion: apps/v1', 'kind: Deployment', 'metadata:', '  name: calico-kube-controllers', '  namespace: kube-system'];
  var CN_NEW_POOL = ['apiVersion: projectcalico.org/v3', 'kind: IPPool', 'metadata:', '  name: new-pool', 'spec:', '  cidr: 192.168.0.0/16', '  ipipMode: Always', '  natOutgoing: true'];
  function cnPoolYaml(name, s, v) {
    var isNew = name === 'new-pool';
    return ['apiVersion: projectcalico.org/v3', 'kind: IPPool', 'metadata:', '  name: ' + name, 'spec:', '  blockSize: 26', '  cidr: ' + (isNew ? '192.168.0.0/16' : (s.cidrOverlap || v.oldDisabled ? '10.0.0.0/16' : '192.168.0.0/16')),
      '  disabled: ' + (!isNew && v.oldDisabled ? 'true' : 'false'), '  ipipMode: Always', '  natOutgoing: true', '  nodeSelector: all()'];
  }
  function cnPing(s, d, ip) {
    var I = cnIps(s), m = d.metrics, same = [I.client, I.web0].indexOf(ip) >= 0, cross = [I.web1, I.dns0, I.dns1].indexOf(ip) >= 0;
    var head = 'PING ' + ip + ' (' + ip + '): 56 data bytes', stat = '--- ' + ip + ' ping statistics ---';
    var lost = function (note, ev) { return res([head].concat(note ? [note] : []).concat(['', stat, '2 packets transmitted, 0 packets received, 100% packet loss', 'command terminated with exit code 1']), 1, null, ['ping'].concat(ev)); };
    if (ip === CN_CLUSTER_IP) return lost('(sim) a ClusterIP is a virtual IP: kube-proxy in iptables/nftables mode forwards only the Service\'s ports, so ICMP gets no reply — test a Service with curl', ['ping-clusterip']);
    if (!same && !cross) return lost('(sim) no pod in this lab has that IP — read them with kubectl get pods -o wide', ['ping-unknown']);
    var ok = same ? m.sameNode : m.crossNode;
    if (!ok) return lost(null, [same ? 'ping-same-fail' : 'ping-cross-fail']);
    var ttl = same ? 63 : 62;
    return res([head, '64 bytes from ' + ip + ': seq=0 ttl=' + ttl + ' time=' + (same ? '0.081' : '0.512') + ' ms', '64 bytes from ' + ip + ': seq=1 ttl=' + ttl + ' time=' + (same ? '0.074' : '0.468') + ' ms', '', stat,
      '2 packets transmitted, 2 packets received, 0% packet loss'], 0, null, ['ping', same ? 'ping-same-ok' : 'ping-cross-ok']);
  }
  function cnCurl(s, d, cmd) {
    var url = '';
    for (var ci = 1; ci < cmd.length; ci++) {
      if (/^(-m|--max-time|--connect-timeout|-o|--output|-H|--header|-w|--write-out|-X|-T|--timeout|-O)$/.test(cmd[ci])) { ci++; continue; }
      if (cmd[ci].charAt(0) !== '-') { url = cmd[ci]; break; }
    }
    var mm = /^(?:https?:\/\/)?([^\/:]+)(?::(\d+))?/.exec(url);
    if (!mm) return res(['curl: (3) URL rejected: No host part in the URL'], 3);
    var host = mm[1].toLowerCase(), port = mm[2] || '80', I = cnIps(s), m = d.metrics;
    var T = function (ev) { return res(['curl: (28) Connection timed out after 3002 milliseconds', 'command terminated with exit code 28'], 28, null, ['probe'].concat(ev)); };
    var ok = function (pod, ev) { return res(['{"service":"web","pod":"' + pod + '","ok":true}'], 0, null, ['probe'].concat(ev)); };
    if (port !== '80') return res(['sim: web listens on port 80 (Service web → targetPort 80)'], 2);
    if (/^web(\.default(\.svc(\.cluster\.local)?)?)?\.?$/.test(host)) {
      if (!m.dns) return res(['curl: (6) Could not resolve host: ' + host, 'command terminated with exit code 6'], 6, null, ['probe', 'curl-web-dns-fail']);
      return ok(CN_POD.web1, ['curl-web-name-ok']);
    }
    if (host === CN_CLUSTER_IP) {
      if (!m.clusterIp) return T(['curl-clusterip-fail']);
      if (!m.crossNode) return res(['curl: (28) Connection timed out after 3002 milliseconds', '(sim) kube-proxy picked the web pod on node-1 and cross-node traffic is broken; real requests succeed only when the node-0 pod is chosen', 'command terminated with exit code 28'], 28, null, ['probe', 'curl-clusterip-flaky']);
      return ok(CN_POD.web1, ['curl-clusterip-ok']);
    }
    if (host === I.web0 || host === I.web1) {
      var same = host === I.web0;
      if (!(same ? m.sameNode : m.crossNode)) return T(['curl-pod-fail']);
      return ok(same ? CN_POD.web0 : CN_POD.web1, ['curl-pod-ok']);
    }
    if (/^\d+\.\d+\.\d+\.\d+$/.test(host)) return res(['curl: (28) Connection timed out after 3002 milliseconds', '(sim) nothing in this lab serves HTTP on ' + host + ' — read IPs with kubectl get pods -o wide / kubectl get svc', 'command terminated with exit code 28'], 28, null, ['probe', 'curl-unknown']);
    return res(['sim: this drill probes Service web (http://web, http://' + CN_CLUSTER_IP + ') and the web pods by IP on port 80'], 2);
  }
  var cniPack = {
    sim: 'cni-network',
    prompt: 'student@node-0:~$',
    note: CN_NOTE,
    files: { 'calico.yaml': { yaml: CN_CALICO }, 'new-pool.yaml': { yaml: CN_NEW_POOL } },
    examples: ['kubectl get nodes', 'kubectl get nodes -o wide', 'kubectl describe node node-1', 'kubectl get pods -o wide', 'kubectl get pods -n kube-system -o wide', 'kubectl get daemonsets -n kube-system',
      'kubectl get deployments -n kube-system', 'ls /etc/cni/net.d', 'cat calico.yaml', 'kubectl get svc web', 'kubectl get endpointslices -l kubernetes.io/service-name=web',
      'kubectl exec deploy/client -- ping -c 2 ' + '192.168.77.3', 'kubectl exec deploy/client -- curl -s -m 3 http://web', 'kubectl exec deploy/client -- curl -s -m 3 http://' + CN_CLUSTER_IP,
      'kubectl exec deploy/client -- nslookup web', 'kubectl get ippools', 'kubectl get ippool default-ipv4-ippool -o yaml', 'fault kube-proxy off'],
    run: function (u, s, d, ctx) {
      var t = u.t, m = d.metrics, I = cnIps(s), v = cnVars(ctx);
      var f = faultArgs(t);
      if (f) {
        var FK = { 'cni': ['cniInstalled', 'calico', 'none'], 'cidr': ['cidrOverlap', 'overlap', 'distinct'], 'kube-proxy': ['kubeProxy', 'on', 'off'], 'coredns': ['corednsUp', '2', '0'] }[f[0]];
        if (!FK || (f[1] !== FK[1] && f[1] !== FK[2])) return res(['usage: fault cni none|calico · fault cidr overlap|distinct · fault kube-proxy off|on · fault coredns 0|2   (lab-only fault injection)'], 2);
        var fs = {}; fs[FK[0]] = f[1] === FK[1];
        if (FK[0] === 'cidrOverlap') ctx.vars.cn = null;
        return res(['[lab fault injection] ' + f.join(' ') + ' (simulated)'], 0, fs, ['fault']);
      }
      if (t[0] === 'ls' && /^\/etc\/cni\/net\.d\/?$/.test(t[t.length - 1] || '')) {
        return s.cniInstalled ? res(['10-calico.conflist  calico-kubeconfig'], 0, null, ['ls-cni', 'cni-conf-ok']) : res([], 0, null, ['ls-cni', 'cni-conf-empty']);
      }
      if (t[0] === 'cat' && /^\/etc\/cni\/net\.d\/10-calico\.conflist$/.test(t[1] || '')) {
        if (!s.cniInstalled) return res(['cat: ' + t[1] + ': No such file or directory'], 1);
        return res(['{', '  "name": "k8s-pod-network",', '  "cniVersion": "0.3.1",', '  "plugins": [', '    { "type": "calico", "ipam": { "type": "calico-ipam" }, "kubernetes": { "kubeconfig": "/etc/cni/net.d/calico-kubeconfig" } },',
          '    { "type": "portmap", "capabilities": { "portMappings": true } }', '  ]', '}'], 0, null, ['cat-cni-conf']);
      }
      var fr = fileRun(cniPack, t); if (fr) return fr;
      if (t[0] === 'kubeadm') {
        if (t[1] === 'init' && t[2] === 'phase' && t[3] === 'addon' && (t[4] === 'kube-proxy' || t[4] === 'coredns')) {
          var kp = t[4] === 'kube-proxy';
          return res(['[addons] Applied essential addon: ' + (kp ? 'kube-proxy' : 'CoreDNS')], 0, kp ? { kubeProxy: true } : { corednsUp: true }, ['kubeadm-addon', kp ? 'kubeadm-addon-kube-proxy' : 'kubeadm-addon-coredns']);
        }
        return res(['sim: this drill models `sudo kubeadm init phase addon kube-proxy|coredns` only (re-install an essential addon on a running cluster)'], 2);
      }
      if (t[0] === 'ping' || t[0] === 'curl' || t[0] === 'nslookup') return res(['sim: node-0 is not inside the pod network — run probes from a pod: kubectl exec deploy/client -- ' + t[0] + ' …'], 2, null, ['probe-wrong-place']);
      if (t[0] !== 'kubectl') return null;
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED.concat(['-c', '--container'])), ns = nsOf(t), out = flag(t, ['-o', '--output']);
      var kind = (args[0] || '').toLowerCase(), name = args[1] || '';
      if (/\//.test(kind)) { name = kind.split('/')[1]; kind = kind.split('/')[0]; }
      var ready = !!s.cniInstalled;
      if (verb === 'get' && /^(nodes?|no)$/.test(kind)) {
        var wide = out === 'wide';
        var hdr = ['NAME', 'STATUS', 'ROLES', 'AGE', 'VERSION'].concat(wide ? ['INTERNAL-IP', 'EXTERNAL-IP', 'OS-IMAGE', 'CONTAINER-RUNTIME'] : []);
        var rows = [hdr].concat([['node-0', 'control-plane', '10.0.1.10'], ['node-1', '<none>', '10.0.2.11']].filter(function (n) { return !name || n[0] === name; }).map(function (n) {
          return [n[0], ready ? 'Ready' : 'NotReady', n[1], '9d', 'v1.37.1'].concat(wide ? [n[2], '<none>', 'Ubuntu 24.04.1 LTS', 'containerd://1.7.22'] : []);
        }));
        return res(table(rows), 0, null, ['get-nodes', ready ? 'nodes-ready' : 'nodes-notready'].concat(wide ? ['nodes-wide'] : []));
      }
      if (verb === 'describe' && /^(nodes?|no)$/.test(kind)) {
        var nn = name || 'node-1';
        if (nn !== 'node-0' && nn !== 'node-1') return notFound('nodes', nn);
        var rd = ready ? ['  Ready            True    KubeletReady                 kubelet is posting ready status']
          : ['  Ready            False   KubeletNotReady              container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:Network plugin returns error: cni plugin not initialized'];
        return res(['Name:               ' + nn, 'Roles:              ' + (nn === 'node-0' ? 'control-plane' : '<none>'),
          'Taints:             ' + (ready ? (nn === 'node-0' ? 'node-role.kubernetes.io/control-plane:NoSchedule' : '<none>') : 'node.kubernetes.io/not-ready:NoSchedule'),
          'Conditions:', '  Type             Status  Reason                       Message', '  ----             ------  ------                       -------',
          '  MemoryPressure   False   KubeletHasSufficientMemory   kubelet has sufficient memory available', '  DiskPressure     False   KubeletHasNoDiskPressure     kubelet has no disk pressure'].concat(rd)
          .concat(['Addresses:', '  InternalIP:  ' + (nn === 'node-0' ? '10.0.1.10' : '10.0.2.11'), '  Hostname:    ' + nn]), 0, null, ['describe-node', ready ? 'describe-node-ready' : 'describe-node-cni']);
      }
      if (verb === 'get' && /^(pods?|po)$/.test(kind)) {
        var w = out === 'wide', all = ns === '*';
        var P = [];
        var podRow = function (pns, nm, ok, ip, node, pendingIfNoCni) {
          var pend = pendingIfNoCni && !ready;
          P.push([pns, nm, pend ? '0/1' : (ok ? '1/1' : '0/1'), pend ? 'Pending' : (ok ? 'Running' : 'Running'), '0', '9d', pend ? '<none>' : ip, pend ? '<none>' : node]);
        };
        if (all || ns === 'default') {
          podRow('default', CN_POD.client, true, I.client, 'node-0', true);
          podRow('default', CN_POD.web0, true, I.web0, 'node-0', true);
          podRow('default', CN_POD.web1, true, I.web1, 'node-1', true);
        }
        if (all || ns === 'kube-system') {
          if (s.corednsUp) { podRow('kube-system', CN_POD.dns0, true, I.dns0, 'node-1', true); podRow('kube-system', CN_POD.dns1, true, I.dns1, 'node-1', true); }
          if (ready) { P.push(['kube-system', 'calico-node-4tq8z', '1/1', 'Running', '0', '9d', '10.0.1.10', 'node-0'], ['kube-system', 'calico-node-9wv2c', '1/1', 'Running', '0', '9d', '10.0.2.11', 'node-1'], ['kube-system', 'calico-kube-controllers-6d8f7c-pq4lz', '1/1', 'Running', '0', '9d', I.dns0.replace(/\.2$/, '.6'), 'node-1']); }
          P.push(['kube-system', 'etcd-node-0', '1/1', 'Running', '0', '9d', '10.0.1.10', 'node-0'], ['kube-system', 'kube-apiserver-node-0', '1/1', 'Running', '0', '9d', '10.0.1.10', 'node-0'],
            ['kube-system', 'kube-controller-manager-node-0', '1/1', 'Running', '0', '9d', '10.0.1.10', 'node-0'], ['kube-system', 'kube-scheduler-node-0', '1/1', 'Running', '0', '9d', '10.0.1.10', 'node-0']);
          if (s.kubeProxy) P.push(['kube-system', 'kube-proxy-7m2kd', '1/1', 'Running', '0', '9d', '10.0.1.10', 'node-0'], ['kube-system', 'kube-proxy-q8z4n', '1/1', 'Running', '0', '9d', '10.0.2.11', 'node-1']);
        }
        if (!P.length) return res(['No resources found in ' + ns + ' namespace.'], 0);
        var H = (all ? ['NAMESPACE'] : []).concat(['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE']).concat(w ? ['IP', 'NODE'] : []);
        var tb = [H].concat(P.map(function (r) { return (all ? [r[0]] : []).concat(r.slice(1, 6)).concat(w ? r.slice(6) : []); }));
        var ev = ['get-pods'];
        if (all || ns === 'kube-system') ev.push(!s.corednsUp ? 'coredns-absent' : (ready ? 'coredns-running' : 'coredns-pending'));
        if (w) ev.push('pods-wide');
        return res(table(tb), 0, null, ev);
      }
      if (verb === 'get' && /^(ds|daemonsets?(\.apps)?)$/.test(kind)) {
        var D = [];
        if (ready) D.push(['kube-system', 'calico-node', '2', '2', '2', '2', '2', 'kubernetes.io/os=linux', '9d']);
        if (s.kubeProxy) D.push(['kube-system', 'kube-proxy', '2', '2', '2', '2', '2', 'kubernetes.io/os=linux', '9d']);
        if (ns !== '*' && ns !== 'kube-system') return res(['No resources found in ' + ns + ' namespace.'], 0, null, ['get-ds-none']);
        var dall = ns === '*';
        if (!D.length) return res(['No resources found in kube-system namespace.'], 0, null, ['get-ds', 'ds-no-cni', 'ds-no-kube-proxy']);
        var DH = (dall ? ['NAMESPACE'] : []).concat(['NAME', 'DESIRED', 'CURRENT', 'READY', 'UP-TO-DATE', 'AVAILABLE', 'NODE SELECTOR', 'AGE']);
        return res(table([DH].concat(D.map(function (r) { return dall ? r : r.slice(1); }))), 0, null, ['get-ds'].concat(ready ? [] : ['ds-no-cni']).concat(s.kubeProxy ? [] : ['ds-no-kube-proxy']));
      }
      if (verb === 'get' && /^(deploy|deployments?(\.apps)?)$/.test(kind)) {
        if (ns === 'default') return res(table([['NAME', 'READY', 'UP-TO-DATE', 'AVAILABLE', 'AGE'], ['client', ready ? '1/1' : '0/1', '1', ready ? '1' : '0', '9d'], ['web', ready ? '2/2' : '0/2', '2', ready ? '2' : '0', '9d']]), 0, null, ['get-deploy']);
        if (ns !== 'kube-system') return res(['No resources found in ' + ns + ' namespace.'], 0);
        var dr = [['NAME', 'READY', 'UP-TO-DATE', 'AVAILABLE', 'AGE'], ['coredns', s.corednsUp ? (ready ? '2/2' : '0/2') : '0/0', s.corednsUp ? '2' : '0', s.corednsUp && ready ? '2' : '0', '9d']];
        if (ready) dr.push(['calico-kube-controllers', '1/1', '1', '1', '9d']);
        return res(table(dr), 0, null, ['get-deploy', s.corednsUp ? 'coredns-deploy' : 'coredns-scaled-zero']);
      }
      if (verb === 'scale') {
        var rep = flag(t, ['--replicas']), tg = name || '';
        if (!/^(deploy|deployments?(\.apps)?)$/.test(kind) || tg !== 'coredns' || ns !== 'kube-system' || rep === null || !/^\d+$/.test(String(rep))) return res(['sim: this drill models `kubectl scale deployment coredns -n kube-system --replicas=N`'], 2);
        return res(['deployment.apps/coredns scaled'], 0, { corednsUp: +rep > 0 }, ['scale-coredns']);
      }
      if (verb === 'get' && /^(svc|services?)$/.test(kind)) {
        if (ns !== 'default' || (name && name !== 'web')) return name ? notFound('services', name) : res(['sim: this drill models Service web in ns default'], 2);
        return res(table([['NAME', 'TYPE', 'CLUSTER-IP', 'EXTERNAL-IP', 'PORT(S)', 'AGE'], ['web', 'ClusterIP', CN_CLUSTER_IP, '<none>', '80/TCP', '9d']]), 0, null, ['get-svc']);
      }
      if (verb === 'get' && /^(endpointslices?(\.discovery\.k8s\.io)?)$/.test(kind)) {
        return res(table([['NAME', 'ADDRESSTYPE', 'PORTS', 'ENDPOINTS', 'AGE'], ['web-9x7kq', 'IPv4', ready ? '80' : '<unset>', ready ? I.web0 + ',' + I.web1 : '<unset>', '9d']]), 0, null, ['eps-web']);
      }
      if (/^(ippools?(\.projectcalico\.org|\.crd\.projectcalico\.org)?)$/.test(kind)) {
        if (!ready) return res(['error: the server doesn\'t have a resource type "' + kind + '"'], 1);
        var pools = ['default-ipv4-ippool'].concat(v.newPool ? ['new-pool'] : []);
        if (verb === 'get') {
          if (name && pools.indexOf(name) < 0) return notFound('ippools.projectcalico.org', name);
          if (out === 'yaml') {
            var nm = name || pools[0];
            var py = cnPoolYaml(nm, s, v);
            return res(py, 0, null, ['ippool-yaml', nm === 'default-ipv4-ippool' && /10\.0\.0\.0\/16/.test(py.join('\n')) ? 'ippool-overlap' : 'ippool-ok']);
          }
          return res(table([['NAME', 'CREATED AT']].concat(pools.filter(function (p) { return !name || p === name; }).map(function (p) { return [p, p === 'new-pool' ? '2026-10-27T13:05:12Z' : '2026-10-18T09:12:40Z']; }))), 0, null, ['get-ippools']);
        }
        if (verb === 'patch') {
          if (name !== 'default-ipv4-ippool') return name && pools.indexOf(name) >= 0 ? res(['sim: this drill models disabling default-ipv4-ippool'], 2) : notFound('ippools.projectcalico.org', name);
          var j = jsonArg(t); if (j.err) return j.err;
          var dis = j.v && j.v.spec && j.v.spec.disabled;
          if (dis !== true) return res(['sim: this drill models {"spec":{"disabled":true}} on default-ipv4-ippool (stop allocating from it; existing pods keep their IPs)'], 2);
          if (!v.newPool) return res(['ippool.projectcalico.org/default-ipv4-ippool patched', '(sim) with no other enabled pool, new pods cannot get an IP — create the replacement pool first'], 0, null, ['ippool-disabled-early']);
          v.oldDisabled = true;
          return res(['ippool.projectcalico.org/default-ipv4-ippool patched'], 0, null, ['ippool-old-disabled']);
        }
      }
      if (verb === 'apply' || (verb === 'create' && hasFlag(t, ['-f', '--filename']))) {
        var a = applyFile(cniPack, t); if (a.err) return a.err;
        if (a.name === 'calico.yaml') {
          return res(['serviceaccount/calico-node ' + (ready ? 'unchanged' : 'created'), 'customresourcedefinition.apiextensions.k8s.io/ippools.crd.projectcalico.org ' + (ready ? 'unchanged' : 'created'),
            'daemonset.apps/calico-node ' + (ready ? 'unchanged' : 'created'), 'deployment.apps/calico-kube-controllers ' + (ready ? 'unchanged' : 'created'),
            '(sim) output trimmed — the lab excerpt stands in for the full manifest; calico-node writes /etc/cni/net.d/10-calico.conflist on each node'], 0, ready ? null : { cniInstalled: true }, ['apply-calico']);
        }
        if (!ready) return res(['error: resource mapping not found for name: "new-pool" namespace: "" from "new-pool.yaml": no matches for kind "IPPool" in version "projectcalico.org/v3"', 'ensure CRDs are installed first'], 1);
        var was = v.newPool; v.newPool = true;
        return res(['ippool.projectcalico.org/new-pool ' + (was ? 'unchanged' : 'created')], 0, null, ['ippool-new-created']);
      }
      if (verb === 'rollout' && args[0] === 'restart') {
        var rk = (args[1] || '').toLowerCase(), rn = args[2] || '';
        if (/\//.test(rk)) { rn = rk.split('/')[1]; rk = rk.split('/')[0]; }
        if (!/^(deploy|deployments?(\.apps)?)$/.test(rk)) return res(['sim: this drill models `kubectl rollout restart deployment [NAME]`'], 2);
        var targets = ns === 'kube-system' ? (rn ? (rn === 'coredns' ? ['coredns'] : []) : ['coredns', 'calico-kube-controllers']) : (ns === 'default' ? (rn ? ([ 'client', 'web'].indexOf(rn) >= 0 ? [rn] : []) : ['client', 'web']) : []);
        if (!targets.length) return notFound('deployments.apps', rn || '(none in ' + ns + ')');
        var fixed = v.newPool && v.oldDisabled;
        targets.forEach(function (x) { if (fixed) v.re[x] = true; });
        var L = targets.map(function (x) { return 'deployment.apps/' + x + ' restarted'; });
        var patch = null, evr = ['rollout-restart'];
        if (s.cidrOverlap) {
          if (!fixed) L.push('(sim) the new pods still get addresses from default-ipv4-ippool (10.0.0.0/16) — nothing changed');
          else if (v.re.client && v.re.web && v.re.coredns) { patch = { cidrOverlap: false }; L.push('(sim) every pod in the drill now has an address from new-pool (192.168.0.0/16)'); evr.push('pods-reip'); }
          else L.push('(sim) these pods now use new-pool; still on the old range: ' + ['client', 'web', 'coredns'].filter(function (x) { return !v.re[x]; }).join(', '));
        }
        return res(L, 0, patch, evr);
      }
      var ex = execArgs(t);
      if (ex) {
        if (!ex.hasDd || !ex.cmd.length) return res(['error: you must specify at least one command for the container (kubectl exec … -- CMD)'], 1);
        if (ex.ns !== 'default' || !(ex.target === 'client' || ex.target === CN_POD.client)) return res(['Error from server (NotFound): pods "' + ex.target + '" not found (sim: probe from deploy/client in ns default)'], 1, null, ['not-found']);
        if (!ready) return res(['Error from server (BadRequest): pod ' + CN_POD.client + ' does not have a host assigned'], 1, null, ['exec-pending']);
        var bin = ex.cmd[0];
        if (bin === 'ping') { var ip = ex.cmd.filter(function (a, i) { return a.charAt(0) !== '-' && i > 0 && !/^-[cwW]$/.test(ex.cmd[i - 1]); })[0]; return ip ? cnPing(s, d, ip) : res(['ping: usage error: Destination address required'], 1); }
        if (bin === 'curl' || bin === 'wget') return cnCurl(s, d, ex.cmd);
        if (bin === 'nslookup') {
          var q = ex.cmd[ex.cmd.length - 1];
          if (!/^(web|kubernetes)(\.default(\.svc(\.cluster\.local)?)?)?\.?$/.test(q)) return res(['sim: this lab resolves web and kubernetes.default only'], 2);
          if (!m.dns) return res([';; connection timed out; no servers could be reached', '', 'command terminated with exit code 1'], 1, null, ['dns', 'dns-fail']);
          var web = /^web/.test(q);
          return res(['Server:\t\t10.96.0.10', 'Address:\t10.96.0.10:53', '', 'Name:\t' + (web ? 'web' : 'kubernetes') + '.default.svc.cluster.local', 'Address: ' + (web ? CN_CLUSTER_IP : '10.96.0.1')], 0, null, ['dns', 'dns-ok']);
        }
        return res(['sim: inside deploy/client this drill models ping, curl / wget and nslookup'], 2);
      }
      return unmodelled(t.join(' '), cniPack.examples);
    },
    tasks: [
      { id: 'no-cni', title: 'Fresh cluster, every node NotReady',
        goal: 'kubeadm init and join finished, but both nodes are NotReady and CoreDNS will not start. Find the missing piece, install it, and get the nodes and CoreDNS up.',
        setup: { cniInstalled: false, cidrOverlap: false, kubeProxy: true, corednsUp: true },
        steps: [
          { label: 'See both nodes NotReady', event: 'nodes-notready', hint: 'kubectl get nodes' },
          { label: 'See CoreDNS stuck in Pending', event: 'coredns-pending', hint: 'kubectl get pods -n kube-system' },
          { label: 'Read the Ready condition: the network plugin is not ready', event: 'describe-node-cni', hint: 'kubectl describe node node-1' },
          { label: 'Confirm the CNI config directory is empty', event: 'cni-conf-empty', hint: 'ls /etc/cni/net.d' },
          { label: 'Install a CNI plugin (Calico)', state: function (s) { return !!s.cniInstalled; }, hint: 'kubectl apply -f calico.yaml' },
          { label: 'Both nodes are Ready', event: 'nodes-ready', hint: 'kubectl get nodes' },
          { label: 'CoreDNS is Running', event: 'coredns-running', hint: 'kubectl get pods -n kube-system' }
        ] },
      { id: 'cidr-overlap', title: 'Same node works, cross-node does not',
        goal: 'Pods on the same node reach each other, but nothing crosses to node-1. Find out why the pod addresses are the problem and move the pods to a pool that does not overlap the VPC, the way Calico documents it.',
        setup: { cniInstalled: true, cidrOverlap: true, kubeProxy: true, corednsUp: true },
        steps: [
          { label: 'Ping the web pod on node-1 from the client: no reply', event: 'ping-cross-fail', hint: 'kubectl exec deploy/client -- ping -c 2 10.0.77.3' },
          { label: 'Ping the web pod on the same node: it answers', event: 'ping-same-ok', hint: 'kubectl exec deploy/client -- ping -c 2 10.0.10.5' },
          { label: 'Compare the node addresses with the pod addresses', event: 'nodes-wide', hint: 'kubectl get nodes -o wide' },
          { label: 'Read the IP pool: 10.0.0.0/16, the same range as the VPC', event: 'ippool-overlap', hint: 'kubectl get ippool default-ipv4-ippool -o yaml' },
          { label: 'Create a replacement pool that does not overlap', event: 'ippool-new-created', hint: 'kubectl apply -f new-pool.yaml' },
          { label: 'Stop allocating from the old pool', event: 'ippool-old-disabled', hint: 'kubectl patch ippool default-ipv4-ippool --type merge -p \'{"spec":{"disabled":true}}\'' },
          { label: 'Recreate the pods so they get new addresses', state: function (s) { return !s.cidrOverlap; }, hint: 'kubectl rollout restart deployment  then  kubectl rollout restart deployment coredns -n kube-system' },
          { label: 'Cross-node ping works', event: 'ping-cross-ok', hint: 'kubectl exec deploy/client -- ping -c 2 192.168.77.3' }
        ] },
      { id: 'no-kube-proxy', title: 'Pod IPs work, Services do not',
        goal: 'The client cannot reach Service web by name or by ClusterIP, yet the pods answer on their own IPs. Find which component should program the Service and restore it.',
        setup: { cniInstalled: true, cidrOverlap: false, kubeProxy: false, corednsUp: true },
        steps: [
          { label: 'curl web by name: the name does not resolve', event: 'curl-web-dns-fail', hint: 'kubectl exec deploy/client -- curl -s -m 3 http://web' },
          { label: 'curl a web pod by its own IP: it answers', event: 'curl-pod-ok', hint: 'kubectl exec deploy/client -- curl -s -m 3 http://192.168.77.3' },
          { label: 'curl the ClusterIP: it times out', event: 'curl-clusterip-fail', hint: 'kubectl exec deploy/client -- curl -s -m 3 http://10.96.45.12' },
          { label: 'Find what is missing among the node DaemonSets', event: 'ds-no-kube-proxy', hint: 'kubectl get daemonsets -n kube-system' },
          { label: 'Re-install the kube-proxy addon', state: function (s) { return !!s.kubeProxy; }, hint: 'sudo kubeadm init phase addon kube-proxy' },
          { label: 'The ClusterIP answers', event: 'curl-clusterip-ok', hint: 'kubectl exec deploy/client -- curl -s -m 3 http://10.96.45.12' },
          { label: 'web answers by name again', event: 'curl-web-name-ok', hint: 'kubectl exec deploy/client -- curl -s -m 3 http://web' }
        ] }
    ]
  };

  /* ── pack: service mesh mTLS (v1.6.0, 2026-10-27 — Istio semantics; optional CKA+ / ICA, not graded on the CKA paper) ──
   * Drives mesh-mtls on the authored service-mesh-sidecar.glb: app-0 = deploy/frontend in ns shop (the client), app-1 =
   * deploy/payments in ns payments (already meshed; PeerAuthentication "default" in its namespace), istiod in ns
   * istio-system. payments echoes request headers like httpbin /headers, so X-Forwarded-Client-Cert (set by the server
   * sidecar only for mTLS peers) shows whether the hop was mTLS. Outcomes come from ILImmersiveSims meshDecide. */
  var MS_NOTE = 'Namespaces: shop (deploy/frontend, the client) · payments (deploy/payments, already meshed, PeerAuthentication default) · istio-system (istiod). payments echoes request headers like httpbin /headers: X-Forwarded-Client-Cert is present only when the hop was mTLS. Sidecar injection is the istio-sidecar-injector mutating webhook (namespace label istio-injection=enabled). istioctl output is computed and trimmed, not byte-identical. Istio semantics, not CKA core. No live mesh, no real Envoy or istiod.';
  var MS_CURL = 'kubectl exec -n shop deploy/frontend -- curl -s -m 3 http://payments.payments:8080/headers';
  var MS_PODS = { old: ['frontend-7d9c8b6f5-kq2xz', 'frontend-7d9c8b6f5-m8wpl'], neu: ['frontend-6f4b9c7d8-2vnrt', 'frontend-6f4b9c7d8-h5xjq'], pay: ['payments-58c7d9f6b-4tlwq', 'payments-58c7d9f6b-zr6kp'], istiod: 'istiod-5d8f8b6c9-x7k2p' };
  function msPa(mode) { return ['apiVersion: security.istio.io/v1', 'kind: PeerAuthentication', 'metadata:', '  name: default', '  namespace: payments', 'spec:', '  mtls:', '    mode: ' + mode]; }
  var MS_WEBHOOK = 'Error creating: Internal error occurred: failed calling webhook "namespace.sidecar-injector.istio.io": failed to call webhook: Post "https://istiod.istio-system.svc:443/inject?timeout=10s": no endpoints available for service "istiod"';
  var meshPack = {
    sim: 'mesh-mtls',
    prompt: 'student@controlplane:~$',
    note: MS_NOTE,
    files: { 'pa-strict.yaml': { yaml: msPa('STRICT'), set: { strict: true } }, 'pa-permissive.yaml': { yaml: msPa('PERMISSIVE'), set: { strict: false } } },
    examples: ['kubectl get namespace shop --show-labels', 'kubectl get namespaces -L istio-injection', 'kubectl get pods -n shop', 'kubectl get pods -n payments', 'kubectl get peerauthentication -n payments',
      'kubectl get peerauthentication default -n payments -o yaml', 'cat pa-strict.yaml', MS_CURL, 'kubectl get events -n shop', 'kubectl rollout status deployment/frontend -n shop',
      'kubectl get deployments -n istio-system', 'istioctl proxy-status'],
    run: function (u, s, d, ctx) {
      var t = u.t, m = d.metrics;
      var fr = fileRun(meshPack, t); if (fr) return fr;
      if (t[0] === 'istioctl') {
        if (t[1] === 'proxy-status' || t[1] === 'ps') {
          if (!s.cpUp) return res(['Error: unable to find any Istiod instances'], 1, null, ['proxy-status', 'proxy-status-no-istiod']);
          var rows = [['NAME', 'CLUSTER', 'CDS', 'LDS', 'EDS', 'RDS', 'ISTIOD']];
          if (m.clientSidecar) MS_PODS.neu.forEach(function (p) { rows.push([p + '.shop', 'Kubernetes', 'SYNCED', 'SYNCED', 'SYNCED', 'SYNCED', MS_PODS.istiod]); });
          MS_PODS.pay.forEach(function (p) { rows.push([p + '.payments', 'Kubernetes', 'SYNCED', 'SYNCED', 'SYNCED', 'SYNCED', MS_PODS.istiod]); });
          return res(table(rows).concat(['(sim) computed from the drill state; columns trimmed']), 0, null, ['proxy-status', 'proxy-status-synced'].concat(m.clientSidecar ? ['proxy-status-frontend'] : []));
        }
        return res(['sim: this drill models `istioctl proxy-status` only'], 2);
      }
      if (t[0] === 'curl') return res(['sim: controlplane is outside the mesh — probe from the client: ' + MS_CURL], 2, null, ['probe-wrong-place']);
      if (t[0] !== 'kubectl') return null;
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED.concat(['-L', '--label-columns', '-c', '--container'])), ns = nsOf(t), out = flag(t, ['-o', '--output']);
      var kind = (args[0] || '').toLowerCase(), name = args[1] || '';
      if (/\//.test(kind)) { name = kind.split('/')[1]; kind = kind.split('/')[0]; }
      var pending = !!ctx.vars.msPending;
      if (verb === 'get' && /^(ns|namespaces?)$/.test(kind)) {
        var showL = hasFlag(t, '--show-labels'), lc = flag(t, ['-L', '--label-columns']);
        var NS = [['default', ''], ['istio-system', ''], ['payments', 'istio-injection=enabled'], ['shop', s.nsLabeled ? 'istio-injection=enabled' : '']].filter(function (r) { return !name || r[0] === name; });
        if (!NS.length) return notFound('namespaces', name);
        var hdr = ['NAME', 'STATUS', 'AGE'].concat(showL ? ['LABELS'] : []).concat(lc === 'istio-injection' ? ['ISTIO-INJECTION'] : []);
        var tb = [hdr].concat(NS.map(function (r) {
          var labels = ['kubernetes.io/metadata.name=' + r[0]].concat(r[1] ? [r[1]] : []).join(',');
          return [r[0], 'Active', '21d'].concat(showL ? [labels] : []).concat(lc === 'istio-injection' ? [r[1] ? 'enabled' : ''] : []);
        }));
        var ev = ['get-ns'];
        if ((showL || lc === 'istio-injection') && NS.some(function (r) { return r[0] === 'shop'; })) ev.push(s.nsLabeled ? 'ns-shop-inject' : 'ns-shop-noinject');
        return res(table(tb), 0, null, ev);
      }
      if (verb === 'label' && /^(ns|namespaces?)$/.test(kind)) {
        var kv = args.slice(1).filter(function (a) { return /^istio-injection/.test(a); })[0] || '';
        if (name !== 'shop') return name === 'payments' ? res(['namespace/payments not labeled'], 0) : (name ? notFound('namespaces', name) : res(['error: one or more resources must be specified as <resource> <name>'], 1));
        if (kv === 'istio-injection=enabled') {
          if (s.nsLabeled) return res(['namespace/shop not labeled'], 0, null, ['label-ns']);
          return res(['namespace/shop labeled'], 0, { nsLabeled: true, restarted: false }, ['label-ns', 'label-ns-inject']);
        }
        if (kv === 'istio-injection-' || /^istio-injection=/.test(kv)) return res(['sim: only enabling injection is modelled — removing or changing the label never strips sidecars from running pods (they keep them until recreated)'], 2);
        return res(['sim: this drill models `kubectl label namespace shop istio-injection=enabled`'], 2);
      }
      if (verb === 'get' && /^(pods?|po)$/.test(kind)) {
        var P = [], all = ns === '*';
        if (all || ns === 'shop') {
          var fp = s.restarted ? MS_PODS.neu : MS_PODS.old, sc = m.clientSidecar;
          fp.forEach(function (p) { P.push(['shop', p, sc ? '2/2' : '1/1', 'Running', '0', s.restarted ? '4m' : '3d']); });
        }
        if (all || ns === 'payments') MS_PODS.pay.forEach(function (p) { P.push(['payments', p, '2/2', 'Running', '0', '3d']); });
        if ((all || ns === 'istio-system') && s.cpUp) P.push(['istio-system', MS_PODS.istiod, '1/1', 'Running', '0', '21d']);
        if (!P.length) return res(['No resources found in ' + ns + ' namespace.'], 0, null, ['get-pods']);
        var H = (all ? ['NAMESPACE'] : []).concat(['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE']);
        var ev2 = ['get-pods'];
        if (all || ns === 'shop') ev2.push(m.clientSidecar ? 'pods-frontend-sidecar' : 'pods-frontend-nosidecar');
        return res(table([H].concat(P.map(function (r) { return all ? r : r.slice(1); }))), 0, null, ev2);
      }
      if (verb === 'rollout' && (args[0] === 'restart' || args[0] === 'status')) {
        var rk = (args[1] || '').toLowerCase(), rn = args[2] || '';
        if (/\//.test(rk)) { rn = rk.split('/')[1]; rk = rk.split('/')[0]; }
        if (!/^(deploy|deployments?(\.apps)?)$/.test(rk) || rn !== 'frontend' || ns !== 'shop') return (rn && rn !== 'frontend') || (rn === 'frontend' && ns !== 'shop') ? notFound('deployments.apps', rn) : res(['sim: this drill models `kubectl rollout restart|status deployment/frontend -n shop`'], 2);
        if (args[0] === 'status') {
          if (pending) return res(['Waiting for deployment "frontend" rollout to finish: 0 out of 2 new replicas have been updated...', '(sim) a real rollout status keeps waiting here; the sim stops'], 0, null, ['rollout-status', 'rollout-waiting']);
          return res(['deployment "frontend" successfully rolled out'], 0, null, ['rollout-status', 'rollout-done']);
        }
        if (s.nsLabeled && !s.cpUp) {
          ctx.vars.msPending = true;
          return res(['deployment.apps/frontend restarted'], 0, null, ['rollout-restart', 'rollout-blocked']);
        }
        ctx.vars.msPending = false;
        return res(['deployment.apps/frontend restarted'], 0, { restarted: !!s.nsLabeled }, ['rollout-restart', s.nsLabeled ? 'rollout-injected' : 'rollout-plain']);
      }
      if (verb === 'get' && /^(events?|ev)$/.test(kind)) {
        if (ns !== 'shop' || !pending) return res(['No events found in ' + (ns === '*' ? 'any' : ns) + ' namespace.'], 0, null, ['get-events']);
        return res(table([['LAST SEEN', 'TYPE', 'REASON', 'OBJECT', 'MESSAGE'], ['12s', 'Warning', 'FailedCreate', 'replicaset/frontend-6f4b9c7d8', MS_WEBHOOK]]), 0, null, ['get-events', 'inject-webhook-fail']);
      }
      if (/^(peerauthentications?(\.security\.istio\.io)?|pa)$/.test(kind)) {
        var mode = s.strict ? 'STRICT' : 'PERMISSIVE';
        if (verb === 'get' || verb === 'describe') {
          if (ns !== 'payments' && ns !== '*') return res(['No resources found in ' + ns + ' namespace.'], 0, null, ['get-pa-none']);
          if (name && name !== 'default') return notFound('peerauthentications.security.istio.io', name);
          if (out === 'yaml' || verb === 'describe') return res(msPa(mode), 0, null, ['get-pa', 'pa-' + mode.toLowerCase()]);
          var ph = (ns === '*' ? ['NAMESPACE'] : []).concat(['NAME', 'MODE', 'AGE']);
          return res(table([ph, (ns === '*' ? ['payments'] : []).concat(['default', mode, '21d'])]), 0, null, ['get-pa', 'pa-' + mode.toLowerCase()]);
        }
      }
      if (verb === 'apply' || (verb === 'create' && hasFlag(t, ['-f', '--filename']))) {
        var a = applyFile(meshPack, t); if (a.err) return a.err;
        var same = !!s.strict === a.f.set.strict;
        if (verb === 'create') return res(['Error from server (AlreadyExists): error when creating "' + a.name + '": peerauthentications.security.istio.io "default" already exists'], 1);
        return res(['peerauthentication.security.istio.io/default ' + (same ? 'unchanged' : 'configured')], 0, same ? null : a.f.set, ['apply-pa', a.f.set.strict ? 'apply-pa-strict' : 'apply-pa-permissive']);
      }
      if (verb === 'get' && /^(deploy|deployments?(\.apps)?)$/.test(kind)) {
        var rowsD = { shop: [['frontend', '2/2', pending ? '0' : '2', '2', '21d']], payments: [['payments', '2/2', '2', '2', '21d']], 'istio-system': [['istiod', s.cpUp ? '1/1' : '0/0', s.cpUp ? '1' : '0', s.cpUp ? '1' : '0', '21d']] }[ns];
        if (!rowsD) return res(['No resources found in ' + ns + ' namespace.'], 0);
        return res(table([['NAME', 'READY', 'UP-TO-DATE', 'AVAILABLE', 'AGE']].concat(rowsD)), 0, null, ['get-deploy'].concat(ns === 'istio-system' ? [s.cpUp ? 'istiod-up' : 'istiod-scaled-zero'] : []));
      }
      if (verb === 'scale') {
        var rep = flag(t, ['--replicas']);
        if (!/^(deploy|deployments?(\.apps)?)$/.test(kind) || name !== 'istiod' || ns !== 'istio-system' || rep === null || !/^\d+$/.test(String(rep))) return res(['sim: this drill models `kubectl scale deployment istiod -n istio-system --replicas=N`'], 2);
        var up = +rep > 0, L = ['deployment.apps/istiod scaled'], patch = { cpUp: up };
        if (up && pending) { ctx.vars.msPending = false; patch.restarted = true; L.push('(sim) the injection webhook has endpoints again; the ReplicaSet controller retries and the new frontend pods are created with sidecars'); }
        return res(L, 0, patch, ['scale-istiod', up ? 'istiod-scaled-up' : 'istiod-scaled-down']);
      }
      var ex = execArgs(t);
      if (ex) {
        if (!ex.hasDd || !ex.cmd.length) return res(['error: you must specify at least one command for the container (kubectl exec … -- CMD)'], 1);
        if (ex.ns !== 'shop' || ex.target.indexOf('frontend') !== 0) return res(['Error from server (NotFound): pods "' + ex.target + '" not found (sim: probe from deploy/frontend in ns shop)'], 1, null, ['not-found']);
        if (ex.cmd[0] !== 'curl') return res(['sim: inside deploy/frontend this drill models curl to http://payments.payments:8080/headers'], 2);
        var url = ex.cmd.filter(function (x) { return /payments/.test(x) && x.charAt(0) !== '-'; })[0] || '';
        if (!/^(https?:\/\/)?payments(\.payments(\.svc(\.cluster\.local)?)?)?:8080(\/headers)?\/?$/.test(url)) return res(['sim: this drill probes http://payments.payments:8080/headers (payments echoes request headers)'], 2);
        if (!m.accepted) return res(['curl: (56) Recv failure: Connection reset by peer', 'command terminated with exit code 56'], 56, null, ['probe', 'curl-payments-reset']);
        var H2 = ['{', '  "headers": {', '    "Accept": "*/*",', '    "Host": "payments.payments:8080",', '    "User-Agent": "curl/8.10.1"'];
        if (m.transport === 'mTLS') { H2[4] += ','; H2.push('    "X-Forwarded-Client-Cert": "By=spiffe://cluster.local/ns/payments/sa/payments;Hash=<sha256 of the client cert>;Subject=\\"\\";URI=spiffe://cluster.local/ns/shop/sa/frontend"'); }
        H2.push('  }', '}');
        return res(H2, 0, null, ['probe', m.transport === 'mTLS' ? 'curl-payments-mtls' : 'curl-payments-plain']);
      }
      return unmodelled(t.join(' '), meshPack.examples);
    },
    tasks: [
      { id: 'strict-reset', title: 'Connection reset by peer under STRICT',
        goal: 'frontend → payments fails with a reset. payments is meshed and requires mTLS; frontend is not. Prove why, mesh frontend the way injection really works, and get an mTLS call through.',
        setup: { nsLabeled: false, restarted: false, strict: true, cpUp: true },
        steps: [
          { label: 'Reproduce it: the call is reset', event: 'curl-payments-reset', hint: MS_CURL },
          { label: 'Read payments’ PeerAuthentication: STRICT', event: 'pa-strict', hint: 'kubectl get peerauthentication -n payments' },
          { label: 'See the frontend pods have one container (no sidecar)', event: 'pods-frontend-nosidecar', hint: 'kubectl get pods -n shop' },
          { label: 'See ns shop has no injection label', event: 'ns-shop-noinject', hint: 'kubectl get namespace shop --show-labels' },
          { label: 'Enable sidecar injection for ns shop', state: function (s) { return !!s.nsLabeled; }, hint: 'kubectl label namespace shop istio-injection=enabled' },
          { label: 'Recreate the frontend pods so the webhook injects them', state: function (s) { return !!s.nsLabeled && !!s.restarted; }, hint: 'kubectl rollout restart deployment/frontend -n shop' },
          { label: 'The call goes through over mTLS (client cert header present)', event: 'curl-payments-mtls', hint: MS_CURL }
        ] },
      { id: 'permissive-to-strict', title: 'Migrate payments from PERMISSIVE to STRICT without an outage',
        goal: 'payments accepts plaintext today. Show that frontend’s calls are plaintext, mesh frontend first, prove the hop is mTLS, and only then lock payments to STRICT.',
        setup: { nsLabeled: false, restarted: false, strict: false, cpUp: true },
        steps: [
          { label: 'The call works, but with no client certificate header (plaintext)', event: 'curl-payments-plain', hint: MS_CURL },
          { label: 'Read payments’ PeerAuthentication: PERMISSIVE', event: 'pa-permissive', hint: 'kubectl get peerauthentication -n payments' },
          { label: 'Mesh frontend: enable injection, then recreate its pods', state: function (s) { return !!s.nsLabeled && !!s.restarted; }, hint: 'kubectl label namespace shop istio-injection=enabled  then  kubectl rollout restart deployment/frontend -n shop' },
          { label: 'The frontend pods now run 2/2 containers', event: 'pods-frontend-sidecar', hint: 'kubectl get pods -n shop' },
          { label: 'The same call now carries the client certificate (mTLS)', event: 'curl-payments-mtls', hint: MS_CURL },
          { label: 'Switch payments to STRICT', state: function (s) { return !!s.strict; }, hint: 'kubectl apply -f pa-strict.yaml' },
          { label: 'Under STRICT the call still works', event: 'curl-payments-mtls', hint: MS_CURL }
        ] },
      { id: 'istiod-down', title: 'Traffic flows, but nothing new can join the mesh',
        goal: 'Someone scaled istiod to zero. Show that meshed traffic still flows, see what breaks when frontend is redeployed, find the cause and restore the control plane.',
        setup: { nsLabeled: true, restarted: true, strict: true, cpUp: false },
        steps: [
          { label: 'Existing meshed traffic still flows over mTLS', event: 'curl-payments-mtls', hint: MS_CURL },
          { label: 'Redeploy frontend', event: 'rollout-blocked', hint: 'kubectl rollout restart deployment/frontend -n shop' },
          { label: 'Read why the new pods are not created: the injection webhook fails', event: 'inject-webhook-fail', hint: 'kubectl get events -n shop' },
          { label: 'Find istiod at zero replicas', event: 'istiod-scaled-zero', hint: 'kubectl get deployments -n istio-system' },
          { label: 'Bring istiod back', state: function (s) { return !!s.cpUp; }, hint: 'kubectl scale deployment istiod -n istio-system --replicas=1' },
          { label: 'Every sidecar is SYNCED with istiod again', event: 'proxy-status-synced', hint: 'istioctl proxy-status' }
        ] }
    ]
  };

  /* ── pack: CKS workload security (v1.7.0, 2026-10-29 — the first CKS pack) ──────────────────────────────────────
   * Drives cks-pod-security on the NEW authored cks-pod-security.glb. Namespaces: payments (Deployment payments-api,
   * ServiceAccount api-sa, Secret db-creds), frontend (deploy/web, the legitimate client), default (pod attacker, a
   * compromised workload). PodSecurity admission messages follow the built-in controller's format; the audit event is
   * shaped like audit.k8s.io/v1 (representative, not byte-identical). Lab files stand in for editing YAML; the one
   * modelled edit is `sed -i` on the kube-apiserver static-pod manifest. */
  var CKS_NOTE = 'Namespaces: payments (deploy/payments-api, ServiceAccount api-sa, Secret db-creds) · frontend (deploy/web, the real client) · default (pod attacker, a compromised workload). Lab files stand in for editing YAML (ls / cat / kubectl apply -f). Admission, probes, RBAC answers and the audit log are computed by the rules engine. Lab-only: fault psa|harden|seccomp|netpol|allow|rbac|audit break|fix.';
  var CKS_SA = 'system:serviceaccount:payments:api-sa';
  var CKS_PODS = { api0: 'payments-api-7d9c6b8f5-q4m2x', api1: 'payments-api-7d9c6b8f5-t8n6w', rs: 'payments-api-7d9c6b8f5', web: 'web-6b7f9c8d4-k2p9z', attacker: 'attacker' };
  var CKS_APISERVER = '/etc/kubernetes/manifests/kube-apiserver.yaml';
  var CKS_AUDIT_LOG = '/var/log/kubernetes/audit/audit.log';
  var CKS_LOGPATH_LINE = '- --audit-log-path=' + CKS_AUDIT_LOG;
  function cksDeployYaml(hardened, seccomp) {
    var y = ['apiVersion: apps/v1', 'kind: Deployment', 'metadata:', '  name: payments-api', '  namespace: payments', 'spec:', '  replicas: 2', '  selector:', '    matchLabels:', '      app: payments-api', '  template:', '    metadata:', '      labels:', '        app: payments-api', '    spec:', '      serviceAccountName: api-sa'];
    if (hardened || seccomp) {
      y.push('      securityContext:');
      if (hardened) y.push('        runAsNonRoot: true', '        runAsUser: 10001');
      if (seccomp) y.push('        seccompProfile:', '          type: RuntimeDefault');
    }
    y.push('      containers:', '      - name: api', '        image: registry.example.com/payments/api:2.4.1', '        ports:', '        - containerPort: 8080');
    if (hardened) y.push('        securityContext:', '          allowPrivilegeEscalation: false', '          capabilities:', '            drop: ["ALL"]', '          readOnlyRootFilesystem: true');
    else y.push('        securityContext:', '          privileged: true');
    return y;
  }
  var CKS_DEFAULT_DENY = ['apiVersion: networking.k8s.io/v1', 'kind: NetworkPolicy', 'metadata:', '  name: default-deny-ingress', '  namespace: payments', 'spec:', '  podSelector: {}', '  policyTypes:', '  - Ingress'];
  var CKS_ALLOW_FE = ['apiVersion: networking.k8s.io/v1', 'kind: NetworkPolicy', 'metadata:', '  name: allow-frontend', '  namespace: payments', 'spec:', '  podSelector:', '    matchLabels:', '      app: payments-api', '  policyTypes:', '  - Ingress', '  ingress:', '  - from:', '    - namespaceSelector:', '        matchLabels:', '          kubernetes.io/metadata.name: frontend', '    ports:', '    - protocol: TCP', '      port: 8080'];
  var CKS_DEBUG = ['apiVersion: v1', 'kind: Pod', 'metadata:', '  name: debug', '  namespace: payments', 'spec:', '  containers:', '  - name: debug', '    image: busybox:1.37', '    command: ["sleep", "3600"]', '    securityContext:', '      privileged: true'];
  var CKS_POLICY = ['apiVersion: audit.k8s.io/v1', 'kind: Policy', 'omitStages:', '- RequestReceived', 'rules:', '# Secrets and ConfigMaps: who/what/when only, never the body (it would contain the data)', '- level: Metadata', '  resources:', '  - group: ""', '    resources: ["secrets", "configmaps"]',
    '- level: None', '  users: ["system:kube-proxy"]', '  verbs: ["watch"]', '- level: Request', '  resources:', '  - group: ""', '    resources: ["pods"]', '- level: Metadata'];
  function cksManifest(auditOn) {
    return ['# (sim) trimmed — only the fields this task needs', 'apiVersion: v1', 'kind: Pod', 'metadata:', '  name: kube-apiserver', '  namespace: kube-system', 'spec:', '  containers:', '  - command:', '    - kube-apiserver', '    - --advertise-address=10.0.0.10',
      '    - --authorization-mode=Node,RBAC', '    - --enable-admission-plugins=NodeRestriction', '    - --audit-policy-file=/etc/kubernetes/audit/policy.yaml', '    ' + (auditOn ? '' : '# ') + CKS_LOGPATH_LINE, '    - --audit-log-maxage=7', '    - --audit-log-maxbackup=2', '    - --audit-log-maxsize=100',
      '    image: registry.k8s.io/kube-apiserver:v1.37.1', '    name: kube-apiserver', '    volumeMounts:', '    - mountPath: /etc/kubernetes/audit/policy.yaml', '      name: audit-policy', '      readOnly: true', '    - mountPath: /var/log/kubernetes/audit/', '      name: audit-log',
      '  volumes:', '  - hostPath:', '      path: /etc/kubernetes/audit/policy.yaml', '      type: File', '    name: audit-policy', '  - hostPath:', '      path: /var/log/kubernetes/audit/', '      type: DirectoryOrCreate', '    name: audit-log'];
  }
  /** Role/RoleBinding for api-sa: lazily seeded from the first state the terminal sees (least = they exist). */
  function cksRbac(s, ctx) {
    if (!ctx.vars.cksRbac) ctx.vars.cksRbac = s.rbacLeast ? { role: 'config-reader', rb: 'api-sa-config-reader' } : { role: null, rb: null };
    return ctx.vars.cksRbac;
  }
  function cksCan(s, ctx, who, verb, rsc, ns) {
    if (!who) return true; /* kubernetes-admin */
    if (who !== CKS_SA) return false;
    if (!s.rbacLeast) return true; /* ClusterRoleBinding api-sa-admin → cluster-admin */
    var r = cksRbac(s, ctx);
    return !!(r.role && r.rb) && rsc === 'configmaps' && /^(get|list|watch)$/.test(verb) && ns === 'payments';
  }
  function cksRes(x) {
    x = String(x || '').toLowerCase();
    if (/^(secrets?)$/.test(x)) return 'secrets';
    if (/^(cm|configmaps?)$/.test(x)) return 'configmaps';
    if (/^(po|pods?)$/.test(x)) return 'pods';
    if (/^(deploy|deployments?(\.apps)?)$/.test(x)) return 'deployments';
    if (x === '*') return '*';
    return null;
  }
  function cksForbidden(who, verb, rsc, ns) {
    return 'Error from server (Forbidden): ' + rsc + ' is forbidden: User "' + who + '" cannot ' + verb + ' resource "' + rsc + '" in API group "' + (rsc === 'deployments' ? 'apps' : '') + '" ' + (ns === '*' ? 'at the cluster scope' : 'in the namespace "' + ns + '"');
  }
  function cksAuditLine(ctx) {
    var a = ctx.vars.cksAudit; if (!a) return null;
    var ev = { kind: 'Event', apiVersion: 'audit.k8s.io/v1', level: 'Metadata', auditID: '5b0e8f4c-2d61-4a8e-9a43-0c7f1e2b9d17', stage: 'ResponseComplete',
      requestURI: '/api/v1/namespaces/payments/secrets/db-creds', verb: 'get', user: { username: 'kubernetes-admin', groups: ['kubeadm:cluster-admins', 'system:authenticated'] } };
    if (a.as) ev.impersonatedUser = { username: a.as, groups: ['system:serviceaccounts', 'system:serviceaccounts:payments', 'system:authenticated'] };
    ev.sourceIPs = ['10.0.0.10']; ev.userAgent = 'kubectl/v1.37.1 (linux/amd64) kubernetes/3c1e5f2';
    ev.objectRef = { resource: 'secrets', namespace: 'payments', name: 'db-creds', apiVersion: 'v1' };
    ev.responseStatus = { metadata: {}, code: a.code };
    ev.requestReceivedTimestamp = '2026-10-29T13:05:12.402118Z'; ev.stageTimestamp = '2026-10-29T13:05:12.405771Z';
    ev.annotations = { 'authorization.k8s.io/decision': a.code === 200 ? 'allow' : 'forbid' };
    return JSON.stringify(ev);
  }
  /** Probe payments-api from a pod in ns frontend (web) or default (attacker). */
  function cksCurl(s, d, from, cmd) {
    var url = '';
    for (var ci = 1; ci < cmd.length; ci++) {
      if (/^(-m|--max-time|--connect-timeout|-o|--output|-H|--header|-w|--write-out|-X|-T|--timeout|-O)$/.test(cmd[ci])) { ci++; continue; }
      if (cmd[ci].charAt(0) !== '-') { url = cmd[ci]; break; }
    }
    var mm = /^(?:https?:\/\/)?([^\/:]+)(?::(\d+))?/.exec(url);
    if (!mm) return res(['curl: (3) URL rejected: No host part in the URL'], 3);
    var host = mm[1].toLowerCase(), port = mm[2] || '80';
    if (!/^(payments-api\.payments(\.svc(\.cluster\.local)?)?\.?|10\.96\.77\.10)$/.test(host) || port !== '8080') return res(['sim: this drill probes Service payments-api on port 8080 (http://payments-api.payments:8080 or http://10.96.77.10:8080)'], 2);
    var m = d.metrics, who = from === 'frontend' ? 'frontend' : 'attacker';
    if (!m.admitted) return res(['curl: (7) Failed to connect to ' + host + ' port 8080 after 1 ms: Couldn\'t connect to server', '(sim) Service payments-api has no endpoints — its pods were never admitted', 'command terminated with exit code 7'], 7, null, ['probe', who + '-refused']);
    var ok = who === 'frontend' ? m.frontendReach : m.attackerReach;
    if (!ok) return res(['curl: (28) Connection timed out after 3001 milliseconds', '(sim) dropped by NetworkPolicy in ns payments (a drop, not a reset — so it times out)', 'command terminated with exit code 28'], 28, null, ['probe', who + '-blocked']);
    return res(['{"service":"payments-api","pod":"' + CKS_PODS.api0 + '","ok":true}'], 0, null, ['probe', who + '-ok']);
  }
  var cksPack = {
    sim: 'cks-pod-security',
    prompt: 'student@controlplane:~$',
    note: CKS_NOTE,
    files: {
      'payments-api-hardened.yaml': { yaml: cksDeployYaml(true, true), kind: 'deploy', hardened: true, seccomp: true },
      'payments-api-nonroot.yaml': { yaml: cksDeployYaml(true, false), kind: 'deploy', hardened: true, seccomp: false },
      'payments-api-privileged.yaml': { yaml: cksDeployYaml(false, false), kind: 'deploy', hardened: false, seccomp: false },
      'privileged-debug.yaml': { yaml: CKS_DEBUG, kind: 'debug' },
      'default-deny-ingress.yaml': { yaml: CKS_DEFAULT_DENY, kind: 'deny' },
      'allow-frontend.yaml': { yaml: CKS_ALLOW_FE, kind: 'allow' }
    },
    examples: ['kubectl get ns payments --show-labels', 'kubectl label --dry-run=server --overwrite ns payments pod-security.kubernetes.io/enforce=restricted', 'kubectl get deployment payments-api -n payments',
      'kubectl get pods -n payments', 'kubectl get events -n payments', 'cat payments-api-hardened.yaml', 'kubectl exec -n payments deploy/payments-api -- id', 'kubectl exec -n payments deploy/payments-api -- grep Seccomp /proc/1/status',
      'kubectl get networkpolicy -n payments', 'kubectl exec -n default attacker -- curl -s -m 3 http://payments-api.payments:8080', 'kubectl exec -n frontend deploy/web -- curl -s -m 3 http://payments-api.payments:8080',
      'kubectl auth can-i get secrets -A --as ' + CKS_SA, 'kubectl get clusterrolebindings -o wide', 'kubectl get rolebindings -n payments -o wide', 'cat ' + CKS_APISERVER, 'cat /etc/kubernetes/audit/policy.yaml', 'tail -n 1 ' + CKS_AUDIT_LOG],
    run: function (u, s, d, ctx) {
      var t = u.t, m = d.metrics, rb = cksRbac(s, ctx);
      var f = faultArgs(t);
      if (f) {
        var key = { psa: 'psaEnforce', harden: 'podHardened', seccomp: 'seccomp', netpol: 'denyIngress', allow: 'allowFrontend', rbac: 'rbacLeast', audit: 'auditOn' }[f[0]];
        if (!key || (f[1] !== 'break' && f[1] !== 'fix')) return res(['usage: fault psa|harden|seccomp|netpol|allow|rbac|audit break|fix   (lab-only fault injection)'], 2);
        var fs = {}; fs[key] = f[1] === 'fix';
        if (key === 'rbacLeast') ctx.vars.cksRbac = f[1] === 'fix' ? { role: 'config-reader', rb: 'api-sa-config-reader' } : { role: null, rb: null };
        return res(['[lab fault injection] ' + f.join(' ') + ' (simulated)'], 0, fs, ['fault']);
      }
      /* control-plane files: kube-apiserver static-pod manifest, audit policy, audit log */
      var file = (t[t.length - 1] || '');
      if ((t[0] === 'cat' || t[0] === 'less' || t[0] === 'head') && file === CKS_APISERVER) return res(cksManifest(!!s.auditOn), 0, null, ['cat-manifest', 'apiserver-audit-flags']);
      if (t[0] === 'cat' && file === '/etc/kubernetes/audit/policy.yaml') return res(CKS_POLICY, 0, null, ['audit-policy-read']);
      if (t[0] === 'ls' && /^\/var\/log\/kubernetes\/audit\/?$/.test(t[t.length - 1] || '')) return s.auditOn ? res(['audit.log'], 0, null, ['ls-audit']) : res([], 0, null, ['ls-audit-empty']);
      if ((t[0] === 'tail' || t[0] === 'cat' || t[0] === 'grep') && file === CKS_AUDIT_LOG) {
        if (!s.auditOn) return res([t[0] + ': ' + (t[0] === 'tail' ? 'cannot open \'' + file + '\' for reading' : file) + ': No such file or directory', '(sim) no log backend: kube-apiserver has no --audit-log-path'], 1, null, ['audit-log-missing']);
        if (t[0] === 'grep' && !/db-creds|secrets/.test(t.slice(1, -1).join(' '))) return res(['sim: this drill models grep for db-creds / secrets in the audit log'], 2);
        var line = cksAuditLine(ctx);
        if (!line) return res(t[0] === 'grep' ? [] : ['{"kind":"Event","apiVersion":"audit.k8s.io/v1","level":"Metadata","stage":"ResponseComplete","requestURI":"/api/v1/namespaces/kube-system/configmaps/kube-proxy","verb":"get","user":{"username":"system:node:node-01"},"objectRef":{"resource":"configmaps","namespace":"kube-system","name":"kube-proxy"},"responseStatus":{"code":200}}', '(sim) representative event — no read of Secret db-creds has been recorded since the log backend came up'], t[0] === 'grep' ? 1 : 0, null, ['audit-log-read']);
        return res(['-- (sim) representative audit.k8s.io/v1 event --', line, '(sim) level Metadata: who · verb · object · source IP · response code — no requestObject / responseObject, so the secret value never reaches the log'], 0, null, ['audit-log-read', 'audit-event-found']);
      }
      if (t[0] === 'sed') {
        var inPlace = t.some(function (a) { return /^-[a-zA-Z]*i/.test(a) || a === '--in-place'; });
        var expr = t.filter(function (a) { return a.charAt(0) === 's' && a.length > 3 && !/[a-z]/i.test(a.charAt(1)); })[0];
        if (file !== CKS_APISERVER) return res(['sim: this drill models sed on ' + CKS_APISERVER + ' only'], 2);
        var sub = sedSubst(expr);
        if (!sub) return res(["sed: -e expression #1, char 1: unknown command: `" + String(expr || '').charAt(0) + "'"], 1);
        var cur = '    ' + (s.auditOn ? '' : '# ') + CKS_LOGPATH_LINE, a0 = sub.a.replace(/^\^/, ''), next = cur;
        if (sub.a.charAt(0) === '^') { if (cur.indexOf(a0) === 0) next = sub.b + cur.slice(a0.length); }
        else if (cur.indexOf(a0) >= 0) next = cur.replace(a0, sub.b);
        var fixed = !s.auditOn && next.trim() === CKS_LOGPATH_LINE && /^\s+-/.test(next);
        if (!inPlace) return res(['(sim) without -i sed prints the edited file to stdout — nothing was written', next], 0);
        if (next === cur) return res([], 0, null, ['sed-nochange']);
        if (!fixed) return res(['(sim) the edit would leave an invalid manifest (the kubelet would fail to start the static pod) — this drill only models un-commenting the --audit-log-path line'], 1, null, ['sed-bad-edit']);
        ctx.vars.cksApiRestarts = (ctx.vars.cksApiRestarts || 0) + 1;
        return res(['(sim) the kubelet sees the manifest change and recreates the kube-apiserver static pod; kubectl is unavailable for a short while (no clock is simulated)'], 0, { auditOn: true }, ['manifest-edited', 'audit-backend-on']);
      }
      var fr = fileRun(cksPack, t); if (fr) return fr;
      if (t[0] === 'vi' || t[0] === 'vim' || t[0] === 'nano') return res(['sim: no interactive editor in a simulated shell — use sed -i on the manifest, or kubectl apply -f with the lab files'], 2);
      if (t[0] !== 'kubectl') return null;
      var verb = t[1], args = positional(t.slice(2), KUBECTL_VALUED.concat(['--as', '--as-group', '--role', '--clusterrole', '--serviceaccount', '--verb', '--resource', '--dry-run'])), ns = nsOf(t), out = flag(t, ['-o', '--output']);
      var as = flag(t, '--as'); if (as === true) as = null;
      var kind = (args[0] || '').toLowerCase(), name = args[1] || '';
      if (/\//.test(kind)) { name = kind.split('/')[1]; kind = kind.split('/')[0]; }
      if (verb === 'edit') return res(['sim: interactive editors are not modelled — use kubectl apply -f with the lab files (ls), kubectl label, or kubectl create/delete'], 2);
      /* namespaces + Pod Security labels */
      if (verb === 'get' && /^(ns|namespaces?)$/.test(kind)) {
        var lab = hasFlag(t, '--show-labels'), rows = [['NAME', 'STATUS', 'AGE'].concat(lab ? ['LABELS'] : [])];
        [['default', ''], ['frontend', ''], ['kube-system', ''], ['payments', s.psaEnforce ? ',pod-security.kubernetes.io/enforce=restricted' : '']].forEach(function (r) {
          if (!name || name === r[0]) rows.push([r[0], 'Active', '30d'].concat(lab ? ['kubernetes.io/metadata.name=' + r[0] + r[1]] : []));
        });
        if (rows.length === 1) return notFound('namespaces', name);
        return res(table(rows), 0, null, ['get-ns'].concat(lab && (!name || name === 'payments') ? ['ns-labels', s.psaEnforce ? 'ns-labels-restricted' : 'ns-labels-nopsa'] : []));
      }
      if (verb === 'label' && /^(ns|namespaces?)$/.test(kind)) {
        if (name !== 'payments') return name ? notFound('namespaces', name) : res(['error: resource(s) were provided, but no name was specified'], 1);
        var kv = args.slice(2).filter(function (a) { return /^pod-security\.kubernetes\.io\//.test(a); })[0];
        if (!kv) return res(['sim: this drill models Pod Security labels on ns payments (pod-security.kubernetes.io/enforce=restricted)'], 2);
        var dry = flag(t, '--dry-run'), over = hasFlag(t, '--overwrite');
        if (dry && dry !== 'server') return res(['sim: use --dry-run=server — only the API server runs the PodSecurity check (client dry-run never contacts it)'], 2);
        var lm = /^pod-security\.kubernetes\.io\/(enforce|warn|audit)(?:=([a-z]+)|(-))$/.exec(kv);
        if (!lm) return res(['sim: this drill models pod-security.kubernetes.io/enforce=restricted (and enforce- to remove it)'], 2);
        if (lm[1] !== 'enforce') return res(['sim: warn / audit modes are explained, not modelled — this drill changes only the enforce label (warn would add API warnings, audit would annotate audit events; neither blocks a pod)'], 2);
        if (lm[3]) { if (dry) return res(['namespace/payments unlabeled (server dry run)'], 0, null, ['psa-dryrun-remove']); return res(['namespace/payments unlabeled'], 0, s.psaEnforce ? { psaEnforce: false } : null, ['psa-unlabel']); }
        if (lm[2] !== 'restricted') return res(['sim: this drill models enforce=restricted (baseline would also block privileged: true, but not root, added capabilities like NET_RAW off the default set, or a missing seccompProfile)'], 2);
        if (s.psaEnforce && !over) return res(["error: 'pod-security.kubernetes.io/enforce' already has a value (restricted), and --overwrite is false"], 1);
        var warn = [];
        if (m.admitted && m.violations.length) {
          warn.push('Warning: existing pods in namespace "payments" violate the new PodSecurity enforce level "restricted:latest"');
          warn.push('Warning: ' + CKS_PODS.api0 + ' (and 1 other pod): ' + m.violations.map(function (v) { return v.split(' (')[0]; }).join(', '));
        }
        if (dry) return res(warn.concat(['namespace/payments labeled (server dry run)']), 0, null, ['psa-dryrun', warn.length ? 'psa-dryrun-warnings' : 'psa-dryrun-clean']);
        return res(warn.concat(['namespace/payments labeled']).concat(warn.length ? ['(sim) enforcement applies to new pods only: the running pods keep running until they are recreated'] : []), 0, { psaEnforce: true }, ['psa-label', 'psa-enforced']);
      }
      /* workloads */
      if (verb === 'get' && /^(deploy|deployments?(\.apps)?)$/.test(kind)) {
        if (ns !== 'payments' || (name && name !== 'payments-api')) return name ? notFound('deployments.apps', name) : res(['No resources found in ' + ns + ' namespace.'], 0);
        var ready = m.admitted ? '2/2' : '0/2';
        return res(table([['NAME', 'READY', 'UP-TO-DATE', 'AVAILABLE', 'AGE'], ['payments-api', ready, m.admitted ? '2' : '0', m.admitted ? '2' : '0', '3m']]), 0, null, ['get-deploy', m.admitted ? 'deploy-ready' : 'deploy-0-ready']);
      }
      if (verb === 'get' && /^(rs|replicasets?(\.apps)?)$/.test(kind)) {
        if (ns !== 'payments') return res(['No resources found in ' + ns + ' namespace.'], 0);
        return res(table([['NAME', 'DESIRED', 'CURRENT', 'READY', 'AGE'], [CKS_PODS.rs, '2', m.admitted ? '2' : '0', m.admitted ? '2' : '0', '3m']]), 0, null, ['get-rs']);
      }
      if (verb === 'get' && /^(po|pods?)$/.test(kind)) {
        var lsel = flag(t, ['-l', '--selector']) || '';
        if (ns === 'kube-system') {
          if (lsel && !/component=kube-apiserver/.test(lsel)) return res(['sim: this drill models -l component=kube-apiserver in kube-system'], 2);
          var restarts = ctx.vars.cksApiRestarts || 0;
          return res(table([['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE'], ['kube-apiserver-controlplane', '1/1', 'Running', String(restarts), restarts ? '25s' : '30d']]), 0, null, ['get-pods-apiserver', s.auditOn ? 'apiserver-back' : 'apiserver-running']);
        }
        if (ns === 'frontend') return res(table([['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE'], [CKS_PODS.web, '1/1', 'Running', '0', '30d']]), 0, null, ['get-pods-frontend']);
        if (ns === 'default') return res(table([['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE'], [CKS_PODS.attacker, '1/1', 'Running', '0', '2h']]), 0, null, ['get-pods-default']);
        if (ns !== 'payments') return res(['No resources found in ' + (ns === '*' ? 'the cluster (sim: pass -n payments, -n frontend, -n default or -n kube-system)' : ns + ' namespace.')], 0);
        if (!m.admitted) return res(['No resources found in payments namespace.'], 0, null, ['get-pods', 'pods-none']);
        return res(table([['NAME', 'READY', 'STATUS', 'RESTARTS', 'AGE'], [CKS_PODS.api0, '1/1', 'Running', '0', '40s'], [CKS_PODS.api1, '1/1', 'Running', '0', '38s']]), 0, null, ['get-pods', 'pods-running']);
      }
      if ((verb === 'get' && /^(ev|events?)$/.test(kind)) || (verb === 'describe' && /^(rs|replicasets?(\.apps)?)$/.test(kind))) {
        if (ns !== 'payments') return res(['No events found in ' + ns + ' namespace.'], 0);
        if (!m.admitted) {
          var msg = 'Error creating: pods "' + CKS_PODS.rs + '-x2x4k" is forbidden: violates PodSecurity "restricted:latest": ' + m.violations.join(', ');
          var ev = verb === 'get' ? table([['LAST SEEN', 'TYPE', 'REASON', 'OBJECT', 'MESSAGE'], ['8s', 'Warning', 'FailedCreate', 'replicaset/' + CKS_PODS.rs, msg]])
            : ['Name:           ' + CKS_PODS.rs, 'Namespace:      payments', 'Replicas:       0 current / 2 desired', 'Pods Status:    0 Running / 0 Waiting / 0 Succeeded / 0 Failed', 'Events:', '  Type     Reason        Age                From                   Message', '  ----     ------        ----               ----                   -------', '  Warning  FailedCreate  8s (x6 over 3m)    replicaset-controller  ' + msg];
          return res(ev, 0, null, ['events', 'psa-failedcreate']);
        }
        return res(table([['LAST SEEN', 'TYPE', 'REASON', 'OBJECT', 'MESSAGE'], ['40s', 'Normal', 'SuccessfulCreate', 'replicaset/' + CKS_PODS.rs, 'Created pod: ' + CKS_PODS.api0], ['38s', 'Normal', 'Started', 'pod/' + CKS_PODS.api0, 'Started container api']]), 0, null, ['events', 'events-ok']);
      }
      if (verb === 'apply' || (verb === 'create' && hasFlag(t, ['-f', '--filename']))) {
        var a = applyFile(cksPack, t); if (a.err) return a.err;
        var lf = a.f;
        if (lf.kind === 'debug') {
          if (s.psaEnforce) return res(['Error from server (Forbidden): error when creating "' + a.name + '": pods "debug" is forbidden: violates PodSecurity "restricted:latest": ' + [CKS_VIOLATIONS_CLI.privileged, CKS_VIOLATIONS_CLI.ape, CKS_VIOLATIONS_CLI.caps, CKS_VIOLATIONS_CLI.nonroot, CKS_VIOLATIONS_CLI.seccomp].join(', ')], 1, null, ['psa-forbidden']);
          return res(['pod/debug created', '(sim) admitted: an unlabelled namespace defaults to the privileged level. The debug pod is not drawn in the scene; it is deleted when you leave this terminal'], 0, null, ['privileged-admitted']);
        }
        if (lf.kind === 'deploy') {
          var nowOk = !s.psaEnforce || (lf.hardened && lf.seccomp);
          var lines = ['deployment.apps/payments-api configured'];
          if (s.psaEnforce && !nowOk) lines.push('(sim) the Deployment is accepted (enforce mode checks Pods, not templates); the new ReplicaSet will get FailedCreate — read the events');
          else if (s.psaEnforce && !m.admitted) lines.push('(sim) the new pod template passes restricted, so the ReplicaSet creates the pods');
          return res(lines, 0, { podHardened: !!lf.hardened, seccomp: !!lf.seccomp }, ['apply-deploy', lf.hardened && lf.seccomp ? 'apply-hardened' : 'apply-weak']);
        }
        if (lf.kind === 'deny') return res(['networkpolicy.networking.k8s.io/default-deny-ingress ' + (s.denyIngress ? 'unchanged' : 'created')], 0, s.denyIngress ? null : { denyIngress: true }, ['apply-deny']);
        return res(['networkpolicy.networking.k8s.io/allow-frontend ' + (s.allowFrontend ? 'unchanged' : 'created')], 0, s.allowFrontend ? null : { allowFrontend: true }, ['apply-allow']);
      }
      if (/^(netpol|networkpolic(y|ies)(\.networking\.k8s\.io)?)$/.test(kind)) {
        if (verb === 'get') {
          if (ns !== 'payments') return res(['No resources found in ' + ns + ' namespace.'], 0);
          var np = [['NAME', 'POD-SELECTOR', 'AGE']];
          if (s.denyIngress) np.push(['default-deny-ingress', '<none>', '5m']);
          if (s.allowFrontend) np.push(['allow-frontend', 'app=payments-api', '5m']);
          if (np.length === 1) return res(['No resources found in payments namespace.'], 0, null, ['get-netpol', 'netpol-none']);
          return res(table(np), 0, null, ['get-netpol']);
        }
        if (verb === 'delete') {
          var dk = name === 'default-deny-ingress' ? 'denyIngress' : (name === 'allow-frontend' ? 'allowFrontend' : null);
          if (ns !== 'payments' || !dk || !s[dk]) return notFound('networkpolicies.networking.k8s.io', name);
          var dp = {}; dp[dk] = false;
          return res(['networkpolicy.networking.k8s.io "' + name + '" deleted'], 0, dp, ['delete-netpol']);
        }
      }
      if (verb === 'delete' && /^(po|pods?)$/.test(kind) && name === 'debug') return res(['pod "debug" deleted'], 0, null, ['delete-debug']);
      /* RBAC */
      if (verb === 'auth' && t[2] === 'can-i') {
        var cargs = positional(t.slice(3), KUBECTL_VALUED.concat(['--as', '--as-group']));
        if (hasFlag(t, '--list')) return res(['sim: `can-i --list` is not modelled — ask one verb + resource at a time'], 2);
        var cv = cargs[0], cr = cksRes(cargs[1]);
        if (!cv || !cr || cr === '*') return res(['sim: this drill models can-i on secrets, configmaps, pods and deployments (e.g. kubectl auth can-i get secrets -A --as ' + CKS_SA + ')'], 2);
        if (as && as !== CKS_SA) return res(['no', '# sim: only ' + CKS_SA + ' is modelled as a subject (a ServiceAccount is impersonated as system:serviceaccount:<ns>:<name>)'], 1, null, ['cani', 'cani-other']);
        var scope = ns === '*' ? 'all' : ns, okc = cksCan(s, ctx, as, cv, cr, ns);
        return res([okc ? 'yes' : 'no'], okc ? 0 : 1, null, ['cani', 'cani-' + (okc ? 'yes' : 'no'), 'cani-' + (as ? 'sa' : 'admin') + '-' + cr + '-' + scope + '-' + (okc ? 'yes' : 'no')].concat(as ? ['cani-' + cr + '-' + scope + '-' + (okc ? 'yes' : 'no')] : []));
      }
      if (verb === 'get' && /^(clusterrolebindings?|crb)$/.test(kind)) {
        var wide = out === 'wide', cr2 = [['NAME', 'ROLE', 'AGE'].concat(wide ? ['USERS', 'GROUPS', 'SERVICEACCOUNTS'] : [])];
        cr2.push(['cluster-admin', 'ClusterRole/cluster-admin', '30d'].concat(wide ? ['', 'system:masters', ''] : []));
        cr2.push(['kubeadm:cluster-admins', 'ClusterRole/cluster-admin', '30d'].concat(wide ? ['', 'kubeadm:cluster-admins', ''] : []));
        if (!s.rbacLeast) cr2.push(['api-sa-admin', 'ClusterRole/cluster-admin', '6d'].concat(wide ? ['', '', 'payments/api-sa'] : []));
        return res(table(cr2).concat(['# sim: other system:* ClusterRoleBindings omitted']), 0, null, ['get-crb'].concat(!s.rbacLeast && wide ? ['crb-api-sa-found'] : []));
      }
      if (verb === 'delete' && /^(clusterrolebindings?|crb)$/.test(kind)) {
        if (name !== 'api-sa-admin' || s.rbacLeast) return name === 'cluster-admin' || name === 'kubeadm:cluster-admins' ? res(['sim: refusing to model deleting a kubeadm default binding — that locks the admin out'], 2) : notFound('clusterrolebindings.rbac.authorization.k8s.io', name);
        return res(['clusterrolebinding.rbac.authorization.k8s.io "api-sa-admin" deleted'], 0, { rbacLeast: true }, ['delete-crb']);
      }
      if (verb === 'get' && /^(rolebindings?|rb|roles?)$/.test(kind)) {
        if (ns !== 'payments') return res(['No resources found in ' + ns + ' namespace.'], 0);
        if (/^roles?$/.test(kind)) return rb.role ? res(table([['NAME', 'CREATED AT'], [rb.role, '2026-10-29T13:00:00Z']]), 0, null, ['get-roles']) : res(['No resources found in payments namespace.'], 0, null, ['get-roles']);
        if (!rb.rb) return res(['No resources found in payments namespace.'], 0, null, ['get-rolebindings']);
        return res(table([['NAME', 'ROLE', 'AGE'].concat(out === 'wide' ? ['USERS', 'GROUPS', 'SERVICEACCOUNTS'] : []), [rb.rb, 'Role/' + rb.role, '1m'].concat(out === 'wide' ? ['', '', 'payments/api-sa'] : [])]), 0, null, ['get-rolebindings']);
      }
      if (verb === 'create' && kind === 'role') {
        var vv = String(flag(t, '--verb') || ''), rr = String(flag(t, '--resource') || '');
        if (!name || !vv || vv === 'true' || !rr || rr === 'true') return res(['error: at least one verb must be specified', '(e.g. kubectl create role config-reader -n payments --verb=get,list,watch --resource=configmaps)'], 1);
        if (ns !== 'payments') return res(['role.rbac.authorization.k8s.io/' + name + ' created', '# sim: created in namespace ' + ns + ' — it grants nothing in payments (add -n payments). Not reflected in the scene.'], 0, null, ['role-wrong-ns']);
        var verbs = vv.split(','), rscs = rr.split(',').map(cksRes);
        if (verbs.some(function (x) { return !/^(get|list|watch)$/.test(x); }) || rscs.some(function (x) { return x !== 'configmaps'; })) return res(['sim: least privilege for this app: it only reads its configuration — --verb=get,list,watch --resource=configmaps (secrets, * or write verbs would re-open the hole)'], 2, null, ['role-too-broad']);
        if (rb.role === name) return res(['error: failed to create role: roles.rbac.authorization.k8s.io "' + name + '" already exists'], 1);
        rb.role = name;
        return res(['role.rbac.authorization.k8s.io/' + name + ' created'], 0, null, ['role-created']);
      }
      if (verb === 'create' && kind === 'rolebinding') {
        var rl = flag(t, '--role'), sa = flag(t, '--serviceaccount');
        if (!name || !rl || rl === true) return res(['error: exactly one NAME is required, and one of --role or --clusterrole'], 1);
        if (ns !== 'payments') return res(['rolebinding.rbac.authorization.k8s.io/' + name + ' created', '# sim: created in namespace ' + ns + ' — it grants nothing in payments (add -n payments). Not reflected in the scene.'], 0, null, ['rolebinding-wrong-ns']);
        if (sa && sa !== true && !/:/.test(sa)) return res(['error: serviceaccount must be <namespace>:<name>'], 1);
        if (sa !== 'payments:api-sa') return res(['sim: bind the ServiceAccount the app runs as: --serviceaccount=payments:api-sa'], 2);
        if (!rb.role || rl !== rb.role) return res(['rolebinding.rbac.authorization.k8s.io/' + name + ' created', '# sim: Role "' + rl + '" does not exist in payments, so this binding grants nothing until it does — create the Role first'], 0, null, ['rolebinding-dangling']);
        if (rb.rb) return res(['error: failed to create rolebinding: rolebindings.rbac.authorization.k8s.io "' + rb.rb + '" already exists' + (rb.rb === name ? '' : ' (sim: one binding for api-sa in this drill)')], 1);
        rb.rb = name;
        return res(['rolebinding.rbac.authorization.k8s.io/' + name + ' created'], 0, null, ['rolebinding-created']);
      }
      if (verb === 'get' && /^(secrets?)$/.test(kind)) {
        var sns = ns === '*' ? '*' : ns;
        if (!cksCan(s, ctx, as, name ? 'get' : 'list', 'secrets', sns)) {
          if (s.auditOn && name === 'db-creds' && sns === 'payments') ctx.vars.cksAudit = { as: as, code: 403 };
          return res([cksForbidden(as, name ? 'get' : 'list', 'secrets', sns)], 1, null, ['forbidden', 'secrets-forbidden']);
        }
        if (name && (name !== 'db-creds' || sns !== 'payments')) return notFound('secrets', name);
        if (name) {
          if (s.auditOn) ctx.vars.cksAudit = { as: as, code: 200 };
          if (out === 'yaml' || out === 'json') return res(['apiVersion: v1', 'kind: Secret', 'metadata:', '  name: db-creds', '  namespace: payments', 'type: Opaque', 'data:', '  password: czNjcjN0LWRiLXBhc3M=   # (sim) base64 is encoding, not encryption', '  username: cGF5bWVudHM='], 0, null, ['secret-read', 'secret-read-yaml']);
          return res(table([['NAME', 'TYPE', 'DATA', 'AGE'], ['db-creds', 'Opaque', '2', '30d']]), 0, null, ['secret-read']);
        }
        var srows = [['NAMESPACE', 'NAME', 'TYPE', 'DATA', 'AGE'], ['kube-system', 'bootstrap-token-abcdef', 'bootstrap.kubernetes.io/token', '6', '30d'], ['payments', 'db-creds', 'Opaque', '2', '30d'], ['frontend', 'session-key', 'Opaque', '1', '30d']];
        var shown = sns === '*' ? srows : [srows[0].slice(1)].concat(srows.slice(1).filter(function (r) { return r[0] === sns; }).map(function (r) { return r.slice(1); }));
        if (shown.length === 1) return res(['No resources found in ' + sns + ' namespace.'], 0);
        return res(table(shown), 0, null, ['secrets-list'].concat(as && sns === '*' ? ['sa-secrets-all-ns'] : []));
      }
      var ex = execArgs(t);
      if (ex) {
        if (!ex.hasDd || !ex.cmd.length) return res(['error: you must specify at least one command for the container (kubectl exec … -- CMD)'], 1);
        if (ex.ns === 'default' && ex.target === 'attacker') return /^(curl|wget)$/.test(ex.cmd[0]) ? cksCurl(s, d, 'default', ex.cmd) : res(['sim: from the attacker pod this drill models curl to payments-api'], 2);
        if (ex.ns === 'frontend' && (ex.target === 'web' || ex.target === CKS_PODS.web)) return /^(curl|wget)$/.test(ex.cmd[0]) ? cksCurl(s, d, 'frontend', ex.cmd) : res(['sim: from web this drill models curl to payments-api'], 2);
        if (ex.ns === 'payments' && (ex.target === 'payments-api' || ex.target === CKS_PODS.api0 || ex.target === CKS_PODS.api1)) {
          if (!m.admitted) return res(['error: cannot exec: deployment/payments-api has no running pods (sim) — they were never admitted'], 1, null, ['exec-no-pods']);
          var c0 = ex.cmd[0], cjoin = ex.cmd.join(' ');
          if (c0 === 'id' || c0 === 'whoami') return s.podHardened ? res([c0 === 'id' ? 'uid=10001 gid=0(root) groups=0(root)' : 'whoami: unknown uid 10001'], 0, null, ['id', 'id-nonroot']) : res([c0 === 'id' ? 'uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel)' : 'root'], 0, null, ['id', 'id-root']);
          if (/^(grep|cat)$/.test(c0) && /\/proc\/(1|self)\/status/.test(cjoin)) {
            var sc = s.seccomp ? ['Seccomp:\t2', 'Seccomp_filters:\t1'] : ['Seccomp:\t0', 'Seccomp_filters:\t0'];
            var capl = s.podHardened ? ['CapEff:\t0000000000000000'] : ['CapEff:\t000001ffffffffff'];
            var lines2 = c0 === 'cat' ? ['Name:\tapi', 'Uid:\t' + (s.podHardened ? '10001\t10001\t10001\t10001' : '0\t0\t0\t0')].concat(capl, ['NoNewPrivs:\t' + (s.podHardened ? 1 : 0)], sc) : (/Cap/i.test(cjoin) ? capl : (/NoNewPrivs/.test(cjoin) ? ['NoNewPrivs:\t' + (s.podHardened ? 1 : 0)] : sc));
            return res(lines2, 0, null, ['proc-status', s.seccomp ? 'seccomp-filtered' : 'seccomp-unconfined']);
          }
          if (c0 === 'cat' && /serviceaccount\/token/.test(cjoin)) return res(['eyJhbGciOiJSUzI1NiIsImtpZCI6IkxhYiJ9.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjIl0sInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpwYXltZW50czphcGktc2EifQ.(sim-signature)', '(sim) a projected, time-bound bearer token for ' + CKS_SA + ' — whoever holds it can use it until it expires or the pod is deleted'], 0, null, ['token-read']);
          return res(['sim: inside payments-api this drill models id, grep Seccomp|CapEff|NoNewPrivs /proc/1/status and cat /var/run/secrets/kubernetes.io/serviceaccount/token'], 2);
        }
        return res(['Error from server (NotFound): pods "' + ex.target + '" not found' + ' (sim: pods in this lab — payments: deploy/payments-api · frontend: deploy/web · default: attacker)'], 1, null, ['not-found']);
      }
      if (verb === 'rollout' && args[0] === 'restart') {
        if (ns !== 'payments' || !/payments-api$/.test(args[1] || '') && args[2] !== 'payments-api') return res(['sim: this drill models kubectl rollout restart deployment payments-api -n payments'], 2);
        return res(['deployment.apps/payments-api restarted'].concat(m.admitted ? [] : ['(sim) the new pods still fail admission — read the events']), 0, null, ['rollout-restart']);
      }
      return unmodelled(t.join(' '), cksPack.examples);
    },
    tasks: [
      { id: 'psa-enforce', title: 'Enforce Pod Security “restricted” on payments',
        goal: 'Namespace payments runs hardened workloads, yet anyone can still create a privileged pod there. Preview restricted with a server-side dry run, enforce it, and prove a privileged pod is now refused.',
        setup: { psaEnforce: false, podHardened: true, seccomp: true },
        steps: [
          { label: 'See that payments carries no Pod Security labels', event: 'ns-labels-nopsa', hint: 'kubectl get ns payments --show-labels' },
          { label: 'Preview restricted with a server-side dry run (no warnings = no running pod would break)', event: 'psa-dryrun', hint: 'kubectl label --dry-run=server --overwrite ns payments pod-security.kubernetes.io/enforce=restricted' },
          { label: 'Enforce restricted on payments', state: function (s) { return !!s.psaEnforce; }, hint: 'kubectl label --overwrite ns payments pod-security.kubernetes.io/enforce=restricted' },
          { label: 'Prove it: a privileged debug pod is now Forbidden', event: 'psa-forbidden', hint: 'kubectl apply -f privileged-debug.yaml' }
        ] },
      { id: 'harden-pod', title: 'Deployment is 0/2: harden its securityContext',
        goal: 'payments-api was redeployed into the restricted namespace and has no pods. Find the admission error, apply a template that passes restricted, and prove the container runs non-root under a seccomp filter.',
        setup: { psaEnforce: true, podHardened: false, seccomp: false },
        steps: [
          { label: 'The Deployment has 0 of 2 pods ready', event: 'deploy-0-ready', hint: 'kubectl get deployment payments-api -n payments' },
          { label: 'Read why: FailedCreate … violates PodSecurity "restricted:latest"', event: 'psa-failedcreate', hint: 'kubectl get events -n payments' },
          { label: 'Apply a template that passes every restricted check', state: function (s) { return !!s.podHardened && !!s.seccomp; }, hint: 'kubectl apply -f payments-api-hardened.yaml' },
          { label: 'The pods are Running', event: 'pods-running', hint: 'kubectl get pods -n payments' },
          { label: 'Prove the container is not root', event: 'id-nonroot', hint: 'kubectl exec -n payments deploy/payments-api -- id' },
          { label: 'Prove a seccomp filter is loaded (Seccomp: 2)', event: 'seccomp-filtered', hint: 'kubectl exec -n payments deploy/payments-api -- grep Seccomp /proc/1/status' }
        ] },
      { id: 'default-deny', title: 'Anything can reach payments-api: default-deny, then allow frontend',
        goal: 'A compromised pod in namespace default can call payments-api. Isolate the namespace with a default-deny ingress policy, notice what else it blocks, and allow only frontend on 8080.',
        setup: { denyIngress: false, allowFrontend: false },
        steps: [
          { label: 'Reproduce: the attacker pod gets a 200', event: 'attacker-ok', hint: 'kubectl exec -n default attacker -- curl -s -m 3 http://payments-api.payments:8080' },
          { label: 'Apply default-deny ingress in payments', state: function (s) { return !!s.denyIngress; }, hint: 'kubectl apply -f default-deny-ingress.yaml' },
          { label: 'The attacker now times out', event: 'attacker-blocked', hint: 'kubectl exec -n default attacker -- curl -s -m 3 http://payments-api.payments:8080' },
          { label: 'So does the real client in frontend', event: 'frontend-blocked', hint: 'kubectl exec -n frontend deploy/web -- curl -s -m 3 http://payments-api.payments:8080' },
          { label: 'Allow namespace frontend on TCP 8080', state: function (s) { return !!s.denyIngress && !!s.allowFrontend; }, hint: 'kubectl apply -f allow-frontend.yaml' },
          { label: 'frontend gets a 200 again (the attacker still does not)', event: 'frontend-ok', hint: 'kubectl exec -n frontend deploy/web -- curl -s -m 3 http://payments-api.payments:8080' }
        ] },
      { id: 'sa-least-privilege', title: 'The app’s ServiceAccount is cluster-admin',
        goal: 'payments-api only reads its ConfigMaps, but its ServiceAccount token can read every Secret in the cluster. Find the binding, remove it, and grant exactly what the app needs.',
        setup: { rbacLeast: false },
        steps: [
          { label: 'Prove the blast radius: api-sa can read Secrets in every namespace', event: 'cani-secrets-all-yes', hint: 'kubectl auth can-i get secrets -A --as ' + CKS_SA },
          { label: 'Find the ClusterRoleBinding that grants it', event: 'crb-api-sa-found', hint: 'kubectl get clusterrolebindings -o wide' },
          { label: 'Delete that binding', state: function (s) { return !!s.rbacLeast; }, hint: 'kubectl delete clusterrolebinding api-sa-admin' },
          { label: 'Create a Role that only reads ConfigMaps in payments', event: 'role-created', hint: 'kubectl create role config-reader -n payments --verb=get,list,watch --resource=configmaps' },
          { label: 'Bind it to the ServiceAccount', event: 'rolebinding-created', hint: 'kubectl create rolebinding api-sa-config-reader -n payments --role=config-reader --serviceaccount=payments:api-sa' },
          { label: 'Verify: no Secrets anywhere…', event: 'cani-secrets-all-no', hint: 'kubectl auth can-i get secrets -A --as ' + CKS_SA },
          { label: '…but ConfigMaps in payments still work', event: 'cani-configmaps-payments-yes', hint: 'kubectl auth can-i list configmaps -n payments --as ' + CKS_SA }
        ] },
      { id: 'audit-log', title: 'Who read db-creds? Turn on the audit log backend',
        goal: 'Security asks who read Secret db-creds, and the API server has an audit policy — but nothing is being written. Find out why, turn the log backend on, and find a Secret read in the log (without its value).',
        setup: { auditOn: false },
        steps: [
          { label: 'Read the kube-apiserver manifest: a policy file, but --audit-log-path is commented out', event: 'apiserver-audit-flags', hint: 'cat ' + CKS_APISERVER },
          { label: 'Read the audit policy: Secrets at Metadata', event: 'audit-policy-read', hint: 'cat /etc/kubernetes/audit/policy.yaml' },
          { label: 'Un-comment --audit-log-path in the static-pod manifest', state: function (s) { return !!s.auditOn; }, hint: "sed -i 's|# - --audit-log-path|- --audit-log-path|' " + CKS_APISERVER },
          { label: 'The kube-apiserver static pod is back', event: 'apiserver-back', hint: 'kubectl get pods -n kube-system -l component=kube-apiserver' },
          { label: 'Read Secret db-creds once (that is the event you will look for)', event: 'secret-read', hint: 'kubectl get secret db-creds -n payments' },
          { label: 'Find it in the audit log: user, verb, object, but no data', event: 'audit-event-found', hint: 'tail -n 1 ' + CKS_AUDIT_LOG }
        ] }
    ]
  };
  var CKS_VIOLATIONS_CLI = {
    privileged: 'privileged (container "debug" must not set securityContext.privileged=true)',
    ape: 'allowPrivilegeEscalation != false (container "debug" must set securityContext.allowPrivilegeEscalation=false)',
    caps: 'unrestricted capabilities (container "debug" must set securityContext.capabilities.drop=["ALL"])',
    nonroot: 'runAsNonRoot != true (pod or container "debug" must set securityContext.runAsNonRoot=true)',
    seccomp: 'seccompProfile (pod or container "debug" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")'
  };

  /** Prompt for the terminal after the last command (node packs change host with `ssh NODE` / `exit`). */
  function promptFor(simId, ctx) {
    var p = PACKS[simId]; if (!p) return '';
    return ctx && ctx.vars && ctx.vars.host ? 'student@' + ctx.vars.host + ':~$' : p.prompt;
  }

  var PACKS = {};
  [etcdPack, cpPack, schedPack, hpaPack, awsPack, netpolPack, rbacPack, storagePack, ingressPack, gatewayPack, configPack, nodePack, svcDnsPack, cniPack, meshPack, cksPack].forEach(function (p) { PACKS[p.sim] = p; });

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
    },
    /* v1.3.0 (2026-10-21) */
    'gateway-api': {
      'gw-pending': [
        ['Request the orders URL over HTTPS and read what curl reports.', '^(client-0|req-0-[0-3])$'],
        ['List the Gateways in the default namespace and read the ADDRESS and PROGRAMMED columns.', '^ingress-controller$'],
        ['A Gateway names a class, and the class names a controller. Is that class Accepted?', '^ingress-controller$'],
        ['Nothing reconciles lab-gw yet. A ready-made manifest in your home directory stands in for installing an implementation — read it, then apply it.', '^ingress-controller$'],
        ['Request the orders URL again.', '^(client-0|route-0-[0-4]|service-0)$']
      ],
      'gw-hostname': [
        ['Request the orders URL and read only the status line.', '^(client-0|req-0-[0-3])$'],
        ['Attachment is reported per parent in the route’s own status — describe the HTTPRoute.', '^rule-2$'],
        ['A route attaches only where its hostnames intersect the listener’s (shop.example.com). A JSON patch can replace the first hostname.', '^rule-2$'],
        ['Request the orders URL once more.', '^(client-0|route-0-[0-4])$']
      ],
      'gw-refgrant': [
        ['Request the orders URL and read the status code — it is neither 404 nor 503.', '^(client-0|req-0-[0-3])$'],
        ['Describe the route and read the ResolvedRefs condition and its reason.', '^(rule-0|service-0)$'],
        ['A cross-namespace reference is allowed by an object in the namespace that owns the target. Look there.', '^service-0$'],
        ['Apply the ready-made grant from your home directory (read it first: from HTTPRoute in default, to Service).', '^(service-0|rule-0)$'],
        ['Request the orders URL again.', '^(ep-[01]-[0-2]|endpoint-pod-[01])$']
      ],
      'gw-cert': [
        ['Request the /api URL over HTTPS and read curl’s error number.', '^(tls-terminate|client-1)$'],
        ['Listener health lives in the Gateway’s status — describe it and read the https listener’s conditions.', '^tls-terminate$'],
        ['certificateRefs names a Secret. Ask for that Secret by name.', '^(tls-terminate|rule-2)$'],
        ['kubectl has a dedicated generator for kubernetes.io/tls Secrets; the cert and key files are in your home directory.', '^tls-terminate$'],
        ['Repeat the HTTPS request without the insecure flag.', '^(tls-terminate|client-1|req-1-[0-3])$']
      ]
    },
    'config-propagation': {
      'volume-vs-env': [
        ['Change the LOG_LEVEL key of app-config to debug with a merge patch on its data.', '^(configmap-app-config|configmap-sheet-0)$'],
        ['Read the file the volume projects into the container, right away.', '^(volume-configmap|edge-configmap-mount)$'],
        ['The kubelet refreshes projected ConfigMap volumes on its sync loop — let about a minute and a half pass.', '^kubelet-led$'],
        ['Read the mounted file again.', '^volume-configmap$'],
        ['Now print the environment variable inside the container.', '^env-chip-1$'],
        ['Env vars are resolved at container start. Make the Deployment replace its pods.', '^(container-app|pod-boundary)$'],
        ['Print the environment variable once more.', '^env-chip-1$']
      ],
      'immutable': [
        ['Try the same data patch you would use on any ConfigMap and read the API server’s answer.', '^configmap-app-config$'],
        ['Read the ConfigMap back as YAML and look below data.', '^configmap-app-config$'],
        ['An immutable ConfigMap can only be deleted and recreated. Remove it (running pods keep their copy).', '^configmap-app-config$'],
        ['Create it again from a literal, with the new value.', '^(configmap-app-config|configmap-sheet-0)$'],
        ['Existing containers never re-read env vars. Replace the pods.', '^(container-app|pod-boundary)$'],
        ['Print the environment variable inside the container.', '^env-chip-1$']
      ],
      'missing-key': [
        ['List the pods and read the STATUS column.', '^(pod-boundary|container-app)$'],
        ['The kubelet writes its reason into the pod’s Events — describe the api pod by its label.', '^(env-chip-0|container-app)$'],
        ['Describe the Secret the env var references; describe lists key names and sizes, never values.', '^(secret-db-creds|secret-key-[0-2])$'],
        ['Add the missing key with a patch on stringData (the API server base64-encodes it into data).', '^(secret-db-creds|secret-key-1)$'],
        ['List the pods again — the kubelet retries container creation on its own.', '^(pod-boundary|container-app|env-chip-0)$']
      ]
    },
    /* v1.4.0 (2026-10-22) — worker-node troubleshooting on node-troubleshoot.glb */
    'node-troubleshoot': {
      'kubelet-203': [
        ['Start from the control plane: list the nodes and read the STATUS column.', '^(node-ready-lamp|node-chassis)$'],
        ['Describe the sick node and read every row under Conditions — who last wrote them?', '^(node-ready-lamp|edge-node-lease|node-lifecycle-controller)$'],
        ['The kubelet is a systemd unit on the node itself. Get onto node-01 and ask systemd how the unit is doing.', '^(kubelet|systemd-ring|kubelet-led)$'],
        ['203/EXEC means systemd could not execute ExecStart. kubeadm keeps that line in a drop-in next to the unit — read it.', '^kubelet-unit$'],
        ['Compare the ExecStart path with where the binary really is (which kubelet), then substitute it in place with sed.', '^(kubelet-unit|kubelet)$'],
        ['systemd still runs the definition it loaded before your edit. Tell it to re-read unit files.', '^(systemd-ring|kubelet-unit)$'],
        ['Restart the unit, then read its status again: Active should say running.', '^(kubelet|kubelet-led)$'],
        ['Back on the control plane, list the nodes once more.', '^(node-ready-lamp|edge-node-lease)$']
      ],
      'runtime-down': [
        ['Describe node-01 and read the Ready row’s message.', '^(node-ready-lamp|edge-kubelet-cri)$'],
        ['On node-01, ask the CRI CLI for running containers and read where it fails.', '^(cri-socket|edge-cri-containerd)$'],
        ['The runtime is its own systemd unit. Ask systemd about it on node-01.', '^containerd$'],
        ['Start the runtime and make sure it comes back after a reboot too (one systemctl verb with a flag does both).', '^(containerd|cri-socket)$'],
        ['List the nodes from the control plane.', '^node-ready-lamp$']
      ],
      'cni-missing': [
        ['List the nodes and read the STATUS column.', '^(node-ready-lamp|node-chassis)$'],
        ['Describe node-01: the Ready message names the subsystem that is not ready.', '^(node-ready-lamp|cni-conf)$'],
        ['On node-01, read the kubelet’s own journal for the same reason.', '^journal-page-[0-2]$'],
        ['The runtime looks for CNI config in one well-known directory. List it.', '^cni-conf$'],
        ['Calico’s DaemonSet pod writes that config when it starts. Make the DaemonSet roll its pods.', '^(cni-conf|cni-plugin)$'],
        ['List the nodes once more.', '^node-ready-lamp$']
      ],
      'disk-pressure': [
        ['Describe node-01: look at the pressure conditions, the taints and the events.', '^(disk-gauge|sim-disk-fill-[34]|sim-taint-flag)$'],
        ['List pods wide. Which QoS class went first, and where did their replacements land?', '^pod-besteffort-[01]$'],
        ['On node-01, check how full the root filesystem is.', '^(disk-gauge|disk-fill-[0-2]|sim-disk-fill-[34])$'],
        ['Unused container images are the usual culprit. The CRI CLI can remove every image no container uses.', '^(containerd|sim-disk-fill-[34])$'],
        ['Describe node-01 again and read DiskPressure.', '^(disk-gauge|kubelet-config)$']
      ]
    },
    /* v1.5.0 (2026-10-23) — Service + DNS troubleshooting on service-dns.glb */
    'service-dns': {
      'target-port': [
        ['Start from the client: probe the api Service by name from the web Deployment and read curl’s exit reason.', '^(client-pod|edge-client-api|svc-api)$'],
        ['A Service’s backends are recorded in EndpointSlices labelled with its name. Are there addresses, and on which port?', '^(endpointslice-api|edge-svc-pod-[01])$'],
        ['Describe the Service and compare Port with TargetPort.', '^(svc-api|svc-api-port)$'],
        ['The Deployment’s pod template says which port the container exposes. Describe it.', '^(container-port-[01]|api-pod-[01])$'],
        ['Ports are a list merged on the `port` key: patch the entry for port 80 with the container’s port as its target.', '^(svc-api-port|container-port-[01])$'],
        ['Probe api from web once more.', '^(edge-client-api|svc-api)$']
      ],
      'coredns-corefile': [
        ['Use the dnsutils debug pod in ns shop and look up the api Service. Is the answer a timeout or a refusal?', '^(client-pod|edge-client-dns|svc-kube-dns)$'],
        ['CoreDNS runs as pods labelled k8s-app=kube-dns in kube-system. List them and read STATUS and RESTARTS.', '^(coredns-[01]|sim-crash-ring-[01])$'],
        ['A crash-looping pod tells you why in its log. Read the CoreDNS logs by label.', '^(coredns-[01]|corefile)$'],
        ['Its configuration is a ConfigMap. Save it as YAML into a file you can edit (redirect the output).', '^corefile$'],
        ['The log named a directive CoreDNS does not know. Substitute the correct plugin name in place.', '^corefile$'],
        ['Send the edited file back to the API server.', '^(corefile|ns-kube-system)$'],
        ['Look up api again from the debug pod.', '^(edge-client-dns|svc-kube-dns)$']
      ],
      'dns-egress': [
        ['From the debug pod in ns shop, look up api and note how it fails (timed out, not refused).', '^(edge-client-dns|client-pod)$'],
        ['Skip DNS: probe the api Service by its ClusterIP from web. If that works, routing is fine.', '^(svc-api|edge-client-api)$'],
        ['Something filters egress in this namespace only. List the policies there and describe the deny one.', '^(netpol-tablet|sim-netpol-wall)$'],
        ['Policies are additive allow-lists: add one that lets every shop pod reach the kube-dns pods on port 53, both protocols. There is a lab file for it.', '^(sim-netpol-wall|svc-kube-dns)$'],
        ['Look up api again from the debug pod.', '^(edge-client-dns|coredns-[01])$']
      ],
      'cross-ns-fqdn': [
        ['Read the web Deployment’s log: which name does it fail to look up?', '^(client-pod|edge-client-db)$'],
        ['Ask the same short name from the debug pod and read the status.', '^(sim-nxdomain-flag|resolv-conf)$'],
        ['Every pod gets its DNS settings from a file. Read its search list and ndots.', '^resolv-conf$'],
        ['List Services across all namespaces and find the database.', '^(svc-db|ns-data)$'],
        ['Set the web Deployment’s DB_HOST to a name that includes the database’s namespace.', '^(client-pod|svc-db)$'],
        ['Read web’s log again.', '^(edge-client-db|db-pod)$']
      ]
    },
    /* v1.6.0 (2026-10-27) — CNI on cni-pod-network.glb */
    'cni-network': {
      'no-cni': [
        ['Start with the cluster’s view of its nodes and read the STATUS column.', '^(node|kubelet)-[01]$'],
        ['Cluster DNS runs as pods in kube-system. Are they scheduled at all?', '^coredns$'],
        ['Describe a node and read the message on its Ready condition — it names the subsystem.', '^kubelet-[01]$'],
        ['The container runtime looks for network plugin config in one well-known directory on each node. List it.', '^(cni-bridge|kubelet-[01])$'],
        ['A ready-made Calico manifest sits in your home directory. Read it, then send it to the API server.', '^(cni-bridge|veth-\\d-\\d)$'],
        ['Look at the nodes again.', '^(node|kubelet)-[01]$'],
        ['Check the DNS pods in kube-system again.', '^(coredns|pod-1-\\d)$']
      ],
      'cidr-overlap': [
        ['From the client Deployment, ping the web pod that runs on node-1 (wide pod output lists IPs and nodes).', '^overlay-arc-\\d-\\d$'],
        ['Now ping the web pod that shares node-0 with the client.', '^(cni-bridge|veth-0-\\d)$'],
        ['Wide node output shows each node’s internal address. Do the node and pod ranges overlap?', '^node-[01]$'],
        ['Calico hands out pod addresses from IP pools. Read the default pool as YAML and find its cidr.', '^(cni-bridge|overlay-arc-\\d-\\d)$'],
        ['There is a replacement pool manifest in your home directory with a range outside the VPC. Apply it.', '^cni-bridge$'],
        ['Mark the old pool disabled with a merge patch on its spec, so no new pod gets an address from it.', '^cni-bridge$'],
        ['Pods keep their address for life. Restart every Deployment in default, and CoreDNS in kube-system.', '^pod-\\d-\\d$'],
        ['Ping the node-1 web pod again — at its new address.', '^overlay-arc-\\d-\\d$']
      ],
      'no-kube-proxy': [
        ['From the client Deployment, curl the web Service by its name and read curl’s exit reason.', '^(coredns|cluster-ip)$'],
        ['Skip the Service: curl one web pod directly by its pod IP.', '^(overlay-arc-\\d-\\d|pod-1-\\d)$'],
        ['Now curl the Service’s ClusterIP. Something has to turn that virtual IP into a pod address.', '^cluster-ip$'],
        ['That something runs as a DaemonSet on every node. List the DaemonSets in kube-system.', '^(node|kubelet)-[01]$'],
        ['kubeadm can re-install one of its essential addons on a running cluster, phase by phase.', '^cluster-ip$'],
        ['curl the ClusterIP again.', '^cluster-ip$'],
        ['curl web by name again — DNS also travels through a ClusterIP.', '^(coredns|cluster-ip)$']
      ]
    },
    /* v1.6.0 (2026-10-27) — Istio mTLS on service-mesh-sidecar.glb */
    'mesh-mtls': {
      'strict-reset': [
        ['From the frontend Deployment in shop, call the payments headers endpoint and read curl’s error number.', '^(app-0|dataplane-hop-\\d)$'],
        ['Peer authentication policy lives in the server’s namespace. List it there and read the MODE.', '^(mtls-1|sidecar-1)$'],
        ['Count the containers in the frontend pods (READY column). A meshed pod has one more.', '^(app-0|sidecar-0)$'],
        ['Injection is switched on per namespace by a label. Show shop’s labels.', '^app-0$'],
        ['Add the injection label to the shop namespace.', '^(mesh-control-plane|cp-halo)$'],
        ['The webhook only runs when a pod is created. Make the frontend Deployment replace its pods.', '^(sidecar-0|xds-0-\\d)$'],
        ['Call payments again and look for the client certificate header.', '^(mtls-0|mtls-1|dataplane-hop-\\d)$']
      ],
      'permissive-to-strict': [
        ['Call the payments headers endpoint from frontend. Which header would prove a client certificate was used?', '^(app-0|dataplane-hop-\\d)$'],
        ['List the peer authentication policy in the payments namespace and read the MODE.', '^(mtls-1|sidecar-1)$'],
        ['Mesh the client first: label its namespace for injection, then recreate its pods.', '^(sidecar-0|mesh-control-plane)$'],
        ['List the shop pods and read the READY column.', '^(app-0|sidecar-0)$'],
        ['Call payments again: the hop should now carry the client’s SPIFFE identity.', '^(mtls-0|dataplane-hop-\\d)$'],
        ['Every client is meshed now. Apply the STRICT policy manifest from your home directory.', '^mtls-1$'],
        ['Call payments one more time.', '^(mtls-0|mtls-1|dataplane-hop-\\d)$']
      ],
      'istiod-down': [
        ['Call payments from frontend. The control plane is not in the request path.', '^(dataplane-hop-\\d|mtls-[01])$'],
        ['Redeploy the frontend Deployment the usual way.', '^(app-0|sidecar-0)$'],
        ['When a ReplicaSet cannot create pods it records why. List the events in shop.', '^(mesh-control-plane|cp-halo)$'],
        ['The webhook is served by the control plane. List the Deployments in istio-system.', '^(mesh-control-plane|cp-halo)$'],
        ['Scale the control plane back to one replica.', '^(mesh-control-plane|cp-halo)$'],
        ['Ask istioctl whether every proxy is in sync with the control plane.', '^xds-[01]-\\d$']
      ]
    },
    /* v1.7.0 (2026-10-29) — CKS workload security on cks-pod-security.glb */
    'cks-pod-security': {
      'psa-enforce': [
        ['Pod Security levels are set per namespace with labels. List the payments namespace with its labels showing.', '^(psa-label|ns-payments)$'],
        ['Before enforcing, ask the API server what would break: the same label command, as a server-side dry run, with overwrite allowed.', '^(psa-gate|psa-label)$'],
        ['Now set the enforce mode label to the restricted level for real.', '^(psa-label|psa-gate)$'],
        ['There is a lab manifest for a privileged debug pod. Try to create it and read who refuses it.', '^(psa-gate|sim-psa-reject)$']
      ],
      'harden-pod': [
        ['Start from the workload: how many of its replicas are ready?', '^(payments-pod|edge-pod-apiserver)$'],
        ['A ReplicaSet that cannot create pods records why. List the namespace’s events and read the message.', '^(sim-psa-reject|psa-gate)$'],
        ['The lab has three versions of the Deployment. Read them and apply the one that sets non-root, no escalation, drop ALL and a RuntimeDefault seccomp profile.', '^(sec-context|seccomp-filter)$'],
        ['List the pods in payments again.', '^(payments-pod|psa-gate)$'],
        ['Run the identity command inside the Deployment’s container.', '^(payments-pod|sec-context)$'],
        ['The kernel reports a process’s seccomp mode in its /proc status file. Read the Seccomp line for PID 1.', '^(seccomp-filter|node-kernel)$']
      ],
      'default-deny': [
        ['From the attacker pod in default, call the payments-api Service on 8080.', '^(attacker-pod|edge-attacker-api)$'],
        ['The lab has a policy that selects every pod in payments with no ingress rules. Apply it.', '^(sim-netpol-wall|netpol-tablet)$'],
        ['Call payments-api from the attacker pod again. A dropped packet looks like a timeout.', '^(edge-attacker-api|sim-netpol-wall)$'],
        ['Now call it from the web Deployment in frontend, the legitimate client.', '^(frontend-pod|edge-frontend-api)$'],
        ['Policies add up: apply the lab policy that admits namespace frontend on TCP 8080 to the payments-api pods.', '^(netpol-tablet|edge-frontend-api)$'],
        ['Call payments-api from frontend once more.', '^(frontend-pod|edge-frontend-api)$']
      ],
      'sa-least-privilege': [
        ['Impersonate the ServiceAccount (system:serviceaccount:<ns>:<name>) and ask whether it may get Secrets across all namespaces.', '^(sa-token|secrets-vault|edge-token-secrets)$'],
        ['Cluster-wide grants come from ClusterRoleBindings. List them wide enough to see the ServiceAccount column.', '^(rbac-binding|sim-cluster-admin-crown)$'],
        ['Remove the binding that ties api-sa to cluster-admin.', '^(sim-cluster-admin-crown|rbac-binding)$'],
        ['Create a namespaced Role in payments that can only read ConfigMaps (get, list, watch).', '^rbac-binding$'],
        ['Bind that Role to the ServiceAccount (namespace:name form) in payments.', '^(rbac-binding|sa-token)$'],
        ['Ask the Secrets question again as api-sa.', '^(secrets-vault|edge-token-secrets)$'],
        ['Ask whether api-sa may list ConfigMaps in payments.', '^(rbac-binding|ns-payments)$']
      ],
      'audit-log': [
        ['The API server is a static pod: read its manifest and look at every audit flag.', '^(kube-apiserver|audit-log)$'],
        ['The policy file says what is logged and at which level. Read it.', '^audit-policy$'],
        ['The log path flag is there, just commented out. Remove the comment marker in place in the manifest.', '^(sim-audit-gap|audit-log)$'],
        ['The kubelet recreates the static pod after a manifest change. List it in kube-system by its component label.', '^(kube-apiserver|control-plane)$'],
        ['Generate the event you want to find: read that Secret once as admin.', '^(secret-db-creds|kube-apiserver)$'],
        ['Read the last line of the audit log file and check what it does and does not contain.', '^(audit-log|edge-api-audit)$']
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
    [/\b(system|systemd) ?(control|ctl|cuttle|c t l)\b/g, 'systemctl'], [/\bjournal ?(control|ctl|c t l)\b/g, 'journalctl'], [/\bdaemon reload\b/g, 'daemon-reload'],
    [/\bm v\b/g, 'mv'], [/\bl s\b/g, 'ls'], [/\bp v c\b/g, 'pvc'], [/\bp v\b/g, 'pv'], [/\bh p a\b/g, 'hpa'], [/\bt l s\b/g, 'tls'], [/\br d s\b/g, 'rds'], [/\bd n s\b/g, 'dns'],
    [/\bnet pol\b|\bnetwork ?polic(y|ies)\b/g, 'networkpolicy'],
    [/\bname ?space\b/g, 'namespace'], [/\brole ?binding(s?)\b/g, 'rolebinding$1'], [/\bcluster ?role ?binding(s?)\b/g, 'clusterrolebinding$1'], [/\bcluster ?role\b/g, 'clusterrole'], [/\bservice ?account\b/g, 'serviceaccount'],
    [/\bstorage ?class(es)?\b/g, 'storageclass$1'], [/\bendpoint ?slices?\b/g, 'endpointslices'], [/\bdaemon ?sets?\b/g, 'daemonsets'],
    [/\bistio ?(control|ctl|cuttle|c t l)\b/g, 'istioctl'], [/\bpeer ?authentications?\b/g, 'peerauthentication'], [/\bi ?p ?pool(s?)\b/g, 'ippool$1'], [/\b(cube|kube) ?(adm|admin|a d m)\b/g, 'kubeadm'], [/\bproxy status\b/g, 'proxy-status'],
    [/\bn ?s ?look ?up\b/g, 'nslookup'], [/\bcore ?d n s\b|\bcore ?dns\b/g, 'coredns'], [/\bconfig ?maps?\b/g, 'configmap'], [/\bresolv(e)? dot conf\b/g, 'resolv.conf'],
    [/\bsec ?comp\b/g, 'seccomp'], [/\bdry run\b/g, 'dry-run'], [/\bcan i\b/g, 'can-i'], [/\bsudo\b/g, 'sudo'],
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
    VERSION: '1.7.0',
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
    promptFor: promptFor,
    fromSpeech: fromSpeech
  };
});
