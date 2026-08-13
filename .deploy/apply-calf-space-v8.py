from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
s = path.read_text(encoding='utf-8')

if 'CALF_SPACE_V8' in s:
    print('CALF_SPACE_V8 already applied')
    raise SystemExit(0)

def must_replace(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'Missing expected anchor: {label}')
    s = s.replace(old, new, 1)

must_replace(
    "function shelterTab(p){const s=p.shelter||{},a=shelterAssessment(s),roof=s.roofMaterial||'straw',animalType=s.animalType||'calf',project=s.projectType||'fattening',waste=s.wasteUse||'undecided';return",
    "/* CALF_SPACE_V8 */\nfunction shelterTab(p){const s=p.shelter||{},a=shelterAssessment(s),roof=s.roofMaterial||'straw',animalType=s.animalType||'calf',project=s.projectType||'fattening',waste=s.wasteUse||'undecided',calfSpace=Number(s.calfSpacePerHead)||3;return",
    'shelterTab header'
)

must_replace(
    '<div class=\"field\"><label>عدد الحيوانات المخطط</label><input name=\"headCount\" type=\"number\" min=\"1\" value=\"${s.headCount||\'\'}\" required></div><div class=\"field\"><label>مكان التسمين</label>',
    '<div class=\"field\"><label>عدد الحيوانات المخطط</label><input name=\"headCount\" type=\"number\" min=\"1\" value=\"${s.headCount||\'\'}\" required></div><div class=\"field\" id=\"calfSpaceField\" style=\"${animalType===\'calf\'?\'\':\'display:none\'}\"><label>المساحة المعتمدة لكل عجل (م²)</label><input name=\"calfSpacePerHead\" type=\"number\" min=\"0.1\" step=\"0.1\" value=\"${calfSpace}\" required><div class=\"form-help\">القيمة التشغيلية الحالية 3 م² لكل عجل. يمكن تعديلها لاحقًا عند اعتماد قيمة جديدة.</div></div><div class=\"field\"><label>مكان التسمين</label>',
    'calf space field'
)

must_replace(
    '<div class=\"source-note\">غير محدد تفاصيل أمان الزريبة، أبعاد المعالف والمساقي، مساحة العجل، تكلفة زريبة أربعة عجول أو روتين النظافة التفصيلي؛ لذلك لم تُحدد في النظام.</div>',
    '<div class=\"source-note\">مساحة العجل التشغيلية المعتمدة حاليًا هي 3 م² للرأس. يمكن تعديلها من الحقل أعلاه مستقبلًا دون تغيير بقية حسابات الزريبة. أما أبعاد المعالف والمساقي وتفاصيل الأمان غير المحددة فتبقى دون افتراضات إضافية.</div>',
    'old calf source note'
)

must_replace(
    '<div class=\"alert\"><span class=\"dot\"></span><div><strong>العجول</strong><small>لا يعرض النظام رقم مساحة للعجل لأن البيانات المرجعية غير محدد رقمًا واضحًا.</small></div></div>',
    '<div class=\"alert good\"><span class=\"dot\"></span><div><strong>العجول: 3 م² لكل رأس</strong><small>هذه هي القيمة التشغيلية الحالية، ويمكن تعديلها لاحقًا من إعداد الزريبة.</small></div></div>',
    'calf space alert'
)

must_replace(
    "function updateShelterAssessment(){const f=document.getElementById('shelterForm');if(!f)return;const type=f.elements.animalType.value,count=+f.elements.headCount.value||0,roof=f.elements.roofMaterial.value;const space=document.getElementById('shelterSpaceNote'),roofNote=document.getElementById('shelterRoofNote'),ins=document.getElementById('insulationField'),wasteNote=document.getElementById('wasteNote'),beginner=document.getElementById('beginnerNote'),box=document.getElementById('shelterAssessment');if(ins)ins.style.display=roof==='zinc'?'':'none';if(space)space.textContent=type==='sheep'?(count?`المساحة المسقوفة المطلوبة تقريبًا: ${count} م² (${count} رأس × 1 م²).`:'للضأن: متر مربع مسقوف تقريبًا لكل رأس.'):'لا توجد قيمة محددة لـ رقم واضح لمساحة العجل الواحد؛ لذلك لا يحسب النظام رقمًا غير موثقة.';",
    "function updateShelterAssessment(){const f=document.getElementById('shelterForm');if(!f)return;const type=f.elements.animalType.value,count=+f.elements.headCount.value||0,roof=f.elements.roofMaterial.value,calfSpace=Math.max(.1,Number(f.elements.calfSpacePerHead?.value)||3);const space=document.getElementById('shelterSpaceNote'),roofNote=document.getElementById('shelterRoofNote'),ins=document.getElementById('insulationField'),calfSpaceField=document.getElementById('calfSpaceField'),wasteNote=document.getElementById('wasteNote'),beginner=document.getElementById('beginnerNote'),box=document.getElementById('shelterAssessment');if(ins)ins.style.display=roof==='zinc'?'':'none';if(calfSpaceField)calfSpaceField.style.display=type==='calf'?'grid':'none';if(space)space.textContent=type==='sheep'?(count?`المساحة المسقوفة المطلوبة تقريبًا: ${count} م² (${count} رأس × 1 م²).`:'للضأن: متر مربع مسقوف تقريبًا لكل رأس.'):(count?`المساحة المطلوبة للعجول: ${Number((count*calfSpace).toFixed(2))} م² (${count} رأس × ${calfSpace} م²).`:`للعجول: ${calfSpace} م² لكل رأس.`);",
    'shelter dynamic calculation'
)

must_replace(
    "const data={projectType:f.get('projectType'),animalType:f.get('animalType'),headCount:+f.get('headCount'),locationType:f.get('locationType'),roofMaterial:f.get('roofMaterial'),insulation:!!f.get('insulation'),tapeMeasure:!!f.get('tapeMeasure'),wasteUse:f.get('wasteUse'),firstCycle:!!f.get('firstCycle')};",
    "const data={projectType:f.get('projectType'),animalType:f.get('animalType'),headCount:+f.get('headCount'),calfSpacePerHead:Math.max(.1,+f.get('calfSpacePerHead')||3),locationType:f.get('locationType'),roofMaterial:f.get('roofMaterial'),insulation:!!f.get('insulation'),tapeMeasure:!!f.get('tapeMeasure'),wasteUse:f.get('wasteUse'),firstCycle:!!f.get('firstCycle')};",
    'save shelter data'
)

path.write_text(s, encoding='utf-8')
print(f'Applied configurable calf shelter space v8: {len(s.encode("utf-8"))} bytes')
