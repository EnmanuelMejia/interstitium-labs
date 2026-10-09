#!/usr/bin/env python3
"""Themed-content rollout (2026-10-09): add topicTheme + topic to course JSONs.

Usage: python3 apply_course_themes.py
- Backs up each JSON to ~/workspace/apex-audit/.work/course-json-backups-themes/
- Adds top-level "topicTheme" and "topic" fields via explicit per-course map
- Validates every file with json.load after editing
"""
import json, os, shutil, sys

COURSE_DIR = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses")
BACKUP_DIR = os.path.expanduser("~/workspace/apex-audit/.work/course-json-backups-themes")

# slug -> (topic, theme)
COURSE_MAP = {
    "il-01-esoteric-foundations": ("math", "sacredgeo"),
    "il-02-mathematical-maturity-engine": ("math", "sacredgeo"),
    "il-03-programming-language-forge": ("programming", "hackers95"),
    "il-04-systems-linux-windows-networks": ("linux-systems", "industrial"),
    "il-05-cloud-devsecops-platform-sre": ("cloud-devops", "steampunk"),
    "il-06-cybersecurity-secure-engineering": ("cybersecurity", "mr-robot"),
    "il-07-data-engineering-analytics-ai": ("data-eng", "oceandeep"),
    "il-08-algorithms-compilers-distributed-formal": ("programming", "hackers95"),
    "il-09-adaptive-certification-command": ("cybersecurity", "mr-robot"),
    "il-10-portfolio-career-professional-practice": ("web-dev", "vaporwave"),
    "il-11-zero-trust-endpoint-defense": ("cybersecurity", "mr-robot"),
    "il-12-ai-engineering": ("ai-ml", "exmachina"),
    "il-13-software-engineering-interview-prep": ("programming", "hackers95"),
    "il-14-sre-devops-cloud-security-interview-prep": ("cloud-devops", "steampunk"),
    "il-15-data-engineering-analytics-interview-prep": ("data-eng", "oceandeep"),
    "il-16-machine-learning-ai-engineering": ("ai-ml", "exmachina"),
    "il-17-agentic-ai-engineering": ("ai-ml", "exmachina"),
    "il-18-technical-leadership-interview-prep": ("system-design", "cyberpunk"),
    "il-19-multicloud-devops-ai-bootcamp": ("cloud-devops", "steampunk"),
    "il-20-mathematics": ("math", "sacredgeo"),
    "il-21-humanities": ("math", "sacredgeo"),
    "il-22-esoteric-secret-knowledge": ("math", "sacredgeo"),
    "il-23-frontier-knowledge": ("ai-ml", "exmachina"),
    "il-24-threatlocker-assessment-prep-cbt": ("cybersecurity", "mr-robot"),
    "il-25-cybersecurity-professional-certificate": ("cybersecurity", "mr-robot"),
    "il-26-data-analyst-certification-senior-mastery": ("data-eng", "oceandeep"),
    "il-27-it-infrastructure-specialist-threatlocker-mastery": ("cybersecurity", "mr-robot"),
    "il-28-devsecops-cloud-infrastructure-mastery": ("cloud-devops", "steampunk"),
    "il-29-threatlocker-ai-cybersecurity-mastery": ("cybersecurity", "mr-robot"),
}

def main():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    counts = {}
    done = 0
    for slug, (topic, theme) in sorted(COURSE_MAP.items()):
        path = os.path.join(COURSE_DIR, slug + ".json")
        if not os.path.isfile(path):
            print("MISSING:", path, file=sys.stderr)
            continue
        # backup (only if not already backed up this run)
        bak = os.path.join(BACKUP_DIR, slug + ".json")
        if not os.path.isfile(bak):
            shutil.copy2(path, bak)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        data["topicTheme"] = theme
        data["topic"] = topic
        tmp = path + ".tmp-theme"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, path)
        # validate
        with open(path, encoding="utf-8") as f:
            check = json.load(f)
        assert check["topicTheme"] == theme and check["topic"] == topic, slug
        counts[theme] = counts.get(theme, 0) + 1
        done += 1
        print("OK", slug, "->", topic, "/", theme)
    print("\n%d courses updated." % done)
    print("Theme counts:", json.dumps(counts, indent=2, sort_keys=True))
    print("Backups in:", BACKUP_DIR)

if __name__ == "__main__":
    main()
