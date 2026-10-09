#!/usr/bin/env python3
"""Batch 7 merge: validate + append simulations/consoleSims/terminalMissions to 12 bootcamps."""
import importlib.util
import json
import os
import re
import sys

WORK = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.expanduser("~/workspace/cert-bootcamps/site/bootcamps")

MODULES = {
    "deep-work": "deep_work",
    "edward-bernays": "edward_bernays",
    "entrepreneurship": "entrepreneurship",
    "frontier-path": "frontier_path",
    "occult-esoteric": "occult_esoteric",
    "philosophy": "philosophy",
    "quant-finance-ladder": "quant_finance_ladder",
    "quant-finance-math": "quant_finance_math",
    "roles-library": "roles_library",
    "study-protocol": "study_protocol",
    "vendor-map": "vendor_map",
    "windows-admin": "windows_admin",
}

KINDS = {"troubleshoot", "branching", "ordering", "config-check"}
CONSOLE_ACTIONS = {
    "aws-vpc": {"create-vpc", "create-subnet", "create-igw", "attach-igw", "create-route-table",
                "add-route", "associate-route-table", "create-sg", "add-sg-rule", "launch-instance"},
    "aws-iam": {"create-user", "create-group", "add-user-to-group", "create-role",
                "create-policy", "attach-policy", "enable-mfa"},
    "azure-portal": {"create-rg", "create-vnet", "create-vm", "create-nsg", "add-nsg-rule", "assign-rbac"},
    "k8s-dashboard": {"create-namespace", "deploy", "expose-service", "scale", "create-configmap"},
    "firewall": {"add-rule", "delete-rule", "set-default-policy"},
    "switch-cli": {"create-vlan", "assign-port", "set-trunk", "save-config", "show-vlan"},
    "linux-desktop": {"select", "chmod", "chown", "create-file", "create-dir", "delete"},
    "sql-studio": {"create-table", "create-index", "run-query"},
    "git-host": {"create-branch", "open-pr", "approve-pr", "request-changes", "add-comment", "merge-pr"},
    "cicd-pipeline": {"trigger-build", "retry-stage", "approve-stage", "set-variable"},
    "siem-dashboard": {"acknowledge-alert", "assign-alert", "escalate", "isolate-host", "create-rule"},
    "ticketing": {"create-ticket", "assign-ticket", "update-status", "add-note", "resolve-ticket"},
    "code-editor": {"open-file", "toggle-breakpoint", "step-over", "run-to-breakpoint",
                    "fix-line", "inspect-variable"},
    "db-admin": {"create-database", "create-user", "grant-priv", "backup", "set-parameter"},
    "generic-web": {"set-field", "submit-form"},
}
ALLOWED_CMDS = {"sha256sum", "cat", "ls", "echo", "grep", "head", "tail", "sort",
                "find", "ps", "wc", "dig", "ping", "diff"}

errors = []


def err(msg):
    errors.append(msg)


def req(obj, fields, where):
    for f in fields:
        if f not in obj:
            err("%s: missing field %r" % (where, f))


def validate_sim(s, slug, domain_ids):
    w = "sim %s" % s.get("id")
    req(s, ["id", "title", "kind", "domain_id", "difficulty", "brief", "steps", "debrief", "points"], w)
    if not str(s.get("id", "")).startswith(slug + "-"):
        err("%s: id not slug-prefixed" % w)
    if s.get("kind") not in KINDS:
        err("%s: bad kind %r" % (w, s.get("kind")))
        return
    if s.get("domain_id") not in domain_ids:
        err("%s: domain_id %r not in %s" % (w, s.get("domain_id"), domain_ids))
    if s.get("difficulty") not in (1, 2, 3):
        err("%s: difficulty %r" % (w, s.get("difficulty")))
    k = s["kind"]
    steps = s.get("steps")
    if k == "troubleshoot":
        if not isinstance(steps, list) or not steps:
            err("%s: steps must be non-empty list" % w)
        for i, st in enumerate(steps):
            req(st, ["symptom", "evidence", "options", "correct", "explain"], "%s step %d" % (w, i))
            if not (0 <= st.get("correct", -1) < len(st.get("options", []))):
                err("%s step %d: correct index out of range" % (w, i))
    elif k == "branching":
        if not isinstance(steps, list) or not steps:
            err("%s: steps must be non-empty list" % w)
        ids = {n.get("id") for n in steps}
        for i, n in enumerate(steps):
            req(n, ["id", "text", "choices"], "%s node %d" % (w, i))
            for j, ch in enumerate(n.get("choices", [])):
                req(ch, ["label", "feedback", "points", "next"], "%s node %s choice %d" % (w, n.get("id"), j))
                if ch.get("next") not in ids and ch.get("next") != "END":
                    err("%s node %s choice %d: next %r unknown" % (w, n.get("id"), j, ch.get("next")))
    elif k == "ordering":
        req(steps, ["context", "items", "correct_order"], "%s steps" % w)
        n = len(steps.get("items", []))
        if sorted(steps.get("correct_order", [])) != list(range(n)):
            err("%s: correct_order is not a permutation of 0..%d" % (w, n - 1))
    elif k == "config-check":
        req(steps, ["config", "find", "issues"], "%s steps" % w)
        lines = str(steps.get("config", "")).split("\n")
        if steps.get("find") != len(steps.get("issues", [])):
            err("%s: find=%r but %d issues" % (w, steps.get("find"), len(steps.get("issues", []))))
        for j, iss in enumerate(steps.get("issues", [])):
            req(iss, ["line", "description", "fix"], "%s issue %d" % (w, j))
            ln = iss.get("line")
            if not (1 <= ln <= len(lines)):
                err("%s issue %d: line %r out of range (1..%d)" % (w, j, ln, len(lines)))


def validate_console(c, slug, domain_ids):
    w = "console %s" % c.get("id")
    req(c, ["id", "title", "console", "domain_id", "difficulty", "brief", "tasks", "debrief"], w)
    if not str(c.get("id", "")).startswith(slug + "-"):
        err("%s: id not slug-prefixed" % w)
    con = c.get("console")
    if con not in CONSOLE_ACTIONS:
        err("%s: unknown console %r" % (w, con))
        return
    if c.get("domain_id") not in domain_ids:
        err("%s: domain_id %r" % (w, c.get("domain_id")))
    if c.get("difficulty") not in (1, 2, 3):
        err("%s: difficulty %r" % (w, c.get("difficulty")))
    tasks = c.get("tasks", [])
    if not tasks:
        err("%s: no tasks" % w)
    for t in tasks:
        tw = "%s task %s" % (w, t.get("id"))
        req(t, ["id", "instruction", "validate", "hint"], tw)
        if not t.get("hint"):
            err("%s: empty hint" % tw)
        v = t.get("validate", {})
        req(v, ["action", "params"], tw + " validate")
        if v.get("action") not in CONSOLE_ACTIONS[con]:
            err("%s: action %r not in %s vocab" % (tw, v.get("action"), con))
        if not isinstance(v.get("params"), dict):
            err("%s: params not a dict" % tw)
        if con == "sql-studio" and v.get("action") == "run-query" and "match" not in v.get("params", {}):
            err("%s: run-query without match param" % tw)


def validate_mission(m, slug, domain_ids):
    w = "mission %s" % m.get("id")
    req(m, ["id", "title", "domain_id", "difficulty", "brief", "objectives", "checks",
            "success_message"], w)
    if not str(m.get("id", "")).startswith(slug + "-"):
        err("%s: id not slug-prefixed" % w)
    if m.get("domain_id") not in domain_ids:
        err("%s: domain_id %r" % (w, m.get("domain_id")))
    if m.get("difficulty") not in (1, 2, 3):
        err("%s: difficulty %r" % (w, m.get("difficulty")))
    if not m.get("objectives"):
        err("%s: no objectives" % w)
    checks = m.get("checks", [])
    if not checks:
        err("%s: no checks" % w)
    for i, ch in enumerate(checks):
        cw = "%s check %d" % (w, i)
        req(ch, ["command_pattern", "expect_contains", "hint"], cw)
        if not ch.get("hint"):
            err("%s: empty hint" % cw)
        try:
            rx = re.compile(ch["command_pattern"])
        except re.error as e:
            err("%s: bad regex: %s" % (cw, e))
            continue
        # allowed-command sanity: pattern must name one of the allowed commands
        pat = ch["command_pattern"]
        if not any(cmd in pat for cmd in ALLOWED_CMDS):
            err("%s: pattern names no allowed command" % cw)
        if "grep -c" in pat or "grep  -c" in pat:
            err("%s: grep -c forbidden" % cw)


def main():
    only = sys.argv[1:]
    for slug, modname in MODULES.items():
        if only and slug not in only:
            continue
        path = os.path.join(SITE, slug, "content.json")
        doc = json.load(open(path))
        domain_ids = [d["id"] for d in doc.get("domains", [])]
        spec = importlib.util.spec_from_file_location(modname, os.path.join(WORK, modname + ".py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        sims, consoles, missions = mod.SIMS, mod.CONSOLES, mod.MISSIONS

        # JSON-serializable
        try:
            json.dumps(sims)
            json.dumps(consoles)
            json.dumps(missions)
        except TypeError as e:
            err("%s: not JSON-serializable: %s" % (slug, e))

        # counts
        if len(sims) != 5:
            err("%s: %d sims (want 5)" % (slug, len(sims)))
        if len(consoles) != 4:
            err("%s: %d consoles (want 4)" % (slug, len(consoles)))
        if len(missions) != 7:
            err("%s: %d missions (want 7)" % (slug, len(missions)))

        # unique ids
        ids = [s["id"] for s in sims] + [c["id"] for c in consoles] + [m["id"] for m in missions]
        if len(ids) != len(set(ids)):
            err("%s: duplicate ids" % slug)
        tids = [t["id"] for c in consoles for t in c.get("tasks", [])]
        if len(tids) != len(set(tids)):
            err("%s: duplicate task ids" % slug)

        for s in sims:
            validate_sim(s, slug, domain_ids)
        for c in consoles:
            validate_console(c, slug, domain_ids)
        for m in missions:
            validate_mission(m, slug, domain_ids)

        if errors:
            continue

        # merge: only fill empty/missing arrays
        for key, val in (("simulations", sims), ("consoleSims", consoles),
                         ("terminalMissions", missions)):
            cur = doc.get(key)
            if cur is None:
                doc[key] = []
                cur = doc[key]
            if not isinstance(cur, list):
                err("%s: existing %s is not a list" % (slug, key))
                continue
            if len(cur) != 0:
                err("%s: existing %s non-empty (%d) — refusing to overwrite" % (slug, key, len(cur)))
                continue
            doc[key] = val

        if errors:
            continue

        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
            f.write("\n")
        # re-validate from disk
        doc2 = json.load(open(tmp))
        assert len(doc2["simulations"]) == 5 and len(doc2["consoleSims"]) == 4 \
            and len(doc2["terminalMissions"]) == 7, slug
        os.replace(tmp, path)
        print("OK %s: +5 sims, +4 consoles, +7 missions" % slug)

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("\nAll merges validated and written.")


if __name__ == "__main__":
    main()
