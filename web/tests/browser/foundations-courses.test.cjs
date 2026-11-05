// Real browser interaction with synthetic API responses, including a pending reply.
// Backend content/authorization/grading is covered by test_foundations_courses.py.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const WEB=process.env.EDUCYBER_E2E_WEB_URL||'http://127.0.0.1:3100';
const courses=[
  {id:1,academy_id:'cyber',title:'Cyber Safety Foundations',lesson:'Recognising phishing',revision:'cyber-foundations-v1',
   objective:'Verify a request independently.',prompt:'Which route gives an independent check?',
   options:['Use only the number in the message','Open the verified school portal'],
   feedback:['The message may control that number.','Correct. You used an independent route.']},
  {id:2,academy_id:'secondary',title:'Digital Citizenship Essentials',lesson:'Your digital footprint',revision:'digital-citizenship-v1',
   objective:'Choose an audience and check consent.',prompt:'What should happen before publishing the group photo?',
   options:['Post it without asking','Check permission and unnecessary identifying details'],
   feedback:['Taking the photo does not settle permission to publish.','Correct. Check consent and limit unnecessary exposure.']},
];
for(const course of courses)for(const mobile of [false,true]){
  test(course.title+' practice preserves focus and prevents duplicate checks; mobile='+mobile,async t=>{
    const browser=await chromium.launch({channel:'chromium',headless:true,args:['--disable-dev-shm-usage']});
    t.after(()=>browser.close());
    const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1280,height:720},reducedMotion:'reduce'});
    await context.addInitScript(()=>sessionStorage.setItem('educyber_token','synthetic-foundations-user'));
    const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
    let completed=false,checks=0,releaseResponse;
    const pending=new Promise(resolve=>{releaseResponse=resolve;});
    await page.route('**/api/v1/**',async route=>{
      const request=route.request(),path=new URL(request.url()).pathname;
      const json=body=>route.fulfill({contentType:'application/json',body:JSON.stringify(body)});
      if(path.endsWith('/learning/catalog'))return json({courses:[{...course,lesson_count:1}]});
      if(path.endsWith('/learning/enrollments'))return json({enrollments:[{...course,total_lessons:1,completed_lessons:completed?1:0,progress_percent:completed?100:0}]});
      if(path.endsWith('/practice')){
        checks++;const body=request.postDataJSON();
        assert.deepEqual(Object.keys(body).sort(),['exercise_id','option_index']);
        assert.equal(request.headers().authorization,'Bearer synthetic-foundations-user');
        if(checks===1)await pending;
        return json({exercise_id:'scenario',correct:body.option_index===1,explanation:course.feedback[body.option_index]});
      }
      if(path.endsWith('/complete')){completed=true;return json({lesson_id:course.id,completed:true});}
      return json({course,lessons:[{id:course.id,title:course.lesson,position:1,completed,content:'Plain text fallback',learning_guide:{
        revision:course.revision,objectives:[{id:'objective',text:course.objective}],
        sections:[{title:'Worked scenario',body:'Read the request, consider the audience and choose a thoughtful next step.'}],
        exercises:[{id:'scenario',objective:'objective',prompt:course.prompt,options:course.options}]
      }}]});
    });
    await page.goto(WEB+'/learn');
    await page.getByRole('button',{name:'Continue learning →'}).click();
    await page.getByRole('heading',{name:course.lesson,exact:true}).waitFor();
    assert.equal(await page.getByText('Python examples are for reading and prediction; this lesson does not run code.',{exact:true}).count(),0);
    const button=page.getByRole('button',{name:'Check answer',exact:true});
    assert.equal(await button.isDisabled(),true);
    const first=page.getByRole('radio',{name:course.options[0],exact:true});
    const second=page.getByRole('radio',{name:course.options[1],exact:true});
    await first.check();await button.focus();await page.keyboard.press('Enter');
    const checking=page.getByRole('button',{name:'Checking…',exact:true});await checking.waitFor();
    assert.equal(await checking.getAttribute('aria-disabled'),'true');
    assert.equal(await checking.evaluate(el=>el===document.activeElement),true);
    await page.keyboard.press('Enter');
    await second.evaluate(element=>element.click());
    assert.equal(await first.isChecked(),true,'An in-flight check must keep its selected answer');
    releaseResponse();
    await page.getByText(course.feedback[0],{exact:false}).waitFor();
    assert.equal(checks,1);assert.equal(completed,false);
    await second.check();await button.focus();await page.keyboard.press('Enter');
    await page.getByText(course.feedback[1],{exact:false}).waitFor();
    assert.equal(checks,2);assert.equal(await button.evaluate(el=>el===document.activeElement),true);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth),true);
    await page.getByRole('button',{name:'Mark lesson complete'}).click();
    await page.getByRole('button',{name:'Completed ✓',exact:true}).waitFor();
    assert.equal(completed,true);assert.deepEqual(errors,[]);
  });
}
