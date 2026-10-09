"""Add noahTutoring integration to completed courses (Groups A + E: IL-01..IL-06, IL-26..IL-29)."""
import json, os

BASE = '/home/hatch/workspace/apex-audit/docs/university/data/courses'

PERSONA_DESC = {
    'visionary': 'Big-picture connections, future implications, "why this matters" framing',
    'engineer': 'Hands-on labs, debugging, building, technical deep-dives',
    'philosopher': 'First principles, conceptual foundations, Socratic questioning',
    'mentor': 'Guided practice, encouragement, review, study planning',
    'trickster': 'Adversary mindset (defensive), edge cases, "what breaks this?" thinking',
}

def tutoring(code, primary, secondary, focus_notes, module_hint):
    return {
        'enabled': True,
        'driver': 'Noah AI is the core tutoring driver for this course — personalized, self-paced, voice-first tutoring, not a bolt-on.',
        'differentiator': 'Self-paced personalized tutoring powered by Noah: the course adapts to the learner, not the other way around.',
        'personas': primary + secondary,
        'personaRoles': {p: PERSONA_DESC[p] for p in primary + secondary},
        'primaryPersona': primary[0],
        'moduleGuidance': module_hint,
        'voices': {
            'count': 5,
            'note': 'Five distinct natural server-generated voices. Learners choose their tutor voice; each persona can carry its own voice.',
        },
        'adaptive': 'SM-2 spaced repetition drives review scheduling; Noah tracks mastery per module and re-routes the learner to weak areas.',
        'voiceChat': True,
        'voiceChatNote': 'Full voice conversation with Noah while working through modules — ask questions aloud, get spoken explanations.',
        'courseAware': True,
        'courseAwareNote': f'Noah is course-aware for {code}: it knows the module sequence, prerequisites, and certification objectives, and tutors accordingly.',
        'focusNotes': focus_notes,
    }

CONFIG = {
    'il-01-esoteric-foundations': dict(
        code='IL-01', primary=['philosopher', 'visionary'], secondary=['mentor'],
        focus_notes='Philosopher leads contemplative modules via Socratic dialogue; Visionary connects esoteric systems across traditions; Mentor guides reflective review.',
        module_hint='Philosopher fronts foundations modules; Visionary fronts synthesis/comparison modules.',
    ),
    'il-02-mathematical-maturity-engine': dict(
        code='IL-02', primary=['mentor', 'engineer'], secondary=['philosopher'],
        focus_notes='Mentor guides step-by-step proof practice; Engineer runs problem-solving drills; Philosopher grounds concepts in first principles.',
        module_hint='Mentor fronts proof-technique modules; Engineer fronts computation/drill modules.',
    ),
    'il-03-programming-language-forge': dict(
        code='IL-03', primary=['engineer', 'mentor'], secondary=['philosopher'],
        focus_notes='Engineer pair-programs through language labs; Mentor debugs with the learner; Philosopher explains language design from first principles.',
        module_hint='Engineer fronts all hands-on language labs; Mentor fronts debugging/review modules.',
    ),
    'il-04-systems-linux-windows-networks': dict(
        code='IL-04', primary=['engineer', 'trickster'], secondary=['mentor'],
        focus_notes='Engineer walks through systems labs; Trickster poses "what breaks?" troubleshooting scenarios (defensive); Mentor reviews networking fundamentals.',
        module_hint='Engineer fronts lab modules; Trickster fronts troubleshooting/diagnostic modules.',
    ),
    'il-05-cloud-devsecops-platform-sre': dict(
        code='IL-05', primary=['engineer', 'visionary'], secondary=['mentor'],
        focus_notes='Engineer guides infrastructure-as-code labs; Visionary frames platform architecture decisions; Mentor reviews SRE practices.',
        module_hint='Engineer fronts IaC/pipeline labs; Visionary fronts architecture/design modules.',
    ),
    'il-06-cybersecurity-secure-engineering': dict(
        code='IL-06', primary=['trickster', 'engineer'], secondary=['mentor'],
        focus_notes='Trickster teaches adversary mindset for defensive engineering; Engineer runs secure-coding labs; Mentor reviews security fundamentals. All adversary content is defensive-framed.',
        module_hint='Trickster fronts threat-model modules (defensive); Engineer fronts secure-engineering labs.',
    ),
    'il-26-data-analyst-certification-senior-mastery': dict(
        code='IL-26', primary=['mentor', 'engineer'], secondary=['visionary'],
        focus_notes='Mentor guides analytical thinking and portfolio building; Engineer runs SQL/Python labs; Visionary connects analysis to business impact (senior bar).',
        module_hint='Mentor fronts analysis-method modules; Engineer fronts SQL/Python/data labs.',
    ),
    'il-27-it-infrastructure-specialist-threatlocker-mastery': dict(
        code='IL-27', primary=['engineer', 'mentor'], secondary=['trickster'],
        focus_notes='Engineer guides Windows Server/AD/Hyper-V labs; Mentor runs troubleshooting practice; Trickster poses infrastructure failure scenarios.',
        module_hint='Engineer fronts all infrastructure labs; Mentor fronts review/assessment modules.',
    ),
    'il-28-devsecops-cloud-infrastructure-mastery': dict(
        code='IL-28', primary=['engineer', 'visionary'], secondary=['mentor'],
        focus_notes='Engineer drives production pipeline labs; Visionary frames platform architecture; Mentor reviews DevSecOps practices.',
        module_hint='Engineer fronts pipeline/infra labs; Visionary fronts architecture modules.',
    ),
    'il-29-threatlocker-ai-cybersecurity-mastery': dict(
        code='IL-29', primary=['trickster', 'engineer', 'mentor'], secondary=['visionary'],
        focus_notes='Trickster teaches zero-trust adversary thinking (defensive); Engineer runs allowlisting/ringfencing labs; Mentor drives assessment readiness. ThreatLocker branding stays prominent; independent-prep framing preserved.',
        module_hint='Trickster fronts zero-trust/threat modules (defensive); Engineer fronts hands-on labs; Mentor fronts assessment-prep modules.',
    ),
}

results = []
for slug, cfg in CONFIG.items():
    path = os.path.join(BASE, slug + '.json')
    with open(path) as f:
        d = json.load(f)
    d['noahTutoring'] = tutoring(**cfg)
    d['updatedAt'] = '2026-10-09'
    with open(path, 'w') as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
        f.write('\n')
    # validate
    d2 = json.load(open(path))
    assert d2['noahTutoring']['enabled'] is True
    assert d2['schemaVersion'] == '4'
    results.append(f"{cfg['code']}: noahTutoring added, personas={d2['noahTutoring']['personas']}")

print('\n'.join(results))
print(f'\nDone: {len(results)} courses updated.')
