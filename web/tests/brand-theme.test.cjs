const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs"),
  path = require("node:path");
test("display branding is global while existing session keys stay stable", () => {
  for (const file of [
    "app/layout.tsx",
    "app/page.tsx",
    "app/dashboard/page.tsx",
    "app/journey/page.tsx",
    "app/account/page.tsx",
    "app/red-blue/page.tsx",
    "components/home/account-navigation.tsx",
  ])
    assert.equal(
      fs
        .readFileSync(path.join(__dirname, "..", file), "utf8")
        .includes("EduCyber Nigeria"),
      false,
      file,
    );
  assert.ok(
    fs
      .readFileSync(path.join(__dirname, "../lib/sign-out.ts"), "utf8")
      .includes("educyber_token"),
  );
});
test("primary navy and teal theme retains accessible foreground contrast", () => {
  const css = fs.readFileSync(
    path.join(__dirname, "../app/globals.css"),
    "utf8",
  );
  const token = (k) => css.match(new RegExp("--" + k + ":(#[a-f0-9]{6})"))[1];
  const lum = (hex) => {
    const v = [1, 3, 5]
      .map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
      .map((n) => (n <= 0.04045 ? n / 12.92 : ((n + 0.055) / 1.055) ** 2.4));
    return v[0] * 0.2126 + v[1] * 0.7152 + v[2] * 0.0722;
  };
  const ratio = (a, b) =>
    (Math.max(lum(a), lum(b)) + 0.05) / (Math.min(lum(a), lum(b)) + 0.05);
  assert.ok(ratio(token("text"), token("bg")) >= 7);
  assert.ok(ratio(token("muted"), token("surface")) >= 4.5);
  assert.ok(ratio(token("accent"), token("bg")) >= 4.5);
});

test("seat palettes are distinct and scoped to active simulator workspace", () => {
 const css=fs.readFileSync(path.join(__dirname,"../app/red-blue/arena.module.css"),"utf8");
 const globals=fs.readFileSync(path.join(__dirname,"../app/globals.css"),"utf8");
 for(const side of ["red","blue"]) {
  assert.ok(css.includes(`.workspace[data-side="${side}"]`));
  assert.ok(css.includes(`--seat-accent:var(--role-${side}-accent)`));
 }
 assert.ok(globals.includes("--bg:#080f1e"));
 assert.ok(globals.includes("--accent:#54e0c1"));
 assert.ok(css.includes("border-color:var(--seat-accent)"));
});
