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
