const {test,after}=require('node:test');
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const WEB=process.env.EDUCYBER_E2E_WEB_URL||'http://127.0.0.1:3100';let browser;
after(async()=>{if(browser)await browser.close()});
async function setup(t,mobile=false,signedIn=true){
  browser ||= await chromium.launch({headless:true,args:['--disable-dev-shm-usage']});
  const context=await browser.newContext({baseURL:WEB,reducedMotion:'reduce',viewport:mobile?{width:320,height:780}:{width:1280,height:800}});
  t.after(()=>context.close());
  if(signedIn)await context.addInitScript(()=>{if(!sessionStorage.getItem('initialized')){sessionStorage.setItem('educyber_token','synthetic');sessionStorage.setItem('initialized','yes');}});
  return context.newPage();
}
const overview={enrolled_count:0,completed_courses:0,courses:[],recent_attempts:[]};
const mission={run_id:9,mission_id:'phishing-investigation',title:'Saved Scholarship Mission',score:20,max_score:45,step_index:3,step_count:3,completed:true,step:null,last_feedback:'Saved final reasoning',learning:null,
 decision_recap:[{stage:1,points:5,feedback:'Original saved stage explanation',next_step:'Review this saved explanation and the mission briefing before replaying.'},{stage:2,points:null,feedback:'Legacy detail',next_step:'Detailed scoring evidence is unavailable.'}]};
async function mock(page,handler){
 await page.route('**/api/v1/**',async route=>{
  const path=new URL(route.request().url()).pathname;
  const json=(body,status=200)=>route.fulfill({status,contentType:'application/json',body:JSON.stringify(body)});
  if(await handler?.(path,json,route))return;
  if(path.endsWith('/dashboard'))return json({user:{full_name:'Synthetic Learner',role:'student',is_approved:true}});
  if(path.endsWith('/learning/overview'))return json(overview);
  if(path.endsWith('/missions/progress'))return json({completed_missions:1,active_missions:0,available_missions:30,recent_missions:[{...mission,completed_stages:3,total_stages:3}]});
  if(path.endsWith('/games'))return json({games:[]});
  if(path==='/api/v1/missions')return json({missions:[]});
  if(path.endsWith('/missions/history'))return json({runs:[{id:9,title:mission.title,score:20,max_score:45,completed:true,created_at:'2026-10-28T10:00:00Z'}],next_before_id:9});
  if(path.endsWith('/missions/runs/9')||path.endsWith('/missions/runs/7'))return json(mission);
  if(path.endsWith('/learning/catalog'))return json({courses:[]});
  if(path.endsWith('/learning/enrollments'))return json({enrollments:[]});
  return json({});
 });
}
for(const mobile of [false,true])test('mission saved progress, recap, older history and focus; mobile='+mobile,async t=>{
 const page=await setup(t,mobile);const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await mock(page,async(path,json,route)=>{
  if(path.endsWith('/missions/history')&&new URL(route.request().url()).searchParams.has('before_id')){await json({runs:[{id:7,title:'Older mission',score:10,max_score:45,completed:true,created_at:'2026-10-27T10:00:00Z'}],next_before_id:null});return true;}
  return false;
 });
 await page.goto('/dashboard');
 await page.getByText('1 of 30 missions completed at least once · 0 latest attempts in progress',{exact:true}).waitFor();
 await page.getByRole('link',{name:'Review saved mission result: Saved Scholarship Mission',exact:true}).click();
 await page.getByRole('heading',{name:'Saved decisions and next steps',exact:true}).waitFor();
 await page.waitForFunction(()=>document.activeElement?.textContent==='Mission workspace');
 await page.getByText('Original saved stage explanation',{exact:true}).waitFor();
 await page.getByRole('heading',{name:'Stage 2 · Detailed scoring unavailable',exact:true}).waitFor();
 await page.getByRole('button',{name:'Load older mission attempts',exact:true}).click();
 await page.getByRole('button',{name:'View saved result 7',exact:true}).waitFor();
 assert.equal(await page.getByRole('button',{name:'Load older mission attempts',exact:true}).count(),0);
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 assert.deepEqual(errors,[]);
});

for(const pageName of ['learn','assessments'])test('loading failure recovers without inventing empty progress: '+pageName,async t=>{
 const page=await setup(t,true);let failed=true;
 await mock(page,async(path,json)=>{
  if(path.endsWith('/learning/enrollments')&&failed){await json({detail:'Synthetic unavailable'},503);return true;}return false;
 });
 await page.goto('/'+pageName);
 await page.getByRole('alert').filter({hasText:'Synthetic unavailable'}).waitFor();
 const empty=pageName==='learn'?'You have not enrolled in a course yet.':'Enroll in a course first at';
 assert.equal(await page.getByText(empty,{exact:false}).count(),0);
 failed=false;
 await page.getByRole('button',{name:pageName==='learn'?'Retry learning data':'Retry enrolled courses',exact:true}).click();
 await page.getByText(empty,{exact:false}).waitFor();
});

function contrast(a,b){
 const luminance=c=>{const rgb=c.match(/[\d.]+/g).slice(0,3).map(Number).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4;});return rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722;};
 const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);
}
for(const mobile of [false,true])test('onboarding confirmation, focus, dark error contrast and sign-in; mobile='+mobile,async t=>{
 const page=await setup(t,mobile,false);let registrations=0,login;
 await mock(page,async(path,json,route)=>{
  if(path.endsWith('/auth/register')){registrations++;await json({message:'Account created'});return true;}
  if(path.endsWith('/auth/login')){login=route.request().postDataJSON();await json({access_token:'synthetic'});return true;}return false;
 });
 await page.goto('/account');
 await page.getByLabel('Full name',{exact:true}).fill('Synthetic Learner');
 await page.getByLabel('Date of birth',{exact:true}).fill('1991-01-01');
 await page.getByLabel('Email',{exact:true}).fill('LEARNER@EXAMPLE.INVALID');
 await page.getByLabel('Password',{exact:true}).fill('Synthetic-learning-pass');
 await page.getByLabel('Confirm password',{exact:true}).fill('Different-learning-pass');
 await page.getByRole('button',{name:'Create account',exact:true}).click();
 const error=page.getByRole('alert').filter({hasText:'Passwords do not match'});await error.waitFor();
 await page.waitForFunction(()=>document.activeElement?.textContent?.startsWith('Passwords do not match'));
 assert.equal(registrations,0);
 const colors=await error.evaluate(el=>({fg:getComputedStyle(el).color,bg:getComputedStyle(document.body).backgroundColor}));
 assert.ok(contrast(colors.fg,colors.bg)>=4.5,'Dark-theme error must meet ordinary text contrast');
 await page.getByLabel('Confirm password',{exact:true}).fill('Synthetic-learning-pass');
 await page.getByRole('button',{name:'Create account',exact:true}).click();
 await page.getByRole('heading',{name:'Welcome back',exact:true}).waitFor();
 await page.waitForFunction(()=>document.activeElement?.textContent?.includes('Please sign in using the exact password'));
 assert.equal(registrations,1);assert.equal(await page.getByLabel('Password',{exact:true}).inputValue(),'');
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.getByLabel('Password',{exact:true}).fill('Synthetic-learning-pass');
 await page.getByRole('button',{name:'Sign in',exact:true}).last().click();await page.waitForURL('**/dashboard');
 assert.equal(login.email,'learner@example.invalid');assert.equal(login.password,'Synthetic-learning-pass');
 assert.equal(login.confirmPassword,undefined);
});

test('older assessment history can be loaded and reopened without losing saved scores',async t=>{
 const page=await setup(t,true);
 const attempt=id=>({id,score:1,total:1,percentage:100,submitted_at:'2026-10-28T10:00:00Z'});
 await mock(page,async(path,json,route)=>{
  if(path.endsWith('/learning/enrollments')){await json({enrollments:[{id:1,title:'Synthetic course'}]});return true;}
  if(path.endsWith('/options')){await json({available_count:20});return true;}
  if(path.endsWith('/attempts')){await json(new URL(route.request().url()).searchParams.has('before_id')?{attempts:[attempt(81),attempt(80)],next_before_id:null}:{attempts:Array.from({length:20},(_,i)=>attempt(101-i)),next_before_id:82});return true;}
  if(path.endsWith('/attempts/80')){await json({...attempt(80),analysis:null});return true;}return false;
 });
 await page.goto('/assessments');await page.getByRole('button',{name:'Synthetic course',exact:true}).click();
 await page.getByRole('button',{name:'Load older assessment attempts',exact:true}).click();
 await page.getByRole('button',{name:'View result 80',exact:true}).click();
 await page.getByRole('heading',{name:'Saved result: 1/1 (100%)',exact:true}).waitFor();
 assert.equal(await page.getByRole('button',{name:'Load older assessment attempts',exact:true}).count(),0);
 assert.equal(await page.getByRole('button',{name:/^View result \d+$/}).count(),22);
});
