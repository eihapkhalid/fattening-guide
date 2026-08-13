from pathlib import Path
import sys

path=Path(sys.argv[1] if len(sys.argv)>1 else 'index.html')
s=path.read_text(encoding='utf-8')
marker='FLEXIBLE_MIX_STATUS_V11'
if marker in s:
    print('FLEXIBLE_MIX_STATUS_V11 already applied')
    raise SystemExit(0)
addon=Path(__file__).with_name('flexible-mix-status-v11-addon.html').read_text(encoding='utf-8')
if '</body>' not in s:
    raise RuntimeError('closing body tag not found')
s=s.replace('</body>',addon+'\n</body>',1)
path.write_text(s,encoding='utf-8')
print(f'Applied flexible mix/status v11: {len(s.encode("utf-8"))} bytes')
