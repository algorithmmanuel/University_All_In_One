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
  const theme = await page.locator(`[data-side="${side}"]`).evaluate((el) => ({
    accent: getComputedStyle(el).getPropertyValue("--seat-accent").trim(),
    brand: getComputedStyle(document.documentElement).getPropertyValue("--accent").trim(),
    surface: getComputedStyle(el.querySelector('[aria-label="Known assets"]')).backgroundColor,
  }));
  assert.equal(theme.accent, side === "red" ? "#ff9bb3" : "#79d9ef");
  assert.equal(theme.brand, "#54e0c1");
  assert.equal(theme.surface, side === "red" ? "rgb(36, 19, 31)" : "rgb(16, 43, 64)");
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
test("Red Blue six scenarios: mobile, keyboard, trust paths and seat-only evidence", async (t) => {
  const { page: catalogPage } = await context(t, TOKEN, false);
  await catalogPage.goto("/red-blue");
  const catalogResponse = await catalogPage.request.get(API + "/api/v1/red-blue/catalog", {
    headers: { Authorization: "Bearer " + TOKEN },
  });
  assert.equal(catalogResponse.status(), 200);
  const scenarios = (await catalogResponse.json()).scenarios;
  assert.equal(scenarios.length, 6);

  for (const mobile of [false, true]) {
    const { page, errors } = await context(t, TOKEN, mobile);
    for (const scenario of scenarios) {
      for (const side of ["red", "blue"]) {
        await page.goto("/red-blue");
        await page.getByLabel("Scenario", { exact: true }).selectOption(scenario.id);
        await page.getByLabel("Your seat", { exact: true }).selectOption(side);
        const created = page.waitForResponse((response) =>
          response.url().endsWith("/api/v1/red-blue/matches") &&
          response.request().method() === "POST");
        await page.getByRole("button", { name: "Start match", exact: true }).click();
        const response = await created;
        assert.equal(response.status(), 201);
        const projection = await response.json();
        const key = `${scenario.id} ${side} ${mobile ? "mobile" : "desktop"}`;
        assert.equal(projection.side, side, key);
        assert.equal(projection.scenario, scenario.id, key);
        for (const secret of ["seed", "transcript", "timeline", "plans", "seats"])
          assert.equal(secret in projection, false, key + ": hidden " + secret);
        assert.ok(projection.connections.every((edge) =>
          projection.assets.some((asset) => asset.id === edge.source) &&
          projection.assets.some((asset) => asset.id === edge.target)), key);
        const board = page.getByRole("region", { name: "Known assets" });
        await board.getByText(
          `Observed match revision ${projection.version} · round ${projection.round ?? projection.turn}`,
          { exact: true },
        ).waitFor();
        await board.getByText(
          `${projection.assets.length} known assets · ${projection.connections.length} known trust paths`,
          { exact: true },
        ).waitFor();
        // The accessible list is the mobile and dense-graph fallback. Verify
        // real keyboard selection updates the seat-filtered evidence inspector.
        await board.getByRole("button", { name: "Asset list", exact: true }).click();
        const asset = projection.assets[0];
        const button = board.getByRole("button").filter({ hasText: asset.name }).last();
        await button.focus();
        await button.press("Enter");
        assert.equal(await button.getAttribute("aria-pressed"), "true", key);
        await board.getByRole("heading", {
          name: `${asset.name} · observed evidence`, exact: true,
        }).waitFor();
        assert.equal(await page.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth
        ), true, key + ": no document overflow");
        await board.getByRole("button", { name: "Network", exact: true }).click();
        const geometry = await board.evaluate((element, state) => {
          const paths = [...element.querySelectorAll("svg path[marker-end]")];
          const nodes = [...element.querySelectorAll('button[style*="left:"]')];
          const crossing = [];
          for (let i = 0; i < paths.length; i++) {
            const edge = state.connections[i];
            if (!edge) { crossing.push("unexpected edge"); continue; }
            const path = paths[i];
            for (let d = 0; d <= path.getTotalLength(); d += 5) {
              const point = path.getPointAtLength(d);
              for (let k = 0; k < nodes.length; k++) {
                const asset = state.assets[k];
                if (asset.id === edge.source || asset.id === edge.target) continue;
                const x = parseFloat(nodes[k].style.left);
                const y = parseFloat(nodes[k].style.top);
                if (point.x > x + 2 && point.x < x + nodes[k].offsetWidth - 2 &&
                    point.y > y + 2 && point.y < y + nodes[k].offsetHeight - 2) {
                  crossing.push(`${edge.source}->${edge.target} crosses ${asset.id}`);
                  break;
                }
              }
              if (crossing.length) break;
            }
          }
          return { edges: paths.length, nodes: nodes.length, crossing };
        }, projection);
        assert.equal(geometry.nodes, projection.assets.length, key + ": node count");
        assert.equal(geometry.edges, projection.connections.length, key + ": edge count");
        assert.deepEqual(geometry.crossing, [], key + ": no edges through asset cards");
        assert.equal(await page.evaluate(
          () => document.documentElement.scrollWidth <= window.innerWidth
        ), true, key + ": no overflow in network mode");
      }
    }
    assert.deepEqual(errors, [], mobile ? "mobile page errors" : "desktop page errors");
  }
});

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
        // Sample every rendered trust path against non-endpoint node boxes.
        // Only authorised visible edges/assets from the match projection
        // are supplied; a missing or secret edge cannot appear here.
        const graph = await page
          .getByRole("region", { name: "Known assets" })
          .evaluate((section, projection) => {
            const paths = [...section.querySelectorAll('svg path[marker-end]')];
            const nodes = [...section.querySelectorAll('button[style*="left:"]')];
            const names = projection.assets.map((asset) => asset.name);
            return {
              count: paths.length,
              collisions: paths.flatMap((path, index) => {
                const edge = projection.connections[index];
                if (!edge) return ["Unexpected path " + index];
                const total = path.getTotalLength();
                const problems = [];
                for (let step = 0; step <= Math.ceil(total / 5); step++) {
                  const point = path.getPointAtLength(Math.min(step * 5, total));
                  for (let assetIndex = 0; assetIndex < nodes.length; assetIndex++) {
                    const asset = projection.assets[assetIndex];
                    if (asset.id === edge.source || asset.id === edge.target) continue;
                    const node = nodes[assetIndex];
                    const x = parseFloat(node.style.left);
                    const y = parseFloat(node.style.top);
                    if (point.x > x + 2 && point.x < x + node.offsetWidth - 2 &&
                        point.y > y + 2 && point.y < y + node.offsetHeight - 2) {
                      problems.push(`${edge.source}->${edge.target} crosses ${names[assetIndex]}`);
                      return problems;
                    }
                  }
                }
                return problems;
              }),
            };
          }, match);
        assert.equal(graph.count, match.connections.length);
        assert.deepEqual(graph.collisions, []);
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
      const initialProjection = match;
      match = await submit(page, initial);
      assert.ok(match.budget < 24);
      // All dynamic labels and highlights are derived from this seat's
      // authenticated projection; the test never inspects private engine data.
      const board = page.getByRole("region", { name: "Known assets" });
      await board.getByText(
        `Observed match revision ${match.version} · round ${match.round ?? match.turn}`,
        { exact: true },
      ).waitFor();
      const beforeAssets = new Map(initialProjection.assets.map((asset) => [
        asset.id,
        JSON.stringify([
          asset,
          initialProjection.observations.filter((event) => event.target === asset.id)
            .map((event) => [event.turn, event.type, event.action, event.message]),
        ]),
      ]));
      const changedAssets = match.assets.filter((asset) => (
        beforeAssets.get(asset.id) !== JSON.stringify([
          asset,
          match.observations.filter((event) => event.target === asset.id)
            .map((event) => [event.turn, event.type, event.action, event.message]),
        ])
      ));
      if (changedAssets.length) {
        await board.getByText(
          `${changedAssets.length} asset${changedAssets.length === 1 ? "" : "s"} with new visible information.`,
          { exact: true },
        ).waitFor();
      }
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
    // While Blue is active but has NOT committed, it must still refresh.
    // Polls are read-only: the hidden Red sealed order must remain invisible.
    const bluePolling = blue.page.waitForResponse(
      (response) =>
        response.url().endsWith("/api/v1/red-blue/matches/" + match.id) &&
        response.request().method() === "GET" &&
        response.status() === 200,
      { timeout: 10000 },
    );
    await submit(red.page, "recon · 1 credits");
    const bluePoll = await (await bluePolling).json();
    assert.equal(bluePoll.side, "blue");
    assert.equal(bluePoll.committed, false);
    assert.equal(bluePoll.committed_order, null);
    assert.deepEqual(bluePoll.assets, before.assets);
    assert.deepEqual(bluePoll.observations, before.observations);
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
        name: "Sign out of EduCyber",
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
