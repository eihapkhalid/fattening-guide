from pathlib import Path
import sys

path=Path(sys.argv[1] if len(sys.argv)>1 else 'index.html')
s=path.read_text(encoding='utf-8')
marker='FEEDING_INPUT_PERSISTENCE_V15'
if marker in s:
    print(marker+' already applied')
    raise SystemExit(0)
addon=Path('.deploy/feeding-input-persistence-v15-addon.html').read_text(encoding='utf-8')
needle='</body>'
if needle not in s:
    raise SystemExit('Missing </body>')
s=s.replace(needle,addon+'\n'+needle,1)
path.write_text(s,encoding='utf-8')
print('Applied '+marker)
