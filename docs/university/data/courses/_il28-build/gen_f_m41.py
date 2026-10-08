#!/usr/bin/env python3
"""Build IL28-M41 module object -> part_f_m41.json"""
import json

notes = [
{"title": "Why Multiple Node Pools Beat One Giant Pool",
"body": "An AKS node pool is a group of nodes that share the same VM size, OS, and scaling configuration. Every cluster starts with at least one system node pool (which runs kube-system pods like CoreDNS and metrics-server) plus one or more user node pools for your workloads. The panel question is direct: what is the benefit of multiple pools versus one giant pool? First, blast radius and upgrade safety: you can cordon, drain, and upgrade one pool at a time instead of rolling the entire fleet at once. Second, heterogeneous hardware: GPU workloads, memory-heavy caches, and cheap spot VMs cannot share one VM SKU, so each gets its own pool. Third, scaling independence: the cluster autoscaler scales each pool against its own min/max, so a batch queue bursting at night never steals capacity planning from the latency-sensitive API pool. Fourth, cost: you can run steady workloads on reserved/priced VMs in one pool and elastic overflow on spot in another. Worked example: design pools for a payments API with steady traffic plus a nightly reconciliation batch. Solution: (1) system pool: 3 x Standard_D4s_v5, autoscaler disabled, min=max=3 for control-plane-adjacent stability; (2) user pool 'apipool': Standard_D8s_v5, min 4 max 20 with autoscaler, taint-free so API pods schedule freely; (3) user pool 'batchpool': spot VMs, min 0 max 30, tainted spot=true:NoSchedule so only batch jobs with the matching toleration land there. One giant pool forces a single VM size, a single upgrade blast radius, and a single scaling policy — three compromises you never need to accept."},
{"title": "How the Cluster Autoscaler Thinks",
"body": "The cluster autoscaler watches for pods that cannot be scheduled and adds nodes; it watches for underutilized nodes and removes them. Scale-up triggers when a pod stays Pending because no existing node has room — the autoscaler simulates scheduling, picks the pool that fits, and calls the Azure API to grow that pool, bounded by --max-count. Scale-down is conservative: a node becomes eligible only after all its pods can move elsewhere and it has been underutilized (default under 50% requested resources) for about 10 minutes, and it never removes nodes running kube-system pods it cannot evict. Two limits shape every design. First, max pods per node: with Azure CNI each pod consumes a VNet IP, so a Standard_D4s_v5 node might cap at 30 pods; with Azure CNI Overlay, pods use overlay IPs and the cap rises toward 250. Second, the pool's min/max counts are hard ceilings the autoscaler will not cross. Worked example: your API needs 120 pod replicas, each requesting 0.5 CPU, on D8s_v5 nodes (8 vCPUs, 30-pod cap with Azure CNI). CPU math: 120 x 0.5 = 60 vCPUs / 8 per node = 7.5, so 8 nodes by CPU. Pod-count math: 120 / 30 = 4 nodes. The binding constraint is CPU: 8 nodes. Solution: set the pool to min 4 (steady state) and max 12 (headroom for the burst plus rolling-update surge), and let the autoscaler float between them; a max of 8 would deadlock a rolling update that temporarily needs extra nodes."},
{"title": "Manual Scaling: az aks nodepool scale and update",
"body": "The panel asks how to manually increase the maximum nodes per pool, and the answer is the Azure CLI, not the portal. To change the live node count immediately: az aks nodepool scale --resource-group myRG --cluster-name myAKS --name apipool --node-count 8. To change the autoscaler's bounds: az aks nodepool update --resource-group myRG --cluster-name myAKS --name apipool --enable-cluster-autoscaler --min-count 4 --max-count 20. To disable the autoscaler and pin a count: az aks nodepool update --resource-group myRG --cluster-name myAKS --name apipool --disable-cluster-autoscaler followed by a scale command. Know the precedence: a manual scale sets node-count inside the min/max window; if the autoscaler is enabled it may scale back down within minutes, so pinning the count without disabling the autoscaler is a classic exam trap. Worked example: on-call at 2 AM, pods are Pending with 'Insufficient cpu', and the pool shows max-count 6 with 6 nodes running. The autoscaler cannot help — it is already at its ceiling. Solution: run az aks nodepool update with --max-count 12 (keep --min-count as-is), then watch kubectl get nodes; within a few minutes new nodes join and Pending pods schedule. If instead the pool had 3 nodes against a max of 12 and pods were still Pending, raising the ceiling would do nothing — the problem is elsewhere (quotas, taints, or subnet IPs), which is exactly the triage in the next note."},
{"title": "Pod Stuck in Pending: The Triage Runbook",
"body": "A pod in Pending means the scheduler could not place it. Start with kubectl describe pod <name> and read the Events section — the FailedScheduling message names the cause: 'Insufficient cpu', 'Insufficient memory', or 'didn't match pod affinity'. If it says insufficient resources, the panel's follow-up is 'out of nodes — how do you fix it?': raise the pool's max count (previous note) and confirm the autoscaler has room. When new nodes still do not appear, walk the full triage checklist the panel expects: (1) cluster autoscaler logs — is it even attempting scale-up? (2) Azure subscription quotas — vCPU quota per region and per VM family; (3) region capacity — the SKU may be unavailable in that zone; (4) taints and tolerations — nodes exist but pods cannot tolerate their taints; (5) labels and node selectors — a nodeSelector pointing at a label no node carries; (6) service principal / managed identity permissions — the cluster identity cannot create VMs; (7) Azure Activity log — failed VM creation operations with error codes; (8) Azure Monitor / Resource Health — platform issues; (9) subnet IP space — with Azure CNI, no free IPs means no new nodes; (10) VM SKU restrictions — policy or subscription blocks the SKU; (11) Azure Policy assignments denying the deployment; (12) max pods per node already saturated. Worked example: describe shows '0/5 nodes are available: 5 Insufficient cpu', the pool is at max-count 6/6, and the Activity log shows a failed deployment with error 'OperationNotAllowed - quota exceeded'. Solution: quota is the blocker — request a vCPU quota increase for that VM family in that region, then raise max-count. Scaling commands cannot fix a quota denial."},
{"title": "Taints, Tolerations, and Labels: The Scheduling Vocabulary",
"body": "Labels, taints, and tolerations are three different scheduling controls and the panel asks you to distinguish them. Labels are key/value metadata on nodes and pods used for selection: kubectl label nodes node1 workload=api, then a pod's nodeSelector: {workload: api} restricts it to matching nodes. Labels attract; they never repel. Taints repel: kubectl taint nodes node1 sku=gpu:NoSchedule marks the node so only pods that tolerate the taint may schedule there. The three effects are NoSchedule (new pods blocked), PreferNoSchedule (soft preference), and NoExecute (existing pods evicted too — used for node problems like disk pressure). Tolerations are the pod-side opt-in, declared in the pod spec: tolerations: [{key: sku, operator: Equal, value: gpu, effect: NoSchedule}]. A common production pattern is tainting the system pool so user workloads can never land on it: kubectl taint nodes -l kubernetes.azure.com/mode=system CriticalAddonsOnly=true:NoSchedule. Worked example: GPU nodes sit idle while GPU pods stay Pending with 'didn't match toleration'. Solution: the nodes were tainted sku=gpu:NoSchedule but the deployment lacks the toleration — add the toleration block above to the pod template, or remove the taint if GPU isolation is no longer needed. Remember the asymmetry the panel probes: a pod without a toleration can never schedule on a tainted node, but a pod with a toleration may still schedule on untainted nodes — tolerations permit, they do not require."},
{"title": "Application Gateway Ingress: L7 Traffic into AKS",
"body": "The panel asks about exposing Kubernetes endpoints through Application Gateway and how it differs from a Load Balancer. An Azure Load Balancer operates at Layer 4 (TCP/UDP): it forwards packets to backend IPs without understanding HTTP. Application Gateway operates at Layer 7: it terminates TLS, reads HTTP hostnames and paths, and routes to different backend pools — exactly what an Ingress controller needs. The Azure Application Gateway Ingress Controller (AGIC) runs as a pod in your cluster, watches Ingress resources, and programs the Application Gateway accordingly, so developers declare routing in YAML and AGIC translates it to gateway config. Traffic flow for a browser request: DNS resolves your hostname to the Application Gateway's public IP, the gateway terminates TLS and matches the host/path rule, then forwards to the AKS nodes' backend pool, where kube-proxy routes to the pod. Worked example: expose shop.example.com/api to the api service and shop.example.com/ to the web service. Solution — an Ingress with the annotation kubernetes.io/ingress.class: azure/application-gateway and rules: [{host: shop.example.com, http: {paths: [{path: /api/*, backend: {service: {name: api, port: {number: 80}}}}, {path: /*, backend: {service: {name: web, port: {number: 80}}}]}}]. Add the WAF tier (WAF_v2) on the gateway for OWASP rule protection at the edge. Know the contrast cold: need raw TCP passthrough or ultra-low latency? Load Balancer (L4). Need host/path routing, TLS termination, or WAF? Application Gateway (L7)."},
]

cards = [
{"front": "Command to manually set an AKS node pool to 8 nodes", "back": "az aks nodepool scale --resource-group myRG --cluster-name myAKS --name <pool> --node-count 8"},
{"front": "Command to raise an AKS pool's autoscaler ceiling to 20 nodes", "back": "az aks nodepool update -g myRG --cluster-name myAKS -n <pool> --enable-cluster-autoscaler --min-count 4 --max-count 20"},
{"front": "First kubectl command when a pod is stuck in Pending", "back": "kubectl describe pod <name> — read the Events section for the FailedScheduling reason (Insufficient cpu/memory, affinity mismatch)"},
{"front": "Benefit of multiple node pools vs one giant pool (panel answer)", "back": "Separate VM SKUs per workload, independent autoscaler min/max, smaller upgrade blast radius, cost mixing (spot vs regular), and workload isolation"},
{"front": "Difference between a taint and a label", "back": "Labels attract via selectors; taints repel — only pods with a matching toleration can schedule on a tainted node"},
{"front": "The three taint effects", "back": "NoSchedule (blocks new pods), PreferNoSchedule (soft), NoExecute (evicts existing pods too)"},
{"front": "Application Gateway vs Azure Load Balancer (panel answer)", "back": "App Gateway is Layer 7 (HTTP routing, TLS termination, WAF); Load Balancer is Layer 4 (TCP/UDP forwarding)"},
{"front": "What AGIC does", "back": "Application Gateway Ingress Controller: a pod that watches Kubernetes Ingress resources and programs the Azure Application Gateway"},
{"front": "Browser-to-pod traffic flow through App Gateway", "back": "DNS -> Application Gateway public IP -> TLS termination + host/path routing -> AKS backend pool -> kube-proxy -> pod"},
{"front": "Why the autoscaler may not add nodes despite Pending pods", "back": "Pool already at --max-count; vCPU quota exhausted; region/SKU capacity; subnet IP exhaustion (Azure CNI); Azure Policy denial; identity lacking VM-create permission"},
{"front": "kubectl command to taint GPU nodes so only GPU pods schedule there", "back": "kubectl taint nodes -l sku=gpu sku=gpu:NoSchedule (pods then need a matching toleration)"},
{"front": "What 'Insufficient cpu' in FailedScheduling really means", "back": "No node has enough unallocated CPU for the pod's requests — fix by scaling the pool, lowering requests, or freeing capacity, not by raising limits"},
]

quiz = [
{"q": "A payments API (steady) and a nightly batch job (bursty, fault-tolerant) share one giant AKS node pool. What is the strongest reason to split them into two pools?",
"choices": ["Two pools double the Kubernetes version", "Independent autoscaler min/max and VM SKUs let the batch pool use spot VMs at min 0 while the API pool stays stable", "Node pools are required for kubectl to work", "A single pool cannot exceed 3 nodes"],
"answer": 1,
"explain": "Separate pools give each workload its own VM SKU, scaling bounds, and upgrade blast radius — the batch pool can run cheap spot VMs scaled to zero while the API pool holds steady capacity."},
{"q": "Pods are Pending with 'Insufficient cpu'. The pool shows 6/6 nodes and max-count is 6. What is the correct first fix?",
"choices": ["Delete the Pending pods", "Raise the pool's max-count with az aks nodepool update", "Restart kubelet on every node", "Increase the pods' CPU limits"],
"answer": 1,
"explain": "The autoscaler is already at its ceiling, so it cannot add nodes. Raising --max-count gives it room; deleting pods or raising limits does not create capacity."},
{"q": "After raising max-count, still no new nodes appear. The Azure Activity log shows 'OperationNotAllowed' quota errors. What is the blocker?",
"choices": ["The cluster autoscaler is disabled", "Subscription vCPU quota for that VM family/region is exhausted", "Pods lack tolerations", "CoreDNS is down"],
"answer": 1,
"explain": "OperationNotAllowed quota errors mean Azure refused the VM creation — no CLI scaling command can fix this; you must request a quota increase, then scale."},
{"q": "Which kubectl command applies a repelling mark so that only specially-marked pods schedule on GPU nodes?",
"choices": ["kubectl label nodes -l sku=gpu sku=gpu:NoSchedule", "kubectl taint nodes -l sku=gpu sku=gpu:NoSchedule", "kubectl cordon -l sku=gpu", "kubectl annotate nodes -l sku=gpu taint=gpu"],
"answer": 1,
"explain": "kubectl taint with effect NoSchedule repels pods; only pods declaring a matching toleration may schedule there. Labels attract, cordon blocks all scheduling."},
{"q": "A pod spec has nodeSelector {workload: api} but stays Pending although nodes exist. What should you check first?",
"choices": ["Whether any node actually carries the label workload=api", "The container image tag", "The cluster's DNS suffix", "The Azure subscription ID"],
"answer": 0,
"explain": "nodeSelector only matches nodes carrying that exact label; a typo'd or missing label is the classic cause. Verify with kubectl get nodes -l workload=api."},
{"q": "Why choose Application Gateway over Azure Load Balancer for exposing a web app on AKS?",
"choices": ["It is always cheaper", "Layer 7 routing: host/path rules, TLS termination, and WAF at the edge", "It replaces kube-proxy", "It works without any Ingress resource"],
"answer": 1,
"explain": "App Gateway understands HTTP — host/path routing, TLS termination, WAF — while a Load Balancer only forwards TCP/UDP (L4). AGIC still needs Ingress resources to program it."},
{"q": "What does AGIC do in an AKS cluster?",
"choices": ["It replaces the cluster autoscaler", "It watches Ingress resources and configures the Azure Application Gateway", "It issues TLS certificates from Azure Key Vault", "It snapshots etcd"],
"answer": 1,
"explain": "The Application Gateway Ingress Controller runs in-cluster, watches Ingress objects, and translates them into Application Gateway backend pools, listeners, and routing rules."},
{"q": "The autoscaler removed a node 12 minutes after it became idle, killing a long-running batch pod. Which behavior explains this?",
"choices": ["Scale-down of underutilized nodes after the ~10-minute delay; batch pods need protection via PodDisruptionBudgets or dedicated tainted pools", "A Kubernetes bug", "The node ran out of disk", "AGIC deleted the node"],
"answer": 0,
"explain": "Scale-down evicts moveable pods after roughly 10 minutes of underutilization. Long-running or stateful work belongs on protected/dedicated pools, not mixed with elastic capacity."},
{"q": "With Azure CNI, new nodes fail to join and the subnet shows no free IPs. What is happening?",
"choices": ["The VNet peering is misconfigured", "Each pod consumes a VNet IP, so IP exhaustion blocks node provisioning — expand the subnet or switch to Overlay", "The nodes need bigger OS disks", "AGIC is blocking the nodes"],
"answer": 1,
"explain": "Azure CNI assigns real VNet IPs to pods, so a full subnet stops both pod scheduling and node joins. Overlay mode avoids this by using overlay IPs."},
]

drills = [
{"id": "il28-m41-nodepool-decisions", "title": "Timed drill: node pool and autoscaler decisions",
"items": [
{"prompt": "90 seconds: state the benefit of multiple node pools vs one giant pool.", "answer": "Independent VM SKUs, autoscaler min/max per pool, smaller upgrade blast radius, cost mixing (spot vs on-demand), workload isolation.",
"explain": "Hit all five: SKUs, scaling bounds, blast radius, cost, isolation. The panel wants the contrast, not just a definition."},
{"prompt": "Command: set pool 'apipool' to exactly 8 nodes right now.", "answer": "az aks nodepool scale --resource-group myRG --cluster-name myAKS --name apipool --node-count 8",
"explain": "scale sets the live count. If the autoscaler is enabled it may drift back — disable it first for a pinned count."},
{"prompt": "Command: enable the autoscaler on 'apipool' with min 3, max 15.", "answer": "az aks nodepool update --resource-group myRG --cluster-name myAKS --name apipool --enable-cluster-autoscaler --min-count 3 --max-count 15",
"explain": "update changes configuration; scale changes the live count. Mixing them up is the classic panel trap."},
{"prompt": "Pods Pending 'Insufficient memory', pool at 5/5 nodes, max-count 5. Fix?", "answer": "Raise the ceiling: az aks nodepool update ... --max-count <higher> (keep min). The autoscaler is capped.",
"explain": "The autoscaler cannot exceed max-count. Raising it is the fix — but verify quota first if Activity log shows denials."},
{"prompt": "Max-count raised, still no nodes; Activity log shows quota 'OperationNotAllowed'. Next step?", "answer": "Request a vCPU quota increase for that VM family in that region, then confirm nodes join.",
"explain": "Quota denials come from Azure policy on the subscription, not from Kubernetes — only a quota increase unblocks it."},
{"prompt": "Why taint the system node pool?", "answer": "So user workloads can never schedule on nodes running CoreDNS/metrics-server — e.g. taint CriticalAddonsOnly=true:NoSchedule.",
"explain": "Protects cluster-critical pods from noisy neighbors and from scale-down eviction pressure."},
{"prompt": "Toleration vs nodeSelector: which one permits scheduling on a tainted node?", "answer": "Toleration. nodeSelector only attracts to labels; it cannot overcome a taint.",
"explain": "Tolerations permit, never require; labels attract, never repel. Say the asymmetry explicitly."},
]},
{"id": "il28-m41-pending-triage", "title": "Timed drill: Pending-pod triage from events",
"items": [
{"prompt": "Event: '0/4 nodes are available: 4 Insufficient cpu'. Pool 4/4, max 4. Diagnosis and fix?", "answer": "Scheduler found no CPU headroom and the pool is at its autoscaler ceiling. Fix: az aks nodepool update --max-count higher.",
"explain": "Read the two facts together: insufficient CPU + at ceiling = raise the ceiling. Either fact alone changes the answer."},
{"prompt": "Event: 'didn't match pod affinity/anti-affinity'. What do you check?", "answer": "The pod's affinity rules vs actual node labels — kubectl get nodes --show-labels; fix the rule or label the nodes.",
"explain": "Affinity mismatch is a label problem, not a capacity problem. Scaling never fixes it."},
{"prompt": "Nodes exist with free CPU but the pod has nodeSelector {gpu: 'true'} and stays Pending. Cause?", "answer": "No node carries label gpu=true. Add the label or correct the selector.",
"explain": "nodeSelector is exact-match. Verify with kubectl get nodes -l gpu=true — empty result confirms it."},
{"prompt": "GPU nodes are Ready but GPU pods report 'toleration not matched'. Fix?", "answer": "Add the matching toleration to the pod template, or remove the NoSchedule taint from the nodes.",
"explain": "Taint without toleration = Pending forever. The toleration key/value/effect must match the taint exactly."},
{"prompt": "New nodes fail: subnet has 0 free IPs, Azure CNI in use. Two remedies?", "answer": "Expand the subnet address space, or migrate the pool to Azure CNI Overlay so pods stop consuming VNet IPs.",
"explain": "Azure CNI burns one VNet IP per pod — IP exhaustion blocks node joins entirely."},
{"prompt": "Name three non-Kubernetes places to check when nodes will not provision.", "answer": "Azure Activity log (failed operations), subscription vCPU quotas, Azure Policy assignments (deny rules).",
"explain": "The panel's 'new nodes still not deploying' checklist lives half outside Kubernetes — say these three first, then region capacity, SKU restrictions, identity permissions."},
{"prompt": "Pod was Running, then suddenly restarts with no code change. Which probe do you suspect and what command confirms the reason?", "answer": "Suspect the liveness probe (it restarts containers). Confirm with kubectl describe pod — check Last State: Terminated, Reason, and Exit Code.",
"explain": "Liveness failures trigger restarts; readiness only removes from service. describe shows lastState.terminated.reason (e.g. OOMKilled, Error) and exit code."},
]},
]

handsOnLab = {
"id": "il28-m41-lab",
"title": "Lab: multi-pool AKS with autoscaling and App Gateway ingress",
"brief": "You will provision an AKS cluster with separate system and user node pools, enable the cluster autoscaler, deploy the Application Gateway Ingress Controller, expose a sample app through host/path routing, and practice the Pending-pod triage commands. Estimated cloud cost is a few dollars if you delete the resource group the same day.",
"steps": [
"Create the resource group and a virtual network with two subnets: az group create -n rg-il28-m41 -l eastus; az network vnet create -g rg-il28-m41 -n vnet-m41 --address-prefix 10.0.0.0/16 --subnet-name aks-subnet --subnet-prefix 10.0.0.0/20; az network vnet subnet create -g rg-il28-m41 --vnet-name vnet-m41 -n appgw-subnet --address-prefix 10.0.16.0/24.",
"Create the AKS cluster with a system pool only: az aks create -g rg-il28-m41 -n aks-m41 --node-count 3 --node-vm-size Standard_D4s_v5 --vnet-subnet-id <aks-subnet-id> --network-plugin azure. Record the system pool name with az aks nodepool list.",
"Add a user pool with the autoscaler: az aks nodepool add -g rg-il28-m41 --cluster-name aks-m41 -n apipool --node-count 2 --node-vm-size Standard_D8s_v5 --enable-cluster-autoscaler --min-count 2 --max-count 6.",
"Get credentials and verify both pools: az aks get-credentials -g rg-il28-m41 -n aks-m41; kubectl get nodes -l agentpool=apipool and kubectl get nodes -l kubernetes.azure.com/mode=system.",
"Taint the system pool so workloads stay off it: kubectl taint nodes -l kubernetes.azure.com/mode=system CriticalAddonsOnly=true:NoSchedule. Deploy a test pod without tolerations and confirm via kubectl describe that it avoids system nodes.",
"Deploy AGIC: create the Application Gateway in appgw-subnet, then helm install agic with the gateway ID (follow the current AGIC add-on docs), and verify the ingress controller pod is Running.",
"Deploy a sample app (two Deployments: web and api, each with a ClusterIP Service) and an Ingress with host shop.local, path /api/* -> api service and /* -> web service, using ingress class azure/application-gateway.",
"Force a scale-up: temporarily set the api Deployment replicas to 60 with high CPU requests, watch kubectl get pods for Pending, then kubectl get nodes to see the autoscaler add nodes to apipool.",
"Practice triage: pick one Pending pod, run kubectl describe pod, and write down the FailedScheduling reason; then scale the deployment back to 2 and watch scale-down after ~10 minutes.",
"Raise the ceiling manually: az aks nodepool update -g rg-il28-m41 --cluster-name aks-m41 -n apipool --max-count 10; confirm with az aks nodepool show.",
"Clean up to stop charges: az group delete -n rg-il28-m41 --yes --no-wait. Verify deletion with az group show.",
"Write a one-page triage runbook: the 12-check list for 'new nodes still not deploying' (autoscaler logs, quotas, region capacity, taints, labels, identity permissions, Activity log, Azure Monitor, Resource Health, subnet IPs, SKU restrictions, Azure Policy, max pods)."],
"deliverable": "A running (then deleted) two-pool AKS cluster, a working host/path Ingress through Application Gateway, and a one-page Pending-pod/node-provisioning triage runbook.",
"checkpoint": "kubectl get nodes shows both pools; the Ingress routes /api/* and /* correctly; your runbook lists all 12 triage checks; the resource group is deleted (az group show returns not found)."
}

mockTask = {"id": "il28-m41-mock", "type": "choice",
"q": "Panel scenario: you raised an AKS node pool's max-count from 6 to 12, pods are still Pending, and no new nodes appear after 10 minutes. What do you check FIRST?",
"choices": ["Restart the cluster autoscaler pod", "The Azure Activity log for failed VM creation operations and the subscription's vCPU quota", "Increase every pod's CPU limits", "Delete and recreate the node pool"],
"answer": 1,
"explain": "No new nodes after a ceiling raise means Azure refused or never received the VM creation. The Activity log shows the failed operation and its error code (quota, policy, SKU capacity); the quota check confirms the most common cause. Restarting autoscaler components or editing pod specs cannot fix a cloud-side denial."}

module = {
"id": "IL28-M41", "code": "IL-28",
"title": "AKS: Node Pools, Autoscaling & App Gateway Ingress",
"summary": "Design AKS node pools, drive the cluster autoscaler, triage Pending pods and stalled node provisioning with the full panel checklist, and expose workloads through Application Gateway ingress — answering every AKS panel question cold.",
"objectives": [
"Justify multiple node pools over one giant pool across SKU, scaling, cost, and blast-radius dimensions",
"Configure the cluster autoscaler and manual scaling with az aks nodepool scale/update, including min/max semantics",
"Diagnose Pending pods from kubectl describe events and distinguish scheduler causes from cloud-side provisioning failures",
"Apply taints, tolerations, and labels correctly to control pod placement",
"Expose AKS workloads through Application Gateway with AGIC, contrasting L7 and L4 exposure"],
"notes": notes, "cards": cards, "quiz": quiz, "weight": 2,
"prerequisiteFor": ["IL28-M45"],
"drills": drills, "handsOnLab": handsOnLab, "mockTask": mockTask,
"crossLinks": ["IL28-M45", "IL28-M49"],
"videos": [{"title": "Kubernetes Tutorial for Beginners [FULL COURSE in 4 Hours]", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "source": "YouTube - TechWorld with Nana", "durationMin": 240, "order": 1, "watchBefore": "notes", "blurb": "Full Kubernetes foundations course; focus on the architecture, scheduling, and troubleshooting sections before the AKS-specific notes."}],
"estimatedMinutes": 690,
}

with open("/home/hatch/workspace/apex-audit/docs/university/data/courses/_il28-build/part_f_m41.json", "w") as f:
    json.dump(module, f, indent=2, ensure_ascii=False)
print("M41 written")
