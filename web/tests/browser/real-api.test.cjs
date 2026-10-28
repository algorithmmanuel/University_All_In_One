'use strict';
const {test,after} = require('node:test');
const assert = require('node:assert/strict');
const {chromium} = require('playwright');

const WEB=process.env.EDUCYBER_E2E_WEB_URL||'http://127.0.0.1:3100';
const API=process.env.EDUCYBER_E2E_API_URL||'http://127.0.0.1:8000';
const TOKEN=process.env.EDUCYBER_E2E_TOKEN;
if(!TOKEN)throw new Error('EDUCYBER_E2E_TOKEN must be provisioned by the isolated CI database seeder');
let browser;
after(async()=>{if(browser)await browser.close()});

test('real backend: thirty-game catalogue, persistent scoring, and 2D/3D browser switching',async t=>{
  browser=await chromium.launch({headless:true,args:['--disable-dev-shm-usage']});
  const context=await browser.newContext({baseURL:WEB});
  t.after(()=>context.close());
  const page=await context.newPage();
  const errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  const headers={Authorization:'Bearer '+TOKEN};
  const response=await page.request.get(API+'/api/v1/games');
  assert.equal(response.status(),200);
  const catalogue=await response.json();
  assert.equal(catalogue.games.length,30);
  assert.equal(catalogue.games.filter(g=>g.status==='playable').length,30);

  await page.goto('/account');
  await page.evaluate(token=>sessionStorage.setItem('educyber_token',token),TOKEN);
  await page.goto('/missions?pathway=professional');
  await page.getByRole('heading',{name:'Cyber Command game library'}).waitFor();
  await page.getByRole('button',{name:'Play game'}).first().click();
  await page.getByRole('button',{name:'Enter 3D investigation room'}).click();
  await page.getByRole('button',{name:'Switch to 2D workstation'}).waitFor();
  await page.getByRole('button',{name:'Switch to 2D workstation'}).click();

  // The API must persist the same user-specific run across browser reloads.
  const missionsResponse=await page.request.get(API+'/api/v1/missions',{headers});
  assert.equal(missionsResponse.status(),200);
  const missions=(await missionsResponse.json()).missions;
  const run=missions.find(m=>m.latest_run&&!m.latest_run.completed);
  assert.ok(run,'Browser-created run must persist in PostgreSQL');
  const runId=run.latest_run.run_id;
  const before=await page.request.get(API+'/api/v1/missions/runs/'+runId,{headers});
  assert.equal(before.status(),200);
  let state=await before.json();
  assert.equal(state.step_index,0);
  await page.reload();
  await page.getByRole('heading',{name:'Cyber Command game library'}).waitFor();
  const persisted=await page.request.get(API+'/api/v1/missions/runs/'+runId,{headers});
  assert.equal((await persisted.json()).step_index,0);
  for(let i=0;i<3;i++){
    const decision=await page.request.post(API+'/api/v1/missions/runs/'+runId+'/decide',{
      headers,data:{expected_step:i,option_index:0,finding_index:0}
    });
    assert.equal(decision.status(),200);
    state=await decision.json();
    assert.equal(state.step_index,i+1);
    const replay=await page.request.post(API+'/api/v1/missions/runs/'+runId+'/decide',{
      headers,data:{expected_step:i,option_index:0,finding_index:0}
    });
    assert.equal(replay.status(),409);
  }
  assert.equal(state.completed,true);
  assert.ok(state.score>=0&&state.score<=45);
  const history=await page.request.get(API+'/api/v1/missions/history',{headers});
  assert.equal(history.status(),200);
  assert.ok((await history.json()).runs.some(r=>r.id===runId&&r.completed));
  assert.deepEqual(errors,[]);
});

for(const mobile of [false,true])test('real backend: onboarding, learning, assessment persistence and logout; mobile='+mobile,async t=>{
  browser ||= await chromium.launch({headless:true,args:['--disable-dev-shm-usage']});
  const context=await browser.newContext({baseURL:WEB,reducedMotion:'reduce',viewport:mobile?{width:390,height:844}:{width:1280,height:800}});
  t.after(()=>context.close());const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const email='phase5-'+Date.now()+'-'+Number(mobile)+'@example.com',password='Synthetic-learning-pass-2026!';
  await page.goto('/account');
  await page.getByLabel('Full name',{exact:true}).fill('Synthetic Browser Learner');
  await page.getByLabel('Date of birth',{exact:true}).fill('1991-01-01');
  await page.getByLabel('Email',{exact:true}).fill(email);
  await page.getByLabel('Password',{exact:true}).fill(password);
  await page.getByLabel('Confirm password',{exact:true}).fill(password);
  await page.getByRole('button',{name:'Create account',exact:true}).click();
  await page.getByRole('heading',{name:'Welcome back',exact:true}).waitFor();
  await page.getByLabel('Password',{exact:true}).fill(password);
  await page.getByRole('button',{name:'Sign in',exact:true}).last().click();
  await page.waitForURL('**/dashboard');
  await page.getByRole('link',{name:'Choose your first course',exact:true}).click();
  const course=page.getByRole('article').filter({has:page.getByRole('heading',{name:'Introduction to Python',exact:true})});
  await course.getByRole('button',{name:'Enroll for free',exact:true}).click();
  await page.getByRole('button',{name:'Mark lesson complete',exact:true}).first().click();
  await page.getByRole('button',{name:'Completed ✓',exact:true}).waitFor();
  await page.goto('/dashboard');
  await page.getByText('1 of 3 lessons complete',{exact:true}).waitFor();
  await page.getByRole('link',{name:'Continue Introduction to Python',exact:true}).click();
  await page.waitForFunction(()=>document.activeElement?.textContent==='Conditional logic');
  await page.goto('/assessments');
  await page.getByRole('button',{name:'Introduction to Python',exact:true}).click();
  await page.getByRole('radio',{name:'Quick (5 questions)',exact:true}).check();
  await page.getByRole('button',{name:'Start 5-question assessment',exact:true}).click();
  await page.locator('form fieldset').nth(4).waitFor();
  for(const field of await page.locator('form fieldset').all())await field.getByRole('radio').first().check();
  await page.getByRole('button',{name:'Submit assessment',exact:true}).click();
  await page.getByText('Saved as a 5-question practice attempt.',{exact:true}).waitFor();
  await page.getByRole('heading',{name:'Topic results and next steps',exact:true}).waitFor();
  await page.goto('/dashboard');
  await page.getByRole('link',{name:/Introduction to Python: .*\/5/}).click();
  await page.getByRole('heading',{name:/Saved result: .*\/5/}).waitFor();
  await page.reload();
  await page.getByRole('heading',{name:/Saved result: .*\/5/}).waitFor();
  const token=await page.evaluate(()=>sessionStorage.getItem('educyber_token'));
  await page.goto('/dashboard');await page.getByRole('button',{name:'Sign out',exact:true}).click();
  await page.waitForURL('**/account');
  assert.equal(await page.evaluate(()=>sessionStorage.getItem('educyber_token')),null);
  assert.equal((await page.request.get(API+'/api/v1/dashboard',{headers:{Authorization:'Bearer '+token}})).status(),401);
  assert.deepEqual(errors,[]);
});
