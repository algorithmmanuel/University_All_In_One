// Development-only timed preview acceptance: real browser, real FastAPI/PG.
// CI runs the API with EDUCYBER_ENV=development against its isolated DB.
// No live Beta user, database or credential is used.
const { test, after } = require("node:test");
const assert = require("node:assert/strict");
const { chromium } = require("playwright");

const WEB = process.env.EDUCYBER_E2E_WEB_URL || "http://127.0.0.1:3100";
const API = process.env.EDUCYBER_E2E_API_URL || "http://127.0.0.1:8000";
const TOKEN = process.env.EDUCYBER_E2E_TOKEN;
if (!TOKEN) throw new Error("Isolated synthetic browser session required");
let browser;
after(async () => { if (browser) await browser.close(); });

async function seat(token) {
  browser ||= await chromium.launch({ headless: true, args: ["--disable-dev-shm-usage"] });
  const ctx = await browser.newContext({ baseURL: WEB, reducedMotion: "reduce" });
  await ctx.addInitScript((value) => sessionStorage.setItem("educyber_token", value), token);
  const page = await ctx.newPage();
  page.setDefaultTimeout(12000);
  return { ctx, page };
}

test("Development timed preview: separate human seats, live clock and immediate Blue action", async (t) => {
  const blue = await seat(TOKEN);
  t.after(() => blue.ctx.close());
  await blue.page.goto("/red-blue");
  await blue.page.getByLabel("Match rules", { exact: true }).selectOption("timed_preview");
  await blue.page.getByLabel("Your seat", { exact: true }).selectOption("blue");
  await blue.page.getByLabel("Opponent", { exact: true }).selectOption("human");
  const createdPromise = blue.page.waitForResponse((response) =>
    response.url().endsWith("/api/v1/red-blue/matches") &&
    response.request().method() === "POST");
  await blue.page.getByRole("button", { name: "Start match" }).click();
  const created = await createdPromise;
  assert.equal(created.status(), 201);
  const waiting = await created.json();
  assert.equal(waiting.status, "waiting");

  await blue.page.getByRole("button", { name: "Create invitation code" }).click();
  const invitation = await blue.page.getByLabel("Share this code privately").inputValue();
  assert.equal(invitation.length, 43);

  const credentials = {
    email: `timed-learner-${Date.now()}@example.com`,
    password: "Synthetic-simulator-pass-2026!",
  };
  const registered = await blue.page.request.post(API + "/api/v1/auth/register", {
    data: { ...credentials, full_name: "Synthetic Timed Learner",
            date_of_birth: "1990-01-01" },
  });
  assert.equal(registered.status(), 201);
  const login = await blue.page.request.post(API + "/api/v1/auth/login", {
    data: credentials,
  });
  assert.equal(login.status(), 200);
  const redToken = (await login.json()).access_token;
  const red = await seat(redToken);
  t.after(() => red.ctx.close());
  await red.page.goto("/red-blue");
  await red.page.getByLabel("Invitation code").fill(invitation);
  await red.page.getByRole("button", { name: "Join match" }).click();

  await blue.page.getByRole("heading", { name: "Server-controlled turn clock" }).waitFor();
  const original = await blue.page.request.get(
    API + "/api/v1/red-blue/matches/" + waiting.id,
    { headers: { Authorization: "Bearer " + TOKEN } },
  );
  assert.equal(original.status(), 200);
  const first = await original.json();
  assert.equal(first.active_side, "blue");
  assert.ok(first.clock.seconds_remaining > 0 && first.clock.seconds_remaining <= 90);
  assert.equal(first.clock.grace_active, false);
  await blue.page.getByText("Your turn · BLUE", { exact: true }).waitFor();
  // The second browser has rendered its own initial filtered projection
  // before Blue acts. Observe the later revision through read-only polling.
  const redBoard = red.page.getByRole("region", { name: "Known assets" });
  await redBoard.getByText("Observed match revision 0 · round 1", { exact: true }).waitFor();

  const heartbeat = await blue.page.request.post(
    API + "/api/v1/red-blue/matches/" + waiting.id + "/heartbeat",
    { headers: { Authorization: "Bearer " + TOKEN },
      data: { expected_round: 1 } },
  );
  assert.equal(heartbeat.status(), 200);
  const beatState = await heartbeat.json();
  assert.equal(beatState.clock.deadline_at, first.clock.deadline_at);

  const redUnauthorizedHeartbeat = await red.page.request.post(
    API + "/api/v1/red-blue/matches/" + waiting.id + "/heartbeat",
    { headers: { Authorization: "Bearer " + redToken },
      data: { expected_round: 1 } },
  );
  assert.equal(redUnauthorizedHeartbeat.status(), 409);

  await blue.page.getByLabel(/^Action for /).selectOption({ label: "wait blue · 0 credits" });
  const command = blue.page.waitForResponse((response) =>
    /\/red-blue\/matches\/\d+\/commands$/.test(response.url()) &&
    response.request().method() === "POST");
  await blue.page.getByRole("button", { name: "Take action", exact: true }).click();
  const response = await command;
  assert.equal(response.status(), 200);
  const result = await response.json();
  assert.equal(result.active_side, "red");
  assert.equal(result.version, 1);
  assert.equal(result.turn, 1);
  await red.page.getByText("Your turn · RED", { exact: true }).waitFor();
  await redBoard.getByText("Observed match revision 1 · round 1", { exact: true }).waitFor();
  await redBoard.getByText(/Match updated|new visible information/).waitFor();
  const redView = await red.page.request.get(
    API + "/api/v1/red-blue/matches/" + waiting.id,
    { headers: { Authorization: "Bearer " + redToken } },
  );
  const redState = await redView.json();
  assert.equal(redState.committed_order, null);
  assert.equal("transcript" in redState, false);
  assert.equal("last_seen_blue" in redState.clock, false);
  assert.equal("seed" in redState, false);

  // Complete the opposing Red turn: Blue must see the server's new
  // projection, not Red's private reconnaissance or a browser-made state.
  const blueBeforeRedMove = await blue.page.request.get(
    API + "/api/v1/red-blue/matches/" + waiting.id,
    { headers: { Authorization: "Bearer " + TOKEN } },
  );
  assert.equal(blueBeforeRedMove.status(), 200);
  const bluePrior = await blueBeforeRedMove.json();
  const redOptions = await red.page.getByLabel(/^Action for /)
    .locator("option").allTextContents();
  const reconnaissance = redOptions.find((label) => label.startsWith("recon ·"));
  assert.ok(reconnaissance, "Red must have a projected reconnaissance choice");
  await red.page.getByLabel(/^Action for /).selectOption({ label: reconnaissance });
  const redCommand = red.page.waitForResponse((response) =>
    response.url().endsWith("/api/v1/red-blue/matches/" + waiting.id + "/commands") &&
    response.request().method() === "POST");
  await red.page.getByRole("button", { name: "Take action", exact: true }).click();
  const redResult = await redCommand;
  assert.equal(redResult.status(), 200);
  const committedRed = await redResult.json();
  assert.equal(committedRed.version, 2);
  assert.equal(committedRed.active_side, "blue");
  const blueBoard = blue.page.getByRole("region", { name: "Known assets" });
  await blueBoard.getByText("Observed match revision 2 · round 2", { exact: true }).waitFor();
  await blueBoard.getByText(/Match updated|new visible information/).waitFor();
  const blueAfterRedMove = await blue.page.request.get(
    API + "/api/v1/red-blue/matches/" + waiting.id,
    { headers: { Authorization: "Bearer " + TOKEN } },
  );
  assert.equal(blueAfterRedMove.status(), 200);
  const blueCurrent = await blueAfterRedMove.json();
  assert.equal(blueCurrent.side, "blue");
  assert.equal(blueCurrent.committed_order, null);
  for (const key of ["transcript", "seed", "plans", "seats", "timeline"])
    assert.equal(key in blueCurrent, false);
  assert.equal(blueCurrent.version, 2);
  // An undetected Red reconnaissance must not manufacture Blue telemetry.
  // Compare observations as delivered by the authorised API; detection and
  // its fidelity are exclusively server decisions.
  assert.ok(blueCurrent.observations.length >= bluePrior.observations.length);
});
