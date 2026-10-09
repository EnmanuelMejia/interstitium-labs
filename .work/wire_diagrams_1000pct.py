#!/usr/bin/env python3
"""Wire generated SVG diagrams into bootcamp content.json media[] arrays.

Safety: backup each content.json to bootcamp-json-backups-embed/ BEFORE editing;
write via temp file + os.replace; json.load re-validation; append-only guarantee
(every key except "media" must be byte-identical after the edit).
"""
import json, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.expanduser("~/workspace/cert-bootcamps/site/bootcamps")
BACKUP_DIR = os.path.join(HERE, "bootcamp-json-backups-embed")
MANIFEST = os.path.join(HERE, "diagram-manifest-20261009.json")

def main():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    manifest = json.load(open(MANIFEST))
    by_slug = {}
    for e in manifest:
        by_slug.setdefault(e["slug"], []).append(e["entry"])

    total_added = 0
    for slug in sorted(by_slug):
        path = os.path.join(BASE, slug, "content.json")
        bak = os.path.join(BACKUP_DIR, slug + ".content.json")
        if not os.path.exists(bak):
            shutil.copy2(path, bak)
        with open(path) as f:
            old_text = f.read()
        data = json.loads(old_text)

        media = data.setdefault("media", [])
        have = {m.get("lesson_ref") for m in media if isinstance(m, dict)}
        for entry in by_slug[slug]:
            if entry["lesson_ref"] in have:
                print("SKIP dup %s %s" % (slug, entry["lesson_ref"]))
                continue
            media.append(entry)
            total_added += 1

        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(tmp) as f:
            check = json.load(f)
        old = json.loads(old_text)
        for k in old:
            if k == "media":
                continue
            assert k in check, "KEY LOST: %s in %s" % (k, slug)
            assert check[k] == old[k], "KEY MUTATED: %s in %s" % (k, slug)
        assert len(check) == len(old) + (0 if "media" in old else 1), \
            "unexpected key count change in %s" % slug
        os.replace(tmp, path)
        print("wired %s: media[] now %d entries" % (slug, len(check["media"])))
    print("TOTAL media entries added this run:", total_added)

if __name__ == "__main__":
    main()
