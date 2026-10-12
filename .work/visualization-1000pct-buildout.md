# Sitewide Visualization 1000% Buildout — Progress Report

**Started:** 2026-10-09 ~01:10 EDT
**User order:** "Yes recursive audit all content sitewide and all tabs, sub domains etc build optimally enhanced all byte byte go and adjacent visualizations, diagrams, charts, media rich animations"

## Current State (Pre-Buildout)

| Metric | Count |
|---|---|
| Videos live (from video buildout) | 319 MP4s |
| Courses with video | 29/29 (6 videos each) |
| Bootcamps with video | 42/143 |
| Bootcamps remaining | 101 (79 with content.json + 22 non-standard) |

## Blocker: TTS Service Down

**Status:** TTS auth token rejected 2026-10-08. All videos ship as "Preview — narration coming" with complete narration scripts and caption files staged.

## Buildout Plan

### Phase 1: Remaining Bootcamp Videos (B5–B12)
3 videos per bootcamp × 79 remaining bootcamps = ~237 videos

| Batch | Bootcamps | Count | Status |
|---|---|---|---|
| B5 | python, python-web, java, cpp, c-lang, dsa, fullstack, react-frontend, spring, dotnet, docker, terraform | 12 | 🔄 Rendering (builder active) |
| B6 | aws-clf, aws-data, aws-dop, aws-ml, aws-saa, aws-scs, aws-soa, az-104, az-305, az-700, azure-developer, oracle-oci | 12 | ✅ Generator ready, queued |
| B7 | cism, cissp, comptia-cyber, dod-8140, nice-framework, nsa-codebreaker, pentest, sc-200, sc-300, soc-analyst, fde-training, hackers-arise | 12 | ✅ Generator ready, queued |
| B8 | cka, ckad, k8s-associate, openshift, linux-essentials, rhce, rhcsa, comptia-infra, comptia-core, m365, ms-fundamentals, windows-admin | 12 | ✅ Generator ready, queued |
| B9 | ai-lab, ai-product, alan-turing, il12-ai-engineering, llm-engineering, ml-defense, nvidia-ai, quantum, dp-203, mongodb, oracle-db, oracle-sql | 12 | ✅ Generator ready, queued |
| B10 | blockchain-dev, creative-code, enochian-programming, git-devops, ides-tooling, platform-engineering, python-systems, sre-platform, sre-practices, systems-cs, vault-consul, fullstack-desk | 12 | ✅ Generator ready, queued |
| B11 | career-launch, deep-work, edward-bernays, electrician-apprentice, embedded-interview, entrepreneurship, frontier-path, full-spectrum-dominance, hermetica, humanmetrics, philosophy, occult-esoteric | 12 | ✅ Generator ready, queued |
| B12 | aleks-ops-math, math-tech, android-interview, ios-interview, tl-interview, threatlocker-assessment-prep, vendor-map, zerotrust | 8 | ✅ Generator ready, queued (⚠️ needs threatlocker-assessment-prep dir created) |

### Phase 2: Course Tab Visualizations
Ensure Labs, Simulations, Terminal, Practice tabs have relevant visualizations.

### Phase 3: System Architecture Diagrams
Key concepts: networking, cloud, security, AI/ML.

### Phase 4: IL-26 Data Visualizations
Charts, graphs, dashboards for the data analyst course.

## Progress Log

### 2026-10-09 ~01:10 EDT — Coordinator initialized
- Audited state: 319 MP4s live, 42/143 bootcamps covered, 79 real bootcamps remaining (with content.json)
- B5 generator ready (12 bootcamps: python, python-web, java, cpp, c-lang, dsa, fullstack, react-frontend, spring, dotnet, docker, terraform) — NOT yet rendered
- Spawned B5 builder subagent (render 36 videos, wire, deploy both workers, verify)
- Spawned B6–B12 generator writer subagent (7 generators: B6 cloud certs, B7 security certs, B8 k8s/linux/infra, B9 data/AI, B10 dev/misc, B11 career/human, B12 final 8)
- System constrained: 2 CPUs, 138MB RAM free — sequential rendering only, no parallel builders
- Updated batch table above with B5 "In progress", B6–B12 "Pending"

### 2026-10-09 ~01:15 EDT — Builders active
- B5 builder: actively rendering (PID 16012, 36% CPU), SMOKE test running in parallel
- B6–B12 generator writer: spawned, working on 7 generators + wire scripts
- Coordinator waiting for completions; 5-min monitor will track progress

### 2026-10-09 ~01:55 EDT — B6–B12 Generators Complete ✅
- Generator writer subagent completed all 7 generators + 7 wire scripts
- **240 videos** total: B6(36) + B7(36) + B8(36) + B9(36) + B10(36) + B11(36) + B12(24)
- All SMOKE-tested: 240/240 rendered, 0 failures
- All 240 scene functions executed at 7 time points each — 0 errors
- 240 unique `bc-<style>-<slug>.mp4` filenames, verified non-colliding
- Files: `~/workspace/apex-audit/.work/gen_bootcamp_b{6,7,8,9,10,11,12}.py` + `wire_bootcamp_b{6,7,8,9,10,11,12}.py`
- Regeneration: `python3 build_bootcamp_b6_b12.py`

**CAVEAT for B12 builder:** `~/workspace/cert-bootcamps/site/bootcamps/threatlocker-assessment-prep/` does not exist — `wire_bootcamp_b12.py` will fail on that slug until the directory is created with a content.json. All other 78 slugs verified. B12 builder must create this directory first (model on tl-interview/content.json structure).

### 2026-10-09 ~02:39 EDT — B5 Complete ✅ / CRITICAL: File Deleter Active 🚨
- B5 builder completed: 36/36 videos rendered, wired, deployed (both workers), verified HTTP 200
- Bootcamp coverage: 54/143

**🚨 CRITICAL ISSUE: Unidentified bc-*.mp4 deleter**
- Between 01:35–05:10 EDT: ~126 B1–B4 bc-*.mp4 files (+sidecars) deleted
- Between 05:14–05:56 EDT: all 36 B5 files + ~8 B6 files deleted in bursts
- Confirmed via honeypot bait files (deleted within 1–3 min)
- NOT a cron, NOT the trash tool, no local script contains deletion logic, disk has 83G free
- Pattern suggests uncoordinated cleanup step in some agent's task
- System reboot 06:03 UTC wiped /tmp and killed renders; deleter has not reappeared post-reboot
- Post-reboot B5 re-render: 36/36 clean
- **Current state:** Only 45 bc-*.mp4 files present (B5 only); 153 B1–B4 files MISSING
- **Action required:** Investigate deleter BEFORE dispatching B6–B12 renders
- Rerender script exists: `~/workspace/apex-audit/.work/rerender_b1b4.py` (not currently running)

### Status Summary
| Batch | Videos | Generator | Rendered | Wired | Deployed |
|---|---|---|---|---|---|
| B5 | 36 | ✅ Ready | 🔄 In progress | ⏳ | ⏳ |
| B6 | 36 | ✅ Ready | ⏳ Queued | ⏳ | ⏳ |
| B7 | 36 | ✅ Ready | ⏳ Queued | ⏳ | ⏳ |
| B8 | 36 | ✅ Ready | ⏳ Queued | ⏳ | ⏳ |
| B9 | 36 | ✅ Ready | ⏳ Queued | ⏳ | ⏳ |
| B10 | 36 | ✅ Ready | ⏳ Queued | ⏳ | ⏳ |
| B11 | 36 | ✅ Ready | ⏳ Queued | ⏳ | ⏳ |
| B12 | 24 | ✅ Ready | ⏳ Queued | ⏳ | ⏳ |
