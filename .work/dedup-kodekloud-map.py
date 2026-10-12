#!/usr/bin/env python3
"""Recursive dedup + KodeKloud-style path/career/cert mapping for all 31 IL courses."""
import json, glob, os, copy
from datetime import date

CDIR = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses')
DATA = os.path.expanduser('~/workspace/apex-audit/docs/university/data')
TODAY = '2026-10-09'
INDEP = ("Independent practice and preparation. Not affiliated with, endorsed by, "
         "or sponsored by any vendor or employer; confers no certificate.")

def load(f):
    with open(f) as fh:
        return json.load(fh)

def save(f, d):
    tmp = f + '.tmp'
    with open(tmp, 'w') as fh:
        json.dump(d, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    os.replace(tmp, f)

def course_files():
    return sorted(glob.glob(os.path.join(CDIR, 'il-[0-9]*.json')))

def by_code():
    out = {}
    for f in course_files():
        d = load(f)
        out[d.get('code')] = (f, d)
    return out

# ---------------------------------------------------------------- DEDUP FIXES
def fix_dedup():
    fixes = []
    cmap = by_code()

    # 1. IL-12: khanacademy.org/math appears 6x -> keep 1
    f, d = cmap['IL-12']
    links = d.get('sourceLinks') or []
    seen_urls, new_links, removed = set(), [], 0
    for s in links:
        u = (s.get('url') or '').strip().lower()
        if u == 'https://www.khanacademy.org/math' and u in seen_urls:
            removed += 1
            continue
        seen_urls.add(u)
        new_links.append(s)
    if removed:
        d['sourceLinks'] = new_links
        save(f, d)
        fixes.append(f'IL-12: removed {removed} duplicate khanacademy.org/math sourceLinks')

    # 2. ocw-togo-20261009 signal: fix `courses` field to match host course
    for code, (f, d) in cmap.items():
        changed = False
        for s in (d.get('freshSignals') or []):
            if s.get('id') == 'ocw-togo-20261009':
                if s.get('courses') != [code]:
                    s['courses'] = [code]
                    changed = True
        if changed:
            save(f, d)
            fixes.append(f'{code}: fixed ocw-togo-20261009 signal courses field -> [{code}]')
    return fixes

# ---------------------------------------------------------------- PATHS
PATHS = [
    dict(id='foundations', name='Technology Foundations', type='foundations',
         tagline='Math, programming, and systems fundamentals every technical career stands on.',
         courses=['IL-01','IL-02','IL-03','IL-04','IL-20']),
    dict(id='software-engineer', name='Software Engineer', type='career',
         tagline='From code to production: programming depth, algorithms, and interview readiness.',
         courses=['IL-02','IL-03','IL-08','IL-13']),
    dict(id='fullstack-developer', name='Full-Stack Developer', type='career',
         tagline='Build and ship complete applications across the stack.',
         courses=['IL-02','IL-03','IL-04','IL-08']),
    dict(id='devops-engineer', name='DevOps Engineer', type='career',
         tagline='CI/CD, containers, Kubernetes, Terraform, and cloud platforms.',
         courses=['IL-04','IL-05','IL-14','IL-19','IL-28']),
    dict(id='cloud-architect', name='Cloud Architect', type='career',
         tagline='Design resilient, secure, cost-optimized multicloud architectures.',
         courses=['IL-04','IL-05','IL-19','IL-28']),
    dict(id='sre', name='Site Reliability Engineer', type='career',
         tagline='Keep production alive: observability, incident response, and reliability engineering.',
         courses=['IL-04','IL-05','IL-14','IL-19','IL-28']),
    dict(id='cybersecurity-analyst', name='Cybersecurity Analyst', type='career',
         tagline='Defend systems end to end: security engineering, zero trust, and cert prep.',
         courses=['IL-04','IL-06','IL-11','IL-25','IL-29']),
    dict(id='soc-analyst', name='SOC Analyst', type='career',
         tagline='Detect and respond: operations, endpoint defense, and ThreatLocker assessment prep.',
         courses=['IL-06','IL-11','IL-24','IL-29']),
    dict(id='zero-trust-engineer', name='Zero Trust Engineer', type='career',
         tagline='Architect and operate zero-trust environments with ThreatLocker depth.',
         courses=['IL-06','IL-11','IL-27','IL-29']),
    dict(id='threatlocker-specialist', name='ThreatLocker Specialist', type='career',
         tagline='Master the ThreatLocker platform: assessment prep, CBT, and zero-trust operations.',
         courses=['IL-11','IL-24','IL-27','IL-29']),
    dict(id='it-infrastructure', name='IT Infrastructure Specialist', type='career',
         tagline='Run the backbone: Windows Server, networks, virtualization, and zero-trust infrastructure.',
         courses=['IL-04','IL-11','IL-27']),
    dict(id='data-analyst', name='Data Analyst', type='career',
         tagline='Turn data into decisions: SQL, BI, statistics, and senior-level analytics.',
         courses=['IL-02','IL-03','IL-07','IL-15','IL-20','IL-26']),
    dict(id='data-engineer', name='Data Engineer', type='career',
         tagline='Build the pipelines: data engineering, analytics, and distributed systems.',
         courses=['IL-03','IL-07','IL-08','IL-15','IL-26']),
    dict(id='ml-engineer', name='Machine Learning Engineer', type='career',
         tagline='Ship models to production: math, ML engineering, and MLOps.',
         courses=['IL-02','IL-03','IL-08','IL-12','IL-16','IL-20']),
    dict(id='ai-engineer', name='AI Engineer', type='career',
         tagline='Build with foundation models: AI engineering, agents, and applied ML.',
         courses=['IL-03','IL-12','IL-16','IL-17']),
    dict(id='ai-safety', name='AI Safety Engineer', type='career',
         tagline='Evaluate and red-team AI systems: safety evals, alignment, and defensive practice.',
         courses=['IL-16','IL-17','IL-31']),
    dict(id='tech-lead', name='Technical Leader', type='career',
         tagline='Lead teams and ship strategy: leadership, communication, and professional practice.',
         courses=['IL-10','IL-18','IL-21']),
    dict(id='quantum-safe', name='Quantum-Safe Engineer', type='career',
         tagline='Prepare cryptography for the quantum era: PQC standards and migration engineering.',
         courses=['IL-02','IL-06','IL-20','IL-30']),
    dict(id='frontier-researcher', name='Frontier Researcher', type='career',
         tagline='Work at the edge: esoteric knowledge systems and cutting-edge research distillation.',
         courses=['IL-01','IL-22','IL-23']),
    dict(id='interview-ready', name='Interview Ready', type='certification',
         tagline='Role-specific interview preparation across software, SRE, data, and leadership.',
         courses=['IL-13','IL-14','IL-15','IL-18','IL-24']),
    dict(id='cert-command', name='Certification Command', type='certification',
         tagline='Adaptive certification accelerator — pair with any certification path.',
         courses=['IL-09']),
]

# ---------------------------------------------------------------- CAREERS per course
CAREERS = {
    'IL-01': ['Esoteric Researcher', 'Content Creator'],
    'IL-02': [],
    'IL-03': ['Junior Software Developer', 'Backend Developer', 'Software Engineer'],
    'IL-04': ['Systems Administrator', 'IT Support Specialist', 'Network Administrator', 'IT Infrastructure Specialist'],
    'IL-05': ['DevOps Engineer', 'Platform Engineer', 'Cloud Engineer', 'Site Reliability Engineer'],
    'IL-06': ['Security Analyst', 'SOC Analyst', 'Security Engineer', 'Cybersecurity Analyst'],
    'IL-07': ['Data Engineer', 'Analytics Engineer'],
    'IL-08': ['Software Engineer', 'Backend Engineer', 'Systems Engineer'],
    'IL-09': [],
    'IL-10': [],
    'IL-11': ['SOC Analyst', 'Endpoint Security Analyst', 'Zero Trust Engineer'],
    'IL-12': ['AI Engineer', 'Machine Learning Engineer'],
    'IL-13': [],
    'IL-14': [],
    'IL-15': [],
    'IL-16': ['Machine Learning Engineer', 'Data Scientist', 'AI Engineer'],
    'IL-17': ['AI Engineer', 'Applied AI Engineer', 'AI Agent Developer'],
    'IL-18': ['Engineering Manager', 'Tech Lead', 'Staff Engineer'],
    'IL-19': ['DevOps Engineer', 'Cloud Engineer', 'Multicloud Architect'],
    'IL-20': [],
    'IL-21': [],
    'IL-22': ['Researcher', 'Writer', 'Content Creator'],
    'IL-23': ['Emerging Tech Analyst', 'Research Engineer'],
    'IL-24': ['ThreatLocker Administrator', 'Endpoint Security Specialist'],
    'IL-25': ['Security Analyst', 'Cybersecurity Specialist', 'SOC Analyst'],
    'IL-26': ['Data Analyst', 'Senior Data Analyst', 'Business Intelligence Analyst'],
    'IL-27': ['IT Infrastructure Specialist', 'Systems Administrator', 'Network Administrator'],
    'IL-28': ['DevSecOps Engineer', 'Cloud Security Engineer', 'Senior DevOps Engineer'],
    'IL-29': ['Zero Trust Security Engineer', 'ThreatLocker Specialist', 'Security Engineer'],
    'IL-30': ['Cryptography Engineer', 'Quantum-Safe Security Architect', 'Security Engineer'],
    'IL-31': ['AI Safety Engineer', 'AI Red Team Engineer', 'Trust & Safety Analyst'],
}

# ---------------------------------------------------------------- CERTIFICATIONS to add (only for courses missing them)
# Real certs only. Each: name, issuer, exam, coverage note.
NEW_CERTS = {
    'IL-11': [
        dict(name='CompTIA Security+ (SY0-701)', issuer='CompTIA',
             trackCoverage='Endpoint defense, identity, and zero-trust modules map to Security+ domains.'),
        dict(name='CompTIA CySA+ (CS0-003)', issuer='CompTIA',
             trackCoverage='Detection, analysis, and response workflows map to CySA+ domains.'),
    ],
    'IL-12': [
        dict(name='AWS Certified AI Practitioner (AIF-C01)', issuer='Amazon Web Services',
             trackCoverage='AI fundamentals modules map to AIF-C01 domains.'),
    ],
    'IL-16': [
        dict(name='AWS Certified Machine Learning Engineer – Associate (MLA-C01)', issuer='Amazon Web Services',
             trackCoverage='ML engineering modules map to MLA-C01 domains.'),
        dict(name='AWS Certified AI Practitioner (AIF-C01)', issuer='Amazon Web Services',
             trackCoverage='AI fundamentals coverage maps to AIF-C01.'),
    ],
    'IL-19': [
        dict(name='Certified Kubernetes Administrator (CKA)', issuer='Cloud Native Computing Foundation',
             trackCoverage='Kubernetes modules map to CKA domains.'),
        dict(name='HashiCorp Certified: Terraform Associate (003)', issuer='HashiCorp',
             trackCoverage='Terraform modules map to the Associate exam objectives.'),
        dict(name='AWS Certified Solutions Architect – Associate (SAA-C03)', issuer='Amazon Web Services',
             trackCoverage='AWS architecture modules map to SAA-C03 domains.'),
    ],
    'IL-24': [
        dict(name='ThreatLocker Cyber Hero Certification', issuer='ThreatLocker',
             trackCoverage='Assessment-prep modules map to ThreatLocker certification tracks.'),
    ],
    'IL-25': [
        dict(name='CompTIA Security+ (SY0-701)', issuer='CompTIA',
             trackCoverage='Core security modules map to Security+ domains.'),
        dict(name='ISC2 SSCP – Systems Security Certified Practitioner', issuer='ISC2',
             trackCoverage='Security operations modules map to SSCP domains.'),
    ],
    'IL-26': [
        dict(name='Google Data Analytics Professional Certificate', issuer='Google',
             trackCoverage='Data analyst modules map to the Google certificate curriculum.'),
        dict(name='Microsoft Certified: Power BI Data Analyst Associate (PL-300)', issuer='Microsoft',
             trackCoverage='BI and visualization modules map to PL-300 skills.'),
    ],
    'IL-27': [
        dict(name='CompTIA Network+ (N10-009)', issuer='CompTIA',
             trackCoverage='Networking modules map to Network+ domains.'),
        dict(name='CompTIA Security+ (SY0-701)', issuer='CompTIA',
             trackCoverage='Security modules map to Security+ domains.'),
        dict(name='Microsoft Certified: Windows Server Hybrid Administrator Associate (AZ-800 / AZ-801)', issuer='Microsoft',
             trackCoverage='Windows Server modules map to AZ-800/AZ-801 skills.'),
    ],
    'IL-28': [
        dict(name='Certified Kubernetes Administrator (CKA)', issuer='Cloud Native Computing Foundation',
             trackCoverage='Kubernetes modules map to CKA domains.'),
        dict(name='Certified Kubernetes Security Specialist (CKS)', issuer='Cloud Native Computing Foundation',
             trackCoverage='Security hardening modules map to CKS domains.'),
        dict(name='HashiCorp Certified: Terraform Associate (003)', issuer='HashiCorp',
             trackCoverage='Terraform modules map to the Associate exam objectives.'),
    ],
    'IL-29': [
        dict(name='ThreatLocker Cyber Hero Certification', issuer='ThreatLocker',
             trackCoverage='Zero-trust CBT modules map to ThreatLocker certification tracks.'),
    ],
    'IL-30': [
        dict(name='ISC2 CISSP – Cryptography Domain Study', issuer='ISC2',
             trackCoverage='Cryptography modules support the CISSP Security Architecture & Engineering domain.'),
    ],
    'IL-31': [
        dict(name='NIST AI Risk Management Framework (AI RMF) Practitioner Study', issuer='NIST',
             trackCoverage='Safety eval modules map to the AI RMF Govern/Map/Measure/Manage functions.'),
    ],
}

def apply_mappings():
    cmap = by_code()
    # path id -> path
    pmap = {p['id']: p for p in PATHS}
    # invert: course -> [path ids]
    course_paths = {code: [] for code in cmap}
    for p in PATHS:
        for c in p['courses']:
            if c in course_paths:
                course_paths[c].append(p['id'])

    changed = []
    for code, (f, d) in cmap.items():
        touched = False
        # paths
        want_paths = sorted(course_paths.get(code, []))
        if d.get('paths') != want_paths:
            d['paths'] = want_paths
            touched = True
        # careers
        want_careers = CAREERS.get(code, [])
        if d.get('careers') != want_careers:
            d['careers'] = want_careers
            touched = True
        # certifications: add for missing
        if code in NEW_CERTS and not d.get('certifications'):
            certs = []
            for c in NEW_CERTS[code]:
                certs.append({
                    'name': c['name'],
                    'issuer': c['issuer'],
                    'trackCoverage': c['trackCoverage'],
                    'note': INDEP,
                })
            d['certifications'] = certs
            touched = True
        if touched:
            save(f, d)
            changed.append(code)
    return changed, pmap

def write_learning_paths(pmap):
    cmap = by_code()
    out = {
        'schemaVersion': '1.0',
        'updatedAt': TODAY,
        'title': 'Interstitium Labs — Learning Paths',
        'honesty': ('Paths sequence our courses toward careers and certifications. '
                    + INDEP + ' Paths confer no credential.'),
        'paths': [],
    }
    for p in PATHS:
        total_hours = 0
        careers = []
        certs = []
        for c in p['courses']:
            f, d = cmap[c]
            try:
                total_hours += int(d.get('hours') or 0)
            except Exception:
                pass
            for car in (d.get('careers') or []):
                if car not in careers:
                    careers.append(car)
            for cert in (d.get('certifications') or []):
                n = cert.get('name') if isinstance(cert, dict) else str(cert)
                if n and n not in certs:
                    certs.append(n)
        entry = dict(p)
        entry['totalHours'] = total_hours
        entry['careers'] = careers
        entry['certifications'] = certs
        entry['noahNote'] = ('Noah AI tutors every course in this path — pick a persona, '
                             'ask questions by voice or text, and get adaptive review.')
        out['paths'].append(entry)
    # also: career -> paths, cert -> paths indexes
    career_index = {}
    cert_index = {}
    for e in out['paths']:
        for car in e['careers']:
            career_index.setdefault(car, []).append(e['id'])
        for ct in e['certifications']:
            cert_index.setdefault(ct, []).append(e['id'])
    out['careerIndex'] = career_index
    out['certificationIndex'] = cert_index
    path = os.path.join(DATA, 'learning-paths.json')
    with open(path, 'w') as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    return path, len(out['paths']), len(career_index), len(cert_index)

def update_specs():
    cmap = by_code()
    specdir = os.path.expanduser('~/workspace/apex-audit/.work/course-spec-clone/specs')
    updated = []
    for code, (f, d) in cmap.items():
        sp = os.path.join(specdir, code.replace('-', '') + '.md')
        # specs are named like IL-05.md
        alt = os.path.join(specdir, code + '.md')
        target = sp if os.path.exists(sp) else (alt if os.path.exists(alt) else None)
        if not target:
            continue
        with open(target) as fh:
            txt = fh.read()
        # Build the new section
        paths = d.get('paths') or []
        careers = d.get('careers') or []
        certs = d.get('certifications') or []
        section = '\n## Learning Paths (KodeKloud-style mapping)\n'
        if paths:
            section += 'This course is part of the following learning paths:\n'
            for pid in paths:
                section += f'- `{pid}`\n'
        else:
            section += 'Foundational / accelerator course — included across paths as a prerequisite or accelerator.\n'
        section += '\n## Career Mapping\n'
        if careers:
            for c in careers:
                section += f'- {c}\n'
        else:
            section += 'Foundational / prep course — supports all technical career tracks.\n'
        section += '\n## Certification Mapping (independent-prep framing)\n'
        if certs:
            for c in certs:
                nm = c.get('name') if isinstance(c, dict) else str(c)
                iss = c.get('issuer', '') if isinstance(c, dict) else ''
                section += f'- {nm}' + (f' — {iss}' if iss else '') + '\n'
            section += f'\n{INDEP}\n'
        else:
            section += 'No direct vendor certification target — portfolio and interview evidence.\n'
        # Append if not already present
        if '## Learning Paths (KodeKloud-style mapping)' in txt:
            continue
        # Append before Honesty Note if present, else at end
        marker = '## Honesty Note'
        if marker in txt:
            txt = txt.replace(marker, section + '\n' + marker, 1)
        else:
            txt = txt.rstrip() + '\n' + section
        with open(target, 'w') as fh:
            fh.write(txt)
        updated.append(code)
    return updated

if __name__ == '__main__':
    print('--- DEDUP FIXES ---')
    for x in fix_dedup():
        print(' ', x)
    print('--- MAPPINGS ---')
    changed, pmap = apply_mappings()
    print('  courses updated:', len(changed), changed)
    print('--- LEARNING-PATHS.JSON ---')
    p, np, nc, nct = write_learning_paths(pmap)
    print(f'  wrote {p}: {np} paths, {nc} careers, {nct} certs')
    print('--- SPEC SHEETS ---')
    upd = update_specs()
    print('  spec sheets updated:', len(upd))
