/**
 * IL Immersive Sims v1.1.0 (2026-10-07; v1.0.0 2026-10-06) — interactive state machines that drive authored .glb scenes.
 *
 * State changes the scene: each sim derives per-node styles (tint / glow / pulse / hide / reveal)
 * from a small state object using the documented rules (Raft quorum, AWS Multi-AZ failover,
 * AWS IAM policy evaluation, NetworkPolicy isolation, RBAC binding scope, scheduler filter/score,
 * HPA autoscaling/v2 math). Option order is shuffled per attempt so the keyed answer is not positional. Predict-then-reveal checkpoints record correctness + latency.
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

  var SIMS = { 'etcd-quorum': etcd, 'aws-az-failure': awsAz, 'iam-eval': iam,
    'netpol-isolation': netpol, 'rbac-authz': rbac, 'sched-taints': sched, 'hpa-scale': hpa };

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
    VERSION: '1.1.0',
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
    shuffleOrder: shuffleOrder,
    honesty: 'In-browser rules engine over authored glTF. No live cluster, AWS account, or hosted fleet.'
  };
});
