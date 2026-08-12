from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
text = path.read_text(encoding='utf-8')
marker = 'LECTURE6_EMERGENCY_MODULE'
if marker in text:
    print('Lecture 6 module already applied')
    sys.exit(0)

css = r'''
/* LECTURE6_EMERGENCY_MODULE */
.emergency-card{border:1px solid #efc5c5;background:linear-gradient(180deg,#fff,#fffafa)}
.emergency-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:9px;margin:12px 0}
.emergency-case{border:1px solid var(--border);border-radius:12px;background:white;padding:12px;font-size:11px}
.emergency-case strong{display:block;font-size:13px;margin-bottom:5px}
.emergency-guide{border:1px solid #efd8a7;background:#fff8ea;border-radius:13px;padding:14px;margin-top:12px}
.emergency-guide.danger{border-color:#efc5c5;background:#fff1f1}
.emergency-guide h4{margin:0 0 9px;font-size:14px}.emergency-guide ol{margin:0;padding-right:20px}.emergency-guide li{margin:6px 0;font-size:12px}
.emergency-rule{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin-top:10px}.emergency-rule span{padding:9px;border-radius:10px;background:#fff;border:1px solid var(--border);font-size:11px;text-align:center}
.emergency-call{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:10px}
@media(max-width:900px){.emergency-grid,.emergency-rule{grid-template-columns:1fr 1fr}}
@media(max-width:520px){.emergency-grid,.emergency-rule{grid-template-columns:1fr}}
'''
needle = '@media(max-width:1100px)'
if needle not in text:
    raise SystemExit('CSS insertion point not found')
text = text.replace(needle, css + '\n' + needle, 1)

old_items = "const healthCabinetItems=['albendazole','ivermectin','vitamins','bicarbonate','paraffin','antibloat','intestinalDisinfectant','woundSpray','needles','gloves','woundDisinfectant','vetNumberVisible'];"
new_items = "const healthCabinetItems=['albendazole','ivermectin','vitamins','bicarbonate','paraffin','antibloat','saltSugar','externalParasiteProduct','intestinalDisinfectant','woundSpray','needles','gloves','woundDisinfectant','vetNumberVisible'];"
if old_items not in text:
    raise SystemExit('healthCabinetItems pattern not found')
text = text.replace(old_items, new_items, 1)
old_labels = "const healthCabinetLabels={albendazole:'ألبندازول',ivermectin:'إيفرمكتين',vitamins:'فيتامينات',bicarbonate:'بيكربونات الصوديوم',paraffin:'زيت برافين',antibloat:'مستحضر مضاد للنفاخ (دون تثبيت اسم تجاري)',intestinalDisinfectant:'مطهر معوي',woundSpray:'بخاخ للجروح والحشرات/الديدان',needles:'حقن وإبر',gloves:'قفازات',woundDisinfectant:'مطهر للجروح',vetNumberVisible:'رقم الطبيب البيطري ظاهر'};"
new_labels = "const healthCabinetLabels={albendazole:'ألبندازول',ivermectin:'إيفرمكتين',vitamins:'فيتامينات',bicarbonate:'بيكربونات الصوديوم',paraffin:'زيت برافين',antibloat:'مستحضر مضاد للنفاخ (دون تثبيت اسم تجاري)',saltSugar:'ملح وسكر لمحلول تعويض السوائل (دون نسبة ثابتة)',externalParasiteProduct:'مستحضر طفيليات خارجية مع تعليمات العبوة',intestinalDisinfectant:'مطهر معوي',woundSpray:'بخاخ للجروح والحشرات/الديدان',needles:'حقن وإبر',gloves:'قفازات',woundDisinfectant:'مطهر للجروح',vetNumberVisible:'رقم الطبيب البيطري ظاهر'};"
if old_labels not in text:
    raise SystemExit('healthCabinetLabels pattern not found')
text = text.replace(old_labels, new_labels, 1)

emergency_js = r'''
function addDaysDate(d,n){const x=dateObj(d);if(!x)return'';x.setDate(x.getDate()+n);return x.toISOString().slice(0,10)}
function emergencyTypeLabel(t){return t==='bloat'?'نفاخ':t==='acidosis'?'حموضة':t==='diarrhea'?'إسهال':t==='ticks'?'قراد / طفيليات خارجية':t}
function planEmergencies(pid){state.emergencies=state.emergencies||[];return state.emergencies.filter(e=>e.planId===pid)}
function emergencyGuideHtml(type,pid){
 const st=state.healthSettings[pid]||{},phone=st.vetPhone||'',call=phone?`<a class="btn danger small" href="tel:${phone}">📞 اتصل بالطبيب: ${phone}</a>`:`<span class="badge treat">رقم الطبيب غير مسجل — أضفه من صيدلية الزريبة</span>`;
 if(type==='bloat')return `<div class="emergency-guide danger"><h4>النفاخ — انتفاخ الجهة اليسرى</h4><ol><li>اجعل الحيوان يقف ويتحرك.</li><li>ذكرت الدكتورة <strong>لترًا واحدًا من زيت البرافين بالفم</strong> كإسعاف أولي في هذه المحاضرة.</li><li>يمكن استخدام مستحضر مضاد للنفاخ، لكن لا يحدد النظام اسمًا أو جرعة لأي منتج.</li><li><strong>اتصل بالطبيب البيطري ولا تنتظر.</strong></li><li>لا تنفذ ثقبًا أو تدخلًا مباشرًا في الكرش بنفسك؛ هذه الإجراءات للطبيب.</li></ol><div class="emergency-call">${call}</div><div class="source-note">إسعاف أولي كما ورد في المحاضرة السادسة، وليس تشخيصًا أو بديلًا عن الطبيب.</div></div>`;
 if(type==='acidosis')return `<div class="emergency-guide"><h4>الحموضة — اشتباه فقط</h4><ol><li>راجع العلامات: توقف الأكل، خمول، رائحة حامضة من الفم شبيهة بالخل، وقد يوجد إسهال.</li><li>ذكرت الدكتورة إيقاف العلف لمدة <strong>24 ساعة</strong>.</li><li>المثال الوارد: <strong>4 ملاعق بيكربونات صوديوم في 5 لترات ماء</strong>.</li><li>تأكد مع الطبيب أن المشكلة حموضة؛ توقف الأكل قد يكون له أسباب أخرى.</li></ol><div class="emergency-call">${call}</div><div class="source-note">لا يحول النظام هذا المثال إلى جرعة عامة لحالات أخرى.</div></div>`;
 if(type==='diarrhea')return `<div class="emergency-guide"><h4>الإسهال</h4><ol><li>أوقف العلف المركز.</li><li>ذكرت الدكتورة ماءً دافئًا مع الملح والسكر لتعويض السوائل.</li><li><strong>لم تحفظ مقادير الملح والسكر بوضوح؛ لذلك لا يعرض النظام نسبة من عنده.</strong></li><li>إذا ظهر دم في الإسهال: <strong>اتصل بالطبيب فورًا.</strong></li></ol><div class="emergency-call">${call}</div></div>`;
 if(type==='ticks')return `<div class="emergency-guide"><h4>القراد والطفيليات الخارجية</h4><ol><li>سجل وجود القراد/الطفيليات على الجلد.</li><li>ورد في التسجيل رش مستحضر سُمّي صوتيًا «السايبر» كل <strong>14 يومًا</strong> عند الحديث عن ملاحظة القراد.</li><li>لم يذكر التسجيل تركيزًا أو نسبة تخفيف؛ راجع العبوة والطبيب قبل الاستعمال.</li><li>للعدد الكبير: يمكن استخدام المغاطس. للعدد القليل: الرش والتعامل مع الحيوانات واحدةً واحدة.</li><li>الإيفرمكتين كل شهرين موجود أصلًا في البرنامج الوقائي؛ لا يعطيه هذا النموذج تلقائيًا.</li></ol><div class="emergency-call">${call}</div></div>`;
 return '<div class="emergency-guide">اختر الحالة لعرض الإسعاف الأولي الموثق.</div>';
}
function emergencyFieldsHtml(type){
 if(type==='bloat')return `<div class="check-grid"><label class="check-item"><input type="checkbox" name="leftBloat">انتفاخ واضح في الجهة اليسرى</label><label class="check-item"><input type="checkbox" name="moved">تم جعل الحيوان يقف ويتحرك</label><label class="check-item"><input type="checkbox" name="paraffin">تم إعطاء زيت البرافين وفق توجيه المحاضرة/الطبيب</label><label class="check-item"><input type="checkbox" name="vetContacted">تم التواصل مع الطبيب/جارٍ التواصل</label><label class="check-item"><input type="checkbox" name="noRumenIntervention">لم أنفذ تدخلًا مباشرًا في الكرش بنفسي</label></div>`;
 if(type==='acidosis')return `<div class="check-grid"><label class="check-item"><input type="checkbox" name="stoppedEating">توقف عن الأكل</label><label class="check-item"><input type="checkbox" name="lethargy">خمول</label><label class="check-item"><input type="checkbox" name="sourBreath">رائحة فم حامضة</label><label class="check-item"><input type="checkbox" name="diarrhea">يوجد إسهال</label><label class="check-item"><input type="checkbox" name="feedStopped24">تم إيقاف العلف حسب الإرشاد المذكور</label><label class="check-item"><input type="checkbox" name="bicarbonateSolution">تم استخدام مثال البيكربونات المذكور بعد التحقق</label><label class="check-item"><input type="checkbox" name="vetContacted">تم التواصل مع الطبيب للتأكد من التشخيص</label></div>`;
 if(type==='diarrhea')return `<div class="check-grid"><label class="check-item"><input type="checkbox" name="looseStool">فضلات لينة</label><label class="check-item"><input type="checkbox" name="blood">يوجد دم في الإسهال</label><label class="check-item"><input type="checkbox" name="concentrateStopped">تم إيقاف العلف المركز</label><label class="check-item"><input type="checkbox" name="warmSaltSugar">تم تقديم ماء دافئ مع ملح وسكر دون اختراع نسبة</label><label class="check-item"><input type="checkbox" name="vetContacted">تم التواصل مع الطبيب</label></div>`;
 if(type==='ticks')return `<div class="field"><label>عدد الحيوانات المتأثرة</label><select name="caseScale"><option value="few">عدد قليل</option><option value="many">عدد كبير</option></select></div><div class="check-grid" style="margin-top:10px"><label class="check-item"><input type="checkbox" name="ticksSeen">لوحظ قراد/طفيليات خارجية</label><label class="check-item"><input type="checkbox" name="spray">تم الرش</label><label class="check-item"><input type="checkbox" name="dip">تم استخدام مغطس للمجموعة</label><label class="check-item"><input type="checkbox" name="labelChecked">تمت مراجعة تعليمات العبوة/الطبيب للتركيز والتخفيف</label><label class="check-item"><input type="checkbox" name="vetContacted">تم التواصل مع الطبيب/الجهة البيطرية عند الحاجة</label></div>`;
 return '';
}
function updateEmergencyCase(pid){const s=document.getElementById('emergencyType'),t=s?.value||'bloat',g=document.getElementById('emergencyGuide'),f=document.getElementById('emergencyCaseFields');if(g)g.innerHTML=emergencyGuideHtml(t,pid);if(f)f.innerHTML=emergencyFieldsHtml(t)}
function emergencyCard(p){
 const es=planEmergencies(p.id).slice().reverse(),open=es.filter(e=>e.status!=='resolved'),st=state.healthSettings[p.id]||{};
 return `<div class="card emergency-card" style="margin-bottom:16px"><div class="section-title"><div><h3>🚨 التدخل السريع — قاعدة الدقائق الثلاث</h3><div class="small muted">لاحظ العلامة → نفّذ الإسعاف البسيط الموثق → اتصل بالطبيب → لا تنفذ إجراءً خطيرًا بنفسك.</div></div><button class="btn danger" onclick="openEmergencyModal('${p.id}')">تسجيل حالة طارئة</button></div><div class="emergency-rule"><span><strong>1</strong><br>لاحظ بسرعة</span><span><strong>2</strong><br>إسعاف بسيط فقط</span><span><strong>3</strong><br>اتصل بالطبيب</span><span><strong>4</strong><br>لا تدخل خطير</span></div><div class="emergency-grid"><div class="emergency-case"><strong>نفاخ</strong>انتفاخ الجهة اليسرى</div><div class="emergency-case"><strong>حموضة</strong>توقف أكل + خمول + رائحة حامضة</div><div class="emergency-case"><strong>إسهال</strong>والدم يعني طبيبًا فورًا</div><div class="emergency-case"><strong>قراد</strong>رش/مغطس حسب العدد مع تعليمات العبوة</div></div>${st.vetPhone?`<div class="emergency-call"><a class="btn danger small" href="tel:${st.vetPhone}">📞 ${st.vetName||'الطبيب البيطري'} — ${st.vetPhone}</a></div>`:`<div class="alert danger"><span class="dot"></span><div><strong>رقم الطبيب غير مسجل</strong><small>أضفه من «الطبيب وصيدلية الزريبة» قبل الطوارئ.</small></div></div>`}${open.length?`<div class="table-wrap" style="margin-top:12px"><table><thead><tr><th>التاريخ</th><th>الحيوان</th><th>الحالة</th><th>الطبيب</th><th>المتابعة</th><th></th></tr></thead><tbody>${open.slice(0,6).map(e=>`<tr><td>${e.date}</td><td>#${state.animals.find(a=>a.id===e.animalId)?.tag||'-'}</td><td><span class="badge treat">${emergencyTypeLabel(e.type)}</span></td><td>${e.vetContacted?'تم التواصل':'لم يوثق'}</td><td>${e.nextReview||'-'}</td><td><button class="btn small" onclick="markEmergencyResolved('${e.id}')">إغلاق الحالة</button></td></tr>`).join('')}</tbody></table></div>`:''}<div class="source-note">الوحدة تعرض فقط الإسعافات والمقادير التي وردت صراحةً في المحاضرة السادسة، ولا تستبدل التشخيص والعلاج البيطري.</div></div>`;
}
function openEmergencyModal(pid){const as=planAnimals(pid).filter(a=>a.status!=='sold');modal(`<div class="modal-head"><div><h3>🚨 تسجيل تدخل سريع</h3><div class="small muted">الإسعاف الأولي إلى أن يصل الطبيب — لا تستخدم هذه الشاشة بدل التشخيص.</div></div><button class="close" onclick="closeModal()">×</button></div><form onsubmit="saveEmergency(event,'${pid}')"><div class="form-grid"><div class="field"><label>الحيوان</label><select name="animal" required>${as.map(a=>`<option value="${a.id}">#${a.tag}</option>`).join('')}</select></div><div class="field"><label>التاريخ</label><input name="date" type="date" value="${today()}" required></div><div class="field"><label>الحالة</label><select id="emergencyType" name="type" onchange="updateEmergencyCase('${pid}')" required><option value="bloat">نفاخ</option><option value="acidosis">حموضة</option><option value="diarrhea">إسهال</option><option value="ticks">قراد / طفيليات خارجية</option></select></div></div><div id="emergencyGuide">${emergencyGuideHtml('bloat',pid)}</div><div class="selection-box"><h4>ما الذي لاحظته أو نفذته؟</h4><div id="emergencyCaseFields">${emergencyFieldsHtml('bloat')}</div></div><div class="field full" style="margin-top:12px"><label>ملاحظة الحالة / توجيه الطبيب</label><textarea name="note"></textarea></div><div class="modal-actions"><button type="button" class="btn" onclick="closeModal()">إلغاء</button><button class="btn danger">حفظ الحالة</button></div></form>`)}
function saveEmergency(ev,pid){ev.preventDefault();const f=new FormData(ev.target),type=f.get('type'),aid=f.get('animal'),date=f.get('date'),boolNames=['leftBloat','moved','paraffin','vetContacted','noRumenIntervention','stoppedEating','lethargy','sourBreath','diarrhea','feedStopped24','bicarbonateSolution','looseStool','blood','concentrateStopped','warmSaltSugar','ticksSeen','spray','dip','labelChecked'];const actions=Object.fromEntries(boolNames.map(n=>[n,!!f.get(n)]));if(type==='ticks'&&(actions.spray||actions.dip)&&!actions.labelChecked){alert('لا تسجل رشًا أو مغطسًا قبل توثيق مراجعة تعليمات العبوة/الطبيب للتركيز والتخفيف.');return;}const urgent=type==='bloat'||(type==='diarrhea'&&actions.blood),nextReview=type==='ticks'&&(actions.spray||actions.dip)?addDaysDate(date,14):'';state.emergencies=state.emergencies||[];state.emergencies.push({id:uid('em'),planId:pid,animalId:aid,date,type,status:'open',urgent,vetContacted:actions.vetContacted,actions,caseScale:f.get('caseScale')||'',nextReview,note:f.get('note')});const a=state.animals.find(x=>x.id===aid);if(a&&type!=='ticks'&&a.status!=='sold')a.status='treatment';save();closeModal();render();setTimeout(()=>{if(urgent&&!actions.vetContacted)alert('تم حفظ الحالة، لكن المحاضرة تنص على الاتصال بالطبيب فورًا في هذه الحالة.');else if(type==='ticks'&&nextReview)alert(`تم حفظ الإجراء. موعد المراجعة التالي حسب تكرار 14 يومًا الوارد في التسجيل: ${nextReview}. راجع العبوة والطبيب ولا تعتبر هذا التذكير جرعة تلقائية.`);else alert('تم حفظ التدخل السريع في سجل الحيوان.');},0)}
function markEmergencyResolved(id){state.emergencies=state.emergencies||[];const e=state.emergencies.find(x=>x.id===id);if(!e)return;e.status='resolved';e.resolvedAt=today();save();render()}
'''
insert_point = 'function openArrivalHealthModal(pid)'
if insert_point not in text:
    raise SystemExit('Emergency JS insertion point not found')
text = text.replace(insert_point, emergency_js + '\n' + insert_point, 1)

start = text.find('function healthTab(p){')
end = text.find('function openArrivalHealthModal(pid)', start)
if start < 0 or end < 0:
    raise SystemExit('healthTab region not found')
segment = text[start:end]
needle = '${withdraw?'
if needle not in segment:
    raise SystemExit('healthTab withdrawal insertion anchor not found')
segment = segment.replace(needle, '${emergencyCard(p)}\n ${withdraw?', 1)
text = text[:start] + segment + text[end:]

lethargy_label = '<label class="check-item"><input type="checkbox" name="lethargy">خمول أو تغير مفاجئ في السلوك</label>'
addition = '<label class="check-item"><input type="checkbox" name="sourBreath">رائحة غير معتادة/حامضة من الفم</label><label class="check-item"><input type="checkbox" name="ticks">وجود قراد أو طفيليات خارجية على الجلد</label>' + lethargy_label
if lethargy_label not in text:
    raise SystemExit('daily health lethargy label not found')
text = text.replace(lethargy_label, addition, 1)

save_anchor = "woundOrDischarge:!!f.get('woundOrDischarge'),severeWound:!!f.get('severeWound'),lethargy:!!f.get('lethargy')"
if save_anchor not in text:
    raise SystemExit('saveHealthDaily object anchor not found')
text = text.replace(save_anchor, "woundOrDischarge:!!f.get('woundOrDischarge'),severeWound:!!f.get('severeWound'),sourBreath:!!f.get('sourBreath'),ticks:!!f.get('ticks'),lethargy:!!f.get('lethargy')", 1)

status_anchor = "l.woundOrDischarge||l.lethargy||l.suddenStopFoodWater"
if status_anchor not in text:
    raise SystemExit('health daily status anchor not found')
text = text.replace(status_anchor, "l.woundOrDischarge||l.sourBreath||l.ticks||l.lethargy||l.suddenStopFoodWater", 1)

notes_anchor = "l.woundOrDischarge?'جرح/إفرازات':'',l.lethargy?'خمول':''"
if notes_anchor not in text:
    raise SystemExit('health daily table notes anchor not found')
text = text.replace(notes_anchor, "l.woundOrDischarge?'جرح/إفرازات':'',l.sourBreath?'رائحة فم حامضة':'',l.ticks?'قراد/طفيليات خارجية':'',l.lethargy?'خمول':''", 1)

alert_anchor = "if(dg.length)setTimeout(()=>alert('علامة خطر تستدعي التواصل مع الطبيب فورًا حسب المحاضرة: '+dg.join('، ')+(l.isolated?'':'\\nكما لم يتم توثيق عزل الحيوان.')),0)"
if alert_anchor in text:
    text = text.replace(alert_anchor, "if(dg.length)setTimeout(()=>alert('علامة خطر تستدعي التواصل مع الطبيب فورًا حسب المحاضرة: '+dg.join('، ')+(l.isolated?'':'\\nكما لم يتم توثيق عزل الحيوان.')+'\\nافتح «التدخل السريع» من تبويب الصحة الوقائية لتسجيل الإسعاف الأولي.'),0)", 1)

path.write_text(text, encoding='utf-8')
print(f'Patched {path} - bytes={path.stat().st_size}')
