#!/usr/bin/env python3
"""W6: re-animate 4 legacy static diagrams from earlier batches (in place)."""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/apex-audit/.work/inline-diagrams"))
from diag_framework import Diagram

BASE = os.path.expanduser("~/workspace/cert-bootcamps/site/bootcamps")

def save(slug, fname, d):
    d.animate()
    svg = d.render_svg()
    assert "il-anim" in svg and "@keyframes il-pop" in svg
    open(os.path.join(BASE, slug, "assets", "diagrams", fname), "w").write(svg)

# 1. kubernetes-sre: reliability practice loop
d = Diagram()
d.flow([("Define SLO", "target"), ("Measure SLIs", "signals"),
        ("Spend budget", "deliberately"), ("Respond", "incidents"),
        ("Improve", "iterate")], box_w=112, gap=22)
save("kubernetes-sre", "kubernetes-sre-d2.svg", d)

# 2. k8s-cka-exceed: six hardening layers (bottom-up)
d = Diagram()
d.layers([("Runtime detection", "Falco / audit logs"),
          ("Sealed secrets", "encrypted at rest"),
          ("RBAC", "least privilege"),
          ("Network policy", "deny by default"),
          ("Pod security", "standards enforced"),
          ("Trusted images", "signed & scanned")])
save("k8s-cka-exceed", "k8s-cka-exceed-d2.svg", d)

# 3. iac-terraform-gitops: ArgoCD push-to-healthy
d = Diagram()
d.flow([("Push to git", "commit"), ("ArgoCD syncs", "desired state"),
        ("K8s reconciles", "controllers"), ("Health gates", "checks"),
        ("Rollback", "git revert")], box_w=112, gap=22)
save("iac-terraform-gitops", "iac-terraform-gitops-d2.svg", d)

# 4. devops-zero-to-hire: infinity loop plan->monitor
d = Diagram()
d.flow([("Plan", ""), ("Code", ""), ("Build", ""), ("Test", ""),
        ("Release", ""), ("Deploy", ""), ("Operate", ""), ("Monitor", "")],
       box_w=70, gap=14)
save("devops-zero-to-hire", "devops-zero-to-hire-d2.svg", d)

# update alt text on the 4 media entries
for slug, fname, mid in [
    ("kubernetes-sre", "kubernetes-sre-d2.svg", "kubernetes-sre-d2"),
    ("k8s-cka-exceed", "k8s-cka-exceed-d2.svg", "k8s-cka-exceed-d2"),
    ("iac-terraform-gitops", "iac-terraform-gitops-d2.svg", "iac-terraform-gitops-d2"),
    ("devops-zero-to-hire", "devops-zero-to-hire-d2.svg", "devops-zero-to-hire-d2"),
]:
    p = os.path.join(BASE, slug, "content.json")
    data = json.load(open(p))
    for m in data["media"]:
        if m.get("id") == mid:
            m["alt"] = f"Animated diagram: {m.get('title', '')}."
    tmp = p + ".w6tmp"
    json.dump(data, open(tmp, "w"), ensure_ascii=False, indent=2)
    json.load(open(tmp))
    os.replace(tmp, p)
    print("animated:", slug, fname)
