const STORAGE_KEY='il.progress.nvidia.quest';
const COURSES=[
{id:1,title:'Generative AI Explained',phase:1,hours:2,xp:60,url:'https://lnkd.in/gBb3peXi'},
{id:2,title:'Building A Brain in 10 Minutes',phase:1,hours:0.2,xp:20,url:'https://lnkd.in/gCaA-XKp'},
{id:3,title:'Agentic AI Explained',phase:1,hours:1,xp:40,url:'https://lnkd.in/guBtU3-k'},
{id:4,title:"A Beginner's Guide to Autonomous Robots",phase:1,hours:1,xp:40,url:'https://lnkd.in/g5sVKrWu'},
{id:5,title:'Data Science Workflows with Zero Code Changes',phase:2,hours:1,xp:50,url:'https://lnkd.in/gF7eVk2V'},
{id:6,title:'NVIDIA Tools for Generative AI in Digital Health',phase:2,hours:2,xp:60,url:'https://lnkd.in/gaMUhSVR'},
{id:7,title:'AI Infrastructure and Operations Fundamentals',phase:2,hours:8,xp:250,url:'https://lnkd.in/gKTS6uMS'},
{id:8,title:'An Introduction to Developing With NVIDIA Omniverse',phase:2,hours:2,xp:60,url:'https://lnkd.in/gmS-kc3p'},
{id:9,title:'Getting Started with AI on Jetson Nano',phase:3,hours:8,xp:250,url:'https://lnkd.in/gnmrhBJm'},
{id:10,title:'Building RAG Agents with LLMs',phase:3,hours:8,xp:250,url:'https://lnkd.in/gcK2ZJ4a'},
];
const PHASES={1:'Phase 1 · Foundations (Weeks 1–3)',2:'Phase 2 · Applied skills (Weeks 4–7)',3:'Phase 3 · Advanced (Weeks 8–10)'};
const LEVELS=[{min:0,name:'Recruit'},{min:100,name:'Cadet'},{min:250,name:'Specialist'},{min:450,name:'Operator'},{min:700,name:'Architect'},{min:950,name:'AI Ranger'},{min:1140,name:'NVIDIA Master'}];
const MAX_XP=COURSES.reduce((s,c)=>s+c.xp,0);
const BADGES=[
{id:'first',icon:'🎯',name:'First Steps',desc:'Complete your first course',test:s=>Object.keys(s.completed).length>=1},
{id:'found',icon:'🧠',name:'Foundations',desc:'Finish all Phase 1 courses',test:s=>[1,2,3,4].every(i=>s.completed[i])},
{id:'half',icon:'⚡',name:'Halfway Hero',desc:'Complete 5 courses',test:s=>Object.keys(s.completed).length>=5},
{id:'deep',icon:'💎',name:'Deep Diver',desc:'Finish all 8-hour courses',test:s=>[7,9,10].every(i=>s.completed[i])},
{id:'all',icon:'🏆',name:'Completionist',desc:'Complete all 10 courses',test:s=>Object.keys(s.completed).length>=10},
];
function today(){return new Date().toISOString().slice(0,10)}
function load(){
  let s={completed:{},streak:{count:0,last:null},unlocked:[]};
  try{let raw=JSON.parse(localStorage.getItem(STORAGE_KEY)||'null');
  if(!raw){const legacy=JSON.parse(localStorage.getItem('il-nvidia-quest-v1')||'null');if(legacy){raw=legacy;localStorage.setItem(STORAGE_KEY,JSON.stringify(legacy));}}
  if(raw)s={...s,...raw,completed:raw.completed||{},streak:raw.streak||s.streak,unlocked:raw.unlocked||[]}}catch(e){}
  return s;
}
let state=load();
function save(){localStorage.setItem(STORAGE_KEY,JSON.stringify(state))}
function xpTotal(){return COURSES.reduce((s,c)=>s+(state.completed[c.id]?c.xp:0),0)}
function levelName(xp){let n=LEVELS[0].name;for(const L of LEVELS){if(xp>=L.min)n=L.name}return n}
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2200)}
function confettiBurst(){
  const c=document.getElementById('confetti'),ctx=c.getContext('2d');
  c.width=innerWidth;c.height=innerHeight;
  const parts=Array.from({length:80},()=>({x:Math.random()*c.width,y:-20-Math.random()*c.height*.2,v:2+Math.random()*4,r:Math.random()*Math.PI,vr:(Math.random()-.5)*.2,col:`hsl(${Math.random()*60+140},70%,60%)`,s:3+Math.random()*4}));
  let frames=0;
  (function tick(){
    ctx.clearRect(0,0,c.width,c.height);
    parts.forEach(p=>{p.y+=p.v;p.x+=Math.sin(p.r)*1.2;p.r+=p.vr;ctx.fillStyle=p.col;ctx.fillRect(p.x,p.y,p.s,p.s*0.6)});
    if(++frames<90)requestAnimationFrame(tick);else ctx.clearRect(0,0,c.width,c.height);
  })();
}
function bumpStreak(){
  const d=today();
  if(state.streak.last===d)return;
  const y=new Date();y.setDate(y.getDate()-1);
  const ymd=y.toISOString().slice(0,10);
  state.streak.count=(state.streak.last===ymd)?state.streak.count+1:1;
  state.streak.last=d;
}
function toggle(id){
  const before=xpTotal();
  if(state.completed[id]){delete state.completed[id]}
  else{state.completed[id]=true;bumpStreak();confettiBurst()}
  const after=xpTotal();
  BADGES.forEach(b=>{if(b.test(state)&&!state.unlocked.includes(b.id)){state.unlocked.push(b.id);toast(b.icon+' '+b.name)}});
  if(levelName(after)!==levelName(before)&&after>before)toast('Rank up · '+levelName(after));
  if(after===MAX_XP)toast('🏆 Quest complete');
  save();render();
}
function render(){
  const xp=xpTotal();
  document.getElementById('xp').textContent=xp+'/'+MAX_XP;
  document.getElementById('lvl').textContent=levelName(xp);
  document.getElementById('done').textContent=Object.keys(state.completed).length+'/10';
  document.getElementById('streak').textContent=String(state.streak.count||0);
  document.getElementById('xpbar').style.width=((xp/MAX_XP)*100).toFixed(1)+'%';
  const next=COURSES.find(c=>!state.completed[c.id]);
  const root=document.getElementById('phases');root.innerHTML='';
  [1,2,3].forEach(ph=>{
    const sec=document.createElement('div');sec.className='phase';
    sec.innerHTML='<h2>'+PHASES[ph]+'</h2>';
    COURSES.filter(c=>c.phase===ph).forEach(c=>{
      const done=!!state.completed[c.id];
      const div=document.createElement('div');
      div.className='card'+(done?' done':'')+(next&&next.id===c.id?' next':'');
      div.innerHTML='<div style="flex:1"><h3>'+(done?'✓ ':'')+c.title+'</h3><p class="meta">'+c.xp+' XP · ~'+c.hours+' h'+(next&&next.id===c.id?' · START HERE':'')+'</p><a href="'+c.url+'" target="_blank" rel="noopener">Open course ↗</a></div><button class="'+(done?'ghost':'primary')+'" type="button">'+(done?'Undo':'Mark complete')+'</button>';
      div.querySelector('button').onclick=()=>toggle(c.id);
      sec.appendChild(div);
    });
    root.appendChild(sec);
  });
  const bg=document.getElementById('badges');bg.innerHTML='';
  BADGES.forEach(b=>{
    const on=state.unlocked.includes(b.id)||b.test(state);
    const el=document.createElement('span');el.className='badge'+(on?' on':'');
    el.title=b.desc;el.textContent=b.icon+' '+b.name;bg.appendChild(el);
  });
}
document.getElementById('reset').onclick=()=>{if(confirm('Reset all Quest progress on this browser?')){state={completed:{},streak:{count:0,last:null},unlocked:[]};save();render()}};
render();
