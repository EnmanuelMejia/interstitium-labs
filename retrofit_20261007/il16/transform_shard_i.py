"""Add path-level topics / sources / il_provides to shard-i.json.

- topics: deduped string list drawn from the path's own phases[].topics
- sources: deduped {name, url, note} drawn from the path's own modules' sources
  (URLs already in the repo; nothing new, nothing unverified)
- il_provides: 2-3 sentence instructor-voice blurb grounded in the path's
  subtitle, suited_for, and phase outcomes. Everything else preserved.
"""
import json, os

IL_PROVIDES = {
    'ml-in-practice':
        "Welcome to the path where the applied loop becomes habit. I'm your instructor, and over these six "
        "modules you'll run the sequence working engineers actually use \u2014 frame the problem, build the "
        "baseline, engineer features without leaking the future, evaluate honestly, pipeline it, and ship it "
        "behind an API. You'll finish with a deployed capstone and a writeup a hiring manager can evaluate.",
    'advanced-ml':
        "Welcome to the advanced toolkit. I'm your instructor, and here we go beyond the basics: ensembles "
        "and probabilistic models, optimization discipline, deep architectures, and interpretation you can "
        "defend to stakeholders \u2014 plus a read of RE-Bench so you can judge \u2018AI does research\u2019 "
        "claims like an evaluator. You'll finish with a hard project and a writeup a practitioner would respect.",
    'python-for-ml':
        "Welcome to the Python subset ML actually uses. I'm your instructor, and over six modules you'll make "
        "NumPy, pandas, visualization, and the scikit-learn API second nature \u2014 on real, messy data, not "
        "toy arrays. You'll finish with a complete project: dataset, baseline, honest evaluation, and a writeup "
        "of what you learned.",
    'advanced-genai':
        "Welcome to generative AI, built from the inside out. I'm your instructor: we start with the "
        "transformer as an implementable operation, move through pretraining, fine-tuning, and alignment, then "
        "face the production questions \u2014 evals, inference serving, and cost. You'll finish with a scoped "
        "GenAI system, an eval suite measuring what matters, and a demo with stated limits.",
    'advanced-nlp-practice':
        "Welcome to language systems, built and evaluated. I'm your instructor, and we'll work the full NLP "
        "stack in practice: pipelines and tokenization, embeddings and similarity search, sequence models where "
        "they still win, LLM-powered NLP, and retrieval. You'll finish with a real text problem, a full "
        "pipeline, and an error analysis on linguistic failures.",
    'ai-enabled-software':
        "Welcome to shipping software with models inside. I'm your instructor: LLM APIs, RAG that actually "
        "retrieves, eval harnesses that catch regressions, tool use with least privilege \u2014 the engineering "
        "discipline that keeps AI features reliable and affordable. You'll finish with a scoped feature, a golden "
        "dataset, guardrails, and a launch writeup with the failure catalog.",
    'applied-ai-production':
        "Welcome to the production judgment layer. I'm your instructor, and this path is about the decisions "
        "around the model: framing the problem honestly, data strategy on a real budget, prototyping with "
        "stakeholders, communicating without jargon, and measuring value. You'll finish with a production-shaped "
        "plan and handoff documentation for a real problem with real constraints.",
}

def main():
    path = os.path.expanduser('~/workspace/apex-audit/docs/university/data/catalog/shard-i.json')
    with open(path, encoding='utf-8') as f:
        d = json.load(f)  # FRESH load immediately before editing

    for p in d['paths']:
        pid = p['id']
        # topics: from the path's own phases
        topics = []
        for ph in p.get('phases', []):
            for t in ph.get('topics', []):
                if t not in topics:
                    topics.append(t)
        p['topics'] = topics
        # sources: dedupe the path's own modules' sources by URL
        seen, sources = set(), []
        for mod in p.get('modules', []):
            for s in mod.get('sources', []):
                u = s.get('url')
                if u and u not in seen:
                    seen.add(u)
                    sources.append({'name': s.get('name'), 'url': u, 'note': s.get('note')})
        p['sources'] = sources
        # il_provides: instructor-voice blurb
        p['il_provides'] = IL_PROVIDES[pid]

    tmp = path + '.retrofit_tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')
    with open(tmp, encoding='utf-8') as f:
        json.load(f)
    os.replace(tmp, path)

    with open(path, encoding='utf-8') as f:
        d2 = json.load(f)
    for p in d2['paths']:
        assert isinstance(p['topics'], list) and p['topics'], p['id']
        assert isinstance(p['sources'], list) and p['sources'], p['id']
        assert isinstance(p['il_provides'], str) and len(p['il_provides']) > 100, p['id']
        for s in p['sources']:
            assert set(s.keys()) == {'name', 'url', 'note'}, s
    print('OK: shard-i paths retrofitted:', len(d2['paths']))
    for p in d2['paths']:
        print(' ', p['id'], '| topics:', len(p['topics']), '| sources:', len(p['sources']))

if __name__ == '__main__':
    main()
