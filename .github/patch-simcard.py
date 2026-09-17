from pathlib import Path

p = Path('itinerary-base.html')
s = p.read_text(encoding='utf-8')

old = '''    <article class="event transport"><div class="time-row"><div class="time">14:50–15:10</div><span class="duration">出租车</span></div><h3>酒店 → 赤崁楼</h3><p>台南两人出行以出租车节省时间，不把市区公交作为主方案。</p><p class="note">若选择码头直达酒店共乘并提前到达，可把本段及后续景点整体提前约60分钟。</p><div class="fallback"><b>没有叫到车：</b>换用Uber或请酒店前台叫车，通常无需等固定班次。<span class="freq">即时叫车</span></div></article>
    <article class="event"><div class="time-row"><div class="time">15:10–16:15</div><span class="duration">约65分钟</span></div><h3>赤崁楼及周边</h3><p>以建筑和历史区域为主，不在纪念品店停太久。</p></article>
    <article class="event food"><div class="time-row"><div class="time">16:15–18:40</div><span class="duration">边走边吃</span></div><h3>永乐市场 → 国华街</h3><p>虾仁饭、米糕、碗粿、豆花分食。热门店售完即止，不必执着单一店家。</p></article>'''

new = '''    <article class="event"><div class="time-row"><div class="time">14:50–15:35</div><span class="duration">办卡手续</span></div><h3>中华电信台南服务中心｜办理台湾手机号预付卡</h3><p>到烟波放下行李后，优先去办1张带台湾手机号的预付卡。你们两个人共用1个台湾本地号码即可；另一人继续使用提前准备好的纯流量eSIM。</p><div class="steps"><div class="step"><div class="num">1</div><div><b>资料带齐</b>护照＋可作为第二证件的身份证件都随身带着，不要放在酒店行李里。</div></div><div class="step"><div class="num">2</div><div><b>明确说需求</b>要「预付卡／有台湾手机号码／可通话＋上网」，不要只办纯流量eSIM。</div></div><div class="step"><div class="num">3</div><div><b>现场确认号码可用</b>办完后当场确认能打电话、收短信，再离开门市。</div></div></div><div class="critical">这一段优先级高于赤崁楼。后面9/23包车、9/24山区叫车与住宿联系都更需要台湾本地号码。</div><div class="fallback"><b>交通延误：</b>若船班／9127D导致抵达台南明显变晚，先取消或压缩赤崁楼，优先在门店关门前把号码办好；如果当天最终赶不上，则9/22早上把办卡放在去安平之前。<span class="freq">Plan B：9/22早上</span></div></article>
    <article class="event transport"><div class="time-row"><div class="time">15:35–15:50</div><span class="duration">出租车</span></div><h3>中华电信 → 赤崁楼</h3><p>办完卡后直接叫车去赤崁楼；台南两人出行继续以出租车节省时间。</p><p class="note">若选择码头直达酒店共乘并提前到达，可把办卡和后续景点整体提前。</p><div class="fallback"><b>没有叫到车：</b>换用Uber或请门店／酒店协助叫车，通常无需等固定班次。<span class="freq">即时叫车</span></div></article>
    <article class="event"><div class="time-row"><div class="time">15:50–16:35</div><span class="duration">约45分钟</span></div><h3>赤崁楼及周边</h3><p>缩成精华版参观，以建筑和历史区域为主，不在纪念品店停太久。</p></article>
    <article class="event food"><div class="time-row"><div class="time">16:35–18:40</div><span class="duration">边走边吃</span></div><h3>永乐市场 → 国华街</h3><p>虾仁饭、米糕、碗粿、豆花分食。热门店售完即止，不必执着单一店家。</p></article>'''

if old not in s:
    raise RuntimeError('Target Day 3 timeline block not found; itinerary may have changed')

s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
