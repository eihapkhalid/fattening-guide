from pathlib import Path
import sys
p=Path(sys.argv[1] if len(sys.argv)>1 else 'index.html')
s=p.read_text(encoding='utf-8')
old="save();closeModal();state.planTab='feeding';save();render();if(quality)successV9('تمت إضافة الأعلاف إلى المخزون. انتقلنا إلى تسجيل التغذية.');else warningV9('تم حفظ الأعلاف، لكنها تحتاج مراجعة الجودة قبل استخدامها.');setTimeout(()=>openFeedingLogModal(pid),130)"
new="save();closeModal();if(quality){state.planTab='feeding';save();render();successV9('تمت إضافة الأعلاف إلى المخزون. انتقلنا إلى تسجيل التغذية.');setTimeout(()=>openFeedingLogModal(pid),130)}else{state.planTab='feeds';save();render();warningV9('تم حفظ الأعلاف، لكنها تحتاج مراجعة الجودة قبل استخدامها؛ لذلك لم يتم فتح تسجيل التغذية.')}"
if new not in s:
    if old not in s:
        raise RuntimeError('guided feed transition pattern not found')
    s=s.replace(old,new,1)

# Keep the plan state structurally safe before guided workflow tests and user actions.
marker='GUIDED_STATE_INIT_V10'
if marker not in s:
    init=f'''\n<script>\n/* {marker} */\nif(typeof state!=="undefined"&&Array.isArray(state.plans)){{state.plans.forEach(p=>{{if(!p.shelter)p.shelter={{}}}});}}\n</script>\n'''
    s=s.replace('</body>',init+'\n</body>',1)

p.write_text(s,encoding='utf-8')
print('Hardened guided feed quality transition and shelter state')
