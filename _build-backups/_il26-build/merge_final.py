"""IL-26 final merge: expand course JSON with all fragments.
Preserves ALL existing content (flesh = REPLACE for notes/cards/quiz/objectives,
ADD for drills/handsOnLab/mockTask/crossLinks). Atomic write + validation.
"""
import io, json, os, shutil

BASE = '/home/hatch/workspace/apex-audit/docs/university/data/courses'
BD = BASE + '/_il26-build'
COURSE = BASE + '/il-26-data-analyst-certification-senior-mastery.json'

def load(p):
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)

course = load(COURSE)
flesh = load(BD + '/module-flesh.json')
tool_labs = load(BD + '/tool-labs.json')
videos = load(BD + '/videos.json')
install_labs = load(BD + '/install-labs.json')
crosswalk_v2 = load(BD + '/crosswalk-v2.json')
interactive = load(BD + '/interactive.json')
enrich = load(BD + '/m41_51_enrichment.json')

stats = {}

# ---------- 1. Flesh patches (REPLACE thin arrays, ADD new keys) ----------
by_id = {m['id']: m for m in course['modules']}
assert len(by_id) == 40, 'expected 40 modules, got %d' % len(by_id)
replaced = 0
for f in flesh['modules']:
    mid = f['id']
    assert mid in by_id, 'flesh patch for unknown module %s' % mid
    m, p = by_id[mid], f['patch']
    for k in ('notes', 'cards', 'quiz', 'objectives'):
        if k in p:
            m[k] = p[k]
    for k in ('drills', 'handsOnLab', 'mockTask', 'crossLinks'):
        if k in p:
            m[k] = p[k]
    replaced += 1
stats['flesh_patched'] = replaced

# ---------- 2. Videos -> module.videos[] (watchBefore ordering kept) ----------
vid_map = {}
for v in videos['videos']:
    items = sorted(v['items'], key=lambda i: i.get('order', 0))
    vid_map[v['moduleId']] = items
vid_attached = 0
for m in course['modules']:
    m['videos'] = vid_map.get(m['id'], [])
    if m['videos']:
        vid_attached += 1
stats['videos_modules'] = vid_attached
stats['videos_items'] = sum(len(v) for v in vid_map.values())

# ---------- 3. Tool-lab modules M41-M51 (normalize TL refs) ----------
tl_ids = set(t['id'] for t in tool_labs['toolLabs'])
existing_ids = set(by_id.keys())
normed = 0
for m in tool_labs['modules']:
    assert m['id'] not in existing_ids, 'dup module id ' + m['id']
    lab_refs = [t for t in m.get('prerequisiteFor', []) if t in tl_ids]
    mod_refs = [t for t in m.get('prerequisiteFor', []) if t not in tl_ids]
    for t in mod_refs:
        assert t in existing_ids or t in set(x['id'] for x in tool_labs['modules']), \
            'unresolved prerequisiteFor %s in %s' % (t, m['id'])
    for t in lab_refs:
        normed += 1
    m['prerequisiteFor'] = mod_refs
    if lab_refs:
        m['prerequisiteForLabs'] = lab_refs
    m['videos'] = []
    course['modules'].append(m)
stats['modules_appended'] = len(tool_labs['modules'])
stats['tl_refs_normalized'] = normed
by_id = {m['id']: m for m in course['modules']}
assert len(by_id) == 51, 'expected 51 modules'

# ---------- 4. M41-M51 enrichment (original drills/labs/mock tasks) ----------
en_applied = 0
for e in enrich['enrichments']:
    m = by_id[e['id']]
    m['drills'] = e['drills']
    m['handsOnLab'] = e['handsOnLab']
    m['mockTask'] = e['mockTask']
    m['crossLinks'] = e['crossLinks']
    en_applied += 1
stats['enrichments_applied'] = en_applied

# ---------- 5. Top-level arrays ----------
course['toolLabs'] = tool_labs['toolLabs']
course['multicloudLabs'] = tool_labs['multicloudLabs']
course['sampleDatasets'] = tool_labs['datasets']
course['installSteps'] = tool_labs['installSteps']
course['installLabs'] = install_labs['installLabs']
course['installPrereqOrder'] = install_labs['prereqOrder']
course['employerMappings'] = crosswalk_v2['employerMappings']
course['jdMatrix'] = crosswalk_v2['jdMatrix']
framing = crosswalk_v2.get('framing', {})
if 'employerCompetencies' in framing:
    course['employerCompetencies'] = framing['employerCompetencies']
course['sqlPlaygrounds'] = interactive['sqlPlaygrounds']
course['pythonExercises'] = interactive['pythonExercises']
course['daxPlaygrounds'] = interactive['daxPlaygrounds']
# terminalSims: keep existing canned-shell sims, append graded sims
existing_term_ids = set(t['id'] for t in course['terminalSims'])
for t in interactive['terminalSims']:
    assert t['id'] not in existing_term_ids, 'dup terminalSim ' + t['id']
    existing_term_ids.add(t['id'])
course['terminalSims'] = course['terminalSims'] + interactive['terminalSims']
course['branchingScenarios'] = interactive['branchingScenarios']
course['clickSims'] = interactive['clickSims']

stats['top_level_added'] = {
    'toolLabs': len(course['toolLabs']),
    'multicloudLabs': len(course['multicloudLabs']),
    'sampleDatasets': len(course['sampleDatasets']),
    'installSteps': len(course['installSteps']),
    'installLabs': len(course['installLabs']),
    'installPrereqOrder': len(course['installPrereqOrder']),
    'employerMappings': len(course['employerMappings']),
    'jdMatrix': len(course['jdMatrix']),
    'sqlPlaygrounds': len(course['sqlPlaygrounds']),
    'pythonExercises': len(course['pythonExercises']),
    'daxPlaygrounds': len(course['daxPlaygrounds']),
    'terminalSims': len(course['terminalSims']),
    'branchingScenarios': len(course['branchingScenarios']),
    'clickSims': len(course['clickSims']),
}

# interactive element index: moduleId -> element list
inter_idx = {}
def add_inter(mid, eid, etype):
    inter_idx.setdefault(mid, []).append({'id': eid, 'type': etype})

for pg in course['sqlPlaygrounds']:
    if pg.get('moduleId'): add_inter(pg['moduleId'], pg['id'], 'sqlPlayground')
for ex in course['pythonExercises']:
    if ex.get('moduleId'): add_inter(ex['moduleId'], ex['id'], 'pythonExercise')
for dg in course['daxPlaygrounds']:
    if dg.get('moduleId'): add_inter(dg['moduleId'], dg['id'], 'daxPlayground')
for ts in interactive['terminalSims']:
    if ts.get('moduleId'): add_inter(ts['moduleId'], ts['id'], 'terminalSim')
for bs in course['branchingScenarios']:
    if bs.get('moduleId'): add_inter(bs['moduleId'], bs['id'], 'branchingScenario')
for cs in course['clickSims']:
    if cs.get('moduleId'): add_inter(cs['moduleId'], cs['id'], 'clickSim')
tool_by_mod, inst_by_mod = {}, {}
for t in course['toolLabs']:
    if t.get('moduleId'):
        tool_by_mod.setdefault(t['moduleId'], []).append(t)
        add_inter(t['moduleId'], t['id'], 'toolLab')
for il in course['installLabs']:
    if il.get('moduleId'):
        inst_by_mod.setdefault(il['moduleId'], []).append(il)
        add_inter(il['moduleId'], il['id'], 'installLab')

# ---------- 6. Interactivity audit: keep 40, add M41-M51 ----------
audit = list(interactive['interactivityAudit'])
audited = set(a['moduleId'] for a in audit)
for m in course['modules']:
    mid = m['id']
    if mid in audited:
        continue
    elems = list(inter_idx.get(mid, []))
    if m.get('drills'):
        for d in m['drills']:
            elems.append({'id': d['id'], 'type': 'drill'})
    if m.get('handsOnLab'):
        elems.append({'id': m['handsOnLab']['id'], 'type': 'handsOnLab'})
    if m.get('mockTask'):
        elems.append({'id': m['mockTask']['id'], 'type': 'mockTask'})
    if m.get('videos'):
        elems.append({'id': 'videos:' + mid, 'type': 'videos'})
    # de-dupe by id
    seen, uniq = set(), []
    for e in elems:
        if e['id'] not in seen:
            seen.add(e['id']); uniq.append(e)
    audit.append({'moduleId': mid, 'elementCount': len(uniq),
                  'elements': uniq, 'gatePass': len(uniq) >= 2})
course['interactivityAudit'] = audit
stats['audit_entries'] = len(audit)
stats['audit_failures'] = [a['moduleId'] for a in audit if not a['gatePass']]

# ---------- 7. Honest time estimates per module ----------
# Formula (documented in studyGuide): reading base per weight + per-item work
# + lab time + referenced tool/install lab time + targeted video time
# (videos are full-length reference courses; count 50% of runtime, cap 180 min).
for m in course['modules']:
    mins = m.get('weight', 1) * 120
    mins += len(m.get('notes', [])) * 12
    mins += len(m.get('cards', [])) * 4
    mins += len(m.get('quiz', [])) * 8
    vid = sum((v.get('durationMin') or 0) for v in m.get('videos', []))
    mins += min(vid * 0.5, 180)
    mins += sum(len(d.get('items', [])) * 4 for d in m.get('drills', []))
    if m.get('handsOnLab'):
        mins += 90
    mins += len(tool_by_mod.get(m['id'], [])) * 150
    mins += sum(il.get('estimatedMinutes', 0) for il in inst_by_mod.get(m['id'], []))
    m['estimatedMinutes'] = int(mins)

total_min = sum(m['estimatedMinutes'] for m in course['modules'])
total_hours = round(total_min / 60)
course['hours'] = total_hours
stats['total_minutes'] = total_min
stats['total_hours'] = total_hours

# ---------- 8. Study guide (rendered as course's first section by shell) ----------
gate_order = [
    ('gate-google', 'Google Data Analytics Professional Certificate',
     'Broadest foundation coverage; its domain map overlaps every later exam. Sit first to bank a win and validate the workflow.'),
    ('gate-dataplus', 'CompTIA Data+ (DA0-002)',
     'Vendor-neutral data lifecycle and governance; builds directly on the Google prep with deeper data-quality and visualization depth.'),
    ('gate-ibm', 'IBM Data Analyst Professional Certificate',
     'SQL/Python/spreadsheet core with dashboard emphasis; the heaviest SQL stretch before the vendor exams.'),
    ('gate-tableau', 'Tableau Certified Data Analyst',
     'Visualization-specialist exam; sit after the analysis fundamentals are solid so you can focus on Tableau idioms.'),
    ('gate-pl300', 'Microsoft PL-300: Power BI Data Analyst',
     'DAX and Power BI modeling depth; needs the modeling modules (M08, M13) fresh — schedule right after Tableau.'),
    ('gate-databricks', 'Databricks Certified Data Analyst Associate',
     'Lakehouse SQL and Delta concepts; pairs with the M43 Iceberg/table-format module while it is fresh.'),
    ('gate-aws', 'AWS Data Analytics (Data Engineer Associate topic map)',
     'Widest cloud-services surface; sit last when the pipeline and architecture modules (M12-M14) are strongest.'),
]
th = ((course.get('readinessDashboard') or {}).get('thresholds') or {})
ready_t, near_t = th.get('ready', 85), th.get('nearlyReady', 70)
weeks_90 = round(total_hours / 7.5, 1)  # 90 min/day x 5 days/week

course['studyGuide'] = {
    'title': 'Study guide: how to work this course',
    'totalHours': total_hours,
    'totalMinutes': total_min,
    'pacing': {
        'dailyMinutes': 90, 'daysPerWeek': 5,
        'estimatedWeeks': weeks_90,
        'plan': [
            'Phase 1 — Foundations reset, M26-M34 (~83 h, ~11 weeks): one math module per day; drill until the audit drill is green before moving on.',
            'Phase 2 — Tool core, M08-M18 + M25 (~112 h, ~15 weeks): install each tool via its install lab before the tool lab; keep the SQL playground open beside the notes.',
            'Phase 3 — Platform & craft, M01-M07 (~50 h, ~7 weeks): certification-domain modules plus exam framing.',
            'Phase 4 — Tools, M41-M51 (~79 h, ~11 weeks): DuckDB, Polars, dbt, Iceberg, semantic layer, dashboards, storytelling.',
            'Phase 5 — Senior tracks, M35-M40 (~39 h, ~5 weeks): Palantir-bar and BNY Mellon interview prep; timed mock tasks daily.',
            'Phase 6 — Career & portfolio, M19-M24 (~42 h, ~6 weeks): portfolio builds, interview loops, 90-day readiness plan.',
            'Phase 7 — Certification gates: sit practice gates in the order below; book each real exam only when the dashboard reads READY.',
        ],
        'note': '90 minutes a day, 5 days a week, completes the course in about %s weeks. Slower is fine — the dashboard measures readiness, not speed.' % weeks_90,
    },
    'whenStuck': {
        'title': 'When you are stuck (exact remediation path)',
        'steps': [
            '1. Re-check: re-read the note that introduced the concept and re-run its worked example by hand. Most blocks are a skipped prerequisite.',
            '2. Drills: work the module drill set until every item is correct twice in a row. If a drill item confuses you, that is the exact gap — name it.',
            '3. Videos: watch the module video marked watchBefore=drill/lab. Pause and replicate each step in your own environment.',
            '4. Cross-linked catalog modules: follow the module crossLinks — the concept is rebuilt from a different angle there (e.g. window functions in M09 and again in M41).',
            '5. Ask Noah: the in-course tutor answers from this course material only. Bring your hypothesis, not just the error.',
        ],
    },
    'examOrder': {
        'title': 'Recommended certification exam order',
        'thresholds': {'ready': ready_t, 'nearlyReady': near_t},
        'rule': 'Sit a practice gate only when that exam dashboard row is at least NEARLY READY (%d%%). Book the real exam only when it reads READY (%d%%) on the 60%%-modules / 40%%-gate formula.' % (near_t, ready_t),
        'order': [{'gateId': g, 'cert': c_, 'why': w} for (g, c_, w) in gate_order],
    },
    'timeFormula': ('estimatedMinutes per module = weight x 120 + notes x 12 + cards x 4 + quiz x 8 '
                    '+ drill items x 4 + handsOnLab 90 + tool labs x 150 + install-lab minutes '
                    '+ targeted video time (50%% of runtime, capped at 180 min/module). '
                    'Course total = sum of module estimates = %d minutes (~%d hours).' % (total_min, total_hours)),
}

# ---------- 9. Dossier link, metadata, honesty note ----------
course['dossierUrl'] = 'il-26-dossier.html'
course['updatedAt'] = '2026-10-07'
course['schemaVersion'] = 4
course['honestyNote'] = (
    (course.get('honestyNote') or '').rstrip()
    + ' Expanded 2026-10-07: 11 tool modules (M41-M51), install labs, tool labs, '
    + 'multicloud labs, sample datasets, 25 curated video modules (third-party videos are linked, not hosted; '
    + 'verify availability), SQL/Python/DAX playgrounds, terminal sims, branching scenarios, click-through sims, '
    + 'employer crosswalk mappings, and the graduate evidence dossier (il-26-dossier.html + .pdf). '
    + 'All prose, drills, labs, and scenarios are original Interstitium Labs content. '
    + 'Independent certification prep: no affiliation with, endorsement by, or certification from Google, Microsoft, '
    + 'Tableau, CompTIA, IBM, AWS, Databricks, Palantir, or BNY Mellon; practice gates confer no credential.'
)

# ---------- 10. Final structural validation ----------
assert len(course['modules']) == 51
ids = [m['id'] for m in course['modules']]
assert len(set(ids)) == 51, 'duplicate module ids'
by = {m['id']: m for m in course['modules']}
for m in course['modules']:
    for t in m.get('prerequisiteFor', []):
        assert t in by, 'unresolved prerequisiteFor %s in %s' % (t, m['id'])
    for t in m.get('prerequisiteForLabs', []):
        assert t in tl_ids, 'unresolved prerequisiteForLabs %s in %s' % (t, m['id'])
    for t in m.get('crossLinks', []):
        if isinstance(t, dict):
            assert t.get('course') and t.get('moduleId'), 'bad cross-catalog link in %s' % m['id']
        else:
            assert t in by or t in tl_ids, 'unresolved crossLink %s in %s' % (t, m['id'])
for v in videos['videos']:
    assert v['moduleId'] in by, 'video for unknown module ' + v['moduleId']

# ---------- 11. Atomic write ----------
tmp = COURSE + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as f:
    json.dump(course, f, ensure_ascii=False, indent=2)
with io.open(tmp, encoding='utf-8') as f:
    reloaded = json.load(f)
assert len(reloaded['modules']) == 51
os.replace(tmp, COURSE)
print('MERGE COMPLETE')
for k, v in stats.items():
    print(' - %s: %s' % (k, v))
