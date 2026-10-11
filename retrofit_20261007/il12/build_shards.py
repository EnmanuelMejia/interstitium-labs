#!/usr/bin/env python3
"""IL-12 shard retrofit — ensures every path-module entry in shard-l/m has:
topics (string list), sources [{name,url,note}], il_provides (2-3 sentence
instructor-voice blurb). One-sentence blurbs get their original preserved
verbatim plus an appended second sentence. Everything else preserved.
Fresh json.load immediately before edits; atomic writes; validate after.
"""
import json, os, re, sys, importlib.util

BASE = os.path.expanduser("~/workspace/apex-audit")
RETRO = os.path.join(BASE, "retrofit_20261007", "il12")
SHARDS = {
    "l": os.path.join(BASE, "docs/university/data/catalog/shard-l.json"),
    "m": os.path.join(BASE, "docs/university/data/catalog/shard-m.json"),
}

def load_ilp():
    path = os.path.join(RETRO, "shard_ilp.py")
    spec = importlib.util.spec_from_file_location("shard_ilp", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ILP_SECOND

def sentences(s):
    return [x for x in re.split(r"[.!?]\s+", s.strip()) if x]

def main():
    ilp_second = load_ilp()
    for sn, path in SHARDS.items():
        # FRESH load immediately before edits (sibling-safe)
        with open(path, encoding="utf-8") as f:
            d = json.load(f)

        expanded, problems = 0, []
        for p in d.get("paths", []):
            for mo in p.get("modules", []):
                key = f"{sn}/{p['id']}/{mo['id']}"
                t = mo.get("topics")
                if not (isinstance(t, list) and t and all(isinstance(x, str) and x.strip() for x in t)):
                    problems.append(f"{key}: topics not a non-empty string list")
                s = mo.get("sources")
                if not (isinstance(s, list) and s and all(
                        isinstance(x, dict) and x.get("name") and x.get("url") and x.get("note")
                        for x in s)):
                    problems.append(f"{key}: sources malformed")
                ip = mo.get("il_provides", "")
                if not (isinstance(ip, str) and ip.strip()):
                    problems.append(f"{key}: il_provides missing")
                    continue
                if len(sentences(ip)) < 2:
                    second = ilp_second.get(key)
                    if not second:
                        problems.append(f"{key}: no expansion text available")
                        continue
                    mo["il_provides"] = ip.rstrip() + " " + second
                    expanded += 1

        if problems:
            print(f"SHARD-{sn.upper()} PROBLEMS:")
            for pr in problems:
                print("  -", pr)
            sys.exit(1)

        tmp = path + ".retrofit_tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
            f.write("\n")
        with open(tmp, encoding="utf-8") as f:
            json.load(f)
        os.replace(tmp, path)
        n_entries = sum(len(p.get("modules", [])) for p in d.get("paths", []))
        print(f"SHARD-{sn.upper()} OK: {n_entries} path entries verified, {expanded} il_provides expanded to 2 sentences")

if __name__ == "__main__":
    main()
