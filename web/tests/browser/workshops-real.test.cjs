// Real API/state; only the retry case drops a response after a real commit.
const { test, after } = require("node:test");
const assert = require("node:assert/strict");
const { chromium } = require("playwright");
const WEB = process.env.EDUCYBER_E2E_WEB_URL || "http://127.0.0.1:3100",
  API = process.env.EDUCYBER_E2E_API_URL || "http://127.0.0.1:8000",
  TOKEN = process.env.EDUCYBER_E2E_TOKEN;
if (!TOKEN) throw Error("An isolated synthetic learner is required");
let browser;
after(async () => {
  if (browser) await browser.close();
});
async function setup(t, mobile) {
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
    (t) => sessionStorage.setItem("educyber_token", t),
    TOKEN,
  );
  return ctx.newPage();
}
for (const mobile of [false, true])
  test(`EduCyber decision workshop: complete, reopen and compare; mobile=${mobile}`, async (t) => {
    const page = await setup(t, mobile),
      errors = [];
    page.on("pageerror", (e) => errors.push(e.message));
    await page.goto("/journey?stage=command&pathway=secondary");
    await page
      .getByRole("link", {
        name: "Open The reconnection decision →",
        exact: true,
      })
      .click();
    await page
      .getByRole("heading", { name: "Decision workshop library", exact: true })
      .waitFor();
    assert.equal(
      await page.title(),
      "EduCyber | Learn. Practise. Build. Secure.",
    );
    const created = page.waitForResponse(
      (r) =>
        r.url().endsWith("/api/v1/workshops/runs") &&
        r.request().method() === "POST",
    );
    await page
      .getByRole("button", { name: "Start saved workshop", exact: true })
      .click();
    let run = await (await created).json();
    const area = page.getByRole("region", { name: "Workshop workspace" });
    const choose = async (id) => {
      const response = page.waitForResponse((r) =>
        r.url().endsWith(`/workshops/runs/${run.id}/decisions`),
      );
      await area
        .getByRole("button", {
          name: new RegExp(
            run.step.choices
              .find((c) => c.id === id)
              .label.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
          ),
        })
        .click();
      run = await (await response).json();
    };
    await choose("b");
    await page.reload();
    await page
      .getByRole("button", {
        name: new RegExp(`Resume decision 2 · workshop ${run.id}`),
      })
      .click();
    for (const id of ["a", "a"]) await choose(id);
    await page
      .getByRole("heading", { name: "Your case review", exact: true })
      .waitFor();
    assert.equal(run.unresolved.length, 1);
    if (process.env.EDUCYBER_SCREENSHOT_DIR)
      await page.screenshot({
        path:
          process.env.EDUCYBER_SCREENSHOT_DIR +
          `/workshop-review-${mobile ? "mobile" : "desktop"}.png`,
        fullPage: true,
      });
    const replayed = page.waitForResponse(
      (r) =>
        r.url().endsWith("/api/v1/workshops/runs") &&
        r.request().method() === "POST",
    );
    await page
      .getByRole("button", {
        name: "Replay and compare another approach",
        exact: true,
      })
      .click();
    run = await (await replayed).json();
    for (const id of ["a", "a", "a"]) await choose(id);
    await page
      .getByRole("heading", {
        name: "Compared with your previous approach",
        exact: true,
      })
      .waitFor();
    assert.equal(run.unresolved.length, 0);
    assert.equal(run.baseline.unresolved.length, 1);
    assert.equal(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
      true,
    );
    const body = await page.locator("body").innerText();
    assert.equal(body.includes("EduCyber Nigeria"), false);
    assert.deepEqual(errors, []);
  });
test("workshop lost response retries the same UUID without duplicate findings", async (t) => {
  const page = await setup(t, false);
  await page.goto("/workshops?case=scholarship-pressure");
  const created = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/v1/workshops/runs") &&
      r.request().method() === "POST",
  );
  await page
    .getByRole("button", { name: "Start saved workshop", exact: true })
    .click();
  const run = await (await created).json();
  const requests = [];
  page.on("request", (r) => {
    if (r.url().endsWith(`/workshops/runs/${run.id}/decisions`))
      requests.push(r.postDataJSON());
  });
  const pattern = "**/api/v1/workshops/runs/*/decisions";
  await page.route(pattern, async (route) => {
    assert.equal((await route.fetch()).status(), 200);
    await route.abort("failed");
  });
  const label = run.step.choices.find((c) => c.id === "a").label;
  await page
    .getByRole("region", { name: "Workshop workspace" })
    .getByRole("button", { name: new RegExp(label) })
    .click();
  await page
    .getByRole("button", { name: "Retry same decision", exact: true })
    .waitFor();
  await page.unroute(pattern);
  const response = page.waitForResponse((r) =>
    r.url().endsWith(`/workshops/runs/${run.id}/decisions`),
  );
  await page
    .getByRole("button", { name: "Retry same decision", exact: true })
    .click();
  const saved = await (await response).json();
  assert.equal(saved.step_index, 1);
  assert.equal(saved.findings.length, 1);
  assert.deepEqual(requests[0], requests[1]);
  const direct = await page.request.get(
    API + `/api/v1/workshops/runs/${run.id}`,
    { headers: { Authorization: "Bearer " + TOKEN } },
  );
  assert.equal((await direct.json()).step_index, 1);
});
