// Real browser; synthetic API. Actual handlers/scoring: api/test_mission_learning.py.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const WEB=process.env.EDUCYBER_E2E_WEB_URL||'http://127.0.0.1:3100';
for(const mobile of [false,true])for(const use3D of [false,true]){
 test(`scholarship journey, review and resume; mobile=${mobile}, 3D=${use3D}`,async t=>{
  const browser=await chromium.launch({channel:'chromium',headless:true,args:['--disable-dev-shm-usage','--enable-unsafe-swiftshader']});
  t.after(()=>browser.close());
  const context=await browser.newContext({baseURL:WEB,viewport:mobile?{width:390,height:844}:{width:1280,height:720},reducedMotion:'reduce'});
  await context.addInitScript(()=>sessionStorage.setItem('educyber_token','synthetic-mission-token'));
  const page=await context.newPage(),errors=[];page.on('pageerror',error=>errors.push(error.message));
  let stage=0,started=false,decisions=0,reviews=0,releaseReview;
  const pendingReview=new Promise(resolve=>{releaseReview=resolve;});
  const questions=Array.from({length:5},(_,i)=>({id:'review-'+i,prompt:'Review scenario '+(i+1),options:['Rely on the message','Verify independently']}));
  function run(){return {run_id:77,mission_id:'phishing-investigation',title:'The Scholarship Email',step_index:stage,step_count:3,
   score:stage*15,max_score:45,completed:stage===3,last_feedback:stage?'Saved stage '+stage:null,
   step:stage===3?null:{scene:'Stage '+(stage+1),story:'Investigate this fictional request.',evidence:['Sender','Destination'],question:'Choose a safe action.',options:['Verify through the real portal','Follow the link']},
   learning:{revision:'synthetic-v1',role:'Help a classmate.',objectives:['Verify independently.'],workflow:['Inspect records, select a finding, then commit a response.'],completion:'Complete three decisions; review is optional.',
    stage:stage===3?null:{task:'Check the request at stage '+(stage+1),hints:['Compare sender and destination.','Use an independent route.'],artifacts:[{title:'Sender record',body:'Fictional sender stage '+(stage+1)},{title:'Destination preview',body:'Fictional destination stage '+(stage+1)}]},review:stage===3?questions:[]}};}
  await page.route('**/api/v1/**',async route=>{
   const request=route.request(),path=new URL(request.url()).pathname;
   const json=body=>route.fulfill({contentType:'application/json',body:JSON.stringify(body)});
   if(path.endsWith('/games'))return json({games:[{id:'scholarship',pathway:'secondary',title:'Scholarship game',mechanic:'Investigation',mission_ids:['phishing-investigation'],status:'playable',mission_count:1}]});
   if(path.endsWith('/missions'))return json({missions:[{id:'phishing-investigation',title:'The Scholarship Email',latest_run:started?{run_id:77,completed:stage===3,score:stage*15,step_index:stage}:null}]});
   if(path.endsWith('/history'))return json({runs:[]});
   if(path.endsWith('/start'))started=true;
   if(path.endsWith('/decide')){decisions++;assert.deepEqual(request.postDataJSON(),{expected_step:stage,finding_index:1,option_index:0});stage++;}
   if(path.endsWith('/review')){
    reviews++;const body=request.postDataJSON();assert.deepEqual(Object.keys(body).sort(),['option_index','question_id']);
    if(reviews===1)await pendingReview;
    if(reviews===2)return route.fulfill({status:503,contentType:'application/json',body:JSON.stringify({detail:'Try the review again.'})});
    return json({question_id:body.question_id,correct:body.option_index===1,explanation:body.option_index===1?'Independent verification protects the account.':'The message cannot verify itself.'});
   }
   return json(run());
  });
  await page.goto('/missions');await page.getByRole('button',{name:'Play game',exact:true}).click();
  await page.getByRole('heading',{name:'Your role and goals'}).waitFor();
  await page.getByText('Need a hint?',{exact:true}).click();await page.getByText('Compare sender and destination.',{exact:true}).waitFor();
  await page.getByText('Show another hint',{exact:true}).click();await page.getByText('Use an independent route.',{exact:true}).waitFor();
  for(let index=0;index<3;index++){
   await page.getByText('Check the request at stage '+(index+1),{exact:true}).waitFor();
   if(use3D){
    await page.getByRole('button',{name:'Enter 3D investigation room',exact:true}).click();
    const scene=page.getByRole('region',{name:'Interactive 3D cybersecurity investigation room',exact:true});
    await scene.getByRole('button',{name:/Inspect artifact 1/}).click();await scene.getByText('Fictional sender stage '+(index+1),{exact:true}).waitFor();
    await scene.getByRole('button',{name:/Inspect artifact 2/}).click();await scene.getByText('Fictional destination stage '+(index+1),{exact:true}).waitFor();
    await page.getByRole('button',{name:'Switch to 2D workstation',exact:true}).click();
   }else{
    await page.getByRole('button',{name:'Open evidence locker →',exact:true}).click();
    const artifacts=page.getByRole('region',{name:'Scholarship case artifacts'});
    await artifacts.getByRole('button',{name:/Sender record/}).focus();await page.keyboard.press('Enter');
    await artifacts.getByText('Fictional sender stage '+(index+1),{exact:true}).waitFor();
    await artifacts.getByRole('button',{name:/Destination preview/}).click();
   }
   await page.getByRole('radio',{name:'Destination',exact:true}).check();
   await page.getByRole('button',{name:'Proceed to decision desk →',exact:true}).click();
   await page.getByRole('radio',{name:/Verify through the real portal/}).check();
   await page.getByRole('button',{name:'Commit decision →',exact:true}).click();
  }
  await page.getByRole('heading',{name:'Mission complete',exact:true}).waitFor();assert.equal(decisions,3);
  const review=page.getByRole('region',{name:'Mission review',exact:true});assert.equal(await review.locator('fieldset').count(),5);
  const first=review.locator('form').first();
  await first.getByRole('radio',{name:'Rely on the message',exact:true}).check();
  await first.getByRole('button',{name:'Check review answer',exact:true}).focus();await page.keyboard.press('Enter');
  const checking=first.getByRole('button',{name:'Checking…',exact:true});await checking.waitFor();
  assert.equal(await checking.evaluate(el=>el===document.activeElement),true);
  await page.keyboard.press('Enter');releaseReview();
  await first.getByText('Try again. The message cannot verify itself.',{exact:true}).waitFor();assert.equal(reviews,1);
  await first.getByRole('radio',{name:'Verify independently',exact:true}).check();
  assert.equal(await first.getByText('Try again. The message cannot verify itself.',{exact:true}).count(),0);
  await first.getByRole('button',{name:'Check review answer',exact:true}).click();
  await review.getByRole('alert').filter({hasText:'Try the review again.'}).waitFor();
  await first.getByRole('button',{name:'Check review answer',exact:true}).click();
  await first.getByText('Correct. Independent verification protects the account.',{exact:true}).waitFor();
  assert.equal(reviews,3);assert.equal(stage,3);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  await page.reload();
  await page.getByRole('button',{name:'View result for The Scholarship Email',exact:true}).click();
  await page.getByRole('heading',{name:'Mission complete',exact:true}).waitFor();
  assert.equal(await page.getByRole('region',{name:'Mission review'}).locator('fieldset').count(),5);
  stage=1;await page.reload();
  await page.getByRole('button',{name:'Resume The Scholarship Email',exact:true}).click();
  await page.getByText('Check the request at stage 2',{exact:true}).waitFor();assert.deepEqual(errors,[]);
 });
}
