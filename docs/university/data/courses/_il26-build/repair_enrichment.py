import io, json

p1 = '/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/m41_51_enrichment.json'
p2 = '/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/m49_51_enrichment.json'
s = io.open(p1, encoding='utf-8').read()

# Seam A: chunk1 -> chunk2 boundary (missing opening brace for M45 entry)
old_a = '"type":"choice"}}]},\"crossLinks\":[\"IL26-M09\"'
new_a = '"type":"choice"}},{\"crossLinks\":[\"IL26-M09\"'
assert s.count(old_a) == 1, 'seam A count %d' % s.count(old_a)
s = s.replace(old_a, new_a)

# Seam C: intra-chunk entry boundaries M45->M46, M46->M47, M47->M48
# (verified already correct: '}},{\"crossLinks\":' present)
pat = '"type":"choice"}},{\"crossLinks\":'
n = s.count(pat)
assert n == 7, 'intra boundaries %d (expected 7)' % n
print('intra boundaries OK:', n)

e1 = json.loads(s)
print('part1 valid:', len(e1['enrichments']))

e2 = json.loads(io.open(p2, encoding='utf-8').read())
print('part2 valid:', len(e2['enrichments']))

all_ids = [x['id'] for x in e1['enrichments']] + [x['id'] for x in e2['enrichments']]
assert all_ids == ['IL26-M%d' % i for i in range(41, 52)], all_ids
assert len(set(all_ids)) == 11

merged = {'enrichments': e1['enrichments'] + e2['enrichments']}
for x in merged['enrichments']:
    assert set(['crossLinks', 'drills', 'handsOnLab', 'id', 'mockTask']) <= set(x.keys()), x.get('id')
    assert len(x['drills'][0]['items']) >= 6, x['id']

with io.open(p1, 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False)
json.loads(io.open(p1, encoding='utf-8').read())
print('MERGED: 11 enrichments, valid JSON')
