import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';
import { computeFillStatus } from '../../../../../scripts/gemini/fill-lib.mjs';

const batch = 1606;
const base = `data/artwork-generated/batch-${batch}`;
const ledger = JSON.parse(fs.readFileSync(`data/artwork-batch-${batch}.json`));
const registry = JSON.parse(fs.readFileSync(`${base}/drafts/root/root-native-reviews.json`, 'utf8'));
const before = JSON.parse(fs.readFileSync(`${base}/drafts/root/protected-before.json`));
const { entries, status } = await computeFillStatus(JSON.parse(fs.readFileSync('data/creatures.json')));
const hash = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
let checks = 0, finals = 0, declined = 0, archives = 0;
const errors = [], hashes = new Set();
function check(condition, message) { checks++; if (!condition) errors.push(message); }
function png(p) {
  const buf = fs.readFileSync(p);
  check(buf.subarray(0, 8).equals(Buffer.from([137,80,78,71,13,10,26,10])), `${p}: not PNG`);
  return [buf.readUInt32BE(16), buf.readUInt32BE(20)];
}
for (const item of ledger.items) {
  const tag = item.slug, rp = `${base}/${tag}.json`;
  check(fs.existsSync(rp), `${tag}: receipt missing`);
  if (!fs.existsSync(rp)) continue;
  const r = JSON.parse(fs.readFileSync(rp));
  check(isDeepStrictEqual(entries.get(tag), item.research), `${tag}: accepted research changed`);
  check(status[tag]?.status === 'lengkap-informasi', `${tag}: research no longer eligible`);
  check(r.slug === tag && r.batch === batch && r.worker === 'codex', `${tag}: identity metadata`);
  check(r.review_path === item.review_path, `${tag}: review_path`);
  check(r.tool === ledger.tool, `${tag}: tool`);
  check(r.subagent_model === 'gpt-6.1-sol' && r.subagent_reasoning_effort === 'high', `${tag}: worker model`);
  check(['lane-A','lane-B','lane-C'].includes(r.worker_agent), `${tag}: lane`);
  check(item.status === r.status && item.receipt_path === rp, `${tag}: ledger status/path`);
  for (const name of ['root_visual_review','independent_visual_review','correction_notes']) check(!Object.hasOwn(r,name), `${tag}: forbidden ${name}`);
  check(Array.isArray(r.generation_failures) && Array.isArray(r.rejected_attempts), `${tag}: history arrays`);
  for (const a of r.rejected_attempts || []) {
    archives++;
    const pp = a.original_file, ap = a.receipt_file;
    check(pp?.startsWith(`${base}/rejected/`) && fs.existsSync(pp), `${tag}: rejected PNG missing`);
    check(ap?.startsWith(`${base}/rejected/`) && fs.existsSync(ap), `${tag}: rejected JSON missing`);
    if (fs.existsSync(pp || '') && fs.existsSync(ap || '')) {
      const ar = JSON.parse(fs.readFileSync(ap));
      check(hash(pp) === a.native_sha256 && ar.native_sha256 === a.native_sha256, `${tag}: rejected hash`);
      check(Boolean(ar.prompt?.trim()) && Boolean(ar.reason?.trim()) && ar.reason === a.reason, `${tag}: rejected provenance`);
      const [w,h] = png(pp); check(w >= 1024 && h >= 1024, `${tag}: rejected dimensions`);
    }
  }
  if (r.status === 'tidak-digambar') {
    declined++;
    check(Boolean(r.reason?.trim()), `${tag}: decline without reason`);
    continue;
  }
  finals++;
  check(r.status === 'awaiting-independent-review', `${tag}: unexpected status ${r.status}`);
  for (const key of ['image_model','rationale','prompt','depicted_variant','aura','generated_file','generated_at']) check(Boolean(String(r[key] || '').trim()), `${tag}: empty ${key}`);
  check(r.rationale === ledger.user_policy.intent, `${tag}: policy rationale`);
  const claims = new Set(item.research.claims.map(c => c.id));
  check(r.basis_claim_ids?.length > 0 && new Set(r.basis_claim_ids).size === r.basis_claim_ids.length, `${tag}: empty/duplicate basis`);
  for (const id of r.basis_claim_ids || []) check(claims.has(id), `${tag}: unknown ${id}`);
  check(r.visual_requirements?.length > 0 && r.artistic_choices?.length > 0, `${tag}: requirements/artistic choices missing`);
  for (const q of r.visual_requirements || []) {
    check(['anatomy','effect','setting'].includes(q.kind) && Boolean(q.description?.trim()), `${tag}: malformed requirement`);
    check(q.claim_ids?.length > 0, `${tag}: ungrounded requirement`);
    for (const id of q.claim_ids || []) check(claims.has(id) && r.basis_claim_ids?.includes(id), `${tag}: requirement ${id}`);
  }
  check(r.original_file === `${base}/originals/${tag}.png` && fs.existsSync(r.original_file), `${tag}: original missing/path`);
  if (fs.existsSync(r.original_file || '')) {
    const h = hash(r.original_file), [w,height] = png(r.original_file);
    check(r.native_sha256 === h && r.visual_review?.native_sha256 === h && item.native_sha256 === h, `${tag}: hash binding`);
    check(w === r.width && height === r.height && w === height && Math.min(w,height) >= 1024, `${tag}: dimensions`);
    check(!hashes.has(h), `${tag}: duplicate native`); hashes.add(h);
    check(fs.existsSync(r.generated_file) && hash(r.generated_file) === h, `${tag}: native tool provenance`);
    check(r.visual_review?.verdict === 'pass' && r.visual_review.reviewer === 'codex' && Boolean(r.visual_review.notes?.trim()) && Boolean(r.visual_review.reviewed_at), `${tag}: self review`);
    check(Array.isArray(r.visual_review?.limitations) && r.visual_review.limitations.length === 0, `${tag}: unresolved limitations`);
    check(registry[tag]?.native_sha256 === h && registry[tag]?.verdict === 'pass' && registry[tag]?.sangar_checks?.length === 7 && registry[tag].sangar_checks.every(v => v === true), `${tag}: main native review missing`);
    check(registry[tag]?.thumbnail_200_reviewed === true && Boolean(registry[tag]?.thumbnail_notes), `${tag}: main 200px review missing`);
    check(item.original_file === r.original_file, `${tag}: ledger original`);
  }
}
for (const [p,h] of Object.entries(before)) check(fs.existsSync(p) && hash(p) === h, `${p}: protected file changed`);
check(finals + declined === ledger.target && ledger.target === 50, 'batch incomplete');
check(ledger.generation_complete === true && ledger.complete === 0, 'generation/integration metadata');
const output = { checked_at: new Date().toISOString(), batch, checks, errors, finals, declined, archived_rejected_pngs: archives, unique_selected_hashes: hashes.size, protected_files_unchanged: !errors.some(e => e.includes('protected file changed')), all_current_accepted_research_equal: !errors.some(e => e.includes('research changed')), all_native_and_200px_main_reviews: !errors.some(e => e.includes('main ')), independent_review_pending: true, integration_performed: false };
fs.writeFileSync(`${base}/drafts/root/batch-validation.json`, JSON.stringify(output,null,2)+'\n');
console.log(JSON.stringify(output,null,2));
process.exitCode = errors.length ? 1 : 0;
