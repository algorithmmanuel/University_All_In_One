'use strict';
const {test, after} = require('node:test');
const assert = require('node:assert/strict');
const {chromium} = require('playwright');

const WEB = process.env.EDUCYBER_E2E_WEB_URL || 'http://127.0.0.1:3100';
const API = 'http://127.0.0.1:8000';
const pathways = [
  ['secondary','Cyber Explorers'],
  ['university','Cyber Academy'],
  ['professional','Cyber Command']
];
let browser;
after(async () => {if (browser) await browser.close();});

async function setup(t) {
  browser ||= await chromium.launch({headless:true,args:['--disable-dev-shm-usage']});
  const context = await browser.newContext({baseURL:WEB});
  t.after(()=>context.close());
  const page = await context.newPage();
  const failures = [];
  page.on('pageerror',e=>failures.push(e.message));
  return {page,failures};
}

function fixture(gameId='risk-command') {
  let runId = 77;
  let step = 0;
  let score = 0;
  let saved = [];
  const names = {'secondary':'Privacy Patrol','university':'Network Watch','professional':'Risk Command'};
  const ids = {'secondary':'privacy-patrol','university':'network-watch','professional':'risk-command'};
  const games = pathways.map(([pathway])=>({id:ids[pathway],pathway,title:names[pathway],
    mechanic:'Evidence analysis',difficulty:'Intermediate',summary:'Defensive simulated investigation',
    mission_ids:[ids[pathway]],mission_count:1,status:'playable'}));
  const missions = games.map(g=>({id:g.id,title:g.title,track:'defensive',difficulty:'Intermediate',
    summary:g.summary,step_count:3,latest_run:null}));
  const current=()=>({run_id:runId,mission_id:gameId,title:games.find(g=>g.id===gameId)?.title||'Risk Command',
    step_index:step,step_count:3,score,max_score:45,completed:step===3,last_feedback:step?'Decision recorded':null,
    step:step===3?null:{scene:'Stage '+(step+1),story:'Review simulated case evidence.',
      evidence:['Access anomaly','Control gap','Incident timeline'],
      question:'Which action is safest?',options:['Investigate and contain','Ignore the evidence','Delete the logs']}});
  return {games,missions,current,
    reset(id){gameId=id;runId++;step=0;score=0;},
    decide(body){if(body.expected_step!==step)return false;step++;score+=15;saved.push({step,score});return true;},
    history(){return {runs:saved.length?[{id:runId,title:current().title,score,max_score:45,
      completed:step===3,created_at:new Date().toISOString()}]:[]}}};
}

async function mockApi(page,model) {
  await page.route('**/api/v1/**',async route=>{
    const request=route.request();
    const path=new URL(request.url()).pathname;
    const json=(body,status=200)=>route.fulfill({status,contentType:'application/json',body:JSON.stringify(body),
      headers:{'access-control-allow-origin':'*'}});
    if(request.method()==='OPTIONS')return route.fulfill({status:204,headers:{
      'access-control-allow-origin':'*','access-control-allow-methods':'GET, POST, OPTIONS',
      'access-control-allow-headers':'Authorization, Content-Type'}});
    if(path==='/api/v1/auth/login')return json({access_token:'fixture-token'});
    if(path==='/api/v1/dashboard')return json({user:{id:1,full_name:'Test Learner',
      email:'learner@example.invalid',role:'student',is_approved:true}});
    if(path==='/api/v1/games')return json({version:5,games:model.games});
    if(path==='/api/v1/missions')return json({missions:model.missions});
    if(path==='/api/v1/missions/history')return json(model.history());
    const start=path.match(/^\/api\/v1\/missions\/([^/]+)\/start$/);
    if(start){model.reset(start[1]);return json(model.current(),201);}
    if(/^\/api\/v1\/missions\/runs\/\d+\/decide$/.test(path)){
      const body=JSON.parse(request.postData()||'{}');
      if(!model.decide(body))return json({detail:'Mission has advanced'},409);
      return json(model.current());
    }
    if(/^\/api\/v1\/missions\/runs\/\d+$/.test(path))return json(model.current());
    return json({detail:'Unexpected API route: '+path},404);
  });
}

test('sign in, dashboard pathway navigation and 3D/2D mission evidence',async t=>{
  const {page,failures}=await setup(t);
  const model=fixture();
  await mockApi(page,model);
  await page.goto('/account');
  await page.getByRole('button',{name:'Sign in'}).click();
  await page.getByLabel('Email').fill('learner@example.invalid');
  await page.getByLabel('Password').fill('fixture-password');
  await page.getByRole('button',{name:'Sign in',exact:true}).last().click();
  await page.waitForURL('**/dashboard');
  await page.getByRole('heading',{name:'Welcome, Test Learner'}).waitFor();
  await page.getByRole('link',{name:'Open pathway'}).last().click();
  await page.waitForURL('**/missions?pathway=professional');
  await page.getByRole('heading',{name:'Cyber Command game library'}).waitFor();
  await page.getByRole('button',{name:'Play game'}).click();
  await page.getByRole('heading',{name:'Risk Command'}).last().waitFor();
  await page.getByRole('button',{name:'Enter 3D investigation room'}).click();
  await page.getByRole('button',{name:'Switch to 2D workstation'}).waitFor();
  await page.getByRole('button',{name:'Switch to 2D workstation'}).click();
  await page.getByRole('button',{name:'Open evidence locker'}).click();
  for(let i=1;i<=3;i++)await page.getByRole('button',{name:'Inspect professional evidence '+i}).click();
  await page.getByRole('button',{name:/Evidence locker/}).getByText('3/3').waitFor();
  assert.deepEqual(failures,[]);
});

test('three server responses update progress, completion and history',async t=>{
  const {page,failures}=await setup(t);
  const model=fixture('risk-command');
  await mockApi(page,model);
  await page.goto('/account');
  await page.evaluate(()=>sessionStorage.setItem('educyber_token','fixture-token'));
  await page.goto('/missions');
  await page.getByRole('button',{name:'Cyber Command'}).click();
  await page.getByRole('button',{name:'Play game'}).click();
  for(let stage=0;stage<3;stage++){
    await page.getByRole('button',{name:'Open evidence locker'}).click();
    for(let i=1;i<=3;i++)await page.getByRole('button',{name:'Inspect professional evidence '+i}).click();
    await page.getByRole('radio',{name:'Access anomaly'}).check();
    await page.getByRole('button',{name:'Proceed to decision desk'}).click();
    await page.getByRole('radio',{name:/Investigate and contain/}).check();
    await page.getByRole('button',{name:'Commit decision'}).click();
    if(stage<2)await page.getByRole('button',{name:'Open evidence locker'}).waitFor();
  }
  await page.getByRole('heading',{name:'Mission complete'}).waitFor();
  await page.getByText('45 out of 45').waitFor();
  assert.equal(model.history().runs[0].completed,true);
  assert.deepEqual(failures,[]);
});
