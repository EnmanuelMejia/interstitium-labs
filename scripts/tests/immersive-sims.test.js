// Interactive 3D sims (2026-10-06): rules match the documented behaviour; every node a sim addresses exists in its .glb.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const S = require('../../docs/assets/il-immersive-sims.js');

const docs = path.join(__dirname, '..', '..', 'docs');
function glbNodes(rel) {
  const buf = fs.readFileSync(path.join(docs, rel));
  assert.equal(buf.toString('ascii', 0, 4), 'glTF');
  assert.equal(buf.readUInt32LE(4), 2);
  assert.equal(buf.readUInt32LE(8), buf.length);
  const json = JSON.parse(buf.toString('utf8', 20, 20 + buf.readUInt32LE(12)).trim());
  return json.nodes.map(n => n.name);
}

test('etcd quorum follows Raft floor(n/2)+1', () => {
  assert.deepEqual(S.etcdQuorum(3, 3), { quorum: 2, writable: true });
  assert.deepEqual(S.etcdQuorum(3, 2), { quorum: 2, writable: true });
  assert.deepEqual(S.etcdQuorum(3, 1), { quorum: 2, writable: false });
  assert.deepEqual(S.etcdQuorum(5, 3), { quorum: 3, writable: true });
  const sim = S.get('etcd-quorum');
  const leaderLoss = sim.derive({ m0: false, m1: true, m2: true });
  assert.equal(leaderLoss.verdict, 'degraded');
  assert.equal(leaderLoss.metrics.leader, 1, 'a surviving follower is elected');
  assert.equal(sim.derive({ m0: true, m1: false, m2: false }).verdict, 'down');
});

test('AWS Multi-AZ: failover only when Multi-AZ is on and the standby AZ is healthy', () => {
  assert.deepEqual(
    (({ serving, dbWriter, failover, surge }) => ({ serving, dbWriter, failover, surge }))(S.awsHa({ azA: false, azB: true, multiAz: true })),
    { serving: true, dbWriter: 'b', failover: true, surge: 'b' });
  assert.equal(S.awsHa({ azA: false, azB: true, multiAz: false }).serving, false, 'Single-AZ RDS dies with its AZ');
  const bDown = S.awsHa({ azA: true, azB: false, multiAz: true });
  assert.equal(bDown.failover, false); assert.equal(bDown.dbWriter, 'a'); assert.equal(bDown.surge, 'a');
  assert.equal(S.awsHa({ azA: false, azB: false, multiAz: true }).serving, false);
});

test('IAM evaluation order: explicit Deny > SCP > resource grant > identity > boundary > session', () => {
  const base = S.get('iam-eval').initial;
  const d = (o) => S.iamDecide(Object.assign({}, base, o)).decision;
  assert.equal(d({}), 'allow');
  assert.equal(d({ explicitDeny: true, resourceAllow: true }), 'explicit-deny');
  assert.equal(d({ scpAllow: false, resourceAllow: true }), 'implicit-deny', 'SCP caps even resource grants');
  assert.equal(d({ inOrg: false, scpAllow: false }), 'allow', 'SCP gate only applies inside an organization');
  assert.equal(d({ identityAllow: false }), 'implicit-deny');
  assert.equal(d({ identityAllow: false, resourceAllow: true }), 'allow', 'same-account resource policy grant');
  assert.equal(d({ boundarySet: true, boundaryAllow: false }), 'implicit-deny');
  assert.equal(d({ boundarySet: false, boundaryAllow: false }), 'allow', 'no boundary attached → no cap');
  assert.equal(d({ sessionSet: true, sessionAllow: false }), 'implicit-deny');
});

test('every scenario predicts the outcome its own derive() produces, and option 0 is the keyed answer', () => {
  for (const id of S.list()) {
    const sim = S.get(id);
    for (const sc of sim.scenarios) {
      if (!sc.predict) continue;
      assert.ok(sc.predict.options.length >= 2, id + '/' + sc.id);
      assert.equal(S.scorePredict(id, sc.id, sc.predict.answer).correct, true);
      assert.equal(S.scorePredict(id, sc.id, (sc.predict.answer + 1) % sc.predict.options.length).correct, false);
      const out = sim.derive(S.merge(sim.initial, sc.set));
      assert.ok(out.caption && out.rules.length, id + '/' + sc.id + ' derives a scene');
    }
  }
});

test('sim rules only address nodes that exist in the authored, Blender-polished .glb', () => {
  for (const id of S.list()) {
    const sim = S.get(id);
    const names = glbNodes(sim.glb);
    const lod0 = names.filter(n => !S.isLodNode(n));
    assert.ok(names.some(S.isLodNode), sim.glb + ' carries Blender LOD1 duplicates (polish ran)');
    const states = [sim.initial, ...sim.scenarios.map(sc => S.merge(sim.initial, sc.set))];
    for (const st of states) {
      for (const r of sim.derive(st).rules) {
        assert.ok(lod0.some(n => new RegExp(r.match).test(n)), `${id}: rule ${r.match} matches no node in ${sim.glb}`);
      }
    }
  }
});

test('sim-* nodes are hidden by default and revealed only by a show rule', () => {
  assert.equal(S.styleFor('sim-az-b-ec2-surge-0', []).hide, true);
  assert.equal(S.styleFor('sim-az-b-ec2-surge-0', [{ match: '^sim-az-b-', show: true }]).hide, false);
  assert.equal(S.styleFor('az-a-ec2-0', []).hide, false);
  const aws = S.get('aws-az-failure');
  const st = aws.derive(S.merge(aws.initial, { azA: false }));
  assert.equal(S.styleFor('sim-az-b-ec2-surge-1', st.rules).hide, false);
  assert.equal(S.styleFor('sim-az-a-ec2-surge-1', st.rules).hide, true);
});

test('all immersive .glb assets are valid glTF 2.0 binaries with in-range indices', () => {
  const dir = path.join(docs, 'assets', 'immersive');
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.glb') && !/\.(polished|kit-v2\.bak)\.glb$/.test(f));
  assert.ok(files.length >= 19);
  for (const f of files) {
    const buf = fs.readFileSync(path.join(dir, f));
    assert.equal(buf.toString('ascii', 0, 4), 'glTF', f);
    assert.equal(buf.readUInt32LE(8), buf.length, f + ' length header');
    const jl = buf.readUInt32LE(12);
    assert.equal(buf.toString('ascii', 16, 20), 'JSON');
    const json = JSON.parse(buf.toString('utf8', 20, 20 + jl).trim());
    const binOff = 20 + jl;
    const binLen = buf.readUInt32LE(binOff);
    assert.equal(buf.toString('ascii', binOff + 4, binOff + 7), 'BIN');
    const bin = buf.subarray(binOff + 8, binOff + 8 + binLen);
    for (const m of json.meshes) for (const p of m.primitives) {
      const pos = json.accessors[p.attributes.POSITION];
      assert.ok(pos && pos.count > 0, f + ' POSITION');
      if (p.indices != null) {
        const acc = json.accessors[p.indices];
        const view = json.bufferViews[acc.bufferView];
        const off = (view.byteOffset || 0) + (acc.byteOffset || 0);
        const size = acc.componentType === 5125 ? 4 : acc.componentType === 5123 ? 2 : 1;
        assert.ok(off + acc.count * size <= bin.length, f + ' index view in BIN');
        let max = 0;
        for (let i = 0; i < acc.count; i++) {
          const v = size === 4 ? bin.readUInt32LE(off + i * 4) : size === 2 ? bin.readUInt16LE(off + i * 2) : bin[off + i];
          if (v > max) max = v;
        }
        assert.ok(max < pos.count, `${f} ${m.name}: index ${max} >= vertex count ${pos.count}`);
      }
    }
  }
});

// 2026-10-07: four more CKA sims over existing Blender-polished glTF + shuffled predict options.
test('NetworkPolicy: isolation needs a selecting policy AND an enforcing CNI; rules are additive allow-lists', () => {
  const sim = S.get('netpol-isolation');
  const d = (o) => S.netpolDecide(S.merge(sim.initial, o));
  assert.deepEqual((({ frontend, untrusted, dns }) => ({ frontend, untrusted, dns }))(d({})), { frontend: true, untrusted: false, dns: true });
  assert.equal(d({ ruleFrontend: false }).frontend, false, 'no matching ingress rule = default deny');
  assert.equal(d({ policy: false }).untrusted, true, 'no policy selects the pod → non-isolated');
  assert.equal(d({ cniEnforces: false }).untrusted, true, 'flannel silently ignores NetworkPolicy');
  assert.equal(d({ egressIsolated: true, ruleDns: false }).dns, false, 'egress isolation blocks DNS unless allowed');
  assert.equal(d({ egressIsolated: false, ruleDns: false }).dns, true, 'no Egress policyType → egress not isolated');
  assert.equal(sim.derive(S.merge(sim.initial, { cniEnforces: false })).verdict, 'down');
});

test('RBAC: binding kind decides scope; RoleBinding→ClusterRole never grants cluster-scoped nodes', () => {
  const sim = S.get('rbac-authz');
  const d = (o) => S.rbacDecide(S.merge(sim.initial, o));
  assert.equal(d({}).ciNodes, false);
  assert.equal(d({}).ciDeploys, true);
  assert.equal(d({ sameNs: false }).ciDeploys, false, 'RoleBinding in dev does not reach prod');
  assert.equal(d({ b2Cluster: true, sameNs: false }).ciDeploys, true);
  assert.equal(d({ b2Cluster: true }).ciNodes, true);
  assert.equal(d({ sameNs: false }).alicePods, false);
  assert.equal(d({ b1: false }).bobSecrets, false, 'additive only: no binding, no permission');
  assert.equal(sim.derive(S.merge(sim.initial, { b0: false, b1: false, b2: false })).verdict, 'implicit-deny');
});

test('Scheduler: taints filter even when affinity matches; tolerations allow but do not attract; cordon spares running pods', () => {
  const sim = S.get('sched-taints');
  const d = (o) => S.schedDecide(S.merge(sim.initial, o));
  assert.equal(d({}).db, null, 'no nvme node → Pending');
  assert.equal(d({ cNvme: true, cTaint: true }).db, null, 'NoExecute taint still filters node-c');
  assert.equal(d({ cNvme: true, cTaint: false }).db, 'c');
  assert.equal(d({}).trainer, 'b');
  assert.equal(d({ trainerTol: false }).trainer, 'a', 'gpu taint repels; preference cannot override');
  const cordoned = d({ aCordoned: true });
  assert.equal(cordoned.webRunning, 'a'); assert.equal(cordoned.webNewReplica, null);
});

test('HPA: autoscaling/v2 ceil formula, 10% tolerance, clamp to [min,max], hold without metrics', () => {
  assert.equal(S.hpaDesired(2, 120, 50, 2, 5), 5);
  assert.equal(S.hpaDesired(2, 120, 50, 2, 3), 3);
  assert.equal(S.hpaDesired(2, 40, 50, 2, 5), 2, 'minReplicas floor');
  assert.equal(S.hpaDesired(4, 54, 50, 1, 10), 4, 'inside 10% tolerance → no change');
  assert.equal(S.hpaDesired(4, 60, 50, 1, 10), 5, 'ceil(4.8)');
  const sim = S.get('hpa-scale');
  const out = (o) => sim.derive(S.merge(sim.initial, o));
  assert.equal(out({ spike: true }).metrics.desired, 5);
  assert.equal(out({ spike: true, max5: false }).verdict, 'degraded');
  assert.equal(out({ spike: true, requestsSet: false }).metrics.desired, 2);
  assert.equal(out({ spike: true, metricsUp: false }).verdict, 'down');
  assert.equal(S.styleFor('replica-4', out({ spike: true }).rules).hide, false);
  assert.equal(S.styleFor('replica-4', out({}).rules).hide, true);
});

test('predict options shuffle per attempt but stay a permutation of original indices', () => {
  let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  const seen = new Set();
  for (let i = 0; i < 40; i++) {
    const o = S.shuffleOrder(3, rnd);
    assert.deepEqual([...o].sort(), [0, 1, 2]);
    seen.add(o.indexOf(0));
  }
  assert.equal(seen.size, 3, 'keyed answer appears in every position across attempts');
  assert.ok(S.list().length >= 7);
});
