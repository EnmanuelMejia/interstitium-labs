#!/usr/bin/env python3
"""Update video-1000pct-buildout.md with Batch B10 completion."""
import os

PATH = os.path.expanduser("~/workspace/apex-audit/.work/video-1000pct-buildout.md")
with open(PATH) as f:
    lines = f.readlines()

# 1) Insert the B10 batch section before the Totals header
totals_idx = next(i for i, l in enumerate(lines)
                  if l.rstrip("\n") == "## Totals (Combined — Two Parallel Builders)")
assert totals_idx > 0 and lines[totals_idx - 1].strip() == "", "expected blank line before Totals"

b10_section = """### Bootcamp video Phase 2 — Batch B10 (Dev/Misc ×12): 36 videos
- [x] Generating — 36/36 rendered 2026-10-09 ~04:30 EDT / ~08:30 UTC (all 30s, 1280x720@24fps, h264+aac-silent, burned-in captions, "Preview — narration coming" tag; SMOKE pass 36/36 clean + 5 full-length style probes (bbg/3b1b/fireship/primer/story) all ffprobe-clean before the batch — primer×10/bbg×10/fireship×6/story×6/3b1b×4; render log .work/b10-fullbatch.log; each with .vtt captions + .narration.md script staged alongside; collision pre-check clean — zero cross-batch filename collisions against docs/assets/videos/ and all B1–B9 sibling gen scripts)
- [x] Wired — 36 entries appended as top-level "videos" arrays in blockchain-dev/creative-code/enochian-programming/fullstack-desk/git-devops/ides-tooling/platform-engineering/python-systems/sre-platform/sre-practices/systems-cs/vault-consul content.json under ~/workspace/cert-bootcamps/site/bootcamps/ (source: "Interstitium Labs", preview: true, captionsUrl + narrationUrl, verifiedUtc + httpStatus 200 stamped via --stamp pass; backups in .work/bootcamp-video-backups-b10/; append-only: parsed old-vs-new equality on every other key; all 12 dirs confirmed clean with no pre-existing videos arrays)
- [x] Deployed (1/2) — flagship deploy-worker-assets, solitary-sound-015a, etag 136a0f618590, modified 2026-10-09T08:30:09.971803Z (23 files uploaded, manifest 3409 files; log .work/bootcamp_b10_deploy_flagship.log)
- [x] Deployed (2/2) — cert-bootcamps worker redeployed via ~/workspace/apex-audit/.work/certbootcamps-deploy-config-20261009.json (absolute assets_dir — the proven path), modified 2026-10-09T08:32:48.780681Z (12 files uploaded: the 12 stamped B10 content.json; log .work/bootcamp_b10_deploy_certbootcamps.log) — the wired "videos" arrays are LIVE
- [x] Verified — all 108 files (36 mp4 + 36 .vtt + 36 .narration.md) return HTTP 200 at https://interstitiumlabs.dev/assets/videos/ (browser-UA GET-range probes; results saved to .work/b10-verify-results.txt)
- ⚠️ INCIDENTS: (1) the runtime terminated the full-batch background process at video 30/36 (session vanished, no ffmpeg alive) — re-ran the remaining 6 via .work/run_b10_catchup.py (all 6 OK, zero failures); (2) while re-launching, killed a redundant second full-batch attempt mid-render of its first file, leaving a partial 2.79s bc-primer-bcd-chain.mp4 — caught by the ffprobe sweep on all 36, re-rendered clean once (verified h264/1280x720/30.0s, same deterministic byte size 228968). No deleter strikes during the render window. Deleter watch post-deploy: 342 bc-* MP4s locally (unchanged from pre-batch baseline), 5/5 B1–B9 CDN spot samples (incl. both collision-repair files bc-bbg-m365-compliance, bc-bbg-m365-pipeline) HTTP 200.

Batch B10 files (3 per bootcamp, bc- prefixed): blockchain-dev — bc-primer-bcd-chain, bc-fireship-bcd-solidity, bc-bbg-bcd-consensus; creative-code — bc-primer-cr-generative, bc-fireship-cr-shader, bc-story-cr-installation; enochian-programming — bc-bbg-eno-calls, bc-primer-eno-tablets, bc-story-eno-ritual; git-devops — bc-primer-git-branch, bc-fireship-git-rebase, bc-bbg-git-cicd; ides-tooling — bc-primer-ide-debug, bc-3b1b-ide-keys, bc-bbg-ide-extensions; platform-engineering — bc-bbg-plat-idp, bc-fireship-plat-golden, bc-story-plat-adopt; python-systems — bc-primer-pys-asyncio, bc-fireship-pys-cffi, bc-bbg-pys-packaging; sre-platform — bc-3b1b-srep-slo, bc-bbg-srep-observability, bc-story-srep-incident; sre-practices — bc-story-srepr-blameless, bc-primer-srepr-chaos, bc-3b1b-srepr-toil; systems-cs — bc-primer-sys-syscall, bc-bbg-sys-virtual, bc-3b1b-sys-amdahl; vault-consul — bc-primer-vc-secrets, bc-fireship-vc-policy, bc-bbg-vc-mesh; fullstack-desk — bc-story-fsd-day, bc-bbg-fsd-ticket, bc-primer-fsd-standup. Generator: ~/workspace/apex-audit/.work/gen_bootcamp_b10.py; wiring: wire_bootcamp_b10.py (backups in bootcamp-video-backups-b10/).

"""

insert_lines = [b10_section]
new_lines = lines[:totals_idx] + insert_lines + lines[totals_idx:]

# 2) Totals updates
def sub(old, new):
    global new_lines
    hits = [i for i, l in enumerate(new_lines) if old in l]
    assert hits, "not found: %r" % old
    for i in hits:
        new_lines[i] = new_lines[i].replace(old, new)

sub("- **Total videos live:** ~499 MP4s (16 original + 87 Builder A + 87 Builder B + 3 misc + 30 Bootcamp B1 + 24 Bootcamp B2 + 36 Bootcamp B3 + 36 Bootcamp B4 + 36 Bootcamp B5 + 36 Bootcamp B6 + 36 Bootcamp B7 + 36 Bootcamp B8 + 36 Bootcamp B9); local docs/assets/videos holds 496 MP4s (306 bc-*), CDN verify shows no losses",
    "- **Total videos live:** ~535 MP4s (16 original + 87 Builder A + 87 Builder B + 3 misc + 30 Bootcamp B1 + 24 Bootcamp B2 + 36 Bootcamp B3 + 36 Bootcamp B4 + 36 Bootcamp B5 + 36 Bootcamp B6 + 36 Bootcamp B7 + 36 Bootcamp B8 + 36 Bootcamp B9 + 36 Bootcamp B10); local docs/assets/videos holds 532 MP4s (342 bc-*), CDN verify shows no losses")
sub("- **Bootcamps with video:** 102 / 143 (acad Batch B1 + cyber Batch B2 + infra/cloud Batch B3 + data/ML Batch B4 + programming/dev Batch B5 + cloud-certs Batch B6 + security-certs Batch B7 + K8s/Linux/infra Batch B8 + Data/AI Batch B9 done; 41 remaining — gen_bootcamp_b10.py already prepped by a sibling)",
    "- **Bootcamps with video:** 114 / 143 (acad Batch B1 + cyber Batch B2 + infra/cloud Batch B3 + data/ML Batch B4 + programming/dev Batch B5 + cloud-certs Batch B6 + security-certs Batch B7 + K8s/Linux/infra Batch B8 + Data/AI Batch B9 + Dev/Misc Batch B10 done; 29 remaining — no B11 generator prepped yet)")
sub("- **Voiceover:** blocked on TTS restore (all 300 buildout videos ship as captioned previews with complete narration scripts staged)",
    "- **Voiceover:** blocked on TTS restore (all 336 buildout videos ship as captioned previews with complete narration scripts staged)")

# 3) Monitor-run log line
run_line = ("\n- **Batch B10 COMPLETE 2026-10-09 ~04:33 EDT:** builder handoff received — 36/36 rendered "
    "(Dev/Misc cluster: blockchain-dev, creative-code, enochian-programming, git-devops, ides-tooling, "
    "platform-engineering, python-systems, sre-platform, sre-practices, systems-cs, vault-consul, fullstack-desk; "
    "primer×10/bbg×10/fireship×6/story×6/3b1b×4; smoke 36/36 + 5 probes clean, ffprobe 30s on all 36), "
    "wired into 12 content.json (append-only, backups in bootcamp-video-backups-b10/), TWO deploys done "
    "(flagship solitary-sound-015a modified 2026-10-09T08:30:09Z, 23 files; cert-bootcamps worker modified "
    "2026-10-09T08:32:48Z — 12 stamped arrays LIVE), 108/108 files verified HTTP 200 (browser-UA GET-range probes). "
    "Incidents: runtime terminated the batch process at 30/36 — caught up via scoped re-run; one partial "
    "bc-primer-bcd-chain.mp4 from a killed redundant re-launch — re-rendered clean once (one clean retry per policy). "
    "No deleter re-strike (342 bc-* MP4s locally, unchanged; 5/5 B1–B9 CDN spot samples 200). "
    "Bootcamp coverage 114/143, ~535 MP4s live. Voiceover still blocked on TTS restore. "
    "NOTE: no gen_bootcamp_b11.py exists — next monitor run starts a fresh 2-run stall count before spawning B11.\n")

with open(PATH, "w") as f:
    f.writelines(new_lines)
with open(PATH, "a") as f:
    f.write(run_line)
print("updated OK")
