const state={air:null,fruit:null,bed:null},visited=new Set(),comments=[];
let serial=0,active=null,anchor={x:50,y:50},draft=null,returnFocus=null;
const $=s=>document.querySelector(s),room=$('#room'),panel=$('#popup');
const names={air:'Temperature',fruit:'Welcome fruit',bed:'Preferred bed side'};
const value=k=>state[k]===null?'Explored · not set':k==='air'?(state.air==='default'?'Hotel default':state.air+' °C'):{yes:'Fruit platter',no:'No fruit platter',left:'Left side',right:'Right side'}[state[k]];
function update(){updateBed();document.querySelectorAll('[data-key]').forEach(b=>{const k=b.dataset.key;b.classList.toggle('visited',visited.has(k));b.classList.toggle('set',state[k]!==null);b.setAttribute('aria-expanded',String(active===k));b.querySelector('i').textContent=state[k]!==null?'✓':'＋';b.querySelector('small').textContent=visited.has(k)?value(k):'Click to set'});$('#fruit-art').style.opacity=state.fruit==='no'?'0':state.fruit==='yes'?'1':'.45';$('#status').textContent=Object.values(state).filter(x=>x!==null).length+' preferences · '+comments.length+' comments';$('#pins').replaceChildren();comments.forEach((c,i)=>{const b=document.createElement('button');b.className='pin';b.style.left=c.x+'%';b.style.top=c.y+'%';b.textContent=i+1;b.title=c.text;b.setAttribute('aria-label','Comment '+(i+1)+'：'+c.text);b.setAttribute('aria-expanded',String(active==='comment'&&draft?.id===c.id));b.onclick=e=>{e.stopPropagation();openComment(c.x,c.y,c,b)};$('#pins').append(b)})}
function position(){const w=room.clientWidth,h=room.clientHeight,pw=panel.offsetWidth,ph=panel.offsetHeight,x=anchor.x*w/100,y=anchor.y*h/100;let left=x+22;if(left+pw>w-8)left=x-pw-22;panel.style.left=Math.max(8,Math.min(left,w-pw-8))+'px';panel.style.top=Math.max(8,Math.min(y-ph/2,h-ph-8))+'px'}
function close(){panel.hidden=true;$('#draft-pin').hidden=true;active=null;draft=null;update();if(returnFocus?.isConnected)returnFocus.focus();else room.focus()}
function show(){panel.hidden=false;position();update();$('#close').focus()}
function drawPreference(){
 const isAir=active==='air';
 $('#editor').innerHTML='<h2 id="popup-title">'+names[active]+'</h2><p class="description">'+(isAir?'Scroll up or down to set the arrival temperature.':'A warm welcome can also mean less. Choose what feels right.')+'</p>'+
 (isAir?'<div class="wheel-shell"><div class="wheel-highlight"></div><div id="temp-wheel" role="listbox" tabindex="0" aria-label="Arrival temperature" aria-orientation="vertical">'+Array.from({length:11},(_,i)=>'<div role="option" id="temp-'+(i+18)+'" data-degree="'+(i+18)+'" aria-selected="'+(state.air===i+18)+'">'+(i+18)+' <small>°C</small></div>').join('')+'</div></div><p class="wheel-note" id="wheel-note"></p>':'')+
 '<div class="choices">'+(isAir?[['default','Hotel default'],['null','Not specified']]:[['yes','Seasonal fruit platter'],['no','No fruit platter'],['null','Not specified']]).map(([v,t])=>'<button class="choice" data-value="'+v+'" aria-pressed="'+(String(state[active])===v)+'">'+t+'</button>').join('')+'</div><button class="primary" id="done">Done</button>';
 document.querySelectorAll('[data-value]').forEach(b=>b.onclick=()=>{state[active]=b.dataset.value==='null'?null:b.dataset.value;drawPreference();update();position()});
 $('#done').onclick=close;
 if(isAir)setupWheel();
}
function setupWheel(){
 const wheel=$('#temp-wheel'),note=$('#wheel-note');let lastTop=(typeof state.air==='number'?state.air:22)-18;lastTop*=44;
 requestAnimationFrame(()=>{if(wheel.isConnected)wheel.scrollTop=lastTop});
 const paint=()=>{wheel.querySelectorAll('[data-degree]').forEach(o=>o.setAttribute('aria-selected',String(Number(o.dataset.degree)===state.air)));note.textContent=typeof state.air==='number'?'Selected: '+state.air+' °C':'Scroll or click a number to choose';if(typeof state.air==='number')wheel.setAttribute('aria-activedescendant','temp-'+state.air)};
 const commit=n=>{state.air=Math.min(28,Math.max(18,n));visited.add('air');update();paint();document.querySelectorAll('[data-value]').forEach(b=>b.setAttribute('aria-pressed','false'))};
 wheel.addEventListener('scroll',()=>{if(!wheel.isConnected)return;if(Math.abs(wheel.scrollTop-lastTop)<1)return;lastTop=wheel.scrollTop;commit(18+Math.round(lastTop/44))});
 wheel.querySelectorAll('[data-degree]').forEach(o=>o.onclick=()=>{commit(Number(o.dataset.degree));wheel.scrollTo({top:(state.air-18)*44,behavior:'smooth'})});
 wheel.onkeydown=e=>{const n=typeof state.air==='number'?state.air:22;let next;if(e.key==='ArrowUp')next=n-1;else if(e.key==='ArrowDown')next=n+1;else if(e.key==='Home')next=18;else if(e.key==='End')next=28;else return;e.preventDefault();commit(next);wheel.scrollTop=(state.air-18)*44};
 paint();
}
document.querySelectorAll('[data-key]').forEach(b=>b.onclick=e=>{e.stopPropagation();draft=null;$('#draft-pin').hidden=true;active=b.dataset.key;visited.add(active);returnFocus=b;const r=room.getBoundingClientRect(),br=b.getBoundingClientRect();anchor={x:(br.left+br.width/2-r.left)/r.width*100,y:(br.top+br.height/2-r.top)/r.height*100};drawPreference();show()});
function openComment(x,y,existing=null,origin=room){active='comment';returnFocus=origin;draft={id:existing?.id??null,x,y};anchor={x,y};$('#draft-pin').hidden=!!existing;$('#draft-pin').style.left=x+'%';$('#draft-pin').style.top=y+'%';$('#editor').innerHTML='<h2 id="popup-title">'+(existing?'Edit comment':'Leave a note here')+'</h2><p class="description">For example: please leave a power adapter here.</p><label for="comment-text" class="description">Comments</label><textarea id="comment-text" maxlength="500" placeholder="How should we prepare this spot?"></textarea><div class="meta"><span id="char-count"></span><button id="delete-comment" class="delete">'+(existing?'Delete comment':'Cancel')+'</button></div><button id="save-comment" class="primary">Save comment</button>';$('#comment-text').value=existing?.text??'';const count=()=>{$('#char-count').textContent=$('#comment-text').value.length+' / 500';$('#save-comment').disabled=!$('#comment-text').value.trim()};$('#comment-text').oninput=count;count();$('#save-comment').onclick=()=>{const text=$('#comment-text').value.trim();if(!text)return;if(draft.id!==null){const c=comments.find(c=>c.id===draft.id);if(c)c.text=text}else comments.push({...draft,id:++serial,text});close()};$('#delete-comment').onclick=()=>{if(draft.id!==null){const i=comments.findIndex(c=>c.id===draft.id);if(i>=0)comments.splice(i,1)}close()};show();$('#comment-text').focus()}
function updateBed(){
 const box=$('#bed-control'),slider=$('#bed-slider');box.classList.toggle('visited',visited.has('bed'));box.classList.toggle('set',state.bed!==null);
 $('#bed-status').textContent=state.bed?value('bed'):'Drag the block left or right';
 $('#bed-clear').hidden=state.bed===null;
 slider.setAttribute('aria-valuetext',state.bed?value('bed'):'Not selected');
}
const bedSlider=$('#bed-slider'),bedBlock=$('#bed-block');
function moveBed(v){bedSlider.value=v;bedBlock.style.left='calc('+v+'% - '+(v/100*72)+'px)';bedBlock.textContent=state.bed===null?'DRAG ↔':state.bed==='left'?'LEFT':'RIGHT'}
bedSlider.onpointerdown=()=>{visited.add('bed');updateBed()};
bedSlider.oninput=()=>{state.bed=Number(bedSlider.value)<50?'left':'right';visited.add('bed');moveBed(Number(bedSlider.value));update()};
bedSlider.onchange=()=>moveBed(state.bed==='left'?0:100);
bedSlider.onkeydown=e=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(e.key))return;e.preventDefault();state.bed=['ArrowLeft','Home'].includes(e.key)?'left':'right';visited.add('bed');moveBed(state.bed==='left'?0:100);update()};
$('#bed-clear').onclick=()=>{state.bed=null;moveBed(50);update()};
moveBed(50);

room.addEventListener('click',e=>{if(e.target.closest('button,#popup,.bed-control'))return;const r=room.getBoundingClientRect();openComment(Math.min(98,Math.max(2,(e.clientX-r.left)/r.width*100)),Math.min(98,Math.max(2,(e.clientY-r.top)/r.height*100)))});$('#add').onclick=()=>openComment(50,70,null,$('#add'));$('#close').onclick=close;document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!panel.hidden)close()});window.addEventListener('resize',()=>{if(!panel.hidden)position()});update();
if(document.modelContext?.registerTool){try{Promise.resolve(document.modelContext.registerTool({name:'get_room_annotations',description:'Read simulated room preferences, visited hotspots, and spatial comments. Viewing is not a service request.',annotations:{readOnlyHint:true},inputSchema:{type:'object',properties:{},additionalProperties:false},execute:async()=>({preferences:{...state},visited:[...visited],comments:comments.map(c=>({...c}))})})).catch(()=>{});}catch{}}
