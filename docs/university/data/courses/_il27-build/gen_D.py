"""IL-27 Track D: Virtualization & Cloud (IL27-M18..M22)."""

MODULES_D = [
{
"id": "IL27-M18",
"code": "IL-27",
"title": "Hyper-V Deep Dive",
"summary": "The Windows-native hypervisor: vSwitches, VHDX, checkpoints vs backups, clustering, and performance tuning. Interview-critical for Windows shops. You need this for -> M19/M34 and the homelab.",
"objectives": [
"Design virtual switches (external/internal/private) and explain NIC teaming.",
"Choose VHDX types (fixed/dynamic/differencing) and virtual hardware generations.",
"Use checkpoints correctly and explain why they are not backups.",
"Build a Hyper-V failover cluster with Cluster Shared Volumes.",
"Troubleshoot performance: dynamic memory, vCPU oversubscription, storage QoS."
],
"notes": [
{"title": "Architecture and virtual networking",
"body": "Hyper-V architecture: Type-1 hypervisor - the hypervisor sits on hardware, and the 'host' Windows (management OS / parent partition) is itself virtualized. Child partitions (VMs) get virtual devices via the VMBus (fast, enlightened) or emulated devices (slow, legacy).\n\nVirtual switches: External (bound to a physical NIC - VMs reach the LAN/internet), Internal (host<->VMs only), Private (VMs<->VMs only). Production pattern: external vSwitch on teamed NICs (SET - Switch Embedded Teaming), separate vSwitch or VLANs for management/Live Migration/storage traffic. VLAN tagging on vSwitch ports segments VM traffic without extra hardware.\n\nGeneration matters: Gen 2 VMs (UEFI, Secure Boot, faster boot, SCSI boot) for all modern OSes; Gen 1 only for legacy. Secure Boot + vTPM + Shielded VMs for sensitive workloads. Integration Services (guest enlightenments) must be current - mismatched versions cause weird performance bugs."
},
{"title": "Storage: VHDX done right",
"body": "VHDX (not legacy VHD): 64TB max, power-failure resilience, 4KB alignment. Types: Fixed (preallocated - best performance, predictable), Dynamic (grows on demand - space efficient, slight overhead), Differencing (child tracks changes vs parent - great for labs/VDI, never for production data).\n\nPlacement: CSVs (Cluster Shared Volumes) for clustered hosts - all nodes read/write simultaneously. Pass-through disks are legacy; use VHDX on CSV. Storage QoS policies cap noisy VMs. Deduplication on VHDX libraries saves enormous space for golden images.\n\nCheckpoints (snapshots): point-in-time differencing chains for 'let me try this risky change'. They are NOT backups: they live on the same storage, chains degrade performance, and production checkpoints left for months are a classic outage cause. Rule: checkpoints for changes measured in hours, backups for everything else; merge/delete promptly."
},
{"title": "Clustering, HA, and performance",
"body": "Failover clustering: 2+ Hyper-V hosts + shared storage (CSV) or Storage Spaces Direct. Quorum (witness: disk/file/cloud) decides who survives a split - even node counts need one. Quick Migration (pause, move, resume - brief downtime) vs Live Migration (zero downtime - needs fast network, ideally RDMA/SMB Direct for storage).\n\nDynamic Memory: ballooning gives VMs memory on demand within min/max - great for consolidation, dangerous for SQL/Exchange (use static for memory-hungry apps). vCPU oversubscription: 4:1 to 8:1 typical for light VMs; monitor hypervisor CPU wait time - high wait = oversubscribed.\n\nReplica (Hyper-V Replica): async VM replication to a second site every 30s/5m/15m - the poor man's DR (M31 deep-dives DR). NUMA: keep VM memory within one NUMA node when possible (vNUMA); spanning nodes costs latency. Measure with Performance Monitor: Hyper-V Hypervisor Logical Processor, Virtual Storage Device counters."
}
],
"cards": [
{"front": "Hyper-V hypervisor type", "back": "Type-1: hypervisor on hardware; management OS is itself virtualized."},
{"front": "External vs Internal vs Private vSwitch", "back": "External: LAN/internet. Internal: host-VMs. Private: VMs only."},
{"front": "Gen 2 VM advantages", "back": "UEFI, Secure Boot, faster boot, SCSI boot - default for modern OSes."},
{"front": "Fixed vs Dynamic vs Differencing VHDX", "back": "Fixed: performance. Dynamic: space efficiency. Differencing: labs/VDI, not production."},
{"front": "Checkpoints are not backups because", "back": "Same storage, chain performance decay, left for months = outages."},
{"front": "Quorum witness purpose", "back": "Breaks ties in split-brain; even-node clusters need one."},
{"front": "Quick vs Live Migration", "back": "Quick: brief downtime. Live: zero downtime."},
{"front": "Dynamic Memory caution", "back": "Great for consolidation; use static for SQL/Exchange-like workloads."}
],
"quiz": [
{"q": "VMs need LAN access; host management must stay separate. Design?", "choices": ["External vSwitch on teamed NICs + separate management network/VLAN", "One internal switch", "Private switch", "Wi-Fi bridging"], "answer": 0, "index": 0, "explain": "Segmented virtual networking with teaming for resilience."},
{"q": "Production SQL VM storage. VHDX type?", "choices": ["Fixed (predictable performance)", "Differencing", "Dynamic on USB", "VHD legacy"], "answer": 0, "index": 0, "explain": "Fixed avoids growth overhead on latency-sensitive workloads."},
{"q": "Checkpoint chain 6 months old on a production VM. Risk?", "choices": ["Performance decay + storage risk; merge/delete promptly", "None", "Faster backups", "Better HA"], "answer": 0, "index": 0, "explain": "Checkpoints are short-term change tools, not archives."},
{"q": "Two-node cluster, network split between nodes. Who stays up?", "choices": ["Whoever holds quorum (witness vote)", "Both", "Neither", "The newer one"], "answer": 0, "index": 0, "explain": "Quorum decides; without a witness both may fence."},
{"q": "VMs show high hypervisor CPU wait time. Meaning?", "choices": ["vCPU oversubscription - too many vCPUs for physical cores", "Too much RAM", "Disk is fast", "Network is down"], "answer": 0, "index": 0, "explain": "Wait time = VMs queuing for physical CPU."},
{"q": "Zero-downtime host maintenance needs:", "choices": ["Live Migration to another host", "Quick Migration", "Shutdown", "Checkpoints"], "answer": 0, "index": 0, "explain": "Live Migration moves running VMs with no downtime."},
{"q": "Hyper-V Replica gives you:", "choices": ["Async DR copy to a second site (30s/5m/15m)", "Synchronous mirroring", "Backup tapes", "Load balancing"], "answer": 0, "index": 0, "explain": "Async replication = affordable DR, some data-loss window."},
{"q": "VM memory spanning NUMA nodes causes:", "choices": ["Latency - keep VMs within a node (vNUMA)", "Faster boot", "More vCPUs", "Nothing"], "answer": 0, "index": 0, "explain": "Cross-node memory access is slower."}
],
"weight": 3,
"prerequisiteFor": ["IL27-M19", "IL27-M34"],
"drills": [
{"id": "m18-drill-hv", "title": "Hyper-V Drill",
"items": [
{"prompt": "VMs need internet: switch type?", "answer": "External vSwitch", "explain": "Bound to physical NIC."},
{"prompt": "Isolated lab network", "answer": "Private vSwitch", "explain": "VM-to-VM only."},
{"prompt": "Risky change, 2-hour window", "answer": "Checkpoint, then delete after", "explain": "Short-term safety net."},
{"prompt": "Move running VM, no downtime", "answer": "Live Migration", "explain": "Zero-downtime move."},
{"prompt": "Two-node cluster tie-breaker", "answer": "Quorum witness", "explain": "Decides split-brain."},
{"prompt": "SQL VM memory setting", "answer": "Static memory (not dynamic)", "explain": "Predictable for memory-hungry apps."}
]}
],
"handsOnLab": {
"id": "m18-lab",
"title": "Hyper-V Build: switches, VMs, migration",
"brief": "Build a mini Hyper-V environment with proper networking and a live migration.",
"steps": [
"Enable Hyper-V; create External (teamed if 2 NICs), Internal, Private switches.",
"Build 2 Gen 2 VMs (Server Core) on the external switch with fixed VHDX; install OS.",
"Take a checkpoint, make a breaking change, restore - then delete the checkpoint chain.",
"Set up Hyper-V Replica between two lab hosts (or nested); verify replication state.",
"Perform a Live Migration (or Quick if single host) and measure downtime.",
"Configure Dynamic Memory on one VM and observe ballooning under load."
],
"deliverable": "Switch diagram + VM configs + migration/replica verification + observations.",
"checkpoint": "You can design, build, and operate Hyper-V like a production admin."
},
"mockTask": {"id": "m18-mock", "type": "choice",
"q": "Interview: 'Checkpoints vs backups - what's the difference?'",
"choices": ["Checkpoints are short-term differencing chains on the same storage for quick rollback; backups are independent copies for recovery - never substitute", "They're the same", "Checkpoints are better", "Backups are obsolete"],
"answer": 0, "explain": "The classic trap question - precision here signals experience."},
"crossLinks": ["il04-virtualization"],
"videos": [],
"estimatedMinutes": 300,
"fastTrackEligible": True
},
{
"id": "IL27-M19",
"code": "IL-27",
"title": "VMware & VirtualBox Essentials",
"summary": "The rest of the virtualization world: ESXi/vSphere concepts, vCenter, and VirtualBox for portable labs. You need this for -> mixed environments and interview breadth.",
"objectives": [
"Compare Hyper-V, ESXi, and VirtualBox and choose per scenario.",
"Explain vSphere components: ESXi, vCenter, vMotion, DRS, HA, vSAN.",
"Build and manage VMs in VirtualBox for portable labs.",
"Describe licensing basics (vSphere editions, Broadcom changes) conversationally.",
"Convert/migrate VMs between platforms (V2V concepts)."
],
"notes": [
{"title": "The three platforms",
"body": "ESXi/vSphere: the enterprise standard for two decades - bare-metal ESXi hosts managed by vCenter, with vMotion (live migration), DRS (automatic load balancing), HA (VM restart on host failure), and vSAN (hyperconverged storage). Richest ecosystem, historically priciest; Broadcom's acquisition changed licensing (subscription, per-core) - many shops are re-evaluating, which is why Hyper-V and Proxmox knowledge now pays.\n\nHyper-V: Windows-native, licensed with Windows Server, excellent for Windows shops (M18). VirtualBox: free, cross-platform type-2 hypervisor - perfect for portable labs on a laptop, not for production. Proxmox VE: the open-source rising star (KVM+LXC, clustering, Ceph) - worth knowing exists.\n\nInterview framing: 'I've run production on Hyper-V, labbed vSphere concepts, and keep a VirtualBox lab for portability.' Breadth + honesty beats claiming vCenter expertise you don't have."
},
{"title": "vSphere concepts that transfer",
"body": "Even if you never touch vCenter, its concepts are the industry vocabulary: Cluster (group of hosts), Resource Pool (CPU/RAM reservations/limits), Datastore (shared storage), vMotion (live migrate), Storage vMotion (live migrate storage), DRS (auto-balance VMs across hosts), HA (restart VMs when a host dies - not zero-downtime; that's Fault Tolerance, 1:1 shadow VM).\n\nTemplates + cloning: golden templates -> rapid VM deployment; customization specs handle SID/hostname (the vSphere answer to sysprep). Snapshots: same rules as Hyper-V checkpoints (short-term only). vSwitch/dvSwitch: standard vs distributed virtual switching - distributed = centrally managed across hosts.\n\nThese map 1:1 to Hyper-V concepts (cluster, CSV, Live Migration, templates) - learn the mapping and you can talk to any virtualization admin."
},
{"title": "VirtualBox lab craft",
"body": "VirtualBox: free type-2 hypervisor for Windows/Mac/Linux. Networking modes: NAT (VMs out, host-only inbound), Bridged (VM on the LAN like a physical box), Host-only (VM<->host), Internal (VMs only). Snapshots with branching - great for lab experiments.\n\nLab craft: linked clones (differencing-like, fast lab builds), host-only networks for isolated AD labs, port forwarding for NAT access, shared folders for file exchange, and exporting appliances (OVA) to share lab builds. Performance: enable VT-x/AMD-V, use fixed VHD for heavy VMs, don't oversubscribe a laptop.\n\nV2V migration: convert VHDX<->VMDK with StarWind V2V or qemu-img; VMware vCenter Converter (retired - now use alternatives); always sysprep/generalize Windows when cloning across platforms to avoid SID/duplication issues."
}
],
"cards": [
{"front": "vMotion vs DRS vs HA", "back": "vMotion: live migrate. DRS: auto-balance. HA: restart VMs on host failure."},
{"front": "HA vs Fault Tolerance", "back": "HA: restart (brief outage). FT: shadow VM (zero downtime, 1:1 cost)."},
{"front": "VirtualBox NAT vs Bridged", "back": "NAT: outbound only. Bridged: VM is a LAN citizen."},
{"front": "Broadcom licensing change (conversational)", "back": "vSphere moved to subscription per-core; shops re-evaluating alternatives."},
{"front": "Hyper-V Live Migration = vSphere ?", "back": "vMotion."},
{"front": "CSV = vSphere ?", "back": "Datastore (shared clustered storage)."},
{"front": "Snapshot rule (all platforms)", "back": "Short-term change safety only - never a backup, merge promptly."},
{"front": "V2V conversion tools", "back": "StarWind V2V, qemu-img; sysprep Windows when cloning."}
],
"quiz": [
{"q": "Zero-downtime VM move in vSphere is called:", "choices": ["vMotion", "HA", "DRS", "Clone"], "answer": 0, "index": 0, "explain": "vMotion = live migration."},
{"q": "Host dies; VMs restart on surviving hosts. That's:", "choices": ["HA", "Fault Tolerance", "vMotion", "DRS"], "answer": 0, "index": 0, "explain": "HA restarts (brief outage); FT would have zero downtime."},
{"q": "Laptop lab: isolated AD network, no LAN access. VirtualBox mode?", "choices": ["Host-only or Internal", "Bridged", "NAT with forwarding", "None"], "answer": 0, "index": 0, "explain": "Isolated VM networks without LAN leakage."},
{"q": "Shop re-evaluating vSphere on cost. Alternatives to discuss?", "choices": ["Hyper-V, Proxmox VE", "Mainframes", "No virtualization", "Only cloud"], "answer": 0, "index": 0, "explain": "The real conversation happening in IT now."},
{"q": "Cloned Windows VM shows duplicate SID issues. Prevention?", "choices": ["Sysprep/generalize before cloning", "Rename only", "New IP only", "Reinstall"], "answer": 0, "index": 0, "explain": "Generalize resets identity."},
{"q": "DRS does what automatically?", "choices": ["Balances VM load across hosts", "Backs up VMs", "Patches hosts", "Creates VLANs"], "answer": 0, "index": 0, "explain": "Distributed Resource Scheduler = auto load balancing."},
{"q": "Fast lab builds of 10 identical VMs in VirtualBox:", "choices": ["Linked clones from a golden VM", "10 full installs", "Copy the laptop", "USB sticks"], "answer": 0, "index": 0, "explain": "Differencing-like clones deploy in seconds."},
{"q": "Share a lab build with a colleague. Format?", "choices": ["OVA appliance export", "Screenshot", "ISO of host", "Email the VHD"], "answer": 0, "index": 0, "explain": "OVA = portable VM package."}
],
"weight": 2,
"prerequisiteFor": [],
"drills": [
{"id": "m19-drill-virt", "title": "Virtualization Cross-Platform Drill",
"items": [
{"prompt": "Live migrate: Hyper-V term / vSphere term", "answer": "Live Migration / vMotion", "explain": "Same concept, both vendors."},
{"prompt": "Host failure auto-restart", "answer": "Hyper-V cluster / vSphere HA", "explain": "Restart, not zero-downtime."},
{"prompt": "Portable laptop lab hypervisor", "answer": "VirtualBox", "explain": "Free type-2."},
{"prompt": "Zero-downtime shadow VM", "answer": "Fault Tolerance (vSphere)", "explain": "1:1 shadow cost."},
{"prompt": "Convert VHDX to VMDK", "answer": "StarWind V2V / qemu-img", "explain": "V2V conversion."},
{"prompt": "Avoid duplicate SIDs on clone", "answer": "Sysprep / generalize", "explain": "Reset machine identity."}
]}
],
"handsOnLab": {
"id": "m19-lab",
"title": "Portable Lab: VirtualBox AD playground",
"brief": "Build a portable, isolated AD lab in VirtualBox you can carry anywhere.",
"steps": [
"Install VirtualBox; create a Host-only network (192.168.56.0/24).",
"Build 2 linked clones from a golden Server Core VM: DC + member.",
"Promote the DC (isolated forest), join the member - all on host-only.",
"Practice snapshots: branch, break, restore - then clean up.",
"Export the DC as an OVA; document the import steps.",
"Write the concept map: Hyper-V term -> vSphere term for 10 items."
],
"deliverable": "Portable lab + OVA + Hyper-V/vSphere concept map.",
"checkpoint": "You speak both virtualization dialects and carry a lab in your pocket."
},
"mockTask": {"id": "m19-mock", "type": "choice",
"q": "Interview: 'Hyper-V or VMware - which do you prefer?'",
"choices": ["Depends on the shop: Hyper-V for Windows-centric cost efficiency, vSphere for the mature ecosystem; I run both concepts and choose per workload", "VMware always", "Hyper-V always", "VirtualBox for production"],
"answer": 0, "explain": "Vendor-neutral, workload-driven - the senior answer."},
"crossLinks": ["il04-virtualization"],
"videos": [],
"estimatedMinutes": 220,
"fastTrackEligible": False
},
{
"id": "IL27-M20",
"code": "IL-27",
"title": "Containers & Docker for Infra Admins",
"summary": "What containers change for infrastructure: images, Docker workflow, Compose, and when containers beat VMs. You need this for -> M21/M22 and modern deployment conversations.",
"objectives": [
"Explain containers vs VMs (kernel sharing, density, immutability).",
"Run and manage containers: images, volumes, networks, Compose.",
"Write Dockerfiles with layer-caching and least-privilege practices.",
"Decide containers vs VMs per workload.",
"Describe Kubernetes' role at a conversational level."
],
"notes": [
{"title": "Containers vs VMs: the mental model",
"body": "VM: full guest OS per workload (GBs, minutes to boot). Container: shares the host kernel, packages app + dependencies (MBs, seconds to start). Density: dozens of containers where a few VMs fit. Immutability: containers are rebuilt from images, not patched in place - 'cattle, not pets' taken literally.\n\nImages are layered filesystems (each Dockerfile instruction = a layer, cached). Containers are ephemeral instances of images; state lives in volumes (persisted) or dies with the container. This changes backup thinking: you back up VOLUMES and image definitions, not containers.\n\nFor infra admins, containers shine for: lab services (spin up a test web server in seconds), CI/CD agents, and portable tooling. They don't replace VMs for: Windows AD, stateful monoliths needing full OS control, or workloads needing kernel isolation."
},
{"title": "Docker workflow that matters",
"body": "Core loop: docker pull (image) -> docker run (container) -> docker ps/logs/exec (operate) -> docker stop/rm. Volumes: -v data:/data persists beyond the container. Networks: bridge (default), host, custom - containers get DNS by name on user-defined networks.\n\nDockerfile craft: FROM a minimal official base, one concern per layer, order instructions by change frequency (deps first for cache), COPY not ADD, run as non-root (USER), .dockerignore to keep secrets out. Multi-stage builds: compile in one stage, ship only the binary - tiny, safer images.\n\nCompose: docker-compose.yml defines multi-container apps (web + db + cache) with one command. The homelab superpower: your entire monitoring stack (M33) or test environment as one Compose file - versioned, reproducible, shareable."
},
{"title": "Security and the Kubernetes conversation",
"body": "Container security for infra: never run as root inside, scan images (known CVEs in base layers), pin versions (never :latest in production), keep the host patched (shared kernel = shared fate), and treat registries like software supply chain (private registry, signed images).\n\nKubernetes (K8s): the orchestrator - schedules containers across nodes, self-heals, scales, rolling updates. Concepts: Pod (smallest unit), Deployment, Service (stable networking), Ingress, ConfigMap/Secret. You won't admin K8s day-one in most infra roles, but 'pods vs containers, services for discovery, rolling updates' must be conversational.\n\nDecision framework: VM when you need full OS control, strong isolation, or Windows roles. Container when you need density, speed, reproducibility, and stateless-ish services. Many shops run containers ON VMs - the layers compose."
}
],
"cards": [
{"front": "Container vs VM isolation", "back": "VM: hardware-level, full OS. Container: shared kernel, process-level."},
{"front": "Image vs container vs volume", "back": "Image: template (layers). Container: running instance. Volume: persistent state."},
{"front": "Why pin image versions?", "back": ":latest shifts under you - non-reproducible, risky."},
{"front": "Multi-stage build value", "back": "Compile in one stage, ship only artifacts - small, safer images."},
{"front": "Never do in a Dockerfile", "back": "Run as root; bake in secrets; use :latest in prod."},
{"front": "Kubernetes Pod", "back": "Smallest deployable unit - one or more containers sharing network/storage."},
{"front": "Back up what in container-land?", "back": "Volumes + image definitions/Compose files - not containers."},
{"front": "Compose superpower", "back": "Multi-container app as one versioned, reproducible file."}
],
"quiz": [
{"q": "Containers start in seconds because:", "choices": ["They share the host kernel - no guest OS boot", "They're magic", "Smaller CPUs", "No network"], "answer": 0, "index": 0, "explain": "No OS boot = instant start."},
{"q": "Database in a container loses data on restart. Fix?", "choices": ["Attach a volume for the data directory", "Bigger image", "More RAM", "Restart less"], "answer": 0, "index": 0, "explain": "State must live outside the ephemeral container."},
{"q": "Dockerfile best practice:", "choices": ["Non-root USER, pinned base, .dockerignore, layer order by change frequency", "Root everywhere, :latest", "Secrets in ENV", "One giant layer"], "answer": 0, "index": 0, "explain": "Least privilege + reproducibility + cache efficiency."},
{"q": "AD domain controller in a container?", "choices": ["No - full OS role needing strong isolation; use a VM", "Yes, ideal", "Only on Fridays", "In the registry"], "answer": 0, "index": 0, "explain": "Wrong tool: DCs need full OS control and isolation."},
{"q": "K8s Service provides:", "choices": ["Stable networking/discovery for ephemeral pods", "Storage", "Backups", "DNS for the internet"], "answer": 0, "index": 0, "explain": "Pods die; Services give a stable endpoint."},
{"q": "Shared kernel means:", "choices": ["Host kernel CVE affects all containers - patch the host", "Containers are VMs", "No patching needed", "Windows only"], "answer": 0, "index": 0, "explain": "Shared fate - host patching is container security."},
{"q": "Rolling update in K8s:", "choices": ["Replace pods incrementally with zero downtime", "Big bang reboot", "Manual binary copy", "Downtime window"], "answer": 0, "index": 0, "explain": "Incremental replacement = always serving."},
{"q": "Your monitoring stack as code:", "choices": ["docker-compose.yml - versioned, reproducible, one command", "Screenshots", "Memory", "Sticky notes"], "answer": 0, "index": 0, "explain": "Compose = infrastructure as code for services."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M33"],
"drills": [
{"id": "m20-drill-containers", "title": "Containers Drill",
"items": [
{"prompt": "Run nginx detached, port 8080", "answer": "docker run -d -p 8080:80 nginx", "explain": "Core run pattern."},
{"prompt": "Persist container data", "answer": "docker run -v mydata:/data ...", "explain": "Volumes outlive containers."},
{"prompt": "See container logs", "answer": "docker logs <name>", "explain": "Ops basics."},
{"prompt": "Multi-container app file", "answer": "docker-compose.yml", "explain": "One file, one command."},
{"prompt": "Shell into a running container", "answer": "docker exec -it <name> sh", "explain": "Debug access."},
{"prompt": "K8s smallest unit", "answer": "Pod", "explain": "One+ containers."}
]}
],
"handsOnLab": {
"id": "m20-lab",
"title": "Container Stack: Compose your lab services",
"brief": "Run real lab services as containers with Compose.",
"steps": [
"Install Docker; run nginx and verify; practice ps/logs/exec/stop/rm.",
"Write a Dockerfile for a simple app (multi-stage, non-root, pinned base).",
"Build and run it; scan the image (docker scout or similar) and note CVEs.",
"Write docker-compose.yml: web + redis; verify inter-container DNS by name.",
"Add a volume; prove data survives container recreation.",
"Document the containers-vs-VMs decision for 5 lab workloads."
],
"deliverable": "Dockerfile + Compose stack + scan notes + decision doc.",
"checkpoint": "You run containerized services and know when NOT to."
},
"mockTask": {"id": "m20-mock", "type": "choice",
"q": "Interview: 'When would you use containers vs VMs?'",
"choices": ["Containers for dense, fast, reproducible stateless-ish services; VMs for full-OS control, strong isolation, Windows roles - often containers on VMs", "Containers for everything", "VMs for everything", "Neither"],
"answer": 0, "explain": "Workload-driven, layered thinking."},
"crossLinks": ["il06-devops"],
"videos": "VIDEOS_M20",
"estimatedMinutes": 240,
"fastTrackEligible": False
},
{
"id": "IL27-M21",
"code": "IL-27",
"title": "Azure Fundamentals for Infra Admins",
"summary": "Azure through an infrastructure lens: subscriptions, VNets, VMs, storage, Entra, and what everything costs. You need this for -> M17/M22 and hybrid/cloud interviews.",
"objectives": [
"Navigate the hierarchy: management groups, subscriptions, resource groups.",
"Build a VNet with subnets, NSGs, and a VM (portal + CLI).",
"Choose storage tiers and VM series conversationally.",
"Estimate costs and name the top cost controls.",
"Explain hybrid: Arc, VPN/ExpressRoute, and Entra's role."
],
"notes": [
{"title": "Hierarchy and identity",
"body": "Hierarchy: Management Groups -> Subscriptions (billing + policy boundary) -> Resource Groups (lifecycle boundary - delete the group, delete everything) -> Resources. Naming convention + mandatory tags (owner, env, costcenter) from day one - untagged sprawl is the #1 cloud mess.\n\nEntra ID is the identity plane (M17): every Azure action authenticates through it. RBAC: Owner/Contributor/Reader + granular roles, assigned at scope (subscription/RG/resource). PIM (Privileged Identity Management): just-in-time admin elevation - standing admin rights are the old way.\n\nPolicy: guardrails as code (allowed regions, required tags, VM SKUs). Blueprints/landing zones package the standard. An infra admin who says 'policy enforces our tagging and region rules' speaks cloud governance."
},
{"title": "Network and compute",
"body": "VNet: your cloud network - address space, subnets (separate tiers: web/app/data), NSGs (subnet/NIC firewall rules - the cloud ACL), route tables, peering (VNet-to-VNet). No broadcast domain worries; plan address space to avoid overlap with on-prem (VPN/ExpressRoute needs non-overlapping ranges).\n\nVMs: series (D=general, E=memory, F=compute, N=GPU), sizes, managed disks (Premium SSD for production), availability sets/zones (fault/update domains; zones = datacenter-level). Bastion for RDP/SSH without public IPs; JIT access narrows exposure.\n\nHybrid: Site-to-Site VPN (encrypted over internet) vs ExpressRoute (private circuit - consistent latency, more money). Azure Arc extends management to on-prem servers (policy, updates, inventory) - the hybrid admin's bridge."
},
{"title": "Storage, backup, and the money",
"body": "Storage accounts: Blob (object), Files (SMB shares!), Disks, Tables/Queues. Tiers: Hot/Cool/Cold/Archive - lifecycle policies move data down automatically. Azure Files can literally replace a file server with AD-authenticated SMB shares.\n\nBackup: Azure Backup (VMs, files, SQL) with vaults and retention policies; Site Recovery for DR failover (the cloud M31). Monitor: Log Analytics + alerts - the M33 concepts, cloud-native.\n\nCost: pay-as-you-go per second; the bill shock comes from: oversized VMs, unattached disks, forgotten test RGs, data egress. Controls: budgets + alerts, auto-shutdown for dev VMs, reserved instances (1-3 yr commit = big discount), Azure Advisor right-sizing, and deleting what you don't use. 'Show me the cost' should be your first question for any cloud design."
}
],
"cards": [
{"front": "Hierarchy order", "back": "Management Groups -> Subscriptions -> Resource Groups -> Resources."},
{"front": "Resource Group deletion does what?", "back": "Deletes everything in it - lifecycle boundary."},
{"front": "NSG is the cloud equivalent of", "back": "ACL/firewall rules on subnets and NICs."},
{"front": "VPN vs ExpressRoute", "back": "VPN: encrypted over internet. ExpressRoute: private circuit, consistent, pricier."},
{"front": "Availability zones protect against", "back": "Datacenter-level failure (fault isolation across DCs)."},
{"front": "Azure Arc does what?", "back": "Extends Azure management (policy, updates) to on-prem servers."},
{"front": "Top cloud cost surprises", "back": "Oversized VMs, unattached disks, forgotten RGs, egress."},
{"front": "Reserved instances value", "back": "1-3 year commit for steady workloads = large discount."}
],
"quiz": [
{"q": "Dev team left 20 test VMs running for 3 months. Prevention?", "choices": ["Auto-shutdown policies + budgets/alerts + RG lifecycle", "Bigger subscription", "More admins", "Ignore it"], "answer": 0, "index": 0, "explain": "Automation + alerts kill sprawl."},
{"q": "On-prem 10.0.0.0/16; new Azure VNet should be:", "choices": ["Non-overlapping (e.g., 10.1.0.0/16 is wrong - use 172.16.0.0/16)", "10.0.0.0/16", "Same as on-prem", "Anything"], "answer": 0, "index": 0, "explain": "VPN/ER peering requires non-overlapping space."},
{"q": "VM needs datacenter-level resilience in Azure:", "choices": ["Availability Zones", "Bigger VM", "More disks", "Premium support"], "answer": 0, "index": 0, "explain": "Zones isolate datacenter failures."},
{"q": "RDP to Azure VMs without public IPs:", "choices": ["Azure Bastion", "Open RDP to internet", "Email", "Carrier pigeon"], "answer": 0, "index": 0, "explain": "Bastion = browser RDP/SSH, no exposed ports."},
{"q": "Replace an on-prem file server with cloud SMB:", "choices": ["Azure Files with AD authentication", "Blob only", "VMs only", "USB drives"], "answer": 0, "index": 0, "explain": "Files = managed SMB shares, AD-integrated."},
{"q": "Standing domain-admin-equivalent rights in Azure. Better?", "choices": ["PIM just-in-time elevation", "More admins", "Shared credentials", "No access"], "answer": 0, "index": 0, "explain": "JIT admin = least privilege for the cloud."},
{"q": "Steady production VM running 24/7 for a year. Save money?", "choices": ["Reserved instance (1-yr)", "Bigger VM", "Spot only", "Two VMs"], "answer": 0, "index": 0, "explain": "Commit to steady = discount."},
{"q": "Enforce 'all resources tagged with owner' automatically:", "choices": ["Azure Policy", "An email", "Hope", "A spreadsheet"], "answer": 0, "index": 0, "explain": "Policy = guardrails as code."}
],
"weight": 2,
"prerequisiteFor": ["IL27-M17"],
"drills": [
{"id": "m21-drill-azure", "title": "Azure Drill",
"items": [
{"prompt": "Billing boundary?", "answer": "Subscription", "explain": "Billing + policy scope."},
{"prompt": "Delete a whole environment at once", "answer": "Delete its Resource Group", "explain": "Lifecycle boundary."},
{"prompt": "Subnet firewall", "answer": "NSG", "explain": "Cloud ACL."},
{"prompt": "Private on-prem link", "answer": "ExpressRoute", "explain": "Not over internet."},
{"prompt": "Manage on-prem servers from Azure", "answer": "Azure Arc", "explain": "Hybrid bridge."},
{"prompt": "No public IP RDP", "answer": "Azure Bastion", "explain": "Browser-based access."}
]}
],
"handsOnLab": {
"id": "m21-lab",
"title": "Azure Build: VNet + VM + budget (free tier)",
"brief": "Build a real Azure network and VM inside free-tier limits, with cost guardrails.",
"steps": [
"Create free account; set up a budget alert at $5.",
"Create RG + VNet (non-overlapping space) with 2 subnets + NSG (RDP only from your IP).",
"Deploy a B-series VM via portal, then redeploy via CLI (az vm create) to compare.",
"Attach a data disk; create a storage account with a Cool-tier container.",
"Set auto-shutdown on the VM; verify the budget alert fires on a test.",
"Document the monthly cost estimate for the build."
],
"deliverable": "Running VNet+VM + budget alert proof + cost estimate doc.",
"checkpoint": "You can build in Azure without fearing the bill."
},
"mockTask": {"id": "m21-mock", "type": "choice",
"q": "Interview: 'How do you keep Azure costs under control?'",
"choices": ["Budgets/alerts, auto-shutdown dev, right-size via Advisor, reserved instances for steady, delete orphans, tag everything", "Trust the portal", "One big VM", "Prepay everything"],
"answer": 0, "explain": "Cost discipline is an infra skill, not a finance afterthought."},
"crossLinks": ["il11-entra-identity--sc300-hybrid"],
"videos": "VIDEOS_M21",
"estimatedMinutes": 260,
"fastTrackEligible": False
},
{
"id": "IL27-M22",
"code": "IL-27",
"title": "AWS Fundamentals for Infra Admins",
"summary": "AWS through the same infrastructure lens: VPCs, EC2, storage, IAM, and cost. Multi-cloud literacy doubles your interview surface. You need this for -> cloud conversations and M31/M33.",
"objectives": [
"Build a VPC with public/private subnets, IGW, NAT, and security groups.",
"Launch and operate EC2 instances (AMIs, instance types, EBS).",
"Choose S3 storage classes and explain lifecycle policies.",
"Apply IAM least privilege (users, roles, policies, MFA).",
"Name AWS cost controls and the shared responsibility model."
],
"notes": [
{"title": "VPC: your cloud datacenter",
"body": "VPC = isolated network: CIDR block, subnets across Availability Zones (AZs - separate datacenters). Public subnets route to an Internet Gateway; private subnets reach the internet via NAT Gateway (outbound only). Route tables steer; Network ACLs (stateless, subnet-level) + Security Groups (stateful, instance-level) filter - SGs are the ones you touch daily.\n\nAZ design: spread across 2-3 AZs for resilience; each AZ is isolated power/cooling/network. Regions for geography/compliance. Non-overlapping CIDRs with on-prem for VPN/Direct Connect - same rule as Azure.\n\nVPC peering / Transit Gateway connect VPCs; VPN or Direct Connect (the ExpressRoute equivalent) bridges on-prem. Default VPC exists - don't build production in it; build your own with intention."
},
{"title": "EC2, storage, and IAM",
"body": "EC2: AMIs (golden images - build your own hardened ones), instance types (t=burstable, m=general, c=compute, r=memory, g=GPU), EBS volumes (gp3 general, io2 critical; snapshots for backup), key pairs for SSH (guard the .pem like a password), user data for bootstrap scripts.\n\nS3: object storage - buckets, versioning, encryption, storage classes (Standard/IA/Glacier), lifecycle policies to Glacier. EFS (managed NFS) and FSx (Windows file shares!) for file workloads.\n\nIAM: users (humans), roles (for services/instances - EC2 instance profiles, never access keys on instances), policies (JSON least-privilege), MFA everywhere, no root key usage. IAM is the FIRST thing to get right - most AWS breaches are IAM mistakes, not AWS mistakes."
},
{"title": "Shared responsibility and cost",
"body": "Shared responsibility: AWS secures OF the cloud (hardware, hypervisor, facilities); you secure IN the cloud (your data, IAM, OS patching, SG rules, encryption). Saying this correctly in an interview signals cloud maturity.\n\nCost: per-second EC2, S3 per-GB, data transfer out. Surprises: NAT Gateway hourly + per-GB, forgotten EBS snapshots, cross-AZ traffic. Controls: Budgets + Cost Anomaly alerts, Compute Optimizer right-sizing, Savings Plans / Reserved Instances, S3 Intelligent-Tiering, Instance Scheduler for dev.\n\nMulti-cloud reality: most orgs are Azure-primary or AWS-primary with the other for specific workloads. Your value: the patterns transfer (VNet=VPC, NSG=SG, Bastion=Session Manager). Learn one deeply, map the other."
}
],
"cards": [
{"front": "Public vs private subnet", "back": "Public: IGW route. Private: NAT for outbound only."},
{"front": "Security Groups vs NACLs", "back": "SG: stateful, instance-level. NACL: stateless, subnet-level."},
{"front": "Never put on an EC2 instance", "back": "Long-lived access keys - use IAM roles (instance profiles)."},
{"front": "Shared responsibility split", "back": "AWS: OF the cloud. You: IN the cloud (data, IAM, OS, config)."},
{"front": "S3 Glacier is for", "back": "Archive - cheap, slow retrieval; lifecycle policies move data there."},
{"front": "AZ vs Region", "back": "AZ: isolated datacenter. Region: geographic area of AZs."},
{"front": "NAT Gateway cost gotcha", "back": "Hourly charge + per-GB processing - adds up fast."},
{"front": "VNet=VPC; NSG=?; Bastion=?", "back": "Security Groups; Systems Manager Session Manager."}
],
"quiz": [
{"q": "Web servers need internet; databases must not be directly reachable. Design?", "choices": ["Public subnets (web) + private subnets (DB), SGs restricting DB to web tier", "All public", "All private", "One subnet"], "answer": 0, "index": 0, "explain": "Tiered subnets + least-privilege SGs."},
{"q": "App on EC2 needs S3 access. Secure way?", "choices": ["IAM role via instance profile", "Access keys in code", "Public bucket", "Root keys"], "answer": 0, "index": 0, "explain": "Roles rotate automatically; keys leak."},
{"q": "Most AWS breaches trace to:", "choices": ["Customer IAM/config mistakes", "AWS datacenter break-ins", "Hypervisor escapes", "Aliens"], "answer": 0, "index": 0, "explain": "Shared responsibility: the customer side is where errors happen."},
{"q": "Old backups, rarely accessed, must be kept 7 years:", "choices": ["S3 Glacier via lifecycle policy", "Standard always", "EBS", "Local disks"], "answer": 0, "index": 0, "explain": "Archive tier = cheapest compliant retention."},
{"q": "SSH to EC2 without opening port 22:", "choices": ["Systems Manager Session Manager", "Telnet", "Public RDP", "Email"], "answer": 0, "index": 0, "explain": "SSM = audited shell, no inbound ports."},
{"q": "Surprise $800 NAT bill. Cause?", "choices": ["NAT Gateway hourly + per-GB on heavy traffic", "EC2", "S3", "IAM"], "answer": 0, "index": 0, "explain": "NAT processing charges surprise everyone once."},
{"q": "Golden image strategy:", "choices": ["Build hardened AMIs, version them, launch from AMI", "Manual setup each time", "Share passwords", "Public AMIs blindly"], "answer": 0, "index": 0, "explain": "Immutable infrastructure starts with images."},
{"q": "Direct Connect is AWS's:", "choices": ["Private circuit to on-prem (like ExpressRoute)", "VPN", "Satellite", "CDN"], "answer": 0, "index": 0, "explain": "Dedicated private connectivity."}
],
"weight": 2,
"prerequisiteFor": [],
"drills": [
{"id": "m22-drill-aws", "title": "AWS Drill",
"items": [
{"prompt": "Isolated AWS network", "answer": "VPC", "explain": "Your cloud datacenter."},
{"prompt": "Instance firewall", "answer": "Security Group (stateful)", "explain": "Attached to instances."},
{"prompt": "EC2 accessing AWS services", "answer": "IAM role / instance profile", "explain": "No keys on instances."},
{"prompt": "Cheapest 7-year retention", "answer": "S3 Glacier", "explain": "Archive tier."},
{"prompt": "Your half of shared responsibility", "answer": "IN the cloud: data, IAM, OS, config", "explain": "AWS handles OF."},
{"prompt": "No-port-22 shell", "answer": "Session Manager", "explain": "Via SSM agent."}
]}
],
"handsOnLab": {
"id": "m22-lab",
"title": "AWS Build: VPC + EC2 + S3 (free tier)",
"brief": "Build a tiered VPC with a web server and private backend inside free-tier limits.",
"steps": [
"Create free account; enable MFA on root; create an admin IAM user; never use root again.",
"Build a custom VPC: 2 public + 2 private subnets across 2 AZs, IGW, NAT Gateway (note the cost!).",
"Launch EC2 (Amazon Linux) in public subnet via hardened AMI thinking; SG allows 80/443 only.",
"Put a test instance in private subnet; reach it via Session Manager (no SSH port).",
"Create an S3 bucket with versioning + lifecycle to Glacier; upload test data.",
"Set a $5 budget alert; document the architecture and monthly estimate."
],
"deliverable": "VPC diagram + running instances + S3 lifecycle + budget alert + cost doc.",
"checkpoint": "You can build secure, tiered infrastructure in AWS."
},
"mockTask": {"id": "m22-mock", "type": "choice",
"q": "Interview: 'Explain the AWS shared responsibility model.'",
"choices": ["AWS secures OF the cloud (facilities, hardware, hypervisor); I secure IN the cloud - my data, IAM, OS patching, security groups, encryption", "AWS handles everything", "I handle everything", "It's 50/50 on everything"],
"answer": 0, "explain": "The crisp split interviewers want to hear."},
"crossLinks": [],
"videos": [],
"estimatedMinutes": 260,
"fastTrackEligible": False
}
]
