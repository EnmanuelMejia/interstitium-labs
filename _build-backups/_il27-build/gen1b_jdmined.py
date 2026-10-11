"""IL-27 certs.json — part 1b: append JD rows mined from REAL ThreatLocker IT postings.

Sources (publicly retrieved 2026-10-07, paraphrased — not quoted at length):
 S1 = Special Project IT Engineer, ThreatLocker — startup.jobs
      https://startup.jobs/special-project-it-engineer-threatlocker-5346652 (HTTP 200, full text fetched)
 S2 = Senior Technical Support Specialist, ThreatLocker (Orlando FL) — grabjobs.co
      https://grabjobs.co/us/job/full-time/others/senior-technical-support-specialist-139286526
      (retrieved via search-engine snippet 2026-10-07; full page not fetched)
Neither is the IT Infrastructure Specialist posting. Every row is labeled accordingly —
never presented as the Infrastructure Specialist JD.
"""
import json, os

PARTS = os.path.expanduser("~/workspace/apex-audit/docs/university/data/courses/_il27-build/parts")
p = os.path.join(PARTS, "course.json")
doc = json.load(open(p))

S1_TITLE = "Special Project IT Engineer — ThreatLocker (adjacent ThreatLocker IT posting; NOT the IT Infrastructure Specialist posting)"
S1_URL = "https://startup.jobs/special-project-it-engineer-threatlocker-5346652"
S1_STATUS = ("HTTP 200 verified 2026-10-07 — real ThreatLocker IT posting fetched in full. "
             "ADJACENT role, not the IT Infrastructure Specialist posting: requirements below are paraphrased "
             "from its listed duties/qualifications and mapped to IL-27 modules as role-profile grounding.")

S2_TITLE = "Senior Technical Support Specialist — ThreatLocker, Orlando FL (adjacent ThreatLocker IT posting; NOT the IT Infrastructure Specialist posting)"
S2_URL = "https://grabjobs.co/us/job/full-time/others/senior-technical-support-specialist-139286526"
S2_STATUS = ("Retrieved via search-engine snippet 2026-10-07 — full page not fetched; requirements paraphrased "
             "from the visible snippet. ADJACENT role, not the IT Infrastructure Specialist posting.")

def mrow(title, url, status, requirement, modules, certDomain, portfolioArtifact):
    return {"postingTitle": title, "postingUrl": url, "employer": "ThreatLocker",
            "urlStatus": status, "requirement": requirement, "modules": modules,
            "certDomain": certDomain, "portfolioArtifact": portfolioArtifact}

mined = [
 # --- from S1: Special Project IT Engineer (real posting) ---
 mrow(S1_TITLE, S1_URL, S1_STATUS,
      "Diagnose and resolve complex customer issues related to IT systems (high-end L2/L3 engineer profile; MSP or corporate IT background preferred)",
      ["IL27-M04", "IL27-M10", "IL27-M21"], "A+: Troubleshooting; Network+: Troubleshooting; AZ-801: Monitor & troubleshoot",
      "Complex-issue triage write-up: two annotated L3 escalations from lab work"),
 mrow(S1_TITLE, S1_URL, S1_STATUS,
      "Deploy and manage IT systems including O365, Active Directory, and networking infrastructure",
      ["IL27-M15", "IL27-M22"], "AZ-800: AD DS on-prem & cloud; MD-102: Deploy Windows client",
      "AD + M365 deployment notes: tenant setup, user provisioning, license assignment"),
 mrow(S1_TITLE, S1_URL, S1_STATUS,
      "Develop and execute test scripts for various IT systems and applications; strong understanding of API integrations and scripting languages",
      ["IL27-M16", "IL27-M21"], "AZ-800: Manage Windows Servers; AZ-801: Monitor & troubleshoot",
      "PowerShell test-script portfolio: health checks, API-integration smoke tests"),
 mrow(S1_TITLE, S1_URL, S1_STATUS,
      "Conduct in-depth research on products and technologies to enhance company offerings; stay updated on emerging technologies",
      ["IL27-M13"], "Security+: Security architecture",
      "Technology evaluation one-pager: options, trade-offs, recommendation"),
 mrow(S1_TITLE, S1_URL, S1_STATUS,
      "Document processes, procedures, and troubleshooting steps for internal knowledge sharing",
      ["IL27-M06", "IL27-M09"], "A+ 1102: Operational Procedures; Network+: Operations",
      "KB article portfolio: five annotated how-tos from lab work"),
 mrow(S1_TITLE, S1_URL, S1_STATUS,
      "Effective communication and interpersonal skills for customers and internal teams; work independently and collaborate in a team environment",
      ["IL27-M06"], "A+ 1102: Operational Procedures",
      "Customer-communication scripts: status updates, outage notices, handoff notes"),
 mrow(S1_TITLE, S1_URL, S1_STATUS,
      "Certifications such as CCNA, MCSA, or equivalent are a plus (employer values vendor certs)",
      ["IL27-M07", "IL27-M15"], "Network+; AZ-800 — full IL-27 crosswalk",
      "Certification plan: readiness-dashboard printout with target sit dates"),
 # --- from S2: Senior Technical Support Specialist (real posting, snippet) ---
 mrow(S2_TITLE, S2_URL, S2_STATUS,
      "Strong troubleshooting and diagnostic skills across hardware, software, and network layers",
      ["IL27-M04", "IL27-M10"], "A+: Troubleshooting; Network+: Troubleshooting",
      "Layered triage runbook: hardware, OS, and network decision trees"),
 mrow(S2_TITLE, S2_URL, S2_STATUS,
      "Solid knowledge of Windows and/or Linux environments; scripting or automation experience (PowerShell, Bash, Python)",
      ["IL27-M05", "IL27-M16"], "A+ 1102: Operating Systems; AZ-800: Manage Windows Servers",
      "PowerShell toolkit: user-provisioning script, log parser, health-check script"),
 mrow(S2_TITLE, S2_URL, S2_STATUS,
      "Willingness to be onsite full-time for shift work and take part in an on-call schedule; SLA-aware support mindset",
      ["IL27-M06"], "A+ 1102: Operational Procedures",
      "On-call readiness notes: escalation tiers, SLA targets, handoff template"),
 mrow(S2_TITLE, S2_URL, S2_STATUS,
      "Relevant certifications (CompTIA, ITIL, Microsoft, AWS, etc.) preferred — employer explicitly rewards certification",
      ["IL27-M01", "IL27-M11", "IL27-M22"], "A+; Security+; MD-102 — full IL-27 crosswalk",
      "Certification plan: readiness-dashboard printout with target sit dates"),
]

doc["jdMatrix"].extend(mined)
with open(p, "w") as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
print("part1b ok: jdMatrix now", len(doc["jdMatrix"]), "rows (10 role-profile + 11 mined)")
