#!/usr/bin/env python3
"""Group E (IL-26..IL-29) course audit: apply fixes, write spec sheets + audit reports."""
import json, os, shutil, copy, re

COURSES = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')
SPECS = os.path.expanduser('~/workspace/apex-audit/.work/course-spec-clone/specs')
DATE = '2026-10-09'

V4_KEYS = ['code','courseId','title','tagline','blurb','hours','mockMinutes','schemaVersion',
'updatedAt','honestyNote','objectives','arc','priorities','battlePlan','modules',
'crosswalk','certGates','readinessDashboard','scriptLabs','drills','scenarios',
'trainers','terminalSims','mockTasks','cheatSheets','answerBank','sourceLinks',
'toolLabs','multicloudLabs','sampleDatasets','installSteps','installPrereqOrder',
'installLabs','employerMappings','jdMatrix','sqlPlaygrounds','pythonExercises',
'daxPlaygrounds','branchingScenarios','clickSims','interactivityAudit','studyGuide',
'timeFormula','glossary','faq','tips','legends','topicTheme','topic']

FILES = {
 'IL-26': 'il-26-data-analyst-certification-senior-mastery.json',
 'IL-27': 'il-27-it-infrastructure-specialist-threatlocker-mastery.json',
 'IL-28': 'il-28-devsecops-cloud-infrastructure-mastery.json',
 'IL-29': 'il-29-threatlocker-ai-cybersecurity-mastery.json',
}

CANON_FORMULA = ("estimatedMinutes per module = instruction + videos + drills + hands-on lab, "
 "set per module by the author; course total = sum of module estimates. "
 "Declared hours are the honest rounded sum.")

CROSSLINK_ADDS = {
 'IL-26': ('IL26-M08', {'course': 'il-07-data-engineering-analytics-ai',
   'moduleId': 'il07-data-schools', 'topic': 'The Data-School Spine',
   'why': 'IL-07 teaches data-engineering foundations; this module applies SQL at analyst depth.'}),
 'IL-28': ('IL28-M44', {'course': 'il-05-cloud-devsecops-platform-sre',
   'moduleId': 'il05-devops-core', 'topic': 'DevOps at Cloud-Native Parity',
   'why': 'IL-05 teaches cloud/DevOps foundations; this module deepens production mastery.'}),
 'IL-29a': ('IL29-M01', {'course': 'il-11-zero-trust-endpoint-defense',
   'moduleId': 'il11-zero-trust-foundations--zt-default-deny', 'topic': 'Default-Deny Architecture',
   'why': 'IL-11 teaches zero-trust theory; this module applies it at ThreatLocker operator depth.'}),
 'IL-29b': ('IL29-M41', {'course': 'il-06-cybersecurity-secure-engineering',
   'moduleId': 'il06-defensive', 'topic': 'Defensive Operations: SOC to Incident Response',
   'why': 'IL-06 teaches security operations; this module applies IR at the endpoint.'}),
}

def load(code):
    with open(os.path.join(COURSES, FILES[code])) as f:
        return json.load(f)

def save(code, d):
    p = os.path.join(COURSES, FILES[code])
    tmp = p + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write('\n')
    json.load(open(tmp))  # validate
    os.replace(tmp, p)

results = {}

for code, fname in FILES.items():
    p = os.path.join(COURSES, fname)
    shutil.copy2(p, p + '.auditbak-20261009')
    d = load(code)
    mods = d.get('modules', [])
    fixes = []
    pre_missing = [k for k in V4_KEYS if k not in d]
    pre_schema = repr(d.get('schemaVersion'))

    # 1. schemaVersion -> "4" string
    if d.get('schemaVersion') != '4':
        d['schemaVersion'] = '4'; fixes.append('schemaVersion int 4 -> string "4"')
    # 2. timeFormula
    if 'timeFormula' not in d:
        d['timeFormula'] = CANON_FORMULA; fixes.append('added timeFormula (canonical template formula)')
    # 3. IL-27 missing keys -> honest empty lists
    if code == 'IL-27':
        for k in ['multicloudLabs','sampleDatasets','installSteps','installPrereqOrder',
                  'employerMappings','sqlPlaygrounds','pythonExercises','daxPlaygrounds']:
            if k not in d:
                d[k] = []; fixes.append('added %s = [] (section not applicable; no content invented)' % k)
    # 4. IL-26 stale blurb hours
    if code == 'IL-26' and '96-hour' in d.get('blurb',''):
        d['blurb'] = d['blurb'].replace('96-hour', '414-hour', 1)
        fixes.append('blurb "96-hour" -> "414-hour" (stale copy; declared hours = 414)')
    if code == 'IL-26' and d.get('tagline','').startswith('From zero to certified senior'):
        d['tagline'] = d['tagline'].replace('From zero to certified senior:', 'From zero to senior-ready:')
        fixes.append('tagline "certified senior" -> "senior-ready" (course confers no certificate)')
    # 5. cross-links
    def add_xlink(host_id, entry):
        for m in mods:
            if m['id'] == host_id:
                cl = m.get('crossLinks') or []
                if not any(isinstance(x, dict) and x.get('course') == entry['course'] for x in cl):
                    cl.append(entry); m['crossLinks'] = cl
                    return True
        return False
    if code == 'IL-26':
        if add_xlink(*CROSSLINK_ADDS['IL-26']): fixes.append('cross-link IL26-M08 -> IL-07 added')
    if code == 'IL-28':
        if add_xlink(*CROSSLINK_ADDS['IL-28']): fixes.append('cross-link IL28-M44 -> IL-05 added')
    if code == 'IL-29':
        if add_xlink(*CROSSLINK_ADDS['IL-29a']): fixes.append('cross-link IL29-M01 -> IL-11 added')
        if add_xlink(*CROSSLINK_ADDS['IL-29b']): fixes.append('cross-link IL29-M41 -> IL-06 added')
    # 6. updatedAt
    if fixes:
        d['updatedAt'] = DATE; fixes.append('updatedAt -> %s' % DATE)
    save(code, d)
    post_missing = [k for k in V4_KEYS if k not in d]
    results[code] = {'fixes': fixes, 'pre_missing': pre_missing, 'post_missing': post_missing,
                     'pre_schema': pre_schema}
    print(code, '| pre-missing:', pre_missing, '| fixes:', len(fixes))

json.dump(results, open(os.path.join(SPECS, '_fixlog.json'), 'w'), indent=2)
print('fixlog written')
