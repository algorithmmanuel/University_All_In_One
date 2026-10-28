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
