#!/usr/bin/env python3
"""Social scrape -> course refresh pipeline.

Takes fresh trending STEM/tech signals and folds them into the relevant
Interstitium Labs course JSONs as date-stamped `freshSignals` entries.

Usage:
  python3 social-course-refresh.py --signals-file signals-YYYY-MM-DD.json [--dry-run]
  python3 social-course-refresh.py --from-daily-fold [--dry-run]

Inputs:
  --signals-file   JSON file with {"signals": [...]} — each signal has:
                     id, date, headline, brief, sources[{label,url}],
                     courses[courseId...], tags[], noahPrompt
  --from-daily-fold  Also pull socialSignals from il-trending-catalog.json
                     dailyFold and map them to courses via keywords.

Behavior:
  - For each signal, appends a freshSignals entry to each mapped course JSON
    (dedup by signal id — never double-adds).
  - Keeps only the newest 20 entries per course (prunes old, keeps JSON lean).
  - Writes a run log to .work/social-refresh/run-YYYY-MM-DD.md.
  - Exits 0 with a summary; --dry-run prints what it would do.

Course keyword fallback mapping for dailyFold signals (courseId -> keywords):
"""
import argparse
import glob
import json
import os
import sys
from datetime import date

WORK = "/home/hatch/workspace/apex-audit/.work/social-refresh"
COURSES_DIR = "/home/hatch/workspace/apex-audit/docs/university/data/courses"
CATALOG = "/home/hatch/workspace/apex-audit/docs/assets/il-trending-catalog.json"
MAX_SIGNALS_PER_COURSE = 20

# Fallback keyword mapping: courseId -> keywords (lowercase match on note text)
KEYWORD_MAP = {
    "il-12-ai-engineering": ["claude", "gpt", "llm", "open-weight", "open weight", "mistral", "qwen", "deepseek", "inference", "model release", "frontier model", "coding model", "vision model", "muse spark"],
    "il-17-agentic-ai-engineering": ["agent", "agentic", "manus", "coworker", "autonomous"],
    "il-16-machine-learning-ai-engineering": ["benchmark", "leaderboard", "vision model", "training", "fine-tune"],
    "il-31-ai-red-teaming-safety-evals": ["safety", "eval", "red team", "alignment", "jailbreak", "vulnerability disclosure", "regulation", "catastrophic", "chatbot safety"],
    "il-11-zero-trust-endpoint-defense": ["zero trust", "zscaler", "microsegmentation", "reachability"],
    "il-06-cybersecurity-secure-engineering": ["cve", "zero-day", "vulnerability", "exploit", "breach", "ransomware", "patch", "cisa"],
    "il-29-threatlocker-ai-cybersecurity-mastery": ["zero trust", "endpoint", "allowlist", "threatlocker", "cve", "ot security", "ransomware"],
    "il-24-threatlocker-assessment-prep-cbt": ["threatlocker", "assessment", "cbt"],
    "il-20-mathematics": ["math", "proof", "millennium", "formal"],
    "il-03-programming-language-forge": ["coding model", "code leaderboard", "developer"],
    "il-04-systems-linux-windows-networks": ["hardware", "laptop", "chip", "nvidia", "local inference", "surface"],
    "il-10-portfolio-career-professional-practice": ["hiring", "jobs", "funding", "acquisition", "raise", "ipo"],
    "il-28-devsecops-cloud-infrastructure-mastery": ["devsecops", "ci/cd", "supply chain", "sbom"],
    "il-05-cloud-devsecops-platform-sre": ["cloud", "sre", "kubernetes", "neocloud"],
    "il-26-data-analyst-certification-senior-mastery": ["data analyst", "analytics", "bi ", "dashboard"],
    "il-30-post-quantum-cryptography-quantum-safe": ["quantum", "post-quantum", "nist pqc", "shor"],
    "il-07-data-engineering-analytics-ai": ["data engineering", "pipeline", "etl"],
    "il-02-mathematical-maturity-engine": ["math", "proof", "theorem"],
    "il-23-frontier-knowledge": ["frontier", "world model", "agi"],
}


def load_course_index():
    index = {}
    for f in sorted(glob.glob(os.path.join(COURSES_DIR, "il-*.json"))):
        if ".bak" in f or ".diagbak" in f:
            continue
        try:
            d = json.load(open(f))
            cid = d.get("courseId")
            if cid:
                index[cid] = f
        except Exception as e:
            print(f"  WARN: could not read {f}: {e}", file=sys.stderr)
    return index


def fold_signals(signals, course_index, dry_run=False):
    """Append signals to mapped courses. Returns (added, skipped, errors)."""
    added, skipped, errors = 0, 0, 0
    per_course = {}
    for sig in signals:
        targets = sig.get("courses") or []
        for cid in targets:
            per_course.setdefault(cid, []).append(sig)

    for cid, sigs in per_course.items():
        path = course_index.get(cid)
        if not path:
            print(f"  WARN: unknown courseId {cid} — skipping {len(sigs)} signals", file=sys.stderr)
            errors += len(sigs)
            continue
        try:
            d = json.load(open(path))
        except Exception as e:
            print(f"  WARN: read fail {path}: {e}", file=sys.stderr)
            errors += len(sigs)
            continue
        fs = d.setdefault("freshSignals", [])
        existing_ids = {e.get("id") for e in fs}
        new_entries = []
        for sig in sigs:
            if sig["id"] in existing_ids:
                skipped += 1
                continue
            entry = {
                "id": sig["id"],
                "date": sig.get("date", str(date.today())),
                "headline": sig["headline"],
                "brief": sig["brief"],
                "sources": sig.get("sources", []),
                "tags": sig.get("tags", []),
                "noahPrompt": sig.get("noahPrompt", ""),
            }
            new_entries.append(entry)
            existing_ids.add(sig["id"])
        if new_entries:
            fs.extend(new_entries)
            # prune to newest MAX, keeping chronological order (oldest first)
            if len(fs) > MAX_SIGNALS_PER_COURSE:
                fs[:] = fs[-MAX_SIGNALS_PER_COURSE:]
            d["updatedAt"] = str(date.today())
            if not dry_run:
                tmp = path + ".tmp"
                with open(tmp, "w") as f:
                    json.dump(d, f, indent=2, ensure_ascii=False)
                    f.write("\n")
                os.replace(tmp, path)
            added += len(new_entries)
            print(f"  {cid}: +{len(new_entries)} fresh signals")
    return added, skipped, errors


def signals_from_daily_fold():
    """Map dailyFold socialSignals to courses via keywords. Returns signal list."""
    try:
        cat = json.load(open(CATALOG))
    except Exception as e:
        print(f"  WARN: catalog unreadable: {e}", file=sys.stderr)
        return []
    df = cat.get("dailyFold", {})
    out = []
    for i, s in enumerate(df.get("socialSignals", [])):
        note = s.get("note", "")
        text = note.lower()
        targets = [cid for cid, kws in KEYWORD_MAP.items()
                   if any(k in text for k in kws)]
        if not targets:
            continue
        out.append({
            "id": f"{df.get('date', 'nodate')}-dailyfold-{i}",
            "date": df.get("date", str(date.today())),
            "headline": note[:120],
            "brief": note,  # dailyFold notes are already distilled by that pipeline
            "sources": [{"label": s.get("source", "daily fold"), "url": s.get("url", "")}],
            "courses": targets,
            "tags": ["daily-fold"],
            "noahPrompt": "",
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--signals-file", default=None)
    ap.add_argument("--from-daily-fold", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    os.makedirs(WORK, exist_ok=True)
    course_index = load_course_index()
    print(f"Course index: {len(course_index)} courses")

    signals = []
    if args.signals_file:
        sf = json.load(open(args.signals_file))
        signals.extend(sf.get("signals", []))
        print(f"Signals file: {len(sf.get('signals', []))} signals")
    if args.from_daily_fold:
        dfs = signals_from_daily_fold()
        signals.extend(dfs)
        print(f"Daily-fold signals: {len(dfs)}")

    if not signals:
        print("No signals to fold. Nothing to do.")
        return 0

    added, skipped, errors = fold_signals(signals, course_index, dry_run=args.dry_run)
    print(f"\nDone: added={added} skipped(dup)={skipped} errors={errors}"
          + (" [DRY RUN]" if args.dry_run else ""))

    # run log
    today = str(date.today())
    log_path = os.path.join(WORK, f"run-{today}.md")
    if not args.dry_run:
        with open(log_path, "a") as f:
            f.write(f"\n## Run {today}\n")
            f.write(f"- signals in: {len(signals)}, added: {added}, skipped: {skipped}, errors: {errors}\n")
            for sig in signals:
                f.write(f"- {sig['id']} -> {', '.join(sig.get('courses', []))}\n")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
