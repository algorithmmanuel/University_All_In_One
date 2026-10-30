// Actual HTTP API and persisted database state; never intercept responses here.
const { test, after } = require("node:test");
const assert = require("node:assert/strict");
const { chromium } = require("playwright");
const WEB = process.env.EDUCYBER_E2E_WEB_URL || "http://127.0.0.1:3100";
const API = process.env.EDUCYBER_E2E_API_URL || "http://127.0.0.1:8000";
const TOKEN = process.env.EDUCYBER_E2E_TOKEN;
if (!TOKEN) throw new Error("An isolated synthetic test session is required");
let browser;
after(async () => {
  if (browser) await browser.close();
});
for (const mobile of [false, true])
  test(`Branch Defender saved strategy, learning and practice; mobile=${mobile}`, async (t) => {
    browser ||= await chromium.launch({
      headless: true,
      args: ["--disable-dev-shm-usage"],
    });
    const context = await browser.newContext({
      baseURL: WEB,
      viewport: mobile
        ? { width: 390, height: 844 }
        : { width: 1440, height: 1000 },
      reducedMotion: "reduce",
    });
    t.after(() => context.close());
    await context.addInitScript(
      (token) => sessionStorage.setItem("educyber_token", token),
      TOKEN,
    );
    const page = await context.newPage(),
      errors = [];
    page.on("pageerror", (e) => errors.push(e.message));
    const headers = { Authorization: "Bearer " + TOKEN };
    const api = async (path) =>
      await (
        await page.request.get(API + "/api/v1/cyber-lab" + path, { headers })
      ).json();
    await page.goto("/dashboard");
    await page
      .getByRole("link", { name: "Play Branch Defender →", exact: true })
      .click();
    await page
      .getByRole("button", { name: "Start a new shift →", exact: true })
      .click();
    const game = page.getByRole("region", { name: "Branch Defender game" });
    await game
      .getByRole("heading", { name: "Protect the branch.", exact: true })
      .waitFor();
    const created = (await api("/runs")).runs[0];
    for (const [asset, action, expected] of [
      ["Identity service", "Strengthen sign-in", "✓ Sign-in protected"],
      ["Banking application", "Patch system", "Maintenance: patch"],
      ["Recovery vault", "Verify recovery copy", "Maintenance: backup"],
    ]) {
      await game
        .getByRole("button", { name: new RegExp("^" + asset + ":") })
        .click();
      await game
        .getByRole("button", { name: new RegExp("^" + action) })
        .click();
      await game.getByText(expected, { exact: true }).waitFor();
    }
    if (process.env.EDUCYBER_SCREENSHOT_DIR)
      await game.screenshot({
        path:
          process.env.EDUCYBER_SCREENSHOT_DIR +
          `/branch-defender-${mobile ? "mobile" : "desktop"}.png`,
      });
    await page.reload();
    await page
      .getByRole("button", { name: new RegExp(`^Shift #${created.id}\\b`) })
      .click();
    for (let turn = 2; turn <= 8; turn++) {
      const response = page.waitForResponse(
        (r) =>
          r.url().includes(`/runs/${created.id}/commands`) &&
          r.request().method() === "POST",
      );
      await game
        .getByRole("button", { name: "Advance turn →", exact: true })
        .click();
      assert.equal((await response).status(), 200);
      await game.getByText(`${turn}/18 turns`, { exact: true }).waitFor();
    }
    await game
      .getByRole("heading", { name: "After-action review", exact: true })
      .waitFor();
    const saved = await api("/runs/" + created.id);
    assert.equal(saved.status, "won");
    assert.equal(saved.budget, 19);
    await page.getByRole("button", { name: "02 / Learn", exact: true }).click();
    await page
      .getByRole("heading", { name: "Protect the branch", exact: true })
      .waitFor();
    const complete = page.getByRole("button", {
      name: "Mark module complete",
      exact: true,
    });
    if (await complete.count()) await complete.click();
    await page
      .getByRole("button", { name: "Module completed ✓", exact: true })
      .waitFor();
    await page
      .getByRole("button", { name: "03 / Practise", exact: true })
      .click();
    await page.getByLabel("Topic", { exact: true }).selectOption("identity");
    await page.getByLabel("Questions", { exact: true }).fill("5");
    await page
      .getByRole("button", { name: "Start practice →", exact: true })
      .click();
    const questions = page.locator("fieldset");
    await questions.first().waitFor();
    assert.equal(await questions.count(), 5);
    for (let i = 0; i < 5; i++)
      await questions.nth(i).getByRole("radio").first().check();
    await page
      .getByRole("button", { name: "Submit practice answers", exact: true })
      .click();
    const notice =
      "This practice sample is not a certification or a complete measure of topic mastery.";
    await page.getByText(notice, { exact: true }).waitFor();
    const sessions = await api("/practice");
    assert.equal(sessions.sessions[0].completed, true);
    await page.reload();
    await page
      .getByRole("button", { name: "03 / Practise", exact: true })
      .click();
    await page
      .getByRole("button", {
        name: new RegExp(`^Practice #${sessions.sessions[0].id}\\b`),
      })
      .click();
    await page.getByText(notice, { exact: true }).waitFor();
    assert.deepEqual(errors, []);
    assert.equal(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
      true,
    );
  });

for (const scenario of ["supplier", "ransomware"])
  for (const mobile of [false, true])
    test(`Build B scenario ${scenario}; mobile=${mobile}`, async (t) => {
      browser ||= await chromium.launch({
        headless: true,
        args: ["--disable-dev-shm-usage"],
      });
      const context = await browser.newContext({
        baseURL: WEB,
        viewport: mobile
          ? { width: 390, height: 844 }
          : { width: 1440, height: 1000 },
        reducedMotion: "reduce",
      });
      t.after(() => context.close());
      await context.addInitScript(
        (token) => sessionStorage.setItem("educyber_token", token),
        TOKEN,
      );
      const page = await context.newPage(),
        errors = [];
      page.on("pageerror", (e) => errors.push(e.message));
      await page.goto("/cyber-lab");
      await page.getByLabel("Scenario", { exact: true }).selectOption(scenario);
      await page
        .getByRole("button", { name: "Start a new shift →", exact: true })
        .click();
      const game = page.getByRole("region", { name: "Branch Defender game" });
      await game
        .getByRole("heading", {
          name:
            scenario === "supplier"
              ? "Supplier Access Crisis"
              : "Recovery Under Pressure",
          exact: true,
        })
        .waitFor();
      const act = async (asset, action) => {
        await game
          .getByRole("button", { name: new RegExp("^" + asset + ":") })
          .click();
        const reply = page.waitForResponse(
          (r) =>
            r.url().includes("/commands") && r.request().method() === "POST",
        );
        await game
          .getByRole("button", { name: new RegExp("^" + action) })
          .click();
        assert.equal((await reply).status(), 200);
        await game
          .getByRole("button", { name: "Advance turn →", exact: true })
          .waitFor({ state: "visible" });
      };
      const next = async (turn) => {
        await game
          .getByRole("button", { name: "Advance turn →", exact: true })
          .click();
        await game.getByText(`${turn}/18 turns`, { exact: true }).waitFor();
      };
      let turn = 1;
      if (scenario === "supplier") {
        await act("Branch gateway", "Revoke supplier access");
        await game
          .getByText("✓ Supplier access revoked", { exact: true })
          .waitFor();
        await act("Recovery vault", "Verify recovery copy");
      } else {
        for (const asset of [
          "Staff workstation",
          "Banking application",
          "Customer database",
        ])
          await act(asset, "Isolate asset");
        await next(++turn);
        for (const [asset, action] of [
          ["Recovery vault", "Verify recovery copy"],
          ["Staff workstation", "Patch system"],
          ["Banking application", "Patch system"],
        ])
          await act(asset, action);
        await next(++turn);
        for (const asset of [
          "Staff workstation",
          "Banking application",
          "Customer database",
        ])
          await act(asset, "Restore asset");
        await next(++turn);
        for (const asset of [
          "Staff workstation",
          "Banking application",
          "Customer database",
        ])
          await act(asset, "Reconnect asset");
      }
      const target = scenario === "supplier" ? 10 : 8;
      while (turn < target) await next(++turn);
      await game
        .getByRole("heading", { name: "After-action review", exact: true })
        .waitFor();
      const headers = { Authorization: "Bearer " + TOKEN };
      const list = await (
        await page.request.get(API + "/api/v1/cyber-lab/runs", { headers })
      ).json();
      const saved = await (
        await page.request.get(
          API + "/api/v1/cyber-lab/runs/" + list.runs[0].id,
          { headers },
        )
      ).json();
      assert.equal(saved.scenario, scenario);
      assert.equal(saved.status, "won");
      await page.reload();
      await page
        .getByRole("button", { name: new RegExp(`^Shift #${saved.id}\\b`) })
        .click();
      await game
        .getByRole("heading", { name: "After-action review", exact: true })
        .waitFor();
      assert.deepEqual(errors, []);
    });

test("Build B saved mistake review uses actual graded evidence", async (t) => {
  const { execFileSync } = require("node:child_process"),
    path = require("node:path");
  const keys = JSON.parse(
    execFileSync(
      process.env.EDUCYBER_TEST_PYTHON || "python3",
      [
        "-c",
        "import json;from cyber_content import BANK;print(json.dumps({q['id']:q['options'][q['answer']] for q in BANK}))",
      ],
      { cwd: path.resolve(__dirname, "../../../api"), encoding: "utf8" },
    ),
  );
  browser ||= await chromium.launch({
    headless: true,
    args: ["--disable-dev-shm-usage"],
  });
  const context = await browser.newContext({ baseURL: WEB });
  t.after(() => context.close());
  await context.addInitScript(
    (token) => sessionStorage.setItem("educyber_token", token),
    TOKEN,
  );
  const page = await context.newPage();
  const headers = { Authorization: "Bearer " + TOKEN };
  const started = await page.request.post(API + "/api/v1/cyber-lab/practice", {
    headers,
    data: { topic: "governance", difficulty: "challenging", count: 1 },
  });
  assert.equal(started.status(), 201);
  const first = await started.json(),
    q = first.questions[0];
  const wrong = q.options.findIndex((option) => option !== keys[q.id]);
  const graded = await page.request.post(
    API + `/api/v1/cyber-lab/practice/${first.id}/submit`,
    { headers, data: { answers: { [q.id]: wrong } } },
  );
  assert.equal(graded.status(), 200);
  await page.goto("/cyber-lab?tab=practice");
  await page.getByLabel("Topic", { exact: true }).selectOption("governance");
  await page
    .getByLabel("Difficulty", { exact: true })
    .selectOption("challenging");
  await page
    .getByLabel("Practice mode", { exact: true })
    .selectOption("mistakes");
  await page.getByLabel("Questions", { exact: true }).fill("1");
  await page
    .getByRole("button", { name: "Start practice →", exact: true })
    .click();
  const field = page.locator("fieldset").first();
  await field.waitFor();
  // Review is selected from actual incorrect verdicts, not invented weaknesses.
  const sessionId = Number(
    (
      await page.getByRole("heading", { name: /^Practice #/ }).textContent()
    ).split("#")[1],
  );
  const review = await (
    await page.request.get(API + `/api/v1/cyber-lab/practice/${sessionId}`, {
      headers,
    })
  ).json();
  const selected = review.questions[0];
  await field
    .getByRole("radio", { name: keys[selected.id], exact: true })
    .check();
  await page
    .getByRole("button", { name: "Submit practice answers", exact: true })
    .click();
  await page
    .getByText(
      "This practice sample is not a certification or a complete measure of topic mastery.",
      { exact: true },
    )
    .waitFor();
  assert.ok(
    (
      await (
        await page.request.get(
          API + `/api/v1/cyber-lab/practice/${sessionId}`,
          { headers },
        )
      ).json()
    ).result.feedback[0].correct,
  );
});

for (const mobile of [false, true])
  test(`Build C campaign, reflection, 500-question bank and keyboard asset list; mobile=${mobile}`, async (t) => {
    browser ||= await chromium.launch({
      headless: true,
      args: ["--disable-dev-shm-usage"],
    });
    const context = await browser.newContext({
      baseURL: WEB,
      viewport: mobile
        ? { width: 390, height: 844 }
        : { width: 1440, height: 1000 },
      reducedMotion: "reduce",
    });
    t.after(() => context.close());
    await context.addInitScript(
      (token) => sessionStorage.setItem("educyber_token", token),
      TOKEN,
    );
    const page = await context.newPage(),
      errors = [];
    page.on("pageerror", (error) => errors.push(error.message));
    const headers = { Authorization: "Bearer " + TOKEN };
    const get = async (path) =>
      (
        await page.request.get(API + "/api/v1/cyber-lab" + path, { headers })
      ).json();
    await page.goto("/cyber-lab");
    const campaign = page.getByRole("region", {
      name: "Your campaign",
      exact: true,
    });
    await campaign.waitFor();
    if (process.env.EDUCYBER_SCREENSHOT_DIR)
      await campaign.screenshot({
        path:
          process.env.EDUCYBER_SCREENSHOT_DIR +
          `/build-c-campaign-${mobile ? "mobile" : "desktop"}.png`,
      });
    const catalog = await get("/catalog");
    assert.equal(catalog.question_count, 500);
    assert.equal(catalog.campaign.chapters.length, 4);
    assert.ok(
      catalog.topics.every(
        (topic) =>
          topic.count === 50 &&
          topic.counts.foundational === 20 &&
          topic.counts.challenging === 10,
      ),
    );
    const first = campaign.locator("ol > li").first();
    const step = catalog.campaign.chapters[0].next;
    await first
      .getByRole("button", { name: step.label + " →", exact: true })
      .click();
    if (step.kind === "learn")
      await page
        .getByRole("heading", {
          name: "Cybersecurity learning modules",
          exact: true,
        })
        .waitFor();
    else if (step.kind === "practice")
      await page
        .getByRole("heading", { name: "Cybersecurity practice", exact: true })
        .waitFor();
    else
      assert.equal(
        await page.getByLabel("Scenario", { exact: true }).inputValue(),
        "branch",
      );
    await page.getByRole("button", { name: "02 / Learn", exact: true }).click();
    await page
      .getByRole("button", { name: /Defend connected services/ })
      .click();
    const section = page.locator("#topic-application");
    const before = await get("/practice");
    await section
      .getByRole("radio", {
        name: "Observation of covered violations, not policy enforcement",
        exact: true,
      })
      .check();
    await section
      .getByRole("button", { name: "Check my reasoning", exact: true })
      .click();
    await section.getByText(/That fits the evidence/).waitFor();
    assert.deepEqual(await get("/practice"), before);
    if (process.env.EDUCYBER_SCREENSHOT_DIR)
      await section.screenshot({
        path:
          process.env.EDUCYBER_SCREENSHOT_DIR +
          `/build-c-lesson-${mobile ? "mobile" : "desktop"}.png`,
      });
    await section
      .getByText("Explore 50 worked decisions", { exact: true })
      .click();
    await section
      .getByRole("button", { name: "Next decisions", exact: true })
      .click();
    await section.getByText("Decisions 6–10 of 50", { exact: true }).waitFor();
    await section
      .getByRole("button", { name: "Practise this topic →", exact: true })
      .click();
    assert.equal(
      await page.getByLabel("Topic", { exact: true }).inputValue(),
      "application",
    );
    await page
      .getByLabel("Difficulty", { exact: true })
      .selectOption("foundational");
    await page.getByText("20 eligible questions.", { exact: true }).waitFor();
    await page.getByRole("button", { name: "01 / Play", exact: true }).click();
    await page
      .getByLabel("Scenario", { exact: true })
      .selectOption("ransomware");
    await page
      .getByRole("button", { name: "Start a new shift →", exact: true })
      .click();
    const game = page.getByRole("region", {
      name: "Branch Defender game",
      exact: true,
    });
    await game.getByRole("button", { name: "Asset list", exact: true }).click();
    const application = game.getByRole("button", {
      name: /^Banking application:/,
    });
    await application.focus();
    await page.keyboard.press("Enter");
    const controls = game.getByRole("complementary", {
      name: "Selected asset controls",
      exact: true,
    });
    await controls
      .getByRole("heading", { name: "Banking application", exact: true })
      .waitFor();
    const reply = page.waitForResponse(
      (response) =>
        response.url().includes("/commands") &&
        response.request().method() === "POST",
    );
    const isolate = controls.getByRole("button", { name: /^Isolate asset/ });
    await isolate.focus();
    await page.keyboard.press("Enter");
    assert.equal((await reply).status(), 200);
    await controls.getByText(/Service encrypted/).waitFor();
    const latest = (await get("/runs")).runs[0];
    assert.equal(
      (await get("/runs/" + latest.id)).assets.find(
        (asset) => asset.id === "app",
      ).isolated,
      true,
    );
    assert.equal(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
      true,
    );
    if (process.env.EDUCYBER_SCREENSHOT_DIR)
      await game.screenshot({
        path:
          process.env.EDUCYBER_SCREENSHOT_DIR +
          `/build-c-list-${mobile ? "mobile" : "desktop"}.png`,
      });
    await page.reload();
    await page
      .getByRole("button", { name: new RegExp(`^Shift #${latest.id}\\b`) })
      .click();
    await game.getByRole("button", { name: "Asset list", exact: true }).click();
    await application.focus();
    await page.keyboard.press("Enter");
    await controls.getByText(/isolated/).waitFor();
    assert.deepEqual(errors, []);
  });

for (const mobile of [false, true])
  test(`Branch Siege investigations, consequential recovery and same-incident replay; mobile=${mobile}`, async (t) => {
    browser ||= await chromium.launch({
      headless: true,
      args: ["--disable-dev-shm-usage"],
    });
    const context = await browser.newContext({
      baseURL: WEB,
      viewport: mobile
        ? { width: 390, height: 844 }
        : { width: 1440, height: 1000 },
      reducedMotion: "reduce",
    });
    t.after(() => context.close());
    await context.addInitScript(
      (token) => sessionStorage.setItem("educyber_token", token),
      TOKEN,
    );
    const page = await context.newPage(),
      errors = [];
    page.on("pageerror", (error) => errors.push(error.message));
    await page.goto("/cyber-lab?scenario=siege");
    await page.getByLabel("Scenario", { exact: true }).waitFor();
    assert.equal(
      await page.getByLabel("Scenario", { exact: true }).inputValue(),
      "siege",
    );
    const startReply = page.waitForResponse(
      (r) =>
        r.url().endsWith("/api/v1/cyber-lab/runs") &&
        r.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "Start a new shift →", exact: true })
      .click();
    let run = await (await startReply).json();
    const firstId = run.id,
      opening = structuredClone(run.tactics.signals);
    const game = page.getByRole("region", {
      name: "Branch Defender game",
      exact: true,
    });
    await game
      .getByRole("heading", { name: "Branch Siege", exact: true })
      .waitFor();
    if (process.env.EDUCYBER_SCREENSHOT_DIR)
      await game
        .locator('[aria-label="Interactive branch network"]')
        .screenshot({
          path:
            process.env.EDUCYBER_SCREENSHOT_DIR +
            `/siege-map-${mobile ? "mobile" : "desktop"}.png`,
        });

    const ready = async () =>
      page.waitForFunction(() =>
        [...document.querySelectorAll("button")].some(
          (b) => b.textContent === "Reload saved run" && !b.disabled,
        ),
      );
    const commandButton = async (button) => {
      const reply = page.waitForResponse(
        (r) =>
          r.url().includes(`/runs/${run.id}/commands`) &&
          r.request().method() === "POST",
      );
      await button.click();
      const response = await reply;
      assert.equal(response.status(), 200);
      run = await response.json();
      await ready();
    };
    const support = async () =>
      commandButton(
        game.getByRole("button", {
          name: "Mobilise emergency support · 6 credits",
          exact: true,
        }),
      );
    const act = async (assetId, action) => {
      const asset = run.assets.find((a) => a.id === assetId);
      await game
        .getByRole("button", { name: new RegExp("^" + asset.label + ":") })
        .click();
      await commandButton(
        game
          .getByRole("complementary", {
            name: "Selected asset controls",
            exact: true,
          })
          .getByRole("button", { name: new RegExp("^" + action) }),
      );
    };
    const next = async () =>
      commandButton(
        game.getByRole("button", { name: "Advance turn →", exact: true }),
      );
    await support();
    for (const signal of opening)
      await commandButton(
        game.getByRole("button", {
          name: `Investigate ${signal.id} · 1 staff`,
          exact: true,
        }),
      );
    const affected = run.assets.find(
      (asset) => asset.condition === "Compromise detected",
    ).id;
    await game.getByText(/Latest finding:/).waitFor();
    const latestLabel = run.assets.find(
      (asset) => asset.id === opening[1].asset,
    ).label;
    await game
      .getByRole("button", {
        name: "Open " + latestLabel + " controls",
        exact: true,
      })
      .click();
    await page.waitForFunction(
      () =>
        document.activeElement?.getAttribute("aria-label") ===
        "Selected asset controls",
    );

    await game.getByRole("button", { name: "Asset list", exact: true }).click();
    await act(affected, "Isolate asset");
    await act("app", "Patch system");
    if (affected === "staff") await act("remote", "Revoke supplier access");
    else await act("identity", "Strengthen sign-in");
    if (process.env.EDUCYBER_SCREENSHOT_DIR)
      await game
        .getByRole("region", { name: "Incident command console", exact: true })
        .screenshot({
          path:
            process.env.EDUCYBER_SCREENSHOT_DIR +
            `/siege-console-${mobile ? "mobile" : "desktop"}.png`,
        });
    await next();
    if (!run.mfa) await act("identity", "Strengthen sign-in");
    if (!run.vendor_revoked) await act("remote", "Revoke supplier access");
    await act("backup", "Verify recovery copy");
    while (run.turn < 4) await next();
    await act(affected, "Restore asset");
    await act("app", "Validate recovery");
    await act("database", "Validate recovery");
    // Reopening must retain due turns, the investigation queue and resource spending.
    const version = run.version;
    await page.reload();
    await page
      .getByRole("button", { name: new RegExp(`^Shift #${firstId}\\b`) })
      .click();
    const saved = await (
      await page.request.get(API + `/api/v1/cyber-lab/runs/${firstId}`, {
        headers: { Authorization: "Bearer " + TOKEN },
      })
    ).json();
    assert.equal(saved.version, version);
    assert.equal(saved.assets.find((a) => a.id === affected).due_turn, 6);
    await game.getByRole("button", { name: "Asset list", exact: true }).click();
    while (run.turn < 6) await next();
    await act(affected, "Validate recovery");
    await act(affected, "Reconnect asset");
    while (run.status === "active") await next();
    assert.equal(run.status, "won");
    assert.equal(run.budget, 13);
    const outcome = game.getByRole("region", {
      name: "Incident outcome comparison",
      exact: true,
    });
    await outcome.waitFor();
    if (process.env.EDUCYBER_SCREENSHOT_DIR)
      await outcome.screenshot({
        path:
          process.env.EDUCYBER_SCREENSHOT_DIR +
          `/siege-review-${mobile ? "mobile" : "desktop"}.png`,
      });
    const replayReply = page.waitForResponse(
      (r) =>
        r.url().endsWith("/api/v1/cyber-lab/runs") &&
        r.request().method() === "POST",
    );
    await outcome
      .getByRole("button", { name: "Replay the same incident →", exact: true })
      .click();
    run = await (await replayReply).json();
    await ready();
    assert.equal(run.replay_of, firstId);
    assert.deepEqual(run.tactics.signals, opening);
    assert.equal(run.budget, 38);
    assert.equal("seed" in run, false);
    await game.getByRole("button", { name: "Asset list", exact: true }).click();
    await support();
    for (const asset of ["staff", "remote"]) await act(asset, "Isolate asset");
    await act("identity", "Strengthen sign-in");
    await act("app", "Patch system");
    await act("remote", "Revoke supplier access");
    await next();
    await act("backup", "Verify recovery copy");
    while (run.turn < 4) await next();
    for (const asset of ["staff", "remote"]) await act(asset, "Restore asset");
    await act("app", "Validate recovery");
    while (run.turn < 6) await next();
    for (const asset of ["staff", "remote", "database"])
      await act(asset, "Validate recovery");
    await next();
    for (const asset of ["staff", "remote"])
      await act(asset, "Reconnect asset");
    while (run.status === "active") await next();
    assert.equal(run.status, "won");
    assert.equal(run.budget, 9);
    assert.equal(run.debrief.metrics.credits_spent, 29);
    assert.equal(run.debrief.comparison.credits_spent, 25);
    assert.equal(run.debrief.metrics.signals_reviewed, 0);
    assert.equal(run.debrief.comparison.signals_reviewed, 2);
    await outcome
      .getByRole("table", {
        name: "Same opening: previous attempt versus this attempt",
        exact: true,
      })
      .waitFor();
    await page.reload();
    await page
      .getByRole("button", { name: new RegExp(`^Shift #${run.id}\\b`) })
      .click();
    await outcome
      .getByRole("table", {
        name: "Same opening: previous attempt versus this attempt",
        exact: true,
      })
      .waitFor();
    assert.equal(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
      true,
    );
    assert.deepEqual(errors, []);
  });
