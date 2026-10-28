// Real browser, synthetic intercepted API: pairs with backend snapshot HTTP tests.
const {test,after}=require('node:test');
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const WEB=process.env.EDUCYBER_E2E_WEB_URL||'http://127.0.0.1:3100';
let browser;
after(async()=>{if(browser)await browser.close()});
const analysis={version:1,curriculum_revision:'synthetic-v1',unmapped_count:0,
  evidence_note:'One practice attempt, not proof of mastery.',
  topics:[['A','Trace assignment',2,2,'strength_in_this_attempt'],['B','Trace conditions',0,2,'revisit'],['C','Trace loops',1,1,'limited_evidence'],['D','Compare values',0,0,'not_assessed']].map(([id,objective,correct,total,status])=>({
    objective_id:id,objective,correct,total,status,percentage:total?Math.round(100*correct/total):null,
    lesson_id:1,lesson_title:'Worked examples',recommendation:'Review this lesson and try another example.'})),
  feedback:[{question_id:1,prompt:'What value prints?',options:['4','7'],correct_index:1,selected_index:0,correct:false,explanation:'Assignment replaces the old value.',objective_id:'A'}]};
async function setup(t,mobile){
  browser ||= await chromium.launch({channel:'chromium',headless:true,args:['--disable-dev-shm-usage']});
  const context=await browser.newContext({baseURL:WEB,reducedMotion:'reduce',viewport:mobile?{width:390,height:844}:{width:1280,height:800}});
  t.after(()=>context.close());
  await context.addInitScript(()=>sessionStorage.setItem('educyber_token','synthetic'));
  return context.newPage();
}
for(const mobile of [false,true])test('topic results, saved reopening and legacy limits; mobile='+mobile,async t=>{
  const page=await setup(t,mobile);
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const history=[{id:7,score:1,total:1,percentage:100,submitted_at:'2026-10-26T12:00:00Z'}];
  let denyDetail=false;
  await page.route('**/api/v1/**',async route=>{
    const path=new URL(route.request().url()).pathname;
    const json=(body,status=200)=>route.fulfill({status,contentType:'application/json',body:JSON.stringify(body)});
    if(path.endsWith('/learning/enrollments'))return json({enrollments:[{id:1,title:'Synthetic course',academy_id:'cyber'}]});
    if(path.endsWith('/options'))return json({available_count:20,presets:[5,10,20]});
    if(path.endsWith('/attempts'))return json({attempts:history});
    if(path.endsWith('/attempts/7'))return json({...history.find(a=>a.id===7),analysis:null});
    if(path.endsWith('/attempts/8'))return denyDetail?json({detail:'Attempt not found'},404):json({...history.find(a=>a.id===8),analysis});
    if(path.endsWith('/submit')){
      history.unshift({id:8,score:3,total:5,percentage:60,submitted_at:'2026-10-28T12:00:00Z'});
      return json({attempt_id:8,score:3,total:5,percentage:60,analysis,feedback:[]},201);
    }
    return json({question_count:5,questions:Array.from({length:5},(_,i)=>({id:i+1,prompt:'Scenario '+i,options:['A','B']}))});
  });
  async function choose(){await page.getByRole('button',{name:'Synthetic course',exact:true}).click();}
  await page.goto('/assessments');await choose();
  await page.getByRole('button',{name:'View result 7',exact:true}).click();
  await page.getByText('Topic evidence is unavailable for this historical attempt.',{exact:false}).waitFor();
  await page.getByRole('heading',{name:'Saved result: 1/1 (100%)'}).waitFor();
  await page.getByRole('radio',{name:'Quick (5 questions)',exact:true}).check();
  await page.getByRole('button',{name:'Start 5-question assessment'}).click();
  await page.locator('form fieldset').nth(4).waitFor();
  assert.equal(await page.locator('form fieldset').count(),5);
  for(const field of await page.locator('form fieldset').all())await field.getByRole('radio').first().check();
  await page.getByRole('button',{name:'Submit assessment',exact:true}).click();
  await page.getByRole('heading',{name:'Topic results and next steps',exact:true}).waitFor();
  for(const text of ['Strength in this attempt','Revisit this objective','Limited evidence','Not assessed'])await page.getByText(text,{exact:true}).waitFor();
  await page.getByText('No questions sampled',{exact:true}).waitFor();
  const link=page.getByRole('link',{name:'Review: Worked examples'}).first();
  assert.equal(await link.getAttribute('href'),'/learn?course=1#lesson-1');
  await page.getByText('Review answers and explanations',{exact:true}).click();
  await page.getByText('Your answer: 4',{exact:true}).waitFor();
  await page.getByText('Correct answer: 7',{exact:true}).waitFor();
  await page.reload();await choose();
  denyDetail=true;
  await page.getByRole('button',{name:'View result 8',exact:true}).click();
  await page.getByRole('alert').filter({hasText:'Attempt not found'}).waitFor();
  denyDetail=false;
  await page.getByRole('button',{name:'View result 8',exact:true}).click();
  await page.getByRole('heading',{name:'Saved result: 3/5 (60%)'}).waitFor();
  await page.waitForFunction(()=>document.activeElement?.textContent==='Saved result: 3/5 (60%)');
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
  assert.deepEqual(errors,[]);
});

test('lesson recommendation opens the returned lesson and does not refocus on completion',async t=>{
  const page=await setup(t,true);
  let completed=false;
  await page.route('**/api/v1/learning/**',async route=>{
    const path=new URL(route.request().url()).pathname;
    const json=body=>route.fulfill({contentType:'application/json',body:JSON.stringify(body)});
    if(path.endsWith('/catalog'))return json({courses:[]});
    if(path.endsWith('/enrollments'))return json({enrollments:[{id:1,title:'Synthetic course',total_lessons:1,completed_lessons:Number(completed),progress_percent:completed?100:0}]});
    if(path.endsWith('/complete')){completed=true;return json({});}
    return json({course:{id:1,title:'Synthetic course'},lessons:[{id:1,title:'Worked examples',content:'Trace each step.',position:1,completed}]});
  });
  await page.goto('/learn?course=1#lesson-1');
  await page.getByRole('heading',{name:'Worked examples',exact:true}).waitFor();
  await page.waitForFunction(()=>document.activeElement?.id==='lesson-1');
  await page.getByRole('button',{name:'Mark lesson complete'}).click();
  await page.getByRole('button',{name:'Completed ✓',exact:true}).waitFor();
  assert.notEqual(await page.evaluate(()=>document.activeElement?.id),'lesson-1');
});
