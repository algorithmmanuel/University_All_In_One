const { test, after } = require("node:test");
const assert = require("node:assert/strict");
const { chromium } = require("playwright");
const WEB = process.env.EDUCYBER_E2E_WEB_URL || "http://127.0.0.1:3100";
let browser;
after(async () => {
  if (browser) await browser.close();
});
for (const mobile of [false, true])
  test(`journey: beginner, experienced, audience and back navigation; mobile=${mobile}`, async (t) => {
    browser ||= await chromium.launch({
      headless: true,
      args: ["--disable-dev-shm-usage"],
    });
    const ctx = await browser.newContext({
      baseURL: WEB,
      reducedMotion: "reduce",
      viewport: mobile
        ? { width: 320, height: 780 }
        : { width: 1440, height: 1000 },
    });
    t.after(() => ctx.close());
    const page = await ctx.newPage(),
      errors = [],
      writes = [];
    page.on("pageerror", (e) => errors.push(e.message));
    page.on("request", (r) => {
      if (r.method() === "POST") writes.push(r.url());
    });
    // The public journey remains useful while discovery services are unavailable.
    await page.route("**/api/v1/**", (r) =>
      r.fulfill({
        status: 503,
        contentType: "application/json",
        body: JSON.stringify({ detail: "Synthetic unavailable" }),
      }),
    );
    await page.goto("/");
    await page
      .getByRole("link", { name: "Begin my journey →", exact: true })
      .click();
    await page
      .getByRole("heading", { name: "Discover", exact: true })
      .waitFor();
    const nav = page.getByRole("navigation", {
      name: "Choose your starting stage",
    });
    assert.equal(await nav.getByRole("button").count(), 8);
    await page.getByRole("button", { name: /Cyber Command/ }).click();
    await nav
      .getByRole("button", { name: "3 Check understanding", exact: true })
      .click();
    await page.waitForFunction(
      () => document.activeElement?.textContent === "Check understanding",
    );
    assert.ok(
      (
        await page
          .getByRole("link", { name: /Open Practise governance/ })
          .getAttribute("href")
      ).includes("topic=governance"),
    );
    await nav
      .getByRole("button", { name: "8 Compete and reflect", exact: true })
      .click();
    const human = await page
      .getByRole("link", { name: /Open Create a two-learner/ })
      .getAttribute("href");
    assert.ok(
      human.includes("mode=human") &&
        human.includes("scenario=payment_insider"),
    );
    await page.reload();
    await page
      .getByRole("heading", { name: "Compete and reflect", exact: true })
      .waitFor();
    assert.equal(
      await page
        .getByRole("button", { name: /Cyber Command/ })
        .getAttribute("aria-pressed"),
      "true",
    );
    await nav
      .getByRole("button", { name: "6 Command an incident", exact: true })
      .click();
    await page.goBack();
    await page
      .getByRole("heading", { name: "Compete and reflect", exact: true })
      .waitFor();
    await page.goto("/journey?stage=understand&pathway=secondary");
    await page
      .getByRole("link", { name: /Open Digital Citizenship Essentials/ })
      .waitFor();
    await nav
      .getByRole("button", { name: "6 Command an incident", exact: true })
      .click();
    await page
      .getByRole("link", { name: "Open Branch Siege →", exact: true })
      .waitFor();
    assert.equal(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
      true,
    );
    if (process.env.EDUCYBER_SCREENSHOT_DIR)
      await page.screenshot({
        path:
          process.env.EDUCYBER_SCREENSHOT_DIR +
          `/journey-${mobile ? "mobile" : "desktop"}.png`,
        fullPage: true,
      });
    await page.goto("/journey?stage=malicious&pathway=admin");
    await page
      .getByRole("heading", { name: "Discover", exact: true })
      .waitFor();
    assert.deepEqual(writes, []);
    assert.deepEqual(errors, []);
  });

test("journey foundation handoff suggests a real course without automatic enrolment", async (t) => {
  browser ||= await chromium.launch({
    headless: true,
    args: ["--disable-dev-shm-usage"],
  });
  const ctx = await browser.newContext({
    baseURL: WEB,
    viewport: { width: 390, height: 844 },
    reducedMotion: "reduce",
  });
  t.after(() => ctx.close());
  await ctx.addInitScript(() =>
    sessionStorage.setItem("educyber_token", "synthetic"),
  );
  const page = await ctx.newPage(),
    writes = [];
  page.on("request", (r) => {
    if (r.method() === "POST") writes.push(r.url());
  });
  await page.route("**/api/v1/**", (route) => {
    const path = new URL(route.request().url()).pathname;
    const body = path.endsWith("/learning/catalog")
      ? {
          courses: [
            {
              id: 1,
              title: "Introduction to Python",
              academy_id: "university",
              description: "Synthetic Python",
              lesson_count: 3,
            },
            {
              id: 2,
              title: "Cyber Safety Foundations",
              academy_id: "cyber",
              description: "Synthetic safety",
              lesson_count: 3,
            },
          ],
        }
      : { enrollments: [] };
    return route.fulfill({
      contentType: "application/json",
      body: JSON.stringify(body),
    });
  });
  await page.goto("/journey?stage=understand&pathway=secondary");
  await page
    .getByRole("link", { name: "Open Cyber Safety Foundations →", exact: true })
    .click();
  await page
    .getByText("Suggested from your journey:", { exact: false })
    .waitFor();
  assert.equal(
    await page.getByRole("article").first().getByRole("heading").innerText(),
    "Cyber Safety Foundations",
  );
  await page
    .getByRole("link", { name: "Learning journey", exact: true })
    .click();
  await page
    .getByRole("heading", { name: "Understand", exact: true })
    .waitFor();
  assert.equal(
    await page
      .getByRole("button", { name: /Cyber Explorers/ })
      .getAttribute("aria-pressed"),
    "true",
  );
  assert.deepEqual(writes, []);
});
