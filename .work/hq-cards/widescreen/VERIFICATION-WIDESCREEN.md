# Widescreen HQ Card Verification

Date: 2026-10-09 ~03:05 EDT
Dir: ~/workspace/apex-audit/.work/hq-cards/widescreen/

## Batch 1 (standard widescreen prompts)

| File | Res | FPS | Dur | Codec | Video bitrate | Audio |
|---|---|---|---|---|---|---|
| widescreen-01-il29-threatlocke-*.mp4 | 1280x720 | 24 | 10.0s | h264 | 3,928,044 | AAC 24kHz |
| widescreen-02-il28-devsecops-*.mp4 | 1280x720 | 24 | 10.0s | h264 | 2,844,653 | AAC 24kHz |
| widescreen-03-il26-data-analys-*.mp4 | 1280x720 | 24 | 10.0s | h264 | 3,489,248 | AAC 24kHz |
| widescreen-04-devops-superlab-*.mp4 | 1280x720 | 24 | 10.0s | h264 | 4,487,625 | AAC 24kHz |
| widescreen-05-rhel-fabric-*.mp4 | 1280x720 | 24 | 10.0s | h264 | 4,846,178 | AAC 24kHz |
| widescreen-06-bootcamp-catalog-*.mp4 | 1280x720 | 24 | 10.0s | h264 | 4,343,569 | AAC 24kHz |

## Batch 2 (max-fidelity prompts: "ultra high detail, maximum quality, sharp focus, premium cinematic rendering")

| File | Res | FPS | Dur | Codec | Video bitrate | Audio | Delta vs batch 1 |
|---|---|---|---|---|---|---|---|
| hq-widescreen-01-il29-threatlo-*.mp4 | 1280x720 | 24 | 10.0s | h264 | 4,037,054 | AAC 24kHz | +2.8% |
| hq-widescreen-02-il28-devsecop-*.mp4 | 1280x720 | 24 | 10.0s | h264 | 3,089,353 | AAC 24kHz | +8.6% |
| hq-widescreen-03-il26-data-ana-*.mp4 | 1280x720 | 24 | 10.0s | h264 | 3,347,729 | AAC 24kHz | -4.1% |
| hq-widescreen-04-devops-superl-*.mp4 | 1280x720 | 24 | 10.0s | h264 | 4,050,876 | AAC 24kHz | -9.7% |
| hq-widescreen-05-rhel-fabric-*.mp4 | 1280x720 | 24 | 10.0s | h264 | 4,293,477 | AAC 24kHz | -11.4% |
| hq-widescreen-06-bootcamp-cata-*.mp4 | 1280x720 | 24 | 10.0s | h264 | 3,432,103 | AAC 24kHz | -21.0% |

## Honest flag

The 16:9 widescreen prompt was honored on both passes (true 1280x720, not 9:16). But prompt-level
"maximum quality" language does NOT raise the pipeline's encoder ceiling: 4 of 6 batch-2 files
came back at LOWER bitrate than batch 1. Bitrate reflects scene complexity/motion as much as
quality, so batch 2 is not proven worse — but it is not proven better either. The pipeline appears
to use fixed encoding settings; fidelity phrasing in the prompt cannot force a higher bitrate.

Recommendation: keep BOTH batches available. The parent should visually A/B the two passes per
card (composition/detail may differ even when bitrate doesn't) and ship the better-looking one.
Do not delete batch 1 based on this data alone.

Full file paths:
- Batch 1: ~/workspace/apex-audit/.work/hq-cards/widescreen/media-generation-widescreen-*.mp4
- Batch 2: ~/workspace/apex-audit/.work/hq-cards/widescreen/media-generation-hq-widescreen-*.mp4
