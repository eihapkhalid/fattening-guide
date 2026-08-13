from pathlib import Path
import sys

path=Path(sys.argv[1] if len(sys.argv)>1 else 'index.html')
s=path.read_text(encoding='utf-8')
changed=False

marker='PLAN_LIFECYCLE_POLISH_V14'
if marker not in s:
    addon=Path('.deploy/plan-lifecycle-polish-v14-addon.html').read_text(encoding='utf-8')
    if '</body>' not in s:
        raise RuntimeError('Missing </body>')
    s=s.replace('</body>',addon+'\n</body>',1)
    changed=True
    print('Applied plan lifecycle polish v14')
else:
    print('Plan lifecycle polish v14 already applied')

# Keep the newest feeding-input fix in the single main deployment chain.
v15_marker='FEEDING_INPUT_PERSISTENCE_V15'
if v15_marker not in s:
    addon=Path('.deploy/feeding-input-persistence-v15-addon.html').read_text(encoding='utf-8')
    if '</body>' not in s:
        raise RuntimeError('Missing </body>')
    s=s.replace('</body>',addon+'\n</body>',1)
    changed=True
    print('Applied feeding input persistence v15')
else:
    print('Feeding input persistence v15 already applied')

# Keep feed actions prominent without creating a second deployment workflow.
v16_marker='FEED_ACTIONS_V16'
if v16_marker not in s:
    addon=Path('.deploy/feed-actions-v16-addon.html').read_text(encoding='utf-8')
    if '</body>' not in s:
        raise RuntimeError('Missing </body>')
    s=s.replace('</body>',addon+'\n</body>',1)
    changed=True
    print('Applied feed actions v16')
else:
    print('Feed actions v16 already applied')

if changed:
    path.write_text(s,encoding='utf-8')
