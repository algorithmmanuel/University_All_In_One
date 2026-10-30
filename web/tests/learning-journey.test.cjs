const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs"),
  path = require("node:path"),
  ts = require("typescript"),
  Module = require("node:module");
const file = path.join(__dirname, "../lib/learning-journey.ts");
const loaded = new Module(file, module);
loaded._compile(
  ts.transpileModule(fs.readFileSync(file, "utf8"), {
    compilerOptions: {
      module: ts.ModuleKind.CommonJS,
      target: ts.ScriptTarget.ES2020,
    },
  }).outputText,
  file,
);
const { STAGES, AUDIENCES, PATHWAY_CONTENT, workshopFor, workshopBelongsTo, nextPathway, resourcesFor, parseJourney, activityJourney } =
  loaded.exports;
test("every audience can enter every stage with local, context-preserving materials", () => {
  assert.equal(STAGES.length, 8);
  for (const audience of AUDIENCES)
    for (const stage of STAGES) {
      const resources = resourcesFor(stage.id, audience.id);
      assert.ok(resources.length > 0);
      for (const resource of resources) {
        const url = new URL(resource.href, "https://educyber.invalid");
        assert.equal(url.origin, "https://educyber.invalid");
        assert.ok(
          [
            "/",
            "/preview",
            "/help",
            "/learn",
            "/assessments",
            "/missions",
            "/cyber-lab",
            "/red-blue",
            "/workshops",
          ].includes(url.pathname),
        );
        assert.equal(
          activityJourney(url.pathname, url.search),
          `/journey?stage=${stage.id}&pathway=${audience.id}`,
        );
        assert.ok(resource.title && resource.description && resource.kind);
        if (url.pathname === "/red-blue") {
          assert.ok(
            fs.existsSync(
              path.join(
                __dirname,
                "../../api/cyber_warfare/scenarios",
                url.searchParams.get("scenario") + ".json",
              ),
            ) || url.hash === "#saved-matches",
          );
        }
      }
    }
});
test("untrusted navigation choices fall back without accepting redirects or arbitrary roles", () => {
  assert.deepEqual(parseJourney("?stage=javascript:alert(1)&pathway=admin"), {
    stage: "discover",
    audience: "all",
  });
  assert.equal(
    activityJourney(
      "/missions",
      "?journey_stage=x&journey_pathway=teacher&returnTo=https://evil.invalid",
    ),
    "/journey?stage=investigate&pathway=all",
  );
  assert.deepEqual(parseJourney("?stage=command&pathway=professional"), {
    stage: "command",
    audience: "professional",
  });
});
test("audience recommendations cover real missions and optional study without hiding advanced stages", () => {
  assert.equal(
    new URL(
      resourcesFor("investigate", "university")[0].href,
      "https://educyber.invalid",
    ).searchParams.get("pathway"),
    "university",
  );
  const study = resourcesFor("understand", "secondary");
  assert.ok(study.some((r) => r.title === "Digital Citizenship Essentials"));
  assert.ok(
    resourcesFor("understand", "university").some(
      (r) => r.title.includes("Python") && r.kind.includes("Optional"),
    ),
  );
  assert.ok(
    resourcesFor("command", "university").some(
      (r) => r.title === "Branch Siege",
    ),
  );
  assert.ok(
    resourcesFor("compete", "secondary").some(
      (r) =>
        new URL(r.href, "https://educyber.invalid").searchParams.get("mode") ===
        "human",
    ),
  );
});

test("Discover recommendations visibly differ across the three learning audiences", () => {
  const ids = ["secondary", "university", "professional"];
  const first = ids.map(id => resourcesFor("discover", id)[0]);
  assert.equal(new Set(first.map(item => item.title)).size, 3);
  assert.equal(new Set(first.map(item => new URL(item.href,"https://educyber.invalid").searchParams.get("pathway"))).size, 3);
  for (const id of ids) assert.ok(resourcesFor("discover",id).some(r => r.href.startsWith("/preview?")));
});

test("core content is distinct across pathways at every stage, with actual source catalogue targets", () => {
  const pathways = ["secondary", "university", "professional"];
  const cases = JSON.parse(fs.readFileSync(path.join(__dirname, "../../api/content/journey_workshops_v1.json"), "utf8"));
  const allocatedCases = [], allocatedTopics = [], allocatedScenarios = [];
  for (const pathway of pathways) {
    const content = PATHWAY_CONTENT[pathway];
    allocatedTopics.push(...content.topics);
    allocatedScenarios.push(content.computer, content.final);
    for (const stage of STAGES) {
      const id = workshopFor(stage.id,pathway);
      const actual = cases.find(c => c.id === id);
      assert.ok(actual, `Missing workshop ${id}`);
      assert.equal(actual.stage,stage.id);
      assert.equal(workshopBelongsTo(id,pathway),true);
      allocatedCases.push(id);
      for (const other of pathways.filter(p=>p!==pathway)) assert.equal(workshopBelongsTo(id,other),false);
    }
    const moduleSource = fs.readFileSync(path.join(__dirname,"../../api/cyber_content.py"),"utf8");
    assert.ok(moduleSource.includes(`'id': '${content.module}'`));
    const moduleRecord = moduleSource.split(`'id': '${content.module}'`)[1].split("'example'")[0];
    for (const topic of content.topics) assert.ok(moduleRecord.includes(`'${topic}'`));
  }
  assert.equal(new Set(allocatedCases).size,24);
  assert.equal(new Set(allocatedTopics).size,10);
  assert.equal(new Set(allocatedScenarios).size,6);
  function identity(resource) {
    const url = new URL(resource.href,"https://educyber.invalid");
    url.searchParams.delete("journey_stage");url.searchParams.delete("journey_pathway");
    return url.pathname + "?" + url.searchParams.toString();
  }
  for (const stage of STAGES) {
    const sets = pathways.map(p=>new Set(resourcesFor(stage.id,p).filter(r=>!r.kind.includes("Saved history")).map(identity)));
    for(let a=0;a<sets.length;a++) for(let b=a+1;b<sets.length;b++)
      assert.deepEqual([...sets[a]].filter(id=>sets[b].has(id)),[],`Repeated ${stage.id} materials`);
  }
  assert.equal(nextPathway("secondary"),"university");assert.equal(nextPathway("university"),"professional");
  assert.equal(nextPathway("professional"),null);assert.equal(workshopFor("check","all"),null);
});

test("pathway introductions use eighteen distinct explained questions and safe fallback", () => {
  const quizFile=path.join(__dirname,"../lib/preview-quiz.ts"),quiz=new Module(quizFile,module);
  quiz._compile(ts.transpileModule(fs.readFileSync(quizFile,"utf8"),{compilerOptions:{module:ts.ModuleKind.CommonJS}}).outputText,quizFile);
  const {previewFor}=quiz.exports;
  const prompts=[];
  for(const pathway of ["secondary","university","professional"]) {
    const rows=previewFor(pathway);assert.equal(rows.length,6);
    for(const q of rows){assert.equal(q.answers.length,3);assert.ok(q.correct>=0&&q.correct<3);assert.ok(q.explanation.length>30);prompts.push(q.q);}
  }
  assert.equal(new Set(prompts).size,18);
  assert.equal(previewFor("admin"),previewFor("all"));
});
