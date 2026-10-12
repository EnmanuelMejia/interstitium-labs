"""Enrich IL-19..IL-25 noahTutoring from 6-key thin to 10-key standard."""
import json, os

BASE = '/home/hatch/workspace/apex-audit/docs/university/data/courses'

# Per-course enrichment content
ENRICH = {
    'il-19-multicloud-devops-ai-bootcamp': {
        'tagline': 'Noah is the learning driver — not a bolt-on.',
        'concept': 'Noah is the core learning driver of IL-19 — a personal multicloud architect and DevOps coach with five voices and five minds. Every cloud platform and pipeline stage pairs with the persona that teaches it best.',
        'bleedingEdge': 'Multicloud moves fast — Noah surfaces current provider developments via the daily-fold pipeline and keeps labs aligned to live console realities.',
        'houseRule': 'Bring Noah your architecture hypothesis — not "just give me the answer." Attempt the lab first.',
        'howToUse': ['Open Noah from any module and pick the persona mapped to that platform.', 'Attempt the hands-on lab first, then bring Noah your debugging hypothesis.', 'Use voice chat to whiteboard architecture decisions aloud.'],
    },
    'il-20-mathematics': {
        'tagline': 'Noah is the learning driver — not a bolt-on.',
        'concept': 'Noah is the core learning driver of IL-20 — a personal mathematics tutor with five voices and five minds. Proofs pair with Philosopher, computations with Engineer, practice with Mentor.',
        'bleedingEdge': None,
        'houseRule': 'Attempt the proof or problem first — then bring Noah your approach, not your blank stare.',
        'howToUse': ['Open Noah from any module and pick the mapped persona.', 'Work the problem first, then ask Noah to check your reasoning step by step.', 'Use voice chat to talk through proofs aloud.'],
    },
    'il-21-humanities': {
        'tagline': 'Noah is the learning driver — not a bolt-on.',
        'concept': 'Noah is the core learning driver of IL-21 — a personal humanities tutor with five voices and five minds. Philosopher leads deep reading; Visionary connects ideas across eras.',
        'bleedingEdge': None,
        'houseRule': 'Read first, reflect, then bring Noah your interpretation to stress-test.',
        'howToUse': ['Open Noah from any module for Socratic dialogue.', 'Bring your essay thesis to Noah before you write.', 'Use voice chat for seminar-style discussion.'],
    },
    'il-22-esoteric-secret-knowledge': {
        'tagline': 'Noah is the learning driver — not a bolt-on.',
        'concept': 'Noah is the core learning driver of IL-22 — a personal guide through esoteric systems with five voices and five minds. Philosopher leads contemplative study; Visionary maps cross-tradition connections.',
        'bleedingEdge': None,
        'houseRule': 'Study the primary material first — then bring Noah your synthesis, not your confusion.',
        'howToUse': ['Open Noah for guided contemplative study.', 'Ask Visionary to connect systems across traditions.', 'Use voice chat for reflective dialogue.'],
    },
    'il-23-frontier-knowledge': {
        'tagline': 'Noah is the learning driver — not a bolt-on.',
        'concept': 'Noah is the core learning driver of IL-23 — a personal frontier-research tutor with five voices and five minds. The frontier moves fast; Noah keeps you current via the daily-fold pipeline.',
        'bleedingEdge': 'The frontier is Noah\'s home turf: daily-fold trending signals feed directly into tutoring, so learners always study the current edge, not last year\'s.',
        'houseRule': 'Check the asOf date on every frontier claim — then ask Noah what has changed since.',
        'howToUse': ['Open Noah from any frontier module for current-context tutoring.', 'Ask what has changed since the module asOf date.', 'Use voice chat to debate frontier implications.'],
        'frontierNote': 'IL-23 is the frontier survey course. Noah cross-references frontier topics folded into companion courses (IL-12, IL-16, IL-17, IL-30, IL-31).',
    },
    'il-24-threatlocker-assessment-prep-cbt': {
        'tagline': 'Noah is the learning driver — not a bolt-on.',
        'concept': 'Noah is the core learning driver of IL-24 — a personal assessment-prep coach with five voices and five minds. Mentor runs practice assessments; Engineer drills product scenarios.',
        'bleedingEdge': 'ThreatLocker platform updates move fast — Noah keeps prep aligned to current product realities. Independent preparation; not affiliated with ThreatLocker.',
        'houseRule': 'Attempt the practice scenario first — then bring Noah your approach.',
        'howToUse': ['Open Noah for guided assessment practice.', 'Use Mentor persona for mock assessment runs.', 'Voice chat for verbal scenario walkthroughs.'],
    },
    'il-25-cybersecurity-professional-certificate': {
        'tagline': 'Noah is the learning driver — not a bolt-on.',
        'concept': 'Noah is the core learning driver of IL-25 — a personal cybersecurity certification coach with five voices and five minds. Mentor guides domain study; Engineer runs hands-on labs.',
        'bleedingEdge': 'Threat landscape evolves — Noah surfaces current threat intel via the daily-fold pipeline alongside certification domains.',
        'houseRule': 'Study the domain first — then bring Noah your weak areas for targeted drills.',
        'howToUse': ['Open Noah from any domain module.', 'Ask for targeted drills on weak domains.', 'Use voice chat to explain concepts aloud (Feynman technique).'],
    },
}

VOICE_FIRST = {
    'supported': True,
    'description': 'Talk with Noah via voice chat while working through modules — 5 distinct natural voices served by POST /api/noah/tts (Scholar, Narrator, Guide, Sage, Spark), plus browser speechSynthesis fallback.',
}

for slug, enrich in ENRICH.items():
    path = os.path.join(BASE, slug + '.json')
    d = json.load(open(path))
    nt = d.get('noahTutoring', {})
    # Build modulePersonaMap from existing personas + module IDs
    personas = nt.get('personas', [])
    modules = d.get('modules', [])
    mids = [m.get('id') for m in modules[:8] if m.get('id')]
    pmap = {}
    for i, p in enumerate(personas):
        pname = p if isinstance(p, str) else p.get('id', f'p{i}')
        pmap[pname] = mids[i::len(personas)][:3] if mids else []
    nt['tagline'] = enrich['tagline']
    nt['concept'] = enrich['concept']
    nt['voiceFirst'] = VOICE_FIRST
    nt['bleedingEdge'] = enrich['bleedingEdge']
    nt['houseRule'] = enrich['houseRule']
    nt['howToUse'] = enrich['howToUse']
    nt['modulePersonaMap'] = pmap
    if 'frontierNote' in enrich:
        nt['frontierNote'] = enrich['frontierNote']
    # normalize voices to dict if string
    if isinstance(nt.get('voices'), str):
        nt['voices'] = {'count': 5, 'description': nt['voices']}
    d['noahTutoring'] = nt
    d['updatedAt'] = '2026-10-09'
    with open(path, 'w') as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
        f.write('\n')
    d2 = json.load(open(path))
    keys = sorted(d2['noahTutoring'].keys())
    print(f"{d2['code']}: {len(keys)} keys -> {keys}")

print('\nDone.')
