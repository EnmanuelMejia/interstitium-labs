import json, sys

P = "/home/hatch/workspace/apex-audit/docs/university/data/courses/_il28-build/batch-A.json"
raw = open(P).read()
# repair: stray ']' closed the array early at the M6/M7 boundary
bad = '"weight": 1}],\n{"cards":[{"back":"/etc"'
good = '"weight": 1},\n{"cards":[{"back":"/etc"'
assert raw.count(bad) == 1, raw.count(bad)
raw = raw.replace(bad, good, 1)
raw = raw.rstrip()
assert raw.endswith('}]]'), repr(raw[-10:])
raw = raw[:-1]  # drop the leftover duplicate array close
mods = json.loads(raw)
by_id = {m["id"]: m for m in mods}

def rep(container, idx, field, old, new):
    cur = container[idx][field]
    assert old in cur, f"NOT FOUND in {container} [{idx}].{field}: {old[:60]!r}"
    container[idx][field] = cur.replace(old, new, 1)

# --- M5 quiz fixes: broken 5-option Q and meta self-check Q ---
m5 = by_id["IL28-M05"]
q = m5["quiz"]
q[4] = {"q": "In the worked DH example, what is the shared secret both sides compute?",
        "choices": ["8", "19", "2", "6"], "answer": 2,
        "explain": "Alice computed 19^6 mod 23 = 2 and Bob computed 8^15 mod 23 = 2."}
q[5] = {"q": "An attacker records A=8 and B=19 from the worked exchange. Why is a real-world exchange still secure?",
        "choices": ["The public values are encrypted on the wire",
                    "Toy sizes are brute-forceable; real security needs a large prime making the discrete log infeasible",
                    "The secret is transmitted before the attacker starts listening",
                    "TLS prevents anyone recording the values"],
        "answer": 1,
        "explain": "With p=23 an attacker could brute-force a; security comes from the discrete logarithm being infeasible at real prime sizes."}

# --- M3 drill: 5th /23 answer ---
m3 = by_id["IL28-M03"]
d = m3["drills"][0]["items"]
assert d[3]["answer"] == "10.1.0.0/23", d[3]["answer"]
d[3]["answer"] = "10.1.8.0/23"

# --- M7 notes: redirection ordering sentence ---
m7 = by_id["IL28-M07"]
rep(m7["notes"], 4, "body",
    "A classic bug is cmd > file 2>&1 vs cmd 2>&1 > file: only the first form sends stderr to the file in most shells... actually both redirect stderr to where stdout currently points; the safe idiom is > file 2>&1.",
    "A classic ordering gotcha: in > file 2>&1, stderr is duplicated to stdout's current target (the file), so both streams land in the file; in 2>&1 > file, stderr goes to the terminal instead, because stdout still pointed there when 2>&1 was processed. The safe idiom is > file 2>&1.")

# --- M1 lab step 8 cleanup ---
m1 = by_id["IL28-M01"]
steps = m1["handsOnLab"]["steps"]
old8 = [s for s in steps if "wait, predict first" in s]
assert len(old8) == 1, old8
steps[steps.index(old8[0])] = ("Set bit 3 and clear bit 2 of 0b00001111 in one Python line: run "
    "python3 -c \"print(bin((0b00001111 | (1<<3)) & ~(1<<2)))\" and verify you get 0b1011.")

# --- M4 drill: rambling explain ---
m4 = by_id["IL28-M04"]
it = m4["drills"][1]["items"][2]
assert it["answer"] == "{22}"
it["explain"] = "Union of allows is {443, 22}; minus denies {443} leaves {22}."

# --- M2 De Morgan framing fixes (note, drill, card) ---
m2 = by_id["IL28-M02"]
rep(m2["notes"], 2, "body",
    "simplify the policy 'deny unless (is_admin AND on_vpn)'. The allow condition is NOT (is_admin AND on_vpn). Apply the first law: NOT is_admin OR NOT on_vpn, i.e. allow when the user is not an admin or not on the VPN. Verify with a truth table: is_admin=true, on_vpn=true gives NOT(true)=false OR NOT(true)=false = false, so deny, correct since the original required both. is_admin=true, on_vpn=false gives false OR true = true, allow, correct.",
    "simplify the deny condition of the policy 'allow only if (is_admin AND on_vpn)'. The deny condition is NOT (is_admin AND on_vpn). Apply the first law: NOT is_admin OR NOT on_vpn, i.e. deny when the user is not an admin or not on the VPN. Verify with a truth table: is_admin=true, on_vpn=true gives NOT(true)=false OR NOT(true)=false = false, so no deny (allow), correct since both hold. is_admin=true, on_vpn=false gives false OR true = true, deny, correct.")
rep(m2["drills"][0]["items"], 2, "prompt",
    "Rewrite the allow condition for 'deny unless (is_admin AND on_vpn)'.",
    "Write the deny condition for 'allow only if (is_admin AND on_vpn)'.")
rep(m2["drills"][0]["items"], 2, "explain",
    "Deny unless both means allow = NOT(is_admin AND on_vpn) = NOT is_admin OR NOT on_vpn.",
    "Deny = NOT(is_admin AND on_vpn) = NOT is_admin OR NOT on_vpn.")
rep(m2["cards"], 8, "front",
    "A firewall rule says 'deny unless (admin AND on_vpn)'. Write the allow condition using De Morgan.",
    "A policy allows access only if (admin AND on_vpn). Write the deny condition using De Morgan.")
rep(m2["cards"], 8, "back",
    "NOT (A AND B) = NOT A OR NOT B",
    "NOT admin OR NOT on_vpn.")

# --- M3 note word-count pad (118 -> 135) ---
rep(by_id["IL28-M03"]["notes"], 2, "body",
    "and /32 (1 host).",
    "and /32 (1 host). Memorize the powers of two from 2^1 through 2^16; every subnet question is answered by them.")
rep(by_id["IL28-M03"]["notes"], 3, "body",
    "one large CIDR per environment, carved into tier subnets.",
    "one large CIDR per environment, carved into tier subnets. When carving, always verify the first and last subnet addresses with a tool; off-by-one errors in the borrowed bits are the most common subnetting mistake.")
rep(by_id["IL28-M03"]["notes"], 5, "body",
    "ISPs and cloud route tables aggregate aggressively.",
    "ISPs and cloud route tables aggregate aggressively. Practice both directions until they are mechanical: given requirements, allocate with VLSM; given a set of routes, find the tightest summary.")

# --- validation ---
req = ["id","code","title","summary","objectives","notes","cards","quiz","weight",
       "prerequisiteFor","drills","handsOnLab","mockTask","crossLinks","videos","estimatedMinutes"]
for m in mods:
    for f in req:
        assert f in m, f"{m['id']} missing {f}"
    assert 4 <= len(m["objectives"]) <= 5, m["id"]
    assert 5 <= len(m["notes"]) <= 8, m["id"]
    for n in m["notes"]:
        wc = len(n["body"].split())
        assert 120 <= wc <= 300, f"{m['id']} note '{n['title']}' wc={wc}"
        assert set(n) == {"title","body"}, n
    assert 10 <= len(m["cards"]) <= 14, m["id"]
    for c in m["cards"]: assert set(c) == {"front","back"}, c
    assert 8 <= len(m["quiz"]) <= 10, m["id"]
    for x in m["quiz"]:
        assert set(x) == {"q","choices","answer","explain"}, x
        assert len(x["choices"]) == 4, f"{m['id']} quiz choices != 4: {x['q'][:40]}"
        assert 0 <= x["answer"] <= 3
    assert 1 <= len(m["drills"]) <= 2, m["id"]
    di = 0
    for dr in m["drills"]:
        assert set(dr) == {"id","title","items"}, dr
        assert 6 <= len(dr["items"]) <= 8, dr["id"]
        for it2 in dr["items"]:
            assert set(it2) == {"prompt","answer","explain"}, it2
        di += len(dr["items"])
    lab = m["handsOnLab"]
    assert set(lab) == {"id","title","brief","steps","deliverable","checkpoint"}, m["id"]
    assert 8 <= len(lab["steps"]) <= 14, m["id"]
    mk = m["mockTask"]
    assert set(mk) == {"id","type","q","choices","answer","explain"}, m["id"]
    assert len(mk["choices"]) == 4 and 0 <= mk["answer"] <= 3
    assert 1 <= len(m["videos"]) <= 2, m["id"]
    for v in m["videos"]:
        assert set(v) == {"title","url","source","durationMin","order","watchBefore","blurb"}, v
        assert v["url"].startswith("https://"), v["url"]
    # formula check
    vm = sum(v["durationMin"] for v in m["videos"])
    exp = m["weight"]*120 + len(m["notes"])*12 + len(m["cards"])*4 + len(m["quiz"])*8 + di*4 + 90 + min(180, vm/2)
    exp = round(exp/30)*30
    assert m["estimatedMinutes"] == exp, f"{m['id']}: {m['estimatedMinutes']} != {exp}"

with open(P, "w") as f:
    json.dump(mods, f, indent=1, ensure_ascii=False)
    f.write("\n")

total = sum(m["estimatedMinutes"] for m in mods)
print(f"OK: {len(mods)} modules, total estimated minutes = {total}")
for m in mods:
    print(f"  {m['id']}: notes={len(m['notes'])} cards={len(m['cards'])} quiz={len(m['quiz'])} "
          f"drillItems={sum(len(d['items']) for d in m['drills'])} steps={len(m['handsOnLab']['steps'])} "
          f"videos={len(m['videos'])} min={m['estimatedMinutes']}")
