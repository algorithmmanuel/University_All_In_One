// Real browser UI checks with intercepted synthetic API responses.
// Pair with api/test_assessment_lengths.py for actual server grading coverage.
const {test, after} = require('node:test');
const assert = require('node:assert/strict');
const {chromium} = require('playwright');
const WEB = process.env.EDUCYBER_E2E_WEB_URL || 'http://127.0.0.1:3100';
let browser;
after(async () => { if (browser) await browser.close(); });

async function setup(t, mobile=false) {
  browser ||= await chromium.launch({channel:'chromium',headless:true,args:['--disable-dev-shm-usage']});
  const context = await browser.newContext({baseURL:WEB, reducedMotion:'reduce',
    viewport:mobile?{width:390,height:844}:{width:1280,height:720}});
  t.after(() => context.close());
  await context.addInitScript(() => {
    sessionStorage.setItem('educyber_token','synthetic-ui-token');
    window.activityScrolls = [];
    const original = HTMLElement.prototype.scrollIntoView;
    HTMLElement.prototype.scrollIntoView = function(options) {
      if (this.classList.contains('activity-heading')) window.activityScrolls.push(options);
      return original.call(this, options);
    };
  });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  return {page,errors};
}

async function openedHeading(page) {
  const heading = page.locator('.activity-heading');
  await heading.waitFor();
  await page.waitForFunction(() => document.activeElement?.classList.contains('activity-heading'));
  const box = await heading.boundingBox();
  assert.ok(box.y >= 0 && box.y < page.viewportSize().height, 'Opened activity heading must be visible');
  const calls = await page.evaluate(() => window.activityScrolls);
  assert.equal(calls.at(-1).behavior, 'instant', 'Reduced motion must not animate');
  return calls.length;
}

for (const mobile of [false,true]) {
  test('assessment presets, custom validation, grading payload and focus; mobile='+mobile, async t => {
    const {page,errors} = await setup(t,mobile);
    let submitted;
    const history = [];
    await page.route('**/api/v1/**', async route => {
      const request=route.request(), url=new URL(request.url());
      const json = body => route.fulfill({contentType:'application/json',body:JSON.stringify(body)});
      if (url.pathname.endsWith('/learning/enrollments')) return json({enrollments:[{id:1,title:'Practice course',academy_id:'cyber'}]});
      if (url.pathname.endsWith('/options')) return json({available_count:50,presets:[5,10,20]});
      if (url.pathname.endsWith('/attempts')) return json({attempts:history});
      if (url.pathname.endsWith('/submit')) {
        submitted=request.postDataJSON();
        const result={score:3,total:5,percentage:60,feedback:Object.keys(submitted.answers).map(id=>({
          question_id:Number(id),correct_index:0,selected_index:0,correct:true,explanation:'Check the source.'}))};
        history.push({id:1,score:3,total:5,percentage:60,submitted_at:'2026-01-01T00:00:00Z'});
        return json(result);
      }
      const count=Number(url.searchParams.get('question_count'));
      return json({question_count:count,questions:Array.from({length:count},(_,i)=>({
        id:i+1,prompt:'Scenario '+(i+1),options:['Safe action','Unsafe action']}))});
    });
    await page.goto('/assessments');
    await page.getByRole('button',{name:'Practice course'}).click();
    await openedHeading(page);
    await page.getByRole('radio',{name:'Quick (5 questions)',exact:true}).check();
    await page.getByRole('button',{name:'Start 5-question assessment'}).click();
    assert.equal(await openedHeading(page),2);
    assert.equal(await page.locator('form fieldset').count(),5);
    for (const fieldset of await page.locator('form fieldset').all()) await fieldset.getByRole('radio').first().check();
    assert.equal(await page.evaluate(() => window.activityScrolls.length),2,'Answers must not trigger workspace scrolling');
    await page.getByRole('button',{name:'Submit assessment'}).click();
    await page.getByRole('heading',{name:'Score: 3/5 (60%)'}).waitFor();
    assert.equal(submitted.question_count,5);
    assert.equal(Object.keys(submitted.answers).length,5);
    await page.getByText('Saved as a 5-question practice attempt.').waitFor();
    await page.getByRole('button',{name:'Choose another test length'}).click();
    await openedHeading(page);
    await page.getByRole('radio',{name:'Extended (20 questions)',exact:true}).check();
    await page.getByRole('button',{name:'Start 20-question assessment'}).click();
    await openedHeading(page);
    assert.equal(await page.locator('form fieldset').count(),20);
    await page.getByRole('button',{name:'Practice course'}).click();
    await openedHeading(page);
    await page.getByRole('radio',{name:'Custom',exact:true}).check();
    const countInput=page.getByRole('spinbutton',{name:'Number of questions'});
    await countInput.fill('51');
    assert.ok(await page.getByRole('button',{name:'Start assessment',exact:true}).isDisabled());
    await countInput.fill('7');
    await page.getByRole('button',{name:'Start 7-question assessment'}).click();
    await openedHeading(page);
    assert.equal(await page.locator('form fieldset').count(),7);
    assert.deepEqual(errors,[]);
  });
}

test('course opening focuses loaded lessons; completion does not jump back', async t => {
  const {page,errors} = await setup(t);
  let enrolled=false,completed=false;
  const courses=Array.from({length:13},(_,i)=>({id:i+1,title:'Course '+(i+1),academy_id:'cyber',lesson_count:1}));
  await page.route('**/api/v1/**',async route=>{
    const path=new URL(route.request().url()).pathname;
    const json=body=>route.fulfill({contentType:'application/json',body:JSON.stringify(body)});
    if(path.endsWith('/catalog'))return json({courses});
    if(path.endsWith('/enrollments'))return json({enrollments:enrolled?[{...courses[0],total_lessons:1,completed_lessons:completed?1:0,progress_percent:completed?100:0}]:[]});
    if(path.endsWith('/enrollments/1')){enrolled=true;return json({});}
    if(path.endsWith('/complete')){completed=true;return json({});}
    return json({course:courses[0],lessons:[{id:1,title:'A practical example',content:'Verify the sender.',position:1,completed}]});
  });
  await page.goto('/learn');
  await page.getByRole('button',{name:'Enroll for free'}).first().click();
  assert.equal(await openedHeading(page),1);
  await page.getByRole('button',{name:'Mark lesson complete'}).click();
  await page.getByRole('button',{name:'Completed ✓',exact:true}).waitFor();
  assert.equal(await page.evaluate(()=>window.activityScrolls.length),1);
  await page.getByRole('button',{name:'Close lessons'}).click();
  await page.getByRole('button',{name:'Open course',exact:true}).click();
  assert.equal(await openedHeading(page),2);
  assert.deepEqual(errors,[]);
});

test('mission start and resume focus the workspace after the library updates', async t=>{
  const {page,errors}=await setup(t);
  let started=false;
  const run={run_id:77,mission_id:'risk-command',title:'Risk Command',step_index:0,step_count:3,
    score:0,max_score:45,completed:false,last_feedback:null,step:{scene:'Stage 1',story:'Review the case.',
      evidence:['Access anomaly','Control gap','Incident timeline'],question:'Which action is safest?',
      options:['Investigate and contain','Ignore the evidence','Delete the logs']}};
  const games=Array.from({length:10},(_,i)=>({id:'game-'+i,pathway:'professional',title:'Practice game '+i,
    mechanic:'Evidence analysis',difficulty:'Intermediate',summary:'A fictional investigation.',
    mission_ids:['risk-command'],mission_count:1,status:'playable'}));
  await page.route('**/api/v1/**',async route=>{
    const path=new URL(route.request().url()).pathname;
    const json=body=>route.fulfill({contentType:'application/json',body:JSON.stringify(body)});
    if(path.endsWith('/games'))return json({games});
    if(path.endsWith('/missions'))return json({missions:[{id:'risk-command',title:'Risk Command',
      latest_run:started?{run_id:77,completed:false,score:0,step_index:0}:null}]});
    if(path.endsWith('/history'))return json({runs:[]});
    if(path.endsWith('/start'))started=true;
    return json(run);
  });
  await page.goto('/missions?pathway=professional');
  await page.getByRole('button',{name:'Play game',exact:true}).first().click();
  assert.equal(await openedHeading(page),1);
  await page.getByRole('button',{name:'Exit workstation'}).click();
  await page.getByRole('button',{name:'Resume Risk Command'}).first().click();
  assert.equal(await openedHeading(page),2);
  assert.deepEqual(errors,[]);
});
