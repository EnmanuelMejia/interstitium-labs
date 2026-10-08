# Part 2 (re-synced): IL26-M43, IL26-M44 - source of truth is part2_modules.json
import json
mods = json.load(open('/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/part2_modules.json'))
with open('/home/hatch/workspace/apex-audit/docs/university/data/courses/_il26-build/part2_modules.json', 'w') as f:
    json.dump(mods, f, indent=2)
print('part2 re-synced')
