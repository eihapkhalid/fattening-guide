from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
addon_path = Path(__file__).with_name('usability-v4-addon.html')
s = path.read_text(encoding='utf-8')
marker = 'USABILITY_V4_HERD_TIMELINE_FEEDING'
if marker in s:
    print('Usability v4 already applied')
    raise SystemExit(0)
addon = addon_path.read_text(encoding='utf-8')
if '</body>' not in s:
    raise RuntimeError('closing body tag not found')
s = s.replace('</body>', addon + '\n</body>', 1)
path.write_text(s, encoding='utf-8')
print(f'Applied usability v4: {len(s.encode("utf-8"))} bytes')
