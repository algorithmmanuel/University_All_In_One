// Real APIs and existing saved progress, without response interception.
const { test, after } = require("node:test");
const assert = require("node:assert/strict");
const { chromium } = require("playwright");
const WEB = process.env.EDUCYBER_E2E_WEB_URL || "http://127.0.0.1:3100",
  API = process.env.EDUCYBER_E2E_API_URL || "http://127.0.0.1:8000",
  TOKEN = process.env.EDUCYBER_E2E_TOKEN;
if (!TOKEN) throw Error("Isolated synthetic learner required");
let browser;
after(async () => {
  if (browser) await browser.close();
});
for (const mobile of [false, true])
  test(`journey to actual study, practice and match settings; mobile=${mobile}`, async (t) => {
    browser ||= await chromium.launch({
      headless: true,
      args: ["--disable-dev-shm-usage"],
    });
    const ctx = await browser.newContext({
      baseURL: WEB,
      reducedMotion: "reduce",
      viewport: mobile
        ? { width: 390, height: 844 }
        : { width: 1440, height: 1000 },
    });
    t.after(() => ctx.close());
    await ctx.addInitScript(
      (token) => sessionStorage.setItem("educyber_token", token),
      TOKEN,
    );
    const page = await ctx.newPage(),
      writes = [],
      errors = [];
    page.on("request", (r) => {
      if (r.method() === "POST") writes.push(r.url());
    });
    page.on("pageerror", (e) => errors.push(e.message));
    await page.goto("/dashboard");
    await page
      .getByRole("link", { name: "Open your learning journey →", exact: true })
      .click();
    await page.getByRole("button", { name: /Cyber Academy/ }).click();
    await page
      .getByRole("navigation", { name: "Choose your starting stage" })
      .getByRole("button", { name: "4 Investigate with guidance", exact: true })
      .click();
    await page
      .getByRole("link", {
        name: "Open Cyber Academy investigations →",
        exact: true,
      })
      .click();
    await page
      .getByRole("heading", { name: "Cyber Academy game library", exact: true })
      .waitFor();
    await page
      .getByRole("link", { name: "Learning journey", exact: true })
      .click();
    await page
      .getByRole("navigation", { name: "Choose your starting stage" })
      .getByRole("button", { name: "3 Check understanding", exact: true })
      .click();
    await page.getByRole("link", { name: /Open Practise networks/ }).click();
    await page.getByLabel("Topic", { exact: true }).waitFor();
    assert.equal(
      await page.getByLabel("Topic", { exact: true }).inputValue(),
      "network",
    );
    assert.equal(
      await page.getByLabel("Difficulty", { exact: true }).inputValue(),
      "foundational",
    );
    await page
      .getByRole("link", { name: "Learning journey", exact: true })
      .click();
    await page
      .getByRole("heading", { name: "Check understanding", exact: true })
      .waitFor();
    assert.equal(
      await page
        .getByRole("button", { name: /Cyber Academy/ })
        .getAttribute("aria-pressed"),
      "true",
    );
    await page
      .getByRole("navigation", { name: "Choose your starting stage" })
      .getByRole("button", { name: "7 Face an adaptive opponent", exact: true })
      .click();
    await page
      .getByRole("link", {
        name: "Open Start a Red / Blue computer match →",
        exact: true,
      })
      .click();
    await page.getByLabel("Scenario", { exact: true }).waitFor();
    assert.equal(
      await page.getByLabel("Scenario", { exact: true }).inputValue(),
      "software_cloud",
    );
    assert.equal(
      await page
        .getByLabel("Computer difficulty", { exact: true })
        .inputValue(),
      "easy",
    );
    assert.equal(
      await page.getByLabel("Your seat", { exact: true }).inputValue(),
      "blue",
    );
    const pathLink = page
      .getByRole("navigation", { name: "Learning navigation" })
      .getByRole("link", { name: "Learning journey", exact: true });
    await pathLink.click();
    await page
      .getByRole("navigation", { name: "Choose your starting stage" })
      .getByRole("button", { name: "8 Compete and reflect", exact: true })
      .click();
    await page.getByRole("link", { name: /Open Create a two-learner/ }).click();
    await page.getByLabel("Opponent", { exact: true }).waitFor();
    assert.equal(
      await page.getByLabel("Opponent", { exact: true }).inputValue(),
      "human",
    );
    await page
      .getByRole("navigation", { name: "Learning navigation" })
      .getByRole("link", { name: "Learning journey", exact: true })
      .click();
    await page
      .getByRole("link", {
        name: "Open Revisit saved matches and debriefs →",
        exact: true,
      })
      .click();
    await page.waitForFunction(
      () => document.activeElement?.textContent === "Your saved matches",
    );
    assert.deepEqual(writes, []);
    assert.deepEqual(errors, []);
    const response = await page.request.get(API + "/api/v1/learning/overview", {
      headers: { Authorization: "Bearer " + TOKEN },
    });
    assert.equal(response.status(), 200);
  });
