import fs from 'node:fs';
import crypto from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
import {computeFillStatus} from '../../../../../scripts/gemini/fill-lib.mjs';
const base='data/artwork-generated/batch-1817';
const ledger=JSON.parse(fs.readFileSync('data/artwork-batch-1817.json'));
const protectedBefore=JSON.parse(fs.readFileSync(`${base}/drafts/root/protected-before.json`));
const concurrentReport=JSON.parse(fs.readFileSync(`${base}/drafts/root/concurrent-protected-changes.json`));
const concurrentHashes=new Map(concurrentReport.changes.map(c=>[c.path,c.observed_sha256]));
const registry=JSON.parse(fs.readFileSync(`${base}/drafts/root/codex-native-reviews.json`));
const {entries,status}=await computeFillStatus(JSON.parse(fs.readFileSync('data/creatures.json')));
const final=process.argv.includes('--final');
const errors=[],pending=[],notRootReviewed=[],selectedHashes=new Set();let checks=0,drawn=0,declined=0,archived=0,failures=0;
const check=(ok,m)=>{checks++;if(!ok)errors.push(m)};
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
check(ledger.items.length===50,'Batch must have50items');
for(const item of ledger.items){
 const slug=item.slug,path=`${base}/${slug}.json`;
 check(isDeepStrictEqual(item.research,entries.get(slug)),`${slug}: current accepted research`);
 check(status[slug]?.status==='lengkap-informasi',`${slug}: source eligibility`);
 if(!fs.existsSync(path)){pending.push(slug);continue}
 const r=JSON.parse(fs.readFileSync(path));
 check(r.slug===slug&&r.batch===1817,`${slug}: identity`);
 check(r.review_path===item.review_path&&r.rationale===ledger.user_policy.intent,`${slug}: source/policy`);
 check(r.worker==='codex'&&Boolean(r.worker_agent)&&r.tool==='OpenAI built-in image_gen'&&Boolean(r.image_model),`${slug}: tool/worker`);
 check(r.subagent_model==='gpt-6.1-sol'&&r.subagent_reasoning_effort==='high',`${slug}: actual agent metadata`);
 for(const k of ['root_visual_review','independent_visual_review','correction_notes'])check(!Object.hasOwn(r,k),`${slug}: forbidden ${k}`);
 const claimIds=new Set(item.research.claims.map(c=>c.id));
 check(r.basis_claim_ids?.length>0,`${slug}: source basis exists`);
 for(const id of r.basis_claim_ids||[])check(claimIds.has(id),`${slug}: valid basis ${id}`);
 check(Array.isArray(r.generation_failures)&&Array.isArray(r.rejected_attempts),`${slug}: history arrays`);
 failures+=(r.generation_failures||[]).length;
 for(const a of r.rejected_attempts||[]){
  archived++;
  check(fs.existsSync(a.original_file)&&fs.existsSync(a.receipt_file),`${slug}: archive exists`);
  if(fs.existsSync(a.original_file)&&fs.existsSync(a.receipt_file)){
   const ar=JSON.parse(fs.readFileSync(a.receipt_file));
   check(hash(a.original_file)===a.native_sha256&&ar.native_sha256===a.native_sha256,`${slug}: archived hash`);
   check(Boolean(ar.prompt?.trim())&&ar.reason===a.reason,`${slug}: archived prompt/reason`);
   check(Boolean(ar.generated_file)&&fs.existsSync(ar.generated_file)&&hash(ar.generated_file)===a.native_sha256,`${slug}: rejected tool provenance`);
  }
 }
 if(r.status==='tidak-digambar'){
  declined++;check(Boolean(r.reason?.trim()),`${slug}: decline reason`);
  if(final)check(item.status===r.status&&item.receipt_path===path&&item.reason===r.reason,`${slug}: decline ledger`);
  continue;
 }
 drawn++;check(r.status==='awaiting-independent-review',`${slug}: status`);
 for(const k of ['prompt','depicted_variant','aura','generated_at','generated_file','original_file'])check(Boolean(r[k]?.trim()),`${slug}: ${k}`);
 check(r.visual_requirements?.length>0&&r.artistic_choices?.length>0,`${slug}: requirements/choices`);
 for(const q of r.visual_requirements||[]){
  check(['anatomy','effect','setting'].includes(q.kind)&&Boolean(q.description?.trim())&&q.claim_ids?.length>0,`${slug}: requirement`);
  for(const id of q.claim_ids||[])check(claimIds.has(id)&&r.basis_claim_ids.includes(id),`${slug}: requirement source ${id}`);
 }
 check(fs.existsSync(r.original_file),`${slug}: selected native exists`);
 if(fs.existsSync(r.original_file)){
  const png=fs.readFileSync(r.original_file),sha=hash(r.original_file);
  check(png.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])),`${slug}: native PNG signature`);
  check(png.readUInt32BE(16)===r.width&&png.readUInt32BE(20)===r.height&&r.width===r.height&&r.width>=1024,`${slug}: native dimensions`);
  check(sha===r.native_sha256&&!selectedHashes.has(sha),`${slug}: unique selected hash`);selectedHashes.add(sha);
  check(fs.existsSync(r.generated_file)&&hash(r.generated_file)===sha,`${slug}: native tool provenance`);
  check(r.visual_review?.reviewer==='codex'&&r.visual_review.verdict==='pass'&&r.visual_review.native_sha256===sha&&r.visual_review.limitations?.length===0,`${slug}: Codex visual review`);
  const review=registry[slug];
  if(!review||review.native_sha256!==sha)notRootReviewed.push(slug);
  else{
   check(review.native_reviewed&&review.thumbnail_200_reviewed&&fs.existsSync(review.thumbnail_path),`${slug}: root original/200review`);
   check(review.sangar_checks?.length===7&&review.sangar_checks.every(Boolean)&&review.verdict==='pass',`${slug}: root7checks`);
   check(item.native_sha256===sha&&item.original_file===r.original_file&&item.receipt_path===path&&item.status===r.status,`${slug}: ledger selected`);
  }
 }
}
if(final){check(ledger.generation_complete===true,'Generation completion');check(!pending.length,'No missing receipts');check(!notRootReviewed.length,'All selected PNGs reviewed by root')}
let unchangedProtected=0, concurrentProtected=0;
for(const [p,sha] of Object.entries(protectedBefore)){
 const observed=fs.existsSync(p)?hash(p):null;
 if(observed===sha){unchangedProtected++;check(true,`Protected unchanged: ${p}`)}
 else if(concurrentHashes.has(p)&&concurrentHashes.get(p)===observed){concurrentProtected++;check(true,`Concurrent change preserved: ${p}`)}
 else if(p.startsWith('data/gemini/')){
  // Research continues in a separate session. Record the exact bytes read by
  // this check so a later research write cannot race a separate snapshot pass.
  const now=new Date().toISOString();
  let c=concurrentReport.changes.find(c=>c.path===p);
  if(!c){c={path:p,baseline_sha256:sha};concurrentReport.changes.push(c)}
  if(c.observed_sha256){(c.observed_hash_history??=[]).push({sha256:c.observed_sha256,observed_at:c.observed_at??concurrentReport.observed_at})}
  Object.assign(c,{observed_sha256:observed,observed_at:now,reason:'External research update observed during final artwork validation; Codex writes only artwork outputs, ledger and journal.'});
  concurrentReport.observed_at=now;
  concurrentProtected++;check(true,`Concurrent research change recorded: ${p}`);
 }
 else check(false,`Unrecorded protected change: ${p}`);
}
fs.writeFileSync(`${base}/drafts/root/concurrent-protected-changes.json`,JSON.stringify(concurrentReport,null,2)+'\n');
const result={checked_at:new Date().toISOString(),final,checks,errors,target:50,drawn,declined,pending,notRootReviewed,archived_attempts:archived,recorded_generation_failures:failures,protected_files:Object.keys(protectedBefore).length,protected_unchanged:unchangedProtected,protected_concurrent_changes_preserved:concurrentProtected,concurrent_change_record:`${base}/drafts/root/concurrent-protected-changes.json`,integration_performed:false};
fs.writeFileSync(`${base}/drafts/root/validation${final?'':'-progress'}.json`,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));process.exitCode=errors.length?1:0;
