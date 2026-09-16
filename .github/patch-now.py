from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
if 'const nowTracker =' in s:
    print('Already patched')
    raise SystemExit(0)

css = r'''
/* 当前时间定位 */
.event.is-current{border:2px solid #e1a82b!important;box-shadow:0 12px 30px rgba(225,168,43,.22),0 0 0 4px rgba(239,197,91,.15);background:linear-gradient(100deg,#fff8df,#fff 28%)!important;transform:translateY(-1px)}
.event.is-current:before{border-color:#e1a82b!important;background:#fff7d4!important;box-shadow:0 0 0 6px rgba(225,168,43,.16)}
.event.is-next{border:1.5px dashed #3d8e85!important;background:linear-gradient(100deg,rgba(33,120,111,.07),#fff 24%)!important}
.now-status{display:inline-flex;align-items:center;gap:6px;padding:4px 9px;border-radius:999px;font-size:11px;font-weight:900;letter-spacing:.03em;white-space:nowrap}
.now-status.current{background:#f4c94f;color:#4b3700;box-shadow:0 2px 8px rgba(180,128,0,.16)}
.now-status.current:before{content:"";width:7px;height:7px;border-radius:50%;background:#d04b35;box-shadow:0 0 0 4px rgba(208,75,53,.12)}
.now-status.next{background:#dff1ed;color:#176158;border:1px solid #c7e1da}
.now-locator{position:fixed;right:18px;bottom:18px;z-index:9000;display:none;align-items:center;gap:8px;border:1px solid rgba(18,52,71,.15);background:#123447;color:#fff;border-radius:999px;padding:11px 15px;font-size:13px;font-weight:850;box-shadow:0 10px 30px rgba(18,52,71,.28);cursor:pointer}.now-locator.show{display:flex}.now-locator:hover{background:#174b63}.now-locator .pulse{width:9px;height:9px;border-radius:50%;background:#efc55b;box-shadow:0 0 0 0 rgba(239,197,91,.55);animation:tripPulse 1.8s infinite}.now-locator.next-mode .pulse{background:#78c1b8}.now-locator small{font-size:10px;opacity:.72;font-weight:650}@keyframes tripPulse{0%{box-shadow:0 0 0 0 rgba(239,197,91,.5)}70%{box-shadow:0 0 0 8px rgba(239,197,91,0)}100%{box-shadow:0 0 0 0 rgba(239,197,91,0)}}
.day.is-today>.day-head{background:linear-gradient(90deg,rgba(239,197,91,.12),transparent);margin:-8px -8px 0;padding:8px 8px 17px;border-radius:14px 14px 0 0}
@media(max-width:760px){.now-locator{right:12px;bottom:12px;padding:10px 13px}.event.is-current{box-shadow:0 8px 24px rgba(225,168,43,.20),0 0 0 3px rgba(239,197,91,.12)}}
'''
marker = '/* 时间轴节点类型：让“游玩 / 吃饭 / 通勤 / 酒店 / 预约 / 手续”一眼可辨 */'
if marker not in s:
    raise RuntimeError('CSS insertion marker not found')
s = s.replace(marker, css + '\n' + marker, 1)

tracker = r'''  const nowTracker = `
<button class="now-locator" id="nowLocator" type="button" aria-label="定位到当前行程"><span class="pulse"></span><span id="nowLocatorText">定位现在</span><small>设备时间</small></button>
<script>
(()=>{
  const tripYear=2026;
  const dayIds=['d0919','d0920','d0921','d0922','d0923','d0924','d0925','d0926','d0927'];
  const btn=document.getElementById('nowLocator');
  const btnText=document.getElementById('nowLocatorText');
  let target=null;
  const pad=n=>String(n).padStart(2,'0');
  const mins=(h,m)=>h*60+m;
  function parseRange(text){
    const clean=String(text||'').replace(/[：]/g,':');
    const ms=[...clean.matchAll(/(\d{1,2}):(\d{2})/g)].map(x=>mins(+x[1],+x[2]));
    if(ms.length>=2){let a=ms[0],b=ms[1];if(b<a)b+=1440;return [a,b];}
    if(ms.length===1){const t=ms[0];if(/前/.test(clean)) return [Math.max(0,t-60),t];return [t,t+30];}
    return null;
  }
  function dayKeyFromId(id){return tripYear+'-'+id.slice(1,3)+'-'+id.slice(3,5);}
  function reset(){document.querySelectorAll('.event.is-current,.event.is-next').forEach(e=>e.classList.remove('is-current','is-next'));document.querySelectorAll('.now-status').forEach(e=>e.remove());document.querySelectorAll('.day.is-today').forEach(e=>e.classList.remove('is-today'));}
  function addBadge(ev,mode){const row=ev.querySelector('.time-row');if(!row)return;const b=document.createElement('span');b.className='now-status '+mode;b.textContent=mode==='current'?'NOW 当前':'NEXT 接下来';const duration=row.querySelector('.duration');if(duration)row.insertBefore(b,duration);else row.appendChild(b);}
  function getEvents(day){return [...day.querySelectorAll('.timeline .event')].map((ev,i)=>({ev,i,range:parseRange(ev.querySelector('.time')?.textContent)})).filter(x=>x.range);}
  function locate(scroll){
    reset();target=null;btn.classList.remove('show','next-mode');
    const now=new Date();
    const today=now.getFullYear()+'-'+pad(now.getMonth()+1)+'-'+pad(now.getDate());
    let nowMin=mins(now.getHours(),now.getMinutes());
    let day=dayIds.map(id=>document.getElementById(id)).find(d=>d&&dayKeyFromId(d.id)===today);
    let carryPrev=false;
    if(!day && now.getHours()<3){const yesterday=new Date(now);yesterday.setDate(now.getDate()-1);const ykey=yesterday.getFullYear()+'-'+pad(yesterday.getMonth()+1)+'-'+pad(yesterday.getDate());day=dayIds.map(id=>document.getElementById(id)).find(d=>d&&dayKeyFromId(d.id)===ykey);if(day){carryPrev=true;nowMin+=1440;}}
    if(!day) return;
    day.classList.add('is-today');
    const events=getEvents(day).map(x=>{let [a,b]=x.range;if(carryPrev||a<240){if(a<240)a+=1440;if(b<240)b+=1440;}return {...x,a,b};});
    const current=events.find(x=>nowMin>=x.a&&nowMin<=x.b);
    const next=events.find(x=>x.a>nowMin);
    if(current){target=current.ev;target.classList.add('is-current');addBadge(target,'current');btn.classList.add('show');btnText.textContent='现在 '+pad(now.getHours())+':'+pad(now.getMinutes());}
    else if(next){target=next.ev;target.classList.add('is-next');addBadge(target,'next');btn.classList.add('show','next-mode');btnText.textContent='接下来 '+pad(Math.floor(next.a%1440/60))+':'+pad(next.a%60);}
    else{const idx=dayIds.indexOf(day.id);const nextDay=idx>=0?document.getElementById(dayIds[idx+1]):null;if(nextDay){const first=getEvents(nextDay)[0];if(first){target=first.ev;target.classList.add('is-next');addBadge(target,'next');btn.classList.add('show','next-mode');btnText.textContent='下一天';}}}
    if(scroll&&target&&!location.hash)setTimeout(()=>target.scrollIntoView({behavior:'smooth',block:'center'}),420);
  }
  btn?.addEventListener('click',()=>{locate(false);target?.scrollIntoView({behavior:'smooth',block:'center'});});
  locate(true);
  setInterval(()=>locate(false),60000);
})();
<\/script>`;
  src = src.replace('</body>', nowTracker + '\n</body>');

'''
needle = '  document.open(); document.write(src); document.close();'
if needle not in s:
    raise RuntimeError('JS insertion marker not found')
s = s.replace(needle, tracker + needle, 1)
p.write_text(s, encoding='utf-8')
