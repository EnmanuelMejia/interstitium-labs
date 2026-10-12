#!/usr/bin/env python3
"""Wire Batch B11 bootcamp videos into the 12 bootcamp content.json files.
Appends a top-level "videos" array (3 entries per bootcamp) to each
~/workspace/cert-bootcamps/site/bootcamps/<slug>/content.json.

Batch B11 (Career/Human): career-launch, deep-work, edward-bernays, electrician-apprentice, embedded-interview, entrepreneurship, frontier-path, full-spectrum-dominance, hermetica, humanmetrics, occult-esoteric, philosophy.

Safety: backup each content.json to bootcamp-video-backups-b11/ BEFORE editing;
write via temp file + os.replace; json.load re-validation; parsed old-vs-new
JSON equality on every key EXCEPT "videos" (append-only guarantee).
Run with --stamp after deploy verification to set verifiedUtc/httpStatus=200.
"""
import json, os, sys, shutil, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_bootcamp_b11 as G

BOOTCAMPS = os.path.expanduser("~/workspace/cert-bootcamps/site/bootcamps")
BACKUP_DIR = os.path.join(HERE, "bootcamp-video-backups-b11")
STAMP = "--stamp" in sys.argv

EXPECTED = {
    "career-launch",
    "deep-work",
    "edward-bernays",
    "electrician-apprentice",
    "embedded-interview",
    "entrepreneurship",
    "frontier-path",
    "full-spectrum-dominance",
    "hermetica",
    "humanmetrics",
    "occult-esoteric",
    "philosophy"
}

def main():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    by_bootcamp = {}
    for v in G.VIDEOS:
        by_bootcamp.setdefault(v["bootcamp"], []).append(v)
    assert set(by_bootcamp) == EXPECTED, "registry bootcamp mismatch: %s" % sorted(by_bootcamp)
    assert all(len(v) == 3 for v in by_bootcamp.values()), "each bootcamp must have exactly 3 videos"

    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total_added = 0
    for slug, vids in sorted(by_bootcamp.items()):
        path = os.path.join(BOOTCAMPS, slug, "content.json")
        bak = os.path.join(BACKUP_DIR, slug + ".content.json")
        if not os.path.exists(bak):
            shutil.copy2(path, bak)
        with open(path) as f:
            old_text = f.read()
        data = json.loads(old_text)

        vids_list = data.setdefault("videos", [])
        for v in vids:
            url = "/assets/videos/" + v["file"]
            match = next((e for e in vids_list if e.get("url") == url), None)
            if match is None:
                entry = {
                    "title": v["title"],
                    "url": url,
                    "source": "Interstitium Labs",
                    "blurb": v["blurb"] + " (Preview \u2014 narration coming; voiceover pending TTS restore.)",
                    "durationMin": 1,
                    "order": len(vids_list) + 1,
                    "preview": True,
                }
                vids_list.append(entry)
                match = entry
                total_added += 1
            if STAMP:
                match["verifiedUtc"] = now_utc
                match["httpStatus"] = 200
            base = "/assets/videos/" + os.path.splitext(v["file"])[0]
            match["captionsUrl"] = base + ".vtt"
            match["narrationUrl"] = base + ".narration.md"

        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(tmp) as f:
            check = json.load(f)
        # append-only guarantee: every key except "videos" must be byte-identical
        old = json.loads(old_text)
        for k in old:
            if k == "videos":
                continue  # managed key: stamp pass legitimately adds verifiedUtc/httpStatus
            assert k in check, "KEY LOST: %s in %s" % (k, slug)
            assert check[k] == old[k], "KEY MUTATED: %s in %s" % (k, slug)
        assert len(check) == len(old) + (0 if "videos" in old else 1), \
            "unexpected key count change in %s" % slug
        assert len(check["videos"]) == len(vids), "videos array wrong length in %s" % slug
        os.replace(tmp, path)
        print("wired %s: %d videos (%s)" % (slug, len(vids),
              "stamped" if STAMP else "preview, unstamped"), flush=True)
    print("TOTAL entries added this run:", total_added, flush=True)

if __name__ == "__main__":
    main()
