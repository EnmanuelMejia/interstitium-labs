"""STEP 2: 'worth paying for' audit — 5 criteria per module (51 modules)."""
import io, json, re

BASE = '/home/hatch/workspace/apex-audit/docs/university/data/courses'
c = json.load(io.open(BASE + '/il-26-data-analyst-certification-senior-mastery.json', encoding='utf-8'))

PLACEHOLDERS = re.compile(r'todo|coming soon|lorem|placeholder text|\[insert|tbd\]', re.I)
audit_idx = {a['moduleId']: a for a in c.get('interactivityAudit', [])}
tool_mods = set(t.get('moduleId') for t in c.get('toolLabs', []))
inst_mods = set(t.get('moduleId') for t in c.get('installLabs', []))

results = []
for m in c['modules']:
    mid, fails = m['id'], []
    # 1. objective stated plainly
    objs = m.get('objectives', [])
    if not objs or any(len(str(o)) < 20 for o in objs):
        fails.append('C1: objectives missing/short')
    # 2. teaches from zero
    notes = m.get('notes', [])
    nchars = sum(len(n.get('body', '')) for n in notes)
    blob = json.dumps(m)
    if len(notes) < 3 or nchars < 1500 or len(m.get('cards', [])) < 4:
        fails.append('C2: thin content (notes=%d chars=%d cards=%d)' % (len(notes), nchars, len(m.get('cards', []))))
    if PLACEHOLDERS.search(blob):
        fails.append('C2: placeholder text found')
    # 3. interactive element proving mastery
    a = audit_idx.get(mid)
    if not a or a.get('elementCount', 0) < 2:
        fails.append('C3: interactive elements < 2')
    # 4. lab applying it
    if not m.get('handsOnLab') and mid not in tool_mods and mid not in inst_mods:
        fails.append('C4: no lab')
    # 5. honest time estimate
    em = m.get('estimatedMinutes', 0)
    if not em or em < 30 or em > 2400:
        fails.append('C5: bad time estimate (%s)' % em)
    results.append((mid, m['title'], fails))

npass = sum(1 for _, _, f in results if not f)
print('PASS %d / 51' % npass)
for mid, title, fails in results:
    if fails:
        print('FAIL', mid, title[:50])
        for f in fails:
            print('     -', f)
