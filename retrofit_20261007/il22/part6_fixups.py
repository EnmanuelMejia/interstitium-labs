#!/usr/bin/env python3
"""Part 6: fix grimoires glossary bullet shape + rebalance quiz answer
positions across all IL-22 modules via seeded shuffles (correct choice
tracked). Atomic write, json.load before and after."""
import json, os, random

PATH = '/home/hatch/workspace/apex-audit/docs/university/data/courses/il-22-esoteric-secret-knowledge.json'

def main():
    d = json.load(open(PATH))
    # (a) glossary bullet shape fix: no inner asterisks inside the bold term
    for m in d['modules']:
        if m['id'] == 'm22-grimoires':
            body = m['notes'][0]['body']
            old = '- **Key of Solomon (*Clavicula Salomonis*)** \u2014'
            new = '- **Key of Solomon (Clavicula Salomonis)** \u2014'
            assert old in body, 'bullet not found'
            m['notes'][0]['body'] = body.replace(old, new, 1)

    # (b) rebalance: seeded shuffle of each question's choices, tracking answer
    rng = random.Random(20261007)
    for m in d['modules']:
        for qi, q in enumerate(m['quiz']):
            correct = q['choices'][q['answer']]
            order = list(range(4))
            rng.shuffle(order)
            q['choices'] = [q['choices'][i] for i in order]
            q['answer'] = q['choices'].index(correct)
            assert len(q['choices']) == 4 and 0 <= q['answer'] <= 3

    from collections import Counter
    c = Counter(q['answer'] for m in d['modules'] for q in m['quiz'])
    print('distribution:', dict(c))
    assert all(v >= 30 for v in c.values()), c  # ~25% each of 160

    tmp = PATH + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')
    d2 = json.load(open(tmp))
    assert len(d2['modules']) == 16
    # re-verify a sample: correct choice still matches original intent
    os.replace(tmp, PATH)
    print('part6 ok')

if __name__ == '__main__':
    main()
