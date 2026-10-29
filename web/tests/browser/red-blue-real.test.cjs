// Actual API/database journeys. Only the final recovery cases inject an interrupted
// response after the real API has committed; it never fabricates server state.
const { test, after } = require("node:test");
const assert = require("node:assert/strict");
const { chromium } = require("playwright");
const WEB = process.env.EDUCYBER_E2E_WEB_URL || "http://127.0.0.1:3100";
const API = process.env.EDUCYBER_E2E_API_URL || "http://127.0.0.1:8000";
const TOKEN = process.env.EDUCYBER_E2E_TOKEN;
if (!TOKEN) throw new Error("Isolated synthetic browser session required");
let browser;
after(async () => {
  if (browser) await browser.close();
});
async function context(t, token, mobile) {
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
    (value) => sessionStorage.setItem("educyber_token", value),
    token,
  );
  const page = await ctx.newPage();
  page.setDefaultTimeout(12000);
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  return { ctx, page, errors };
}
async function saved(page, id, token = TOKEN) {
  const response = await page.request.get(
    API + "/api/v1/red-blue/matches/" + id,
    { headers: { Authorization: "Bearer " + token } },
  );
  assert.equal(response.status(), 200);
  return response.json();
}
async function start(page, side, mode = "computer") {
  await page.goto("/red-blue");
  await page.getByLabel("Your seat", { exact: true }).selectOption(side);
  await page.getByLabel("Opponent", { exact: true }).selectOption(mode);
  const created = page.waitForResponse(
    (r) =>
      r.url().endsWith("/api/v1/red-blue/matches") &&
      r.request().method() === "POST",
  );
  await page.getByRole("button", { name: "Start match", exact: true }).click();
  const response = await created;
  assert.equal(response.status(), 201);
  const match = await response.json();
  await page.getByRole("heading", { name: match.title, exact: true }).waitFor();
  await page.waitForFunction(
    (title) => document.activeElement?.textContent === title,
    match.title,
  );
  return match;
}
async function submit(page, action) {
  await page.getByLabel(/^Action for /).selectOption({ label: action });
  const resolved = page.waitForResponse((r) =>
    /\/red-blue\/matches\/\d+\/commands$/.test(r.url()),
  );
  await page.getByRole("button", { name: "Seal choice", exact: true }).click();
  const response = await resolved;
  assert.equal(response.status(), 200);
  return response.json();
}
function waitLabel(side) {
  return `wait ${side} · 0 credits`;
}
async function shot(page, name) {
  if (process.env.EDUCYBER_SCREENSHOT_DIR)
    await page.screenshot({
      path: process.env.EDUCYBER_SCREENSHOT_DIR + "/" + name + ".png",
      fullPage: true,
    });
}
for (const mobile of [false, true])
  for (const side of ["red", "blue"])
    test(`Red Blue computer: ${side}, complete/resume/debrief, mobile=${mobile}`, async (t) => {
      const { page, errors } = await context(t, TOKEN, mobile);
      let match = await start(page, side);
      assert.equal(match.side, side);
      await page
        .getByRole("button", { name: "Asset list", exact: true })
        .click();
      assert.ok(await page.getByRole("button", { pressed: true }).count());
      const lastAsset = match.assets.at(-1);
      const assetButton = page
        .getByRole("region", { name: "Known assets" })
        .getByRole("button")
        .filter({ hasText: lastAsset.name })
        .last();
      await assetButton.focus();
      await page.keyboard.press("Enter");
      assert.equal(await assetButton.getAttribute("aria-pressed"), "true");
      if (!mobile) {
        await page
          .getByRole("button", { name: "Network", exact: true })
          .click();
        await shot(page, `red-blue-network-${side}`);
        await page
          .getByRole("button", { name: "Asset list", exact: true })
          .click();
      }
      assert.equal(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth,
        ),
        true,
      );
      const first = await page
        .getByLabel(/^Action for /)
        .locator("option")
        .allTextContents();
      const initial = first.find((x) =>
        x.startsWith(side === "blue" ? "monitor ·" : "recon ·"),
      );
      assert.ok(initial, "A real targeted action must be offered");
      match = await submit(page, initial);
      assert.ok(match.budget < 24);
      await page.reload();
      await page
        .getByRole("button", { name: new RegExp(`Resume match ${match.id} →`) })
        .click();
      await page
        .getByRole("heading", { name: match.title, exact: true })
        .waitFor();
      assert.equal((await saved(page, match.id)).turn, 2);
      while (!match.winner) {
        match = await submit(page, waitLabel(side));
        if (!match.winner)
          await page
            .getByLabel("Match resources")
            .getByText(`${match.turn} / ${match.turn_limit}`, { exact: true })
            .waitFor();
      }
      await page
        .getByRole("heading", {
          name: /Blue protected the objective|Red achieved the objective/,
        })
        .waitFor();
      await page
        .getByText("Round 1 · decisions and missed opportunities", {
          exact: true,
        })
        .click();
      await page
        .getByRole("heading", { name: "Action field guide", exact: true })
        .waitFor();
      await page
        .getByText("BLUE · contain · 2 credits", { exact: true })
        .click();
      await page
        .getByText(
          "Always isolates; removes ordinary access, but retained access needs review or recovery.",
          { exact: true },
        )
        .waitFor();
      await shot(page, `red-blue-${side}-${mobile ? "mobile" : "desktop"}`);
      await page.reload();
      await page
        .getByRole("button", { name: new RegExp(`Resume match ${match.id} →`) })
        .click();
      await page
        .getByRole("heading", {
          name: /Blue protected the objective|Red achieved the objective/,
        })
        .waitFor();
      assert.deepEqual(errors, []);
    });

for (const mobile of [false, true])
  test(`Red Blue two separate learners: invite, secrecy, shared round and logout, mobile=${mobile}`, async (t) => {
    const red = await context(t, TOKEN, mobile);
    const credentials = {
      email: `redblue-${Date.now()}-${mobile}@example.com`,
      password: "Synthetic-simulator-pass-2026!",
    };
    const registered = await red.page.request.post(
      API + "/api/v1/auth/register",
      {
        data: {
          ...credentials,
          full_name: "Synthetic Second Learner",
          date_of_birth: "1990-01-01",
        },
      },
    );
    assert.equal(registered.status(), 201);
    const login = await red.page.request.post(API + "/api/v1/auth/login", {
      data: credentials,
    });
    assert.equal(login.status(), 200);
    const token = (await login.json()).access_token;
    assert.notEqual(token, TOKEN);
    const blue = await context(t, token, mobile);
    const match = await start(red.page, "red", "human");
    await red.page
      .getByRole("button", { name: "Create invitation code", exact: true })
      .click();
    await red.page.getByLabel("Share this code privately").waitFor();
    const code = await red.page
      .getByLabel("Share this code privately")
      .inputValue();
    assert.equal(code.length, 43);
    await blue.page.goto("/red-blue");
    await blue.page.getByLabel("Invitation code", { exact: true }).fill(code);
    await blue.page
      .getByRole("button", { name: "Join match", exact: true })
      .click();
    await blue.page
      .getByRole("heading", { name: match.title, exact: true })
      .waitFor();
    await red.page.getByLabel(/^Action for /).waitFor(); // automatic join polling
    const before = await saved(blue.page, match.id, token);
    await submit(red.page, "recon · 1 credits");
    await red.page
      .getByText("Choice sealed. Waiting for the other seat.", { exact: true })
      .waitFor();
    const after = await saved(blue.page, match.id, token);
    for (const key of ["assets", "observations", "orders", "committed_order"])
      assert.deepEqual(after[key], before[key]);
    for (const key of ["seed", "transcript", "timeline", "plans", "seats"])
      assert.equal(key in after, false);
    await shot(red.page, `red-blue-sealed-${mobile ? "mobile" : "desktop"}`);
    await blue.page
      .getByRole("button", { name: "Refresh saved match", exact: true })
      .click();
    await submit(blue.page, "monitor · 1 credits");
    await red.page
      .getByLabel("Match resources")
      .getByText("2 / 12", { exact: true })
      .waitFor();
    const final = await saved(red.page, match.id);
    assert.equal(final.turn, 2);
    assert.equal(final.version, 2);
    assert.equal(final.budget, 23);
    await red.page.reload();
    await red.page
      .getByRole("button", { name: new RegExp(`Resume match ${match.id} →`) })
      .click();
    await red.page
      .getByLabel("Match resources")
      .getByText("2 / 12", { exact: true })
      .waitFor();
    await blue.page
      .getByRole("button", {
        name: "Sign out of EduCyber Nigeria",
        exact: true,
      })
      .click();
    await blue.page.waitForURL("**/account");
    const revoked = await red.page.request.get(
      API + "/api/v1/red-blue/matches/" + match.id,
      { headers: { Authorization: "Bearer " + token } },
    );
    assert.equal(revoked.status(), 401);
    assert.equal((await saved(red.page, match.id)).turn, 2);
    assert.deepEqual(red.errors, []);
    assert.deepEqual(blue.errors, []);
  });

for (const failure of ["dropped", "503"])
  test(`Red Blue interrupted response (${failure}): retry exact UUID against actual committed state`, async (t) => {
    const { page, errors } = await context(t, TOKEN, false);
    const match = await start(page, "blue");
    const requests = [];
    page.on("request", (r) => {
      if (/\/red-blue\/matches\/\d+\/commands$/.test(r.url()))
        requests.push(r.postDataJSON());
    });
    const pattern = "**/api/v1/red-blue/matches/*/commands";
    await page.route(pattern, async (route) => {
      const response = await route.fetch();
      assert.equal(response.status(), 200);
      if (failure === "dropped") await route.abort("failed");
      else
        await route.fulfill({
          status: 503,
          contentType: "application/json",
          body: JSON.stringify({
            detail: "Synthetic interrupted acknowledgement",
          }),
        });
    });
    await page
      .getByLabel(/^Action for /)
      .selectOption({ label: waitLabel("blue") });
    await page
      .getByRole("button", { name: "Seal choice", exact: true })
      .click();
    await page
      .getByRole("button", { name: "Retry same choice", exact: true })
      .waitFor();
    assert.equal((await saved(page, match.id)).turn, 2);
    await page.unroute(pattern);
    await page
      .getByRole("button", { name: "Retry same choice", exact: true })
      .click();
    await page
      .getByLabel("Match resources")
      .getByText("2 / 12", { exact: true })
      .waitFor();
    assert.equal(requests.length, 2);
    assert.deepEqual(requests[0], requests[1]);
    assert.equal((await saved(page, match.id)).version, 2);
    assert.deepEqual(errors, []);
  });
