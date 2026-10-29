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
const { STAGES, AUDIENCES, resourcesFor, parseJourney, activityJourney } =
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
            "/learn",
            "/assessments",
            "/missions",
            "/cyber-lab",
            "/red-blue",
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
    study.some(
      (r) => r.title.includes("Python") && r.kind.includes("Optional"),
    ),
  );
  assert.ok(
    resourcesFor("command", "secondary").some(
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
