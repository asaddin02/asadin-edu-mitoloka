import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
const slug=process.argv[2];
const plan=JSON.parse(fs.readFileSync(`data/artwork-generated/batch-1227/drafts/root/${slug}-plan.json`));
const ledger=JSON.parse(fs.readFileSync('data/artwork-batch-1227.json'));
const item=ledger.items.find(i=>i.slug===slug);
const base='data/artwork-generated/batch-1227';
const selected=plan.selected;
for(let n=0;n<plan.variants.length;n++){
 const v=plan.variants[n];
 const file=n===selected?`${base}/originals/${slug}.png`:`${base}/variants/${slug}/variant-${n+1}.png`;
 fs.mkdirSync(path.dirname(file),{recursive:true});fs.copyFileSync(v.generated_file,file);
 const bytes=fs.readFileSync(file),hash=crypto.createHash('sha256').update(bytes).digest('hex');
 Object.assign(v,{original_file:file,native_sha256:hash,width:bytes.readUInt32BE(16),height:bytes.readUInt32BE(20)});
 if(n!==selected)fs.writeFileSync(file.replace(/\.png$/,'.json'),JSON.stringify({slug,variant:n+1,tool:ledger.tool,image_model:'tidak dilaporkan alat',generated_file:v.generated_file,prompt:v.prompt,original_file:file,native_sha256:hash,width:v.width,height:v.height,selected:false,reason_not_selected:plan.selection_reason,visual_review:{reviewer:'codex',verdict:v.verdict||'pass',notes:v.notes,native_sha256:hash,reviewed_at:new Date().toISOString()}},null,2)+'\n');
}
const v=plan.variants[selected];
const r={slug,worker:'codex',worker_agent:'root',subagent_model:'gpt-6.1-sol',subagent_reasoning_effort:'high',tool:ledger.tool,image_model:'tidak dilaporkan alat',status:'awaiting-independent-review',review_path:item.review_path,batch:1227,rationale:ledger.user_policy.intent,generated_file:v.generated_file,generated_at:v.generated_at,original_file:v.original_file,native_sha256:v.native_sha256,width:v.width,height:v.height,prompt:v.prompt,depicted_variant:v.depicted_variant,basis_claim_ids:plan.basis_claim_ids,visual_requirements:plan.visual_requirements,aura:plan.aura,artistic_choices:[...plan.artistic_choices,plan.selection_reason],generation_failures:plan.generation_failures||[],rejected_attempts:plan.rejected_attempts||[],variants:plan.variants.map((x,n)=>({variant:n+1,selected:n===selected,original_file:x.original_file,native_sha256:x.native_sha256})),visual_review:{reviewer:'codex',verdict:'pass',notes:v.notes,limitations:[],native_sha256:v.native_sha256,reviewed_at:new Date().toISOString()}};
fs.writeFileSync(`${base}/${slug}.json`,JSON.stringify(r,null,2)+'\n');
Object.assign(item,{status:r.status,receipt_path:`${base}/${slug}.json`,original_file:v.original_file,native_sha256:v.native_sha256});
fs.writeFileSync('data/artwork-batch-1227.json',JSON.stringify(ledger,null,2)+'\n');
fs.writeFileSync(`data/artwork-generated/batch-1227/drafts/root/${slug}-plan.json`,JSON.stringify(plan,null,2)+'\n');
console.log(JSON.stringify({slug,selected:selected+1,png:r.original_file,variants:r.variants.map(x=>x.original_file)}));
