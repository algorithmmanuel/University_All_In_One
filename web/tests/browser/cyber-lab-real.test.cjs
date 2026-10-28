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
      await page.getByRole("link", {name: "Play Branch Defender →", exact: true}).click();
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
