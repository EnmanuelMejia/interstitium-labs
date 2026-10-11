"""Retrofit IL-11 modules to the IL-19 (Multicloud) course template shape.
Reads expansions.py, applies to il-11-zero-trust-endpoint-defense.json, validates, writes atomically.
NEVER touches il-19 or il-23.
"""
import json, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses/il-11-zero-trust-endpoint-defense.json')
sys.path.insert(0, HERE)
from expansions import EXPANSIONS

BANNED_NEW = ['aleks', 'brilliant', 'khan academy', 'coursera', 'udemy', 'edx', 'palantir']

def main():
    with open(SRC, encoding='utf-8') as f:
        course = json.load(f)
    modules = course['modules']
    print('modules in file:', len(modules))

    missing = [m['id'] for m in modules if m['id'] not in EXPANSIONS]
    if missing:
        raise SystemExit('MISSING expansions for: %s' % missing)
    extra = [k for k in EXPANSIONS if k not in {m['id'] for m in modules}]
    if extra:
        raise SystemExit('EXTRA expansions not in file: %s' % extra)

    honesty = course['honestyNote']
    thin_before = []

    for m in modules:
        exp = EXPANSIONS[m['id']]
        thin = len(m['notes']) < 4 or len(m['cards']) < 5 or len(m['quiz']) < 4
        thin_before.append((m['title'], thin))

        # --- summary: instructor voice ---
        m['summary'] = exp['summary']
        # --- objectives: action verbs ---
        m['objectives'] = exp['objectives']
        # --- notes: the four titled sections ---
        concepts_body = '\n'.join(exp['concepts'])
        proc_body = exp['procedure_intro'] + '\n' + '\n'.join(exp['procedure_steps'])
        checkin_body = ('Noah probes mastery with questions like:\n' +
                        '\n'.join('- ' + q for q in exp['checkin']) +
                        '\n\n' + honesty)
        m['notes'] = [
            {'title': 'Concepts', 'body': concepts_body},
            {'title': 'Hands-on procedure', 'body': proc_body},
            {'title': 'Project brief', 'body': exp['project']},
            {'title': 'Noah check-in', 'body': checkin_body},
        ]
        # --- cards ---
        m['cards'] = [{'front': c['front'], 'back': c['back']} for c in exp['cards']]
        # --- quiz ---
        m['quiz'] = [{'q': q['q'], 'choices': list(q['choices']),
                      'answer': q['answer'], 'explain': q['explain']} for q in exp['quiz']]

    # --- course level: terminal sims (renderer consumes generically, proven via course-shell.js) ---
    course['terminalSims'] = [
        {
            'id': 'zt-policy-decision',
            'title': 'Zero Trust policy decision simulator',
            'brief': 'Play the policy engine: evaluate access requests against identity, device, location, and risk signals — the per-session decision from the NIST tenets module.',
            'prompt': 'policy-engine>',
            'commands': [
                {'cmd': 'request dispatcher payroll-app', 'out': 'signals: user=dispatcher (known), device=non-compliant phone, location=home, risk=medium\ndecision: STEP-UP — require phishing-resistant MFA before granting payroll-app'},
                {'cmd': 'request dispatcher payroll-app --mfa fido2', 'out': 'signals: user=dispatcher (known), device=non-compliant phone, location=home, risk=medium, mfa=fido2\ndecision: ALLOW (session) — phishing-resistant MFA satisfies the step-up; re-evaluate continuously'},
                {'cmd': 'request attacker payroll-app', 'out': 'signals: user=unknown, device=unmanaged, location=foreign, risk=high\ndecision: DENY — implicit trust is never granted; block and alert the SOC'},
                {'cmd': 'request admin dc-console', 'out': 'signals: user=admin, device=compliant paw, location=hq, risk=low\ndecision: ALLOW (session) — Tier 0 credential on Tier 0 workstation, compliant device, known location'},
                {'cmd': 'signals', 'out': 'evaluated per request: user identity, device compliance, network location, sign-in risk, resource sensitivity'},
            ],
        },
        {
            'id': 'ad-hygiene',
            'title': 'PowerShell AD hygiene simulator',
            'brief': 'Practice the identity-plane audit commands from the AD modules against a realistic simulated directory.',
            'prompt': 'PS C:\\>',
            'commands': [
                {'cmd': 'Get-ADGroupMember "Domain Admins" -Recursive', 'out': 'Administrator\nsvc-backup (service account — finding: review)\nold-admin-jdoe (departed 2024 — finding: remove)'},
                {'cmd': 'Get-ADUser -Filter * -Properties PasswordLastSet | Where-Object { $_.Enabled -eq $true }', 'out': '312 enabled users returned. 4 service accounts with PasswordLastSet older than 1 year — rotate or manage.'},
                {'cmd': 'Get-ADUser -Filter { Kerberos preauth disabled }', 'out': 'No output means clean. Here: svc-legacy-app — AS-REP roastable. Enable pre-authentication.'},
                {'cmd': 'audit-laps', 'out': '247/250 workstations report unique rotated local admin passwords. 3 failures — remediate before enforcement week.'},
            ],
        },
        {
            'id': 'kql-detection',
            'title': 'KQL detection simulator',
            'brief': 'Query simulated Entra sign-in data with KQL — the failure hunts and anomaly checks from the troubleshooting module.',
            'prompt': 'kql>',
            'commands': [
                {'cmd': 'SigninLogs | where ResultType != 0 | take 3', 'out': 'dispatcher@harborview | 50126 (invalid credentials) | 10.4.0.21\nfinance@harborview | 50076 (MFA required, not completed) | 10.4.0.88\nadmin@harborview | 50074 (strong auth required) | 203.0.113.7 <- foreign IP: investigate'},
                {'cmd': 'SigninLogs | where UserPrincipalName == "admin@harborview" | summarize count() by IPAddress', 'out': '10.4.0.2: 41\n203.0.113.7: 3 <- anomalous: correlate with the CA risk policy evaluation'},
                {'cmd': 'help-hunt', 'out': 'start with failures (ResultType != 0), correlate by user/IP/app, then check which CA policy evaluated — evidence before conclusions'},
            ],
        },
    ]

    # --- course level: enrich cheat sheet command blocks with code/lang (template shape) ---
    for cs in course['cheatSheets']:
        for b in cs['blocks']:
            if b['h'] == 'List Domain Admins (recursive)' and 'code' not in b:
                b['code'] = 'Get-ADGroupMember "Domain Admins" -Recursive | Select-Object name, objectClass'
                b['lang'] = 'powershell'
            elif b['h'] == 'Failed sign-ins (KQL)' and 'code' not in b:
                b['code'] = ('SigninLogs\n| where ResultType != 0\n'
                             '| summarize failures = count() by UserPrincipalName, AppDisplayName\n| order by failures desc')
                b['lang'] = 'kql'
            elif b['h'] == 'Verify a download (PowerShell)' and 'code' not in b:
                b['code'] = ('Get-FileHash .\\installer.exe -Algorithm SHA256\n'
                             '# compare the output digest against the vendor-published checksum\n# mismatch = do not install')
                b['lang'] = 'powershell'

    # ================= VALIDATION =================
    errs = []
    for m in modules:
        titles = [n['title'] for n in m['notes']]
        if titles != ['Concepts', 'Hands-on procedure', 'Project brief', 'Noah check-in']:
            errs.append('%s: bad note titles %s' % (m['id'], titles))
        for n in m['notes']:
            for line in n['body'].split('\n'):
                if n['title'] == 'Concepts' and line.startswith('- ') and not re.match(r'^- \*\*.+?\*\* — ', line):
                    errs.append('%s: Concepts bullet not in glossary shape: %s' % (m['id'], line[:70]))
        if len(m['cards']) < 6:
            errs.append('%s: cards < 6' % m['id'])
        for c in m['cards']:
            if not c.get('front') or not c.get('back'):
                errs.append('%s: empty card' % m['id'])
        if len(m['quiz']) < 4:
            errs.append('%s: quiz < 4' % m['id'])
        for q in m['quiz']:
            if len(q['choices']) != 4:
                errs.append('%s: quiz choices != 4: %s' % (m['id'], q['q'][:50]))
            if not isinstance(q['answer'], int) or not (0 <= q['answer'] <= 3):
                errs.append('%s: bad answer index: %s' % (m['id'], q['q'][:50]))
            if not q.get('explain'):
                errs.append('%s: empty explain: %s' % (m['id'], q['q'][:50]))
        if not m['summary'].startswith("Welcome"):
            errs.append('%s: summary not instructor voice' % m['id'])

    blob = json.dumps(course).lower()
    for bad in BANNED_NEW:
        if bad in blob:
            errs.append('banned term introduced: %s' % bad)
    for k in ['arc', 'priorities', 'battlePlan', 'mockTasks', 'cheatSheets', 'answerBank', 'sourceLinks']:
        if not course.get(k):
            errs.append('missing course key: %s' % k)
    if not isinstance(course.get('mockMinutes'), int):
        errs.append('mockMinutes not int')
    for s in course['sourceLinks']:
        if not s.get('retrieved'):
            errs.append('sourceLink missing retrieved: %s' % s.get('name'))
    for t in course['mockTasks']:
        if len(t['choices']) != 4 or not isinstance(t['answer'], int) or not t.get('explain'):
            errs.append('bad mockTask: %s' % t['id'])

    if errs:
        print('VALIDATION ERRORS:')
        for e in errs:
            print(' -', e)
        raise SystemExit('validation failed')

    # ================= WRITE (atomic) =================
    tmp = SRC + '.retrofit-tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(course, f, ensure_ascii=False, indent=1)
        f.write('\n')
    with open(tmp, encoding='utf-8') as f:
        json.load(f)  # json.load AFTER writing
    os.replace(tmp, SRC)
    print('wrote OK:', SRC)

    print('\nTHIN MODULES EXPANDED (thin = <4 notes or <5 cards or <4 quiz before):')
    for title, thin in thin_before:
        print(('  [EXPANDED] ' if thin else '  [restructured] ') + title)
    print('\nterminalSims added: %d | trainers kept: %d' % (len(course['terminalSims']), len(course.get('trainers', []))))
    print('mockTasks:', len(course['mockTasks']), '| cheatSheets:', len(course['cheatSheets']),
          '| answerBank:', len(course['answerBank']), '| sourceLinks:', len(course['sourceLinks']))

if __name__ == '__main__':
    main()
