const { test, after } = require("node:test");
const assert = require("node:assert/strict");
const { chromium } = require("playwright");
const WEB = process.env.EDUCYBER_E2E_WEB_URL || "http://127.0.0.1:3100";
let browser;
after(async () => {
  if (browser) await browser.close();
});
for (const mobile of [false, true])
  test(`journey: beginner, experienced, audience and back navigation; mobile=${mobile}`, async (t) => {
    browser ||= await chromium.launch({
      headless: true,
      args: ["--disable-dev-shm-usage"],
    });
    const ctx = await browser.newContext({
      baseURL: WEB,
      reducedMotion: "reduce",
      viewport: mobile
        ? { width: 320, height: 780 }
        : { width: 1440, height: 1000 },
    });
    t.after(() => ctx.close());
    const page = await ctx.newPage(),
      errors = [],
      writes = [];
    page.on("pageerror", (e) => errors.push(e.message));
    page.on("request", (r) => {
      if (r.method() === "POST") writes.push(r.url());
    });
    // The public journey remains useful while discovery services are unavailable.
    await page.route("**/api/v1/**", (r) =>
      r.fulfill({
        status: 503,
        contentType: "application/json",
        body: JSON.stringify({ detail: "Synthetic unavailable" }),
      }),
    );
    await page.goto("/");
    await page
      .getByRole("link", { name: "Begin my journey →", exact: true })
      .click();
    await page
      .getByRole("heading", { name: "Discover", exact: true })
      .waitFor();
    const nav = page.getByRole("navigation", {
      name: "Choose your starting stage",
    });
    assert.equal(await nav.getByRole("button").count(), 8);
    await page.getByRole("button", { name: /Cyber Command/ }).click();
    await nav
      .getByRole("button", { name: "3 Check understanding", exact: true })
      .click();
    await page.waitForFunction(
      () => document.activeElement?.textContent === "Check understanding",
    );
    assert.ok(
      (
        await page
          .getByRole("link", { name: /Open Practise governance/ })
          .getAttribute("href")
      ).includes("topic=governance"),
    );
    await nav
      .getByRole("button", { name: "8 Compete and reflect", exact: true })
      .click();
    const human = await page
      .getByRole("link", { name: /Open Create a two-learner/ })
      .getAttribute("href");
    assert.ok(
      human.includes("mode=human") &&
        human.includes("scenario=payment_insider"),
    );
    await page.reload();
    await page
      .getByRole("heading", { name: "Compete and reflect", exact: true })
      .waitFor();
    assert.equal(
      await page
        .getByRole("button", { name: /Cyber Command/ })
        .getAttribute("aria-pressed"),
      "true",
    );
    await nav
      .getByRole("button", { name: "6 Command an incident", exact: true })
      .click();
    await page.goBack();
    await page
      .getByRole("heading", { name: "Compete and reflect", exact: true })
      .waitFor();
    await page.goto("/journey?stage=understand&pathway=secondary");
    await page
      .getByRole("link", { name: /Open Digital Citizenship Essentials/ })
      .waitFor();
    await nav
      .getByRole("button", { name: "6 Command an incident", exact: true })
      .click();
    await page
      .getByRole("link", { name: "Open The reconnection decision →", exact: true })
      .waitFor();
    assert.equal(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
      true,
    );
    if (process.env.EDUCYBER_SCREENSHOT_DIR)
      await page.screenshot({
        path:
          process.env.EDUCYBER_SCREENSHOT_DIR +
          `/journey-${mobile ? "mobile" : "desktop"}.png`,
        fullPage: true,
      });
    await page.goto("/journey?stage=malicious&pathway=admin");
    await page
      .getByRole("heading", { name: "Discover", exact: true })
      .waitFor();
    assert.deepEqual(writes, []);
    assert.deepEqual(errors, []);
  });

test("journey foundation handoff suggests a real course without automatic enrolment", async (t) => {
  browser ||= await chromium.launch({
    headless: true,
    args: ["--disable-dev-shm-usage"],
  });
  const ctx = await browser.newContext({
    baseURL: WEB,
    viewport: { width: 390, height: 844 },
    reducedMotion: "reduce",
  });
  t.after(() => ctx.close());
  await ctx.addInitScript(() =>
    sessionStorage.setItem("educyber_token", "synthetic"),
  );
  const page = await ctx.newPage(),
    writes = [];
  page.on("request", (r) => {
    if (r.method() === "POST") writes.push(r.url());
  });
  await page.route("**/api/v1/**", (route) => {
    const path = new URL(route.request().url()).pathname;
    const body = path.endsWith("/learning/catalog")
      ? {
          courses: [
            {
              id: 1,
              title: "Introduction to Python",
              academy_id: "university",
              description: "Synthetic Python",
              lesson_count: 3,
            },
            {
              id: 2,
              title: "Cyber Safety Foundations",
              academy_id: "cyber",
              description: "Synthetic safety",
              lesson_count: 3,
            },
          ],
        }
      : { enrollments: [] };
    return route.fulfill({
      contentType: "application/json",
      body: JSON.stringify(body),
    });
  });
  await page.goto("/journey?stage=understand&pathway=secondary");
  await page
    .getByRole("link", { name: "Open Cyber Safety Foundations →", exact: true })
    .click();
  await page
    .getByText("Suggested from your journey:", { exact: false })
    .waitFor();
  assert.equal(
    await page.getByRole("article").filter({ has: page.getByRole("heading", { name: "Cyber Safety Foundations", exact: true }) }).getByRole("heading", { name: "Cyber Safety Foundations", exact: true }).innerText(),
    "Cyber Safety Foundations",
  );
  await page
    .getByRole("link", { name: "Learning journey", exact: true })
    .click();
  await page
    .getByRole("heading", { name: "Understand", exact: true })
    .waitFor();
  assert.equal(
    await page
      .getByRole("button", { name: /Cyber Explorers/ })
      .getAttribute("aria-pressed"),
    "true",
  );
  assert.deepEqual(writes, []);
});

// Use the published authored catalogue, not invented case fixtures.
const workshopCatalog = JSON.parse(require('node:fs').readFileSync(require('node:path').join(__dirname,'../../../api/content/journey_workshops_v1.json'),'utf8'));
for (const mobile of [false,true]) for (const [pathway, name, firstQuestion, expectedCase] of [
  ['secondary','Cyber Explorers','A friend sends a shortened link offering free game credits and asks for your account password. What should you do?','scholarship-pressure'],
  ['university','Cyber Academy','An application accepts a record identifier from its browser. Where must permission to read that record be checked?','shared-device'],
  ['professional','Cyber Command','A risk treatment is scheduled six weeks away while exposure remains. What should management require now?','approval-surprise'],
]) test(`distinct ${name} eight-stage content and preview, mobile=${mobile}`,async t=>{
  browser ||= await chromium.launch({headless:true,args:['--disable-dev-shm-usage']});
  const ctx=await browser.newContext({baseURL:WEB,reducedMotion:'reduce',viewport:mobile?{width:390,height:844}:{width:1440,height:1000}});
  t.after(()=>ctx.close());const page=await ctx.newPage(),writes=[],errors=[];
  page.on('request',r=>{if(r.method()==='POST')writes.push(r.url());});page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/api/v1/workshops/catalog',r=>r.fulfill({contentType:'application/json',body:JSON.stringify({cases:workshopCatalog})}));
  await page.goto('/journey?stage=discover&pathway='+pathway);
  await page.getByRole('link',{name:'Explore '+workshopCatalog.find(c=>c.id===expectedCase).title+' →',exact:true}).waitFor();
  assert.equal(await page.getByRole('heading',{level:4}).count(),1);
  const nav=page.getByRole('navigation',{name:'Choose your starting stage'});
  const caseTitles=new Set();
  for(let i=0;i<8;i++){
    await nav.getByRole('button').nth(i).click();
    if(i!==5 || pathway==='university'){
      const title=page.getByRole('heading',{level:4});await title.waitFor();caseTitles.add(await title.innerText());
      assert.equal(await title.count(),1);
    }else{
      const core=page.getByRole('link',{name:/Open The (reconnection decision|urgent executive change)/});assert.equal(await core.count(),1);
    }
  }
  assert.equal(caseTitles.size,pathway==='university'?8:7);
  if(pathway!=='professional'){
    const next=pathway==='secondary'?'Cyber Academy':'Cyber Command';
    await page.getByRole('button',{name:'Explore '+next+' next →',exact:true}).click();
    await page.getByRole('heading',{name:'Discover',exact:true}).waitFor();
    await page.goBack();
  }
  await page.goto('/preview?pathway='+pathway);
  await page.getByRole('heading',{name:firstQuestion,exact:true}).waitFor();
  assert.equal(await page.getByRole('heading',{name:firstQuestion,exact:true}).count(),1);
  for(let i=0;i<6;i++){
    await page.locator('.quiz-options button').first().click();
    await page.getByRole('button',{name:i===5?'See my results →':'Next question →',exact:true}).click();
  }
  await page.getByRole('heading',{name:/Your result:/}).waitFor();
  const onward=page.getByRole('link',{name:'Continue to my suggested stage →',exact:true});
  assert.ok((await onward.getAttribute('href')).includes('pathway='+pathway));
  await onward.click();await page.getByRole('button',{name:new RegExp(name)}).waitFor();
  await page.reload();assert.equal(await page.getByRole('button',{name:new RegExp(name)}).getAttribute('aria-pressed'),'true');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  assert.deepEqual(writes,[]);assert.deepEqual(errors,[]);
});

for(const mobile of [false,true]) test(`detailed Help guide has working chapters and pathway-stage handoffs, mobile=${mobile}`,async t=>{
  browser ||= await chromium.launch({headless:true,args:['--disable-dev-shm-usage']});
  const ctx=await browser.newContext({baseURL:WEB,reducedMotion:'reduce',viewport:mobile?{width:320,height:780}:{width:1440,height:1000}});t.after(()=>ctx.close());
  const page=await ctx.newPage(),writes=[],errors=[];page.on('request',r=>{if(r.method()==='POST')writes.push(r.url());});page.on('pageerror',e=>errors.push(e.message));
  await page.goto('/help');await page.getByRole('heading',{name:'How EduCyber works',exact:true}).waitFor();
  const contents=page.getByRole('navigation',{name:'How to play contents'});
  assert.equal(await contents.getByRole('link').count(),10);
  for(const link of await contents.getByRole('link').all()){
    const href=await link.getAttribute('href');assert.ok(href.startsWith('#'));
    await link.click();await page.locator(href).waitFor();
  }
  await page.getByRole('heading',{name:'8. Play Red / Blue',exact:true}).waitFor();
  await page.getByText('Retry same choice',{exact:false}).waitFor();
  assert.equal(await page.locator('#stages > ol > li').count(),8);
  assert.equal(await page.locator('#stages > ol > li a').count(),24);
  for(const link of await page.locator('#stages > ol > li a').all()){
    const target=new URL(await link.getAttribute('href'),WEB);
    assert.equal(target.pathname,'/journey');assert.ok(['secondary','university','professional'].includes(target.searchParams.get('pathway')));
  }
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  await page.getByRole('link',{name:'Begin Cyber Academy →',exact:true}).click();
  await page.getByRole('heading',{name:'Discover',exact:true}).waitFor();
  assert.equal(await page.getByRole('button',{name:/Cyber Academy/}).getAttribute('aria-pressed'),'true');
  assert.deepEqual(writes,[]);assert.deepEqual(errors,[]);
});
