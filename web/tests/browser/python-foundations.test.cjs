// Browser interaction fixture; backend behavior is tested by test_python_foundations.py.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const WEB=process.env.EDUCYBER_E2E_WEB_URL||'http://127.0.0.1:3100';
for(const mobile of [false,true])test('Python guided practice, retry and saved progress; mobile='+mobile,async t=>{
  const browser=await chromium.launch({channel:'chromium',headless:true,args:['--disable-dev-shm-usage']});
  t.after(()=>browser.close());
  const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1280,height:720},reducedMotion:'reduce'});
  await context.addInitScript(()=>sessionStorage.setItem('educyber_token','synthetic-learner'));
  const page=await context.newPage();let checks=0,completed=false;
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  await page.route('**/api/v1/**',async route=>{
    const request=route.request(),path=new URL(request.url()).pathname;
    const json=body=>route.fulfill({contentType:'application/json',body:JSON.stringify(body)});
    const course={id:1,academy_id:'university',title:'Introduction to Python',description:'Python foundations',lesson_count:1};
    if(path.endsWith('/learning/catalog'))return json({courses:[course]});
    if(path.endsWith('/learning/enrollments'))return json({enrollments:[{...course,total_lessons:1,completed_lessons:completed?1:0,progress_percent:completed?100:0}]});
    if(path.endsWith('/practice')){
      checks++;const body=request.postDataJSON();assert.equal(body.exercise_id,'trace');
      assert.equal(request.headers().authorization,'Bearer synthetic-learner');
      return json({exercise_id:'trace',correct:body.option_index===1,explanation:body.option_index===1?'4 + 3 gives 7.':'4 is the starting value; add 3.'});
    }
    if(path.endsWith('/complete')){completed=true;return json({lesson_id:1,completed:true});}
    return json({course,lessons:[{id:1,title:'Variables and data types',position:1,completed,content:'',learning_guide:{
      revision:'python-foundations-v1',objectives:[{id:'PY-V1',text:'Trace assignment in order.'}],
      sections:[{title:'A value can change',body:'Read top to bottom.',code:'points = 4\npoints = points + 3\nprint(points)',output:'7'}],
      exercises:[{id:'trace',objective:'PY-V1',prompt:'Predict the final output.',code:'points = 4\npoints = points + 3\nprint(points)',options:['4','7','3']}]
    }}]});
  });
  await page.goto(WEB+'/learn');
  await page.getByRole('button',{name:'Continue learning →'}).click();
  await page.getByRole('heading',{name:'What you will learn'}).waitFor();
  const heading=page.locator('.activity-heading');
  assert.equal(await heading.evaluate(el=>el===document.activeElement),true);
  const check=page.getByRole('button',{name:'Check answer',exact:true});
  assert.equal(await check.isDisabled(),true);
  await page.getByRole('radio',{name:'4',exact:true}).check();await check.click();
  await page.getByText('4 is the starting value; add 3.',{exact:false}).waitFor();
  assert.equal(completed,false,'Practice cannot complete a lesson');
  await page.getByRole('radio',{name:'7',exact:true}).check();await check.click();
  await page.getByText('4 + 3 gives 7.',{exact:false}).waitFor();
  assert.equal(checks,2);
  assert.equal(await check.evaluate(el=>el===document.activeElement),true,'Feedback must keep keyboard focus');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),true);
  await page.getByRole('button',{name:'Mark lesson complete'}).click();
  await page.getByRole('button',{name:'Completed ✓'}).waitFor();
  assert.equal(completed,true);assert.deepEqual(errors,[]);
});
