#!/usr/bin/env python3
"""Fill il-27: expand 6 thin FT drills (2 -> 5 items) and add 9 writing-style mockTasks."""
import json, os

P = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses/il-27-it-infrastructure-specialist-threatlocker-mastery.json')
d = json.load(open(P))

DRILL_NEW = {
 "IL27-FT04": {0: [
    {"prompt": "Run a second 8-question set with the same rules \u2014 this time every answer must lead with the verdict in the first 10 seconds.",
     "answer": "Verdict-first inside 10s on all 8; score 0\u20133 each, pass \u226517/24.",
     "explain": "The verdict-first habit is the difference between a 2 and a 3."},
    {"prompt": "For every answer that scored 0\u20131, rewrite it as verdict \u2192 method \u2192 evidence \u2192 close and deliver it again.",
     "answer": "All re-answers at 2+. Record the before/after.",
     "explain": "Rewrites lock in the structure under zero pressure so it survives pressure."},
    {"prompt": "Close with the 3 questions you dread most, answered cold, back-to-back.",
     "answer": "No warm-up, no notes; dread questions at 2+.",
     "explain": "The panel will find your weak spots \u2014 find them first."},
   ],
   2: [
    {"prompt": "Deliver the trade-offs section of the hardening talk alone \u2014 3 minutes, timed.",
     "answer": "3:00 \u00b1 15s; every trade-off names a real cost.",
     "explain": "Trade-offs are where seniors are separated from juniors."},
    {"prompt": "Deliver 'greatest weakness' in 60 seconds with dated evidence of improvement.",
     "answer": "Real weakness + dated evidence + current practice. \u226460s.",
     "explain": "Dated evidence turns a weakness answer into a growth story."},
    {"prompt": "Practice your closer: one sharp question for the panel about their endpoint pain.",
     "answer": "One question that shows you listened and opens a real conversation.",
     "explain": "End as a colleague, not an applicant."},
   ]},
 "IL27-FT05": {0: [
    {"prompt": "State what you will wear and the grooming check \u2014 decided tonight, not tomorrow.",
     "answer": "Outfit decided and laid out tonight; zero morning decisions.",
     "explain": "Decision fatigue is real \u2014 spend none of it on clothes."},
    {"prompt": "Name three things you will NOT bring, and why.",
     "answer": "No laptop (distraction), no strong scent, nothing uncharged.",
     "explain": "Knowing what to leave out is preparation too."},
    {"prompt": "Lay the bag out physically tonight and photograph it.",
     "answer": "Photo taken; bag packed by the door.",
     "explain": "The photo is your morning checklist."},
   ],
   2: [
    {"prompt": "Time the drive at the same time of day as the interview.",
     "answer": "Dry run done; arrival buffer known.",
     "explain": "Traffic at 8 AM is not traffic at 2 PM \u2014 measure the real one."},
    {"prompt": "Identify parking, the building entrance, and the check-in desk.",
     "answer": "All three confirmed; no wandering on the day.",
     "explain": "Wandering burns the calm you built."},
    {"prompt": "Save an offline map and screenshot the route.",
     "answer": "Offline copy saved; the phone cannot betray you.",
     "explain": "Dead zones and dead batteries are both real."},
   ]},
 "IL27-FT06": {0: [
    {"prompt": "Rank the 8 worksheet lines by what you would trade first in negotiation.",
     "answer": "Ranked list written; top-3 non-negotiables starred.",
     "explain": "You cannot negotiate what you have not prioritized."},
    {"prompt": "Write your walk-away number and your yes-on-the-spot number.",
     "answer": "Both numbers written before any call happens.",
     "explain": "Numbers decided calm beat numbers decided excited."},
    {"prompt": "Draft the 5 benefits questions you will email HR before signing.",
     "answer": "Questions drafted; send within 24h of the offer.",
     "explain": "Benefits are compensation \u2014 price them."},
   ],
   1: [
    {"prompt": "Recite days 1\u201330 with one concrete artifact.",
     "answer": "30: shadow + document; artifact: one improved runbook page.",
     "explain": "Artifacts, not adjectives."},
    {"prompt": "Recite days 61\u201390 with one concrete artifact.",
     "answer": "90: own a small system; artifact: a lunch-and-learn delivered.",
     "explain": "Teaching back proves mastery."},
    {"prompt": "Deliver the whole 30/60/90 page in 90 seconds flat, timed.",
     "answer": "\u226490s, all three phases, no filler.",
     "explain": "Brevity signals command."},
   ]},
}

for m in d['modules']:
    if m['id'] in DRILL_NEW:
        for di, items in DRILL_NEW[m['id']].items():
            before = len(m['drills'][di]['items'])
            m['drills'][di]['items'].extend(items)
            print(f"{m['id']} drill {di}: {before} -> {len(m['drills'][di]['items'])}")

NEW_MOCKS = [
 {"id": "IL27-MOCK-04", "moduleId": "IL27-M10", "title": "Write a network outage postmortem", "kind": "writing",
  "brief": "The branch office lost connectivity for 47 minutes yesterday. Write the postmortem the way a senior would: blameless, timestamped, and ending in action items with owners.",
  "scenario": "At 9:02 AM the branch office reported total network loss. You confirmed the WAN link was up, found the core switch unresponsive (failed PSU), failed over to the spare, and restored service at 9:49 AM. No spare PSU was on site.",
  "deliverable": "A one-page postmortem with: summary (3 lines), timeline table (time/action/actor), root cause (hardware, not 'the network'), impact (users, duration, business effect), and 3 action items with owners and dates \u2014 including a spare-PSU procurement.",
  "rubric": ["Timeline is complete and blameless", "Root cause names the failed PSU, not 'connectivity issues'", "Impact quantifies users and minutes", "Action items have owners and dates", "Spare-parts gap is addressed, not just noted"]},
 {"id": "IL27-MOCK-05", "moduleId": "IL27-M13", "title": "Document a GPO change", "kind": "writing",
  "brief": "Write the change record for a new GPO enforcing 15-minute screen lock with password on resume \u2014 the record another admin could use to replicate or roll back your work.",
  "scenario": "Security requested workstation screen lock enforcement. You created the GPO, linked it at the domain level with security filtering to a pilot OU first, verified with gpresult on 5 pilot machines, then rolled it out org-wide after 48 clean hours.",
  "deliverable": "A change record with: GPO name and GUID, link location and order, security filtering, WMI filters (if any), settings configured, pilot results, rollout plan, and a rollback procedure (unlink + gpupdate) with an estimated revert time.",
  "rubric": ["GPO name, link location, and order are stated", "Pilot-then-rollout sequence is documented", "Verification method (gpresult) is named", "Rollback procedure is concrete with a time estimate", "Filtering/scope is explicit \u2014 no 'applied to everyone' vagueness"]},
 {"id": "IL27-MOCK-06", "moduleId": "IL27-M04", "title": "Write a user-facing outage notice", "kind": "writing",
  "brief": "The file server goes down for maintenance Saturday 6\u201310 AM. Write the notice users actually read: short, plain language, and honest about what breaks.",
  "scenario": "Planned storage migration on FILE-01. During the window, mapped drives (S:, P:) will be unavailable. Email keeps working. The help desk number is staffed from 6 AM.",
  "deliverable": "A notice under 120 words with: what is happening, the exact window with timezone, what stops working (drive letters, not server names), what keeps working, and where to get help \u2014 sent 48 hours ahead and again 2 hours ahead.",
  "rubric": ["Under 120 words", "Drive letters named, not server hostnames", "Exact window with timezone", "Help contact is present", "Two-send timing is stated"]},
 {"id": "IL27-MOCK-07", "moduleId": "IL27-M31", "title": "Write a backup restore runbook", "kind": "writing",
  "brief": "Write the runbook a junior follows at 3 AM to restore the shared drive from last night's backup \u2014 every step verifiable, no tribal knowledge.",
  "scenario": "The finance share was encrypted by a macro at 4 PM; the 2 AM backup is clean. RTO is 4 hours, RPO is 24 hours. The backup software is already installed on the restore target.",
  "deliverable": "A numbered runbook with: pre-checks (verify backup integrity first), restore steps with exact console paths or commands, verification steps (spot-check 5 files, confirm share permissions), a rollback note, and the RTO/RPO statement up top.",
  "rubric": ["RTO/RPO stated at the top", "Integrity check comes before the restore", "Steps are numbered and verifiable", "Verification step names a concrete check", "No step assumes unstated knowledge"]},
 {"id": "IL27-MOCK-08", "moduleId": "IL27-M30", "title": "Write a phishing triage note", "kind": "writing",
  "brief": "A user clicked a credential-harvesting link 20 minutes ago. Write the triage note: what you did, in what order, and what is still open.",
  "scenario": "User reported the click themselves. You confirmed the URL was malicious via the email gateway logs, forced a password reset, revoked active sessions, checked mailbox rules for forwarding, and found none. The user's machine is being reimaged as a precaution.",
  "deliverable": "A triage note with: timeline, containment actions in order (account first, then mailbox, then endpoint), what was ruled out (no forwarding rules, no lateral mail), and open items with owners \u2014 plus one preventive control to propose.",
  "rubric": ["Account containment precedes endpoint work", "Mailbox-rule check is present (persistence vector)", "Ruled-out items are stated, not omitted", "Open items have owners", "Preventive control is specific"]},
 {"id": "IL27-MOCK-09", "moduleId": "IL27-M12", "title": "Write an AD OU design proposal", "kind": "writing",
  "brief": "The company is opening a 40-person branch office. Propose the OU structure and justify it in half a page a non-AD-expert manager can follow.",
  "scenario": "New site 'Orlando-Branch' with 40 users, 45 workstations, 2 servers, its own file/print needs, and a local IT contact (not an admin). GPOs must differ from HQ on power settings and mapped drives; security baselines stay identical.",
  "deliverable": "A proposal with: an OU tree diagram (text is fine), where each GPO links and why, which settings are enforced vs. blocked inheritance, delegation for the local contact (least privilege), and a naming convention note.",
  "rubric": ["OU tree is explicit and justified", "GPO link placement matches the stated differences", "Security baseline handling is stated (enforced, no exceptions)", "Delegation follows least privilege", "Naming convention is consistent"]},
 {"id": "IL27-MOCK-10", "moduleId": "IL27-M24", "title": "Write a patching exception request", "kind": "writing",
  "brief": "A legacy line-of-business app breaks on the latest cumulative update. Write the exception request: the risk you are accepting, the controls compensating for it, and the expiry.",
  "scenario": "APP-LEGACY on SRV-APP-02 fails after KB503XXXX. The vendor needs 60 days for a fix. The server is network-segmented, has no internet, and is backed up nightly.",
  "deliverable": "An exception request with: affected systems, the KB number, business impact of patching vs. not patching, compensating controls (segmentation, no internet, EDR, backup), a named owner, and a 60-day expiry with a re-review date.",
  "rubric": ["KB number and affected systems named", "Compensating controls are specific and verifiable", "Expiry date and re-review are present", "Owner is named", "Risk acceptance is explicit, not implied"]},
 {"id": "IL27-MOCK-11", "moduleId": "IL27-M39", "title": "Write a shift handoff note", "kind": "writing",
  "brief": "Write the handoff note the next shift actually needs: what is broken, what is in flight, and what to watch \u2014 in under 150 words.",
  "scenario": "Overnight: the VPN concentrator flapped twice (stable since 4 AM, vendor case open #88213), ticket #4471 (printer) is waiting on a part, and the backup job on SRV-BKP-01 finished with warnings you have not triaged yet.",
  "deliverable": "A handoff under 150 words with three sections: broken (with case numbers), in-flight (with ticket numbers and next step), and watch items \u2014 each with an owner or a next action.",
  "rubric": ["Under 150 words", "Case/ticket numbers included", "Every item has a next action or owner", "Warnings not yet triaged are flagged, not buried", "Tone is factual, no editorializing"]},
 {"id": "IL27-MOCK-12", "moduleId": "IL27-M38", "title": "Write a tier-1 KB article", "kind": "writing",
  "brief": "Write the KB article tier 1 follows when a user reports the VPN client stuck on 'connecting' \u2014 clear enough that a new hire succeeds on the first read.",
  "scenario": "The common causes in order: expired cached credentials, the client service not running, and a stale virtual adapter. The fix sequence is: re-enter credentials, restart the client service, then reinstall the adapter via the client installer.",
  "deliverable": "A KB article with: symptom in the user's words, causes ordered by frequency, numbered fix steps with exact UI paths or commands, an expected result per step, and an escalation line (what to include in the ticket) if all steps fail.",
  "rubric": ["Symptom phrased as the user reports it", "Causes ordered by observed frequency", "Steps have exact UI paths or commands", "Each step states its expected result", "Escalation line names what to put in the ticket"]},
]

before = len(d['mockTasks'])
d['mockTasks'].extend(NEW_MOCKS)
print(f"mockTasks: {before} -> {len(d['mockTasks'])}")

with open(P, 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write('\n')
d2 = json.load(open(P))
assert len(d2['mockTasks']) == 12, "mockTasks count wrong"
print('validated OK')
