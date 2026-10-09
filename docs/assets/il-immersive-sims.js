/**
 * IL Immersive Sims v1.2.0 (2026-10-08; v1.1.0 2026-10-07; v1.0.0 2026-10-06) — interactive state machines that drive authored .glb scenes.
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
      rules.push(rule('^(backend-disk|platter)-1$', d.disk1 === 'kept' ? { tint: 'gold', glow: 0.3 } : (d.disk1 === 'deleted' ? { tint: 'deny', glow: 0.5, pulse: true } : { hide: true })));
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

  var SIMS = { 'etcd-quorum': etcd, 'aws-az-failure': awsAz, 'iam-eval': iam,
    'netpol-isolation': netpol, 'rbac-authz': rbac, 'sched-taints': sched, 'hpa-scale': hpa,
    'storage-csi': storage, 'ingress-routing': ingress, 'config-propagation': config, 'cni-network': cni,
    'mesh-mtls': mesh, 'control-plane-failure': controlPlane };

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

  /** Score a prediction; returns { correct, answer, why }. */
  function scorePredict(simId, scenarioId, choice) {
    var sim = get(simId); if (!sim) return null;
    var sc = null;
    for (var i = 0; i < sim.scenarios.length; i++) if (sim.scenarios[i].id === scenarioId) sc = sim.scenarios[i];
    if (!sc || !sc.predict) return null;
    return { correct: choice === sc.predict.answer, answer: sc.predict.answer, why: sc.predict.why };
  }

  return {
    VERSION: '1.2.0',
    TINTS: TINTS,
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
    configDecide: configDecide,
    cniDecide: cniDecide,
    meshDecide: meshDecide,
    controlPlaneDecide: controlPlaneDecide,
    shuffleOrder: shuffleOrder,
    honesty: 'In-browser rules engine over authored glTF. No live cluster, AWS account, or hosted fleet.'
  };
});
