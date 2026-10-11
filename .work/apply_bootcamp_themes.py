#!/usr/bin/env python3
"""Themed-content rollout (2026-10-09): add topicTheme + topic to bootcamp content.json files.

Usage: python3 apply_bootcamp_themes.py
- Backs up each content.json to ~/workspace/apex-audit/.work/bootcamp-json-backups-themes/
- Adds top-level "topicTheme" and "topic" fields via explicit per-bootcamp map
  (keyword fallback only fires for dirs missing from the map; those are logged)
- Validates every file with json.load after editing
"""
import json, os, re, shutil, sys

BOOT_DIR = os.path.expanduser("~/workspace/cert-bootcamps/site/bootcamps")
BACKUP_DIR = os.path.expanduser("~/workspace/apex-audit/.work/bootcamp-json-backups-themes")

# Explicit per-bootcamp map: slug -> (topic, theme)
BOOT_MAP = {
    "acad-career": ("web-dev", "vaporwave"),
    "acad-cloud": ("cloud-devops", "steampunk"),
    "acad-command": ("cybersecurity", "mr-robot"),
    "acad-cyber": ("cybersecurity", "mr-robot"),
    "acad-data": ("data-eng", "oceandeep"),
    "acad-forge": ("programming", "hackers95"),
    "acad-hermetica": ("math", "sacredgeo"),
    "acad-math": ("math", "sacredgeo"),
    "acad-systems": ("linux-systems", "industrial"),
    "acad-theory": ("math", "sacredgeo"),
    "active-directory-defense": ("cybersecurity", "mr-robot"),
    "adaptive-foundations": ("ai-ml", "exmachina"),
    "ai-agent-sec": ("cybersecurity", "mr-robot"),
    "ai-lab": ("ai-ml", "exmachina"),
    "ai-product": ("ai-ml", "exmachina"),
    "alan-turing": ("math", "sacredgeo"),
    "aleks-ops-math": ("math", "sacredgeo"),
    "android-interview": ("programming", "hackers95"),
    "aws-clf": ("cloud-devops", "steampunk"),
    "aws-cloud-practitioner-plus": ("cloud-devops", "steampunk"),
    "aws-data": ("data-eng", "oceandeep"),
    "aws-dop": ("cloud-devops", "steampunk"),
    "aws-ml": ("ai-ml", "exmachina"),
    "aws-saa": ("cloud-devops", "steampunk"),
    "aws-scs": ("cybersecurity", "mr-robot"),
    "aws-soa": ("cloud-devops", "steampunk"),
    "az-104": ("cloud-devops", "steampunk"),
    "az-305": ("cloud-devops", "steampunk"),
    "az-700": ("networking", "tron"),
    "azure-developer": ("ai-ml", "exmachina"),
    "blockchain-dev": ("blockchain", "goldrush"),
    "c-lang": ("programming", "hackers95"),
    "career-launch": ("web-dev", "vaporwave"),
    "cisco-ccna": ("networking", "tron"),
    "cism": ("cybersecurity", "mr-robot"),
    "cissp": ("cybersecurity", "mr-robot"),
    "cka": ("cloud-devops", "steampunk"),
    "ckad": ("cloud-devops", "steampunk"),
    "comptia-a-plus": ("linux-systems", "industrial"),
    "comptia-core": ("linux-systems", "industrial"),
    "comptia-cyber": ("cybersecurity", "mr-robot"),
    "comptia-infra": ("cloud-devops", "steampunk"),
    "comptia-network-plus": ("networking", "tron"),
    "comptia-security-plus": ("cybersecurity", "mr-robot"),
    "cpp": ("programming", "hackers95"),
    "creative-code": ("web-dev", "vaporwave"),
    "cybernetics": ("math", "sacredgeo"),
    "data-analyst": ("data-eng", "oceandeep"),
    "data-analyst-to-ml": ("ai-ml", "exmachina"),
    "data-engineering": ("data-eng", "oceandeep"),
    "data-science-certs": ("ai-ml", "exmachina"),
    "datascience-ml": ("ai-ml", "exmachina"),
    "deep-learning": ("ai-ml", "exmachina"),
    "deep-work": ("math", "sacredgeo"),
    "devops-zero-to-hire": ("cloud-devops", "steampunk"),
    "devsecops-mastery": ("cloud-devops", "steampunk"),
    "docker": ("cloud-devops", "steampunk"),
    "dod-8140": ("cybersecurity", "mr-robot"),
    "dotnet": ("programming", "hackers95"),
    "dp-203": ("data-eng", "oceandeep"),
    "dsa": ("programming", "hackers95"),
    "edward-bernays": ("math", "sacredgeo"),
    "electrician-apprentice": ("linux-systems", "industrial"),
    "embedded-interview": ("linux-systems", "industrial"),
    "enochian-programming": ("math", "sacredgeo"),
    "entrepreneurship": ("web-dev", "vaporwave"),
    "fde-training": ("cybersecurity", "mr-robot"),
    "frontier-path": ("ai-ml", "exmachina"),
    "full-spectrum-dominance": ("cybersecurity", "mr-robot"),
    "fullstack": ("web-dev", "vaporwave"),
    "fullstack-desk": ("web-dev", "vaporwave"),
    "git-devops": ("cloud-devops", "steampunk"),
    "hackers-arise": ("cybersecurity", "mr-robot"),
    "hermetica": ("math", "sacredgeo"),
    "humanmetrics": ("math", "sacredgeo"),
    "iac-terraform-gitops": ("cloud-devops", "steampunk"),
    "ides-tooling": ("programming", "hackers95"),
    "il12-ai-engineering": ("ai-ml", "exmachina"),
    "ios-interview": ("programming", "hackers95"),
    "isc2-cc": ("cybersecurity", "mr-robot"),
    "java": ("programming", "hackers95"),
    "k8s-associate": ("cloud-devops", "steampunk"),
    "k8s-cka-exceed": ("cloud-devops", "steampunk"),
    "kubernetes-sre": ("cloud-devops", "steampunk"),
    "linux-essentials": ("linux-systems", "industrial"),
    "llm-engineering": ("ai-ml", "exmachina"),
    "m365": ("cloud-devops", "steampunk"),
    "m365-endpoint-admin": ("cybersecurity", "mr-robot"),
    "math-tech": ("math", "sacredgeo"),
    "ml-defense": ("cybersecurity", "mr-robot"),
    "mongodb": ("databases", "alexandria"),
    "ms-fundamentals": ("cloud-devops", "steampunk"),
    "neuroai": ("ai-ml", "exmachina"),
    "nice-framework": ("cybersecurity", "mr-robot"),
    "nlp-advanced": ("ai-ml", "exmachina"),
    "nlp-engineering": ("ai-ml", "exmachina"),
    "nsa-codebreaker": ("cybersecurity", "mr-robot"),
    "nvidia-ai": ("ai-ml", "exmachina"),
    "occult-esoteric": ("math", "sacredgeo"),
    "openshift": ("cloud-devops", "steampunk"),
    "oracle-db": ("databases", "alexandria"),
    "oracle-oci": ("cloud-devops", "steampunk"),
    "oracle-sql": ("databases", "alexandria"),
    "pentest": ("cybersecurity", "mr-robot"),
    "philosophy": ("math", "sacredgeo"),
    "platform-engineering": ("cloud-devops", "steampunk"),
    "python": ("programming", "hackers95"),
    "python-systems": ("programming", "hackers95"),
    "python-web": ("web-dev", "vaporwave"),
    "quant-finance-ladder": ("math", "sacredgeo"),
    "quant-finance-math": ("math", "sacredgeo"),
    "quantum": ("ai-ml", "exmachina"),
    "react-frontend": ("web-dev", "vaporwave"),
    "rhce": ("linux-systems", "industrial"),
    "rhcsa": ("linux-systems", "industrial"),
    "roles-library": ("web-dev", "vaporwave"),
    "sc-200": ("cybersecurity", "mr-robot"),
    "sc-300": ("cybersecurity", "mr-robot"),
    "secops-blue-team": ("cybersecurity", "mr-robot"),
    "security-graphs": ("cybersecurity", "mr-robot"),
    "soc-analyst": ("cybersecurity", "mr-robot"),
    "spring": ("programming", "hackers95"),
    "sql": ("databases", "alexandria"),
    "sre-platform": ("cloud-devops", "steampunk"),
    "sre-practices": ("cloud-devops", "steampunk"),
    "study-protocol": ("math", "sacredgeo"),
    "systems-cs": ("linux-systems", "industrial"),
    "terraform": ("cloud-devops", "steampunk"),
    "tl-endpoint-ops": ("cybersecurity", "mr-robot"),
    "tl-interview": ("cybersecurity", "mr-robot"),
    "vault-consul": ("cloud-devops", "steampunk"),
    "vendor-map": ("web-dev", "vaporwave"),
    "windows-admin": ("linux-systems", "industrial"),
    "zero-trust": ("cybersecurity", "mr-robot"),
    "zerotrust": ("cybersecurity", "mr-robot"),
}

# Keyword fallback (ordered): regex -> (topic, theme). Only for dirs missing from BOOT_MAP.
FALLBACK = [
    (r"blockchain|web3", ("blockchain", "goldrush")),
    (r"threatlocker|\btl-|pentest|hackers-arise|secops|blue-team|\bsoc\b|siem|sentinel|zero.?trust|dod-8140|nice-framework|fde|active.?directory|ml-defense|ai-agent-sec|security-graphs|nsa-codebreaker|cissp|cism|isc2|comptia-cyber|comptia-security", ("cybersecurity", "mr-robot")),
    (r"\bllm\b|nlp|deep.?learning|neuroai|nvidia-ai|aws-ml|datascience-ml|analyst-to-ml|ai-lab|ai-product|quantum", ("ai-ml", "exmachina")),
    (r"mongodb|\bsql\b|oracle-db|oracle-sql", ("databases", "alexandria")),
    (r"ccna|network-plus|az-700|\bnetwork", ("networking", "tron")),
    (r"aws-|azure|az-|docker|kubernetes|k8s|\bcka\b|ckad|terraform|gitops|devops|\bsre\b|platform-engineering|openshift|vault|consul|oracle-oci|m365|ms-fundamentals|comptia-infra", ("cloud-devops", "steampunk")),
    (r"linux|rhcsa|rhce|windows-admin|systems|electrician|embedded|comptia-a|comptia-core", ("linux-systems", "industrial")),
    (r"python|c-lang|\bcpp\b|java|dotnet|spring|\bdsa\b|ides|android|ios-interview", ("programming", "hackers95")),
    (r"react|fullstack|frontend|web|creative-code", ("web-dev", "vaporwave")),
    (r"math|aleks|quant|turing|cybernetics|philosoph|esoteric|hermetica|enochian|deep-work|study-protocol|humanmetrics|bernays", ("math", "sacredgeo")),
    (r"career|roles-library|vendor-map|entrepreneurship", ("web-dev", "vaporwave")),
]

def fallback_theme(slug):
    for pat, pair in FALLBACK:
        if re.search(pat, slug):
            return pair
    return None

def main():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    dirs = sorted(d for d in os.listdir(BOOT_DIR)
                  if os.path.isdir(os.path.join(BOOT_DIR, d))
                  and os.path.isfile(os.path.join(BOOT_DIR, d, "content.json")))
    counts, done, fallback_used = {}, 0, []
    unmapped = []
    for slug in dirs:
        pair = BOOT_MAP.get(slug)
        if pair is None:
            pair = fallback_theme(slug)
            if pair is None:
                unmapped.append(slug)
                continue
            fallback_used.append((slug, pair))
        topic, theme = pair
        path = os.path.join(BOOT_DIR, slug, "content.json")
        bak = os.path.join(BACKUP_DIR, slug + ".content.json")
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
        with open(path, encoding="utf-8") as f:
            check = json.load(f)
        assert check["topicTheme"] == theme and check["topic"] == topic, slug
        counts[theme] = counts.get(theme, 0) + 1
        done += 1
    print("%d bootcamps updated." % done)
    print("Theme counts:", json.dumps(counts, indent=2, sort_keys=True))
    if fallback_used:
        print("FALLBACK USED for:")
        for s, p in fallback_used:
            print("  ", s, "->", p)
    if unmapped:
        print("UNMAPPED (skipped):", unmapped)
    print("Backups in:", BACKUP_DIR)

if __name__ == "__main__":
    main()
