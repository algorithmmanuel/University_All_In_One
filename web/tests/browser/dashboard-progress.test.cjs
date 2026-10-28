// Real browser with intercepted synthetic responses; API projections tested separately.
const {test,after}=require('node:test');
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const WEB=process.env.EDUCYBER_E2E_WEB_URL||'http://127.0.0.1:3100';
let browser;
after(async()=>{if(browser)await browser.close()});
const overview={enrolled_count:4,completed_courses:1,courses:[
  {id:1,title:'Synthetic Python',total_lessons:3,completed_lessons:1,progress_percent:33,completed:false,next_lesson:{id:2,title:'Conditional logic'}},
  {id:2,title:'Completed course',total_lessons:3,completed_lessons:3,progress_percent:100,completed:true,next_lesson:null},
  {id:3,title:'Empty course',total_lessons:0,completed_lessons:0,progress_percent:0,completed:false,next_lesson:null}],
  recent_attempts:[{id:7,course_id:1,course_title:'Synthetic Python',score:2,total:5,percentage:40,submitted_at:'2026-10-28T10:00:00Z'}]};
async function setup(t,mobile=false){
  browser ||= await chromium.launch({channel:'chromium',headless:true,args:['--disable-dev-shm-usage']});
  const context=await browser.newContext({baseURL:WEB,reducedMotion:'reduce',viewport:mobile?{width:390,height:844}:{width:1280,height:800}});
  t.after(()=>context.close());
  await context.addInitScript(()=>{if(!sessionStorage.getItem('test_initialized')){sessionStorage.setItem('educyber_token','synthetic');sessionStorage.setItem('test_initialized','yes');}});
  const page=await context.newPage();
  return page;
}
async function mock(page,handler){
  await page.route('**/api/v1/**',async route=>{
    const path=new URL(route.request().url()).pathname;
    const json=(body,status=200)=>route.fulfill({status,contentType:'application/json',body:JSON.stringify(body)});
    if(await handler?.(path,json,route))return;
    if(path.endsWith('/dashboard'))return json({user:{full_name:'Synthetic learner',role:'student',is_approved:true}});
    if(path.endsWith('/games'))return json({games:[]});
    if(path.endsWith('/missions/progress'))return json({completed_missions:0,active_missions:0,available_missions:30,recent_missions:[]});
    if(path.endsWith('/learning/overview'))return json(overview);
    if(path.endsWith('/learning/enrollments'))return json({enrollments:[{id:1,title:'Synthetic Python',academy_id:'university'}]});
    if(path.endsWith('/options'))return json({available_count:20,presets:[5,10,20]});
    if(path.endsWith('/attempts'))return json({attempts:overview.recent_attempts});
    if(path.endsWith('/attempts/7'))return json({id:7,score:2,total:5,percentage:40,submitted_at:'2026-10-28T10:00:00Z',analysis:null});
    return json({});
  });
}
for(const mobile of [false,true])test('saved dashboard preview and assessment result deep link; mobile='+mobile,async t=>{
  const page=await setup(t,mobile);const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await mock(page);await page.goto('/dashboard');
  await page.getByText('4 enrolled course(s) · 1 completed',{exact:true}).waitFor();
  await page.getByText('1 of 3 lessons complete',{exact:true}).waitFor();
  assert.equal(await page.getByRole('link',{name:'Continue Synthetic Python',exact:true}).getAttribute('href'),'/learn?course=1#lesson-2');
  assert.equal(await page.getByRole('link',{name:'Practise Completed course',exact:true}).getAttribute('href'),'/assessments?course=2');
  await page.getByText('Lessons have not been published yet.',{exact:true}).waitFor();
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),'Mobile dashboard must fit viewport');
  await page.getByRole('link',{name:'Synthetic Python: 2/5 (40%)',exact:true}).click();
  await page.getByRole('heading',{name:'Saved result: 2/5 (40%)',exact:true}).waitFor();
  await page.waitForFunction(()=>document.activeElement?.textContent==='Saved result: 2/5 (40%)');
  await page.getByText('Topic evidence is unavailable for this historical attempt.',{exact:false}).waitFor();
  assert.deepEqual(errors,[]);
});

test('progress failure is retryable; empty data offers real next steps',async t=>{
  const page=await setup(t);let failed=true;
  await mock(page,async(path,json)=>{
    if(!path.endsWith('/learning/overview'))return false;
    await json(failed?{detail:'Unavailable'}:{enrolled_count:0,completed_courses:0,courses:[],recent_attempts:[]},failed?503:200);return true;
  });
  await page.goto('/dashboard');
  await page.getByRole('alert').filter({hasText:'Unable to load saved progress'}).waitFor();
  assert.equal(await page.getByText('0 enrolled course(s) · 0 completed',{exact:true}).count(),0);
  failed=false;await page.getByRole('button',{name:'Retry saved progress',exact:true}).click();
  await page.getByRole('link',{name:'Choose your first course',exact:true}).waitFor();
  await page.getByRole('link',{name:'Choose an assessment',exact:true}).waitFor();
  assert.equal(await page.getByRole('region',{name:'Your saved progress',exact:true}).getByRole('alert').count(),0);
});

test('teacher dashboard does not request student progress',async t=>{
  const page=await setup(t);let overviewRequests=0;
  await mock(page,async(path,json)=>{
    if(path.endsWith('/learning/overview')){overviewRequests++;await json({});return true;}
    if(path.endsWith('/dashboard')){await json({user:{full_name:'Synthetic teacher',role:'teacher',is_approved:false}});return true;}
    return false;
  });
  await page.goto('/dashboard');
  await page.getByRole('heading',{name:'Teacher approval pending',exact:true}).waitFor();
  assert.equal(overviewRequests,0);
  assert.equal(await page.getByRole('heading',{name:'Your saved progress',exact:true}).count(),0);
});

test('stalled dashboard logout clears local token within a bounded wait',async t=>{
  const page=await setup(t);let logoutRequests=0;
  await mock(page,async(path)=>{if(path.endsWith('/auth/logout')){logoutRequests++;return true;}return false;});
  await page.goto('/dashboard');
  await page.getByRole('heading',{name:'Your saved progress',exact:true}).waitFor();
  const started=Date.now();
  await page.getByRole('button',{name:'Sign out',exact:true}).click();
  await page.waitForURL('**/account',{timeout:10000});
  assert.equal(await page.evaluate(()=>sessionStorage.getItem('educyber_token')),null);
  assert.equal(logoutRequests,1);
  assert.ok(Date.now()-started<10000);
});
