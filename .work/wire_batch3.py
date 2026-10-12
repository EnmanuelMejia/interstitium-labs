#!/usr/bin/env python3
"""Wire Batch 3 videos into IL-15..IL-21 course JSONs: append to modules[].videos[].
Mirrors wire_batch2.py: read, validate, write temp, re-validate, os.replace. Backups first.
Run with --stamp after deploy verification to set verifiedUtc/httpStatus=200.
"""
import json, os, sys, shutil, datetime, re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_batch3 as G

COURSES = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
BACKUP_DIR = os.path.join(HERE, "course-json-backups-batch3")
STAMP = "--stamp" in sys.argv

def course_no(v):
    m = re.match(r"IL-(\d+)", v["kicker"])
    return int(m.group(1))

def main():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    by_course = {}
    for v in G.VIDEOS:
        by_course.setdefault(course_no(v), []).append(v)

    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total_added = 0
    for cno, vids in sorted(by_course.items()):
        fname = G.COURSE_FILES[cno]
        path = os.path.join(COURSES, fname)
        bak = os.path.join(BACKUP_DIR, fname)
        if not os.path.exists(bak):
            shutil.copy2(path, bak)
        with open(path) as f:
            data = json.load(f)
        mods = data["modules"]
        for v in vids:
            mi = v["module"]
            if not (0 <= mi < len(mods)):
                raise IndexError("module index %d out of range for IL-%02d (%d modules)"
                                 % (mi, cno, len(mods)))
            mod = mods[mi]
            vids_list = mod.setdefault("videos", [])
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
                    "watchBefore": "notes",
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
        assert len(check["modules"]) == len(mods), "module count changed!"
        os.replace(tmp, path)
        print("wired %s: %d batch3 videos (%s)" % (fname, len(vids),
              "stamped" if STAMP else "preview, unstamped"), flush=True)
    print("TOTAL entries added this run:", total_added, flush=True)

if __name__ == "__main__":
    main()
