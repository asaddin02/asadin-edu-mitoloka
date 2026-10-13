import fs from 'node:fs';
import crypto from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';
import { computeFillStatus } from '../../../../../scripts/gemini/fill-lib.mjs';
const base='data/artwork-generated/batch-1606';
const queue=JSON.parse(fs.readFileSync(`${base}/drafts/root/user-correction-queue.json`));
const registry=JSON.parse(fs.readFileSync(`${base}/drafts/root/correction-native-reviews.json`));
const {entries,status}=await computeFillStatus(JSON.parse(fs.readFileSync('data/creatures.json')));
const ledgers=new Map();
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
let checks=0, archives=0, failures=0;
const errors=[],hashes=new Set();
const check=(v,m)=>{checks++;if(!v)errors.push(m)};
check(queue.length===15,'Expected 15 requested corrections');
for(const row of queue){
 const slug=row.slug;
 if(!ledgers.has(row.ledger))ledgers.set(row.ledger,JSON.parse(fs.readFileSync(row.ledger)));
 const item=ledgers.get(row.ledger).items.find(i=>i.slug===slug);
 const r=JSON.parse(fs.readFileSync(row.receipt_path));
 check(isDeepStrictEqual(item.research,entries.get(slug)),`${slug}: current research differs`);
 check(status[slug]?.status==='lengkap-informasi',`${slug}: research status`);
 check(r.slug===slug && r.batch===Number(row.ledger.match(/batch-(\d+)/)[1]),`${slug}: identity`);
 check(r.tool==='OpenAI built-in image_gen' && r.image_model==='tidak dilaporkan alat',`${slug}: tool metadata`);
 check(r.worker==='codex' && Boolean(r.worker_agent),`${slug}: worker metadata`);
 check(r.worker_agent==='root' ? r.generation_agent==='root' && r.subagent_model===null && r.subagent_reasoning_effort===null : r.subagent_model==='gpt-6.1-sol' && r.subagent_reasoning_effort==='high',`${slug}: actual worker metadata`);
 check(r.status==='awaiting-independent-review' && row.status===r.status && item.status===r.status,`${slug}: status`);
 check(r.review_path===item.review_path && item.receipt_path===row.receipt_path,`${slug}: source/receipt path`);
 check(r.rationale===ledgers.get(row.ledger).user_policy.intent,`${slug}: policy rationale`);
 for(const name of ['root_visual_review','independent_visual_review','correction_notes'])check(!Object.hasOwn(r,name),`${slug}: forbidden ${name}`);
 for(const name of ['prompt','depicted_variant','aura','generated_at','generated_file','original_file'])check(Boolean(r[name]?.trim()),`${slug}: ${name}`);
 const claims=new Set(item.research.claims.map(c=>c.id));
 check(Array.isArray(r.basis_claim_ids) && r.basis_claim_ids.length>0,`${slug}: basis missing`);
 for(const id of r.basis_claim_ids)check(claims.has(id),`${slug}: unknown ${id}`);
 check(r.visual_requirements?.length>0 && r.artistic_choices?.length>0,`${slug}: requirements/choices`);
 for(const requirement of r.visual_requirements){
  check(['anatomy','effect','setting'].includes(requirement.kind) && Boolean(requirement.description?.trim()),`${slug}: requirement`);
  check(requirement.claim_ids?.length>0,`${slug}: ungrounded requirement`);
  for(const id of requirement.claim_ids)check(claims.has(id)&&r.basis_claim_ids.includes(id),`${slug}: requirement claim ${id}`);
 }
 check(fs.existsSync(r.original_file),`${slug}: native missing`);
 if(fs.existsSync(r.original_file)){
  const png=fs.readFileSync(r.original_file),sha=hash(r.original_file);
  check(png.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])),`${slug}: not PNG`);
  check(png.readUInt32BE(16)===r.width&&png.readUInt32BE(20)===r.height&&r.width===r.height&&r.width>=1024,`${slug}: dimensions`);
  check(sha===r.native_sha256 && sha===item.native_sha256 && sha===row.new_native_sha256,`${slug}: selected hash`);
  check(!hashes.has(sha),`${slug}: duplicate selected hash`);hashes.add(sha);
  check(fs.existsSync(r.generated_file)&&hash(r.generated_file)===sha,`${slug}: native tool provenance`);
  check(r.visual_review?.native_sha256===sha && r.visual_review.verdict==='pass' && r.visual_review.reviewer==='codex' && r.visual_review.limitations?.length===0,`${slug}: worker visual review`);
  check(registry[slug]?.native_sha256===sha && registry[slug].verdict==='pass' && registry[slug].sangar_checks?.length===7 && registry[slug].sangar_checks.every(Boolean),`${slug}: root native review`);
  check(registry[slug]?.thumbnail_200_reviewed===true&&fs.existsSync(registry[slug]?.thumbnail_sheet||''),`${slug}: root thumbnail review`);
  check(item.original_file===r.original_file,`${slug}: ledger native path`);
 }
 check(Array.isArray(r.generation_failures)&&Array.isArray(r.rejected_attempts)&&r.rejected_attempts.length>0,`${slug}: history arrays`);
 failures+=r.generation_failures.length;
 for(const a of r.rejected_attempts){
  archives++;
  check(fs.existsSync(a.original_file)&&fs.existsSync(a.receipt_file),`${slug}: archive missing`);
  if(fs.existsSync(a.original_file)&&fs.existsSync(a.receipt_file)){
   const ar=JSON.parse(fs.readFileSync(a.receipt_file));
   check(hash(a.original_file)===a.native_sha256&&ar.native_sha256===a.native_sha256,`${slug}: archive hash`);
   check(a.native_sha256!==r.native_sha256,`${slug}: selected repeats rejected`);
   check(Boolean(ar.prompt?.trim())&&Boolean(ar.reason?.trim())&&ar.reason===a.reason,`${slug}: archive reason/prompt`);
  }
 }
}
const out={checked_at:new Date().toISOString(),checks,errors,corrections:queue.length,unique_selected_hashes:hashes.size,all_current_accepted_research_equal:!errors.some(e=>e.includes('research differs')),all_native_and_200px_root_reviews:!errors.some(e=>e.includes('root')),archived_rejected_pngs:archives,recorded_generation_failures:failures,independent_review_pending:true,integration_performed:false};
fs.writeFileSync(`${base}/drafts/root/corrections-validation.json`,JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out,null,2));process.exitCode=errors.length?1:0;
