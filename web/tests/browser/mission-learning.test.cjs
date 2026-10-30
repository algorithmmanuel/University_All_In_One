// Real browser; synthetic API. Actual handlers/scoring: api/test_mission_learning.py.
const {test,after}=require('node:test');
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const WEB=process.env.EDUCYBER_E2E_WEB_URL||'http://127.0.0.1:3100';
// Reuse the browser process, but isolate storage/routes in a fresh context for
// every case. Larger content batches should not pay browser startup per test.
let browser;
after(async()=>{if(browser)await browser.close();});
// Only static Python data/helpers are loaded: no server, credentials or database.
// This keeps stage shapes/text aligned with source; grading/ownership is tested
// separately through real HTTP handlers in test_mission_learning.py.
const {execFileSync}=require('node:child_process');
const path=require('node:path');
const fixtureSource=`
import ast, json
from pathlib import Path
from mission_data import MISSIONS
from mission_learning import GUIDES, public_learning
# Read the literal catalogue mapping without importing application dependencies.
# Fail visibly if its shape changes, rather than defaulting games to a pathway.
catalog = ast.parse(Path('game_catalog.py').read_text(encoding='utf-8'))
playable_node = next(node.value for node in catalog.body if isinstance(node, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == 'PLAYABLE' for t in node.targets))
pathways = {mission_id: pathway for _, pathway, _, _, ids in ast.literal_eval(playable_node)
            for mission_id in ids}
fixtures = {}
for mission_id, guide in GUIDES.items():
    mission = MISSIONS[mission_id]
    steps = [{**{key: step[key] for key in ('scene', 'story', 'evidence', 'question')},
              'options': [item['text'] for item in step['options']]} for step in mission['steps']]
    fixtures[mission_id] = {'title': mission['title'], 'pathway': pathways[mission_id], 'steps': steps,
        'learning': [public_learning(mission_id, i, False) for i in range(len(steps))],
        'completed_learning': public_learning(mission_id, len(steps), True),
        'review_keys': guide.REVIEW}
print(json.dumps(fixtures))
`;
const fixtures=JSON.parse(execFileSync(process.env.EDUCYBER_TEST_PYTHON||(process.platform==='win32'?'python':'python3'),['-c',fixtureSource],{
 cwd:path.resolve(__dirname,'../../../api'),encoding:'utf8'
}));
for(const missionId of Object.keys(fixtures))for(const mobile of [false,true])for(const use3D of [false,true]){
 const source=fixtures[missionId],title=source.title,pathway=source.pathway;
 test(`${title} journey, review and resume; mobile=${mobile}, 3D=${use3D}`,async t=>{
  browser ||= await chromium.launch({channel:'chromium',headless:true,args:['--disable-dev-shm-usage','--enable-unsafe-swiftshader']});
  const context=await browser.newContext({baseURL:WEB,viewport:mobile?{width:390,height:844}:{width:1280,height:720},reducedMotion:'reduce'});
  t.after(()=>context.close());
  await context.addInitScript(()=>sessionStorage.setItem('educyber_token','synthetic-mission-token'));
  const page=await context.newPage(),errors=[];page.on('pageerror',error=>errors.push(error.message));
  let stage=0,started=false,decisions=0,reviews=0,releaseReview;
  const pendingReview=new Promise(resolve=>{releaseReview=resolve;});
  function run(){return {run_id:77,mission_id:missionId,title,step_index:stage,step_count:3,
   score:stage*15,max_score:45,completed:stage===3,last_feedback:stage?'Saved stage '+stage:null,
   step:stage===3?null:source.steps[stage],learning:stage===3?source.completed_learning:source.learning[stage]};}
  await page.route('**/api/v1/**',async route=>{
   const request=route.request(),path=new URL(request.url()).pathname;
   const json=body=>route.fulfill({contentType:'application/json',body:JSON.stringify(body)});
   if(path.endsWith('/games'))return json({games:[{id:missionId,pathway,title,mechanic:'Investigation',mission_ids:[missionId],status:'playable',mission_count:1}]});
   if(path.endsWith('/missions'))return json({missions:[{id:missionId,title,latest_run:started?{run_id:77,completed:stage===3,score:stage*15,step_index:stage}:null}]});
   if(path.endsWith('/history'))return json({runs:[]});
   if(path.endsWith('/start'))started=true;
   if(path.endsWith('/decide')){decisions++;assert.deepEqual(request.postDataJSON(),{expected_step:stage,finding_index:source.steps[stage].evidence.length-1,option_index:0});stage++;}
   if(path.endsWith('/review')){
    reviews++;const body=request.postDataJSON();assert.deepEqual(Object.keys(body).sort(),['option_index','question_id']);
    if(reviews===1)await pendingReview;
    if(reviews===2)return route.fulfill({status:503,contentType:'application/json',body:JSON.stringify({detail:'Try the review again.'})});
    const question=source.review_keys.find(item=>item.id===body.question_id);
    return json({question_id:body.question_id,correct:body.option_index===question.answer,explanation:question.feedback[body.option_index]});
   }
   return json(run());
  });
  await page.goto('/missions?pathway='+pathway);await page.getByRole('button',{name:'Play game',exact:true}).click();
  await page.getByRole('heading',{name:'Your role and goals'}).waitFor();
  await page.getByText('Need a hint?',{exact:true}).click();
  await page.getByText(source.learning[0].stage.hints[0],{exact:true}).waitFor();
  await page.getByText('Show another hint',{exact:true}).click();
  await page.getByText(source.learning[0].stage.hints[1],{exact:true}).waitFor();
  for(let index=0;index<3;index++){
   const current=source.steps[index],guidance=source.learning[index].stage;
   await page.getByText(guidance.task,{exact:true}).waitFor();
   if(use3D){
    await page.getByRole('button',{name:'Enter 3D investigation room',exact:true}).click();
    const scene=page.getByRole('region',{name:'Interactive 3D cybersecurity investigation room',exact:true});
    for(let item=0;item<guidance.artifacts.length;item++){
     await scene.getByRole('button',{name:new RegExp('^Inspect artifact '+(item+1))}).click();
     await scene.getByText(guidance.artifacts[item].body,{exact:true}).waitFor();
    }
    await page.getByRole('button',{name:'Switch to 2D workstation',exact:true}).click();
   }else{
    await page.getByRole('button',{name:'Open evidence locker →',exact:true}).click();
    const artifacts=page.getByRole('region',{name:'Case artifacts'});
    for(let item=0;item<guidance.artifacts.length;item++){
     await artifacts.getByRole('button').nth(item).focus();await page.keyboard.press('Enter');
     await artifacts.getByText(guidance.artifacts[item].body,{exact:true}).waitFor();
    }
   }
   await page.getByRole('radio',{name:current.evidence.at(-1),exact:true}).check();
   await page.getByRole('button',{name:'Proceed to decision desk →',exact:true}).click();
   // The action label includes its visible letter; choose within the action group.
   await page.locator('input[name="mission-77-'+index+'"]').first().check();
   await page.getByRole('button',{name:'Commit decision →',exact:true}).click();
  }
  await page.getByRole('heading',{name:'Mission complete',exact:true}).waitFor();assert.equal(decisions,3);
  const review=page.getByRole('region',{name:'Mission review',exact:true});assert.equal(await review.locator('fieldset').count(),5);
  const first=review.locator('form').first();
  const reviewQuestion=source.review_keys[0],wrongIndex=(reviewQuestion.answer+1)%reviewQuestion.options.length;
  await first.getByRole('radio').nth(wrongIndex).check();
  await first.getByRole('button',{name:'Check review answer',exact:true}).focus();await page.keyboard.press('Enter');
  const checking=first.getByRole('button',{name:'Checking…',exact:true});await checking.waitFor();
  assert.equal(await checking.evaluate(el=>el===document.activeElement),true);
  await page.keyboard.press('Enter');releaseReview();
  await first.getByText('Try again. '+reviewQuestion.feedback[wrongIndex],{exact:true}).waitFor();assert.equal(reviews,1);
  await first.getByRole('radio').nth(reviewQuestion.answer).check();
  assert.equal(await first.getByText('Try again. '+reviewQuestion.feedback[wrongIndex],{exact:true}).count(),0);
  await first.getByRole('button',{name:'Check review answer',exact:true}).click();
  await review.getByRole('alert').filter({hasText:'Try the review again.'}).waitFor();
  await first.getByRole('button',{name:'Check review answer',exact:true}).click();
  await first.getByText('Correct. '+reviewQuestion.feedback[reviewQuestion.answer],{exact:true}).waitFor();
  assert.equal(reviews,3);assert.equal(stage,3);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  await page.reload();
  await page.getByRole('button',{name:'View result for '+title,exact:true}).click();
  await page.getByRole('heading',{name:'Mission complete',exact:true}).waitFor();
  assert.equal(await page.getByRole('region',{name:'Mission review'}).locator('fieldset').count(),5);
  stage=1;await page.reload();
  await page.getByRole('button',{name:'Resume '+title,exact:true}).click();
  await page.getByText(source.learning[1].stage.task,{exact:true}).waitFor();assert.deepEqual(errors,[]);
 });
}
