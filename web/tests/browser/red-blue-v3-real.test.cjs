// Real browser, isolated PostgreSQL, actual two authenticated V3 seats.
const {test, after} = require("node:test");
const assert = require("node:assert/strict");
const {chromium} = require("playwright");
const WEB = process.env.EDUCYBER_E2E_WEB_URL || "http://127.0.0.1:3100";
const API = process.env.EDUCYBER_E2E_API_URL || "http://127.0.0.1:8000";
const TOKEN = process.env.EDUCYBER_E2E_TOKEN;
if (!TOKEN) throw Error("Isolated synthetic session required");
let browser;
after(async()=>{if(browser)await browser.close();});
async function seat(t,token,mobile=false){
  browser ||= await chromium.launch({headless:true,args:["--disable-dev-shm-usage"]});
  const ctx=await browser.newContext({baseURL:WEB,reducedMotion:"reduce",
    viewport:mobile?{width:390,height:844}:{width:1440,height:1000}});
  t.after(()=>ctx.close());
  await ctx.addInitScript(value=>sessionStorage.setItem("educyber_token",value),token);
  const page=await ctx.newPage();page.setDefaultTimeout(12000);
  const errors=[];page.on("pageerror",e=>errors.push(e.message));
  return {page,errors};
}
const ROOT="/api/v1/red-blue-v3";
test("V3 Microfinance browser: Blue prepares, Red discovers and private views persist",async t=>{
  const blue=await seat(t,TOKEN);
  await blue.page.goto("/red-blue/v3");
  await blue.page.getByRole("heading",{name:/Discover the threat/}).waitFor();
  await blue.page.getByLabel("V3 opponent").selectOption("human");
  await blue.page.getByLabel("V3 match duration").selectOption("15");
  const responsePromise=blue.page.waitForResponse(r=>r.url().endsWith(ROOT+"/matches")&&r.request().method()==="POST");
  await blue.page.getByRole("button",{name:"Create V3 match"}).click();
  const response=await responsePromise;
  assert.equal(response.status(),201);
  const initial=await response.json();
  const matchId=initial.id;
  const blueWorkspace=blue.page.getByRole("region",{name:"V3 match workspace"});
  await blueWorkspace.getByRole("heading",{name:/Prepare your defensive baseline/}).waitFor();
  await blueWorkspace.getByRole("button",{name:"monitoring",exact:true}).last().click();
  await blueWorkspace.getByRole("button",{name:"Create single-use invitation"}).click();
  const token=await blueWorkspace.getByLabel("Share privately with the other learner").inputValue();
  assert.equal(token.length,43);
  const credentials={email:"v3-"+Date.now()+"@example.com",
    password:"Synthetic-v3-password-2026!"};
  const register=await blue.page.request.post(API+"/api/v1/auth/register",{
    data:{...credentials,full_name:"V3 Synthetic Red",date_of_birth:"1990-01-01"}});
  assert.equal(register.status(),201);
  const login=await blue.page.request.post(API+"/api/v1/auth/login",{data:credentials});
  assert.equal(login.status(),200);
  const redToken=(await login.json()).access_token;
  const red=await seat(t,redToken,true);
  await red.page.goto("/red-blue/v3");
  await red.page.getByLabel("Private match invitation code").fill(token);
  await red.page.getByRole("button",{name:"Join another learner"}).click();
  const redWorkspace=red.page.getByRole("region",{name:"V3 match workspace"});
  await redWorkspace.getByRole("heading",{name:/Prepare your reconnaissance strategy/}).waitFor();
  assert.equal(await redWorkspace.getByText("Loan and transaction ledger",{exact:true}).count(),0);
  await redWorkspace.getByRole("button",{name:"quiet investigation"}).click();
  await redWorkspace.getByRole("button",{name:/Finish preparation/}).click();
  await blueWorkspace.getByRole("button",{name:/Finish preparation/}).click();
  await blueWorkspace.getByRole("heading",{name:"Network intelligence"}).waitFor();
  await redWorkspace.getByRole("heading",{name:"Network intelligence"}).waitFor();
  assert.equal(await redWorkspace.getByRole("button",{name:"Inspect Loan and transaction ledger"}).count(),0);
  await blueWorkspace.getByRole("button",{name:"Inspect Loan and transaction ledger"}).click();
  const inspector=blue.page.getByRole("dialog",{name:/Asset details: Loan and transaction ledger/});
  await inspector.getByText(/Current weaknesses/).waitFor();
  await inspector.getByRole("button",{name:"Close asset details"}).click();
  const blueBefore=await blue.page.request.get(API+ROOT+"/matches/"+matchId,{
    headers:{Authorization:"Bearer "+TOKEN}});
  const blueState=await blueBefore.json();
  assert.equal(blueState.clock.active_side,"blue");
  assert.ok(blueState.clock.match_seconds_remaining>0);
  await blue.page.locator("#v3-actions").selectOption({label:"wait blue · 0 credits"});
  await blue.page.getByRole("button",{name:"Commit action"}).click();
  await red.page.waitForFunction(()=>{const input=document.querySelector("#v3-actions");return input && !input.disabled && input.options.length > 1;});
  const labels=await red.page.locator("#v3-actions option").allTextContents();
  const recon=labels.find(label=>label.includes("recon · Teller workstation"));
  assert.ok(recon,"Red should have a teller reconnaissance option");
  await red.page.locator("#v3-actions").selectOption({label:recon});
  const redCommand=red.page.waitForResponse(r=>r.url().endsWith("/matches/"+matchId+"/commands"));
  await red.page.getByRole("button",{name:"Commit action"}).click();
  assert.equal((await redCommand).status(),200);
  await redWorkspace.getByRole("button",{name:"Inspect Branch identity service"}).waitFor();
  assert.equal(await redWorkspace.getByRole("button",{name:"Inspect Loan and transaction ledger"}).count(),0);
  const redResponse=await red.page.request.get(API+ROOT+"/matches/"+matchId,{
    headers:{Authorization:"Bearer "+redToken}});
  const redState=await redResponse.json();
  assert.equal(redState.assets.length,3);
  for(const secret of ["seed","players","red_known","weaknesses","transcript"]){
    assert.equal(secret in redState,false,"Private V3 state: "+secret);
  }
  assert.deepEqual(blue.errors,[]);assert.deepEqual(red.errors,[]);
});
