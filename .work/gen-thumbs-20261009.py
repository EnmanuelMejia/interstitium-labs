#!/usr/bin/env python3
"""Generate poster thumbnails (first frame) for all referenced local MP4s.
Course+bootcamp -> docs/assets/videos/thumbnails/<base>.jpg
Portfolio      -> portfolio-site/media/videos/thumbnails/<base>.jpg
Skips files that already have a thumbnail. Idempotent.
"""
import json, glob, os, subprocess, sys

DOCS_VID = "/home/hatch/workspace/apex-audit/docs/assets/videos"
PORT_VID = "/home/hatch/workspace/portfolio-site/media/videos"

def collect(dirs, pattern):
    names = set()
    for f in glob.glob(pattern):
        try:
            d = json.load(open(f))
        except Exception as e:
            print("PARSE FAIL", f, e, file=sys.stderr)
            continue
        s = json.dumps(d)
        import re
        for m in re.finditer(r'"(/(?:assets|media)/videos/[^"]+?\.mp4)"', s):
            names.add(m.group(1).split("/")[-1])
    return names

def gen(src_dir, thumb_dir, basenames):
    os.makedirs(thumb_dir, exist_ok=True)
    done, skipped, failed = 0, 0, 0
    for b in sorted(basenames):
        src = os.path.join(src_dir, b)
        out = os.path.join(thumb_dir, b[:-4] + ".jpg")
        if os.path.exists(out):
            skipped += 1
            continue
        if not os.path.exists(src):
            failed += 1
            continue
        r = subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", src,
             "-vframes", "1", "-q:v", "4", "-vf", "scale=640:-2", out],
            capture_output=True)
        if r.returncode == 0 and os.path.exists(out):
            done += 1
        else:
            failed += 1
            print("FFMPEG FAIL", b, r.stderr.decode()[:200], file=sys.stderr)
    return done, skipped, failed

course_boot = collect(None, "/home/hatch/workspace/apex-audit/docs/university/data/courses/il-*.json")
course_boot |= collect(None, "/home/hatch/workspace/cert-bootcamps/site/bootcamps/*/*.json")
d, s, f = gen(DOCS_VID, os.path.join(DOCS_VID, "thumbnails"), course_boot)
print(f"flagship: generated={d} skipped={skipped if False else s} failed(missing src)={f}")

port = collect(None, "/home/hatch/workspace/portfolio-site/index.html")
# index.html is not JSON; scrape directly
import re
port = set(re.findall(r'/media/videos/([A-Za-z0-9_.-]+\.mp4)', open("/home/hatch/workspace/portfolio-site/index.html").read()))
d2, s2, f2 = gen(PORT_VID, os.path.join(PORT_VID, "thumbnails"), port)
print(f"portfolio: generated={d2} skipped={s2} failed={f2}")
