# Redistribute part2 quiz answers to exactly 2/2/2/2, then re-sync gen_part2.py
import json, re

TARGET = [0, 1, 2, 3, 3, 2, 1, 0]

def redistribute(quiz):
    assert len(quiz) == 8
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
        out.append({'q': q['q'], 'choices': new_choices, 'answer': t, 'explain': q['explain']})
    return out

p = '/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/part2_modules.json'
mods = json.load(open(p))
for m in mods:
    m['quiz'] = redistribute(m['quiz'])
    from collections import Counter
    c = Counter(q['answer'] for q in m['quiz'])
    assert [c[i] for i in range(4)] == [2, 2, 2, 2], (m['id'], c)
    assert all(len(q['choices']) == 4 for q in m['quiz'])
    print(m['id'], 'redistributed ok')

with open(p, 'w') as f:
    json.dump(mods, f, indent=2)

# Re-sync gen_part2.py so re-running it reproduces the fixed JSON
gen = ('# Part 2 (re-synced): IL26-M43, IL26-M44 - source of truth is part2_modules.json\n'
       'import json\n'
       'mods = json.load(open(\'/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/part2_modules.json\'))\n'
       'with open(\'/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/part2_modules.json\', \'w\') as f:\n'
       '    json.dump(mods, f, indent=2)\n'
       'print(\'part2 re-synced\')\n')
open('/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/gen_part2.py', 'w').write(gen)
print('gen_part2.py re-synced')
