"""Retrofit IL-16 modules to the IL-19 Multicloud course template shape.

Per module (except the sibling's RE-Bench module, preserved byte-identical):
  - summary      -> instructor voice ("Welcome to ... I'm your instructor ..."), existing summary kept verbatim
  - objectives   -> prefix-stripped, capitalized (facts preserved)
  - notes        -> 4 sections: Concepts (glossary bullets), Hands-on procedure
                    (numbered steps), Project brief, Honesty note. Module Sources
                    preserved verbatim at the end of Hands-on procedure.
  - cards        -> 6th card added from the module's own teaching note when only 5 exist
  - quiz         -> untouched (already valid: 4 choices, 0-based answer, non-empty explain)

Course level:
  - priorities   -> rebuilt in battlePlan order (adds the 2 missing paths), minutes from battlePlan
  - terminalSims -> [] (template key; renderer handles empty generically; no invented sims)
"""
import json, re, os, copy

STOP = set("""the a an and or of to in on for with as is are be by from that this it you your we our
at vs not into over under out all any can will do does did have has had which what when where how why
who whom whose their there then than so such no nor too very just about after before between during
each other some most more then also its it's than them they""".split())

def words(s):
    return [w for w in re.findall(r"[a-zA-Z0-9']+", s.lower()) if w not in STOP and len(w) > 2]

def overlap(a, b):
    return len(set(words(a)) & set(words(b)))

def first_sentences(s, n=1):
    parts = [p for p in re.split(r'(?<=[.!?])\s+', s.strip()) if p]
    return ' '.join(parts[:n])

def cap1(s):
    s = s.strip()
    return s[:1].upper() + s[1:] if s else s

PATH_GOAL = {
    'ml-in-practice': 'take you from knowing algorithms to shipping honestly-evaluated ML systems',
    'advanced-ml': 'build real judgment with the advanced toolkit \u2014 ensembles, probabilistic models, optimization, and interpretation',
    'python-for-ml': 'make the Python data stack second nature \u2014 NumPy, pandas, visualization, and the scikit-learn API',
    'advanced-genai': 'take you from transformer internals to deployed generative-AI systems with evals',
    'advanced-nlp-practice': 'build language systems end to end \u2014 pipelines, embeddings, retrieval, and LLM-powered NLP',
    'ai-enabled-software': 'teach you to ship software with models inside \u2014 LLM APIs, RAG, tool use, and eval harnesses',
    'applied-ai-production': 'take AI from idea to production value \u2014 framing, data strategy, prototyping, and measurement',
}

OBJ_PREFIXES = ('Understand and apply: ', 'Practice: ', 'Demonstrate end to end: ')

MANUAL_ELAB = {
    ('advanced-ml--model-interpretation-practice',
     'Interpretability for stakeholders, not just debugging'):
        'Lead with the decision-relevant story \u2014 which inputs drive outcomes and where the model '
        'is uncertain \u2014 not with algorithm internals.',
}

# substring-keyed manual definitions, grounded in each module's own cards/quiz content.
# Checked before the automatic matcher in both glossary lines and procedure steps.
MANUAL_DEF = {
    'scaling and its interaction with model families':
        'Scale features to comparable ranges for distance-based models, and verify the effect on your '
        'model family by measuring before and after.',
    'rollback plans and shadow deployments':
        'Shadow the new model on live traffic without serving decisions, and keep the previous artifact '
        'versioned with a one-command revert triggered by a metric threshold.',
    'interpretability for stakeholders, not just debugging':
        'Lead with the decision-relevant story \u2014 which inputs drive outcomes and where the model '
        'is uncertain \u2014 not with algorithm internals.',
    'broadcasting and vectorization':
        'Broadcasting implicitly expands mismatched shapes so operations vectorize \u2014 the mechanism '
        'behind fast array code; never Python loops over elements.',
    'evaluating before and after: did tuning help?':
        'Evaluate before and after on your task set \u2014 tuning can make models worse, and only '
        'measurement tells.',
    'cleaning decisions: what to normalize, what to keep':
        'Every normalization choice (casing, punctuation, stopwords) changes what the model can learn '
        '\u2014 choose deliberately, document always.',
    'pipeline, model, and evaluation design':
        'Classical vs fine-tuned vs LLM on the same eval set \u2014 a tradeoff table of quality, cost, '
        'and latency.',
    'embeddings and vector indexes':
        'Embed chunks into vectors, index them, and retrieve top-k by similarity \u2014 the retrieval '
        'substrate of the RAG pipeline.',
    'error handling when tools fail':
        'Validate arguments, catch errors, return structured failures the model can reason about, and '
        'retry with backoff where safe.',
    'golden dataset and regression suite':
        'Curate a fixed set of representative inputs with expected outputs, and run it on every change '
        '\u2014 the regression suite that catches silent quality drops.',
}

def manual_def(text):
    low = text.lower()
    for sub, definition in MANUAL_DEF.items():
        if sub in low:
            return definition
    return None

def strip_obj(o):
    for p in OBJ_PREFIXES:
        if o.startswith(p):
            o = o[len(p):]
    return cap1(o)

def build_pool(m):
    # (kind, match_text, display_text) -- display_text is what we quote as elaboration
    pool = []
    for c in m['cards']:
        pool.append(('card', c['front'] + ' ' + c['back'], c['back']))
    for q in m['quiz']:
        pool.append(('quiz', q['q'] + ' ' + q['explain'] + ' ' + ' '.join(q['choices']), q['explain']))
    for o in m['objectives']:
        pool.append(('obj', o, None))  # matchable but never quoted
    pool.append(('how', m['notes'][1]['body'], m['notes'][1]['body']))
    pool.append(('sum', m['summary'], first_sentences(m['summary'], 2)))
    return pool

def best_match(text, pool, skip_kinds=(), floor=2):
    # Prefer grounded card/quiz/teaching-note content; the module summary is only a last resort
    for kinds in (('card', 'quiz', 'how'), ('sum',)):
        best, bs = None, 0
        for kind, match_text, display in pool:
            if kind in skip_kinds or kind not in kinds or display is None:
                continue
            sc = overlap(text, match_text)
            if sc > bs:
                best, bs = (match_text, display), sc
        if bs >= floor:
            return best, bs
    return None, 0

def glossary_line(bullet, pool):
    t = bullet.strip()
    md = manual_def(t)
    if md:
        return '- **' + t + '** \u2014 ' + md
    if ': ' in t:
        left, right = t.split(': ', 1)
        return '- **' + left.strip() + '** \u2014 ' + right.strip()
    if ' \u2014 ' in t:
        left, right = t.split(' \u2014 ', 1)
        return '- **' + left.strip() + '** \u2014 ' + right.strip()
    match, _ = best_match(t, pool)
    definition = first_sentences(match[1], 1) if match else None
    if not definition:
        definition = 'a core working practice in this module \u2014 apply it on real data before moving on'
    return '- **' + cap1(t) + '** \u2014 ' + definition

def transform_module(m, path_title, path_detail, path_idx, path_total, course_honesty):
    pool = build_pool(m)
    bullets = [b.strip()[2:].strip() for b in m['notes'][0]['body'].split('\n') if b.strip().startswith('- ')]
    how = m['notes'][1]['body'].strip()
    sources = m['notes'][2]['body'].strip()
    objs = [strip_obj(o) for o in m['objectives']]

    # --- summary: instructor voice, existing summary preserved verbatim
    welcome = ('Welcome to ' + path_title + ' \u2014 ' + path_detail.rstrip('.') + '. '
               "I'm your instructor for this path, and over the next " + str(path_total) +
               ' modules we\'re going to ' + PATH_GOAL[m['id'].split('--')[0]] + '. '
               'This is module ' + str(path_idx) + ' of ' + str(path_total) + ': ' + m['title'] + '.')
    m['summary'] = welcome + '\n\n' + m['summary'].strip()

    # --- objectives: strip filler prefixes
    m['objectives'] = objs

    # --- notes[0]: Concepts
    gloss = [glossary_line(b, pool) for b in bullets]
    concepts = ('The working vocabulary of ' + m['title'] + ' \u2014 learn these cold; '
                'everything else in the module hangs off them.\n' + '\n'.join(gloss))

    # --- notes[1]: Hands-on procedure
    steps = []
    for i, o in enumerate(objs, 1):
        key = (m['id'], o)
        if key in MANUAL_ELAB:
            elab = MANUAL_ELAB[key]
        else:
            elab = manual_def(o)
            if elab is None:
                match, _ = best_match(o, pool, skip_kinds=('obj',))
                elab = first_sentences(match[1], 1) if match else 'Apply this on real data and record what happens.'
        steps.append(str(i) + '. **' + o + '** \u2014 ' + elab)
    steps.append(str(len(objs) + 1) + '. **Close the loop** \u2014 apply every step above to one real dataset, '
                 'and write down what you tried, what moved the result, and what you would do next.')
    hands_on = (how + '\n\nWork the procedure below on a real dataset, in order \u2014 the sequence is the lesson.\n'
                + '\n'.join(steps) + '\n\nModule sources:\n' + sources)

    # --- notes[2]: Project brief
    brief = ('**Project brief \u2014 ' + m['title'] + '.**\n' + how +
             '\n\n**Deliverable.** A working artifact plus a one-page writeup demonstrating: ' +
             '; '.join(objs) + '.' +
             '\n**Done when.** Someone else can rerun your artifact from your writeup, and the writeup states '
             'what you tried, what moved the result, and the limits you did not evaluate.')

    # --- notes[3]: Honesty note
    honesty = (course_honesty +
               '\n\nModule honesty: this module teaches working practice \u2014 the checks, the procedures, '
               'the failure modes \u2014 not credentials. Tooling moves fast: treat named tools and libraries '
               'as as-of 2026-10-07 and verify against the module\u2019s Sources before quoting them.')

    m['notes'] = [
        {'title': 'Concepts', 'body': concepts},
        {'title': 'Hands-on procedure', 'body': hands_on},
        {'title': 'Project brief', 'body': brief},
        {'title': 'Honesty note', 'body': honesty},
    ]

    # --- cards: 6th card from the module's own teaching note
    if len(m['cards']) == 5:
        m['cards'].append({
            'front': 'In one sentence, what does ' + m['title'] + ' teach you to do?',
            'back': how,
        })
    return m

def main():
    path = os.path.expanduser('~/workspace/apex-audit/docs/university/data/courses/il-16-machine-learning-ai-engineering.json')
    with open(path, encoding='utf-8') as f:
        d = json.load(f)  # FRESH load immediately before editing

    battle = {b['id']: b for b in d['battlePlan']}
    path_ids = [b['id'] for b in d['battlePlan']]
    counts = {}
    for m in d['modules']:
        counts[m['id'].split('--')[0]] = counts.get(m['id'].split('--')[0], 0) + 1
    seen = {}
    retrofitted, skipped, cards_added = 0, 0, 0
    for m in d['modules']:
        if 're-bench' in m['id']:
            skipped += 1  # sibling's module: preserve byte-identical
            continue
        prefix = m['id'].split('--')[0]
        seen[prefix] = seen.get(prefix, 0) + 1
        before_cards = len(m['cards'])
        transform_module(m, battle[prefix]['title'], battle[prefix]['detail'],
                         seen[prefix], counts[prefix], d['honestyNote'])
        cards_added += len(m['cards']) - before_cards
        retrofitted += 1

    # --- course level: priorities rebuilt in battlePlan order with battlePlan minutes
    d['priorities'] = [{'label': battle[pid]['title'], 'minutes': battle[pid]['minutes']} for pid in path_ids]

    # --- course level: terminalSims key (empty; renderer consumes generically, no invented sims)
    if 'terminalSims' not in d:
        keys = list(d.keys())
        nd = {}
        for k in keys:
            nd[k] = d[k]
            if k == 'trainers':
                nd['terminalSims'] = []
        d = nd

    tmp = path + '.retrofit_tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')
    with open(tmp, encoding='utf-8') as f:
        json.load(f)  # validate before replacing
    os.replace(tmp, path)

    with open(path, encoding='utf-8') as f:
        d2 = json.load(f)  # validate after writing
    assert len(d2['modules']) == 43, len(d2['modules'])
    assert sum(p['minutes'] for p in d2['priorities']) == d2['hours'] * 60
    print('OK: modules retrofitted:', retrofitted, '| sibling modules preserved:', skipped,
          '| 6th cards added:', cards_added)
    print('priorities minutes total:', sum(p['minutes'] for p in d2['priorities']))

if __name__ == '__main__':
    main()
