from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
s = path.read_text(encoding='utf-8')

# BEGINNER_FLOW_V2 helpers were local to an IIFE, while a later visual layer
# redefined dashboard/planPage/plansPage and referenced them as globals.
# Expose only the three helpers that the later layer actually uses.
replacements = {
    '  function ezDay(p){': '  window.ezDay=function ezDay(p){',
    '  function ezPhase(p){': '  window.ezPhase=function ezPhase(p){',
    '  function ezNext(p){': '  window.ezNext=function ezNext(p){',
}
for old, new in replacements.items():
    if old in s:
        s = s.replace(old, new, 1)

# Hidden management screens previously highlighted "اليوم" even when the
# user was viewing feeds/cycle/reports/shelter, which made navigation look broken.
old_nav = "const nav=['shelter','feeds','treatments','expenses','reports','cycle','daily','more'].includes(state.planTab)?'overview':(state.planTab||'overview');"
s = s.replace(old_nav, "const nav=state.planTab||'overview';")

# Guard against publishing the known broken scope again.
for name in ('ezDay','ezPhase','ezNext'):
    if f'window.{name}=function {name}' not in s:
        raise RuntimeError(f'{name} was not exposed; expected BEGINNER_FLOW_V2 source not found')

path.write_text(s, encoding='utf-8')
print(f'JavaScript runtime stability fix applied: {path} ({len(s.encode("utf-8"))} bytes)')
