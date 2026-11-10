/**
 * IL Immersive Sims v1.11.0 (2026-11-05; v1.10.0 2026-11-04; v1.9.0 2026-11-03; v1.8.0 2026-11-02; v1.7.0 2026-10-29; v1.6.0 2026-10-23; v1.5.0 2026-10-22; v1.4.0 2026-10-21; v1.3.0 2026-10-19; v1.2.0 2026-10-08; v1.1.0 2026-10-07; v1.0.0 2026-10-06) — interactive state machines that drive authored .glb scenes.
 *
 * State changes the scene: each sim derives per-node styles (tint / glow / pulse / hide / reveal)
 * from a small state object using the documented rules (Raft quorum, AWS Multi-AZ failover,
 * AWS IAM policy evaluation, NetworkPolicy isolation, RBAC binding scope, scheduler filter/score,
 * HPA autoscaling/v2 math; v1.2.0: PV/PVC binding + reclaim, Ingress pathType/endpoints/TLS, ConfigMap/Secret
 * propagation, CNI readiness/CIDR/Service VIP/DNS, mesh injection + mTLS modes, control-plane component failures).
 * Keyed answers vary by index in the data as well; option order is shuffled per attempt so the keyed answer is not positional. Predict-then-reveal checkpoints record correctness + latency.
 *
 * Honest scope: rules are computed in the browser. No live cluster, no AWS account, no hosted fleet.
 * Pure + UMD so `node --test` exercises the same logic the browser runs.
 *
 * Toggle `risk`: which state is the risky one for colouring — 'off' (default), 'on', or 'none'.
 *
 * v1.3.0 (2026-10-19): verdictTone() maps the whole verdict vocabulary to ok / warn / bad so unsafe states
 * (data-deleted, exposed-at-rest, …) never render in the healthy cyan; reclaim Delete hides the backing disk.
 *
 * v1.4.0 (2026-10-21): gateway-api drill on the same authored ingress-gateway.glb — GatewayClass with no controller
 * (Pending, no ADDRESS), route hostnames vs listener (NoMatchingListenerHostname → 404), cross-namespace backendRef
 * without ReferenceGrant (RefNotPermitted → 500, as the spec requires), listener certificateRefs missing
 * (InvalidCertificateRef → listener not programmed), PathPrefix vs Exact. No new asset; rules address existing nodes.
 *
 * v1.5.0 (2026-10-22): node-troubleshoot drill on a NEW authored asset, node-troubleshoot.glb (kit-v2 + Blender CLI
 * polish): kubelet 203/EXEC from a bad ExecStart, daemon-reload after a unit edit, containerd down (containers survive
 * via shims, Ready=False), CNI config missing (NetworkPluginNotReady), nodefs DiskPressure (BestEffort evicted first).
 * Troubleshooting is 30% of the CKA; it previously had one drill.
 *
 * v1.6.0 (2026-10-23): service-dns drill on a NEW authored asset, service-dns.glb (kit-v2 + Blender CLI polish):
 * Service selector matches nothing (empty EndpointSlice → kube-proxy reject), targetPort ≠ containerPort, CoreDNS
 * Corefile parse error (CrashLoopBackOff → lookups refused, ClusterIPs still work), namespace default-deny egress without
 * a kube-dns:53 rule (lookups time out), short name across namespaces (search list → NXDOMAIN). svcDnsResolve() models
 * the pod resolv.conf search list with ndots:5. The other half of CKA Troubleshooting (30%).
 *
 * v1.7.0 (2026-10-29): the first CKS drill, cks-pod-security, on a NEW authored asset cks-pod-security.glb (kit-v2 +
 * Blender CLI polish): Pod Security Admission enforce=restricted vs a privileged template (Deployment accepted,
 * ReplicaSet FailedCreate), unlabelled namespace = privileged by default, no seccompProfile = Unconfined (Seccomp: 0),
 * no NetworkPolicy = allow-all, default-deny ingress without an allow rule (egress untouched), ServiceAccount bound
 * to cluster-admin, audit policy without --audit-log-path (no backend). New verdict 'exposed' (tone bad).
 *
 * v1.8.0 (2026-11-02): the second CKS drill, cks-supply-chain (Supply Chain Security, 20% of the CKS), on a NEW
 * authored asset cks-supply-chain.glb (kit-v2 + Blender CLI polish): no built-in registry allow-list, a
 * ValidatingAdmissionPolicy that matches Deployments denies the apply itself, mutable tags vs @sha256 digests, a signed
 * image with CRITICAL CVEs is still admitted (signature ≠ safety), a Trivy --exit-code 1 gate stops push + sign, a
 * registry allow-list does not prove provenance, signature verification at admission denies an unsigned digest.
 *
 * v1.9.0 (2026-11-03): the third CKS drill, cks-runtime-security (Monitoring, Logging & Runtime Security, 20% of the
 * CKS, plus AppArmor from System Hardening), on a NEW authored asset cks-runtime-security.glb (kit-v2 + Blender CLI
 * polish): an RCE shell never touches the API server (audit is blind), Falco detects but does not block, a Running
 * Falco pod with a disabled rule sees nothing, an AppArmor profile that is not loaded on the node stops the container
 * (CreateContainerError), AppArmor deny-write returns Permission denied, readOnlyRootFilesystem returns Read-only file
 * system, and the audit log records a pods/exec request but never the commands typed inside it.
 *
 * v1.10.0 (2026-11-04): the fourth CKS drill, cks-cluster-hardening (Cluster Setup: CIS benchmark with kube-bench), on a
 * NEW authored asset cks-cluster-hardening.glb (kit-v2 + Blender CLI polish): anonymous + AlwaysAllow serves the kubelet API
 * to anyone, Webhook turns system:anonymous into 403, the read-only port 10255 leaks pods with no auth (kube-bench WARN,
 * Manual), kube-bench PASSes an edited config.yaml the kubelet has not reloaded, etcd data dir 755 (1.1.11), API server
 * --profiling (1.2.15, static pod re-created on save), and a ServiceAccount token under AlwaysAllow.
 *
 * v1.11.0 (2026-11-05): the fifth CKS drill, cks-static-analysis (Supply Chain Security: static analysis of user workloads
 * with kubesec and KubeLinter), on a NEW authored asset cks-static-analysis.glb (kit-v2 + Blender CLI polish): kubesec sums
 * rule points (privileged -30 → "Failed", exit 2), a scan blocks nothing without a gate (|| true), kubesec cannot see a
 * literal secret while KubeLinter env-var-secret can, an ignore-check annotation silences one check only, runAsNonRoot over a
 * root image passes both scanners and fails at the kubelet (CreateContainerConfigError), advise vs failed checks, and a
 * kubesec "critical" entry under a passing score.
 *
 * Node naming contract (scripts/author_immersive_glb.py):
 *   sim-*      hidden unless a rule sets show:true
 *   *_LOD1     Blender LOD duplicates — players skip them
 */
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.ILImmersiveSims = api;
})(typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this), function () {
  'use strict';

  var TINTS = {
    ok: [0.369, 0.918, 0.831],
    gold: [0.831, 0.659, 0.325],
    deny: [0.86, 0.26, 0.24],
    warn: [0.95, 0.55, 0.18],
    down: [0.16, 0.18, 0.22],
    muted: [0.32, 0.36, 0.42]
  };

  function rule(match, style) {
    var r = { match: match };
    for (var k in style) if (Object.prototype.hasOwnProperty.call(style, k)) r[k] = style[k];
    return r;
  }

  /* ── Raft / etcd quorum (CKA) ─────────────────────────────────────────── */
  function etcdQuorum(n, up) { return { quorum: Math.floor(n / 2) + 1, writable: up >= Math.floor(n / 2) + 1 }; }

  var etcd = {
    id: 'etcd-quorum',
    title: 'etcd quorum failure drill',
    cert: 'CKA',
    glb: '/assets/immersive/cka-etcd-quorum.glb',
    initial: { m0: true, m1: true, m2: true },
    toggles: [
      { id: 'm0', label: 'etcd-0', on: 'up', off: 'down' },
      { id: 'm1', label: 'etcd-1', on: 'up', off: 'down' },
      { id: 'm2', label: 'etcd-2', on: 'up', off: 'down' }
    ],
    scenarios: [
      { id: 'lose-one', label: 'Fail 1 member', set: { m0: true, m1: false, m2: true },
        predict: { q: 'etcd-1 crashes. Can kubectl apply still write to the cluster?',
          options: ['Yes — 2 of 3 is still a quorum', 'No — any member loss freezes writes', 'Only reads, writes queue until it returns'],
          answer: 0, why: 'Raft needs floor(n/2)+1 votes: 2 of 3. The cluster tolerates one failure; a 3-member cluster cannot tolerate two.' } },
      { id: 'lose-leader', label: 'Kill the leader', set: { m0: false, m1: true, m2: true },
        predict: { q: 'The leader (etcd-0) dies. What happens?',
          options: ['Followers elect a new leader; writes resume after the election timeout', 'Cluster is read-only until etcd-0 is restored', 'kube-apiserver promotes itself to leader'],
          answer: 0, why: 'Remaining members still form a quorum (2/3), so a follower times out, starts an election and becomes leader.' } },
      { id: 'lose-two', label: 'Fail 2 members', set: { m0: true, m1: false, m2: false },
        predict: { q: 'Two of three members are down. Can you create a Deployment?',
          options: ['No — 1/3 has no quorum; writes fail (restore from snapshot or recover members)', 'Yes — the surviving leader keeps accepting writes', 'Yes, but only in the default namespace'],
          answer: 0, why: '1 of 3 is below quorum (2). The survivor cannot commit; the API server returns errors for writes. CKA fix path: etcdctl snapshot restore.' } },
      { id: 'heal', label: 'Restore all', set: { m0: true, m1: true, m2: true } }
    ],
    derive: function (s) {
      var ups = [s.m0, s.m1, s.m2];
      var up = ups.filter(Boolean).length;
      var q = etcdQuorum(3, up);
      var leader = -1;
      if (q.writable) { for (var i = 0; i < 3; i++) if (ups[i]) { leader = i; break; } }
      var rules = [];
      for (var m = 0; m < 3; m++) {
        if (!ups[m]) rules.push(rule('^etcd-(member|heart)-' + m + '$', { tint: 'down', glow: 0 }));
        else if (m === leader) rules.push(rule('^etcd-(member|heart)-' + m + '$', { tint: 'gold', glow: 0.7, pulse: true }));
        else rules.push(rule('^etcd-(member|heart)-' + m + '$', { tint: q.writable ? 'ok' : 'warn', glow: 0.3, pulse: !q.writable }));
      }
      var links = [[0, 1], [1, 2], [2, 0]];
      links.forEach(function (l) {
        var alive = ups[l[0]] && ups[l[1]];
        rules.push(rule('^raft-link-' + l[0] + '-' + l[1] + '$', alive ? { tint: 'ok', glow: 0.35 } : { tint: 'down', glow: 0 }));
      });
      rules.push(rule('^apiserver-front$', q.writable ? { tint: 'ok', glow: 0.25 } : { tint: 'deny', glow: 0.8, pulse: true }));
      return {
        verdict: q.writable ? (up === 3 ? 'healthy' : 'degraded') : 'down',
        metrics: { up: up, quorum: q.quorum, writable: q.writable, leader: leader },
        caption: up + '/3 members up · quorum needs ' + q.quorum + ' · ' +
          (q.writable ? 'writes OK · leader etcd-' + leader : 'NO QUORUM — API writes fail'),
        rules: rules
      };
    }
  };

  /* ── AWS Multi-AZ resilience (SAA-C03 domain 2) ───────────────────────── */
  function awsHa(s) {
    var azUp = { a: !!s.azA, b: !!s.azB };
    var app = azUp.a || azUp.b;
    var dbWriter = null, failover = false;
    if (azUp.a) dbWriter = 'a';
    else if (s.multiAz && azUp.b) { dbWriter = 'b'; failover = true; }
    var serving = app && dbWriter !== null;
    var surge = null;
    if (azUp.a && !azUp.b) surge = 'a';
    if (azUp.b && !azUp.a) surge = 'b';
    return { azUp: azUp, app: app, dbWriter: dbWriter, failover: failover, serving: serving, surge: surge };
  }

  var awsAz = {
    id: 'aws-az-failure',
    title: 'AZ failure drill — ALB · ASG · RDS Multi-AZ',
    cert: 'AWS SAA-C03 / CLF-C02',
    glb: '/assets/immersive/aws-vpc-multi-az.glb',
    initial: { azA: true, azB: true, multiAz: true },
    toggles: [
      { id: 'azA', label: 'us-east-1a', on: 'up', off: 'outage' },
      { id: 'azB', label: 'us-east-1b', on: 'up', off: 'outage' },
      { id: 'multiAz', label: 'RDS Multi-AZ', on: 'on', off: 'off' }
    ],
    scenarios: [
      { id: 'az-a-outage', label: 'Lose us-east-1a', set: { azA: false, azB: true, multiAz: true },
        predict: { q: 'us-east-1a goes dark. RDS Multi-AZ is ON. What does the customer see?',
          options: ['App stays up: ALB drains 1a, RDS fails over to the 1b standby, same endpoint', 'Outage until you restore an RDS snapshot', 'Route 53 moves traffic to another Region automatically'],
          answer: 0, why: 'ALB health checks stop routing to unhealthy targets; Multi-AZ RDS promotes the synchronous standby and the endpoint CNAME flips (typically 60–120 s); the ASG relaunches capacity in the healthy AZ.' } },
      { id: 'single-az-db', label: 'Lose 1a with single-AZ RDS', set: { azA: false, azB: true, multiAz: false },
        predict: { q: 'Same outage, but RDS was deployed Single-AZ. Is the app serving?',
          options: ['No — web tier survives but there is no standby; the database is down until restore', 'Yes — a read replica takes over automatically', 'Yes — the ASG recreates the database in 1b'],
          answer: 0, why: 'Single-AZ RDS has no standby. Read replicas are for read scaling and need a manual promote. Exam keyword: “high availability” → Multi-AZ.' } },
      { id: 'az-b-outage', label: 'Lose us-east-1b', set: { azA: true, azB: false, multiAz: true },
        predict: { q: 'us-east-1b fails instead. Does the database fail over?',
          options: ['No — the writer is in 1a; RDS keeps serving and re-creates a standby', 'Yes — any AZ loss forces a failover', 'Yes, and writes are lost'],
          answer: 0, why: 'Only the standby lived in 1b. The primary keeps serving; the ALB drains 1b and the ASG rebalances into 1a.' } },
      { id: 'heal', label: 'Restore both AZs', set: { azA: true, azB: true, multiAz: true } }
    ],
    derive: function (s) {
      var h = awsHa(s);
      var rules = [];
      ['a', 'b'].forEach(function (az) {
        if (!h.azUp[az]) {
          rules.push(rule('^az-' + az + '-', { tint: 'down', glow: 0 }));
          rules.push(rule('^az-' + az + '-pad$', { tint: 'deny', glow: 0.35, pulse: true }));
        }
      });
      if (h.surge) rules.push(rule('^sim-az-' + h.surge + '-ec2-surge-', { show: true, tint: 'ok', glow: 0.6, pulse: true }));
      if (h.dbWriter) {
        rules.push(rule('^az-' + h.dbWriter + '-rds$', { tint: 'gold', glow: h.failover ? 0.85 : 0.45, pulse: h.failover }));
        rules.push(rule('^az-' + h.dbWriter + '-rds-role-ring$', { tint: 'ok', glow: 0.7 }));
      }
      var bothUp = h.azUp.a && h.azUp.b;
      rules.push(rule('^edge-rds-sync-replication$', bothUp && s.multiAz ? { tint: 'gold', glow: 0.4 } : { tint: 'down', glow: 0 }));
      if (!s.multiAz) rules.push(rule('^az-b-rds(-role-ring)?$', { tint: 'down', glow: 0 }));
      rules.push(rule('^rds-endpoint-dns$', h.dbWriter ? { tint: h.failover ? 'warn' : 'ok', glow: h.failover ? 0.6 : 0.2, pulse: h.failover } : { tint: 'deny', glow: 0.8, pulse: true }));
      rules.push(rule('^alb$', h.serving ? { tint: 'gold', glow: 0.3 } : { tint: 'deny', glow: 0.7, pulse: true }));
      if (!h.app) rules.push(rule('^(igw|edge-igw-alb-[ab]|internet-users)$', { tint: 'deny', glow: 0.5 }));
      var cap;
      if (!h.serving) cap = h.app ? 'OUTAGE — web tier up but no database writer (Single-AZ RDS lost with its AZ)' : 'OUTAGE — no healthy AZ';
      else if (h.failover) cap = 'Serving · RDS failed over to us-east-1b standby (endpoint CNAME flipped) · ASG rebalancing into 1b';
      else if (h.surge) cap = 'Serving · ALB draining the failed AZ · ASG launching replacements in us-east-1' + h.surge;
      else cap = 'Serving · 2 AZs healthy · RDS writer us-east-1a, sync standby ' + (s.multiAz ? 'us-east-1b' : 'none (Single-AZ)');
      return {
        verdict: h.serving ? ((h.failover || h.surge) ? 'degraded' : 'healthy') : 'down',
        metrics: h,
        caption: cap,
        rules: rules
      };
    }
  };

  /* ── AWS IAM policy evaluation (single account) ───────────────────────── */
  /** Returns { decision, at, trace:{gate→'pass'|'skip'|'grant'|'stop'|'n/a'} } per AWS "Policy evaluation logic" (single account). */
  function iamDecide(s) {
    var tr = { 'explicit-deny': 'n/a', 'scp': 'n/a', 'resource-policy': 'n/a', 'identity-policy': 'n/a', 'permission-boundary': 'n/a', 'session-policy': 'n/a' };
    function out(decision, at) { return { decision: decision, at: at, trace: tr }; }
    if (s.explicitDeny) { tr['explicit-deny'] = 'stop'; return out('explicit-deny', 'explicit-deny'); }
    tr['explicit-deny'] = 'pass';
    if (s.inOrg) {
      if (!s.scpAllow) { tr.scp = 'stop'; return out('implicit-deny', 'scp'); }
      tr.scp = 'pass';
    } else tr.scp = 'skip';
    if (s.resourceAllow) { tr['resource-policy'] = 'grant'; return out('allow', 'resource-policy'); }
    tr['resource-policy'] = 'skip';
    if (!s.identityAllow) { tr['identity-policy'] = 'stop'; return out('implicit-deny', 'identity-policy'); }
    tr['identity-policy'] = 'pass';
    if (s.boundarySet) {
      if (!s.boundaryAllow) { tr['permission-boundary'] = 'stop'; return out('implicit-deny', 'permission-boundary'); }
      tr['permission-boundary'] = 'pass';
    } else tr['permission-boundary'] = 'skip';
    if (s.sessionSet) {
      if (!s.sessionAllow) { tr['session-policy'] = 'stop'; return out('implicit-deny', 'session-policy'); }
      tr['session-policy'] = 'pass';
    } else tr['session-policy'] = 'skip';
    return out('allow', 'identity-policy');
  }
  var IAM_ORDER = ['explicit-deny', 'scp', 'resource-policy', 'identity-policy', 'permission-boundary', 'session-policy'];

  var iam = {
    id: 'iam-eval',
    title: 'IAM policy evaluation walk',
    cert: 'AWS SAA-C03 / CLF-C02',
    glb: '/assets/immersive/aws-iam-policy-eval.glb',
    initial: { explicitDeny: false, inOrg: true, scpAllow: true, resourceAllow: false, identityAllow: true,
      boundarySet: false, boundaryAllow: true, sessionSet: false, sessionAllow: true },
    toggles: [
      { id: 'explicitDeny', label: 'Explicit Deny', on: 'present', off: 'none' },
      { id: 'scpAllow', label: 'SCP allows', on: 'yes', off: 'no' },
      { id: 'resourceAllow', label: 'Bucket policy grants ARN', on: 'yes', off: 'no' },
      { id: 'identityAllow', label: 'Identity policy allows', on: 'yes', off: 'no' },
      { id: 'boundarySet', label: 'Boundary attached', on: 'yes', off: 'no' },
      { id: 'boundaryAllow', label: 'Boundary allows', on: 'yes', off: 'no' }
    ],
    scenarios: [
      { id: 'deny-wins', label: 'Allow + explicit Deny', set: { explicitDeny: true, identityAllow: true, scpAllow: true, resourceAllow: false, boundarySet: false },
        predict: { q: 'The role has AdministratorAccess, and a second policy says Deny s3:DeleteObject. Result?',
          options: ['Explicit deny — a Deny in any policy always wins', 'Allow — AdministratorAccess overrides', 'Depends which policy was attached last'],
          answer: 0, why: 'Evaluation starts by collecting every applicable statement; any matching explicit Deny ends evaluation with Deny.' } },
      { id: 'scp-blocks', label: 'SCP does not allow', set: { explicitDeny: false, scpAllow: false, identityAllow: true, resourceAllow: false, boundarySet: false },
        predict: { q: 'The account admin has full IAM permissions, but the org SCP does not allow s3:DeleteObject. Result?',
          options: ['Denied (implicit) — SCPs set the maximum; they never grant', 'Allowed — SCPs do not apply to admins', 'Allowed — identity policies take precedence'],
          answer: 0, why: 'SCPs (and RCPs) are guardrails on the whole member account, including its admins. No SCP Allow → implicit deny.' } },
      { id: 'boundary-caps', label: 'Boundary caps the role', set: { explicitDeny: false, scpAllow: true, identityAllow: true, resourceAllow: false, boundarySet: true, boundaryAllow: false },
        predict: { q: 'Identity policy allows the action, but the permissions boundary does not. Result?',
          options: ['Denied (implicit) — effective permissions are the intersection', 'Allowed — the identity policy grants it', 'Explicit deny'],
          answer: 0, why: 'A permissions boundary is a ceiling. Identity ∩ boundary must allow; it is an implicit deny, not an explicit one.' } },
      { id: 'resource-grant', label: 'Only the bucket policy allows', set: { explicitDeny: false, scpAllow: true, identityAllow: false, resourceAllow: true, boundarySet: false },
        predict: { q: 'Same account: the user has no identity policy for S3, but the bucket policy names the user ARN. Result?',
          options: ['Allowed — within one account a resource policy grant is enough', 'Denied — identity policy is always required', 'Denied — bucket policies only apply cross-account'],
          answer: 0, why: 'Within a single account, an Allow in either the identity-based or the resource-based policy is sufficient (absent Deny/SCP limits) when the bucket policy names the IAM user ARN. Grants to a role session are still capped by boundaries/session policies; cross-account needs both sides.' } },
      { id: 'reset', label: 'Reset request', set: { explicitDeny: false, inOrg: true, scpAllow: true, resourceAllow: false, identityAllow: true, boundarySet: false, boundaryAllow: true } }
    ],
    derive: function (s) {
      var d = iamDecide(s);
      var rules = [];
      var stopTint = d.decision === 'explicit-deny' ? 'deny' : 'warn';
      IAM_ORDER.forEach(function (gid) {
        var t = d.trace[gid];
        var sel = '^gate-' + gid + '-(post|lintel)';
        if (t === 'pass') rules.push(rule(sel, { tint: 'ok', glow: 0.3 }));
        else if (t === 'grant') rules.push(rule(sel, { tint: 'ok', glow: 0.9, pulse: true }));
        else if (t === 'stop') rules.push(rule(sel, { tint: stopTint, glow: 0.9, pulse: true }));
        else if (t === 'skip') rules.push(rule(sel, { tint: 'muted', glow: 0.05 }));
        else rules.push(rule(sel, { tint: 'down', glow: 0 }));
        rules.push(rule('^flow-to-' + gid + '$', t === 'n/a' ? { tint: 'down', glow: 0 } : { tint: 'ok', glow: 0.35 }));
      });
      rules.push(rule('^decision-', { tint: 'down', glow: 0 }));
      rules.push(rule('^decision-' + d.decision + '(-orb)?$', { tint: d.decision === 'allow' ? 'ok' : (d.decision === 'explicit-deny' ? 'deny' : 'muted'), glow: 0.9, pulse: true }));
      rules.push(rule('^deny-short-circuit$', d.decision === 'explicit-deny' ? { tint: 'deny', glow: 0.8, pulse: true } : { tint: 'down', glow: 0 }));
      var label = d.decision === 'allow' ? 'ALLOW' : (d.decision === 'explicit-deny' ? 'EXPLICIT DENY' : 'IMPLICIT DENY');
      return {
        verdict: d.decision,
        metrics: d,
        caption: label + ' · ' + (d.decision === 'allow' && d.at === 'identity-policy' ? 'every gate passed' : 'decided at gate “' + d.at + '”') + ' · s3:DeleteObject on prod-bucket/*',
        rules: rules
      };
    }
  };

  /* ── NetworkPolicy isolation (CKA services & networking) ──────────────── */
  function netpolDecide(s) {
    var enforced = !!s.cniEnforces;
    var ingressIsolated = enforced && !!s.policy;
    var egressIsolated = enforced && !!s.policy && !!s.egressIsolated;
    return {
      enforced: enforced,
      ingressIsolated: ingressIsolated,
      egressIsolated: egressIsolated,
      frontend: !ingressIsolated || !!s.ruleFrontend,
      untrusted: !ingressIsolated || !!s.ruleUntrusted,
      dns: !egressIsolated || !!s.ruleDns
    };
  }

  var netpol = {
    id: 'netpol-isolation',
    title: 'NetworkPolicy drill — who can reach app=api:8080?',
    cert: 'CKA',
    glb: '/assets/immersive/network-policy-isolation.glb',
    initial: { cniEnforces: true, policy: true, ruleFrontend: true, ruleUntrusted: false, egressIsolated: false, ruleDns: true },
    toggles: [
      { id: 'cniEnforces', label: 'CNI', on: 'Calico/Cilium (enforces)', off: 'flannel (no policy)' },
      { id: 'policy', label: 'NetworkPolicy on app=api', on: 'applied', off: 'none' },
      { id: 'ruleFrontend', label: 'ingress from ns=frontend', on: 'allow', off: 'absent' },
      { id: 'ruleUntrusted', label: 'ingress from ns=untrusted', on: 'allow', off: 'absent', risk: 'on' },
      { id: 'egressIsolated', label: 'policyTypes Egress', on: 'yes', off: 'no', risk: 'none' },
      { id: 'ruleDns', label: 'egress to kube-dns :53', on: 'allow', off: 'absent' }
    ],
    scenarios: [
      { id: 'default-deny', label: 'Empty ingress policy', set: { cniEnforces: true, policy: true, ruleFrontend: false, ruleUntrusted: false, egressIsolated: false },
        predict: { q: 'You apply a NetworkPolicy selecting app=api with policyTypes: [Ingress] and no ingress rules. Can frontend pods still reach api:8080?',
          options: ['No — a selected pod with no matching ingress rule is isolated: all ingress is dropped', 'Yes — an empty rule list means “allow all”', 'Only pods in the same namespace as api'],
          answer: 0, why: 'Selecting a pod for Ingress isolates it; only traffic matching some ingress rule gets in. No rules = default deny. (An empty rule `- {}` would be allow-all — a different thing.)' } },
      { id: 'additive', label: 'Allow frontend only', set: { cniEnforces: true, policy: true, ruleFrontend: true, ruleUntrusted: false, egressIsolated: false },
        predict: { q: 'Now ingress.from has namespaceSelector name=frontend. Can pods in ns untrusted reach api?',
          options: ['No — policies are allow-lists; anything not matched by a rule is dropped', 'Yes — you never wrote a deny rule for untrusted', 'Yes, until you add a second policy that denies it'],
          answer: 0, why: 'NetworkPolicy has no deny rules. Once a pod is isolated, every rule (across every policy selecting it) is unioned as an allow-list.' } },
      { id: 'egress-dns', label: 'Egress lock-down', set: { cniEnforces: true, policy: true, ruleFrontend: true, egressIsolated: true, ruleDns: false },
        predict: { q: 'You add policyTypes: [Egress] allowing only db:5432. Suddenly api cannot connect to db.backend.svc. Why?',
          options: ['Egress isolation also blocks DNS — allow UDP/TCP 53 to kube-dns', 'db rejects the connection because ingress changed', 'Egress policies need a CNI restart to take effect'],
          answer: 0, why: 'The pod can no longer resolve the Service name. Every egress lock-down needs an explicit rule to kube-dns (namespace kube-system, port 53 UDP+TCP).' } },
      { id: 'flannel', label: 'Policy on flannel', set: { cniEnforces: false, policy: true, ruleFrontend: true, ruleUntrusted: false, egressIsolated: false },
        predict: { q: 'Same policy, but the cluster runs plain flannel. Can untrusted pods reach api?',
          options: ['Yes — the API stores the policy, but a CNI without NetworkPolicy support silently ignores it', 'No — kube-apiserver enforces it', 'No — kube-proxy enforces it with iptables'],
          answer: 0, why: 'NetworkPolicy is enforced by the network plugin (Calico, Cilium, …), not the control plane. kubectl apply succeeds and nothing happens.' } },
      { id: 'heal', label: 'Reset', set: { cniEnforces: true, policy: true, ruleFrontend: true, ruleUntrusted: false, egressIsolated: false, ruleDns: true } }
    ],
    derive: function (s) {
      var d = netpolDecide(s);
      var rules = [];
      var shieldOn = d.ingressIsolated;
      rules.push(rule('^netpol-shield-(ring|post-\\d+|crown)$', shieldOn ? { tint: 'ok', glow: 0.45 } : (s.policy ? { tint: 'warn', glow: 0.15, pulse: true } : { tint: 'down', glow: 0 })));
      rules.push(rule('^netpol-manifest$', s.policy ? { tint: shieldOn ? 'gold' : 'warn', glow: 0.35, pulse: !shieldOn } : { tint: 'down', glow: 0 }));
      rules.push(rule('^cni-enforcer$', d.enforced ? { tint: 'ok', glow: 0.4 } : { tint: 'deny', glow: 0.8, pulse: true }));
      rules.push(rule('^edge-allow-\\d$', d.frontend ? { tint: 'ok', glow: 0.5 } : { tint: 'deny', glow: 0.6, pulse: true }));
      rules.push(rule('^edge-deny-\\d$', d.untrusted ? { tint: 'warn', glow: 0.6, pulse: true } : { tint: 'deny', glow: 0.35 }));
      rules.push(rule('^deny-block-\\d$', d.untrusted ? { hide: true } : { tint: 'deny', glow: 0.8, pulse: true }));
      rules.push(rule('^pod-untrusted-\\d$', d.untrusted ? { tint: 'warn', glow: 0.4 } : { tint: 'muted', glow: 0.1 }));
      rules.push(rule('^edge-egress-dns$', d.dns ? { tint: 'ok', glow: 0.35 } : { tint: 'deny', glow: 0.8, pulse: true }));
      rules.push(rule('^kube-dns$', d.dns ? { tint: 'ok', glow: 0.2 } : { tint: 'deny', glow: 0.5 }));
      var verdict, cap;
      if (!d.enforced && s.policy) { verdict = 'down'; cap = 'POLICY IGNORED — CNI does not implement NetworkPolicy; every namespace reaches api'; }
      else if (!d.dns) { verdict = 'degraded'; cap = 'Egress isolated without a DNS rule — api cannot resolve Service names'; }
      else if (d.untrusted) { verdict = 'degraded'; cap = (d.ingressIsolated ? 'Isolated, but a rule admits ns=untrusted' : 'No policy selects app=api — pods are non-isolated, all ingress allowed'); }
      else if (!d.frontend) { verdict = 'implicit-deny'; cap = 'Default deny — app=api isolated with no matching ingress rule; frontend is dropped too'; }
      else { verdict = 'healthy'; cap = 'Isolated · frontend → api:8080 allowed · untrusted dropped at the policy · DNS egress ' + (d.egressIsolated ? 'explicitly allowed' : 'not isolated'); }
      return { verdict: verdict, metrics: d, caption: cap, rules: rules };
    }
  };

  /* ── RBAC authorization (CKA cluster architecture) ────────────────────── */
  function rbacDecide(s) {
    return {
      alicePods: !!s.b0 && !!s.sameNs,
      bobSecrets: !!s.b1 && !!s.sameNs,
      ciDeploys: !!s.b2 && (!!s.b2Cluster || !!s.sameNs),
      ciNodes: !!s.b2 && !!s.b2Cluster
    };
  }

  var rbac = {
    id: 'rbac-authz',
    title: 'RBAC drill — kubectl auth can-i, in 3D',
    cert: 'CKA',
    glb: '/assets/immersive/rbac-authz-graph.glb',
    initial: { b0: true, b1: true, b2: true, b2Cluster: false, sameNs: true },
    toggles: [
      { id: 'b0', label: 'alice → pod-reader (RoleBinding, ns dev)', on: 'bound', off: 'deleted' },
      { id: 'b1', label: 'bob → secret-reader (RoleBinding, ns dev)', on: 'bound', off: 'deleted' },
      { id: 'b2', label: 'ci-bot → ClusterRole deployer', on: 'bound', off: 'deleted' },
      { id: 'b2Cluster', label: 'ci-bot binding kind', on: 'ClusterRoleBinding', off: 'RoleBinding (ns dev)', risk: 'none' },
      { id: 'sameNs', label: 'requests target', on: 'ns dev', off: 'ns prod', risk: 'none' }
    ],
    scenarios: [
      { id: 'clusterrole-rb', label: 'ClusterRole via RoleBinding', set: { b2: true, b2Cluster: false, sameNs: true },
        predict: { q: 'ci-bot’s ClusterRole grants deployments and nodes, but it is bound with a RoleBinding in ns dev. Does `kubectl get nodes` work for ci-bot?',
          options: ['No — a RoleBinding scopes the ClusterRole to ns dev; cluster-scoped nodes are never granted', 'Yes — a ClusterRole is always cluster-wide', 'Only `get`, not `list`'],
          answer: 0, why: 'The binding decides scope, not the role. RoleBinding → ClusterRole grants only namespaced resources in that binding’s namespace. Nodes need a ClusterRoleBinding.' } },
      { id: 'wrong-ns', label: 'Other namespace', set: { b0: true, sameNs: false },
        predict: { q: 'alice is bound to pod-reader in ns dev. Does `kubectl get pods -n prod` work?',
          options: ['No — Forbidden: Roles and RoleBindings only grant inside their own namespace', 'Yes — get pods is a read-only verb', 'Yes, if she uses --as=alice'],
          answer: 0, why: 'Check it the exam way: `kubectl auth can-i get pods -n prod --as alice` → no.' } },
      { id: 'unbind', label: 'Delete bob’s binding', set: { b1: false, sameNs: true },
        predict: { q: 'You delete bob’s RoleBinding. He has no other grants. What does `kubectl get secrets -n dev` return?',
          options: ['Forbidden — RBAC is additive allow-only; no binding, no permission', 'The secrets — the Role still exists', 'An empty list'],
          answer: 0, why: 'RBAC has no deny rules: permissions are the union of every binding. Remove the last binding and the default is deny.' } },
      { id: 'crb', label: 'Promote to ClusterRoleBinding', set: { b2: true, b2Cluster: true, sameNs: false },
        predict: { q: 'Switch ci-bot to a ClusterRoleBinding. Can it list deployments in ns prod and get nodes?',
          options: ['Yes to both — a ClusterRoleBinding grants the ClusterRole in every namespace and on cluster-scoped resources', 'Only nodes — deployments still need a RoleBinding per namespace', 'Neither until kube-apiserver restarts'],
          answer: 0, why: 'ClusterRoleBinding = cluster-wide. Exam tip: least privilege usually means the RoleBinding version.' } },
      { id: 'heal', label: 'Reset', set: { b0: true, b1: true, b2: true, b2Cluster: false, sameNs: true } }
    ],
    derive: function (s) {
      var d = rbacDecide(s);
      var rules = [];
      var bound = [!!s.b0, !!s.b1, !!s.b2];
      for (var i = 0; i < 3; i++) {
        rules.push(rule('^(edge-u' + i + '-b' + i + '|rolebinding-' + i + '|edge-b' + i + '-r' + i + ')$', bound[i] ? { tint: i === 2 && s.b2Cluster ? 'gold' : 'ok', glow: 0.4 } : { tint: 'down', glow: 0 }));
      }
      function grant(edge, res, ok, user) {
        rules.push(rule('^' + edge + '$', ok ? { tint: 'ok', glow: 0.6, pulse: true } : { tint: 'deny', glow: 0.25 }));
        rules.push(rule('^(api|verbs)-' + res + '$', ok ? { tint: 'ok', glow: 0.5 } : { tint: 'deny', glow: 0.35 }));
        rules.push(rule('^user-' + user + '$', ok ? { tint: 'gold', glow: 0.5 } : { tint: 'muted', glow: 0.1 }));
      }
      grant('edge-r0-pods', 'pods', d.alicePods, 0);
      grant('edge-r1-secrets', 'secrets', d.bobSecrets, 1);
      grant('edge-r2-deploys', 'deployments', d.ciDeploys, 2);
      grant('edge-r2-nodes', 'nodes', d.ciNodes, 2);
      if (d.ciDeploys || d.ciNodes) rules.push(rule('^user-2$', { tint: 'gold', glow: 0.5 }));
      var yes = [d.alicePods, d.bobSecrets, d.ciDeploys, d.ciNodes].filter(Boolean).length;
      rules.push(rule('^kube-apiserver$', { tint: yes === 4 ? 'ok' : (yes ? 'gold' : 'deny'), glow: 0.35 }));
      var ns = s.sameNs ? 'dev' : 'prod';
      var yn = function (b) { return b ? 'yes' : 'no'; };
      return {
        verdict: yes === 4 ? 'allow' : (yes ? 'degraded' : 'implicit-deny'),
        metrics: d,
        caption: 'can-i (ns ' + ns + '): alice get pods ' + yn(d.alicePods) + ' · bob get secrets ' + yn(d.bobSecrets) +
          ' · ci-bot list deployments ' + yn(d.ciDeploys) + ' · ci-bot get nodes ' + yn(d.ciNodes),
        rules: rules
      };
    }
  };

  /* ── Scheduling: affinity · taints · tolerations · cordon (CKA workloads) ── */
  function schedDecide(s) {
    var nodes = {
      a: { labels: { disktype: 'ssd' }, taint: null, cordoned: !!s.aCordoned },
      b: { labels: { zone: 'us-east-1b' }, taint: 'gpu', cordoned: false },
      c: { labels: s.cNvme ? { disktype: 'nvme' } : { disktype: 'hdd' }, taint: s.cTaint ? 'maintenance' : null, cordoned: false }
    };
    function feasible(n, pod) {
      var node = nodes[n];
      if (node.cordoned) return false;
      if (node.taint && pod.tolerates.indexOf(node.taint) < 0) return false;
      if (pod.disk && node.labels.disktype !== pod.disk) return false;
      return true;
    }
    function place(pod) {
      var c = ['a', 'b', 'c'].filter(function (n) { return feasible(n, pod); });
      if (!c.length) return null;
      if (pod.prefer && c.indexOf(pod.prefer) >= 0) return pod.prefer;
      return c[0];
    }
    /* web is already Running on node-a; cordon blocks only new replicas. */
    var webNew = place({ disk: 'ssd', tolerates: [] });
    var trainer = place({ tolerates: s.trainerTol ? ['gpu'] : [], prefer: 'b' });
    var db = place({ disk: 'nvme', tolerates: [] });
    return { webRunning: 'a', webNewReplica: webNew, trainer: trainer, db: db };
  }

  var sched = {
    id: 'sched-taints',
    title: 'Scheduler drill — filter · score · bind',
    cert: 'CKA',
    glb: '/assets/immersive/scheduling-affinity.glb',
    initial: { aCordoned: false, trainerTol: true, cNvme: false, cTaint: true },
    toggles: [
      { id: 'aCordoned', label: 'node-a', on: 'cordoned', off: 'schedulable', risk: 'on' },
      { id: 'trainerTol', label: 'trainer toleration gpu=true:NoSchedule', on: 'set', off: 'removed' },
      { id: 'cNvme', label: 'node-c label disktype', on: 'nvme', off: 'hdd', risk: 'none' },
      { id: 'cTaint', label: 'node-c taint maintenance:NoExecute', on: 'on', off: 'removed', risk: 'none' }
    ],
    scenarios: [
      { id: 'label-only', label: 'Label node-c nvme', set: { cNvme: true, cTaint: true },
        predict: { q: 'db requires nodeAffinity disktype=nvme. You label node-c disktype=nvme but leave its maintenance:NoExecute taint. Does db schedule?',
          options: ['No — still Pending: affinity now matches, but the untolerated taint filters node-c out', 'Yes — labels override taints', 'Yes — NoExecute only affects running pods'],
          answer: 0, why: 'The Filter phase checks every predicate. NoExecute also blocks scheduling (and evicts running pods without a toleration).' } },
      { id: 'untaint', label: 'Remove the taint', set: { cNvme: true, cTaint: false },
        predict: { q: 'Now `kubectl taint nodes node-c maintenance:NoExecute-`. Where does db go?',
          options: ['Binds to node-c — the only node passing both filters', 'node-a — it scores highest', 'Stays Pending until you delete and recreate it'],
          answer: 0, why: 'The scheduler retries unschedulable pods when cluster state changes; node-c is now the only feasible node.' } },
      { id: 'drop-tol', label: 'Remove trainer toleration', set: { trainerTol: false, aCordoned: false },
        predict: { q: 'trainer prefers zone=us-east-1b (node-b, tainted gpu=true:NoSchedule). You remove its toleration. Where does it run?',
          options: ['node-a — the taint repels it from node-b; a preference cannot override a taint', 'node-b anyway — preferred affinity wins', 'Pending — preferences are required'],
          answer: 0, why: 'Tolerations allow, they do not attract; preferred affinity only scores feasible nodes. To pin GPU pods use a toleration AND nodeAffinity/nodeSelector.' } },
      { id: 'cordon', label: 'Cordon node-a', set: { aCordoned: true },
        predict: { q: 'You `kubectl cordon node-a`. What happens to the running web pod?',
          options: ['Keeps running — cordon only marks the node unschedulable; new web replicas go Pending', 'Evicted and rescheduled immediately', 'Moves to node-b'],
          answer: 0, why: 'cordon = SchedulingDisabled. drain = cordon + evict. web needs disktype=ssd, so new replicas have nowhere to go.' } },
      { id: 'heal', label: 'Reset', set: { aCordoned: false, trainerTol: true, cNvme: false, cTaint: true } }
    ],
    derive: function (s) {
      var d = schedDecide(s);
      var rules = [];
      rules.push(rule('^node-a$', s.aCordoned ? { tint: 'warn', glow: 0.45, pulse: true } : { tint: 'ok', glow: 0.25 }));
      rules.push(rule('^node-c-taint(-mark)?$', s.cTaint ? { tint: 'deny', glow: 0.6 } : { hide: true }));
      rules.push(rule('^node-c-label-badge$', s.cNvme ? { tint: 'gold', glow: 0.6 } : { tint: 'muted', glow: 0.1 }));
      rules.push(rule('^pod-bound-affinity$', { tint: 'ok', glow: 0.4 }));
      rules.push(rule('^edge-bind-node-a$', s.aCordoned ? { tint: 'warn', glow: 0.3 } : { tint: 'ok', glow: 0.4 }));
      var tOnB = d.trainer === 'b';
      rules.push(rule('^(pod-bound-toleration|edge-bind-node-b)$', tOnB ? { tint: 'gold', glow: 0.45 } : { tint: 'muted', glow: 0.08 }));
      rules.push(rule('^toleration-ring$', s.trainerTol ? { tint: 'gold', glow: 0.5 } : { hide: true }));
      rules.push(rule('^node-b-taint(-mark)?$', s.trainerTol ? { tint: 'gold', glow: 0.3 } : { tint: 'deny', glow: 0.7, pulse: true }));
      var dbBound = d.db === 'c';
      rules.push(rule('^pod-pending$', dbBound ? { tint: 'ok', glow: 0.6 } : { tint: 'muted', glow: 0.3, pulse: true }));
      rules.push(rule('^event-failed-scheduling$', dbBound ? { hide: true } : { tint: 'deny', glow: 0.6, pulse: true }));
      rules.push(rule('^edge-reject-node-c$', dbBound ? { tint: 'ok', glow: 0.6, pulse: true } : { tint: 'deny', glow: 0.3 }));
      rules.push(rule('^edge-sched-pending$', dbBound ? { tint: 'ok', glow: 0.3 } : { tint: 'muted', glow: 0.15 }));
      rules.push(rule('^sched-phase-2$', dbBound ? { tint: 'ok', glow: 0.6, pulse: true } : { tint: 'gold', glow: 0.3 }));
      var pending = (dbBound ? 0 : 1) + (d.webNewReplica ? 0 : 1) + (d.trainer ? 0 : 1);
      var where = function (n) { return n ? 'node-' + n : 'Pending'; };
      return {
        verdict: pending ? 'degraded' : 'healthy',
        metrics: d,
        caption: 'web Running on node-a (new replica → ' + where(d.webNewReplica) + ') · trainer → ' + where(d.trainer) +
          ' · db → ' + where(d.db) + (dbBound ? '' : ' (FailedScheduling: 0/3 nodes available)'),
        rules: rules
      };
    }
  };

  /* ── HPA (autoscaling/v2 algorithm) ───────────────────────────────────── */
  var HPA = { current: 2, min: 2, target: 50, normal: 40, spike: 120 };
  /** desired = ceil(current × currentUtil / targetUtil), skipped inside the 10% tolerance, clamped to [min,max]. */
  function hpaDesired(current, util, target, min, max) {
    var ratio = util / target;
    var raw = Math.abs(ratio - 1) <= 0.1 ? current : Math.ceil(current * ratio);
    return Math.max(min, Math.min(max, raw));
  }

  var hpa = {
    id: 'hpa-scale',
    title: 'HPA drill — desired = ceil(current × util / target)',
    cert: 'CKA',
    glb: '/assets/immersive/hpa-autoscaling.glb',
    initial: { spike: false, metricsUp: true, requestsSet: true, max5: true },
    toggles: [
      { id: 'spike', label: 'load', on: 'spike 120% CPU', off: 'normal 40% CPU', risk: 'on' },
      { id: 'metricsUp', label: 'metrics-server', on: 'up', off: 'down' },
      { id: 'requestsSet', label: 'container CPU requests', on: 'set', off: 'missing' },
      { id: 'max5', label: 'maxReplicas', on: '5', off: '3', risk: 'none' }
    ],
    scenarios: [
      { id: 'spike', label: 'Traffic spike', set: { spike: true, metricsUp: true, requestsSet: true, max5: true },
        predict: { q: '2 replicas average 120% CPU against a 50% target (min 2, max 5). What desiredReplicas does the HPA compute?',
          options: ['5 — ceil(2 × 120 / 50) = ceil(4.8)', '3 — it adds one replica per sync period', '4 — 4.8 rounds to the nearest whole pod'],
          answer: 0, why: 'autoscaling/v2: desired = ceil(current × currentMetric / target). 4.8 rounds UP to 5, still inside maxReplicas.' } },
      { id: 'cap', label: 'Spike with max 3', set: { spike: true, metricsUp: true, requestsSet: true, max5: false },
        predict: { q: 'Same spike, but maxReplicas: 3. What happens?',
          options: ['Scales to 3 and stops; pods stay hot (ScalingLimited=True)', 'Scales to 5 — max is a soft hint', 'Refuses to scale at all'],
          answer: 0, why: 'The computed 5 is clamped to maxReplicas. `kubectl describe hpa` shows ScalingLimited TooManyReplicas.' } },
      { id: 'no-requests', label: 'No CPU requests', set: { spike: true, metricsUp: true, requestsSet: false, max5: true },
        predict: { q: 'The Deployment has no resources.requests.cpu. Under the spike, what does `kubectl get hpa` show?',
          options: ['TARGETS <unknown>/50% and no scaling — utilization is a percentage of requests', '5 replicas, same as before', 'It uses limits instead of requests'],
          answer: 0, why: 'CPU utilization = usage / request. With no request there is nothing to divide by: FailedGetResourceMetric, replicas unchanged.' } },
      { id: 'metrics-down', label: 'metrics-server down', set: { spike: true, metricsUp: false, requestsSet: true, max5: true },
        predict: { q: 'metrics-server crashes during the spike. What does the HPA do?',
          options: ['Holds the current replica count — it cannot compute a new one', 'Scales to maxReplicas to be safe', 'Scales to zero'],
          answer: 0, why: 'No metrics → no recommendation. The HPA keeps the current scale and reports ScalingActive=False until metrics return.' } },
      { id: 'heal', label: 'Reset', set: { spike: false, metricsUp: true, requestsSet: true, max5: true } }
    ],
    derive: function (s) {
      var max = s.max5 ? 5 : 3;
      var util = s.spike ? HPA.spike : HPA.normal;
      var canCompute = !!s.metricsUp && !!s.requestsSet;
      var desired = canCompute ? hpaDesired(HPA.current, util, HPA.target, HPA.min, max) : HPA.current;
      var raw = canCompute ? Math.ceil(HPA.current * util / HPA.target) : null;
      var limited = canCompute && raw > max;
      var rules = [];
      for (var i = 0; i < 5; i++) {
        var on = i < desired;
        rules.push(rule('^(replica|scale-rail)-' + i + '$', on ? { tint: i < HPA.current ? 'ok' : 'gold', glow: i < HPA.current ? 0.35 : 0.7, pulse: i >= HPA.current } : { hide: true }));
      }
      rules.push(rule('^metrics-server$', s.metricsUp ? { tint: 'ok', glow: 0.3 } : { tint: 'deny', glow: 0.8, pulse: true }));
      rules.push(rule('^metric-hop-\\d$', s.metricsUp ? { tint: s.requestsSet ? 'gold' : 'warn', glow: 0.4 } : { hide: true }));
      rules.push(rule('^cpu-bar-\\d$', !s.requestsSet ? { tint: 'muted', glow: 0.1 } : (s.spike ? { tint: 'deny', glow: 0.7, pulse: true } : { tint: 'ok', glow: 0.3 })));
      rules.push(rule('^scale-cmd-\\d$', canCompute && desired !== HPA.current ? { tint: 'gold', glow: 0.7, pulse: true } : { hide: true }));
      rules.push(rule('^hpa-(controller|halo)$', canCompute ? { tint: limited ? 'warn' : 'ok', glow: 0.45, pulse: limited } : { tint: 'deny', glow: 0.6, pulse: true }));
      rules.push(rule('^desired-replicas$', { tint: limited ? 'warn' : 'gold', glow: 0.5 }));
      var cap;
      if (!s.metricsUp) cap = 'metrics-server down — FailedGetResourceMetric · holding ' + desired + ' replicas';
      else if (!s.requestsSet) cap = 'TARGETS <unknown>/' + HPA.target + '% — no CPU requests to compute utilization · holding ' + desired + ' replicas';
      else cap = 'CPU ' + util + '% vs target ' + HPA.target + '% · ceil(' + HPA.current + ' × ' + util + '/' + HPA.target + ') = ' + raw +
        (limited ? ' → clamped to maxReplicas ' + max : '') + ' · desired ' + desired + (desired === HPA.min && raw <= HPA.min ? ' (minReplicas floor)' : '');
      return {
        verdict: !canCompute ? 'down' : (limited ? 'degraded' : 'healthy'),
        metrics: { desired: desired, raw: raw, max: max, util: util, limited: limited, canCompute: canCompute },
        caption: cap,
        rules: rules
      };
    }
  };

  /* ── Storage: StorageClass · CSI · PV/PVC binding · reclaim (CKA storage) ──
   * Scene contract (storage-csi-pv.glb): pvc-1 is a dynamic claim (10Gi RWO, no storageClassName → default
   * class) mounted by consumer-pod on worker-node via pv-1/backend-disk-1. pvc-0 is a static claim
   * (storageClassName: manual, 20Gi RWO) that can only bind pv-0. pv-2 is an Available PV of class fast-ssd. */
  function storageDecide(s) {
    var provisioned = !!s.scDefault && (!s.wffc || !!s.podCreated);
    var inUse = !!s.podCreated && !s.podDeleted;   /* podCreated = a consumer was created at some point (drives WFFC); podDeleted = it is gone now */
    var terminating = !!s.pvcDeleted && inUse; /* kubernetes.io/pvc-protection finalizer */
    var gone = !!s.pvcDeleted && !inUse;
    var pvc1, pv1, disk1;
    if (gone) {
      pvc1 = 'deleted';
      pv1 = provisioned ? (s.retain ? 'Released' : 'deleted') : 'none';
      disk1 = provisioned ? (s.retain ? 'kept' : 'deleted') : 'none';
    } else {
      pvc1 = provisioned ? (terminating ? 'Terminating' : 'Bound') : 'Pending';
      pv1 = provisioned ? 'Bound' : 'none';
      disk1 = provisioned ? 'kept' : 'none';
    }
    var pendingWhy = !s.scDefault ? 'no-default-class' : (!provisioned ? 'wait-for-first-consumer' : null);
    var pod = 'none';
    if (s.podCreated && s.podDeleted) pod = 'deleted';
    else if (inUse) {
      if (!provisioned) pod = 'Pending';
      else pod = s.secondNode ? 'multi-attach' : 'Running';
    }
    var pvc0 = !!s.pv0Big && !s.pvc0Rwx ? 'Bound' : 'Pending';
    return { provisioned: provisioned, pvc1: pvc1, pv1: pv1, disk1: disk1, pod: pod, pendingWhy: pendingWhy,
      pvc0: pvc0, pv0Capacity: s.pv0Big ? '50Gi' : '5Gi' };
  }

  var storage = {
    id: 'storage-csi',
    title: 'Storage drill — StorageClass · CSI · PV/PVC binding · reclaim',
    cert: 'CKA',
    glb: '/assets/immersive/storage-csi-pv.glb',
    initial: { scDefault: true, wffc: true, podCreated: true, podDeleted: false, secondNode: false, retain: false, pvcDeleted: false, pv0Big: true, pvc0Rwx: false },
    toggles: [
      { id: 'scDefault', label: 'default StorageClass', on: 'csi-gp3 (default)', off: 'none' },
      { id: 'wffc', label: 'volumeBindingMode', on: 'WaitForFirstConsumer', off: 'Immediate', risk: 'none' },
      { id: 'podCreated', label: 'pod using pvc-1', on: 'created', off: 'not created yet', risk: 'none' },
      { id: 'podDeleted', label: 'that pod', on: 'deleted since', off: 'still running', risk: 'none' },
      { id: 'secondNode', label: 'replica-2 on node-b (same RWO claim)', on: 'scheduled', off: 'none', risk: 'on' },
      { id: 'retain', label: 'reclaimPolicy', on: 'Retain', off: 'Delete', risk: 'none' },
      { id: 'pvcDeleted', label: 'pvc-1', on: 'deleted', off: 'present', risk: 'on' },
      { id: 'pv0Big', label: 'pv-0 capacity (manual)', on: '50Gi', off: '5Gi' },
      { id: 'pvc0Rwx', label: 'pvc-0 accessModes', on: 'ReadWriteMany', off: 'ReadWriteOnce', risk: 'on' }
    ],
    scenarios: [
      { id: 'no-default-sc', label: 'No default StorageClass', set: { scDefault: false, wffc: false, podCreated: true, podDeleted: false, secondNode: false, pvcDeleted: false },
        predict: { q: 'The cluster has no default StorageClass, and pvc-1 omits storageClassName. A pod mounts pvc-1. What happens?',
          options: ['The CSI driver provisions a volume with its built-in defaults', 'pvc-1 stays Pending — no provisioner is ever asked; the pod stays Pending (unbound PersistentVolumeClaim)', 'The API server rejects the PVC at create time'],
          answer: 1, why: 'Without a default class, a claim with no storageClassName can only bind an existing PV that has no class; nothing triggers dynamic provisioning. Fix: set storageClassName, or mark a class with storageclass.kubernetes.io/is-default-class: "true" (the claim is then updated retroactively).' } },
      { id: 'wffc', label: 'WaitForFirstConsumer, no pod', set: { scDefault: true, wffc: true, podCreated: false, podDeleted: false, secondNode: false, pvcDeleted: false },
        predict: { q: 'The default StorageClass uses volumeBindingMode: WaitForFirstConsumer. You create pvc-1 but no pod uses it yet. Status?',
          options: ['Pending (WaitForFirstConsumer) — no PV is provisioned until a pod using it is scheduled', 'Bound — dynamic provisioning always happens at PVC creation', 'Lost — the claim is garbage-collected without a consumer'],
          answer: 0, why: 'WaitForFirstConsumer delays binding and provisioning until the scheduler picks a node for a consuming pod, so the disk is created in that node’s zone/topology. `kubectl describe pvc` shows “waiting for first consumer to be created before binding”. Immediate mode would provision right away.' } },
      { id: 'static-size', label: 'Static PV too small', set: { pv0Big: false, pvc0Rwx: false },
        predict: { q: 'pvc-0 requests 20Gi, ReadWriteOnce, storageClassName: manual. The only Available manual PV, pv-0, is 5Gi (pv-2 is 100Gi but class fast-ssd). Does pvc-0 bind?',
          options: ['Yes — it binds to pv-2, the larger PV', 'Yes — to pv-0, and the volume grows to 20Gi', 'No — stays Pending: a PV must match the class and offer ≥ the requested size and every requested access mode'],
          answer: 2, why: 'The binder only considers PVs of the same storageClassName whose capacity ≥ the request and whose accessModes include the requested ones. A bigger PV of another class never matches. With a 50Gi manual pv-0 the claim binds 1:1 and reports the whole 50Gi.' } },
      { id: 'multi-attach', label: 'RWO claim on a second node', set: { scDefault: true, podCreated: true, podDeleted: false, secondNode: true, pvcDeleted: false },
        predict: { q: 'A second replica of the Deployment, using the same ReadWriteOnce pvc-1, lands on node-b while replica-1 runs on node-a. Result?',
          options: ['Replica-2 is stuck ContainerCreating with a Multi-Attach error — an RWO volume attaches to one node at a time', 'Both run — RWO means one writer pod, readers are fine', 'The scheduler always co-locates pods that share a PVC'],
          answer: 0, why: 'ReadWriteOnce is per node: pods on the same node can share it, a second node cannot attach it (FailedAttachVolume “Multi-Attach error”). Use RWX storage, a StatefulSet with volumeClaimTemplates, or ReadWriteOncePod to make the single-pod intent explicit.' } },
      { id: 'pvc-protect', label: 'Delete PVC still in use', set: { scDefault: true, podCreated: true, podDeleted: false, secondNode: false, pvcDeleted: true },
        predict: { q: 'You run kubectl delete pvc pvc-1 while the pod is still using it. What happens?',
          options: ['The PVC and its data are deleted immediately; the pod crashes', 'pvc-1 sits in Terminating until the pod is gone (pvc-protection finalizer); the pod keeps its data', 'The delete is rejected with Forbidden'],
          answer: 1, why: 'Storage Object in Use Protection adds the kubernetes.io/pvc-protection finalizer: deletion is postponed until no pod uses the claim. Only then does the reclaimPolicy run.' } },
      { id: 'reclaim-delete', label: 'Delete PVC · reclaim Delete', set: { scDefault: true, podCreated: true, podDeleted: true, secondNode: false, retain: false, pvcDeleted: true },
        predict: { q: 'The pod is gone and you delete pvc-1. Its dynamically provisioned PV has reclaimPolicy: Delete (the StorageClass default). What happens to the disk?',
          options: ['The PV is kept as Released so you can recover the data', 'Nothing until an admin runs kubectl delete pv', 'The PV and the backing disk are deleted by the CSI driver — the data is gone'],
          answer: 2, why: 'Dynamically provisioned PVs inherit the StorageClass reclaimPolicy, which defaults to Delete: the external provisioner deletes the PV and calls the CSI DeleteVolume on the backend disk.' } },
      { id: 'reclaim-retain', label: 'Delete PVC · reclaim Retain', set: { scDefault: true, podCreated: true, podDeleted: true, secondNode: false, retain: true, pvcDeleted: true },
        predict: { q: 'Same delete, but the PV has reclaimPolicy: Retain. Afterwards?',
          options: ['PV becomes Released with the data intact; it will not bind a new claim until an admin clears claimRef or recreates it', 'PV goes back to Available and binds the next matching claim', 'PV and disk are deleted, just later'],
          answer: 0, why: 'Retain keeps both the PV object and the disk. A Released PV still carries the old claimRef, so it cannot be reused automatically — manual reclamation is the point.' } },
      { id: 'heal', label: 'Reset', set: { scDefault: true, wffc: true, podCreated: true, podDeleted: false, secondNode: false, retain: false, pvcDeleted: false, pv0Big: true, pvc0Rwx: false } }
    ],
    derive: function (s) {
      var d = storageDecide(s);
      var rules = [];
      rules.push(rule('^(storage-class|sc-provisioner)$', s.scDefault ? { tint: 'gold', glow: 0.35 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^edge-sc-csi$', s.scDefault ? { tint: 'gold', glow: 0.3 } : { tint: 'down', glow: 0 }));
      var waiting = d.pendingWhy === 'wait-for-first-consumer';
      rules.push(rule('^csi-driver$', d.provisioned ? { tint: 'ok', glow: 0.3 } : { tint: 'muted', glow: 0.1 }));
      rules.push(rule('^csi-controller$', waiting ? { tint: 'gold', glow: 0.6, pulse: true } : (d.provisioned ? { tint: 'ok', glow: 0.4 } : { tint: 'down', glow: 0 })));
      var pv1Live = d.pv1 === 'Bound' || d.pv1 === 'Released';
      rules.push(rule('^edge-csi-pv1$', pv1Live ? { tint: 'ok', glow: 0.35 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^pv-1$', d.pv1 === 'Bound' ? { tint: 'ok', glow: 0.4 } : (d.pv1 === 'Released' ? { tint: 'warn', glow: 0.55, pulse: true } : { hide: true })));
      /* reclaim Delete: the CSI driver deleted the backing disk, so it vanishes (Codex review on #24); only a kept disk renders. */
      rules.push(rule('^(backend-disk|platter)-1$', d.disk1 === 'kept' ? (d.pv1 === 'Released' ? { tint: 'warn', glow: 0.45 } : { tint: 'gold', glow: 0.3 }) : { hide: true }));
      rules.push(rule('^edge-disk-pv1$', pv1Live ? { tint: 'gold', glow: 0.3 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^pvc-1$', d.pvc1 === 'Bound' ? { tint: 'ok', glow: 0.4 } : (d.pvc1 === 'deleted' ? { hide: true } : { tint: 'warn', glow: 0.6, pulse: true })));
      rules.push(rule('^edge-pv1-pvc1$', d.pvc1 === 'Bound' || d.pvc1 === 'Terminating' ? { tint: 'ok', glow: 0.4 } : { tint: 'down', glow: 0 }));
      var mounted = d.pod === 'Running' || d.pod === 'multi-attach';
      rules.push(rule('^consumer-pod$', d.pod === 'none' || d.pod === 'deleted' ? { hide: true } : (d.pod === 'Pending' ? { tint: 'muted', glow: 0.3, pulse: true } : { tint: 'gold', glow: 0.4 })));
      rules.push(rule('^edge-pvc-pod$', mounted ? { tint: 'ok', glow: 0.45 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^volume-mount$', d.pod === 'multi-attach' ? { tint: 'deny', glow: 0.85, pulse: true } : (mounted ? { tint: 'ok', glow: 0.4 } : { tint: 'down', glow: 0 })));
      rules.push(rule('^worker-node$', d.pod === 'multi-attach' ? { tint: 'warn', glow: 0.5, pulse: true } : { tint: 'muted', glow: 0.1 }));
      rules.push(rule('^io-bead-\\d$', mounted ? { tint: 'ok', glow: 0.6, pulse: true } : { hide: true }));
      var b0 = d.pvc0 === 'Bound';
      rules.push(rule('^pvc-0$', b0 ? { tint: 'ok', glow: 0.4 } : { tint: 'warn', glow: 0.6, pulse: true }));
      rules.push(rule('^edge-pv0-pvc0$', b0 ? { tint: 'ok', glow: 0.4 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^pv-0$', b0 ? { tint: 'ok', glow: 0.35 } : { tint: 'muted', glow: 0.15 }));
      rules.push(rule('^edge-csi-pv0$', { tint: 'muted', glow: 0.05 }));
      rules.push(rule('^(pv-2|backend-disk-2|platter-2)$', { tint: 'muted', glow: 0.1 }));
      var cap = [];
      if (d.pvc1 === 'Pending') cap.push('pvc-1 Pending (' + (d.pendingWhy === 'no-default-class' ? 'no default StorageClass — nothing provisions' : 'WaitForFirstConsumer — no pod scheduled yet') + ')');
      else if (d.pvc1 === 'Terminating') cap.push('pvc-1 Terminating — pvc-protection holds it while the pod uses it');
      else if (d.pvc1 === 'deleted') cap.push('pvc-1 deleted → ' + (d.pv1 === 'none' ? 'nothing was provisioned' : (d.pv1 === 'Released' ? 'pv-1 Released, disk kept (Retain)' : 'pv-1 + disk deleted (reclaim Delete)')));
      else cap.push('pvc-1 Bound → pv-1 (CSI-provisioned 10Gi RWO)');
      if (d.pod === 'multi-attach') cap.push('replica-2 ContainerCreating: Multi-Attach error (RWO on node-a)');
      else if (d.pod === 'Pending') cap.push('pod Pending (unbound PVC)');
      else if (d.pod === 'Running') cap.push('pod Running with /data mounted');
      else if (d.pod === 'deleted') cap.push('consumer pod deleted');
      cap.push('pvc-0 ' + (b0 ? 'Bound → pv-0 (' + d.pv0Capacity + ')' : 'Pending (' + (s.pvc0Rwx ? 'pv-0 offers only RWO' : 'pv-0 ' + d.pv0Capacity + ' < 20Gi') + ')'));
      var verdict;
      if (d.pv1 === 'deleted') verdict = 'data-deleted';
      else if (d.pod === 'multi-attach') verdict = 'down';
      else if (d.pvc1 === 'Bound' && b0 && d.pod === 'Running') verdict = 'healthy';
      else if (d.pv1 === 'Released') verdict = 'released';
      else if (d.pvc1 === 'Terminating') verdict = 'terminating';
      else verdict = 'pending';
      return { verdict: verdict, metrics: d, caption: cap.join(' · '), rules: rules };
    }
  };

  /* ── Ingress: controller · pathType · endpoints · TLS (CKA services & networking) ──
   * Scene contract (ingress-gateway.glb): rule-0 = /api → service-0 (endpoint-pod-0/1), rule-1 = /web → service-1
   * (endpoint-pod-2/3), rule-2 = tls host shop.example.com (secret shop-tls). Clients: client-0 GET /api/v1/orders,
   * client-1 GET /api, client-2 GET /web/cart. */
  var INGRESS_CLIENTS = ['/api/v1/orders', '/api', '/web/cart'];
  /** Ingress path matching (networking.k8s.io/v1): Exact = whole path; Prefix = element-wise; longest match wins, Exact beats Prefix on a tie. */
  function ingressMatch(path, rules) {
    var best = null;
    rules.forEach(function (r) {
      var p = r.path.replace(/\/+$/, '') || '/';
      var hit = r.type === 'Exact' ? path === r.path
        : (p === '/' ? true : (path === p || path.indexOf(p + '/') === 0));
      if (!hit) return;
      if (!best || p.length > best.len || (p.length === best.len && r.type === 'Exact')) best = { rule: r, len: p.length };
    });
    return best ? best.rule : null;
  }
  function ingressDecide(s) {
    var rules = [{ path: '/api', type: s.apiExact ? 'Exact' : 'Prefix', svc: 0 }, { path: '/web', type: 'Prefix', svc: 1 }];
    var clients = INGRESS_CLIENTS.map(function (path) {
      if (!s.controller) return { path: path, status: 'no-route', svc: null };
      var r = ingressMatch(path, rules);
      if (!r) return { path: path, status: 404, svc: null };
      if (r.svc === 0 && !s.apiReady) return { path: path, status: 503, svc: 0 };
      return { path: path, status: 200, svc: r.svc };
    });
    return { clients: clients, cert: !s.controller ? null : (s.tlsSecret ? 'shop-tls' : 'controller-default'), apiType: rules[0].type };
  }

  var ingress = {
    id: 'ingress-routing',
    title: 'Ingress drill — controller · pathType · endpoints · TLS',
    cert: 'CKA',
    glb: '/assets/immersive/ingress-gateway.glb',
    initial: { controller: true, apiExact: false, apiReady: true, tlsSecret: true },
    toggles: [
      { id: 'controller', label: 'ingress controller (class nginx)', on: 'installed', off: 'none' },
      { id: 'apiExact', label: 'rule /api pathType', on: 'Exact', off: 'Prefix', risk: 'none' },
      { id: 'apiReady', label: 'service-0 ready endpoints', on: '2 Ready', off: '0 (selector mismatch)' },
      { id: 'tlsSecret', label: 'Secret shop-tls', on: 'present', off: 'missing' }
    ],
    scenarios: [
      { id: 'no-controller', label: 'No controller', set: { controller: false, apiExact: false, apiReady: true, tlsSecret: true },
        predict: { q: 'You kubectl apply an Ingress with ingressClassName: nginx, but no ingress controller is installed. What happens to https://shop.example.com/api/v1/orders?',
          options: ['kube-proxy routes it to service-0', 'Nothing routes it — the Ingress is stored but no controller implements it, so it never gets an ADDRESS', 'The API server rejects the Ingress'],
          answer: 1, why: 'An Ingress is just configuration. Something (ingress-nginx, Traefik, a cloud LB controller…) must watch its IngressClass and program a proxy. `kubectl get ingress` shows an empty ADDRESS.' } },
      { id: 'exact', label: 'pathType Exact', set: { controller: true, apiExact: true, apiReady: true, tlsSecret: true },
        predict: { q: 'Rule /api is changed to pathType: Exact. Where does GET /api/v1/orders go?',
          options: ['404 from the default backend — Exact matches only /api itself', 'service-0 — Exact still matches sub-paths', 'service-1, the next rule'],
          answer: 0, why: 'Exact is a case-sensitive whole-path match. GET /api still reaches service-0; /api/v1/orders matches no rule, so the controller’s default backend answers 404.' } },
      { id: 'prefix', label: 'pathType Prefix', set: { controller: true, apiExact: false, apiReady: true, tlsSecret: true },
        predict: { q: 'Back to pathType: Prefix for /api. Which requests reach service-0?',
          options: ['Only /api', 'Any path starting with the characters “/api”, including /apiv2', '/api and /api/v1/orders — Prefix matches by path element, so /apiv2 would not match'],
          answer: 2, why: 'Prefix splits on “/” and compares element by element: /api matches /api, /api/ and /api/v1/orders but not /apiv2. When several rules match, the longest path wins.' } },
      { id: 'no-endpoints', label: 'Backend has no ready pods', set: { controller: true, apiExact: false, apiReady: false, tlsSecret: true },
        predict: { q: 'service-0’s selector no longer matches any Ready pod. What does the client get for /api/v1/orders?',
          options: ['503 Service Unavailable — the route exists but the Service has no ready endpoints', '404 Not Found', 'The request is load-balanced to service-1'],
          answer: 0, why: 'Routing still resolves to service-0; the controller has no upstream to send it to. Check `kubectl get endpointslices -l kubernetes.io/service-name=service-0` and the Service selector vs pod labels.' } },
      { id: 'tls-missing', label: 'TLS Secret missing', set: { controller: true, apiExact: false, apiReady: true, tlsSecret: false },
        predict: { q: 'spec.tls references secretName shop-tls, which does not exist. What do HTTPS clients see?',
          options: ['The API server rejects the Ingress', 'The controller serves its default certificate (ingress-nginx: a self-signed “Kubernetes Ingress Controller Fake Certificate”) — a browser warning, but routing still works', 'The controller falls back to plain HTTP only'],
          answer: 1, why: 'The Ingress API does not validate that the Secret exists. ingress-nginx logs the missing secret and presents its default/self-signed cert; other controllers behave similarly. Create the kubernetes.io/tls Secret in the Ingress’s namespace.' } },
      { id: 'heal', label: 'Reset', set: { controller: true, apiExact: false, apiReady: true, tlsSecret: true } }
    ],
    derive: function (s) {
      var d = ingressDecide(s);
      var rules = [];
      rules.push(rule('^ingress-controller$', s.controller ? { tint: 'ok', glow: 0.35 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^tls-terminate$', !s.controller ? { tint: 'down', glow: 0 } : (s.tlsSecret ? { tint: 'ok', glow: 0.5 } : { tint: 'warn', glow: 0.8, pulse: true })));
      rules.push(rule('^rule-2$', !s.controller ? { tint: 'down', glow: 0 } : (s.tlsSecret ? { tint: 'gold', glow: 0.3 } : { tint: 'warn', glow: 0.5, pulse: true })));
      rules.push(rule('^rule-0$', !s.controller ? { tint: 'down', glow: 0 } : (s.apiExact ? { tint: 'warn', glow: 0.45 } : { tint: 'gold', glow: 0.35 })));
      rules.push(rule('^rule-1$', !s.controller ? { tint: 'down', glow: 0 } : { tint: 'gold', glow: 0.35 }));
      var STYLE = { 200: { tint: 'ok', glow: 0.55, pulse: true }, 404: { tint: 'warn', glow: 0.55, pulse: true }, 503: { tint: 'deny', glow: 0.75, pulse: true }, 'no-route': { tint: 'down', glow: 0 } };
      var toSvc = [false, false], svcErr = [false, false];
      d.clients.forEach(function (c, i) {
        rules.push(rule('^req-' + i + '-\\d$', STYLE[c.status]));
        rules.push(rule('^client-' + i + '$', c.status === 200 ? { tint: 'gold', glow: 0.4 } : (c.status === 'no-route' ? { tint: 'muted', glow: 0.1 } : { tint: c.status === 503 ? 'deny' : 'warn', glow: 0.4 })));
        if (c.svc !== null) { toSvc[c.svc] = true; if (c.status === 503) svcErr[c.svc] = true; }
      });
      [0, 1].forEach(function (k) {
        rules.push(rule('^route-' + k + '-\\d$', toSvc[k] ? (svcErr[k] ? { tint: 'deny', glow: 0.6, pulse: true } : { tint: 'ok', glow: 0.5, pulse: true }) : { hide: true }));
      });
      rules.push(rule('^service-0$', s.apiReady ? { tint: 'gold', glow: 0.35 } : { tint: 'deny', glow: 0.7, pulse: true }));
      rules.push(rule('^service-1$', { tint: 'gold', glow: 0.35 }));
      rules.push(rule('^endpoint-pod-[01]$', s.apiReady ? { tint: 'ok', glow: 0.3 } : { tint: 'muted', glow: 0.05 }));
      rules.push(rule('^endpoint-pod-[23]$', { tint: 'ok', glow: 0.3 }));
      rules.push(rule('^ep-[01]-\\d$', toSvc[0] && s.apiReady ? { tint: 'ok', glow: 0.5, pulse: true } : { hide: true }));
      rules.push(rule('^ep-[23]-\\d$', toSvc[1] ? { tint: 'ok', glow: 0.5, pulse: true } : { hide: true }));
      var codes = d.clients.map(function (c) { return 'GET ' + c.path + ' → ' + (c.status === 'no-route' ? 'no route (no controller)' : c.status + (c.svc !== null ? ' service-' + c.svc : ' default backend')); });
      var bad = d.clients.filter(function (c) { return c.status !== 200; }).length;
      var verdict = !s.controller ? 'down' : (bad ? 'degraded' : (s.tlsSecret ? 'healthy' : 'cert-warning'));
      var tls = !s.controller ? '' : (s.tlsSecret ? ' · TLS shop-tls' : ' · TLS: controller default cert (shop-tls missing)');
      return { verdict: verdict, metrics: d, caption: codes.join(' · ') + ' · /api ' + d.apiType + tls, rules: rules };
    }
  };

  /* ── v1.4.0 (2026-10-21) Gateway API: GatewayClass · listener hostname · ReferenceGrant · certificateRefs ──
   * Same authored scene as the Ingress drill (ingress-gateway.glb), read as Gateway API (gateway.networking.k8s.io/v1):
   * ingress-controller = the Gateway's data plane (implementation of GatewayClass lab-gw), tls-terminate = the HTTPS
   * listener (certificateRefs shop-tls), rule-2 = listener/route hostname shop.example.com, rule-0 = HTTPRoute rule
   * /api → backendRef service-0 in namespace shop-api (cross-namespace, needs a ReferenceGrant), rule-1 = /web →
   * service-1. Semantics follow the Gateway API spec: no controller → Accepted/Programmed stay Unknown (Pending, no
   * ADDRESS); a route whose hostnames intersect no listener is not Accepted (NoMatchingListenerHostname → 404); an
   * invalid backendRef (RefNotPermitted) MUST get HTTP 500; an unresolved certificateRef leaves the HTTPS listener
   * unprogrammed (InvalidCertificateRef) — no fallback certificate is promised. Rules engine; no live Gateway. */
  function gatewayDecide(s) {
    var rules = [{ path: '/api', type: s.routeExact ? 'Exact' : 'Prefix', svc: 0 }, { path: '/web', type: 'Prefix', svc: 1 }];
    var programmed = !!s.gwcAccepted && !!s.certRef;
    var clients = INGRESS_CLIENTS.map(function (path) {
      if (!s.gwcAccepted) return { path: path, status: 'no-route', svc: null };
      if (!s.certRef) return { path: path, status: 'tls-fail', svc: null };
      if (!s.routeAttached) return { path: path, status: 404, svc: null };
      var r = ingressMatch(path, rules);
      if (!r) return { path: path, status: 404, svc: null };
      if (r.svc === 0 && !s.refGrant) return { path: path, status: 500, svc: 0 };
      return { path: path, status: 200, svc: r.svc };
    });
    return {
      clients: clients,
      gatewayClass: s.gwcAccepted ? 'Accepted' : 'Unknown',
      gatewayProgrammed: !s.gwcAccepted ? 'Unknown' : (programmed ? 'True' : 'False'),
      address: s.gwcAccepted ? '203.0.113.20' : null,
      listener: !s.gwcAccepted ? 'Pending' : (s.certRef ? 'Programmed' : 'InvalidCertificateRef'),
      routeAccepted: !s.gwcAccepted ? 'Pending' : (s.routeAttached ? 'Accepted' : 'NoMatchingListenerHostname'),
      routeResolvedRefs: s.refGrant ? 'ResolvedRefs' : 'RefNotPermitted',
      matchType: s.routeExact ? 'Exact' : 'PathPrefix'
    };
  }

  var gateway = {
    id: 'gateway-api',
    title: 'Gateway API drill — GatewayClass · hostnames · ReferenceGrant · certificateRefs',
    cert: 'CKA',
    glb: '/assets/immersive/ingress-gateway.glb',
    initial: { gwcAccepted: true, routeAttached: true, routeExact: false, refGrant: true, certRef: true },
    toggles: [
      { id: 'gwcAccepted', label: 'GatewayClass lab-gw controller', on: 'running (Accepted)', off: 'none (Pending)' },
      { id: 'routeAttached', label: 'HTTPRoute hostnames', on: 'shop.example.com', off: 'shop.example.org (no listener)' },
      { id: 'routeExact', label: 'rule /api match type', on: 'Exact', off: 'PathPrefix', risk: 'none' },
      { id: 'refGrant', label: 'ReferenceGrant in ns shop-api', on: 'present', off: 'missing' },
      { id: 'certRef', label: 'listener certificateRefs shop-tls', on: 'Secret present', off: 'Secret missing' }
    ],
    scenarios: [
      { id: 'no-controller', label: 'GatewayClass without a controller', set: { gwcAccepted: false, routeAttached: true, routeExact: false, refGrant: true, certRef: true },
        predict: { q: 'Gateway shop-gw uses gatewayClassName lab-gw, but no controller watches that GatewayClass’s controllerName. What does `kubectl get gateway` show?',
          options: ['PROGRAMMED True — the API server programs Gateways itself', 'The API server rejects the Gateway', 'No ADDRESS and PROGRAMMED Unknown — status stays at the default Pending (“Waiting for controller”) because nothing reconciles it'],
          answer: 2, why: 'Gateway API is only an API: an implementation (the controller named by GatewayClass spec.controllerName) must accept the class and program a data plane. Until one does, GatewayClass ACCEPTED and Gateway PROGRAMMED stay Unknown with reason Pending and no address is assigned.' } },
      { id: 'hostname-mismatch', label: 'Route hostname matches no listener', set: { gwcAccepted: true, routeAttached: false, routeExact: false, refGrant: true, certRef: true },
        predict: { q: 'The HTTPS listener has hostname shop.example.com. HTTPRoute shop-route has hostnames: [shop.example.org] and parentRefs shop-gw. What does GET https://shop.example.com/api/v1/orders return?',
          options: ['404 — the route is not Accepted by that parent (reason NoMatchingListenerHostname), so the Gateway has no route for the request', '200 — parentRefs alone attach the route', '503 — the backend has no endpoints'],
          answer: 0, why: 'A route attaches to a listener only if their hostnames intersect. With no intersection the parent status says Accepted=False, reason NoMatchingListenerHostname, and the Gateway answers 404 for the host. `kubectl describe httproute` shows it under Status → Parents.' } },
      { id: 'exact', label: 'Path match Exact', set: { gwcAccepted: true, routeAttached: true, routeExact: true, refGrant: true, certRef: true },
        predict: { q: 'Rule 0 of shop-route changes from path type PathPrefix to Exact with value /api. Which request still reaches service-0?',
          options: ['/api/v1/orders and /api', 'Only /api — Exact is a whole-path match; /api/v1/orders now matches no rule and gets 404', 'Neither — Exact needs a trailing slash'],
          answer: 1, why: 'HTTPRoute PathPrefix matches by path element (like Ingress Prefix); Exact matches the whole path only. /web/cart is unaffected. Read it back with `kubectl get httproute shop-route -o yaml`.' } },
      { id: 'no-refgrant', label: 'Cross-namespace backendRef, no ReferenceGrant', set: { gwcAccepted: true, routeAttached: true, routeExact: false, refGrant: false, certRef: true },
        predict: { q: 'Rule /api has backendRefs: [{name: service-0, namespace: shop-api}] while the HTTPRoute lives in default. shop-api has no ReferenceGrant. What does GET /api/v1/orders return?',
          options: ['200 — any route may reference any Service', '404 — the whole route is rejected', '500 — ResolvedRefs=False (RefNotPermitted); the spec requires requests for an invalid backendRef to get a 500'],
          answer: 2, why: 'Cross-namespace references need a ReferenceGrant in the TARGET namespace (shop-api) allowing HTTPRoute from default to Service. Without it the route is still Accepted, but ResolvedRefs=False/RefNotPermitted and that rule’s traffic gets HTTP 500. /web (same namespace) keeps working.' } },
      { id: 'cert-missing', label: 'certificateRefs Secret missing', set: { gwcAccepted: true, routeAttached: true, routeExact: false, refGrant: true, certRef: false },
        predict: { q: 'The HTTPS listener’s tls.certificateRefs names Secret shop-tls, which does not exist. What do HTTPS clients get?',
          options: ['A failed TLS handshake — the listener reports ResolvedRefs=False (InvalidCertificateRef) and is not programmed; Gateway API does not promise a fallback certificate', 'A self-signed default certificate, like ingress-nginx', 'Plain HTTP on 443'],
          answer: 0, why: 'Listener status is the place to look: `kubectl describe gateway shop-gw` → Listeners → https → ResolvedRefs False, InvalidCertificateRef; Programmed False. Create the kubernetes.io/tls Secret in the Gateway’s namespace (or a ReferenceGrant for a Secret elsewhere).' } },
      { id: 'heal', label: 'Reset', set: { gwcAccepted: true, routeAttached: true, routeExact: false, refGrant: true, certRef: true } }
    ],
    derive: function (s) {
      var d = gatewayDecide(s);
      var rules = [];
      rules.push(rule('^ingress-controller$', !s.gwcAccepted ? { tint: 'down', glow: 0 } : (s.certRef ? { tint: 'ok', glow: 0.4 } : { tint: 'warn', glow: 0.5 })));
      rules.push(rule('^tls-terminate$', !s.gwcAccepted ? { tint: 'down', glow: 0 } : (s.certRef ? { tint: 'ok', glow: 0.5 } : { tint: 'deny', glow: 0.85, pulse: true })));
      rules.push(rule('^rule-2$', !s.gwcAccepted ? { tint: 'down', glow: 0 } : (s.routeAttached ? { tint: 'gold', glow: 0.35 } : { tint: 'warn', glow: 0.7, pulse: true })));
      var routeOff = !s.gwcAccepted || !s.routeAttached;
      rules.push(rule('^rule-0$', routeOff ? { tint: 'down', glow: 0 } : (!s.refGrant ? { tint: 'deny', glow: 0.6, pulse: true } : (s.routeExact ? { tint: 'warn', glow: 0.45 } : { tint: 'gold', glow: 0.35 }))));
      rules.push(rule('^rule-1$', routeOff ? { tint: 'down', glow: 0 } : { tint: 'gold', glow: 0.35 }));
      var STYLE = { 200: { tint: 'ok', glow: 0.55, pulse: true }, 404: { tint: 'warn', glow: 0.55, pulse: true }, 500: { tint: 'deny', glow: 0.75, pulse: true },
        'tls-fail': { tint: 'deny', glow: 0.4 }, 'no-route': { tint: 'down', glow: 0 } };
      var toSvc = [false, false], svcErr = [false, false];
      d.clients.forEach(function (c, i) {
        rules.push(rule('^req-' + i + '-\\d$', STYLE[c.status]));
        rules.push(rule('^client-' + i + '$', c.status === 200 ? { tint: 'gold', glow: 0.4 } : (c.status === 'no-route' ? { tint: 'muted', glow: 0.1 } : { tint: c.status === 404 ? 'warn' : 'deny', glow: 0.4 })));
        if (c.svc !== null) { toSvc[c.svc] = true; if (c.status === 500) svcErr[c.svc] = true; }
      });
      [0, 1].forEach(function (k) {
        rules.push(rule('^route-' + k + '-\\d$', toSvc[k] ? (svcErr[k] ? { tint: 'deny', glow: 0.6, pulse: true } : { tint: 'ok', glow: 0.5, pulse: true }) : { hide: true }));
      });
      rules.push(rule('^service-0$', s.refGrant ? { tint: 'gold', glow: 0.35 } : { tint: 'deny', glow: 0.7, pulse: true }));
      rules.push(rule('^service-1$', { tint: 'gold', glow: 0.35 }));
      rules.push(rule('^endpoint-pod-[0-3]$', { tint: 'ok', glow: 0.3 }));
      rules.push(rule('^ep-[01]-\\d$', toSvc[0] && !svcErr[0] ? { tint: 'ok', glow: 0.5, pulse: true } : { hide: true }));
      rules.push(rule('^ep-[23]-\\d$', toSvc[1] ? { tint: 'ok', glow: 0.5, pulse: true } : { hide: true }));
      var LBL = { 'no-route': 'no address (Gateway Pending)', 'tls-fail': 'TLS handshake fails (listener not programmed)' };
      var codes = d.clients.map(function (c) { return 'GET ' + c.path + ' → ' + (LBL[c.status] || (c.status + (c.svc !== null ? ' service-' + c.svc : ' no matching route'))); });
      var bad = d.clients.filter(function (c) { return c.status !== 200; }).length;
      var verdict = (!s.gwcAccepted || !s.certRef) ? 'down' : (bad ? 'degraded' : 'healthy');
      var st = ' · Gateway ' + (d.gatewayProgrammed === 'True' ? 'Programmed' : (d.gatewayProgrammed === 'Unknown' ? 'Pending' : 'not Programmed (' + d.listener + ')')) +
        (s.gwcAccepted && !s.routeAttached ? ' · HTTPRoute not Accepted (NoMatchingListenerHostname)' : '') +
        (!s.refGrant ? ' · backendRef RefNotPermitted' : '') + ' · /api ' + d.matchType;
      return { verdict: verdict, metrics: d, caption: codes.join(' · ') + st, rules: rules };
    }
  };

  /* ── ConfigMaps & Secrets: update propagation · immutable · missing keys · etcd at rest (CKA workloads) ──
   * Scene contract (secrets-configmaps.glb): env-chip-0 = DB_PASS ← secretKeyRef db-creds/password (secret-key-1),
   * env-chip-1 = LOG_LEVEL ← configMapKeyRef, volume-configmap = app-config at /etc/config. */
  function configDecide(s) {
    var editApplied = !!s.cmEdited && !s.immutable;
    var volumeFresh = !editApplied || !!s.restarted || (!s.subPath && !!s.synced);
    var envFresh = !editApplied || !!s.restarted;
    return {
      editApplied: editApplied,
      editRejected: !!s.cmEdited && !!s.immutable,
      volumeFresh: volumeFresh,
      envFresh: envFresh,
      pod: s.keyMissing ? 'CreateContainerConfigError' : 'Running',
      etcdAtRest: s.encryptAtRest ? 'encrypted' : 'unencrypted'
    };
  }

  var config = {
    id: 'config-propagation',
    title: 'ConfigMap & Secret drill — what updates, what never does',
    cert: 'CKA',
    glb: '/assets/immersive/secrets-configmaps.glb',
    initial: { cmEdited: false, synced: false, subPath: false, immutable: false, restarted: false, keyMissing: false, encryptAtRest: false },
    toggles: [
      { id: 'cmEdited', label: 'kubectl edit app-config (LOG_LEVEL=debug)', on: 'edited', off: 'original', risk: 'none' },
      { id: 'synced', label: 'kubelet sync period', on: 'elapsed', off: 'not yet', risk: 'none' },
      { id: 'subPath', label: 'app.properties mount', on: 'subPath', off: 'whole volume', risk: 'on' },
      { id: 'immutable', label: 'app-config immutable', on: 'true', off: 'false', risk: 'none' },
      { id: 'restarted', label: 'pods since edit', on: 'rollout restart', off: 'same pods', risk: 'none' },
      { id: 'keyMissing', label: 'db-creds key “password”', on: 'missing', off: 'present', risk: 'on' },
      { id: 'encryptAtRest', label: 'EncryptionConfiguration (etcd)', on: 'aescbc/KMS', off: 'none' }
    ],
    scenarios: [
      { id: 'volume-vs-env', label: 'Edit ConfigMap, wait', set: { cmEdited: true, synced: true, subPath: false, immutable: false, restarted: false, keyMissing: false },
        predict: { q: 'You kubectl edit configmap app-config to LOG_LEVEL=debug. The pod mounts it as a volume at /etc/config AND reads LOG_LEVEL via configMapKeyRef. A couple of minutes later, with no restart, what does the container see?',
          options: ['Both the file and the env var show debug', 'Neither — ConfigMaps are read once at scheduling', 'The mounted file shows debug (kubelet sync); the env var still has the old value'],
          answer: 2, why: 'Projected ConfigMap volumes are refreshed by the kubelet on its sync loop (delay ≈ sync period + cache TTL, often up to a minute or two). Environment variables are resolved once, at container start.' } },
      { id: 'subpath', label: 'subPath mount', set: { cmEdited: true, synced: true, subPath: true, immutable: false, restarted: false, keyMissing: false },
        predict: { q: 'Same edit, but /etc/config/app.properties is mounted with subPath. After the kubelet sync?',
          options: ['Still the old content — subPath mounts never receive ConfigMap updates', 'Updated, just later than a full volume', 'The container is restarted automatically'],
          answer: 0, why: 'A subPath is bind-mounted once from the volume and is not swapped on update. Only a new container (rollout restart) sees the change — or mount the whole volume instead.' } },
      { id: 'immutable', label: 'immutable: true', set: { cmEdited: true, synced: true, subPath: false, immutable: true, restarted: false, keyMissing: false },
        predict: { q: 'app-config has immutable: true. You try to change LOG_LEVEL with kubectl edit. What happens?',
          options: ['The edit succeeds; pods only see it after a restart', 'The API server rejects the update — an immutable ConfigMap can only be deleted and recreated', 'The edit succeeds but the kubelet ignores it'],
          answer: 1, why: 'immutable: true makes data/binaryData read-only (and lets the kubelet stop watching it, which reduces apiserver load). The usual pattern is a new name (app-config-v2) plus a rollout.' } },
      { id: 'restart', label: 'Rollout restart', set: { cmEdited: true, synced: false, subPath: true, immutable: false, restarted: true, keyMissing: false },
        predict: { q: 'With the subPath mount still in place, you run kubectl rollout restart deployment/api. What do the new pods see?',
          options: ['The new value everywhere — env vars, subPath and volume files are all read when the container starts', 'Only the env var updates', 'Nothing — subPath pins the original content forever'],
          answer: 0, why: 'New pods resolve env vars and set up mounts from the current ConfigMap. Restart (or a hash annotation that changes the pod template) is the reliable way to roll config.' } },
      { id: 'missing-key', label: 'secretKeyRef to a missing key', set: { cmEdited: false, keyMissing: true, restarted: false },
        predict: { q: 'env DB_PASS uses secretKeyRef {name: db-creds, key: password} with optional unset (false). The Secret has no “password” key. Pod status?',
          options: ['Running with DB_PASS set to an empty string', 'CreateContainerConfigError — the container is not started until the key exists', 'CrashLoopBackOff'],
          answer: 1, why: 'A required (non-optional) reference to a missing Secret/ConfigMap or key fails container creation; `kubectl describe pod` shows “couldn’t find key password in Secret”. With optional: true the variable is simply omitted.' } },
      { id: 'base64', label: 'Secrets at rest', set: { cmEdited: false, keyMissing: false, encryptAtRest: false },
        predict: { q: 'kube-apiserver has no EncryptionConfiguration. Someone with read access to etcd dumps /registry/secrets/default/db-creds. What do they get?',
          options: ['AES ciphertext — Secrets are always encrypted in etcd', 'Nothing — Secret data only lives in kubelet tmpfs', 'The password, readable — without encryption at rest Secret data is stored unencrypted; base64 in the API is encoding, not encryption'],
          answer: 2, why: 'Encryption at rest is opt-in: --encryption-provider-config with aescbc/aesgcm/secretbox or a KMS provider, then rewrite existing Secrets. Also lock down RBAC on get/list secrets — anyone who can read them gets the plaintext.' } },
      { id: 'heal', label: 'Reset', set: { cmEdited: false, synced: false, subPath: false, immutable: false, restarted: false, keyMissing: false, encryptAtRest: false } }
    ],
    derive: function (s) {
      var d = configDecide(s);
      var rules = [];
      rules.push(rule('^configmap-app-config$', d.editRejected ? { tint: 'deny', glow: 0.8, pulse: true } : (s.immutable ? { tint: 'gold', glow: 0.45 } : { tint: 'ok', glow: 0.25 })));
      rules.push(rule('^configmap-sheet-\\d$', { tint: s.immutable ? 'gold' : 'ok', glow: 0.15 }));
      rules.push(rule('^configmap-sheet-0$', d.editApplied ? { tint: 'gold', glow: 0.7, pulse: true } : (d.editRejected ? { tint: 'deny', glow: 0.5 } : { tint: s.immutable ? 'gold' : 'ok', glow: 0.2 })));
      var stale = { tint: 'warn', glow: 0.7, pulse: true };
      rules.push(rule('^volume-configmap$', !d.volumeFresh ? stale : (d.editApplied ? { tint: 'ok', glow: 0.6, pulse: true } : { tint: 'ok', glow: 0.3 })));
      rules.push(rule('^edge-configmap-mount$', !d.volumeFresh ? { tint: 'warn', glow: 0.4 } : { tint: 'ok', glow: 0.35 }));
      rules.push(rule('^env-chip-1$', !d.envFresh ? stale : { tint: 'ok', glow: 0.35 }));
      var syncing = d.editApplied && !s.synced && !s.subPath && !s.restarted;
      rules.push(rule('^kubelet-led$', syncing ? { tint: 'gold', glow: 0.8, pulse: true } : { tint: 'ok', glow: 0.3 }));
      rules.push(rule('^secret-key-1$', s.keyMissing ? { hide: true } : { tint: 'gold', glow: 0.35 }));
      rules.push(rule('^env-chip-0$', s.keyMissing ? { tint: 'deny', glow: 0.85, pulse: true } : { tint: 'gold', glow: 0.35 }));
      rules.push(rule('^(container-app|pod-boundary)$', s.keyMissing ? { tint: 'deny', glow: 0.6, pulse: true } : { tint: 'ok', glow: 0.35 }));
      rules.push(rule('^etcd-store$', s.encryptAtRest ? { tint: 'ok', glow: 0.45 } : { tint: 'warn', glow: 0.5, pulse: true }));
      rules.push(rule('^edge-etcd-secret$', s.encryptAtRest ? { tint: 'ok', glow: 0.3 } : { tint: 'warn', glow: 0.45 }));
      rules.push(rule('^secret-lock$', { tint: 'gold', glow: 0.4 }));
      var cap = [];
      if (d.editRejected) cap.push('edit REJECTED — app-config is immutable');
      else if (d.editApplied) cap.push('LOG_LEVEL=debug in the API · /etc/config ' + (d.volumeFresh ? 'updated' : (s.subPath ? 'stale (subPath never updates)' : 'stale until kubelet sync')) + ' · env ' + (d.envFresh ? 'updated (new pods)' : 'stale until restart'));
      else cap.push('LOG_LEVEL=info everywhere');
      cap.push(s.keyMissing ? 'pod CreateContainerConfigError (db-creds has no key “password”)' : 'pod Running · DB_PASS from db-creds');
      cap.push('etcd: Secret data ' + (s.encryptAtRest ? 'encrypted at rest' : 'NOT encrypted (base64 ≠ encryption)'));
      var verdict = s.keyMissing ? 'down' : (d.editRejected ? 'rejected' : ((!d.volumeFresh || !d.envFresh) ? 'stale' : (s.encryptAtRest ? 'healthy' : 'exposed-at-rest')));
      return { verdict: verdict, metrics: d, caption: cap.join(' · '), rules: rules };
    }
  };

  /* ── CNI / pod networking (CKA services & networking + troubleshooting) ──
   * Scene contract (cni-pod-network.glb): two nodes × three pods, cni-bridge + overlay arcs (cross-node),
   * cluster-ip (Service VIP, programmed by kube-proxy), coredns (assumed scheduled on node-1). */
  function cniDecide(s) {
    var cni = !!s.cniInstalled;
    var sameNode = cni;
    var crossNode = cni && !s.cidrOverlap;
    var clusterIp = cni && !!s.kubeProxy;                 /* VIP → endpoint rules programmed on every node */
    var dns = clusterIp && !!s.corednsUp && crossNode;   /* client on node-0 reaches CoreDNS on node-1 via the kube-dns VIP */
    return { nodesReady: cni, podsNetworked: cni, sameNode: sameNode, crossNode: crossNode, clusterIp: clusterIp, dns: dns };
  }

  var cni = {
    id: 'cni-network',
    title: 'CNI drill — node readiness · pod CIDR · Service VIP · DNS',
    cert: 'CKA',
    glb: '/assets/immersive/cni-pod-network.glb',
    initial: { cniInstalled: true, cidrOverlap: false, kubeProxy: true, corednsUp: true },
    toggles: [
      { id: 'cniInstalled', label: 'CNI plugin (/etc/cni/net.d)', on: 'installed', off: 'none' },
      { id: 'cidrOverlap', label: 'pod CIDR vs VPC 10.0.0.0/16', on: 'overlaps', off: '192.168.0.0/16 (distinct)', risk: 'on' },
      { id: 'kubeProxy', label: 'kube-proxy (or replacement)', on: 'running', off: 'not deployed' },
      { id: 'corednsUp', label: 'CoreDNS', on: '2 replicas', off: 'scaled to 0' }
    ],
    scenarios: [
      { id: 'no-cni', label: 'No CNI installed', set: { cniInstalled: false, cidrOverlap: false, kubeProxy: true, corednsUp: true },
        predict: { q: 'Right after kubeadm init/join, before any CNI plugin is installed: what do kubectl get nodes and the CoreDNS pods show?',
          options: ['Nodes NotReady (network plugin not ready); CoreDNS and new pods stay Pending or ContainerCreating — no pod sandbox gets a network', 'Nodes Ready; pods fall back to host networking', 'kubeadm init fails until a CNI is chosen'],
          answer: 0, why: 'The kubelet reports NetworkReady=false (“cni plugin not initialized”) so the node is NotReady and tainted not-ready. Pods that do land fail sandbox creation. Installing Calico/Cilium/flannel fixes both.' } },
      { id: 'cidr-overlap', label: 'Pod CIDR overlaps VPC', set: { cniInstalled: true, cidrOverlap: true, kubeProxy: true, corednsUp: true },
        predict: { q: 'The cluster was created with --pod-network-cidr=10.0.0.0/16 — the same range as the VPC subnet the nodes live in. What breaks?',
          options: ['Nothing — the CNI NATs every packet', 'Routing: pod IPs collide with node/VPC addresses, so cross-node pod traffic (and anything through it, like DNS on the other node) is misrouted', 'kube-apiserver refuses to start'],
          answer: 1, why: 'Pod, Service and node networks must not overlap. Routes for 10.0.x.x become ambiguous: cross-node pod traffic and pod↔host traffic go to the wrong place. Same-node traffic over the bridge can still work, which makes it confusing to debug. Rebuild with a distinct CIDR.' } },
      { id: 'no-kube-proxy', label: 'No kube-proxy', set: { cniInstalled: true, cidrOverlap: false, kubeProxy: false, corednsUp: true },
        predict: { q: 'kube-proxy was never deployed and nothing replaces it (no eBPF kube-proxy replacement). Pod → pod IP works. What about curl to a Service ClusterIP?',
          options: ['Fails — nothing programs the ClusterIP → endpoint rules (iptables/IPVS/nftables) on the nodes', 'Works — the CNI plugin always implements Services', 'Works — CoreDNS returns pod IPs instead'],
          answer: 0, why: 'A ClusterIP is a virtual IP that only exists as rules written by kube-proxy (or a replacement such as Cilium’s). DNS breaks too, because pods reach CoreDNS through the kube-dns ClusterIP.' } },
      { id: 'dns-down', label: 'CoreDNS scaled to 0', set: { cniInstalled: true, cidrOverlap: false, kubeProxy: true, corednsUp: false },
        predict: { q: 'CoreDNS is scaled to 0. A pod curls http://api.default.svc.cluster.local and http://10.96.45.12 (that Service’s ClusterIP). Which works?',
          options: ['Both', 'Only the ClusterIP — name resolution needs CoreDNS, Service routing does not', 'Neither'],
          answer: 1, why: 'Service VIP routing is kube-proxy’s job; DNS is CoreDNS’s. Troubleshoot with `nslookup kubernetes.default` from a pod and `kubectl -n kube-system get pods -l k8s-app=kube-dns`.' } },
      { id: 'heal', label: 'Reset', set: { cniInstalled: true, cidrOverlap: false, kubeProxy: true, corednsUp: true } }
    ],
    derive: function (s) {
      var d = cniDecide(s);
      var rules = [];
      rules.push(rule('^(node|kubelet)-\\d$', d.nodesReady ? { tint: 'ok', glow: 0.25 } : { tint: 'warn', glow: 0.6, pulse: true }));
      rules.push(rule('^node-\\d$', d.nodesReady ? { tint: 'muted', glow: 0.1 } : { tint: 'warn', glow: 0.35, pulse: true }));
      rules.push(rule('^pod-\\d-\\d$', d.podsNetworked ? { tint: 'ok', glow: 0.35 } : { tint: 'muted', glow: 0.3, pulse: true }));
      rules.push(rule('^veth-\\d-\\d$', d.podsNetworked ? { tint: 'gold', glow: 0.3 } : { hide: true }));
      rules.push(rule('^cni-bridge$', s.cniInstalled ? (s.cidrOverlap ? { tint: 'warn', glow: 0.5 } : { tint: 'ok', glow: 0.4 }) : { tint: 'down', glow: 0 }));
      rules.push(rule('^overlay-arc-\\d-\\d$', d.crossNode ? { tint: 'ok', glow: 0.5, pulse: true } : (d.podsNetworked ? { tint: 'deny', glow: 0.7, pulse: true } : { hide: true })));
      rules.push(rule('^cluster-ip$', d.clusterIp ? { tint: 'gold', glow: 0.5 } : (d.podsNetworked ? { tint: 'deny', glow: 0.7, pulse: true } : { tint: 'down', glow: 0 })));
      rules.push(rule('^coredns$', d.dns ? { tint: 'ok', glow: 0.35 } : (s.corednsUp && d.podsNetworked ? { tint: 'warn', glow: 0.5, pulse: true } : { tint: 'deny', glow: 0.6, pulse: true })));
      var yn = function (b) { return b ? 'OK' : 'FAIL'; };
      var cap = !d.nodesReady
        ? 'Nodes NotReady (NetworkReady=false: cni plugin not initialized) · pods Pending/ContainerCreating · CoreDNS Pending'
        : 'Nodes Ready · same-node pod↔pod ' + yn(d.sameNode) + ' · cross-node ' + yn(d.crossNode) + (s.cidrOverlap ? ' (pod CIDR overlaps VPC)' : '') +
          ' · ClusterIP rules ' + (d.clusterIp ? 'programmed' : 'MISSING') + ' · DNS ' + yn(d.dns);
      var verdict = !d.nodesReady ? 'down' : ((d.crossNode && d.clusterIp && d.dns) ? 'healthy' : 'degraded');
      return { verdict: verdict, metrics: d, caption: cap, rules: rules };
    }
  };

  /* ── Service mesh: sidecar injection · mTLS modes · control-plane outage ──
   * Scene contract (service-mesh-sidecar.glb): app-0 = frontend (ns shop, the client), app-1 = payments (already meshed,
   * PeerAuthentication on its namespace). sidecar-0/mtls-0 exist only when frontend pods were created after injection was enabled. */
  function meshDecide(s) {
    var clientSidecar = !!s.nsLabeled && !!s.restarted;
    var mode = s.strict ? 'STRICT' : 'PERMISSIVE';
    var transport = clientSidecar ? 'mTLS' : 'plaintext';
    var accepted = clientSidecar || !s.strict;
    return { clientSidecar: clientSidecar, mode: mode, transport: transport, accepted: accepted, configPush: !!s.cpUp };
  }

  var mesh = {
    id: 'mesh-mtls',
    title: 'Service mesh drill — sidecar injection · STRICT vs PERMISSIVE mTLS',
    cert: 'CKA+ / Istio (ICA)',
    glb: '/assets/immersive/service-mesh-sidecar.glb',
    initial: { nsLabeled: true, restarted: true, strict: true, cpUp: true },
    toggles: [
      { id: 'nsLabeled', label: 'ns shop label istio-injection', on: 'enabled', off: 'absent' },
      { id: 'restarted', label: 'frontend pods', on: 'recreated after label', off: 'pre-date the label' },
      { id: 'strict', label: 'payments PeerAuthentication', on: 'STRICT', off: 'PERMISSIVE', risk: 'none' },
      { id: 'cpUp', label: 'istiod', on: 'up', off: 'down' }
    ],
    scenarios: [
      { id: 'label-no-restart', label: 'Label namespace only', set: { nsLabeled: true, restarted: false, strict: false, cpUp: true },
        predict: { q: 'You kubectl label namespace shop istio-injection=enabled. The frontend pods were already running. Do they get sidecars?',
          options: ['Yes — istiod patches running pods within seconds', 'No — injection is a mutating admission webhook that only runs when a pod is created; restart the workload', 'Only after the node reboots'],
          answer: 1, why: 'The sidecar is added to the pod spec at admission. Pod specs are (mostly) immutable, so existing pods stay unmeshed until `kubectl rollout restart deployment/frontend`.' } },
      { id: 'strict-plain', label: 'STRICT + unmeshed client', set: { nsLabeled: true, restarted: false, strict: true, cpUp: true },
        predict: { q: 'payments has PeerAuthentication mode: STRICT. frontend still has no sidecar. Does frontend → payments work?',
          options: ['No — STRICT accepts only mTLS; the plaintext connection is rejected (reset) by the payments sidecar', 'Yes — the server sidecar upgrades plaintext to mTLS', 'Yes — STRICT only logs violations'],
          answer: 0, why: 'The server-side proxy requires a client certificate in STRICT mode. Non-mesh clients typically see “connection reset by peer” / “upstream connect error”.' } },
      { id: 'permissive', label: 'PERMISSIVE', set: { nsLabeled: true, restarted: false, strict: false, cpUp: true },
        predict: { q: 'Switch payments to PERMISSIVE, frontend still without a sidecar. Result?',
          options: ['Still rejected until frontend is meshed', 'It works over mTLS anyway', 'It works, in plaintext — PERMISSIVE accepts both mTLS and plaintext (the migration mode)'],
          answer: 2, why: 'PERMISSIVE lets meshed and non-meshed clients talk to the workload during migration. Meshed clients still get auto-mTLS; this one is plaintext — fine for a rollout, not as an end state.' } },
      { id: 'restart', label: 'Rollout restart', set: { nsLabeled: true, restarted: true, strict: true, cpUp: true },
        predict: { q: 'Keep STRICT and run kubectl rollout restart deployment/frontend. Now?',
          options: ['Works over mTLS — the new pods get the sidecar and auto-mTLS upgrades the call', 'Still rejected — STRICT needs a DestinationRule first', 'Works in plaintext'],
          answer: 0, why: 'Recreated pods pass the injection webhook. With auto mTLS (the Istio default), the client sidecar detects the server proxy and originates mTLS without extra config.' } },
      { id: 'cp-down', label: 'istiod down', set: { nsLabeled: true, restarted: true, strict: true, cpUp: false },
        predict: { q: 'istiod crashes. What happens to existing meshed traffic frontend → payments?',
          options: ['Stops immediately — every request needs istiod', 'Keeps flowing — sidecars keep the last pushed config; config changes and certificate rotation stop until istiod returns', 'Falls back to plaintext'],
          answer: 1, why: 'The control plane is not in the request path. Proxies keep serving with cached xDS config and current certs (default workload cert lifetime 24h); new config, new endpoints and new sidecar injection are what you lose.' } },
      { id: 'heal', label: 'Reset', set: { nsLabeled: true, restarted: true, strict: true, cpUp: true } }
    ],
    derive: function (s) {
      var d = meshDecide(s);
      var rules = [];
      rules.push(rule('^(sidecar|mtls)-0$', d.clientSidecar ? { tint: 'ok', glow: 0.45 } : { hide: true }));
      rules.push(rule('^mtls-0$', d.clientSidecar ? { tint: 'gold', glow: 0.6 } : { hide: true }));
      rules.push(rule('^sidecar-1$', { tint: 'ok', glow: 0.4 }));
      rules.push(rule('^mtls-1$', s.strict ? { tint: 'gold', glow: 0.7, pulse: !d.accepted } : { tint: 'warn', glow: 0.35 }));
      var hop = !d.accepted ? { tint: 'deny', glow: 0.8, pulse: true } : (d.transport === 'mTLS' ? { tint: 'gold', glow: 0.55, pulse: true } : { tint: 'warn', glow: 0.55, pulse: true });
      rules.push(rule('^dataplane-hop-\\d$', hop));
      rules.push(rule('^app-0$', { tint: 'muted', glow: 0.15 }));
      rules.push(rule('^app-1$', d.accepted ? { tint: 'ok', glow: 0.3 } : { tint: 'muted', glow: 0.05 }));
      rules.push(rule('^(mesh-control-plane|cp-halo)$', s.cpUp ? { tint: 'gold', glow: 0.35 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^xds-1-\\d$', s.cpUp ? { tint: 'ok', glow: 0.45, pulse: true } : { hide: true }));
      rules.push(rule('^xds-0-\\d$', s.cpUp && d.clientSidecar ? { tint: 'ok', glow: 0.45, pulse: true } : { hide: true }));
      var cap = 'frontend ' + (d.clientSidecar ? 'has sidecar' : (s.nsLabeled ? 'NO sidecar (pods pre-date the label)' : 'NO sidecar (namespace not labeled)')) +
        ' → payments (' + d.mode + '): ' + (d.accepted ? d.transport + ' accepted' : 'plaintext REJECTED') +
        (s.cpUp ? '' : ' · istiod down — data plane on last-known config, no new config/cert rotation');
      var verdict = !d.accepted ? 'down' : ((d.transport === 'plaintext' || !s.cpUp) ? 'degraded' : 'healthy');
      return { verdict: verdict, metrics: d, caption: cap, rules: rules };
    }
  };

  /* ── Control-plane component failures (CKA troubleshooting) ──
   * Scene contract (lecture-k8s-control-plane.glb): api-server, scheduler, controller-manager on the control plane;
   * worker-0..4 with kubelet-led-N. Workload: Deployment web (3 replicas) already Running. */
  function controlPlaneDecide(s) {
    var api = !!s.apiUp, sched = !!s.schedUp, cm = !!s.cmUp;
    return {
      kubectl: api,
      runningPodsKeepRunning: true,
      /* Pods for a scale-up or a deleted replica are created by the ReplicaSet controller (kcm), then bound by the scheduler. */
      controllerPods: !api ? 'no-api' : (!cm ? 'not-created' : (!sched ? 'pending' : 'scheduled')),
      deletedPodReplaced: api && cm,
      /* The node lifecycle controller (in kube-controller-manager) marks a silent node NotReady/Unknown. */
      worker2NotReady: !s.kubelet2Up && api && cm,
      worker2Silent: !s.kubelet2Up
    };
  }

  var controlPlane = {
    id: 'control-plane-failure',
    title: 'Control-plane failure drill — which component did you lose?',
    cert: 'CKA',
    glb: '/assets/immersive/lecture-k8s-control-plane.glb',
    initial: { apiUp: true, schedUp: true, cmUp: true, kubelet2Up: true },
    toggles: [
      { id: 'apiUp', label: 'kube-apiserver', on: 'up', off: 'down' },
      { id: 'schedUp', label: 'kube-scheduler', on: 'up', off: 'down' },
      { id: 'cmUp', label: 'kube-controller-manager', on: 'up', off: 'down' },
      { id: 'kubelet2Up', label: 'kubelet on worker-2', on: 'running', off: 'stopped' }
    ],
    scenarios: [
      { id: 'api-down', label: 'API server down', set: { apiUp: false, schedUp: true, cmUp: true, kubelet2Up: true },
        predict: { q: 'kube-apiserver is down (a bad flag in its static pod manifest). What happens to the pods already running on the workers?',
          options: ['They are evicted after the grace period', 'They keep running — kubelets keep existing containers alive; kubectl and every controller just lose the API', 'They restart in a loop until the API returns'],
          answer: 1, why: 'The data plane does not need the API server to keep running containers. Fix the manifest in /etc/kubernetes/manifests; check with crictl ps and the kubelet logs while kubectl is unavailable.' } },
      { id: 'sched-down', label: 'Scheduler down', set: { apiUp: true, schedUp: false, cmUp: true, kubelet2Up: true },
        predict: { q: 'kube-scheduler is down. You kubectl scale deployment web --replicas=5 (from 3). Result?',
          options: ['Two new pods are created but stay Pending with no nodeName until the scheduler returns', 'The scale command is rejected', 'The kubelets schedule the pods themselves'],
          answer: 0, why: 'The ReplicaSet controller creates the pod objects; binding them to nodes is the scheduler’s job. Pending pods with no events from default-scheduler point at the scheduler.' } },
      { id: 'cm-down', label: 'Controller-manager down', set: { apiUp: true, schedUp: true, cmUp: false, kubelet2Up: true },
        predict: { q: 'kube-controller-manager is down. You delete one pod of the 3-replica web Deployment. What happens?',
          options: ['The scheduler recreates it', 'The kubelet restarts it on the same node', 'It is not replaced — the ReplicaSet controller is not running, so web stays at 2 until kcm returns'],
          answer: 2, why: 'Reconciliation (ReplicaSet, Deployment, node lifecycle, endpoints …) lives in kube-controller-manager. Without it, desired state is stored but nobody acts on it.' } },
      { id: 'kubelet-down', label: 'kubelet stops on worker-2', set: { apiUp: true, schedUp: true, cmUp: true, kubelet2Up: false },
        predict: { q: 'The kubelet on worker-2 stops. What does kubectl get nodes show, and what happens to its pods?',
          options: ['worker-2 NotReady once node-monitor-grace-period passes (50s default since v1.32, 40s before); its pods are evicted about 5 minutes later (default 300s unreachable toleration)', 'worker-2 disappears from the node list immediately', 'Ready — its containers are still running'],
          answer: 0, why: 'The node lifecycle controller in kube-controller-manager stops seeing lease/status updates, sets Ready=Unknown (shown as NotReady) and taints the node unreachable:NoExecute. Pods tolerate that for 300s by default, then get evicted and recreated elsewhere.' } },
      { id: 'heal', label: 'Reset', set: { apiUp: true, schedUp: true, cmUp: true, kubelet2Up: true } }
    ],
    derive: function (s) {
      var d = controlPlaneDecide(s);
      var rules = [];
      rules.push(rule('^api-server$', s.apiUp ? { tint: 'ok', glow: 0.4 } : { tint: 'deny', glow: 0.85, pulse: true }));
      rules.push(rule('^cp-halo$', s.apiUp ? { tint: 'ok', glow: 0.3 } : { tint: 'deny', glow: 0.5, pulse: true }));
      rules.push(rule('^scheduler$', s.schedUp ? { tint: 'ok', glow: 0.4 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^controller-manager$', s.cmUp ? { tint: 'ok', glow: 0.4 } : { tint: 'down', glow: 0 }));
      var allUp = s.apiUp && s.schedUp && s.cmUp;
      rules.push(rule('^control-plane$', allUp ? { tint: 'gold', glow: 0.3 } : { tint: 'warn', glow: 0.45, pulse: true }));
      rules.push(rule('^kubelet-led-\\d$', { tint: 'ok', glow: 0.5 }));
      rules.push(rule('^worker-\\d$', { tint: 'muted', glow: 0.12 }));
      rules.push(rule('^kubelet-led-2$', s.kubelet2Up ? { tint: 'ok', glow: 0.5 } : { tint: 'deny', glow: 0.85, pulse: true }));
      rules.push(rule('^worker-2$', d.worker2NotReady ? { tint: 'warn', glow: 0.55, pulse: true } : (d.worker2Silent ? { tint: 'muted', glow: 0.25, pulse: true } : { tint: 'muted', glow: 0.12 })));
      var cap = [];
      cap.push(s.apiUp ? 'kubectl OK' : 'kubectl: connection refused (API down)');
      cap.push('running pods keep running');
      if (!s.apiUp) cap.push('no scheduling, no reconciliation');
      else {
        cap.push('scale-up / replacement pods ' + ({ 'not-created': 'never created (no ReplicaSet controller)', pending: 'created but Pending (no scheduler)', scheduled: 'created and scheduled' })[d.controllerPods]);
      }
      if (!s.kubelet2Up) cap.push(d.worker2NotReady ? 'worker-2 NotReady after node-monitor-grace-period → evictions after 300s' : 'worker-2 kubelet silent but nobody marks it NotReady (no node lifecycle controller)');
      var verdict = !s.apiUp ? 'down' : ((s.schedUp && s.cmUp && s.kubelet2Up) ? 'healthy' : 'degraded');
      return { verdict: verdict, metrics: d, caption: cap.join(' · '), rules: rules };
    }
  };

  /* ── Worker-node troubleshooting (CKA Troubleshooting, 30% of the exam) — v1.5.0 (2026-10-22) ──
   * Scene contract (node-troubleshoot.glb, authored 2026-10-22): systemd-ring → kubelet (+ kubelet-led, kubelet-unit
   * drop-in, kubelet-config) → edge-kubelet-cri → cri-socket → containerd → cni-conf / cni-plugin; edge-node-lease to
   * control-plane-api + node-lifecycle-controller; pods ranked for eviction (Guaranteed → BestEffort); nodefs gauge with
   * sim-disk-fill-3/4; journal pages; sim-taint-flag. Ready/taint/eviction follow documented kubelet + node lifecycle
   * controller behaviour; durations are not simulated (no clock). */
  function nodeDecide(s) {
    var active = !!s.kubeletOn && !!s.execLoaded;
    var unit = !s.kubeletOn ? 'inactive' : (!s.execLoaded ? 'auto-restart-203' : 'active');
    var ready = !active ? 'Unknown' : (!s.runtimeUp ? 'False-runtime' : (!s.cniOk ? 'False-cni' : 'True'));
    var reason = { Unknown: 'NodeStatusUnknown: Kubelet stopped posting node status.',
      'False-runtime': 'KubeletNotReady: container runtime is down',
      'False-cni': 'KubeletNotReady: container runtime network not ready: NetworkReady=false reason:NetworkPluginNotReady message:Network plugin returns error: cni plugin not initialized',
      True: 'KubeletReady: kubelet is posting ready status' }[ready];
    var pressure = active && !!s.diskPressure;
    var taint = ready === 'Unknown' ? 'node.kubernetes.io/unreachable' : (ready !== 'True' ? 'node.kubernetes.io/not-ready' : (pressure ? 'node.kubernetes.io/disk-pressure' : null));
    return {
      kubeletActive: active,
      kubeletUnit: unit,
      ready: ready,
      readyStatus: ready === 'True' ? 'True' : (ready === 'Unknown' ? 'Unknown' : 'False'),
      reason: reason,
      diskPressure: active ? !!s.diskPressure : 'Unknown',
      taint: taint,
      taintEffects: !taint ? [] : (taint === 'node.kubernetes.io/disk-pressure' ? ['NoSchedule'] : ['NoSchedule', 'NoExecute']),
      /* containers survive a kubelet stop and a containerd stop (containerd-shim keeps them; containerd.service KillMode=process) */
      runningContainersKeepRunning: true,
      evictBestEffort: pressure && !!s.runtimeUp,
      newPodsLand: ready === 'True' && !pressure,
      crictl: !!s.runtimeUp,
      daemonReloadNeeded: !!s.execOnDisk && !s.execLoaded
    };
  }

  var nodeTrouble = {
    id: 'node-troubleshoot',
    title: 'Worker-node troubleshooting drill — kubelet, runtime, CNI, disk pressure',
    cert: 'CKA',
    glb: '/assets/immersive/node-troubleshoot.glb',
    initial: { kubeletOn: true, execLoaded: true, execOnDisk: true, runtimeUp: true, cniOk: true, diskPressure: false },
    toggles: [
      { id: 'kubeletOn', label: 'kubelet.service', on: 'started', off: 'stopped' },
      { id: 'execLoaded', label: 'kubelet ExecStart (as loaded by systemd)', on: '/usr/bin/kubelet', off: '/usr/local/bin/kubelet (missing)' },
      { id: 'runtimeUp', label: 'containerd', on: 'running', off: 'stopped' },
      { id: 'cniOk', label: '/etc/cni/net.d', on: '10-calico.conflist', off: 'empty' },
      { id: 'diskPressure', label: 'nodefs.available', on: '< 10% (evictionHard)', off: 'healthy', risk: 'on' }
    ],
    scenarios: [
      { id: 'exec-203', label: 'kubelet 203/EXEC', set: { kubeletOn: true, execLoaded: false, execOnDisk: false, runtimeUp: true, cniOk: true, diskPressure: false },
        predict: { q: 'After an in-place upgrade node-01 is NotReady. On node-01, systemctl status kubelet shows “activating (auto-restart) … status=203/EXEC”. Where is the fault?',
          options: ['The kubelet client certificate expired, so the API server rejects the node', 'containerd is down, so the kubelet cannot start', 'systemd cannot exec the unit’s ExecStart — the kubeadm drop-in points at a kubelet binary path that does not exist'],
          answer: 2, why: '203/EXEC is systemd failing to execute ExecStart, before the kubelet runs a single line. Compare ExecStart in 10-kubeadm.conf with `which kubelet`, fix the path, then systemctl daemon-reload and restart. A certificate or runtime fault would show the kubelet running and logging errors instead.' } },
      { id: 'reload', label: 'Fixed on disk, not reloaded', set: { kubeletOn: true, execLoaded: false, execOnDisk: true, runtimeUp: true, cniOk: true, diskPressure: false },
        predict: { q: 'You fixed ExecStart in the drop-in and ran systemctl restart kubelet. It still fails with 203/EXEC. Why?',
          options: ['systemd still has the old unit definition loaded — run systemctl daemon-reload, then restart', 'The kubelet caches its binary path in /var/lib/kubelet/config.yaml', 'The node has to be drained and re-joined with kubeadm'],
          answer: 0, why: 'systemd reads unit files and drop-ins when it loads them. After an edit, systemctl warns that the unit changed on disk; daemon-reload picks up the change. /var/lib/kubelet/config.yaml holds kubelet settings, not the binary path.' } },
      { id: 'runtime-down', label: 'containerd stopped', set: { kubeletOn: true, execLoaded: true, execOnDisk: true, runtimeUp: false, cniOk: true, diskPressure: false },
        predict: { q: 'containerd stops on node-01 but the kubelet keeps running. What happens to the containers already running there?',
          options: ['They die with the runtime', 'They keep running (each is held by its containerd-shim), but node-01 goes NotReady — “container runtime is down” — and nothing new can start there', 'Nothing visible: node-01 stays Ready because the kubelet still posts status'],
          answer: 1, why: 'containerd-shim processes keep containers alive when containerd itself stops (the upstream containerd.service uses KillMode=process). The kubelet’s runtime check fails, so it reports Ready=False and the node gets the not-ready taint; crictl fails at the socket. As on any NotReady node, pods are evicted once the default 300s not-ready toleration runs out. systemctl start containerd recovers it.' } },
      { id: 'cni-missing', label: 'CNI config deleted', set: { kubeletOn: true, execLoaded: true, execOnDisk: true, runtimeUp: true, cniOk: false, diskPressure: false },
        predict: { q: 'Someone emptied /etc/cni/net.d on node-01. What does kubectl get nodes show?',
          options: ['node-01 NotReady — the kubelet reports NetworkReady=false: cni plugin not initialized', 'node-01 Ready — pod networking is only the CNI DaemonSet’s concern', 'node-01 disappears from the list until the CNI is reinstalled'],
          answer: 0, why: 'With no CNI config the runtime reports NetworkReady=false and the kubelet turns that into Ready=False (“container runtime network not ready … cni plugin not initialized”) — the same reason a fresh kubeadm cluster stays NotReady until a CNI is installed. Restarting the CNI DaemonSet pod lets its install step write the conflist back.' } },
      { id: 'disk-pressure', label: 'nodefs below 10%', set: { kubeletOn: true, execLoaded: true, execOnDisk: true, runtimeUp: true, cniOk: true, diskPressure: true },
        predict: { q: 'nodefs.available on node-01 drops below the kubelet’s hard eviction threshold (default 10%). What does the kubelet do?',
          options: ['Evicts pods at random until usage is below the threshold', 'Marks node-01 NotReady and stops every pod', 'Sets DiskPressure=True (the node gets the disk-pressure:NoSchedule taint), reclaims dead containers and unused images, then evicts pods — BestEffort first, Guaranteed last'],
          answer: 2, why: 'Node-pressure eviction: the kubelet first reclaims node-level resources, then ranks pods — usage above requests first, then priority, then usage relative to requests. BestEffort pods request nothing, so they go first. Ready stays True; the taint keeps new pods off. crictl rmi --prune frees image space by hand.' } },
      { id: 'heal', label: 'Reset', set: { kubeletOn: true, execLoaded: true, execOnDisk: true, runtimeUp: true, cniOk: true, diskPressure: false } }
    ],
    derive: function (s) {
      var d = nodeDecide(s), rules = [];
      var kStyle = d.kubeletActive ? { tint: 'ok', glow: 0.45 } : (d.kubeletUnit === 'auto-restart-203' ? { tint: 'deny', glow: 0.85, pulse: true } : { tint: 'down', glow: 0 });
      rules.push(rule('^kubelet$', kStyle));
      rules.push(rule('^kubelet-led$', d.kubeletActive ? { tint: 'ok', glow: 0.6 } : { tint: 'deny', glow: 0.8, pulse: true }));
      rules.push(rule('^systemd-ring$', d.kubeletUnit === 'auto-restart-203' ? { tint: 'warn', glow: 0.55, pulse: true } : { tint: 'ok', glow: 0.25 }));
      rules.push(rule('^kubelet-unit$', s.execLoaded ? { tint: 'ok', glow: 0.15 } : { tint: s.execOnDisk ? 'warn' : 'deny', glow: 0.6, pulse: true }));
      rules.push(rule('^kubelet-config$', d.diskPressure === true ? { tint: 'gold', glow: 0.45 } : { tint: 'muted', glow: 0.1 }));
      rules.push(rule('^edge-kubelet-cri$', d.kubeletActive && s.runtimeUp ? { tint: 'ok', glow: 0.4 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^(cri-socket|containerd|edge-cri-containerd)$', s.runtimeUp ? { tint: 'ok', glow: 0.4 } : { tint: 'deny', glow: 0.8, pulse: true }));
      rules.push(rule('^cni-conf$', s.cniOk ? { tint: 'ok', glow: 0.2 } : { tint: 'deny', glow: 0.8, pulse: true }));
      rules.push(rule('^(cni-plugin|edge-containerd-cni)$', s.cniOk && s.runtimeUp ? { tint: 'ok', glow: 0.35 } : { tint: 'muted', glow: 0.05 }));
      rules.push(rule('^node-ready-lamp$', d.ready === 'True' ? { tint: 'ok', glow: 0.7 } : (d.ready === 'Unknown' ? { tint: 'warn', glow: 0.8, pulse: true } : { tint: 'deny', glow: 0.8, pulse: true })));
      rules.push(rule('^edge-node-lease$', d.kubeletActive ? { tint: 'ok', glow: 0.45 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^control-plane-api$', { tint: 'ok', glow: 0.35 }));
      rules.push(rule('^node-lifecycle-controller$', d.taint ? { tint: 'gold', glow: 0.7, pulse: true } : { tint: 'ok', glow: 0.25 }));
      rules.push(rule('^sim-taint-flag$', d.taint ? { show: true, tint: 'warn', glow: 0.6 } : { hide: true }));
      var podOk = d.ready === 'Unknown' ? { tint: 'warn', glow: 0.3, pulse: true } : { tint: 'ok', glow: 0.35 };
      rules.push(rule('^pod-(guaranteed|burstable)$', podOk));
      rules.push(rule('^pod-besteffort-[01]$', d.evictBestEffort ? { tint: 'deny', glow: 0.2, pulse: true } : (d.ready === 'Unknown' ? podOk : { tint: 'muted', glow: 0.2 })));
      rules.push(rule('^disk-fill-[0-2]$', d.diskPressure === true ? { tint: 'warn', glow: 0.45 } : { tint: 'ok', glow: 0.25 }));
      rules.push(rule('^sim-disk-fill-[34]$', d.diskPressure === true ? { show: true, tint: 'deny', glow: 0.7, pulse: true } : { hide: true }));
      rules.push(rule('^disk-gauge$', d.diskPressure === true ? { tint: 'warn', glow: 0.4 } : { tint: 'ok', glow: 0.15 }));
      var evidence = !d.kubeletActive || !s.runtimeUp || !s.cniOk || d.diskPressure === true;
      rules.push(rule('^journal-page-[0-2]$', evidence ? { tint: 'gold', glow: 0.55, pulse: true } : { tint: 'muted', glow: 0.1 }));
      var verdict = d.ready !== 'True' ? 'down' : (d.diskPressure === true ? 'degraded' : 'healthy');
      rules.push(rule('^node-chassis$', verdict === 'healthy' ? { tint: 'muted', glow: 0.1 } : { tint: verdict === 'down' ? 'deny' : 'warn', glow: 0.25 }));
      var cap = ['node-01 Ready=' + d.readyStatus + (d.ready !== 'True' ? ' (' + d.reason.split(': ').slice(1).join(': ') + ')' : '')];
      cap.push('kubelet ' + ({ active: 'active (running)', inactive: 'inactive (dead)', 'auto-restart-203': 'activating (auto-restart) status=203/EXEC' })[d.kubeletUnit]);
      if (d.daemonReloadNeeded) cap.push('unit file fixed on disk but systemd still runs the old definition');
      if (!s.runtimeUp) cap.push('containerd down (running containers kept by shims)');
      if (d.taint) cap.push('taint ' + d.taint + ':' + d.taintEffects.join('+'));
      if (d.evictBestEffort) cap.push('DiskPressure → BestEffort pods evicted first');
      if (d.ready !== 'True') cap.push('running containers keep running; evicted after the 300s toleration');
      return { verdict: verdict, metrics: d, caption: cap.join(' · '), rules: rules };
    }
  };

  /* ── Service + DNS troubleshooting (CKA Troubleshooting 30% · Services & Networking 20%) — v1.6.0 (2026-10-23) ──
   * Scene contract (service-dns.glb, authored 2026-10-23): ns-shop / ns-kube-system / ns-data plates; client-pod +
   * resolv-conf; Service svc-api (+ svc-api-port, svc-api-selector), endpointslice-api, api-pod-0/1 with
   * container-port-0/1, edge-svc-pod-0/1, kube-proxy-rules; svc-kube-dns → coredns-0/1 (+ sim-crash-ring-0/1) and the
   * corefile ConfigMap; edge-client-dns; sim-netpol-wall + netpol-tablet; svc-db + db-pod in ns data; edge-client-db;
   * sim-nxdomain-flag. Rules follow documented Service / EndpointSlice / kube-proxy / CoreDNS / NetworkPolicy behaviour
   * and the pod resolv.conf search path (ndots:5). No clock: CrashLoopBackOff back-off and resolver retries are explained. */
  var SVC_DNS_RECORDS = {
    'api.shop.svc.cluster.local': '10.96.88.20',
    'db.data.svc.cluster.local': '10.96.140.5',
    'kube-dns.kube-system.svc.cluster.local': '10.96.0.10',
    'kubernetes.default.svc.cluster.local': '10.96.0.1'
  };
  var SVC_DNS_SEARCH = ['shop.svc.cluster.local', 'svc.cluster.local', 'cluster.local'];
  /** Resolve a name from a pod in ns shop the way glibc / bind nslookup do with ndots:5 and the search list.
   *  opts.noSearch (dig without +search) treats the name as absolute. Returns { status, fqdn, ip, tried }. */
  function svcDnsResolve(s, name, opts) {
    opts = opts || {};
    if (!s.dnsEgress) return { status: 'timeout', fqdn: null, ip: null, tried: [] };
    if (!s.corefileOk) return { status: 'refused', fqdn: null, ip: null, tried: [] };
    var n = String(name || '').toLowerCase(), abs = /\.$/.test(n);
    n = n.replace(/\.$/, '');
    var dots = (n.match(/\./g) || []).length, tried = [];
    var cands = abs || opts.noSearch ? [n] : (dots >= 5 ? [n].concat(SVC_DNS_SEARCH.map(function (d) { return n + '.' + d; }))
      : SVC_DNS_SEARCH.map(function (d) { return n + '.' + d; }).concat([n]));
    for (var i = 0; i < cands.length; i++) {
      tried.push(cands[i]);
      if (SVC_DNS_RECORDS[cands[i]]) return { status: 'ok', fqdn: cands[i], ip: SVC_DNS_RECORDS[cands[i]], tried: tried };
    }
    return { status: 'nxdomain', fqdn: null, ip: null, tried: tried };
  }
  function serviceDnsDecide(s) {
    var endpoints = s.selectorOk ? 2 : 0;
    var dns = !!s.dnsEgress && !!s.corefileOk;
    var apiByIp = endpoints === 0 ? 'refused-no-endpoints' : (s.targetPortOk ? 'ok' : 'refused-target-port');
    var dbName = s.fqdnOk ? 'db.data.svc.cluster.local' : 'db';
    var db = svcDnsResolve(s, dbName);
    return {
      endpoints: endpoints,
      endpointPort: s.targetPortOk ? 8080 : 80,
      targetPort: s.targetPortOk ? 8080 : 80,
      selector: s.selectorOk ? 'app=api' : 'app=api-v2',
      apiByIp: apiByIp,
      /* A ClusterIP Service gets its A record whether or not it has endpoints. */
      apiResolves: svcDnsResolve(s, 'api').status === 'ok',
      apiByName: dns ? apiByIp : 'dns-' + (!s.dnsEgress ? 'timeout' : 'refused'),
      corednsPods: s.corefileOk ? 'Running' : 'CrashLoopBackOff',
      kubeDnsReadyEndpoints: s.corefileOk ? 2 : 0,
      dns: dns,
      dnsFailure: !s.dnsEgress ? 'timeout' : (!s.corefileOk ? 'refused' : null),
      dbName: dbName,
      dbLookup: db.status,
      dbReach: db.status === 'ok'
    };
  }

  var serviceDns = {
    id: 'service-dns',
    title: 'Service + DNS troubleshooting drill — endpoints, targetPort, CoreDNS, DNS egress, FQDNs',
    cert: 'CKA',
    glb: '/assets/immersive/service-dns.glb',
    initial: { selectorOk: true, targetPortOk: true, corefileOk: true, dnsEgress: true, fqdnOk: true },
    toggles: [
      { id: 'selectorOk', label: 'Service api selector', on: 'app=api (matches pods)', off: 'app=api-v2 (matches nothing)' },
      { id: 'targetPortOk', label: 'Service api targetPort', on: '8080 (= containerPort)', off: '80 (nothing listens)' },
      { id: 'corefileOk', label: 'CoreDNS Corefile', on: 'valid', off: 'typo: forwrd' },
      { id: 'dnsEgress', label: 'ns shop egress to kube-dns:53', on: 'allowed', off: 'default-deny (no DNS rule)' },
      { id: 'fqdnOk', label: 'web DB_HOST', on: 'db.data.svc.cluster.local', off: 'db (short name)' }
    ],
    scenarios: [
      { id: 'selector', label: 'Selector matches nothing', set: { selectorOk: false, targetPortOk: true, corefileOk: true, dnsEgress: true, fqdnOk: true },
        predict: { q: 'A deploy changed Service api’s selector to app=api-v2, but the pods are still labelled app=api. From pod web in the same namespace, what does curl http://api do?',
          options: ['curl cannot resolve the host — a Service with no endpoints has no DNS record', 'The name still resolves to the ClusterIP, but the connection is refused at once — the EndpointSlice is empty, so kube-proxy rejects traffic to that ClusterIP', 'It hangs, then times out after the TCP connect timeout'],
          answer: 1, why: 'A ClusterIP Service gets its DNS A record whether or not anything backs it. The EndpointSlice controller only lists Ready pods whose labels match spec.selector, so the slice is empty. kube-proxy installs a REJECT rule for a Service with no endpoints, so the connection is refused instead of timing out. Compare `kubectl get svc api -o wide` (SELECTOR) with `kubectl get pods --show-labels`.' } },
      { id: 'target-port', label: 'targetPort ≠ containerPort', set: { selectorOk: true, targetPortOk: false, corefileOk: true, dnsEgress: true, fqdnOk: true },
        predict: { q: 'Service api is port 80 → targetPort 80, but the api container listens on 8080. What does kubectl get endpointslices -l kubernetes.io/service-name=api show, and what does curl http://api get?',
          options: ['Both pod IPs with port 80 — the selector is fine; the connection is refused because nothing listens on :80 in the pods. Set targetPort to 8080', 'An empty slice — the controller drops pods whose containerPort does not match targetPort', 'Both pod IPs with port 8080 — kube-proxy rewrites the port to the containerPort'],
          answer: 0, why: 'EndpointSlices copy the Service’s targetPort; they do not check what the container actually listens on (containerPort is informational). kube-proxy DNATs to podIP:80, and the pod answers with a TCP reset. `kubectl describe svc api` shows TargetPort 80/TCP; `kubectl describe deployment api` shows Port 8080/TCP.' } },
      { id: 'corefile', label: 'Corefile typo', set: { selectorOk: true, targetPortOk: true, corefileOk: false, dnsEgress: true, fqdnOk: true },
        predict: { q: 'Someone edited ConfigMap coredns and typed “forwrd” for “forward”. The CoreDNS pods restart. What do pods across the cluster see?',
          options: ['Only external names fail; cluster names still resolve from the kubernetes plugin', 'Nothing changes until the next node reboot', 'CoreDNS exits on the Corefile parse error (CrashLoopBackOff), so kube-dns has no ready endpoints and every lookup fails — but curl to a ClusterIP by IP still works'],
          answer: 2, why: 'CoreDNS parses the whole Corefile at start-up; an unknown directive is fatal (`/etc/coredns/Corefile:… - Error during parsing: Unknown directive \'forwrd\'`), so the pods crash-loop and the kube-dns Service loses its ready endpoints. Service routing is kube-proxy’s job and keeps working by IP. Read `kubectl -n kube-system logs -l k8s-app=kube-dns`, fix the ConfigMap, and the pods recover on their next restart.' } },
      { id: 'dns-egress', label: 'Default-deny egress', set: { selectorOk: true, targetPortOk: true, corefileOk: true, dnsEgress: false, fqdnOk: true },
        predict: { q: 'Namespace shop gets a default-deny egress NetworkPolicy that only allows egress to pods in shop. From pod web, what happens?',
          options: ['Everything still works — DNS traffic is exempt from NetworkPolicy', 'nslookup api times out (no servers could be reached), yet curl http://10.96.88.20 (api’s ClusterIP) still works — CoreDNS lives in kube-system and the policy has no rule for port 53', 'curl http://api works because the name is cached in the pod'],
          answer: 1, why: 'NetworkPolicy matches the pod IP after kube-proxy’s DNAT, so web → api (same namespace) is allowed even through the ClusterIP. The DNS query goes to kube-dns pods in kube-system, which the policy does not allow, so it is dropped silently: a timeout, not a refusal. Add an egress rule to namespace kube-system, pods k8s-app=kube-dns, on UDP and TCP 53. Pods do not cache DNS by default.' } },
      { id: 'fqdn', label: 'Short name across namespaces', set: { selectorOk: true, targetPortOk: true, corefileOk: true, dnsEgress: true, fqdnOk: false },
        predict: { q: 'web (ns shop) connects to DB_HOST=db, but Service db lives in namespace data. What does the lookup return?',
          options: ['NXDOMAIN — the search list only expands db to db.shop.svc.cluster.local, db.svc.cluster.local and db.cluster.local; use db.data (or db.data.svc.cluster.local)', 'db.data.svc.cluster.local — CoreDNS searches every namespace for a unique match', 'A timeout — CoreDNS refuses cross-namespace queries by default'],
          answer: 0, why: 'A pod’s /etc/resolv.conf lists search shop.svc.cluster.local svc.cluster.local cluster.local with ndots:5, so a short name only resolves inside its own namespace. Another namespace’s Service needs <service>.<namespace> at least. CoreDNS answers cross-namespace queries normally; NetworkPolicy, not DNS, is how namespaces are isolated.' } },
      { id: 'heal', label: 'Reset', set: { selectorOk: true, targetPortOk: true, corefileOk: true, dnsEgress: true, fqdnOk: true } }
    ],
    derive: function (s) {
      var d = serviceDnsDecide(s), rules = [];
      var apiOk = d.apiByIp === 'ok';
      rules.push(rule('^svc-api$', apiOk ? { tint: 'ok', glow: 0.45 } : { tint: 'deny', glow: 0.75, pulse: true }));
      rules.push(rule('^svc-api-selector$', s.selectorOk ? { tint: 'ok', glow: 0.3 } : { tint: 'deny', glow: 0.85, pulse: true }));
      rules.push(rule('^svc-api-port$', s.targetPortOk ? { tint: 'ok', glow: 0.25 } : { tint: 'deny', glow: 0.85, pulse: true }));
      rules.push(rule('^endpointslice-api$', !d.endpoints ? { tint: 'down', glow: 0.1, pulse: true } : (s.targetPortOk ? { tint: 'ok', glow: 0.3 } : { tint: 'warn', glow: 0.6, pulse: true })));
      rules.push(rule('^api-pod-[01]$', s.selectorOk ? { tint: 'ok', glow: 0.35 } : { tint: 'muted', glow: 0.1 }));
      rules.push(rule('^container-port-[01]$', s.targetPortOk ? { tint: 'ok', glow: 0.5 } : { tint: 'gold', glow: 0.7, pulse: true }));
      rules.push(rule('^edge-svc-pod-[01]$', apiOk ? { tint: 'ok', glow: 0.4 } : (d.endpoints ? { tint: 'warn', glow: 0.5, pulse: true } : { tint: 'down', glow: 0 })));
      rules.push(rule('^kube-proxy-rules$', d.endpoints ? { tint: 'ok', glow: 0.2 } : { tint: 'warn', glow: 0.6, pulse: true }));
      rules.push(rule('^edge-client-api$', d.apiByName === 'ok' ? { tint: 'ok', glow: 0.45 } : { tint: 'deny', glow: 0.6, pulse: true }));
      rules.push(rule('^(svc-kube-dns|coredns-[01])$', s.corefileOk ? { tint: 'ok', glow: 0.4 } : { tint: 'deny', glow: 0.8, pulse: true }));
      rules.push(rule('^sim-crash-ring-[01]$', s.corefileOk ? { hide: true } : { show: true, tint: 'warn', glow: 0.8, pulse: true }));
      rules.push(rule('^corefile$', s.corefileOk ? { tint: 'muted', glow: 0.15 } : { tint: 'deny', glow: 0.8, pulse: true }));
      rules.push(rule('^edge-client-dns$', d.dns ? { tint: 'ok', glow: 0.5 } : (s.dnsEgress ? { tint: 'deny', glow: 0.6, pulse: true } : { tint: 'down', glow: 0 })));
      rules.push(rule('^sim-netpol-wall$', s.dnsEgress ? { hide: true } : { show: true, tint: 'deny', glow: 0.6 }));
      rules.push(rule('^netpol-tablet$', s.dnsEgress ? { tint: 'muted', glow: 0.15 } : { tint: 'gold', glow: 0.7, pulse: true }));
      rules.push(rule('^resolv-conf$', s.fqdnOk ? { tint: 'muted', glow: 0.15 } : { tint: 'gold', glow: 0.7, pulse: true }));
      rules.push(rule('^sim-nxdomain-flag$', d.dbLookup === 'nxdomain' ? { show: true, tint: 'deny', glow: 0.7, pulse: true } : { hide: true }));
      rules.push(rule('^edge-client-db$', d.dbReach ? { tint: 'ok', glow: 0.45 } : { tint: 'deny', glow: 0.55, pulse: true }));
      rules.push(rule('^(svc-db|db-pod|edge-db-pod)$', { tint: 'ok', glow: 0.3 }));
      rules.push(rule('^ns-kube-system$', s.corefileOk ? { tint: 'muted', glow: 0.05 } : { tint: 'warn', glow: 0.25 }));
      rules.push(rule('^(ns-shop|ns-data)$', { tint: 'muted', glow: 0.05 }));
      var verdict = !d.dns ? 'down' : (!apiOk || !d.dbReach ? 'degraded' : 'healthy');
      rules.push(rule('^client-pod$', verdict === 'healthy' ? { tint: 'ok', glow: 0.4 } : { tint: verdict === 'down' ? 'deny' : 'warn', glow: 0.55, pulse: true }));
      var cap = [];
      cap.push('Service api ' + d.selector + ' → ' + (d.endpoints ? d.endpoints + ' endpoints on :' + d.endpointPort : 'EndpointSlice empty'));
      if (d.apiByIp === 'refused-no-endpoints') cap.push('ClusterIP has no endpoints → kube-proxy rejects (connection refused)');
      if (d.apiByIp === 'refused-target-port') cap.push('targetPort 80 but the container listens on 8080 → connection refused');
      if (!s.corefileOk) cap.push('CoreDNS CrashLoopBackOff (Corefile parse error) → lookups refused; ClusterIPs still work by IP');
      if (!s.dnsEgress) cap.push('ns shop default-deny egress has no rule to kube-dns:53 → lookups time out');
      if (d.dns && d.dbLookup === 'nxdomain') cap.push('DB_HOST=db → NXDOMAIN (search list stays in ns shop)');
      if (verdict === 'healthy') cap.push('web → api:80 → :8080 OK · DNS OK · web → db.data OK');
      return { verdict: verdict, metrics: d, caption: cap.join(' · '), rules: rules };
    }
  };

  /* ── CKS: Pod Security · securityContext/seccomp · default-deny · SA least privilege · audit — v1.7.0 (2026-10-29) ──
   * Scene contract (cks-pod-security.glb, authored 2026-10-29 — the first CKS asset): control-plane plate with
   * kube-apiserver, psa-gate (+ sim-psa-reject), audit-policy, audit-log (+ sim-audit-gap), edge-api-audit; ns-payments
   * with psa-label, payments-pod inside sec-context over seccomp-filter over node-kernel (+ sim-privileged-flare),
   * sa-token (+ sim-cluster-admin-crown), secret-db-creds, netpol-tablet, sim-netpol-wall; ns-frontend/frontend-pod,
   * ns-default/attacker-pod, edge-frontend-api, edge-attacker-api; rbac-binding, secrets-vault, edge-token-secrets,
   * edge-pod-apiserver. Rules follow the documented Pod Security Admission (built-in PodSecurity controller, enforce
   * applies to Pods; warn/audit also to workload templates; unlabelled namespaces default to privileged), PSS
   * restricted checks, kubelet seccomp defaults (Unconfined unless seccompDefault), NetworkPolicy isolation, RBAC
   * binding scope, and the API server audit log backend (off without --audit-log-path). */
  var CKS_VIOLATIONS = {
    privileged: 'privileged (container "api" must not set securityContext.privileged=true)',
    ape: 'allowPrivilegeEscalation != false (container "api" must set securityContext.allowPrivilegeEscalation=false)',
    caps: 'unrestricted capabilities (container "api" must set securityContext.capabilities.drop=["ALL"])',
    nonroot: 'runAsNonRoot != true (pod or container "api" must set securityContext.runAsNonRoot=true)',
    seccomp: 'seccompProfile (pod or container "api" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")'
  };
  /** PSS restricted checks the payments-api pod template fails, in the order the PodSecurity admission lists them. */
  function cksRestrictedViolations(s) {
    var v = [];
    if (!s.podHardened) v.push(CKS_VIOLATIONS.privileged, CKS_VIOLATIONS.ape, CKS_VIOLATIONS.caps, CKS_VIOLATIONS.nonroot);
    if (!s.seccomp) v.push(CKS_VIOLATIONS.seccomp);
    return v;
  }
  function cksDecide(s) {
    var violations = cksRestrictedViolations(s);
    var admitted = !s.psaEnforce || violations.length === 0;
    var privilegedRunning = admitted && !s.podHardened;
    /* allow-frontend also selects the payments-api pods, so on its own it isolates them too (policies are additive allow-lists). */
    var isolated = !!s.denyIngress || !!s.allowFrontend;
    var attackerReach = !isolated;
    var frontendReach = !isolated || !!s.allowFrontend;
    var saClusterAdmin = !s.rbacLeast;
    var exposures = [];
    if (privilegedRunning) exposures.push('privileged-pod');
    if (attackerReach) exposures.push('open-ingress');
    if (saClusterAdmin) exposures.push('cluster-admin-token');
    return {
      psaLevel: s.psaEnforce ? 'restricted' : 'privileged (default: no namespace labels)',
      violations: violations,
      admitted: admitted,
      podStatus: admitted ? 'Running' : 'FailedCreate',
      privilegedRunning: privilegedRunning,
      runAsUser: admitted ? (s.podHardened ? 10001 : 0) : null,
      seccompMode: admitted ? (s.seccomp ? 2 : 0) : null,
      ingressIsolated: isolated,
      attackerReach: attackerReach,
      frontendReach: frontendReach,
      /* policyTypes lists Ingress only, so egress (DNS included) is never isolated by this drill's policy. */
      egressOk: true,
      saClusterAdmin: saClusterAdmin,
      saCanReadAllSecrets: saClusterAdmin,
      auditEvents: !!s.auditOn,
      exposures: exposures
    };
  }

  var cksPodSecurity = {
    id: 'cks-pod-security',
    title: 'CKS workload security drill: Pod Security Admission, securityContext/seccomp, default-deny, least privilege, audit',
    cert: 'CKS',
    glb: '/assets/immersive/cks-pod-security.glb',
    initial: { psaEnforce: true, podHardened: true, seccomp: true, denyIngress: true, allowFrontend: true, rbacLeast: true, auditOn: true },
    toggles: [
      { id: 'psaEnforce', label: 'ns payments Pod Security', on: 'enforce=restricted', off: 'no labels (privileged)' },
      { id: 'podHardened', label: 'payments-api securityContext', on: 'non-root · no escalation · drop ALL', off: 'privileged: true (root)' },
      { id: 'seccomp', label: 'seccompProfile', on: 'RuntimeDefault', off: 'unset (Unconfined)' },
      { id: 'denyIngress', label: 'ns payments default-deny ingress', on: 'applied', off: 'none (allow-all)' },
      { id: 'allowFrontend', label: 'allow frontend → :8080', on: 'applied', off: 'missing' },
      { id: 'rbacLeast', label: 'ServiceAccount api-sa', on: 'Role in payments (least privilege)', off: 'ClusterRoleBinding → cluster-admin' },
      { id: 'auditOn', label: 'API audit log backend', on: '--audit-log-path set', off: 'missing (no backend)' }
    ],
    scenarios: [
      { id: 'psa-reject', label: 'restricted vs a privileged template', set: { psaEnforce: true, podHardened: false, seccomp: false, denyIngress: true, allowFrontend: true, rbacLeast: true, auditOn: true },
        predict: { q: 'Namespace payments is labelled pod-security.kubernetes.io/enforce=restricted. You run kubectl rollout restart deployment payments-api, whose pod template sets privileged: true and no other securityContext. What happens?',
          options: ['The Deployment update is accepted, but the ReplicaSet cannot create the new pods: FailedCreate … violates PodSecurity "restricted:latest". With 2 replicas and the default 25% maxUnavailable, the old pods keep running',
            'kubectl rollout restart is itself rejected with 403 Forbidden, because Pod Security checks Deployments in enforce mode',
            'The new pods are created, then the kubelet kills them with CreateContainerError'],
          answer: 0, why: 'Pod Security Admission enforce mode evaluates Pods only; warn and audit modes also evaluate workload templates. So the Deployment change is accepted, and the ReplicaSet controller gets the 403 when it creates each Pod. You see it in `kubectl get events` or `describe rs` as FailedCreate, with every failing check listed (privileged, allowPrivilegeEscalation, capabilities, runAsNonRoot, seccompProfile). With 2 replicas, maxUnavailable rounds down to 0, so the rollout stalls and the old pods keep serving.' } },
      { id: 'no-psa', label: 'No Pod Security labels', set: { psaEnforce: false, podHardened: false, seccomp: false, denyIngress: true, allowFrontend: true, rbacLeast: true, auditOn: true },
        predict: { q: 'Namespace payments has no pod-security.kubernetes.io labels, and the API server uses the default PodSecurity configuration. A teammate deploys payments-api with privileged: true. What does admission do?',
          options: ['It rejects the pod, because Kubernetes enforces the baseline level by default since PodSecurityPolicy was removed',
            'It admits the pod with a warning, because the default warn level is restricted',
            'It admits the pod silently. With no labels and no AdmissionConfiguration defaults, every mode defaults to privileged. The container gets all capabilities and host devices, which makes it about as powerful as root on the node'],
          answer: 2, why: 'The built-in PodSecurity admission controller defaults enforce, audit and warn to privileged:latest unless you label the namespace or set cluster-wide defaults in the AdmissionConfiguration. PodSecurityPolicy was removed in v1.25, and nothing restrictive replaced it by default. privileged: true turns off most container isolation, including device access and the capability bounding set. Label the namespace (enforce=restricted, or baseline at least) and harden the pod.' } },
      { id: 'seccomp', label: 'No seccompProfile', set: { psaEnforce: false, podHardened: true, seccomp: false, denyIngress: true, allowFrontend: true, rbacLeast: true, auditOn: true },
        predict: { q: 'payments-api now runs as non-root with allowPrivilegeEscalation: false and drop: [ALL], but it sets no seccompProfile. The kubelet runs with its defaults. What does grep Seccomp /proc/1/status print inside the container?',
          options: ['Seccomp: 2, because the container runtime always applies its default profile',
            'Seccomp: 0 (unconfined). The kubelet applies the runtime default profile only when seccompDefault is enabled. Set securityContext.seccompProfile.type: RuntimeDefault, which restricted also requires',
            'Seccomp: 1 (strict mode), because non-root containers get the strict read/write/exit filter'],
          answer: 1, why: 'Kubernetes runs containers Unconfined unless the pod or container sets seccompProfile, or the kubelet has seccompDefault: true. /proc/1/status shows Seccomp: 0 when unconfined and 2 when a filter is loaded. RuntimeDefault loads the container runtime’s profile, which blocks syscalls such as keyctl and add_key (the kernel keyring is not namespaced). PSS restricted rejects pods without RuntimeDefault or Localhost. Strict mode (1) is never used for containers.' } },
      { id: 'no-netpol', label: 'No NetworkPolicy', set: { psaEnforce: true, podHardened: true, seccomp: true, denyIngress: false, allowFrontend: false, rbacLeast: true, auditOn: true },
        predict: { q: 'Namespace payments has no NetworkPolicy. A compromised pod in namespace default runs curl http://payments-api.payments:8080. What happens?',
          options: ['It is refused, because pods accept traffic only from their own namespace by default',
            'It gets a 200. Until a NetworkPolicy selects a pod, the pod accepts traffic from anywhere. Start with a default-deny ingress policy, then allow only what is needed',
            'It times out, because the CNI blocks cross-namespace traffic unless the Service is exported'],
          answer: 1, why: 'Kubernetes networking is flat and allow-all by default. A pod is isolated for ingress only once some NetworkPolicy with Ingress in policyTypes selects it. The CKS pattern is a default-deny policy per namespace (podSelector {} plus policyTypes [Ingress]), followed by narrow allow rules. This needs a CNI that enforces NetworkPolicy, such as Calico or Cilium; flannel alone does not.' } },
      { id: 'deny-all-ingress', label: 'Default-deny, no allow rule', set: { psaEnforce: true, podHardened: true, seccomp: true, denyIngress: true, allowFrontend: false, rbacLeast: true, auditOn: true },
        predict: { q: 'You apply default-deny-ingress (podSelector: {}, policyTypes: [Ingress]) in payments and nothing else. What happens to frontend → payments-api, and to payments-api’s own DNS lookups?',
          options: ['frontend still works because Services bypass NetworkPolicy, but DNS breaks',
            'Both break, because a default-deny policy blocks ingress and egress',
            'frontend → payments-api times out because nothing allows it yet. payments-api’s DNS lookups keep working, because this policy lists only Ingress, so egress is not isolated. Add an allow rule from namespace frontend on 8080'],
          answer: 2, why: 'A policy that selects every pod and has no ingress rules drops all inbound traffic to payments, including legitimate traffic. NetworkPolicy is enforced on pod IPs after the Service DNAT, so a ClusterIP does not get around it. Egress isolation needs Egress in policyTypes, so DNS and outbound calls are untouched. Then allow namespaceSelector kubernetes.io/metadata.name=frontend on TCP 8080.' } },
      { id: 'rbac-admin', label: 'ServiceAccount is cluster-admin', set: { psaEnforce: true, podHardened: true, seccomp: true, denyIngress: true, allowFrontend: true, rbacLeast: false, auditOn: true },
        predict: { q: 'payments-api runs as ServiceAccount api-sa, and a ClusterRoleBinding (api-sa-admin) binds api-sa to cluster-admin. An attacker with RCE in the pod reads the projected token. What can they do?',
          options: ['Anything in any namespace: kubectl auth can-i get secrets -A --as system:serviceaccount:payments:api-sa says yes. Delete the ClusterRoleBinding, then bind a namespaced Role with only the verbs the app needs',
            'Only read objects in payments, because a ServiceAccount token is always scoped to its own namespace',
            'Nothing, because projected tokens are bound to the pod and a copied token is rejected outside it'],
          answer: 0, why: 'RBAC grants come from bindings, not from the namespace the ServiceAccount lives in. A ClusterRoleBinding to cluster-admin gives the token full rights over the whole cluster. Projected tokens are time-bound and audience-bound, and they become invalid when the pod is deleted. They are still bearer tokens, though: anyone who holds one can use it while the pod lives. Least privilege means a Role plus a RoleBinding in payments, and automountServiceAccountToken: false where the app never calls the API.' } },
      { id: 'audit-off', label: 'Audit policy without a backend', set: { psaEnforce: true, podHardened: true, seccomp: true, denyIngress: true, allowFrontend: true, rbacLeast: true, auditOn: false },
        predict: { q: 'kube-apiserver has --audit-policy-file=/etc/kubernetes/audit/policy.yaml, but --audit-log-path is commented out and there is no webhook backend. Someone reads Secret db-creds. What does the cluster record?',
          options: ['A RequestResponse event with the secret value, because the policy file alone turns on logging to stdout',
            'Nothing. The log backend is off when --audit-log-path is not set, so the policy has nowhere to write. Once the flag is set, a Metadata-level rule records who, what, when and from where, but never the secret’s data',
            'An event in etcd under /registry/events, which kubectl get events shows'],
          answer: 1, why: 'The audit log backend is turned on by --audit-log-path (a file path, or - for stdout), and the webhook backend by --audit-webhook-config-file. With neither, no events are written. Use the Metadata level for Secrets: the event carries user, verb, resource, name, sourceIPs and responseStatus, but no request or response body, which would contain the secret. Kubernetes Events are a different API and do not record reads. Remember to hostPath-mount the policy file and the log directory into the static pod.' } },
      { id: 'heal', label: 'Reset', set: { psaEnforce: true, podHardened: true, seccomp: true, denyIngress: true, allowFrontend: true, rbacLeast: true, auditOn: true } }
    ],
    derive: function (s) {
      var d = cksDecide(s), rules = [];
      rules.push(rule('^psa-label$', s.psaEnforce ? { tint: 'ok', glow: 0.35 } : { tint: 'gold', glow: 0.7, pulse: true }));
      rules.push(rule('^psa-gate$', !s.psaEnforce ? { tint: 'muted', glow: 0.1 } : (d.admitted ? { tint: 'ok', glow: 0.4 } : { tint: 'deny', glow: 0.8, pulse: true })));
      rules.push(rule('^sim-psa-reject$', d.admitted ? { hide: true } : { show: true, tint: 'deny', glow: 0.8, pulse: true }));
      rules.push(rule('^edge-pod-apiserver$', d.admitted ? { tint: 'ok', glow: 0.35 } : { tint: 'deny', glow: 0.6, pulse: true }));
      rules.push(rule('^payments-pod$', !d.admitted ? { tint: 'down', glow: 0 } : (d.privilegedRunning ? { tint: 'deny', glow: 0.7, pulse: true } : { tint: 'ok', glow: 0.45 })));
      rules.push(rule('^sec-context$', s.podHardened ? { tint: 'ok', glow: 0.5 } : { tint: 'deny', glow: 0.2 }));
      rules.push(rule('^sim-privileged-flare$', d.privilegedRunning ? { show: true, tint: 'deny', glow: 0.9, pulse: true } : { hide: true }));
      rules.push(rule('^seccomp-filter$', s.seccomp ? { tint: 'ok', glow: 0.55 } : { tint: 'warn', glow: 0.6, pulse: true }));
      rules.push(rule('^node-kernel$', d.privilegedRunning ? { tint: 'deny', glow: 0.5, pulse: true } : (s.seccomp ? { tint: 'muted', glow: 0.1 } : { tint: 'warn', glow: 0.3 })));
      rules.push(rule('^sim-netpol-wall$', s.denyIngress ? { show: true, tint: 'ok', glow: 0.35 } : { hide: true }));
      rules.push(rule('^netpol-tablet$', s.denyIngress && s.allowFrontend ? { tint: 'ok', glow: 0.3 } : { tint: 'gold', glow: 0.7, pulse: true }));
      rules.push(rule('^edge-attacker-api$', d.attackerReach ? { tint: 'deny', glow: 0.8, pulse: true } : { tint: 'down', glow: 0 }));
      rules.push(rule('^attacker-pod$', d.attackerReach ? { tint: 'deny', glow: 0.7, pulse: true } : { tint: 'muted', glow: 0.1 }));
      rules.push(rule('^edge-frontend-api$', d.frontendReach ? { tint: 'ok', glow: 0.45 } : { tint: 'warn', glow: 0.5, pulse: true }));
      rules.push(rule('^frontend-pod$', d.frontendReach ? { tint: 'ok', glow: 0.4 } : { tint: 'warn', glow: 0.5, pulse: true }));
      rules.push(rule('^sim-cluster-admin-crown$', d.saClusterAdmin ? { show: true, tint: 'deny', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^sa-token$', d.saClusterAdmin ? { tint: 'deny', glow: 0.7, pulse: true } : { tint: 'gold', glow: 0.35 }));
      rules.push(rule('^rbac-binding$', s.rbacLeast ? { tint: 'ok', glow: 0.3 } : { tint: 'deny', glow: 0.7, pulse: true }));
      rules.push(rule('^edge-token-secrets$', d.saClusterAdmin ? { tint: 'deny', glow: 0.8, pulse: true } : { tint: 'down', glow: 0 }));
      rules.push(rule('^secrets-vault$', d.saClusterAdmin ? { tint: 'deny', glow: 0.6, pulse: true } : { tint: 'gold', glow: 0.25 }));
      rules.push(rule('^secret-db-creds$', { tint: 'gold', glow: 0.3 }));
      rules.push(rule('^(audit-log|edge-api-audit)$', s.auditOn ? { tint: 'ok', glow: 0.4 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^sim-audit-gap$', s.auditOn ? { hide: true } : { show: true, tint: 'deny', glow: 0.7, pulse: true }));
      rules.push(rule('^audit-policy$', s.auditOn ? { tint: 'muted', glow: 0.15 } : { tint: 'gold', glow: 0.6, pulse: true }));
      rules.push(rule('^kube-apiserver$', { tint: 'gold', glow: 0.35 }));
      rules.push(rule('^(ns-payments|ns-frontend|ns-default|control-plane)$', { tint: 'muted', glow: 0.05 }));
      var verdict = d.exposures.length ? 'exposed' : (!d.admitted ? 'rejected' : (!d.frontendReach ? 'down' : (!s.auditOn || !s.seccomp ? 'degraded' : 'healthy')));
      var cap = [];
      cap.push('PSA ' + (s.psaEnforce ? 'enforce=restricted' : 'unlabelled → privileged') + ' · payments-api ' + (d.admitted ? 'Running' + (d.privilegedRunning ? ' PRIVILEGED (root, all capabilities)' : ' as uid ' + d.runAsUser) : 'FailedCreate (' + d.violations.length + ' restricted checks fail)'));
      if (d.admitted && !s.seccomp) cap.push('no seccompProfile → Unconfined (Seccomp: 0)');
      cap.push(d.attackerReach ? 'no default-deny → attacker in ns default reaches :8080' : (d.frontendReach ? 'default-deny + allow frontend:8080' : 'default-deny, no allow rule → frontend blocked too (egress untouched)'));
      if (d.saClusterAdmin) cap.push('api-sa → cluster-admin: a stolen token reads Secrets in every namespace');
      cap.push(s.auditOn ? 'audit: Metadata events to /var/log/kubernetes/audit/audit.log' : 'audit: no --audit-log-path → nothing recorded');
      return { verdict: verdict, metrics: d, caption: cap.join(' · '), rules: rules };
    }
  };

  /* ── CKS: Supply Chain Security (20% of the CKS) — v1.8.0 (2026-11-02) ─────────────────────────────────────────────
   * Scene contract (cks-supply-chain.glb, authored 2026-11-02 — the second CKS asset): CI lane ci-pipeline / ci-build →
   * trivy-scanner (+ sim-cve-flare, sim-ci-block) → sbom-doc → cosign-key → signature-seal, edge-build-scan,
   * edge-scan-sign, edge-push; registry-trusted with image-artifact, digest-pin (+ sim-tag-drift, sim-unsigned-mark);
   * registry-untrusted / untrusted-image; control-plane with kube-apiserver → vap-gate (+ sim-vap-deny) → sig-webhook
   * (+ sim-sig-deny); ns-payments / payments-pod (+ sim-vuln-halo); edge-registry-api, edge-untrusted-api, edge-api-pod.
   * Rules follow documented behaviour: Kubernetes has no built-in registry allow-list (a ValidatingAdmissionPolicy or a
   * webhook adds one); a VAP that matches Deployments rejects the apply itself; `trivy image --exit-code 1 --severity
   * CRITICAL` fails the CI job so nothing is pushed or signed; a cosign signature proves who signed a digest, not that it
   * is safe; a registry allow-list checks the name, not provenance; signature verification at admission denies a digest
   * with no matching signature; tags are mutable, digests are not. */
  var SC_DIGEST = { good: 'sha256:4f1c9b7e2a6d8c03e5b1f7a9d2c4e6f8a0b3c5d7e9f1a2b4c6d8e0f2a4b6e9a2', prev: 'sha256:2b8e4d6f0a1c3e5b7d9f2a4c6e8b0d1f3a5c7e9b2d4f6a8c0e1b3d5f7a9c0d44',
    vuln: 'sha256:c3a1e5f7b9d2c4e6a8f0b2d4c6e8a0f1b3d5e7c9a2b4d6f8e0c1a3b5d7f9e1b0', laptop: 'sha256:e6f8a0b2c4d6e8f0a1b3c5d7e9f2a4b6c8d0e1f3a5b7c9d2e4f6a8b0c1d3e5f1' };
  function scDigest(s) { return !s.scanClean ? SC_DIGEST.vuln : (!s.signed ? SC_DIGEST.laptop : SC_DIGEST.good); }
  function cksSupplyDecide(s) {
    var ciBlocked = !!s.scanGate && !s.scanClean;
    var sigValid = !!s.signed && !!s.fromTrusted; /* a docker.io image is never signed by our CI key */
    var registryOk = !s.vapRegistry || !!s.fromTrusted;
    var sigOk = !s.verifySig || sigValid;
    var release = ciBlocked ? 'blocked-in-ci' : (!registryOk ? 'denied-registry' : (!sigOk ? 'denied-signature' : 'admitted'));
    var admitted = release === 'admitted';
    var exposures = [];
    if (admitted && !s.fromTrusted) exposures.push('untrusted-registry');
    if (admitted && s.fromTrusted && !s.signed) exposures.push('unsigned-image');
    if (admitted && !s.scanClean) exposures.push('critical-cve');
    var gaps = [];
    if (!s.vapRegistry) gaps.push('no registry allow-list');
    if (!s.verifySig) gaps.push('no signature verification');
    if (!s.scanGate) gaps.push('no scan gate in CI');
    if (!s.pinnedDigest) gaps.push('mutable tag');
    return {
      release: release,
      admitted: admitted,
      ciBlocked: ciBlocked,
      pushed: !ciBlocked,
      registryOk: registryOk,
      sigValid: sigValid,
      sigOk: sigOk,
      criticalCves: s.scanClean ? 0 : 1,
      image: s.fromTrusted ? 'registry.example.com/payments/api' + (s.pinnedDigest ? '@' + scDigest(s) : ':2.4.1') : 'docker.io/payments-tools/api:latest',
      /* when the new release is refused, the previous (clean, signed) ReplicaSet keeps serving */
      runningDigest: admitted ? (s.fromTrusted ? scDigest(s) : 'sha256:(unknown publisher)') : SC_DIGEST.prev,
      digest: scDigest(s),
      driftRisk: !s.pinnedDigest,
      gaps: gaps,
      exposures: exposures
    };
  }

  var cksSupplyChain = {
    id: 'cks-supply-chain',
    title: 'CKS supply chain drill: allowed registries (ValidatingAdmissionPolicy), Trivy scan gate, SBOM, cosign signing + admission verification, digest pinning',
    cert: 'CKS',
    glb: '/assets/immersive/cks-supply-chain.glb',
    initial: { vapRegistry: true, fromTrusted: true, pinnedDigest: true, scanGate: true, scanClean: true, signed: true, verifySig: true },
    toggles: [
      { id: 'vapRegistry', label: 'ValidatingAdmissionPolicy allowed-registries', on: 'bound (Deny)', off: 'none' },
      { id: 'fromTrusted', label: 'payments-api image source', on: 'registry.example.com', off: 'docker.io (public)' },
      { id: 'pinnedDigest', label: 'image reference', on: '@sha256 digest', off: ':2.4.1 tag (mutable)' },
      { id: 'scanGate', label: 'CI Trivy gate', on: '--severity CRITICAL --exit-code 1', off: 'report only' },
      { id: 'scanClean', label: 'new build base image', on: 'patched / minimal (0 CRITICAL)', off: 'debian base · 1 CRITICAL CVE (zlib1g)' },
      { id: 'signed', label: 'cosign signature', on: 'signed by CI key', off: 'unsigned (pushed outside CI)' },
      { id: 'verifySig', label: 'admission signature check', on: 'verify against cosign.pub', off: 'none' }
    ],
    scenarios: [
      { id: 'untrusted-registry', label: 'No registry allow-list', set: { vapRegistry: false, fromTrusted: false, pinnedDigest: true, scanGate: true, scanClean: true, signed: true, verifySig: false },
        predict: { q: 'The cluster has no admission policy about images. A teammate changes payments-api to image docker.io/payments-tools/api:latest, from a publisher nobody has vetted, and applies it. What happens?',
          options: ['The API server rejects it, because kubeadm clusters only pull from registry.k8s.io unless you add an allow-list',
            'The kubelet refuses to pull it, because images without a signature are blocked by containerd by default',
            'It is admitted and runs. Kubernetes has no built-in registry allow-list: you add one with a ValidatingAdmissionPolicy (or a policy webhook) that checks every container image'],
          answer: 2, why: 'Nothing in core Kubernetes restricts where images come from. The API server only validates the object schema, and containerd pulls whatever the kubelet asks for (registry.k8s.io is only where kubeadm gets the control-plane images). The CKS answer is admission control: a ValidatingAdmissionPolicy with a CEL rule such as object.spec.containers.all(c, c.image.startsWith(\'registry.example.com/\')), plus a binding with validationActions [Deny]. Keep the trailing slash, or registry.example.com.evil.io/… would also pass. The old ImagePolicyWebhook admission plugin is another route.' } },
      { id: 'vap-deny', label: 'Allow-list on, public image', set: { vapRegistry: true, fromTrusted: false, pinnedDigest: true, scanGate: true, scanClean: true, signed: true, verifySig: false },
        predict: { q: 'ValidatingAdmissionPolicy allowed-registries matches apps/v1 Deployments and v1 Pods, and its binding in namespace payments has validationActions: [Deny]. You kubectl apply the Deployment with image docker.io/payments-tools/api:latest. What happens?',
          options: ['The apply itself fails: the Deployment is denied with "ValidatingAdmissionPolicy \'allowed-registries\' with binding \'allowed-registries-binding\' denied request …". The running pods are untouched',
            'The Deployment is accepted and its ReplicaSet reports FailedCreate, because admission policies only ever evaluate Pods',
            'It is accepted with a warning, because a VAP only warns until the cluster has been restarted with --enable-admission-plugins'],
          answer: 0, why: 'A VAP evaluates whatever its matchConstraints list. Because this one matches Deployments, the update is refused before it is stored, so the old ReplicaSet keeps serving. (Pod Security Admission is the one that checks only Pods in enforce mode.) ValidatingAdmissionPolicy is GA since Kubernetes 1.30 and needs no flag. validationActions can also be [Warn] or [Audit], which let the object through with a warning or an audit annotation, which is handy for a dry run before you deny.' } },
      { id: 'tag-drift', label: 'Mutable tag', set: { vapRegistry: true, fromTrusted: true, pinnedDigest: false, scanGate: true, scanClean: true, signed: true, verifySig: true },
        predict: { q: 'Everything is green: CI scanned and signed digest sha256:4f1c…e9a2, admission verifies signatures, and the Deployment references registry.example.com/payments/api:2.4.1 by tag. Is the code that runs guaranteed to be the code that was scanned?',
          options: ['Yes. A signature check at admission pins the tag forever',
            'No. Tags are mutable: anyone with push rights can point :2.4.1 at a new digest, and nodes can run different digests (IfNotPresent keeps a cached copy, new nodes pull the new one). Reference the image by @sha256 digest, which never changes',
            'Yes. Kubernetes rewrites tags to digests in the stored pod spec'],
          answer: 1, why: 'A tag is a movable pointer, and a digest is the content hash. The kubelet pulls by whatever string is in the pod spec, so a re-pushed tag can change what runs on the next pull, and replicas on different nodes can disagree (status.containerStatuses[].imageID shows what each one really runs). Signature-verification webhooks check the digest a tag resolves to at admission time; some also rewrite the spec to that digest (Kyverno verifyImages mutateDigest). The simplest fix is image: registry.example.com/payments/api@sha256:…, which is also what you signed.' } },
      { id: 'critical-cve', label: 'Signed, but vulnerable', set: { vapRegistry: true, fromTrusted: true, pinnedDigest: true, scanGate: false, scanClean: false, signed: true, verifySig: true },
        predict: { q: 'CI signs every image it builds with cosign, and admission verifies those signatures. The new build sits on a full debian:bookworm base whose zlib1g carries a CRITICAL CVE (CVE-2023-45853), and the Trivy step only prints a report (no --exit-code). Does signature verification stop the rollout?',
          options: ['No. The image is signed by the right key, so it is admitted and runs. A signature proves who built a digest and that it was not changed, not that it is safe. Gate on the scan: trivy image --severity CRITICAL --exit-code 1 before signing',
            'Yes. cosign refuses to sign an image with CRITICAL CVEs',
            'Yes. The admission webhook re-scans every image and denies CRITICAL findings'],
          answer: 0, why: 'Signing and scanning answer different questions. cosign signs whatever digest it is given, and the verifier only checks that the signature matches a trusted key (or keyless identity). Trivy exits 0 by default even when it finds CVEs; --exit-code 1 with --severity CRITICAL (optionally --ignore-unfixed) makes the pipeline fail. Put the gate before the push and the sign step, so a vulnerable build never gets a signature. Then rebuild on a minimal base (distroless, alpine): fewer packages means fewer CVEs. Watch --ignore-unfixed: CVE-2023-45853 is will_not_fix in Debian, so that flag would hide it and let the gate pass.' } },
      { id: 'scan-gate', label: 'Scan gate blocks the release', set: { vapRegistry: true, fromTrusted: true, pinnedDigest: true, scanGate: true, scanClean: false, signed: true, verifySig: true },
        predict: { q: 'Now the CI job runs trivy image --severity CRITICAL --exit-code 1 before push and sign, and the new build still carries that CRITICAL zlib1g CVE. What happens in production?',
          options: ['Production gets the new image, because the scan only runs after the rollout',
            'Nothing changes in production. Trivy exits 1, the job stops before push and sign, and payments-api keeps running the previous signed digest. Fix the image (a minimal base such as distroless static has no zlib1g at all) and rebuild',
            'Production pods are evicted, because Trivy marks the image as vulnerable in the registry'],
          answer: 1, why: 'A failing step stops the pipeline, so there is no new tag, no signature and no Deployment change. The cluster never sees the vulnerable build, and the running ReplicaSet keeps serving the last good digest. That is the point of shifting left. It is still worth scanning the running images too (trivy image on what is deployed, or trivy k8s), because new CVEs are published for images you already shipped.' } },
      { id: 'unsigned-push', label: 'Pushed outside CI', set: { vapRegistry: true, fromTrusted: true, pinnedDigest: true, scanGate: true, scanClean: true, signed: false, verifySig: false },
        predict: { q: 'Someone with registry credentials builds on a laptop and pushes straight to registry.example.com/payments/api, skipping CI, so the image has no cosign signature. The allowed-registries VAP is bound, and there is no signature check. Is the image admitted?',
          options: ['No. The registry allow-list also checks that the image was built by CI',
            'No. containerd verifies cosign signatures for private registries',
            'Yes. The allow-list matches the name registry.example.com/, which this image has. It says nothing about who built it. Add signature verification at admission (cosign.pub), so an unsigned digest is denied'],
          answer: 2, why: 'A registry allow-list is a string check on the image reference, so anyone who can push to the trusted registry can get code into the cluster. Provenance needs signatures: CI signs the digest with cosign (a key pair or keyless Sigstore), and an admission verifier (Sigstore policy-controller, Kyverno verifyImages, or Connaisseur) denies digests without a matching signature. Locally, cosign verify --key cosign.pub IMAGE shows the same answer.' } },
      { id: 'sig-verify', label: 'Signature check on, unsigned image', set: { vapRegistry: true, fromTrusted: true, pinnedDigest: true, scanGate: true, scanClean: true, signed: false, verifySig: true },
        predict: { q: 'Signature verification is now on in admission, using cosign.pub. The laptop-built, unsigned digest is applied again. What do cosign verify --key cosign.pub and the cluster say?',
          options: ['cosign prints "Error: no matching signatures" and exits 1. Admission denies the pod, and the previous signed ReplicaSet keeps serving. Re-run the image through CI so it is scanned, signed and pushed by digest',
            'cosign verifies it, because the registry is trusted, and the pod runs',
            'cosign warns, and admission lets the pod run with a "signature missing" annotation'],
          answer: 0, why: 'cosign looks up the signature artifact stored next to the digest in the registry (the sha256-….sig tag) and checks it against the public key. No artifact means no matching signatures and exit code 1. Admission verifiers apply the same rule. Webhooks that match Pods make the ReplicaSet report FailedCreate while the old pods keep running. The cure is process, not a bypass: build through the pipeline, which scans, generates the SBOM, signs and pushes.' } },
      { id: 'heal', label: 'Reset', set: { vapRegistry: true, fromTrusted: true, pinnedDigest: true, scanGate: true, scanClean: true, signed: true, verifySig: true } }
    ],
    derive: function (s) {
      var d = cksSupplyDecide(s), rules = [];
      rules.push(rule('^ci-build$', { tint: 'muted', glow: 0.15 }));
      rules.push(rule('^trivy-scanner$', !s.scanGate ? { tint: 'warn', glow: 0.4 } : (d.ciBlocked ? { tint: 'deny', glow: 0.8, pulse: true } : { tint: 'ok', glow: 0.5 })));
      rules.push(rule('^sim-cve-flare$', s.scanClean ? { hide: true } : { show: true, tint: 'deny', glow: 0.9, pulse: true }));
      rules.push(rule('^sim-ci-block$', d.ciBlocked ? { show: true, tint: 'deny', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^(edge-scan-sign|edge-push)$', d.ciBlocked ? { tint: 'down', glow: 0 } : { tint: 'ok', glow: 0.4 }));
      rules.push(rule('^edge-build-scan$', { tint: 'ok', glow: 0.35 }));
      rules.push(rule('^sbom-doc$', d.ciBlocked ? { tint: 'muted', glow: 0.1 } : { tint: 'ok', glow: 0.3 }));
      rules.push(rule('^cosign-key$', { tint: 'gold', glow: 0.35 }));
      rules.push(rule('^signature-seal$', s.signed && !d.ciBlocked ? { tint: 'gold', glow: 0.6 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^sim-unsigned-mark$', s.fromTrusted && !s.signed ? { show: true, tint: 'deny', glow: 0.7, pulse: true } : { hide: true }));
      rules.push(rule('^image-artifact$', !s.fromTrusted ? { tint: 'muted', glow: 0.1 } : (!s.scanClean && !d.ciBlocked ? { tint: 'deny', glow: 0.6, pulse: true } : { tint: 'ok', glow: 0.45 })));
      rules.push(rule('^digest-pin$', s.pinnedDigest ? { tint: 'ok', glow: 0.4 } : { tint: 'muted', glow: 0.1 }));
      rules.push(rule('^sim-tag-drift$', s.pinnedDigest || !s.fromTrusted ? { hide: true } : { show: true, tint: 'warn', glow: 0.7, pulse: true }));
      rules.push(rule('^untrusted-image$', !s.fromTrusted ? (d.admitted ? { tint: 'deny', glow: 0.8, pulse: true } : { tint: 'deny', glow: 0.4 }) : { tint: 'muted', glow: 0.05 }));
      rules.push(rule('^edge-untrusted-api$', !s.fromTrusted ? (d.admitted ? { tint: 'deny', glow: 0.8, pulse: true } : { tint: 'warn', glow: 0.4 }) : { tint: 'down', glow: 0 }));
      rules.push(rule('^edge-registry-api$', s.fromTrusted && !d.ciBlocked ? { tint: 'ok', glow: 0.4 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^vap-gate$', !s.vapRegistry ? { tint: 'muted', glow: 0.1 } : (d.release === 'denied-registry' ? { tint: 'deny', glow: 0.8, pulse: true } : { tint: 'ok', glow: 0.45 })));
      rules.push(rule('^sim-vap-deny$', d.release === 'denied-registry' ? { show: true, tint: 'deny', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^sig-webhook$', !s.verifySig ? { tint: 'muted', glow: 0.1 } : (d.release === 'denied-signature' ? { tint: 'deny', glow: 0.8, pulse: true } : { tint: 'ok', glow: 0.45 })));
      rules.push(rule('^sim-sig-deny$', d.release === 'denied-signature' ? { show: true, tint: 'deny', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^edge-api-pod$', d.admitted ? (d.exposures.length ? { tint: 'deny', glow: 0.6, pulse: true } : { tint: 'ok', glow: 0.4 }) : { tint: 'warn', glow: 0.3 }));
      rules.push(rule('^payments-pod$', d.exposures.length ? { tint: 'deny', glow: 0.7, pulse: true } : (d.admitted && d.driftRisk ? { tint: 'warn', glow: 0.5 } : { tint: 'ok', glow: 0.45 })));
      rules.push(rule('^sim-vuln-halo$', d.exposures.length ? { show: true, tint: 'deny', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^kube-apiserver$', { tint: 'gold', glow: 0.35 }));
      rules.push(rule('^(ci-pipeline|registry-trusted|registry-untrusted|control-plane|ns-payments)$', { tint: 'muted', glow: 0.05 }));
      var verdict = d.exposures.length ? 'exposed' : (!d.admitted ? 'rejected' : (d.gaps.length ? 'degraded' : 'healthy'));
      var cap = [];
      if (!s.fromTrusted) cap.push('not built by our CI (public image, unscanned, unsigned)');
      else cap.push(d.ciBlocked ? 'CI: trivy found ' + d.criticalCves + ' CRITICAL → exit 1, nothing pushed or signed' : ('CI: ' + (s.scanGate ? 'scan gate passed' : 'scan report only (' + d.criticalCves + ' CRITICAL)') + ' · ' + (s.signed ? 'cosign-signed' : 'unsigned (pushed outside CI)')));
      cap.push('image ' + d.image);
      cap.push(d.release === 'admitted' ? 'admitted' : (d.release === 'denied-registry' ? 'VAP allowed-registries denied the Deployment' : (d.release === 'denied-signature' ? 'signature check: no matching signatures → denied' : 'release blocked in CI')));
      if (!d.admitted) cap.push('previous signed ReplicaSet keeps serving');
      if (d.exposures.length) cap.push('running: ' + d.exposures.join(' + '));
      else if (d.admitted && d.gaps.length) cap.push('gaps: ' + d.gaps.join(' · '));
      return { verdict: verdict, metrics: d, caption: cap.join(' · '), rules: rules };
    }
  };

  /* ── CKS: Monitoring, Logging & Runtime Security (+ AppArmor) — v1.9.0 (2026-11-03) ─────────────────────────────────
   * Scene contract (cks-runtime-security.glb, authored 2026-11-03 — the third CKS asset): node01 / node-kernel /
   * syscall-stream → edge-kernel-falco → falco-ds (+ sim-falco-alert, sim-falco-blind) with falco-rules and edge-falco-out →
   * falco-alerts; apparmor-profile (+ sim-apparmor-missing); kube-apiserver → edge-api-audit → audit-log (+ sim-exec-recorded);
   * ns-payments / rootfs-layer / payments-pod / apparmor-shield; sim-attacker-shell, edge-shell-pod, sim-rootfs-write,
   * sim-write-denied, edge-pod-kernel, edge-exec-api.
   * Rules follow documented behaviour: Falco reads syscalls through its kernel probe and emits alerts for matching
   * enabled rules — it detects, it does not block; rules files load in order (falco_rules.yaml, then
   * falco_rules.local.yaml) and a later `enabled: false` override switches a rule off; the kubelet does not load AppArmor
   * profiles, so a Localhost profile missing on the node stops the container (CreateContainerError); an AppArmor deny
   * rule returns EACCES (Permission denied); readOnlyRootFilesystem returns EROFS (Read-only file system); the API audit
   * log records the pods/exec request (who, which pod, when) but never the commands typed inside the stream, and a shell
   * obtained through an application exploit makes no API request at all. */
  function cksRuntimeDecide(s) {
    /* A Localhost profile that is not loaded stops the NEW pods (CreateContainerError); a Deployment rollout stalls and
     * the old ReplicaSet (without the profile) keeps serving, so AppArmor only protects once the profile is loaded. */
    var rolloutStuck = !!s.apparmor && !s.profileLoaded;
    var aaActive = !!s.apparmor && !!s.profileLoaded;
    var shell = !!s.intrusion;
    var detected = shell && !!s.falco && !!s.shellRule;
    var writeBlock = !shell ? null : (s.readOnlyRoot ? 'read-only' : (aaActive ? 'apparmor' : null));
    var dropped = shell && !writeBlock;
    var auditSeen = shell && !!s.viaExec;
    var exposures = [];
    if (dropped) exposures.push('binary-dropped');
    if (shell && !detected) exposures.push('no-runtime-visibility');
    var gaps = [];
    if (!s.falco) gaps.push('no runtime detection');
    else if (!s.shellRule) gaps.push('shell rule disabled');
    if (rolloutStuck) gaps.push('AppArmor profile not loaded on node01 (rollout stuck)');
    else if (!s.apparmor) gaps.push('no AppArmor profile');
    if (!s.readOnlyRoot) gaps.push('writable root filesystem');
    return {
      newPods: rolloutStuck ? 'CreateContainerError' : 'Running',
      rolloutStuck: rolloutStuck,
      aaActive: aaActive,
      shell: shell,
      detected: detected,
      alerts: detected ? 1 : 0,
      writeBlock: writeBlock,
      writeError: writeBlock === 'read-only' ? 'Read-only file system' : (writeBlock === 'apparmor' ? 'Permission denied' : null),
      dropped: dropped,
      auditSeen: auditSeen,
      gaps: gaps,
      exposures: exposures
    };
  }

  var cksRuntimeSecurity = {
    id: 'cks-runtime-security',
    title: 'CKS runtime security drill: Falco detection, rule overrides, AppArmor profiles, immutable containers, audit vs runtime visibility',
    cert: 'CKS',
    glb: '/assets/immersive/cks-runtime-security.glb',
    initial: { falco: true, shellRule: true, apparmor: true, profileLoaded: true, readOnlyRoot: true, intrusion: false, viaExec: false },
    toggles: [
      { id: 'falco', label: 'Falco DaemonSet on node01', on: 'running', off: 'not installed' },
      { id: 'shellRule', label: 'rule "Shell in container"', on: 'enabled', off: 'enabled: false (local override)' },
      { id: 'apparmor', label: 'payments-api appArmorProfile', on: 'Localhost k8s-deny-write', off: 'none (Unconfined)' },
      { id: 'profileLoaded', label: 'k8s-deny-write on node01', on: 'loaded (enforce)', off: 'not loaded' },
      { id: 'readOnlyRoot', label: 'readOnlyRootFilesystem', on: 'true', off: 'false' },
      { id: 'intrusion', label: 'attacker shell in payments-api', on: 'active', off: 'none' },
      { id: 'viaExec', label: 'how the shell started', on: 'kubectl exec (stolen kubeconfig)', off: 'app exploit (RCE)' }
    ],
    scenarios: [
      { id: 'rce-blind', label: 'Shell via app exploit', set: { falco: false, shellRule: true, apparmor: false, profileLoaded: true, readOnlyRoot: false, intrusion: true, viaExec: false },
        predict: { q: 'An attacker exploits a bug in payments-api, gets the app to run sh, and drops a binary into /usr/local/bin. API audit logging is on (pods/exec logged at RequestResponse). There is no Falco and no AppArmor profile. Which record shows the intrusion?',
          options: ['The audit log: every process started in a pod is an API request',
            'The kubelet events: kubectl get events shows "process sh started"',
            'Nothing. The shell came from inside the app process, so no API request was made, and nothing watches syscalls. Only kernel-level runtime detection (Falco, Tetragon, Tracee) sees an execve of sh in that container'],
          answer: 2, why: 'The audit log only records requests to the kube-apiserver. A remote code execution in the application forks sh inside the container through the kernel (execve), and the API server never hears of it. Events are about object lifecycle, not processes. That is the gap runtime security fills: Falco reads the syscall stream through its kernel probe (modern eBPF by default) and matches it against rules such as "a shell spawned in a container" or "a write below a binary directory".' } },
      { id: 'falco-alert', label: 'Falco on, no prevention', set: { falco: true, shellRule: true, apparmor: false, profileLoaded: true, readOnlyRoot: false, intrusion: true, viaExec: true },
        predict: { q: 'Falco runs as a DaemonSet with a rule that fires when a shell spawns in a container. Someone runs kubectl exec -it into payments-api, starts sh and copies a binary into /usr/local/bin. The pod has no AppArmor profile and a writable root filesystem. What happens?',
          options: ['Falco prints a Warning alert naming the namespace, pod and command line, and the write still succeeds. Falco detects; it does not block. Prevention comes from AppArmor / seccomp / readOnlyRootFilesystem',
            'Falco kills the shell, because a Warning-priority rule terminates the process',
            'The write fails, because Falco makes the container filesystem read-only once a rule fires'],
          answer: 0, why: 'Falco is a detection engine: a matching rule produces an alert (stdout by default, read with kubectl logs -n falco, or forwarded by Falcosidekick). It does not kill processes or change the pod. Responding is your job: capture evidence, then replace the pod. Preventing the write needs a control that runs in the kernel at the time of the call: an AppArmor deny rule, a read-only root filesystem, or dropping privileges.' } },
      { id: 'rule-disabled', label: 'Running, but blind', set: { falco: true, shellRule: false, apparmor: true, profileLoaded: true, readOnlyRoot: true, intrusion: true, viaExec: true },
        predict: { q: 'The falco pod on node01 is Running 1/1 and its logs show no errors, yet a shell in payments-api produced no alert. falco_rules.local.yaml contains "- rule: Shell in container" followed by "enabled: false". Why is there no alert?',
          options: ['Falco only alerts on Critical priority by default',
            'The rule is switched off. Falco loads falco_rules.yaml first and falco_rules.local.yaml after it, and the later file overrides the rule. A Running Falco pod with the rule disabled detects nothing for that behaviour',
            'Falco needs a restart after every exec to see new processes'],
          answer: 1, why: 'Rules files load in the order listed in falco.yaml (rules_files), and a later definition of a rule with only enabled: false switches it off. Set it back to true (or delete the override); with watch_config_files on (the default) Falco reloads the rules itself. The default min priority (priority: debug in falco.yaml) lets every priority through, so Warning alerts are printed. Always test a rule: trigger it once and read the alert.' } },
      { id: 'apparmor-not-loaded', label: 'Profile not on the node', set: { falco: true, shellRule: true, apparmor: true, profileLoaded: false, readOnlyRoot: true, intrusion: false, viaExec: false },
        predict: { q: 'You update the payments-api Deployment with securityContext.appArmorProfile {type: Localhost, localhostProfile: k8s-deny-write}. The profile file sits in /etc/apparmor.d/ on node01 but was never loaded with apparmor_parser. What happens?',
          options: ['The new pods run Unconfined and the kubelet logs a warning',
            'The kubelet loads the profile from /etc/apparmor.d/ automatically',
            'The new pods do not start: CreateContainerError with "apparmor profile not found k8s-deny-write". The rollout stalls and the old pods, which have no profile, keep serving. Load the profile on every node that can run the pod (apparmor_parser, or a DaemonSet that loads profiles), then the kubelet retries'],
          answer: 2, why: 'Kubernetes does not load AppArmor profiles; it only asks the container runtime to apply one that is already loaded in the node kernel. A Localhost profile that is not loaded fails the container create, which is safer than silently running Unconfined. With a Deployment the rolling update stops at the first failing pod, so nothing is protected yet: the old ReplicaSet keeps running without the profile. Check with aa-status (or cat /sys/kernel/security/apparmor/profiles), load with apparmor_parser -q /etc/apparmor.d/k8s-deny-write, and use node affinity or a loader DaemonSet so every node has it. Since Kubernetes 1.30 the field is securityContext.appArmorProfile; the old container.apparmor.security.beta.kubernetes.io annotation is deprecated.' } },
      { id: 'apparmor-deny-write', label: 'AppArmor denies the write', set: { falco: true, shellRule: true, apparmor: true, profileLoaded: true, readOnlyRoot: false, intrusion: true, viaExec: true },
        predict: { q: 'k8s-deny-write (it contains "deny /** w,") is loaded and enforced on payments-api, but readOnlyRootFilesystem is false. Inside a shell in the pod, the attacker runs touch /usr/local/bin/miner. What is the result?',
          options: ['The file is created, because AppArmor only restricts network access',
            'touch: /usr/local/bin/miner: Permission denied. The AppArmor deny rule returns EACCES, the kernel logs an apparmor="DENIED" record on the node, and Falco still alerts on the shell itself',
            'The pod is evicted for violating its profile'],
          answer: 1, why: 'AppArmor is mandatory access control in the kernel: the deny rule matches the path and the write permission, so the syscall fails with EACCES (Permission denied) no matter which user runs it. The denial is logged on the node (journalctl -k or /var/log/kern.log, apparmor="DENIED" operation=… profile="k8s-deny-write"). The process keeps running, and the pod is not evicted. Detection (Falco) and prevention (AppArmor) are layers, not alternatives.' } },
      { id: 'readonly-root', label: 'Immutable container', set: { falco: true, shellRule: true, apparmor: false, profileLoaded: true, readOnlyRoot: true, intrusion: true, viaExec: true },
        predict: { q: 'payments-api now runs with readOnlyRootFilesystem: true and no AppArmor profile. A shell in the pod tries touch /usr/local/bin/miner. What does it get, and what must you add if the app itself needs scratch space in /tmp?',
          options: ['touch: /usr/local/bin/miner: Read-only file system (EROFS). /tmp is read-only too, so mount an emptyDir volume at /tmp for the app',
            'Permission denied, and /tmp stays writable because it is always a tmpfs',
            'The write succeeds for root, because readOnlyRootFilesystem only applies to non-root users'],
          answer: 0, why: 'readOnlyRootFilesystem mounts the container image layer read-only, so any write to it fails with EROFS whatever the user. That covers /tmp as well unless you mount a writable volume there (an emptyDir, optionally medium: Memory). This "immutable container" pattern is a CKS staple: an attacker cannot drop tools or change binaries, and the change is one field in securityContext.' } },
      { id: 'audit-exec', label: 'Audit vs runtime', set: { falco: false, shellRule: true, apparmor: true, profileLoaded: true, readOnlyRoot: true, intrusion: true, viaExec: true },
        predict: { q: 'There is no Falco. An attacker with a stolen kubeconfig runs kubectl exec -it payments-api -- sh and types several commands. The audit policy logs pods/exec at Metadata level. What does the audit log contain?',
          options: ['Every command typed, because exec traffic passes through the API server',
            'Nothing, because exec is a kubelet feature and never reaches the API server',
            'One event for the create on the pods/exec subresource (user, source IP, pod, timestamp, the requested command sh), but not the commands typed inside the stream. What happened inside needs runtime detection'],
          answer: 2, why: 'kubectl exec is a request to the API server (POST …/pods/payments-api-…/exec), which then proxies a stream to the kubelet. The audit log records that request at the levels your policy sets, so you learn who opened a shell and when. The bytes in the stream are not audited at any level, so the commands typed inside are invisible to it. Pair audit logs (API layer) with runtime detection (syscall layer).' } },
      { id: 'heal', label: 'Reset', set: { falco: true, shellRule: true, apparmor: true, profileLoaded: true, readOnlyRoot: true, intrusion: false, viaExec: false } }
    ],
    derive: function (s) {
      var d = cksRuntimeDecide(s), rules = [];
      rules.push(rule('^falco-ds$', !s.falco ? { tint: 'down', glow: 0 } : (!s.shellRule ? { tint: 'warn', glow: 0.4 } : (d.detected ? { tint: 'gold', glow: 0.8, pulse: true } : { tint: 'ok', glow: 0.45 }))));
      rules.push(rule('^sim-falco-blind$', !s.falco || !s.shellRule ? { show: true, tint: 'warn', glow: 0.6, pulse: !!d.shell } : { hide: true }));
      rules.push(rule('^sim-falco-alert$', d.detected ? { show: true, tint: 'deny', glow: 0.9, pulse: true } : { hide: true }));
      rules.push(rule('^falco-rules$', s.falco && !s.shellRule ? { tint: 'warn', glow: 0.5, pulse: true } : (s.falco ? { tint: 'ok', glow: 0.3 } : { tint: 'muted', glow: 0.05 })));
      rules.push(rule('^(edge-kernel-falco|syscall-stream)$', s.falco ? { tint: 'ok', glow: 0.4 } : { tint: 'down', glow: 0 }));
      rules.push(rule('^(edge-falco-out|falco-alerts)$', d.detected ? { tint: 'deny', glow: 0.7, pulse: true } : (s.falco ? { tint: 'ok', glow: 0.25 } : { tint: 'down', glow: 0 })));
      rules.push(rule('^apparmor-profile$', s.profileLoaded ? { tint: 'ok', glow: 0.45 } : { tint: 'muted', glow: 0.1 }));
      rules.push(rule('^sim-apparmor-missing$', d.rolloutStuck ? { show: true, tint: 'deny', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^apparmor-shield$', !s.apparmor ? { hide: true } : (d.rolloutStuck ? { tint: 'deny', glow: 0.5, pulse: true } : { tint: 'ok', glow: 0.5 })));
      rules.push(rule('^rootfs-layer$', s.readOnlyRoot ? { tint: 'ok', glow: 0.35 } : (d.dropped ? { tint: 'deny', glow: 0.6 } : { tint: 'warn', glow: 0.25 })));
      rules.push(rule('^payments-pod$', (d.exposures.length ? { tint: 'deny', glow: 0.7, pulse: true } : (d.shell || d.gaps.length ? { tint: 'warn', glow: 0.5 } : { tint: 'ok', glow: 0.45 }))));
      rules.push(rule('^(sim-attacker-shell|edge-shell-pod)$', d.shell ? { show: true, tint: 'deny', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^sim-rootfs-write$', d.dropped ? { show: true, tint: 'deny', glow: 0.9, pulse: true } : { hide: true }));
      rules.push(rule('^sim-write-denied$', d.shell && d.writeBlock ? { show: true, tint: 'ok', glow: 0.7 } : { hide: true }));
      rules.push(rule('^edge-pod-kernel$', { tint: 'ok', glow: 0.3 }));
      rules.push(rule('^edge-exec-api$', d.auditSeen ? { tint: 'warn', glow: 0.6, pulse: true } : { tint: 'muted', glow: 0.05 }));
      rules.push(rule('^sim-exec-recorded$', d.auditSeen ? { show: true, tint: 'warn', glow: 0.7 } : { hide: true }));
      rules.push(rule('^(kube-apiserver|edge-api-audit|audit-log)$', { tint: 'gold', glow: 0.3 }));
      rules.push(rule('^(node01|node-kernel|ns-payments)$', { tint: 'muted', glow: 0.05 }));
      var verdict = d.exposures.length ? 'exposed' : (d.shell || d.gaps.length ? 'degraded' : 'healthy');
      var cap = [];
      cap.push(d.rolloutStuck ? 'new payments-api pods CreateContainerError (apparmor profile not found k8s-deny-write) · old pods keep serving without the profile' : 'payments-api Running');
      if (d.shell) {
        cap.push('attacker shell via ' + (s.viaExec ? 'kubectl exec' : 'app exploit (no API request)'));
        cap.push(d.detected ? 'Falco: Warning Shell spawned in a container' : 'no runtime alert');
        cap.push(d.dropped ? 'write to /usr/local/bin succeeded' : 'write refused: ' + d.writeError);
        cap.push(d.auditSeen ? 'audit: create pods/exec (not the commands)' : 'audit: nothing');
      } else if (d.gaps.length && !d.rolloutStuck) cap.push('gaps: ' + d.gaps.join(' · '));
      return { verdict: verdict, metrics: d, caption: cap.join(' · '), rules: rules };
    }
  };

  /* ── CKS: Cluster Setup — CIS benchmark (kube-bench) — v1.10.0 (2026-11-04) ─────────────────────────────────────────
   * Scene contract (cks-cluster-hardening.glb, authored 2026-11-04 — the fourth CKS asset): cp-node / kube-apiserver /
   * apiserver-manifest (+ sim-profiling-on); etcd-db / etcd-dir (+ sim-etcd-open); kubelet / kubelet-config (+ sim-stale-config),
   * authn-gate, authz-gate, port-10250 (+ sim-kubelet-open, sim-kubelet-denied), port-10255 (+ sim-ro-port-open);
   * kube-bench → bench-report (+ sim-bench-fail, sim-bench-pass); pod-network / attacker-pod (+ sim-attacker-probe);
   * edges edge-kubelet-gates, edge-kubelet-sar, edge-api-etcd, edge-bench-api|etcd|kubelet, edge-probe-kubelet|ro.
   * Rules follow documented behaviour (kubelet authn/authz docs, kube-bench cfg/cis-1.12): an anonymous request to the
   * kubelet API is user system:anonymous; with authorization.mode AlwaysAllow every authenticated or anonymous request is
   * allowed, with Webhook the kubelet asks the API server (SubjectAccessReview) and refuses with 403 Forbidden; with
   * anonymous auth off an unauthenticated request gets 401 Unauthorized; readOnlyPort 10255 serves read-only kubelet data
   * over plain HTTP with no auth; the kubelet reads its config file only at start, so an edit needs a kubelet restart,
   * while kube-bench reads the file (and the process flags) and reports PASS as soon as the file is right; a static-pod
   * manifest edit is picked up by the kubelet, which re-creates the pod. CIS 4.2.4 is a Manual check: kube-bench reports
   * WARN, not FAIL. A not-restarted kubelet keeps the config it started with (snapshotted on the first edit). */
  var CH_CHECKS = [
    { id: '1.1.11', target: 'master', key: 'etcdLocked', manual: false, text: 'Ensure that the etcd data directory permissions are set to 700 or more restrictive (Automated)' },
    { id: '1.2.15', target: 'master', key: 'profilingOff', manual: false, text: 'Ensure that the --profiling argument is set to false (Automated)' },
    { id: '4.2.1', target: 'node', key: 'anonOff', manual: false, text: 'Ensure that the --anonymous-auth argument is set to false (Automated)' },
    { id: '4.2.2', target: 'node', key: 'webhookAuthz', manual: false, text: 'Ensure that the --authorization-mode argument is not set to AlwaysAllow (Automated)' },
    { id: '4.2.4', target: 'node', key: 'roPortClosed', manual: true, text: 'Verify that if defined, the --read-only-port argument is set to 0 (Manual)' }
  ];
  function cksHardenDecide(s) {
    var restarted = s.kubeletRestarted !== false;
    /* Not restarted: the process still runs the config it read at start (runAnonOff/runWebhookAuthz/runRoClosed, snapshotted
     * by the CLI when it edits config.yaml; absent = the insecure pre-hardening config). */
    var run = restarted ? { anonOff: !!s.anonOff, webhookAuthz: !!s.webhookAuthz, roPortClosed: !!s.roPortClosed } : { anonOff: !!s.runAnonOff, webhookAuthz: !!s.runWebhookAuthz, roPortClosed: !!s.runRoClosed };
    var token = !!s.probeToken;
    var user = token ? 'system:serviceaccount:default:default' : (run.anonOff ? null : 'system:anonymous');
    var kubeletCode = !user ? 401 : (run.webhookAuthz ? 403 : 200);
    var bench = CH_CHECKS.map(function (c) { return { id: c.id, target: c.target, text: c.text, result: s[c.key] ? 'PASS' : (c.manual ? 'WARN' : 'FAIL') }; });
    var fails = bench.filter(function (b) { return b.result !== 'PASS'; });
    var stale = !restarted && (run.anonOff !== !!s.anonOff || run.webhookAuthz !== !!s.webhookAuthz || run.roPortClosed !== !!s.roPortClosed);
    var probe = !!s.probe;
    var exposures = [];
    if (probe && kubeletCode === 200) exposures.push('kubelet-api-open');
    if (probe && !run.roPortClosed) exposures.push('readonly-port-leak');
    var gaps = fails.map(function (b) { return 'CIS ' + b.id + ' ' + b.result; });
    if (stale) gaps.push('kubelet not restarted: running config ≠ config.yaml');
    return {
      running: run,
      restarted: restarted,
      stale: stale,
      user: user,
      kubeletCode: kubeletCode,
      kubeletMsg: kubeletCode === 401 ? 'Unauthorized' : (kubeletCode === 403 ? 'Forbidden (user=' + user + ', verb=get, resource=nodes, subresource=proxy)' : '200 OK (PodList)'),
      roOpen: !run.roPortClosed,
      bench: bench,
      fails: fails,
      allPass: !fails.length,
      gaps: gaps,
      exposures: exposures
    };
  }

  var cksClusterHardening = {
    id: 'cks-cluster-hardening',
    title: 'CKS cluster setup drill: CIS benchmark with kube-bench — kubelet anonymous auth, AlwaysAllow vs Webhook, read-only port, restart after config edits, etcd data dir permissions, API server profiling',
    cert: 'CKS',
    glb: '/assets/immersive/cks-cluster-hardening.glb',
    initial: { anonOff: true, webhookAuthz: true, roPortClosed: true, kubeletRestarted: true, etcdLocked: true, profilingOff: true, probe: false, probeToken: false },
    toggles: [
      { id: 'anonOff', label: 'kubelet authentication.anonymous.enabled', on: 'false', off: 'true' },
      { id: 'webhookAuthz', label: 'kubelet authorization.mode', on: 'Webhook', off: 'AlwaysAllow' },
      { id: 'roPortClosed', label: 'kubelet readOnlyPort', on: '0', off: '10255' },
      { id: 'kubeletRestarted', label: 'kubelet since the last config.yaml edit', on: 'restarted', off: 'not restarted' },
      { id: 'etcdLocked', label: '/var/lib/etcd mode', on: '700', off: '755' },
      { id: 'profilingOff', label: 'kube-apiserver --profiling', on: 'false', off: 'true' },
      { id: 'probe', label: 'compromised pod probing node ports', on: 'probing', off: 'quiet' },
      { id: 'probeToken', label: 'probe credential', on: 'its ServiceAccount token', off: 'none (anonymous)' }
    ],
    scenarios: [
      { id: 'anon-alwaysallow', label: 'Anonymous + AlwaysAllow', set: { anonOff: false, webhookAuthz: false, roPortClosed: true, kubeletRestarted: true, etcdLocked: true, profilingOff: true, probe: true, probeToken: false },
        predict: { q: 'The kubelet config on controlplane has authentication.anonymous.enabled: true and authorization.mode: AlwaysAllow. From a compromised pod, an attacker runs curl -sk https://10.0.0.10:10250/pods with no credentials. What comes back?',
          options: ['401 Unauthorized, because the kubelet API always requires a client certificate',
            'A full PodList as JSON. The request is user system:anonymous, AlwaysAllow authorizes everything, and the same API also serves /exec and /run, so the attacker can run commands in any pod on the node. kube-bench reports [FAIL] 4.2.1 and 4.2.2',
            '403 Forbidden, because anonymous users are never authorized'],
          answer: 1, why: 'With anonymous authentication on, a request with no client certificate or bearer token is not rejected; it is authenticated as system:anonymous in group system:unauthenticated. Authorization then decides, and AlwaysAllow allows every request. The kubelet API on :10250 serves /pods, /logs, /exec and /run, so this is remote code execution in every pod on the node. CIS 4.2.1 (anonymous-auth false) and 4.2.2 (authorization-mode not AlwaysAllow) exist for exactly this. kubeadm sets both safely by default; hand-built or old clusters often do not.' } },
      { id: 'anon-webhook', label: 'Anonymous, but Webhook', set: { anonOff: false, webhookAuthz: true, roPortClosed: true, kubeletRestarted: true, etcdLocked: true, profilingOff: true, probe: true, probeToken: false },
        predict: { q: 'Same probe, but authorization.mode is now Webhook while anonymous authentication is still enabled. What does curl -sk https://10.0.0.10:10250/pods return, and what does kube-bench say?',
          options: ['A PodList, because Webhook only applies to bearer tokens',
            '401 Unauthorized, and kube-bench reports every 4.2 check as PASS',
            'Forbidden (user=system:anonymous, verb=get, resource=nodes, subresource=proxy). Webhook mode asks the API server with a SubjectAccessReview and RBAC grants system:anonymous nothing. The request was still authenticated as anonymous, so kube-bench still reports [FAIL] 4.2.1'],
          answer: 2, why: 'Authentication and authorization are separate steps. With anonymous auth on, the request becomes system:anonymous; Webhook authorization then sends a SubjectAccessReview to the API server, which checks RBAC for nodes/proxy and denies it, so the kubelet answers 403 Forbidden and names the user and resource it tried. That is safe today, but one careless ClusterRoleBinding to system:unauthenticated would open the node, so CIS 4.2.1 still wants anonymous auth off (then the answer is 401 Unauthorized).' } },
      { id: 'readonly-port', label: 'Read-only port 10255', set: { anonOff: true, webhookAuthz: true, roPortClosed: false, kubeletRestarted: true, etcdLocked: true, profilingOff: true, probe: true, probeToken: false },
        predict: { q: 'Anonymous auth is off and authorization is Webhook, so :10250 answers 401. But config.yaml still has readOnlyPort: 10255. What does curl -s http://10.0.0.10:10255/pods return, and how does kube-bench report it?',
          options: ['The full PodList over plain HTTP with no credentials at all (pod specs, env values, image names). kube-bench reports [WARN] 4.2.4, not FAIL, because the check is Manual; set readOnlyPort: 0 and restart the kubelet',
            'Nothing, because the read-only port also enforces Webhook authorization',
            '401 Unauthorized, because anonymous auth covers every kubelet port'],
          answer: 0, why: 'The read-only port is a separate, unauthenticated HTTP listener that serves read-only kubelet endpoints such as /pods and /spec. None of the authentication or authorization settings apply to it. Pod specs often carry environment variables and image references an attacker can use. kube-bench marks CIS 4.2.4 as Manual, so a non-zero port shows up as [WARN], which is easy to skim past. Setting readOnlyPort: 0 disables it (a kubelet restart is needed for the change to take effect).' } },
      { id: 'no-restart', label: 'PASS, still open', set: { anonOff: true, webhookAuthz: true, roPortClosed: true, kubeletRestarted: false, etcdLocked: true, profilingOff: true, probe: true, probeToken: false },
        predict: { q: 'You fixed anonymous.enabled, authorization.mode and readOnlyPort in /var/lib/kubelet/config.yaml with sed, then ran kube-bench run --targets node: 4.2.1, 4.2.2 and 4.2.4 all show [PASS]. You did not restart anything. What does the anonymous curl to :10250/pods return now?',
          options: ['401 Unauthorized, because kube-bench PASS means the kubelet is fixed',
            'Still the PodList. The kubelet reads config.yaml only when it starts, so the running process keeps the old settings. kube-bench read the file and passed it. Run systemctl restart kubelet (daemon-reload alone only re-reads unit files), then prove it with curl',
            'The kubelet notices the file change and exits, so the node goes NotReady'],
          answer: 1, why: 'The kubelet loads its configuration file at start-up. Editing the file changes nothing in the running process until the kubelet is restarted (systemctl restart kubelet). kube-bench checks the process flags (ps -fC kubelet) and the config file it points to, so it reports PASS as soon as the file is right. A green report is evidence about configuration, not about the running state, so always re-test the behaviour (curl the port) after restarting.' } },
      { id: 'etcd-perms', label: 'etcd data dir 755', set: { anonOff: true, webhookAuthz: true, roPortClosed: true, kubeletRestarted: true, etcdLocked: false, profilingOff: true, probe: false, probeToken: false },
        predict: { q: 'kube-bench run --targets master reports [FAIL] 1.1.11 on controlplane: stat -c %a /var/lib/etcd prints 755. Why does that matter, and what is the remediation?',
          options: ['It does not matter, because etcd encrypts its data directory by default',
            'It only matters for etcd backups; snapshots refuse to run until the mode is 700',
            'Any local user on the node can read the etcd database files, which hold every Secret (base64, and in plaintext unless encryption at rest is configured). Run chmod 700 /var/lib/etcd (and keep it owned by etcd:etcd, CIS 1.1.12), then re-run the check'],
          answer: 2, why: 'etcd stores the whole cluster state, including every Secret, in its data directory. Secrets are only base64-encoded unless the API server is configured with an EncryptionConfiguration, so readable database files mean readable credentials. CIS 1.1.11 wants mode 700 or stricter so only the owner can read it; 1.1.12 wants ownership etcd:etcd (on kubeadm clusters etcd runs as root in a static pod, so the directory is root-owned there). The remediation in the kube-bench report is literally chmod 700 /var/lib/etcd.' } },
      { id: 'profiling', label: 'API server profiling on', set: { anonOff: true, webhookAuthz: true, roPortClosed: true, kubeletRestarted: true, etcdLocked: true, profilingOff: false, probe: false, probeToken: false },
        predict: { q: 'kube-bench reports [FAIL] 1.2.15 (--profiling). You edit /etc/kubernetes/manifests/kube-apiserver.yaml so it has - --profiling=false. What do you need to do for the change to take effect?',
          options: ['Nothing more. The kubelet watches the static-pod manifest directory and re-creates the kube-apiserver pod when the file changes; wait for it to come back (kubectl may fail for a minute), then re-run kube-bench',
            'systemctl restart kube-apiserver, because the API server is a systemd service',
            'kubectl apply -f /etc/kubernetes/manifests/kube-apiserver.yaml'],
          answer: 0, why: 'On kubeadm clusters the control-plane components are static pods. The kubelet watches /etc/kubernetes/manifests (staticPodPath) and re-creates a pod whose manifest changed, so saving the file is the deployment. There is no kube-apiserver systemd unit, and kubectl apply would create a second, ordinary Pod object and leave the static pod unchanged. Profiling exposes /debug/pprof on the API server, which leaks performance internals and can be abused for denial of service; CIS wants it off on the API server, controller manager and scheduler (1.2.15, 1.3.2, 1.4.1). Back up the manifest outside the manifests directory before editing.' } },
      { id: 'token-alwaysallow', label: 'Anonymous off, AlwaysAllow', set: { anonOff: true, webhookAuthz: false, roPortClosed: true, kubeletRestarted: true, etcdLocked: true, profilingOff: true, probe: true, probeToken: true },
        predict: { q: 'Anonymous auth is off, but authorization.mode is still AlwaysAllow. The attacker reads the default ServiceAccount token mounted in the compromised pod and sends it: curl -sk -H "Authorization: Bearer $TOKEN" https://10.0.0.10:10250/pods. What happens?',
          options: ['401 Unauthorized, because anonymous auth is off',
            'A PodList. The kubelet authenticates the token with a TokenReview (webhook authentication), so the request is system:serviceaccount:default:default, and AlwaysAllow lets any authenticated user do anything, including /exec. Turning anonymous auth off is not enough; set authorization.mode: Webhook (CIS 4.2.2)',
            '403 Forbidden, because ServiceAccount tokens are only valid against the API server'],
          answer: 1, why: 'With authentication.webhook.enabled the kubelet validates bearer tokens through the API server (TokenReview), so any ServiceAccount token from any pod authenticates. Authorization is the step that should stop it, and AlwaysAllow does not. That is why CIS has two separate checks: 4.2.1 removes anonymous access and 4.2.2 makes every authenticated request go through a SubjectAccessReview against RBAC, where a default ServiceAccount has no nodes/proxy permission (403 Forbidden).' } },
      { id: 'heal', label: 'Reset', set: { anonOff: true, webhookAuthz: true, roPortClosed: true, kubeletRestarted: true, etcdLocked: true, profilingOff: true, probe: false, probeToken: false } }
    ],
    derive: function (s) {
      var d = cksHardenDecide(s), rules = [];
      var probe = !!s.probe;
      rules.push(rule('^kubelet$', d.kubeletCode === 200 ? { tint: 'deny', glow: 0.6, pulse: probe } : (d.stale ? { tint: 'warn', glow: 0.5, pulse: true } : { tint: 'ok', glow: 0.45 })));
      rules.push(rule('^kubelet-config$', d.stale ? { tint: 'warn', glow: 0.5 } : (s.anonOff && s.webhookAuthz && s.roPortClosed ? { tint: 'ok', glow: 0.3 } : { tint: 'deny', glow: 0.4 })));
      rules.push(rule('^sim-stale-config$', d.stale ? { show: true, tint: 'warn', glow: 0.7, pulse: true } : { hide: true }));
      rules.push(rule('^authn-gate$', d.running.anonOff ? { tint: 'ok', glow: 0.5 } : { tint: 'warn', glow: 0.25 }));
      rules.push(rule('^authz-gate$', d.running.webhookAuthz ? { tint: 'ok', glow: 0.5 } : { tint: 'deny', glow: 0.3 }));
      rules.push(rule('^(port-10250|edge-kubelet-gates)$', d.kubeletCode === 200 ? { tint: 'deny', glow: 0.6 } : { tint: 'ok', glow: 0.35 }));
      rules.push(rule('^edge-kubelet-sar$', d.running.webhookAuthz ? { tint: 'ok', glow: 0.4 } : { tint: 'muted', glow: 0.05 }));
      rules.push(rule('^sim-kubelet-open$', probe && d.kubeletCode === 200 ? { show: true, tint: 'deny', glow: 0.9, pulse: true } : { hide: true }));
      rules.push(rule('^sim-kubelet-denied$', probe && d.kubeletCode !== 200 ? { show: true, tint: 'ok', glow: 0.7 } : { hide: true }));
      rules.push(rule('^port-10255$', d.roOpen ? { tint: 'deny', glow: 0.5 } : { tint: 'muted', glow: 0.05 }));
      rules.push(rule('^sim-ro-port-open$', d.roOpen ? { show: true, tint: 'deny', glow: 0.8, pulse: probe } : { hide: true }));
      rules.push(rule('^(etcd-dir)$', s.etcdLocked ? { tint: 'ok', glow: 0.3 } : { tint: 'deny', glow: 0.5 }));
      rules.push(rule('^sim-etcd-open$', !s.etcdLocked ? { show: true, tint: 'deny', glow: 0.7, pulse: true } : { hide: true }));
      rules.push(rule('^apiserver-manifest$', s.profilingOff ? { tint: 'ok', glow: 0.3 } : { tint: 'warn', glow: 0.5 }));
      rules.push(rule('^sim-profiling-on$', !s.profilingOff ? { show: true, tint: 'deny', glow: 0.7, pulse: true } : { hide: true }));
      rules.push(rule('^(kube-bench|bench-report)$', d.allPass ? { tint: 'gold', glow: 0.4 } : { tint: 'warn', glow: 0.55 }));
      rules.push(rule('^sim-bench-fail$', !d.allPass ? { show: true, tint: 'deny', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^sim-bench-pass$', d.allPass && (d.stale || s.probe) ? { show: true, tint: d.stale ? 'warn' : 'ok', glow: 0.6 } : { hide: true }));
      rules.push(rule('^(edge-bench-api|edge-bench-etcd|edge-bench-kubelet)$', { tint: 'gold', glow: 0.25 }));
      rules.push(rule('^attacker-pod$', probe ? { tint: 'deny', glow: 0.5 } : { tint: 'muted', glow: 0.05 }));
      rules.push(rule('^sim-attacker-probe$', probe ? { show: true, tint: 'deny', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^edge-probe-kubelet$', probe ? (d.kubeletCode === 200 ? { tint: 'deny', glow: 0.8, pulse: true } : { tint: 'warn', glow: 0.4 }) : { tint: 'muted', glow: 0.05 }));
      rules.push(rule('^edge-probe-ro$', probe && d.roOpen ? { tint: 'deny', glow: 0.8, pulse: true } : { tint: 'muted', glow: 0.05 }));
      rules.push(rule('^(kube-apiserver|etcd-db|edge-api-etcd)$', { tint: 'gold', glow: 0.3 }));
      rules.push(rule('^(cp-node|pod-network)$', { tint: 'muted', glow: 0.05 }));
      var verdict = d.exposures.length ? 'exposed' : (d.gaps.length ? 'degraded' : 'healthy');
      var cap = [];
      cap.push('kube-bench: ' + (d.allPass ? 'every modelled check PASS' : d.fails.map(function (b) { return '[' + b.result + '] ' + b.id; }).join(' ')));
      if (d.stale) cap.push('config.yaml edited, kubelet not restarted: running config is the old one');
      if (probe) {
        cap.push(':10250 ' + (s.probeToken ? 'with SA token' : 'anonymous') + ' → ' + d.kubeletMsg);
        cap.push(':10255 → ' + (d.roOpen ? 'PodList over HTTP, no auth' : 'connection refused'));
      }
      return { verdict: verdict, metrics: d, caption: cap.join(' · '), rules: rules };
    }
  };

  /* ── CKS: Supply Chain Security — static analysis of workloads (kubesec + KubeLinter) — v1.11.0 (2026-11-05) ─────────
   * Scene contract (cks-static-analysis.glb, authored 2026-11-05 — the fifth CKS asset): git-repo / manifest-file with its
   * fields field-privileged, field-nonroot, field-rootfs, field-resources, field-secret, field-image and the lint-ignore
   * annotation tag; kubesec → kubesec-score (+ sim-kubesec-critical); kube-linter → lint-report (+ sim-lint-fail); ci-pipeline
   * → ci-gate (+ sim-gate-block, sim-gate-bypass); kube-apiserver → ns-payments / payments-pod over image-layer (+ sim-ccce,
   * sim-privileged-flare, sim-secret-leak); edges edge-manifest-kubesec|linter, edge-scan-gate, edge-gate-api, edge-api-pod.
   * Rules follow the tools' published behaviour: kubesec (controlplaneio/kubesec v2 ruleset) sums the points of every
   * matched rule (negative rules are listed as "critical", unmatched positive rules as "advise"), reports "Passed with a
   * score of N points" when the total is ≥ 0 and "Failed with a score of N points" otherwise, and `kubesec scan` exits 2
   * when any score is ≤ 0. It has no rule for a literal secret value in env, and it scores env valueFrom.secretKeyRef at -5
   * (SecretsAsEnvironmentVariables). KubeLinter (stackrox/kube-linter) reports one line per failed check and exits 1 with
   * "Error: found N lint errors"; env-var-secret flags a literal value in an env var whose name contains "secret";
   * ignore-check.kube-linter.io/<check> silences only that one check, so a privileged container still fails
   * privilege-escalation-container. Both read only the manifest: the kubelet checks the image user at container start, so
   * runAsNonRoot over an image that runs as root fails with CreateContainerConfigError. A scan blocks nothing unless a CI
   * gate (or admission) acts on its exit code. */
  var SA_POS = [
    { id: 'ServiceAccountName', points: 3, key: null, reason: 'Service accounts restrict Kubernetes API access and should be configured with least privilege' },
    { id: 'CapDropAny', points: 1, key: null, reason: 'Reducing kernel capabilities available to a container limits its attack surface' },
    { id: 'CapDropAll', points: 1, key: null, reason: 'Drop all capabilities and add only those required to reduce syscall attack surface' },
    { id: 'RunAsNonRoot', points: 1, key: 'nonRoot', reason: 'Force the running image to run as a non-root user to ensure least privilege' },
    { id: 'ReadOnlyRootFilesystem', points: 1, key: 'roRoot', reason: 'An immutable root filesystem can prevent malicious binaries being added to PATH and increase attack cost' },
    { id: 'RequestsCPU', points: 1, key: 'requestsSet', reason: 'Enforcing CPU requests aids a fair balancing of resources across the cluster' },
    { id: 'RequestsMemory', points: 1, key: 'requestsSet', reason: 'Enforcing memory requests aids a fair balancing of resources across the cluster' },
    { id: 'LimitsCPU', points: 1, key: 'limitsSet', reason: 'Enforcing CPU limits prevents DOS via resource exhaustion' },
    { id: 'LimitsMemory', points: 1, key: 'limitsSet', reason: 'Enforcing memory limits prevents DOS via resource exhaustion' },
    { id: 'RunAsUser', points: 1, key: false, reason: 'Run as a high-UID user to avoid conflicts with the host\'s users' },
    { id: 'SeccompAny', points: 1, key: false, reason: 'Seccomp profiles set minimum privilege and secure against unknown threats' }
  ];
  var SA_REM = {
    'privileged-container': 'Do not run your container as privileged unless it is required.',
    'privilege-escalation-container': 'Ensure containers do not allow privilege escalation by setting allowPrivilegeEscalation=false, privileged=false and removing CAP_SYS_ADMIN capability. See https://kubernetes.io/docs/tasks/configure-pod-container/security-context/ for more details.',
    'run-as-non-root': 'Set runAsUser and runAsGroup to non-zero numbers and runAsNonRoot to true in your pod or container securityContext. Refer to https://kubernetes.io/docs/tasks/configure-pod-container/security-context/ for details.',
    'no-read-only-root-fs': 'Set readOnlyRootFilesystem to true in the container securityContext.',
    'unset-cpu-requirements': 'Set CPU requests for your container based on its requirements. Refer to https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits for details.',
    'unset-memory-requirements': 'Set memory limits for your container based on its requirements. Refer to https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits for details.',
    'env-var-secret': 'Do not use raw secrets in environment variables. Instead, either mount the secret as a file or use a secretKeyRef. Refer to https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets for details.',
    'latest-tag': 'Use a container image with a specific tag other than latest.'
  };
  var SA_IMAGE = 'registry.example.com/payments-api';
  function cksStaticDecide(s) {
    var critical = [], passed = [], advise = [];
    if (!s.privOff) critical.push({ id: 'Privileged', points: -30, reason: 'Privileged containers can allow almost completely unrestricted host access' });
    if (s.secretRef) critical.push({ id: 'SecretsAsEnvironmentVariables', points: -5, reason: 'Secrets passed as environment variables can be easily exposed through application logs, crash dumps, and system process inspection' });
    SA_POS.forEach(function (r) { var hit = r.key === null ? true : (r.key === false ? false : !!s[r.key]); (hit ? passed : advise).push({ id: r.id, points: r.points, reason: r.reason }); });
    var score = critical.concat(passed).reduce(function (n, r) { return n + r.points; }, 0);
    var lint = [];
    var c = 'container "api"';
    if (!s.privOff && s.noIgnore) lint.push({ check: 'privileged-container', msg: c + ' is privileged' });
    if (!s.privOff) lint.push({ check: 'privilege-escalation-container', msg: c + ' is Privileged hence allows privilege escalation.' });
    if (!s.nonRoot) lint.push({ check: 'run-as-non-root', msg: c + ' is not set to runAsNonRoot' });
    if (!s.roRoot) lint.push({ check: 'no-read-only-root-fs', msg: c + ' does not have a read-only root file system' });
    if (!s.requestsSet) lint.push({ check: 'unset-cpu-requirements', msg: c + ' has cpu request 0' });
    if (!s.limitsSet) lint.push({ check: 'unset-memory-requirements', msg: c + ' has memory limit 0' });
    if (!s.secretRef) lint.push({ check: 'env-var-secret', msg: 'environment variable PAYMENTS_API_SECRET in ' + c + ' found' });
    if (!s.pinned) lint.push({ check: 'latest-tag', msg: 'The ' + c + ' is using an invalid container image, "' + SA_IMAGE + ':latest". Please use images that are not blocked by the `BlockList` criteria : [".*:(latest)$" "^[^:]*$" "(.*/[^:]+)$"]' });
    lint.forEach(function (l) { l.remediation = SA_REM[l.check]; });
    var kubesecFail = score <= 0, lintFail = lint.length > 0, findings = kubesecFail || lintFail;
    var gate = !!s.ciGate, blocked = gate && findings, deployed = !blocked;
    /* The :latest image of this lab was built FROM a base with no USER (root); 1.4.2 is distroless with numeric USER 65532. */
    var imageRoot = !s.pinned;
    var ccce = deployed && !!s.nonRoot && imageRoot;
    var exposures = [];
    if (deployed && !s.privOff) exposures.push('privileged-pod-running');
    if (deployed && !s.secretRef) exposures.push('literal-secret-in-spec');
    var gaps = [];
    if (kubesecFail) gaps.push('kubesec score ' + score);
    lint.forEach(function (l) { gaps.push('kube-linter ' + l.check); });
    if (ccce) gaps.push('CreateContainerConfigError: runAsNonRoot over a root image');
    return {
      score: score,
      kubesecMsg: (score >= 0 ? 'Passed' : 'Failed') + ' with a score of ' + score + ' points',
      kubesecExit: kubesecFail ? 2 : 0,
      critical: critical, passed: passed, advise: advise,
      lint: lint, lintExit: lintFail ? 1 : 0,
      findings: findings, gate: gate, blocked: blocked, deployed: deployed,
      imageRoot: imageRoot, ccce: ccce,
      podStatus: blocked ? 'Running (previous revision — the gate stopped this one)' : (ccce ? 'CreateContainerConfigError' : 'Running'),
      exposures: exposures, gaps: gaps
    };
  }

  var cksStaticAnalysis = {
    id: 'cks-static-analysis',
    title: 'CKS supply chain drill: static analysis of workloads — kubesec scores, KubeLinter checks, CI gates, ignore annotations, and what a manifest scan cannot see',
    cert: 'CKS',
    glb: '/assets/immersive/cks-static-analysis.glb',
    initial: { privOff: true, nonRoot: true, roRoot: true, requestsSet: true, limitsSet: true, secretRef: true, pinned: true, noIgnore: true, ciGate: true, rolled: true },
    toggles: [
      { id: 'privOff', label: 'securityContext.privileged', on: 'false', off: 'true' },
      { id: 'nonRoot', label: 'securityContext.runAsNonRoot', on: 'true', off: 'false' },
      { id: 'roRoot', label: 'securityContext.readOnlyRootFilesystem', on: 'true', off: 'false' },
      { id: 'requestsSet', label: 'resources.requests', on: 'cpu 100m · memory 128Mi', off: '{}' },
      { id: 'limitsSet', label: 'resources.limits', on: 'cpu 500m · memory 256Mi', off: '{}' },
      { id: 'secretRef', label: 'env PAYMENTS_API_SECRET', on: 'valueFrom.secretKeyRef', off: 'literal value' },
      { id: 'pinned', label: 'image', on: 'payments-api:1.4.2 (USER 65532)', off: 'payments-api:latest (root)' },
      { id: 'noIgnore', label: 'ignore-check.kube-linter.io/privileged-container', on: 'absent', off: 'annotated' },
      { id: 'ciGate', label: 'CI acts on the scanners\' exit codes', on: 'gate (set -e)', off: '|| true' }
    ],
    scenarios: [
      { id: 'privileged', label: 'privileged: true', set: { privOff: false, nonRoot: true, roRoot: true, requestsSet: true, limitsSet: true, secretRef: true, pinned: true, noIgnore: true, ciGate: true },
        predict: { q: 'payments-api.yaml is hardened (ServiceAccount, drop ALL, runAsNonRoot, read-only root, requests and limits, secretKeyRef) except one line: privileged: true. CI runs kubesec scan payments-api.yaml under set -e. What does kubesec report?',
          options: ['"Passed with a score of 6 points": the positive rules outweigh one bad field',
            '"Failed with a score of -24 points", with Privileged (-30) listed under critical. kubesec sums every matched rule, the total is ≤ 0, so it exits 2 and the gated pipeline stops before kubectl apply',
            'kubesec refuses to scan a Deployment; it only scores Pods'],
          answer: 1, why: 'kubesec adds up the points of every rule that matches. Privileged is worth -30, more than every positive rule in this manifest combined (ServiceAccountName +3, CapDropAny and CapDropAll +1 each, RunAsNonRoot, ReadOnlyRootFilesystem and four resource rules +1 each = 11, minus 5 for SecretsAsEnvironmentVariables). 6 - 30 = -24, so the message is "Failed with a score of -24 points" and kubesec scan exits 2 (its default --exit-code) because a score is ≤ 0. Deployments, StatefulSets and DaemonSets are scored like Pods, through their pod template.' } },
      { id: 'no-gate', label: 'Scan with || true', set: { privOff: false, nonRoot: true, roRoot: true, requestsSet: true, limitsSet: true, secretRef: true, pinned: true, noIgnore: true, ciGate: false },
        predict: { q: 'Same privileged manifest, but ci/lint.sh runs kubesec scan payments-api.yaml || true and kube-linter lint payments-api.yaml || true before kubectl apply -f payments-api.yaml. What runs in the cluster?',
          options: ['Nothing: kubesec and KubeLinter reject the object at the API server',
            'The pipeline stays green with a warning, and the API server refuses privileged pods by default',
            'A privileged payments-api pod. Both reports print their findings, || true throws the exit codes away, and kubectl apply succeeds. Static analysis is advisory unless something acts on it: a CI gate on the exit code, or admission (Pod Security restricted, a policy engine) in the cluster'],
          answer: 2, why: 'kubesec and KubeLinter are offline tools. They read YAML files and print a report; they are not admission controllers and the API server never consults them. The only thing that turns their findings into a block is their exit code (kubesec 2, KubeLinter 1) and a pipeline that stops on it. With || true the step always succeeds, and nothing in a default cluster rejects privileged: true (Pod Security Admission only enforces when a namespace is labelled). For defence in depth, gate in CI and enforce Pod Security Standards (or a policy engine) at admission, because kubectl apply from a laptop skips CI entirely.' } },
      { id: 'secret-literal', label: 'Literal secret in env', set: { privOff: true, nonRoot: true, roRoot: true, requestsSet: true, limitsSet: true, secretRef: false, pinned: true, noIgnore: true, ciGate: true },
        predict: { q: 'A developer replaced the secretKeyRef with a literal: - name: PAYMENTS_API_SECRET / value: "sk_live_…". What do the two scanners say?',
          options: ['kubesec: "Passed with a score of 11 points", exit 0 (it has no rule for a literal value, and the -5 for secretKeyRef is gone, so the score went UP). KubeLinter: env-var-secret, environment variable PAYMENTS_API_SECRET in container "api" found, exit 1. The gate stops it only because KubeLinter is in the pipeline',
            'Both fail: every scanner detects secrets in manifests',
            'kubesec fails with SecretsAsEnvironmentVariables; KubeLinter passes'],
          answer: 0, why: 'The two tools have different rule sets. kubesec\'s SecretsAsEnvironmentVariables rule (-5) matches env[].valueFrom.secretKeyRef and envFrom[].secretRef, because secrets in env vars leak through logs, crash dumps and /proc. A literal value is not a Secret reference, so kubesec does not see it at all and the score rises from 6 to 11. KubeLinter\'s env-var-secret check matches env vars whose name contains "secret" and that have a literal value. A literal in the manifest is also readable by anyone who can get the Deployment and is committed to git. The safest form is a Secret mounted as a file, which clears both tools.' } },
      { id: 'ignore-annotation', label: 'ignore-check annotation', set: { privOff: false, nonRoot: true, roRoot: true, requestsSet: true, limitsSet: true, secretRef: true, pinned: true, noIgnore: false, ciGate: true },
        predict: { q: 'To get CI green, someone added metadata.annotations: ignore-check.kube-linter.io/privileged-container: "debug needs it" and left privileged: true. What happens on the gated pipeline?',
          options: ['KubeLinter still exits 1: the annotation silences only privileged-container, and privilege-escalation-container still reports: container "api" is Privileged hence allows privilege escalation. kubesec ignores KubeLinter annotations and still fails with -24. The gate holds',
            'Everything passes: the annotation disables KubeLinter for the object and kubesec honours it too',
            'KubeLinter refuses the file because ignore annotations need a cluster-admin signature'],
          answer: 0, why: 'ignore-check.kube-linter.io/<check-name> is KubeLinter\'s documented per-object escape hatch, and it switches off exactly one check. privileged: true also trips privilege-escalation-container, which still fails. kubesec has its own rules and knows nothing about KubeLinter annotations, so its -24 stands. Ignore annotations are code: review them like code (who added it, is the reason true), and treat a new one on a privileged workload as a finding in itself.' } },
      { id: 'nonroot-runtime', label: 'runAsNonRoot over a root image', set: { privOff: true, nonRoot: true, roRoot: true, requestsSet: true, limitsSet: true, secretRef: true, pinned: false, noIgnore: true, ciGate: false },
        predict: { q: 'The manifest says runAsNonRoot: true and uses image payments-api:latest, which was built FROM a base with no USER line (it runs as root). CI is not gated. kubesec passes and KubeLinter only reports latest-tag. What happens to the new pods?',
          options: ['They run as root: runAsNonRoot is only a hint for scanners',
            'They stay in CreateContainerConfigError: "Error: container has runAsNonRoot and image will run as root". The scanners read the manifest, not the image; the kubelet checks the image\'s user when it starts the container. Pin an image whose USER is a numeric non-root UID (payments-api:1.4.2 runs as 65532) or set runAsUser',
            'The API server rejects the Deployment because the image user is root'],
          answer: 1, why: 'runAsNonRoot is enforced by the kubelet at container start, not by the API server and not by any static analyser. If no runAsUser is set, the kubelet reads the user from the image config. If that is root (UID 0, or no USER at all) it refuses to start the container, and the pod shows CreateContainerConfigError with exactly that message. A non-numeric USER fails too, because the kubelet cannot verify it. Manifest scanners such as kubesec and KubeLinter cannot know what the image does. That is why image scanning and a tested build belong in the pipeline as well, and why a mutable :latest tag (KubeLinter latest-tag) makes the result depend on whatever was pushed last.' } },
      { id: 'no-resources', label: 'No requests or limits', set: { privOff: true, nonRoot: true, roRoot: true, requestsSet: false, limitsSet: false, secretRef: true, pinned: true, noIgnore: true, ciGate: true },
        predict: { q: 'resources: requests: {} and limits: {}. Everything else is hardened. Which scanner stops the gated pipeline?',
          options: ['kubesec, because unset limits are critical findings',
            'Neither: resources are not a security setting',
            'Only KubeLinter: unset-cpu-requirements ("has cpu request 0") and unset-memory-requirements ("has memory limit 0"), exit 1. kubesec lists the four resource rules under advise and reports "Passed with a score of 2 points", exit 0, because it only fails when the total is ≤ 0'],
          answer: 2, why: 'kubesec gives +1 each for RequestsCPU, RequestsMemory, LimitsCPU and LimitsMemory and lists missing ones as advice. Advice costs nothing, so 6 - 4 = 2 and the scan still passes with exit 0. KubeLinter turns the same gaps into failed checks (by default it wants a CPU request and a memory limit), so it exits 1. Unbounded containers are a denial-of-service risk to every other pod on the node. Know which tool enforces which policy, because a gate is only as strict as the tool behind it.' } },
      { id: 'critical-but-passed', label: '"critical" but Passed', set: { privOff: true, nonRoot: true, roRoot: false, requestsSet: true, limitsSet: true, secretRef: true, pinned: true, noIgnore: true, ciGate: true },
        predict: { q: 'readOnlyRootFilesystem is false; everything else is hardened and the secret comes from a secretKeyRef. kubesec\'s JSON shows SecretsAsEnvironmentVariables (-5) under "critical". What are its message and exit code, and does the gated pipeline pass?',
          options: ['"Failed with a score of -5 points", exit 2: any critical entry fails',
            '"Passed with a score of 5 points", exit 0: kubesec fails only when the total is ≤ 0, and a "critical" entry is just a negative rule. The pipeline still stops, because KubeLinter reports no-read-only-root-fs and exits 1',
            '"Passed with a score of 5 points" and the pipeline deploys'],
          answer: 1, why: 'In kubesec, every matched negative rule lands in "critical", whatever its size, and the score is the plain sum: 11 positive points - 1 for the missing ReadOnlyRootFilesystem - 5 for SecretsAsEnvironmentVariables = 5. The message is "Passed with a score of 5 points" and kubesec scan exits 0. If you want critical entries to fail the build, check the JSON (for example with jq on .scoring.critical) instead of trusting the exit code. KubeLinter\'s no-read-only-root-fs check fails on its own, so the gate still holds. Mounting the Secret as a file would remove the -5.' } },
      { id: 'heal', label: 'Reset', set: { privOff: true, nonRoot: true, roRoot: true, requestsSet: true, limitsSet: true, secretRef: true, pinned: true, noIgnore: true, ciGate: true } }
    ],
    derive: function (s) {
      var d = cksStaticDecide(s), rules = [];
      var ok = { tint: 'ok', glow: 0.3 };
      rules.push(rule('^field-privileged$', s.privOff ? ok : { tint: 'deny', glow: 0.6, pulse: true }));
      rules.push(rule('^field-nonroot$', !s.nonRoot ? { tint: 'warn', glow: 0.5 } : (d.ccce ? { tint: 'warn', glow: 0.6, pulse: true } : ok)));
      rules.push(rule('^field-rootfs$', s.roRoot ? ok : { tint: 'warn', glow: 0.5 }));
      rules.push(rule('^field-resources$', s.requestsSet && s.limitsSet ? ok : { tint: 'warn', glow: 0.5 }));
      rules.push(rule('^field-secret$', s.secretRef ? { tint: 'warn', glow: 0.2 } : { tint: 'deny', glow: 0.6, pulse: true }));
      rules.push(rule('^field-image$', s.pinned ? ok : { tint: 'warn', glow: 0.5 }));
      rules.push(rule('^lint-ignore$', s.noIgnore ? { tint: 'muted', glow: 0.05 } : { tint: 'warn', glow: 0.7, pulse: true }));
      rules.push(rule('^manifest-file$', d.findings ? { tint: 'warn', glow: 0.4 } : { tint: 'ok', glow: 0.3 }));
      rules.push(rule('^(kubesec|kubesec-score)$', d.score <= 0 ? { tint: 'deny', glow: 0.6 } : (d.critical.length ? { tint: 'warn', glow: 0.35 } : { tint: 'gold', glow: 0.35 })));
      rules.push(rule('^sim-kubesec-critical$', d.score <= 0 ? { show: true, tint: 'deny', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^(kube-linter|lint-report)$', d.lint.length ? { tint: 'warn', glow: 0.55 } : { tint: 'gold', glow: 0.35 }));
      rules.push(rule('^sim-lint-fail$', d.lint.length ? { show: true, tint: 'deny', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^ci-gate$', !d.gate ? { tint: 'muted', glow: 0.05 } : (d.blocked ? { tint: 'deny', glow: 0.7 } : { tint: 'ok', glow: 0.45 })));
      rules.push(rule('^sim-gate-block$', d.blocked ? { show: true, tint: 'ok', glow: 0.7 } : { hide: true }));
      rules.push(rule('^sim-gate-bypass$', !d.gate && d.findings ? { show: true, tint: 'deny', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^(edge-manifest-kubesec|edge-manifest-linter|edge-scan-gate)$', { tint: 'gold', glow: 0.25 }));
      rules.push(rule('^(edge-gate-api|edge-api-pod)$', d.blocked ? { tint: 'muted', glow: 0.05 } : (d.exposures.length ? { tint: 'deny', glow: 0.6, pulse: true } : { tint: 'ok', glow: 0.35 })));
      rules.push(rule('^payments-pod$', d.exposures.length ? { tint: 'deny', glow: 0.6 } : (d.ccce ? { tint: 'warn', glow: 0.6, pulse: true } : { tint: 'ok', glow: 0.4 })));
      rules.push(rule('^image-layer$', d.imageRoot ? { tint: 'warn', glow: 0.5 } : { tint: 'ok', glow: 0.3 }));
      rules.push(rule('^sim-ccce$', d.ccce ? { show: true, tint: 'warn', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^sim-privileged-flare$', d.exposures.indexOf('privileged-pod-running') >= 0 ? { show: true, tint: 'deny', glow: 0.9, pulse: true } : { hide: true }));
      rules.push(rule('^sim-secret-leak$', d.exposures.indexOf('literal-secret-in-spec') >= 0 ? { show: true, tint: 'deny', glow: 0.8, pulse: true } : { hide: true }));
      rules.push(rule('^(kube-apiserver|git-repo)$', { tint: 'gold', glow: 0.3 }));
      rules.push(rule('^(ci-pipeline|ns-payments)$', { tint: 'muted', glow: 0.05 }));
      var verdict = d.exposures.length ? 'exposed' : (d.gaps.length ? 'degraded' : 'healthy');
      var cap = [];
      cap.push('kubesec: ' + d.kubesecMsg + (d.critical.length ? ' (critical: ' + d.critical.map(function (r) { return r.id + ' ' + r.points; }).join(', ') + ')' : ''));
      cap.push('kube-linter: ' + (d.lint.length ? d.lint.length + ' lint error' + (d.lint.length > 1 ? 's' : '') + ' (' + d.lint.map(function (l) { return l.check; }).join(', ') + ')' : 'no lint errors'));
      cap.push(d.gate ? (d.blocked ? 'CI gate: blocked, previous revision keeps serving' : 'CI gate: green → applied') : (d.findings ? 'CI: || true — findings ignored, applied anyway' : 'CI: || true (nothing to ignore this time)'));
      cap.push('pods: ' + d.podStatus);
      return { verdict: verdict, metrics: d, caption: cap.join(' · '), rules: rules };
    }
  };

  var SIMS = { 'etcd-quorum': etcd, 'aws-az-failure': awsAz, 'iam-eval': iam,
    'netpol-isolation': netpol, 'rbac-authz': rbac, 'sched-taints': sched, 'hpa-scale': hpa,
    'storage-csi': storage, 'ingress-routing': ingress, 'gateway-api': gateway, 'config-propagation': config, 'cni-network': cni,
    'mesh-mtls': mesh, 'control-plane-failure': controlPlane, 'node-troubleshoot': nodeTrouble, 'service-dns': serviceDns,
    'cks-pod-security': cksPodSecurity, 'cks-supply-chain': cksSupplyChain, 'cks-runtime-security': cksRuntimeSecurity, 'cks-cluster-hardening': cksClusterHardening, 'cks-static-analysis': cksStaticAnalysis };

  function get(id) { return SIMS[id] || null; }
  function list() { return Object.keys(SIMS); }
  function merge(a, b) { var o = {}, k; for (k in a) o[k] = a[k]; for (k in (b || {})) o[k] = b[k]; return o; }

  /** Resolve the style for one node name: later rules override earlier ones; sim-* hidden unless shown. */
  function styleFor(nodeName, rules) {
    var st = { hide: /^sim-/.test(nodeName) };
    var hit = false;
    for (var i = 0; i < rules.length; i++) {
      var r = rules[i];
      if (!new RegExp(r.match).test(nodeName)) continue;
      hit = true;
      if (r.show) st.hide = false;
      if (r.hide) st.hide = true;
      if (r.tint) st.tint = r.tint;
      if (r.glow != null) st.glow = r.glow;
      if (r.pulse != null) st.pulse = r.pulse;
    }
    st.matched = hit;
    st.color = st.tint ? TINTS[st.tint] : null;
    return st;
  }

  function isLodNode(name) { return /(_LOD1$|^lod1-)/i.test(name || ''); }

  /** Option display order for one attempt (Fisher–Yates; rnd injectable for tests). Values are original indices. */
  function shuffleOrder(n, rnd) {
    var r = rnd || Math.random, o = [];
    for (var i = 0; i < n; i++) o.push(i);
    for (var j = n - 1; j > 0; j--) { var k = Math.floor(r() * (j + 1)); var t = o[j]; o[j] = o[k]; o[k] = t; }
    return o;
  }

  /** Verdict vocabulary → tone. Every verdict any sim derives must be listed (unit-tested), so a new unsafe
   *  state can never fall through to the healthy styling. Unknown → 'info' (neutral, never 'ok'). */
  var VERDICT_TONE = {
    healthy: 'ok', allow: 'ok',
    degraded: 'warn', 'implicit-deny': 'warn', pending: 'warn', terminating: 'warn', released: 'warn',
    stale: 'warn', 'cert-warning': 'warn', rejected: 'warn',
    down: 'bad', 'explicit-deny': 'bad', 'data-deleted': 'bad', 'exposed-at-rest': 'bad', exposed: 'bad'
  };
  function verdictTone(v) { return Object.prototype.hasOwnProperty.call(VERDICT_TONE, v) ? VERDICT_TONE[v] : 'info'; }

  /** Score a prediction; returns { correct, answer, why }. */
  function scorePredict(simId, scenarioId, choice) {
    var sim = get(simId); if (!sim) return null;
    var sc = null;
    for (var i = 0; i < sim.scenarios.length; i++) if (sim.scenarios[i].id === scenarioId) sc = sim.scenarios[i];
    if (!sc || !sc.predict) return null;
    return { correct: choice === sc.predict.answer, answer: sc.predict.answer, why: sc.predict.why };
  }

  return {
    VERSION: '1.11.0',
    TINTS: TINTS,
    VERDICT_TONE: VERDICT_TONE,
    verdictTone: verdictTone,
    get: get,
    list: list,
    merge: merge,
    styleFor: styleFor,
    isLodNode: isLodNode,
    scorePredict: scorePredict,
    iamDecide: iamDecide,
    awsHa: awsHa,
    etcdQuorum: etcdQuorum,
    netpolDecide: netpolDecide,
    rbacDecide: rbacDecide,
    schedDecide: schedDecide,
    hpaDesired: hpaDesired,
    storageDecide: storageDecide,
    ingressMatch: ingressMatch,
    ingressDecide: ingressDecide,
    gatewayDecide: gatewayDecide,
    configDecide: configDecide,
    cniDecide: cniDecide,
    meshDecide: meshDecide,
    controlPlaneDecide: controlPlaneDecide,
    nodeDecide: nodeDecide,
    serviceDnsDecide: serviceDnsDecide,
    svcDnsResolve: svcDnsResolve,
    cksDecide: cksDecide,
    cksRestrictedViolations: cksRestrictedViolations,
    cksSupplyDecide: cksSupplyDecide,
    SC_DIGEST: SC_DIGEST,
    cksRuntimeDecide: cksRuntimeDecide,
    cksHardenDecide: cksHardenDecide,
    cksStaticDecide: cksStaticDecide,
    SA_POS: SA_POS,
    CH_CHECKS: CH_CHECKS,
    shuffleOrder: shuffleOrder,
    honesty: 'In-browser rules engine over authored glTF. No live cluster, AWS account, or hosted fleet.'
  };
});
