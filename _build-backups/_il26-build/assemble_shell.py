import io

shell = '/home/hatch/workspace/apex-audit/docs/university/course-shell.js'
parts = ['il26-shell-a.js', 'il26-shell-b.js', 'il26-shell-c.js', 'il26-shell-d.js', 'il26-shell-e.js']
U = '/home/hatch/workspace/apex-audit/docs/university/'

block = '\n'.join(io.open(U + p, encoding='utf-8').read() for p in parts)
lines = io.open(shell, encoding='utf-8').read().split('\n')

anchor = None
for i, ln in enumerate(lines):
    if ln.strip() == 'var BUILDERS = {':
        anchor = i
        break
assert anchor is not None, 'BUILDERS anchor not found'

new_lines = lines[:anchor] + [''] + block.split('\n') + [''] + lines[anchor:]
with io.open(shell, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))
print('inserted at line', anchor + 1, '| new total lines:', len(new_lines))
