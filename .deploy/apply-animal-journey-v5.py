from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
addon_path = Path(__file__).with_name('animal-journey-v5-addon.html')
s = path.read_text(encoding='utf-8')
marker = 'ANIMAL_JOURNEY_V5'
if marker in s:
    print('Animal journey v5 already applied')
    raise SystemExit(0)
addon = addon_path.read_text(encoding='utf-8')
if '</body>' not in s:
    raise RuntimeError('closing body tag not found')
s = s.replace('</body>', addon + '\n</body>', 1)
path.write_text(s, encoding='utf-8')
print(f'Applied animal journey v5: {len(s.encode("utf-8"))} bytes')
