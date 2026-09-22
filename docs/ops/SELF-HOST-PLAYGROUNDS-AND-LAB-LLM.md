# Self-host guide: live cloud playgrounds + lab-aware local model

**Target host:** `p920-host`  
**You provided:** Windows 11 Pro for Workstations 25H2 (build 26200.9457), Experience Pack 1000.26100.360.0  
**CPU:** Dual Intel Xeon Platinum 8176M @ 2.10 GHz (2 sockets)  
**RAM:** 64 GB (≈63.6 GB usable)  
**GPU:** NVIDIA Quadro P1000 **4 GB** (Pascal)  
**Disk:** ≈9.73 TB total (≈3.49 TB used)  
**Plan:** RHEL **10.2 / 10.3** as KVM hypervisor  
**Product:** Interstitium Labs Learning OS + SuperLab (browser terminals → real clusters)

This guide is written for **your** box. It is honest about what a P1000 can and cannot do.

---

## 0. Reality check (read this first)

| Goal | Fit on p920-host |
|------|------------------|
| RHEL KVM hosting lab VMs / k3s / Kind | **Excellent** (dual Xeon + 64 GB + lots of disk) |
| Concurrent student playgrounds | **Modest** — plan for 2–6 light labs, not 50 |
| Browser-based terminals (ttyd / Wetty / Guacamole) | **Excellent** |
| Local open-source LLM “lab-aware” tutor | **Yes, with constraints** |
| GPU-accelerated 7B–70B chat at speed | **No** — P1000 4 GB is too small; use **CPU** (llama.cpp/Ollama) for 3B–8B Q4/Q5, or tiny GPU models ≤3B |
| Replace AWS/Azure full cloud playgrounds | **Partial** — cloud-shaped labs (K8s, Linux, CI, Terraform local); full AWS APIs only via LocalStack/MinIO stubs |

**Honesty:** live playgrounds + a grounded local coder model on this workstation is a strong lab. Claiming “full AWS Skill Builder at home on a P1000” is not.

---

## 1. Recommended topology

```
┌─────────────────────────────────────────────────────────────┐
│  Bare metal: RHEL 10.2/10.3 (KVM hypervisor)   p920-host   │
│  - libvirt / qemu-kvm                                      │
│  - bridge br0 → lab network 10.42.0.0/16                   │
│  - NVIDIA driver (P1000) optional for tiny GPU LLM         │
└───────────────┬─────────────────────────────┬───────────────┘
                │                             │
     ┌──────────▼──────────┐       ┌──────────▼──────────┐
     │ VM: lab-control     │       │ VM: win11-desktop   │
     │ 8–12 GB RAM         │       │ (optional) GUI seat │
     │ Docker/Podman+k3s   │       │ for daily Windows   │
     │ playground API      │       └─────────────────────┘
     │ Ollama / llama.cpp  │
     │ Open WebUI + tools  │
     └──────────┬──────────┘
                │
     ┌──────────▼──────────┐
     │ Lab pool pods / VMs │
     │ student-XXXX ephemeral│
     │ ttyd → bash/kubectl │
     └─────────────────────┘
```

**Why RHEL as hypervisor:** Linux cloud labs (nested containers, Kind, k3s) are smoother on KVM. Keep Windows 11 as a **guest VM** or dual-boot if you still need the Workstation desktop.

**Temporary Windows-first pilot:** Hyper-V + a RHEL VM works on Xeon but nested virt is slower. Prefer bare-metal RHEL for production labs.

---

## 2. Pre-flight on Windows (before wipe / dual-boot)

1. **Backup** BitLocker keys, Documents, browser profiles, lab ISOs.
2. Export disk inventory (`Get-PhysicalDisk`, `Get-Partition`).
3. Download:
   - RHEL 10.2 or 10.3 Boot ISO from Red Hat Customer Portal (subscription), **or** Rocky/AlmaLinux 10 if you want a free rebuild.
   - NVIDIA Quadro Linux driver for P1000 (Pascal).
4. Create UEFI boot USB (balenaEtcher / Rufus).
5. BIOS (P920): enable **VT-x / VT-d**; keep Secure Boot if drivers allow.
6. Disk layout example:
   - Fast SSD: RHEL root + `/var/lib/libvirt`
   - Large volume: `/var/lib/labs` (images, ISOs, model weights)

---

## 3. Install RHEL 10.2 / 10.3 as hypervisor

### 3.1 Installer

- Software: **Minimal** + Virtualization Host (or add after boot).
- Hostname: `p920-host.lab.interstitium.local`
- Users: admin + `labops` (wheel)
- Enable firewalld

### 3.2 First boot

```bash
sudo subscription-manager register   # RHEL only
sudo dnf update -y
sudo dnf install -y @virtualization-hypervisor @virtualization-tools \
  libvirt libvirt-client qemu-kvm virt-install virt-manager \
  NetworkManager cockpit cockpit-machines \
  git curl jq tmux htop iotop

sudo systemctl enable --now libvirtd cockpit.socket
sudo usermod -aG libvirt labops
```

Cockpit: `https://p920-host:9090`

### 3.3 Bridge / lab network

Prefer NAT libvirt network for home safety; use bridge `br0` if LAN students need L2 access. Document NIC name (`eno1` / `enp*`) before enslaving.

### 3.4 Storage pools

```bash
sudo mkdir -p /var/lib/libvirt/images /var/lib/labs/{isos,instances,models,registry}
sudo virsh pool-define-as default dir - - - - /var/lib/libvirt/images
sudo virsh pool-start default && sudo virsh pool-autostart default
```

### 3.5 Quadro P1000 (optional)

```bash
sudo dnf install -y gcc make kernel-devel kernel-headers
# Install NVIDIA proprietary driver matching P1000 + kernel
nvidia-smi   # expect ~4 GiB
```

If GPU install fails, **skip it** — dual 8176M CPU inference is the real workhorse.

---

## 4. Control plane VM (`lab-control`)

### 4.1 Create VM

- 12 GB RAM, 8 vCPU, 200 GB disk, lab network
- OS: RHEL/Rocky 10

```bash
sudo virt-install \
  --name lab-control \
  --memory 12288 --vcpus 8 \
  --disk path=/var/lib/libvirt/images/lab-control.qcow2,size=200 \
  --cdrom /var/lib/labs/isos/rhel-10.3-x86_64-boot.iso \
  --os-variant rhel10.0 \
  --network network=default \
  --graphics vnc
```

### 4.2 k3s + tools

```bash
sudo dnf install -y podman git make firewalld
curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
sudo kubectl get nodes
```

Optional Kind for disposable per-student clusters:

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64
chmod +x kind && sudo mv kind /usr/local/bin/
```

### 4.3 Local registry

```bash
podman run -d --name registry -p 5000:5000 \
  -v /var/lib/labs/registry:/var/lib/registry:Z \
  docker.io/library/registry:2
```

Mirror `nginx`, `busybox`, `kubectl` helper images, etc.

---

## 5. Live cloud playgrounds (browser → real shell)

### 5.1 Pattern A — Ephemeral Pod + ttyd (simplest)

Teaching image includes curl, jq, vim, kubectl, terraform (as needed). Container command:

```text
ttyd -W -p 7681 bash
```

Expose via k3s Service + Traefik Ingress path per user/scenario. Interstitium “Launch” returns that URL.

### 5.2 Pattern B — Disposable Kind cluster (heavier)

```bash
kind create cluster --name s1-k8s101
# later:
kind delete cluster --name s1-k8s101
```

### 5.3 Pattern C — Cloud-shaped stubs

| Capability | Local stand-in |
|------------|----------------|
| Object storage | MinIO |
| AWS API subset | LocalStack (only services you teach) |
| Git | Gitea |
| CI | Gitea Actions / small runner |
| Terraform | against MinIO + Kubernetes provider |

### 5.4 RAM budget (64 GB host)

| Component | RAM |
|-----------|-----|
| RHEL host + libvirt | 4–6 GB |
| lab-control VM | 10–12 GB |
| Ollama / llama.cpp | 8–16 GB |
| Light ttyd lab | 0.5–2 GB |
| Kind cluster | 3–6 GB |

**Comfortable concurrency:** 1 Kind + 3–4 ttyd **or** 6–8 ttyd only.

### 5.5 Orchestrator API

`POST /api/labs {scenario,user}` → create → `{url,expiresAt}`  
`DELETE /api/labs/{id}` → teardown  
TTL reaper 30–120 minutes  
Auth: HMAC from Interstitium / Cloudflare Access

### 5.6 Security

- No Docker socket for students unless DinD inside isolated VM
- NetworkPolicy deny egress except DNS + registry + mirrors
- Quotas + TTL wipe
- Never expose libvirt or Ollama raw to the public Internet

---

## 6. Lab-aware open-source local model

### 6.1 Definition

1. Sees lab context (scenario, transcript, read-only cluster summary)
2. Stays Socratic (hints, not flag dumps)
3. Optional allowlisted tools (`kubectl get`, `terraform validate`)

### 6.2 Models that fit THIS hardware

| Model | Where | Notes |
|-------|-------|-------|
| Qwen2.5-Coder-3B Q4/Q5 | GPU or CPU | Best small coding tutor |
| Llama-3.2-3B-Instruct | CPU/GPU | General |
| Phi-3.5-mini | CPU/GPU | Instruction following |
| Qwen2.5-Coder-7B Q4 | **CPU** (or heavy offload) | Quality sweet spot on dual Xeon |
| 14B+ full GPU | **No** | Won’t fit 4 GB |

### 6.3 Ollama on lab-control

```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable --now ollama
ollama pull qwen2.5-coder:3b
ollama pull qwen2.5-coder:7b-instruct-q4_K_M
```

systemd override example:

```ini
[Service]
Environment="OLLAMA_NUM_PARALLEL=2"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

### 6.4 Open WebUI (ops) + Coach bridge

Point Interstitium Coach at a small API that builds:

```text
You are Interstitium Lab Coach. Socratic only. Never dump full solutions.
Scenario: ...
Recent terminal: ...
Cluster summary (read-only): ...
```

Then `POST` to Ollama `/api/chat`.

### 6.5 Tool allowlist

Allow: `kubectl get/describe`, `terraform validate`  
Deny: `delete`, `apply`, `destroy`, docker.sock, lateral SSH

### 6.6 Optional RAG

Chunk SuperLab docs + scenario READMEs into Chroma/LanceDB; retrieve top-k per turn.

---

## 7. Wire into Interstitium

| Piece | Action |
|-------|--------|
| SuperLab / Labs | Launch → control API |
| Coach | `IL_COACH.endpoint` → lab-control coach URL |
| Adapt | Export weak topics into coach context |
| Edge | Cloudflare Tunnel → `labs.*` with auth |

```bash
cloudflared tunnel create il-labs
# ingress to ttyd + coach only — not Ollama:11434 public
```

---

## 8. Your Windows 11 Pro for Workstations seat

- **Edition:** Windows 11 Pro for Workstations  
- **Version:** 25H2  
- **OS build:** 26200.9457  
- **Experience Pack:** 1000.26100.360.0  

Use Hyper-V only as a **pilot**. After RHEL is hypervisor, recreate Windows as a guest. **Pass the P1000 to either Linux LLM or Windows — not both.**

---

## 9. Staged rollout

| Week | Milestone |
|------|-----------|
| 0 | Backup Windows; RHEL USB; BIOS VT-d |
| 1 | RHEL hypervisor + Cockpit + lab-control |
| 2 | k3s + registry + ttyd “Linux 101” |
| 3 | Interstitium Launch + TTL reaper |
| 4 | Ollama 3B + Socratic Coach API |
| 5 | Kind scenario + MinIO elective |
| 6 | NetworkPolicy, quotas, Tunnel auth |
| 7 | 7B CPU model + RAG |

---

## 10. Capacity quick math

```
Usable ≈ 64 - 8 (host) - 12 (lab-control) - 12 (ollama 7B) ≈ 32 GB labs
Light ttyd ≈ 1.5 GB → ~8 comfortable
Kind ≈ 4 GB → max ~2 concurrent with headroom
```

---

## 11. Failure modes

| Symptom | Fix |
|---------|-----|
| OOM during Kind | Fewer clusters; prefer ttyd |
| GPU OOM on 7B | CPU layers; 3B on GPU |
| Nested net broken | firewall-cmd + flannel check |
| Student escape | No docker.sock; VM boundary |
| Coach spoilers | Exam-mode; hide healthcheck source |

---

## 12. Software shopping list

RHEL/Rocky 10 · libvirt/Cockpit · k3s or Kind · Podman · ttyd · Ollama · Qwen2.5-Coder 3B/7B · Open WebUI · MinIO/Gitea (optional) · cloudflared (optional) · small Launch/Coach API

---

## 13. Success criteria

1. Launch K8s 101 from Interstitium → terminal &lt;15s  
2. Coach uses real cluster context without dumping answers  
3. Lab TTL wipes disk  
4. No public Ollama; no cloud bill  
5. Dual Xeon busy; P1000 either idle or serving 3B cleanly  

---

## 14. Your decisions (reply when ready)

1. Bare-metal RHEL vs Hyper-V pilot first?  
2. RHEL subscription vs Rocky/Alma 10?  
3. GPU to Linux LLM or Windows desktop?  
4. Want the Launch API + Coach proxy scaffolded in the Interstitium repo next?

---

*Document version: 2026-09-22 · Host: p920-host · Win11 Pro Workstation 25H2 build 26200.9457 · Interstitium Labs ops*
