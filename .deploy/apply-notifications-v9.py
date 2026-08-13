from pathlib import Path
import sys

path=Path(sys.argv[1] if len(sys.argv)>1 else 'index.html')
s=path.read_text(encoding='utf-8')
if 'NOTIFICATIONS_V9' in s:
    print('NOTIFICATIONS_V9 already applied')
    raise SystemExit(0)

block=r'''
<style>
/* NOTIFICATIONS_V9 */
.notify-v9-wrap{position:fixed;top:84px;left:20px;z-index:250;display:grid;gap:10px;width:min(390px,calc(100vw - 32px));pointer-events:none}
.notify-v9{pointer-events:auto;background:#fff;border:1px solid var(--border);border-radius:13px;box-shadow:0 14px 38px rgba(23,42,34,.14);padding:12px 12px 12px 10px;display:grid;grid-template-columns:34px 1fr 28px;gap:10px;align-items:start;animation:notifyV9In .18s ease-out}
.notify-v9-icon{width:34px;height:34px;border-radius:10px;display:grid;place-items:center}.notify-v9-icon svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.notify-v9.success{border-right:4px solid #2f7d59}.notify-v9.success .notify-v9-icon{background:#eaf5ef;color:#276c4d}.notify-v9.error{border-right:4px solid #b94040}.notify-v9.error .notify-v9-icon{background:#fff0f0;color:#a73434}.notify-v9.warning{border-right:4px solid #b77822}.notify-v9.warning .notify-v9-icon{background:#fff6e7;color:#976016}.notify-v9.info{border-right:4px solid #52718a}.notify-v9.info .notify-v9-icon{background:#eef4f8;color:#48677f}
.notify-v9-title{font-size:13px;font-weight:700;line-height:1.5;margin:0 0 2px}.notify-v9-msg{font-size:12px;line-height:1.65;color:var(--muted);overflow-wrap:anywhere}.notify-v9-close{border:0;background:transparent;color:#7c8882;width:28px;height:28px;border-radius:8px;display:grid;place-items:center;font-size:18px;line-height:1}.notify-v9-close:hover{background:#f0f3f1;color:var(--text)}
.notify-v9.out{opacity:0;transform:translateY(-5px);transition:.16s ease}
@keyframes notifyV9In{from{opacity:0;transform:translateY(-7px)}to{opacity:1;transform:none}}
@media(max-width:640px){.notify-v9-wrap{top:76px;left:16px;right:16px;width:auto}.notify-v9{grid-template-columns:32px 1fr 26px;padding:11px 10px}}
@media(prefers-reduced-motion:reduce){.notify-v9{animation:none}.notify-v9.out{transition:none}}
</style>
<script>
/* NOTIFICATIONS_V9 */
(()=>{
  const icons={
    success:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
    error:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="m9 9 6 6m0-6-6 6"/></svg>',
    warning:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 2.8 19h18.4L12 3Z"/><path d="M12 9v4m0 3h.01"/></svg>',
    info:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v5m0-8h.01"/></svg>'
  };
  const titles={success:'تم بنجاح',error:'تعذر إكمال الإجراء',warning:'تنبيه',info:'معلومة'};
  function wrap(){let el=document.getElementById('notifyV9Wrap');if(!el){el=document.createElement('div');el.id='notifyV9Wrap';el.className='notify-v9-wrap';el.setAttribute('aria-live','polite');el.setAttribute('aria-relevant','additions');document.body.appendChild(el)}return el}
  function close(el){if(!el||!el.parentNode)return;el.classList.add('out');setTimeout(()=>el.remove(),180)}
  window.notifyV9=function(type,message,opts={}){
    type=['success','error','warning','info'].includes(type)?type:'info';
    const host=wrap(),el=document.createElement('div');el.className=`notify-v9 ${type}`;el.setAttribute('role',type==='error'?'alert':'status');
    const icon=document.createElement('div');icon.className='notify-v9-icon';icon.innerHTML=icons[type];
    const body=document.createElement('div'),title=document.createElement('div'),msg=document.createElement('div');title.className='notify-v9-title';title.textContent=opts.title||titles[type];msg.className='notify-v9-msg';msg.textContent=String(message??'');body.append(title,msg);
    const x=document.createElement('button');x.type='button';x.className='notify-v9-close';x.setAttribute('aria-label','إغلاق الرسالة');x.textContent='×';x.onclick=()=>close(el);
    el.append(icon,body,x);host.prepend(el);
    while(host.children.length>4)host.lastElementChild.remove();
    const duration=Number(opts.duration??(type==='success'?3200:type==='info'?4200:type==='warning'?5600:7000));if(duration>0)setTimeout(()=>close(el),duration);
    return el;
  };
  window.successV9=(m,o)=>notifyV9('success',m,o);
  window.errorV9=(m,o)=>notifyV9('error',m,o);
  window.warningV9=(m,o)=>notifyV9('warning',m,o);
  window.infoV9=(m,o)=>notifyV9('info',m,o);
  window.notificationTypeV9=function(message){
    const m=String(message??'').trim();
    if(/^(تم|تمت|اكتمل|نجح)|بنجاح|تم حفظ|تم تسجيل|جاهزة/.test(m))return 'success';
    if(/^(لا |لا يمكن|لا يوجد|لا توجد|تعذر|فشل|خطأ|أدخل|اختر|يلزم|يجب)|غير صالح|مفقود|ناقص/.test(m))return 'error';
    if(/تنبيه|تحذير|انتبه|تأكد|راجع|فترة سحب|طوارئ|مشكلة/.test(m))return 'warning';
    return 'info';
  };
  // Keep existing application code compatible while replacing blocking browser alerts.
  window.alert=function(message){return notifyV9(notificationTypeV9(message),message)};
})();
</script>
'''

s=s.replace('</body>',block+'\n</body>',1)
path.write_text(s,encoding='utf-8')
print(f'Applied notification system v9: {len(s.encode("utf-8"))} bytes')
