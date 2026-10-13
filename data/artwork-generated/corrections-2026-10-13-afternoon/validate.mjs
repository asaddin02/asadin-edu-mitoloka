import fs from 'node:fs';
import crypto from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';
import { computeFillStatus } from '../../../scripts/gemini/fill-lib.mjs';
const base = 'data/artwork-generated/corrections-2026-10-13-afternoon';
const old = JSON.parse(fs.readFileSync(`${base}/receipts-before.json`));
const reviews = JSON.parse(fs.readFileSync(`${base}/codex-native-reviews.json`));
const protectedBefore = JSON.parse(fs.readFileSync(`${base}/protected-before.json`));
const hash = p => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const errors = []; let checks = 0, archived = 0;
const check = (condition, message) => { checks++; if (!condition) errors.push(message); };
const selected = new Set();
const {entries, status} = await computeFillStatus(JSON.parse(fs.readFileSync('data/creatures.json')));
for (const [slug, row] of Object.entries(old)) {
  const r = JSON.parse(fs.readFileSync(row.receipt));
  const ledger = JSON.parse(fs.readFileSync(`data/artwork-batch-${r.batch}.json`));
  const item = ledger.items.find(i => i.slug === slug);
  check(isDeepStrictEqual(item.research, entries.get(slug)), `${slug}: current accepted research`);
  check(status[slug]?.status === 'lengkap-informasi', `${slug}: eligible research`);
  check(r.slug === slug && r.batch === row.data.batch, `${slug}: identity`);
  check(r.status === 'awaiting-independent-review' && item.status === r.status, `${slug}: review status`);
  check(r.review_path === item.review_path && item.receipt_path === row.receipt, `${slug}: paths`);
  check(r.rationale === ledger.user_policy.intent, `${slug}: policy intent`);
  check(r.tool === 'OpenAI built-in image_gen' && Boolean(r.image_model), `${slug}: tool`);
  check(r.subagent_model === 'gpt-6.1-sol' && r.subagent_reasoning_effort === 'high', `${slug}: agent`);
  for (const key of ['root_visual_review','independent_visual_review','correction_notes']) check(!Object.hasOwn(r,key), `${slug}: forbidden ${key}`);
  for (const key of ['prompt','depicted_variant','aura','generated_at','generated_file','original_file']) check(Boolean(r[key]?.trim()), `${slug}: ${key}`);
  const claims = new Set(item.research.claims.map(c => c.id));
  for (const id of r.basis_claim_ids) check(claims.has(id), `${slug}: unknown basis ${id}`);
  check(r.visual_requirements.length > 0 && r.artistic_choices.length > 0, `${slug}: requirements/choices`);
  for (const q of r.visual_requirements) {
    check(['anatomy','effect','setting'].includes(q.kind) && Boolean(q.description.trim()) && q.claim_ids.length > 0, `${slug}: requirement`);
    for (const id of q.claim_ids) check(claims.has(id) && r.basis_claim_ids.includes(id), `${slug}: requirement basis ${id}`);
  }
  check(fs.existsSync(r.original_file), `${slug}: native exists`);
  if (fs.existsSync(r.original_file)) {
    const png = fs.readFileSync(r.original_file), sha = hash(r.original_file);
    check(png.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])), `${slug}: PNG`);
    check(png.readUInt32BE(16) === r.width && png.readUInt32BE(20) === r.height && r.width === r.height && r.width >= 1024, `${slug}: dimensions`);
    check(sha === r.native_sha256 && sha === item.native_sha256 && item.original_file === r.original_file, `${slug}: selected hash/path`);
    check(sha !== row.data.native_sha256 && !selected.has(sha), `${slug}: new unique image`); selected.add(sha);
    check(fs.existsSync(r.generated_file) && hash(r.generated_file) === sha, `${slug}: tool provenance`);
    check(r.visual_review.reviewer === 'codex' && r.visual_review.verdict === 'pass' && r.visual_review.native_sha256 === sha && r.visual_review.limitations.length === 0, `${slug}: worker review`);
    check(reviews[slug]?.native_sha256 === sha && reviews[slug]?.sangar_checks?.length === 7 && reviews[slug].sangar_checks.every(Boolean) && reviews[slug].native_reviewed && reviews[slug].thumbnail_200_reviewed, `${slug}: root Codex review`);
  }
  check(Array.isArray(r.generation_failures) && Array.isArray(r.rejected_attempts), `${slug}: history arrays`);
  check(r.rejected_attempts.some(a => a.native_sha256 === row.data.native_sha256 && a.reason === row.data.correction_notes), `${slug}: Claude rejection preserved`);
  for (const a of r.rejected_attempts) {
    archived++;
    check(fs.existsSync(a.original_file) && fs.existsSync(a.receipt_file), `${slug}: archive exists`);
    if (fs.existsSync(a.original_file) && fs.existsSync(a.receipt_file)) {
      const archive = JSON.parse(fs.readFileSync(a.receipt_file));
      check(hash(a.original_file) === a.native_sha256 && archive.native_sha256 === a.native_sha256, `${slug}: archive hash`);
      check(Boolean(archive.prompt?.trim()) && archive.reason === a.reason, `${slug}: archive prompt/reason`);
    }
  }
}
for (const [p, sha] of Object.entries(protectedBefore)) check(fs.existsSync(p) && hash(p) === sha, `Protected file changed: ${p}`);
const result = { checked_at:new Date().toISOString(), checks, errors, corrections: Object.keys(old).length, selected_pngs:selected.size, archived_attempts:archived, protected_files:Object.keys(protectedBefore).length, integration_performed:false };
fs.writeFileSync(`${base}/validation.json`, JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
process.exitCode = errors.length ? 1 : 0;
