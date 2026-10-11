# Reusable: redistribute every module quiz in a part JSON to exactly 2/2/2/2
import json, sys
from collections import Counter

TARGET = [0, 1, 2, 3, 3, 2, 1, 0]

def redistribute(quiz):
    assert len(quiz) == 8, f'expected 8 questions, got {len(quiz)}'
    out = []
    for q, t in zip(quiz, TARGET):
        correct_text = q['choices'][q['answer']]
        others = [c for i, c in enumerate(q['choices']) if i != q['answer']]
        new_choices, oi = [], 0
        for i in range(4):
            if i == t:
                new_choices.append(correct_text)
            else:
                new_choices.append(others[oi]); oi += 1
        assert new_choices[t] == correct_text
        assert sorted(new_choices) == sorted(q['choices'])
        assert len(new_choices) == 4
        out.append({'q': q['q'], 'choices': new_choices, 'answer': t, 'explain': q['explain']})
    return out

def fix_file(path):
    mods = json.load(open(path))
    for m in mods:
        m['quiz'] = redistribute(m['quiz'])
        c = Counter(q['answer'] for q in m['quiz'])
        assert [c[i] for i in range(4)] == [2, 2, 2, 2], (m['id'], dict(c))
        print(m['id'], 'dist ok', '| cards', len(m['cards']), '| notes', len(m['notes']), '| obj', len(m['objectives']))
    with open(path, 'w') as f:
        json.dump(mods, f, indent=2)
    print('wrote', path)

if __name__ == '__main__':
    fix_file(sys.argv[1])
