/** Regression checks for untrusted public pathway responses. Uses installed TypeScript. */
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const ts = require('typescript');
const Module = require('node:module');

const filename = path.join(__dirname, '..', 'lib', 'pathways.ts');
const source = fs.readFileSync(filename, 'utf8');
const js = ts.transpileModule(source, {
  compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020 },
}).outputText;
const loaded = new Module(filename, module);
loaded.filename = filename;
loaded.paths = module.paths;
loaded._compile(js, filename);
const { parsePathways, fallbackAcademies } = loaded.exports;

function valid() {
  return {
    version: 1, domain: 'cybersecurity',
    pathways: fallbackAcademies.map(item => ({
      id: item.id, title: item.title, description: item.description,
      learning_objectives: [...item.topics],
    })),
  };
}

test('valid catalogue preserves academy order and trusted icons', () => {
  const data = valid();
  data.pathways.reverse();
  const result = parsePathways(data);
  assert.deepEqual(result.map(item => item.id), ['secondary', 'university', 'professional']);
  assert.deepEqual(result.map(item => item.icon), fallbackAcademies.map(item => item.icon));
});

test('missing pathway is rejected', () => {
  const data = valid();
  data.pathways.pop();
  assert.throws(() => parsePathways(data), /Incomplete pathway catalogue/);
});

test('wrong domain is rejected', () => {
  const data = valid();
  data.domain = 'other';
  assert.throws(() => parsePathways(data), /Invalid pathway response/);
});

test('invalid learning objectives are rejected', () => {
  const data = valid();
  data.pathways[0].learning_objectives = [null];
  assert.throws(() => parsePathways(data), /Invalid pathway response/);
});

test('null or malformed response is rejected', () => {
  for (const payload of [null, [], {}, { domain: 'cybersecurity', pathways: {} }]) {
    assert.throws(() => parsePathways(payload));
  }
});
