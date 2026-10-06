/**
 * IL Immersive Sims v1.0.0 (2026-10-06) — interactive state machines that drive authored .glb scenes.
 *
 * State changes the scene: each sim derives per-node styles (tint / glow / pulse / hide / reveal)
 * from a small state object using the documented rules (Raft quorum, AWS Multi-AZ failover,
 * AWS IAM policy evaluation). Predict-then-reveal checkpoints record correctness + latency.
 *
 * Honest scope: rules are computed in the browser. No live cluster, no AWS account, no hosted fleet.
 * Pure + UMD so `node --test` exercises the same logic the browser runs.
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

  var SIMS = { 'etcd-quorum': etcd, 'aws-az-failure': awsAz, 'iam-eval': iam };

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

  /** Score a prediction; returns { correct, answer, why }. */
  function scorePredict(simId, scenarioId, choice) {
    var sim = get(simId); if (!sim) return null;
    var sc = null;
    for (var i = 0; i < sim.scenarios.length; i++) if (sim.scenarios[i].id === scenarioId) sc = sim.scenarios[i];
    if (!sc || !sc.predict) return null;
    return { correct: choice === sc.predict.answer, answer: sc.predict.answer, why: sc.predict.why };
  }

  return {
    VERSION: '1.0.0',
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
    honesty: 'In-browser rules engine over authored glTF. No live cluster, AWS account, or hosted fleet.'
  };
});
