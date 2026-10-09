#!/usr/bin/env python3
"""S3: Add og:image + twitter:image (+ dimensions) to all 135 bootcamp pages.
Inserts after the <title> line in each site/bootcamps/{slug}/index.html."""
import os, re

BASE = "/home/hatch/workspace/cert-bootcamps/site/bootcamps"
SITE = "https://interstitiumlabs.dev"
done, skipped, already = 0, 0, []

for slug in sorted(os.listdir(BASE)):
    idx = os.path.join(BASE, slug, "index.html")
    if not os.path.isfile(idx):
        continue
    html = open(idx, encoding="utf-8").read()
    if 'property="og:image"' in html:
        already.append(slug)
        continue
    og = f"{SITE}/assets/cinematic/bootcamps-og/{slug}-og.png"
    tags = (
        f'<meta property="og:image" content="{og}">\n'
        f'<meta property="og:image:width" content="1200">\n'
        f'<meta property="og:image:height" content="630">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:image" content="{og}">'
    )
    new_html, n = re.subn(r"(<title>.*?</title>)", r"\1\n" + tags, html, count=1)
    if n != 1:
        skipped.append(slug)
        continue
    open(idx, "w", encoding="utf-8").write(new_html)
    done += 1

print(f"bootcamp OG tags added: {done} | already had og:image: {len(already)} | skipped (no <title>): {skipped}")
# verify every bootcamp png exists
missing = [s for s in os.listdir(BASE)
           if os.path.isfile(os.path.join(BASE, s, "index.html"))
           and not os.path.exists(f"/home/hatch/workspace/apex-audit/docs/assets/cinematic/bootcamps-og/{s}-og.png")]
print("slugs missing og png:", missing or "none")
