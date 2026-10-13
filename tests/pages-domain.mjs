import assert from 'node:assert/strict';
import { test } from 'node:test';
import { reserveName } from '../scripts/pages-domain.mjs';

const old = { id: 'original', name: 'mitoloka', subdomain: 'mitoloka-99o.pages.dev' };
function mockApi({ assigned = 'mitoloka.pages.dev', creationFails = false, deployed = false } = {}) {
  const calls = [];
  const api = async (method, path, body) => {
    calls.push({ method, path, body });
    if (method === 'PATCH') return { ...old, name: body.name };
    if (method === 'POST' && creationFails) throw new Error('Creation failed');
    if (method === 'POST' || method === 'GET') return { id: 'new', name: 'mitoloka', subdomain: assigned, ...(deployed ? { canonical_deployment: { id: 'deployment' } } : {}) };
    if (method === 'DELETE') return null;
    throw new Error(`Unexpected ${method} ${path}`);
  };
  return { api, calls };
}

test('An available clean domain keeps the original live project as a backup', async () => {
  const { api, calls } = mockApi();
  const result = await reserveName(api, 'mitoloka', [old], () => {});
  assert.equal(result.outcome, 'reserved');
  assert.equal(result.site_url, 'https://mitoloka.pages.dev');
  assert.match(result.backup, /^mitoloka-backup-/);
  assert.deepEqual(calls.map(c => c.method), ['PATCH', 'POST']);
});

test('An unavailable domain removes only the new empty project and restores the original', async () => {
  const { api, calls } = mockApi({ assigned: 'mitoloka-new.pages.dev' });
  const result = await reserveName(api, 'mitoloka', [old], () => {});
  assert.equal(result.outcome, 'unavailable');
  assert.equal(result.restored, old.subdomain);
  assert.deepEqual(calls.map(c => c.method), ['PATCH', 'POST', 'GET', 'DELETE', 'PATCH']);
  assert.equal(calls.at(-1).body.name, 'mitoloka');
  assert.match(calls.at(-1).path, /^\/projects\/mitoloka-backup-/);
});

test('Failed creation restores the original project name', async () => {
  const { api, calls } = mockApi({ creationFails: true });
  await assert.rejects(reserveName(api, 'mitoloka', [old], () => {}), /Creation failed/);
  assert.deepEqual(calls.map(c => c.method), ['PATCH', 'POST', 'PATCH']);
  assert.equal(calls.at(-1).body.name, 'mitoloka');
});

test('A clean domain already owned by the account causes no mutations', async () => {
  const { api, calls } = mockApi();
  const result = await reserveName(api, 'mitoloka', [{ ...old, subdomain: 'mitoloka.pages.dev' }]);
  assert.equal(result.outcome, 'already-owned');
  assert.deepEqual(calls, []);
});

test('A new project that unexpectedly has a deployment is never deleted', async () => {
  const { api, calls } = mockApi({ assigned: 'mitoloka-new.pages.dev', deployed: true });
  await assert.rejects(reserveName(api, 'mitoloka', [old], () => {}), /retaining both/);
  assert.equal(calls.some(c => c.method === 'DELETE'), false);
});
