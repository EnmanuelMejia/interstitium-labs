# W6 Report — Bootcamps Batch: Inline Diagrams (ANIMATED)

**Worker:** W6 · **Date:** 2026-10-09 ~02:15–02:45 EDT · **Status:** COMPLETE

## Headline
- **1,821 animated SVG diagrams delivered** = 607 lessons × 3, across **135 bootcamps** (skipped `_engine/` source dir and `engine/` engine-source dir, neither has content.json).
- **Every W6 diagram is animated**: `d.animate()` called before `d.render_svg()` on all 1,821 (staggered node pop-ins, flowing dashes on arrows, `prefers-reduced-motion` static fallback; animation CSS embedded in each SVG file). Assertion in the generator verified `il-anim` + keyframes in every output.
- 3 diagram types per lesson, rotated across 4 rotation sets (flow / layers / compare / table_schema / concept_box pairs), each tailored to the lesson's actual `concepts[]`, `pitfalls[]`, and title — labels are mined from concept sentences (colon-head extraction), not generic.
- Media entries appended (not replaced): `{"id":"<slug>-<topic>-dN","kind":"diagram","title":"<lesson> — <topic>","svg":"assets/diagrams/<file>.svg","lesson_ref":"c-<domain_id>","caption":"<dynamic caption>","alt":"Animated diagram: ..."}`.

## Safety
- Backup `content.json.diagbak` created per bootcamp (135; `cp -n`, never overwritten).
- JSON validated (`json.load`) after every write; atomic `os.replace` writes.
- No duplicate media ids introduced; all 1,821 referenced SVG files exist on disk.

## Corrections handled mid-run (per the 02:15 EDT user order)
1. **Animation mandate**: I had not yet generated any SVGs when the correction arrived, so `d.animate()` was built into the generator from the start. All 1,821 verified animated.
2. **cism double-run**: the dry-run bootcamp (`cism`) got 15 entries from the test + 15 from the full run. Removed all 30 W6-pattern entries and re-ran cleanly → exactly 15 (3 × 5 lessons).
3. **4 legacy static diagrams re-animated in place** (earlier batches' files, same ids/paths, alt text updated):
   - `kubernetes-sre-d2.svg` — reliability practice loop (animated flow)
   - `k8s-cka-exceed-d2.svg` — six hardening layers (animated layers)
   - `iac-terraform-gitops-d2.svg` — ArgoCD push-to-healthy (animated flow)
   - `devops-zero-to-hire-d2.svg` — DevOps infinity loop (animated flow)

## Out of scope — flagged for coordinator
**530 pre-existing static SVGs remain** (from earlier batches; 516 matched 1-per-lesson diagrams + 14 junk-template leftovers). I did NOT regenerate these — they're another batch's hand-crafted content and re-templating them would be destructive. Full list saved at:
`~/workspace/apex-audit/.work/inline-diagrams/w6-static-remaining.txt`
Coordinator should dispatch re-animation for those files.

## Files produced
- Generator: `~/workspace/apex-audit/.work/inline-diagrams/w6_gen.py`
- Cleanup + re-animate helpers: `w6_cism_fix.py`, `w6_reanimate.py`
- Per-bootcamp counts: `w6-perbootcamp.json`
- Static-remaining list: `w6-static-remaining.txt`
- Diagrams: `<bootcamp>/assets/diagrams/<slug>-<topic>-d{1,2,3}.svg` (v-suffix variants where two lessons share a domain_id)

## Per-bootcamp counts
| Bootcamp | Diagrams |
|---|---|
| acad-career | 3 |
| acad-cloud | 3 |
| acad-command | 3 |
| acad-cyber | 3 |
| acad-data | 3 |
| acad-forge | 3 |
| acad-hermetica | 3 |
| acad-math | 3 |
| acad-systems | 3 |
| acad-theory | 3 |
| active-directory-defense | 6 |
| adaptive-foundations | 3 |
| ai-agent-sec | 3 |
| ai-lab | 3 |
| ai-product | 21 |
| alan-turing | 3 |
| aleks-ops-math | 3 |
| android-interview | 3 |
| aws-clf | 21 |
| aws-cloud-practitioner-plus | 3 |
| aws-data | 21 |
| aws-dop | 18 |
| aws-ml | 21 |
| aws-saa | 21 |
| aws-scs | 21 |
| aws-soa | 24 |
| az-104 | 21 |
| az-305 | 21 |
| az-700 | 21 |
| azure-developer | 21 |
| blockchain-dev | 21 |
| c-lang | 21 |
| career-launch | 21 |
| cisco-ccna | 30 |
| cism | 15 |
| cissp | 27 |
| cka | 21 |
| ckad | 21 |
| comptia-a-plus | 24 |
| comptia-core | 21 |
| comptia-cyber | 21 |
| comptia-infra | 21 |
| comptia-network-plus | 30 |
| comptia-security-plus | 30 |
| cpp | 21 |
| creative-code | 21 |
| cybernetics | 3 |
| data-analyst | 21 |
| data-analyst-to-ml | 3 |
| data-engineering | 21 |
| data-science-certs | 3 |
| datascience-ml | 21 |
| deep-learning | 3 |
| deep-work | 3 |
| devops-zero-to-hire | 3 |
| devsecops-mastery | 3 |
| docker | 18 |
| dod-8140 | 21 |
| dotnet | 21 |
| dp-203 | 21 |
| dsa | 21 |
| edward-bernays | 3 |
| electrician-apprentice | 3 |
| embedded-interview | 3 |
| enochian-programming | 3 |
| entrepreneurship | 3 |
| fde-training | 3 |
| frontier-path | 3 |
| full-spectrum-dominance | 27 |
| fullstack | 21 |
| fullstack-desk | 3 |
| git-devops | 18 |
| hackers-arise | 21 |
| hermetica | 24 |
| humanmetrics | 3 |
| iac-terraform-gitops | 3 |
| ides-tooling | 21 |
| il12-ai-engineering | 3 |
| ios-interview | 3 |
| isc2-cc | 30 |
| java | 21 |
| k8s-associate | 21 |
| k8s-cka-exceed | 3 |
| kubernetes-sre | 3 |
| linux-essentials | 24 |
| llm-engineering | 21 |
| m365 | 21 |
| m365-endpoint-admin | 24 |
| math-tech | 21 |
| ml-defense | 6 |
| mongodb | 21 |
| ms-fundamentals | 15 |
| neuroai | 3 |
| nice-framework | 27 |
| nlp-advanced | 3 |
| nlp-engineering | 3 |
| nsa-codebreaker | 21 |
| nvidia-ai | 21 |
| occult-esoteric | 3 |
| openshift | 24 |
| oracle-db | 21 |
| oracle-oci | 21 |
| oracle-sql | 21 |
| pentest | 21 |
| philosophy | 3 |
| platform-engineering | 3 |
| python | 21 |
| python-systems | 3 |
| python-web | 21 |
| quant-finance-ladder | 3 |
| quant-finance-math | 3 |
| quantum | 3 |
| react-frontend | 21 |
| rhce | 18 |
| rhcsa | 24 |
| roles-library | 3 |
| sc-200 | 21 |
| sc-300 | 21 |
| secops-blue-team | 6 |
| security-graphs | 9 |
| soc-analyst | 21 |
| spring | 21 |
| sql | 21 |
| sre-platform | 18 |
| sre-practices | 3 |
| study-protocol | 6 |
| systems-cs | 21 |
| terraform | 18 |
| tl-endpoint-ops | 3 |
| tl-interview | 6 |
| vault-consul | 21 |
| vendor-map | 3 |
| windows-admin | 3 |
| zero-trust | 6 |
| zerotrust | 18 |