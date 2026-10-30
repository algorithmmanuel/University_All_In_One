const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const ts = require('typescript');
const Module = require('node:module');

const filename = path.join(__dirname, '../lib/activity-focus.ts');
const compiled = ts.transpileModule(fs.readFileSync(filename, 'utf8'), {
  compilerOptions: {module:ts.ModuleKind.CommonJS, target:ts.ScriptTarget.ES2020},
}).outputText;
const loaded = new Module(filename, module);
loaded._compile(compiled, filename);
const {focusActivity} = loaded.exports;

for (const reduced of [false, true]) {
  test('workspace focus avoids double scrolling; reduced motion=' + reduced, () => {
    const calls = [];
    const heading = {
      focus: options => calls.push(['focus', options]),
      scrollIntoView: options => calls.push(['scroll', options]),
    };
    focusActivity(heading, reduced);
    assert.deepEqual(calls, [
      ['focus', {preventScroll:true}],
      ['scroll', {behavior:reduced?'instant':'smooth', block:'start'}],
    ]);
  });
}
test('closed or not-yet-rendered activity is safe', () => {
  assert.doesNotThrow(() => focusActivity(null, true));
});
