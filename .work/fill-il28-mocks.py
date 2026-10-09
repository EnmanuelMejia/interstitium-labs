#!/usr/bin/env python3
"""Fill il-28: replace the 1 index mockTasks entry with 12 real panel-style choice mock tasks."""
import json, os

P = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses/il-28-devsecops-cloud-infrastructure-mastery.json')
d = json.load(open(P))

def T(i, q, choices, answer, explain):
    return {"id": f"IL28-MOCK-{i:02d}", "type": "choice",
            "q": "Panel question: " + q, "choices": choices,
            "answer": answer, "explain": explain}

TASKS = [
 T(1, "terraform apply fails with 'Error acquiring the state lock'. Your first move?",
    ["Delete the .terraform directory and re-run apply.",
     "Run terraform force-unlock with the lock ID after confirming no other run is active.",
     "Edit the state file directly to remove the lock entry.",
     "Re-run apply with -auto-approve to bypass the lock."],
    1, "State locks prevent concurrent writes. force-unlock is the designed escape hatch \u2014 but only after confirming (CI run list, DynamoDB lease holder) that no real run holds it; otherwise you corrupt state."),
 T(2, "A pod is CrashLoopBackOff. kubectl logs shows 'connection refused' to the database on startup. What do you check before touching the app?",
    ["Increase the container memory limit \u2014 it is probably OOMKilled.",
     "Whether the DB endpoint/DNS resolves and the Service + NetworkPolicy allow the pod's traffic.",
     "Delete the deployment and recreate it from scratch.",
     "Scale the deployment to 5 replicas to absorb the failures."],
    1, "CrashLoopBackOff with connection refused at startup is a dependency/connectivity signal: DNS, Service endpoints, security groups/NetworkPolicies. Fixing the app or scaling first wastes the investigation."),
 T(3, "Your Docker image is 1.2 GB. The single most effective shrink for a compiled Go service?",
    ["Switch the base image from alpine to ubuntu for better caching.",
     "Multi-stage build: compile in a builder stage, copy only the binary into a distroless/scratch final stage.",
     "Add more RUN layers so each step caches independently.",
     "Compress the image with gzip before pushing."],
    1, "Multi-stage builds drop the entire toolchain from the shipped image \u2014 a Go binary plus distroless base is typically under 30 MB. Layer count and base choice are second-order."),
 T(4, "An Ansible playbook reports 'changed' on every run for a config file task. What is wrong?",
    ["Nothing \u2014 Ansible always reports changed for file tasks.",
     "The task is not idempotent: it rewrites the file unconditionally instead of converging to the desired state (e.g., template/copy with proper state).",
     "The inventory file is stale.",
     "Ansible needs --check mode to report correctly."],
    1, "Idempotency is the contract: the same playbook run twice changes nothing the second time. A task that always reports changed is lying about convergence \u2014 usually a shell/command task that should be a template, copy, or lineinfile."),
 T(5, "The Jenkins pipeline is green but deployments silently ship the old artifact. Most likely cause?",
    ["The agent ran out of disk space.",
     "The pipeline builds the artifact but deploys a hardcoded/stale version reference instead of the just-built one.",
     "The Git webhook fired twice.",
     "The pipeline needs more executors."],
    1, "Green-but-stale is the classic version-pinning bug: build produces v2.4.1, deploy step references a static tag or cached artifact. Trace the artifact reference end to end \u2014 the pipeline lied about what it shipped."),
 T(6, "Two VPCs in the same region need private connectivity with no overlap risk. You choose?",
    ["VPC peering \u2014 simplest, non-transitive, fine for two VPCs.",
     "A public subnet with elastic IPs on both sides.",
     "Opening all security groups to 0.0.0.0/0 temporarily.",
     "One NAT gateway shared across both VPCs."],
    0, "VPC peering gives private, non-transitive connectivity between two VPCs with no single point of failure to manage. Transit gateway earns its keep at three or more VPCs; NAT gateways are for outbound internet, not VPC-to-VPC."),
 T(7, "Your SLO is 99.9% over 30 days and the error budget is nearly exhausted with a week left. The right call?",
    ["Freeze all deploys and feature work until the budget recovers \u2014 the budget is the policy.",
     "Lower the SLO to 99% so the budget looks healthy.",
     "Delete the alerting rules generating the errors.",
     "Ship the feature anyway; SLOs are aspirational."],
    0, "The error budget is a policy instrument: exhausted budget means reliability work outranks feature work until it recovers. Changing the SLO to hide the burn is the organizational equivalent of deleting the alert."),
 T(8, "A SAST scan flags a hardcoded API key in the repo history, not just HEAD. The correct response?",
    ["Delete the file in a new commit \u2014 the key is gone from HEAD.",
     "Rotate the key immediately, purge it from history (BFG/filter-repo), and add pre-commit secret scanning so it cannot recur.",
     "Add the key to .gitignore.",
     "Nothing \u2014 the key was only in an old commit."],
    1, "Git history is forever and clonable: deleting from HEAD leaves the secret in every clone. Rotate first (assume compromise), rewrite history, then prevent recurrence with pre-commit hooks and push protection."),
 T(9, "The app needs a database password at runtime in Kubernetes. The least-bad pattern?",
    ["Bake it into the container image as an ENV variable.",
     "Mount it from an external secrets manager (e.g., External Secrets Operator / CSI driver) with RBAC-scoped access and rotation.",
     "Commit it to the Helm values file in the repo.",
     "Pass it as a command-line argument to the pod."],
    1, "Secrets must never live in images, repos, or process args (visible in /proc). The mature pattern: secrets live in a manager, are projected into pods at runtime under RBAC, and rotate without redeploys."),
 T(10, "Prometheus shows p99 latency spiking but the average is flat. What does that tell you?",
     ["Nothing \u2014 averages are the reliable signal.",
      "A small fraction of requests is suffering badly while most are fine \u2014 check the tail: slow dependency, GC pauses, or noisy-neighbor on a subset of pods.",
      "The Prometheus server is misconfigured.",
      "All requests are uniformly slower."],
     1, "Averages hide tails. p99 spiking with a flat mean means a minority of requests is pathological \u2014 the classic signature of a slow downstream, GC stalls, or a degraded subset of instances. Alert on percentiles, not means."),
 T(11, "In the BNY panel simulation you are asked to design a deployment pipeline 'with no copilot'. What are they really testing?",
     ["Whether you memorized Jenkins syntax.",
      "Whether you can reason about the pipeline's stages, gates, artifact promotion, and rollback independently \u2014 design judgment, not tool trivia.",
      "How fast you can type YAML.",
      "Whether you prefer GitHub Actions or Jenkins."],
     1, "Panel simulations test independent mastery: can you decompose the problem (build \u2192 test \u2192 scan \u2192 promote \u2192 deploy \u2192 verify \u2192 roll back), name the gates, and defend the trade-offs without leaning on a tool."),
 T(12, "A supplier's compromised build tool injects code into your dependency chain. Which control would have caught it earliest?",
     ["A longer password policy.",
      "Artifact signing with provenance attestation (SLSA-style) verified at deploy time \u2014 unsigned or mis-attested artifacts never promote.",
      "More frequent standups.",
      "A bigger test suite."],
     1, "Supply-chain attacks defeat perimeter thinking: the artifact itself must carry verifiable provenance. Signed builds + attestation verification at the promotion gate is the control that turns 'trust the pipeline' into 'verify the artifact'."),
]

d['mockTasks'] = TASKS
with open(P, 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write('\n')
d2 = json.load(open(P))
assert len(d2['mockTasks']) == 12
for t in d2['mockTasks']:
    assert set(['id','type','q','choices','answer','explain']) <= set(t.keys()), t['id']
    assert len(t['choices']) == 4
print('validated OK: 12 mockTasks, all choice-type with 4 options')
