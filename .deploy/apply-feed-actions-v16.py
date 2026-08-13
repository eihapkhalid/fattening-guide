from pathlib import Path
import sys

path=Path(sys.argv[1] if len(sys.argv)>1 else 'index.html')
s=path.read_text(encoding='utf-8')
marker='FEED_ACTIONS_V16'
if marker in s:
    print('Feed actions v16 already applied')
    raise SystemExit(0)
addon=Path('.deploy/feed-actions-v16-addon.html').read_text(encoding='utf-8')
if '</body>' not in s:
    raise RuntimeError('Missing </body>')
s=s.replace('</body>',addon+'\n</body>',1)
path.write_text(s,encoding='utf-8')
print('Applied feed actions v16')
