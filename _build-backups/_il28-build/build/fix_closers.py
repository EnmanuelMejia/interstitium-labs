for f in ['m23.py', 'm24.py']:
    lines = open(f, encoding='utf-8').readlines()
    openers = [i for i, l in enumerate(lines)
               if l.strip().startswith('"body": """')]
    assert len(openers) == 6, (f, len(openers))
    fixed = 0
    for o in openers:
        c = None
        for j in range(o + 1, len(lines)):
            if lines[j].strip() in ('},', '}'):
                c = j
                break
        assert c is not None, (f, o)
        last = c - 1
        body_end = lines[last].rstrip('\n')
        # ground truth via od: ends with plain '"' not '"""'
        assert body_end.endswith('"') and not body_end.endswith('"""'), \
            (f, last + 1, body_end[-20:])
        lines[last] = body_end + '""\n'
        fixed += 1
    open(f, 'w', encoding='utf-8').write(''.join(lines))
    src = ''.join(lines)
    compile(src, f, 'exec')
    print(f, 'fixed', fixed, 'bodies; compiles OK')
