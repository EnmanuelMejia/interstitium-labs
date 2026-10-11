# Theme Category Audit — interstitiumlabs.dev/topics/ (2026-10-10)

Findings only. Source: `~/workspace/apex-audit/docs/topics/`. Live checked via text fetch (browser.open) + source HTML inspection.

## /topics/ index page — OK
- Lists all 16 themes with working links to `/topics/<slug>/`.
- Shows course/bootcamp counts for 12 themes; NO counts shown for crypto, cybernetics, esoteric, om.
- Minor grammar nit on index: "1 courses · 4 bootcamps" (should be "1 course").
- Counts on index roughly match page content (e.g. Cybersecurity 6 courses · 22 bootcamps).

## Theme table (LIVE status)

| # | Theme | Slug | Status | What exists (live) | Gaps (live) |
|---|-------|------|--------|--------------------|-------------|
| 1 | Cybersecurity | cybersecurity | RICH | 6 courses, 12 bootcamps, Media & Guides, 3 learning paths | none material |
| 2 | System Design | system-design | THIN | 2 courses, 5 bootcamps, Media & Guides | NO Learning paths section |
| 3 | Networking | networking | THIN | 1 course ("Systems, Linux, Windows & Networks" — generic, shared with Linux & Systems), 4 bootcamps, Media & Guides | only 1 course; no learning paths |
| 4 | Cloud & DevOps | cloud-devops | RICH | 4 courses, 12 bootcamps, Media & Guides, 7 learning paths | none material |
| 5 | AI & ML | ai-ml | RICH | 4 courses, 12 bootcamps (per index), 1 learning path (NVIDIA Free AI Course Track), algo-animation section | none material |
| 6 | Data Engineering | data-eng | RICH | 3 courses (incl. IL-26), 11 bootcamps, 2 learning paths, algo-animation section | none material |
| 7 | Programming | programming | THIN (live) | 12 bootcamps, Media & Guides only | NO courses live; NO learning paths live. Source HTML already adds 3 courses (Programming Language Forge, Algorithms/Compilers/Distributed & Formal, Software Engineering Interview Prep) + 1 path — not yet deployed |
| 8 | Databases | databases | THIN (live) | 4 bootcamps (Sql, Mongodb, Oracle Sql, Oracle Db), Media & Guides only | NO courses live; NO learning paths. Source HTML already adds 1 course (SQL, Data Engineering, Analytics & AI) — not yet deployed |
| 9 | Linux & Systems | linux-systems | RICH | 1 course, 11 bootcamps, 2 learning paths, Media & Guides | only 1 course (shared title with Networking) |
| 10 | Mathematics (Turing) | math | RICH | 2 courses, 5 bootcamps, 1 learning path, math-animation section | page renders as "Alan Turing" — matches theme |
| 11 | Web Development | web-dev | THIN | 1 course (Programming Language Forge), 3 bootcamps, 1 learning path ("Full-stack desk") | only 1 course; only 3 bootcamps; no web-specific course |
| 12 | Blockchain | blockchain | EMPTY (live) | Hero + Media & Guides only — zero courses, zero bootcamps, zero learning paths | everything. Source HTML already adds 1 course (The Frontier) + 1 bootcamp (Blockchain Dev) — not yet deployed |
| 13 | Cryptocurrency (XRP) | crypto | THIN | 2 courses (The Frontier, Post-Quantum Cryptography), 1 bootcamp (Blockchain Dev), Media & Guides | only 1 bootcamp; NO learning paths |
| 14 | Cybernetics | cybernetics | EMPTY (live) | Hero + Media & Guides only — zero courses, zero bootcamps, zero learning paths | everything. Source HTML already adds 2 courses (Algorithms/Compilers/Distributed & Formal, The Frontier) — not yet deployed |
| 15 | Esoteric (John Dee) | esoteric | THIN | 2 courses (Esoteric Traditions & Digital Hermetica, The Deep Library), 1 learning path, Media & Guides | NO Bootcamps section at all |
| 16 | Om | om | EMPTY | Hero + Media & Guides + 1 learning path ("Adaptive Foundations" — generic math+CS remediation, NOT Om-specific) | zero courses, zero bootcamps. Hero "Start learning" CTA points to il-23-frontier-knowledge (not Om content). Source HTML has no courses/bootcamps either — Om is empty in source too |

## Notes
- "Media & Guides" is boilerplate on all 16 pages (Visual guides / Cinema / Noah AI) — not real theme content.
- Bootcamp card descriptions are all identical boilerplate ("Interactive certification prep bootcamp.").
- All themes have themed heroes (video + tagline) — present on all 16.
- Source-vs-live drift: `~/workspace/apex-audit/docs/_deploy_stamp.txt` reads 20261007T110032Z, but theme source files were modified Oct 10 00:14 — source is NEWER than the recorded deploy. programming, databases, blockchain, cybernetics gained content sections in source that are NOT live yet.
- Om is the only theme with no course content even in source.

## Status summary
- RICH: cybersecurity, cloud-devops, ai-ml, data-eng, linux-systems, math (6)
- THIN: system-design, networking, programming, databases, web-dev, crypto, esoteric (7)
- EMPTY: blockchain, cybernetics, om (3, all empty on live)
