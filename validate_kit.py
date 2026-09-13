import re, glob, os, sys, collections

SEP = chr(92)
fails = []
checks = 0


def chk(cond, label, detail=''):
    global checks
    checks += 1
    print(('PASS  ' if cond else 'FAIL  ') + label + (f'  -> {detail}' if (detail and not cond) else ''))
    if not cond:
        fails.append(label)


def slash(p):
    return p.replace(SEP, '/')


def fm(path):
    s = open(path, encoding='utf-8').read()
    if not s.startswith('---'):
        return None, s
    end = s.index(chr(10) + '---', 3)
    d = {}
    for ln in s[3:end].strip().split(chr(10)):
        if ':' in ln:
            k, v = ln.split(':', 1)
            d[k.strip()] = v.strip()
    return d, s


files = sorted(slash(f) for f in glob.glob('**/*.md', recursive=True))

print('=== 1. AGENT FRONTMATTER — docs-valid values only ===')
MODELS = {'sonnet', 'opus', 'haiku', 'fable', 'inherit'}
EFFORT = {'low', 'medium', 'high', 'xhigh', 'max'}
COLORS = {'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'cyan'}
AGENTKEYS = {'name', 'description', 'tools', 'disallowedTools', 'model', 'permissionMode',
             'maxTurns', 'skills', 'mcpServers', 'hooks', 'memory', 'background', 'effort',
             'isolation', 'color', 'initialPrompt', 'experimental'}
for p in sorted(glob.glob('core/agents/*.md')):
    d, _ = fm(p)
    n = os.path.basename(p)
    chk(d is not None, f'{n}: has frontmatter')
    chk('name' in d and 'description' in d, f'{n}: required name+description')
    chk(d.get('name') == n[:-3], f'{n}: name matches filename', d.get('name'))
    chk(d.get('model') in MODELS, f'{n}: model is a valid alias', d.get('model'))
    chk(d.get('model') != 'fable', f'{n}: model is NOT fable')
    chk(d.get('effort') in EFFORT, f'{n}: effort is valid', d.get('effort'))
    chk(d.get('color') in COLORS, f'{n}: color is documented', d.get('color'))
    chk(set(d) <= AGENTKEYS, f'{n}: no unknown keys', str(set(d) - AGENTKEYS))

print()
print('=== 2. TOOL RESTRICTIONS ARE REAL ===')
for name, must_lack, must_have in [
        ('refuter', ['Edit', 'Write', 'NotebookEdit'], ['Read', 'Bash']),
        ('scout', ['Edit', 'Write', 'Bash'], ['Read', 'Grep']),
        ('researcher', ['Edit', 'Write'], ['Read']),
        ('debugger', ['Edit', 'Write'], ['Read', 'Bash']),
        ('builder', [], ['Edit', 'Write', 'Bash'])]:
    d, _ = fm(f'core/agents/{name}.md')
    t = [x.strip() for x in d['tools'].split(',')]
    chk(all(m not in t for m in must_lack), f'{name}: lacks {must_lack}', str(t))
    chk(all(m in t for m in must_have), f'{name}: has {must_have}', str(t))

print()
print('=== 3. COMMAND FRONTMATTER ===')
CMDKEYS = {'description', 'when_to_use', 'argument-hint', 'arguments', 'disable-model-invocation',
           'user-invocable', 'allowed-tools', 'disallowed-tools', 'model', 'effort', 'context',
           'agent', 'background', 'hooks', 'shell', 'metadata', 'license', 'compatibility'}
for p in sorted(glob.glob('core/commands/*.md')):
    d, s = fm(p)
    n = os.path.basename(p)
    chk(d is not None and 'description' in d, f'{n}: has description')
    chk(set(d) <= CMDKEYS, f'{n}: only documented keys', str(set(d) - CMDKEYS))
    chk(re.search(r'[$][0-9]', s) is None, f'{n}: no 0-based positional args')

print()
print('=== 4. DUPLICATION ===')


def norm(s):
    s = re.sub(r'^[#>*\d.|`' + SEP + r's-]+', '', s.strip().lower())
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', ' ', s)).strip()


idx = collections.defaultdict(set)
for f in files:
    for ln in open(f, encoding='utf-8'):
        n = norm(ln)
        if len(n.split()) >= 7:
            idx[n].add(f)
dupes = {k: v for k, v in idx.items() if len(v) > 1}
print(f'  files scanned: {len(files)}   duplicated substantive lines: {len(dupes)}')
BUCKET_OK = {'core/CLAUDE.md', 'core/commands/task.md'}
unexplained = []
for k, v in sorted(dupes.items(), key=lambda x: -len(x[1])):
    reason = ''
    if v <= BUCKET_OK:
        reason = 'bucket headings: CLAUDE.md defines, command emits'
    elif v <= (BUCKET_OK | {'README.md'}):
        reason = 'bucket structure: CLAUDE.md defines, command creates, README documents'
    elif 'README.md' in v and len(v) == 2:
        reason = 'README is docs, not config'
    else:
        reason = 'UNEXPLAINED'
        unexplained.append((k, v))
    print(f'    [{len(v)}] {k[:48]:48s} {reason}')
chk(not unexplained, 'no unexplained duplication', str(unexplained[:2]))

print()
print('=== 5. ONE OWNER PER CONCEPT (config only) ===')
cfg = [f for f in files if 'README' not in f]
for concept, pat in [('six-section brief', 'CURRENT STATE'),
                     ('banned phrases', 'explore all approaches'),
                     ('model resolution order', 'Resolution order'),
                     ('roster table', r'`scout`[^|]*\|\s*haiku'),
                     ('bucket protocol rules', 'reverse a decision')]:
    owners = [f for f in cfg if re.search(pat, open(f, encoding='utf-8').read())]
    definers = [f for f in owners if f == 'core/CLAUDE.md']
    chk(len(owners) >= 1, f'{concept}: exists at all', 'ZERO owners - concept vanished')
    chk(len(definers) == 1 or len(owners) == 1, f'{concept}: single definition', str(owners))
    if owners != ['core/CLAUDE.md']:
        print(f'       (also referenced in: {[o for o in owners if o != "core/CLAUDE.md"]})')

print()
print('=== 6. NO DANGLING REFERENCES ===')
nonmd = {slash(f) for f in glob.glob('**/*', recursive=True) if os.path.isfile(f)}
allfiles = set(files) | {slash(f) for f in nonmd}
for f in files:
    s = open(f, encoding='utf-8').read()
    refs = set(re.findall(r'`((?:core|extras)/[A-Za-z0-9_./-]+)`', s))
    for ref in refs:
        r = ref.rstrip('/')
        ok = r in allfiles or any(p.startswith(r + '/') for p in allfiles)
        chk(ok, f'{f} -> {ref}')
    chk('_BRIEF-TEMPLATE' not in s, f'{f}: no ref to deleted _BRIEF-TEMPLATE.md')

print()
print(f'checks run: {checks}   failures: {len(fails)}')
for x in fails:
    print('  FAILED: ' + x)
sys.exit(1 if fails else 0)
