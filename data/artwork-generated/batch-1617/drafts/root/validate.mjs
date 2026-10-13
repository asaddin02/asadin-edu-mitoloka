import fs from 'node:fs';
import crypto from 'node:crypto';
import {isDeepStrictEqual} from 'node:util';
import {computeFillStatus} from '../../../../../scripts/gemini/fill-lib.mjs';
const base='data/artwork-generated/batch-1617';
const ledger=JSON.parse(fs.readFileSync('data/artwork-batch-1617.json'));
const protectedBefore=JSON.parse(fs.readFileSync(`${base}/drafts/root/protected-before.json`));
const reviews=JSON.parse(fs.readFileSync(`${base}/drafts/root/codex-variant-reviews.json`));
const {entries,status}=await computeFillStatus(JSON.parse(fs.readFileSync('data/creatures.json')));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const errors=[];let checks=0,drawn=0,declined=0,variants=0,rejected=0;
const check=(ok,message)=>{checks++;if(!ok)errors.push(message)};
const unique=new Set();
const validateArchives=(r,slug)=>{
 for(const a of r.rejected_attempts){
  rejected++;
  check(fs.existsSync(a.original_file)&&fs.existsSync(a.receipt_file),`${slug}: rejected archive`);
  if(fs.existsSync(a.original_file)&&fs.existsSync(a.receipt_file)){
   const ar=JSON.parse(fs.readFileSync(a.receipt_file));
   check(hash(a.original_file)===a.native_sha256&&ar.native_sha256===a.native_sha256&&Boolean(ar.prompt?.trim())&&ar.reason===a.reason,`${slug}: archive provenance`);
   check(fs.existsSync(ar.generated_file)&&hash(ar.generated_file)===a.native_sha256,`${slug}: rejected tool provenance`);
  }
 }
};
const validatePNG=(p,sha,w,h,label)=>{
 check(fs.existsSync(p),`${label}: PNG exists`);
 if(!fs.existsSync(p))return;
 const png=fs.readFileSync(p);
 check(png.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])),`${label}: PNG signature`);
 check(png.readUInt32BE(16)===w&&png.readUInt32BE(20)===h&&w===h&&w>=1024,`${label}: dimensions`);
 check(hash(p)===sha,`${label}: PNG hash`);
};
check(ledger.items.length===11&&ledger.generation_complete===true,'Batch identity/completeness');
for(const item of ledger.items){
 const slug=item.slug,path=`${base}/${slug}.json`,r=JSON.parse(fs.readFileSync(path));
 check(isDeepStrictEqual(item.research,entries.get(slug)),`${slug}: unchanged accepted research`);
 check(status[slug]?.status==='lengkap-informasi',`${slug}: eligible research`);
 check(r.slug===slug&&r.batch===1617&&item.status===r.status&&item.receipt_path===path,`${slug}: identity/ledger`);
 check(r.review_path===item.review_path&&r.rationale===ledger.user_policy.intent,`${slug}: review/policy`);
 check(r.worker==='codex'&&r.tool==='OpenAI built-in image_gen'&&Boolean(r.image_model),`${slug}: tool`);
 check(r.subagent_model==='gpt-6.1-sol'&&r.subagent_reasoning_effort==='high',`${slug}: agent`);
 for(const k of ['root_visual_review','independent_visual_review','correction_notes'])check(!Object.hasOwn(r,k),`${slug}: forbidden ${k}`);
 const ids=new Set(item.research.claims.map(c=>c.id));
 check(r.basis_claim_ids?.length>0,`${slug}: basis exists`);
 for(const id of r.basis_claim_ids||[])check(ids.has(id),`${slug}: valid basis ${id}`);
 check(Array.isArray(r.generation_failures)&&Array.isArray(r.rejected_attempts),`${slug}: history arrays`);
 validateArchives(r,slug);
 if(r.status==='tidak-digambar'){
  declined++;
  check(Boolean(r.reason?.trim())&&Boolean(item.reason?.trim()),`${slug}: decline reason`);
  continue;
 }
 drawn++;
 check(r.status==='awaiting-independent-review',`${slug}: review status`);
 for(const k of ['prompt','depicted_variant','aura','generated_file','generated_at'])check(Boolean(r[k]?.trim()),`${slug}: ${k}`);
 check(r.visual_requirements?.length>0&&r.artistic_choices?.length>0,`${slug}: requirements/choices`);
 for(const q of r.visual_requirements||[]){
  check(['anatomy','effect','setting'].includes(q.kind)&&Boolean(q.description?.trim())&&q.claim_ids?.length>0,`${slug}: requirement`);
  for(const id of q.claim_ids||[])check(ids.has(id)&&r.basis_claim_ids.includes(id),`${slug}: requirement basis ${id}`);
 }
 validatePNG(r.original_file,r.native_sha256,r.width,r.height,slug);
 check(item.native_sha256===r.native_sha256&&item.original_file===r.original_file,`${slug}: ledger native`);
 check(fs.existsSync(r.generated_file)&&hash(r.generated_file)===r.native_sha256,`${slug}: tool provenance`);
 check(r.visual_review?.verdict==='pass'&&r.visual_review.reviewer==='codex'&&r.visual_review.native_sha256===r.native_sha256&&r.visual_review.limitations.length===0,`${slug}: worker visual review`);
 check(!unique.has(r.native_sha256),`${slug}: unique selected`);unique.add(r.native_sha256);
 const root=reviews[slug];
 check(root?.selected_native_sha256===r.native_sha256&&Boolean(root.selection_reason?.trim()),`${slug}: root selection`);
 check(Object.keys(root?.variants||{}).length===2,`${slug}: two candidate reviews`);
 for(const [name,v] of Object.entries(root?.variants||{})){
  variants++;
  validatePNG(v.original_file,v.native_sha256,v.width,v.height,`${slug}/${name}`);
  check(v.native_reviewed&&v.thumbnail_200_reviewed&&fs.existsSync(v.thumbnail_path),`${slug}/${name}: root native+thumbnail review`);
  check(v.sangar_checks?.length===7,`${slug}/${name}: 7 checks`);
  if(v.native_sha256===r.native_sha256)check(v.sangar_checks.every(Boolean),`${slug}/${name}: selected passes all`);
  check(fs.existsSync(v.receipt_file),`${slug}/${name}: variant metadata`);
  if(fs.existsSync(v.receipt_file)){
   const vr=JSON.parse(fs.readFileSync(v.receipt_file));
   check(vr.native_sha256===v.native_sha256&&Boolean(vr.prompt?.trim()),`${slug}/${name}: metadata hash/prompt`);
   check(fs.existsSync(vr.generated_file)&&hash(vr.generated_file)===v.native_sha256,`${slug}/${name}: provenance`);
   if(v.native_sha256!==r.native_sha256)check(Boolean(vr.not_selected_reason?.trim()),`${slug}/${name}: nonselection reason`);
  }
 }
}
for(const [p,sha] of Object.entries(protectedBefore))check(fs.existsSync(p)&&hash(p)===sha,`Protected file changed: ${p}`);
const result={checked_at:new Date().toISOString(),checks,errors,target:11,drawn,declined,variants_root_reviewed:variants,rejected_attempts:rejected,protected_files:Object.keys(protectedBefore).length,integration_performed:false};
fs.writeFileSync(`${base}/drafts/root/validation.json`,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));process.exitCode=errors.length?1:0;
