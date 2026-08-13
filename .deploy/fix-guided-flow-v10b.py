from pathlib import Path
import sys
p=Path(sys.argv[1] if len(sys.argv)>1 else 'index.html')
s=p.read_text(encoding='utf-8')
old='const cb=form.querySelector(`input[name="feedCode"][value="${CSS.escape(code)}"]`);'
new='const cb=[...form.querySelectorAll(\'input[name="feedCode"]\')].find(x=>x.value===code);'
if old in s:
    s=s.replace(old,new)
if 'GUIDED_FLOW_V10' not in s:
    raise RuntimeError('GUIDED_FLOW_V10 missing')
p.write_text(s,encoding='utf-8')
print('Hardened guided flow v10 selectors')
