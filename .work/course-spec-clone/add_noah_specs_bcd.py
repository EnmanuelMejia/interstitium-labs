"""Add Noah AI Tutoring Integration sections to specs missing them (IL-07..IL-18)."""
import json, os

BASE = '/home/hatch/workspace/apex-audit/docs/university/data/courses'
SPEC = '/home/hatch/workspace/apex-audit/.work/course-spec-clone/specs'

targets = {
    'IL-07': 'il-07-data-engineering-analytics-ai',
    'IL-08': 'il-08-algorithms-compilers-distributed-formal',
    'IL-09': 'il-09-adaptive-certification-command',
    'IL-10': 'il-10-portfolio-career-professional-practice',
    'IL-11': 'il-11-zero-trust-endpoint-defense',
    'IL-12': 'il-12-ai-engineering',
    'IL-13': 'il-13-software-engineering-interview-prep',
    'IL-14': 'il-14-sre-devops-cloud-security-interview-prep',
    'IL-15': 'il-15-data-engineering-analytics-interview-prep',
    'IL-16': 'il-16-machine-learning-ai-engineering',
    'IL-17': 'il-17-agentic-ai-engineering',
    'IL-18': 'il-18-technical-leadership-interview-prep',
}

def s(v, n=400):
    if v is None: return ''
    t = v if isinstance(v, str) else json.dumps(v)
    return t[:n].replace('\n', ' ')

done = []
for code, slug in targets.items():
    spec_path = os.path.join(SPEC, code + '.md')
    with open(spec_path) as f:
        content = f.read()
    if 'Noah AI Tutoring Integration' in content:
        print(f'{code}: already has Noah section'); continue
    d = json.load(open(os.path.join(BASE, slug + '.json')))
    nt = d.get('noahTutoring', {})
    if not nt:
        print(f'{code}: NO noahTutoring in JSON!'); continue
    personas = nt.get('personas', [])
    if personas and isinstance(personas[0], dict):
        pnames = [p.get('name', p.get('id', '?')) for p in personas]
    else:
        pnames = personas
    section = f"""
## Noah AI Tutoring Integration (strategic differentiator)
- Concept: {s(nt.get('concept'))}
- Personas: {', '.join(pnames)}
- Voices: {s(nt.get('voices'))}
- Adaptive: {s(nt.get('adaptive'))}
- Course-aware: {s(nt.get('courseAware'))}
- Bleeding-edge: {s(nt.get('bleedingEdge'))}
- House rule: {s(nt.get('rule'))}
"""
    with open(spec_path, 'a') as f:
        f.write(section)
    done.append(code)

print(f'\nAdded Noah sections to {len(done)} specs: {done}')
