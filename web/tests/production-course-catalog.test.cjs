const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const lib = fs.readFileSync(path.join(__dirname,'../lib/approved-course-catalog.ts'),'utf8');
const page = fs.readFileSync(path.join(__dirname,'../app/learn/page.tsx'),'utf8');

test('approved Course catalogue contains 24 individual courses and eight stages',()=>{
  const array=lib.match(/export const APPROVED_COURSES = (\[[^;]+\]) as const;/);
  assert.ok(array, 'Approved catalogue manifest missing');
  const titles=JSON.parse(array[1]);
  assert.equal(titles.length,24);
  assert.equal(new Set(titles).size,24);
  assert.match(lib,/COURSE_STAGES/);
  assert.match(lib,/ACADEMIES\[Math\.floor\(index \/ COURSE_STAGES\.length\)\]/);
});
test('production catalogue filters actual published records; legacy content remains separate',()=>{
  assert.match(page,/<h2>Course catalogue<\/h2>/);
  assert.match(page,/catalog\.filter\(c=>\{const meta=productionCourseMetadata/);
  assert.match(page,/catalogStage==="all"/);
  assert.match(page,/<h2>Existing courses<\/h2>/);
  assert.doesNotMatch(page,/isProductionCourse\(/);
});
